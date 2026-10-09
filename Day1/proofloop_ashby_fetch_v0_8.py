#!/usr/bin/env python3
"""
ProofLoop Ashby Snapshot Fetcher v0.8

Fetches a public Ashby job-board snapshot and preserves the HTTP response body
as the raw source artifact for the Ashby branch of ProofLoop.

Default board:
    openai

Official public endpoint shape:
    https://api.ashbyhq.com/posting-api/job-board/{BOARD_NAME}
        ?includeCompensation=true

Design goals:
- standard library only
- no PowerShell JSON reserialization
- saves the response BODY bytes unchanged
- parses the bytes only to validate structure and count jobs
- refuses to overwrite an existing snapshot unless --overwrite is supplied
- writes atomically (temporary file -> final file)
- writes a sidecar fetch report containing provenance and SHA-256
- optional expected-count check, but no count is hard-coded because live jobs change

Example:
    python .\proofloop_ashby_fetch_v0_8.py

Example with explicit output:
    python .\proofloop_ashby_fetch_v0_8.py ^
        --output ".\openai_ashby_snapshot_2026-10-07T214500-0600.json"

The raw snapshot is intended to be immutable input for later normalization,
reconciliation, validation, and database enrichment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


VERSION = "ProofLoop Ashby Snapshot Fetcher v0.8"
DEFAULT_BOARD = "openai"
BASE_URL = "https://api.ashbyhq.com/posting-api/job-board"


def utc_timestamp_for_filename() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def utc_timestamp_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_url(board: str, include_compensation: bool) -> str:
    board_encoded = quote(board.strip(), safe="")
    compensation = "true" if include_compensation else "false"
    return (
        f"{BASE_URL}/{board_encoded}"
        f"?includeCompensation={compensation}"
    )


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_and_validate_json(raw: bytes) -> tuple[dict, list[str]]:
    """
    Parse the raw HTTP response without changing the bytes that will be saved.

    Returns:
        (payload, validation_issues)
    """
    issues: list[str] = []

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Response body is not valid UTF-8 JSON: {exc}"
        ) from exc

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Response body is not valid JSON: "
            f"{exc.msg} at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON root is not an object.")

    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise ValueError("JSON root does not contain a 'jobs' array.")

    api_version = payload.get("apiVersion")
    if api_version is None:
        issues.append("apiVersion is missing.")
    elif not isinstance(api_version, str):
        issues.append(
            f"apiVersion is {type(api_version).__name__}, expected string."
        )

    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    missing_ids = 0
    non_object_jobs = 0

    for job in jobs:
        if not isinstance(job, dict):
            non_object_jobs += 1
            continue

        job_id = job.get("id")
        if not isinstance(job_id, str) or not job_id.strip():
            missing_ids += 1
            continue

        if job_id in seen_ids:
            duplicate_ids.add(job_id)

        seen_ids.add(job_id)

    if non_object_jobs:
        issues.append(
            f"{non_object_jobs} job item(s) are not JSON objects."
        )

    if missing_ids:
        issues.append(
            f"{missing_ids} job object(s) have no nonblank 'id'."
        )

    if duplicate_ids:
        issues.append(
            f"{len(duplicate_ids)} duplicate job id(s) found."
        )

    return payload, issues


def fetch_bytes(
    url: str,
    timeout: float,
    retries: int,
) -> tuple[bytes, dict]:
    """
    Fetch raw response bytes.

    Only successful HTTP responses are returned.
    Retries apply to transient network failures and HTTP 5xx responses.
    """
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ProofLoop-Ashby-Snapshot-Fetcher/0.8",
            # Ask for identity transfer so the saved body is directly JSON,
            # not a compressed representation that would require decoding.
            "Accept-Encoding": "identity",
        },
        method="GET",
    )

    last_error: Exception | None = None
    attempts = retries + 1

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read()
                headers = {
                    key: value
                    for key, value in response.headers.items()
                }

                return raw, {
                    "http_status": response.status,
                    "response_url": response.geturl(),
                    "headers": headers,
                    "attempt": attempt,
                }

        except HTTPError as exc:
            last_error = exc
            retryable = 500 <= exc.code <= 599

            if not retryable or attempt >= attempts:
                raise RuntimeError(
                    f"HTTP {exc.code} while fetching {url}: "
                    f"{exc.reason}"
                ) from exc

        except URLError as exc:
            last_error = exc

            if attempt >= attempts:
                raise RuntimeError(
                    f"Network error while fetching {url}: {exc.reason}"
                ) from exc

        except TimeoutError as exc:
            last_error = exc

            if attempt >= attempts:
                raise RuntimeError(
                    f"Timed out while fetching {url}"
                ) from exc

        time.sleep(min(2 ** (attempt - 1), 8))

    raise RuntimeError(f"Fetch failed: {last_error}")


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )

    temp_path = Path(temp_name)

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, path)

    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, obj: dict) -> None:
    data = (
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    atomic_write_bytes(path, data)


def default_report_path(snapshot_path: Path) -> Path:
    return snapshot_path.with_name(
        snapshot_path.stem + ".fetch_report.json"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch and preserve a raw public Ashby job-board JSON snapshot."
        )
    )

    parser.add_argument(
        "--board",
        default=DEFAULT_BOARD,
        help="Ashby job-board name. Default: openai",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Raw snapshot output path. If omitted, a UTC timestamped "
            "filename is created."
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help=(
            "Fetch-report output path. If omitted, a sidecar report "
            "is created beside the snapshot."
        ),
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=None,
        help=(
            "Optional expected live job count. Omit for ordinary snapshots "
            "because the live count is allowed to change."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds. Default: 30",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retries after the first request. Default: 2",
    )
    parser.add_argument(
        "--no-compensation",
        action="store_true",
        help="Fetch without includeCompensation=true.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Intentionally replace an existing snapshot/report.",
    )

    args = parser.parse_args()

    if args.retries < 0:
        print("ERROR: --retries cannot be negative.", file=sys.stderr)
        return 2

    if args.timeout <= 0:
        print("ERROR: --timeout must be greater than zero.", file=sys.stderr)
        return 2

    include_compensation = not args.no_compensation

    if args.output is None:
        args.output = Path(
            f"{args.board}_ashby_snapshot_"
            f"{utc_timestamp_for_filename()}.json"
        )

    if args.report is None:
        args.report = default_report_path(args.output)

    for path, label in (
        (args.output, "snapshot"),
        (args.report, "report"),
    ):
        if path.exists() and not args.overwrite:
            print(
                f"ERROR: {label.capitalize()} already exists: {path}\n"
                "Refusing to overwrite an existing source artifact. "
                "Choose a new filename or use --overwrite intentionally.",
                file=sys.stderr,
            )
            return 1

    url = build_url(args.board, include_compensation)
    fetched_at_utc = utc_timestamp_iso()

    try:
        raw, http = fetch_bytes(
            url=url,
            timeout=args.timeout,
            retries=args.retries,
        )

        payload, issues = decode_and_validate_json(raw)

        jobs = payload["jobs"]
        job_count = len(jobs)

        if args.expected is not None and job_count != args.expected:
            issues.append(
                f"Job count {job_count} does not match "
                f"--expected {args.expected}."
            )

        if issues:
            print("ERROR: Snapshot validation failed:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            print(
                "No snapshot or report was written.",
                file=sys.stderr,
            )
            return 1

        digest = sha256_hex(raw)

        # Save EXACT response bytes after validation.
        atomic_write_bytes(args.output, raw)

        # Verify bytes on disk are exactly what was fetched.
        saved = args.output.read_bytes()
        if saved != raw:
            raise RuntimeError(
                "Post-write verification failed: saved snapshot bytes "
                "differ from fetched response bytes."
            )

        report = {
            "fetcher": VERSION,
            "fetched_at_utc": fetched_at_utc,
            "request": {
                "board": args.board,
                "url": url,
                "include_compensation": include_compensation,
                "timeout_seconds": args.timeout,
                "configured_retries": args.retries,
            },
            "response": {
                "http_status": http["http_status"],
                "response_url": http["response_url"],
                "attempt": http["attempt"],
                "content_type": http["headers"].get("Content-Type"),
                "content_length_header": http["headers"].get(
                    "Content-Length"
                ),
            },
            "snapshot": {
                "path": str(args.output),
                "bytes": len(raw),
                "sha256": digest,
                "api_version": payload.get("apiVersion"),
                "jobs_count": job_count,
                "expected_jobs_count": args.expected,
                "raw_response_bytes_preserved": True,
                "post_write_byte_verification": "PASS",
            },
            "validation": {
                "json_root_is_object": True,
                "jobs_is_array": True,
                "job_count": job_count,
                "issues": [],
                "result": "PASS",
            },
            "result": "PASS",
        }

        atomic_write_json(args.report, report)

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(VERSION)
    print(f"Board:              {args.board}")
    print(f"Request URL:        {url}")
    print(f"HTTP status:        {http['http_status']}")
    print(f"API version:        {payload.get('apiVersion')}")
    print(f"Jobs fetched:       {job_count}")
    if args.expected is not None:
        print(f"Expected jobs:      {args.expected}  [PASS]")
    print(f"Snapshot bytes:     {len(raw)}")
    print(f"SHA-256:            {digest}")
    print(f"Raw snapshot:       {args.output}")
    print(f"Fetch report:       {args.report}")
    print("Raw bytes preserved: YES")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
