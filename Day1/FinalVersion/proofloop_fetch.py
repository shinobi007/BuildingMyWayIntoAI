#!/usr/bin/env python3
r"""ProofLoop Ashby Search | Stage 2: public Ashby snapshot acquisition.

Python 3.10+, standard library only. Requires proofloop_normalize.py from Stage 1
beside this file. The fetcher preserves raw API response bytes, verifies against
Stage 1's structural contract, and publishes a NEW directory containing the
snapshot plus JSON/Markdown acquisition reports. Never overwrites output.

Examples (PowerShell, from Day1\FinalVersion):
 python .\proofloop_fetch.py --board openai --source-file '..\openai_ashby_snapshot_2026-10-07.json' --output-dir '.\runs\stage2_frozen_validation' --expected-count 815
 python .\proofloop_fetch.py --board openai --output-dir '.\runs\stage2_live_001'
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

try:
    from proofloop_normalize import inspect_snapshot
except ImportError as exc:
    raise SystemExit("Stage 1 proofloop_normalize.py must be next to proofloop_fetch.py") from exc

VERSION = "0.2.0"
BASE = "https://api.ashbyhq.com/posting-api/job-board"
DEFAULT_MAX_BYTES = 128 * 1024 * 1024
RETRY_HTTP = {429, 500, 502, 503, 504}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]


def validate_board(board: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", board):
        raise ValueError("--board must be a slug containing only letters, digits, '_' or '-'")
    return board


def public_endpoint(board: str, include_compensation: bool = True) -> str:
    return f"{BASE}/{quote(validate_board(board), safe='')}?includeCompensation={'true' if include_compensation else 'false'}"


def check_final_url(url: str) -> None:
    parts = urlsplit(url)
    if (parts.scheme != "https" or parts.hostname != "api.ashbyhq.com"
            or parts.username or parts.password or parts.port not in (None, 443)
            or not parts.path.startswith("/posting-api/job-board/")):
        raise ValueError("Response redirected outside Ashby's public posting API")


def _json_media_type(headers: object) -> bool:
    # urllib's HTTPMessage supplies .get(); simple test doubles do too.
    value = (headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
    return value in ("application/json", "application/problem+json") or value.endswith("+json")


def _bounded_read(response: object, max_bytes: int) -> bytes:
    raw = response.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError(f"Response exceeds maximum allowed size ({max_bytes} bytes)")
    return raw


def fetch_live(board: str, *, include_compensation: bool = True,
               timeout: float = 25, retries: int = 2,
               max_bytes: int = DEFAULT_MAX_BYTES,
               sleep=time.sleep) -> tuple[bytes, dict]:
    """Fetch exact response BODY bytes; transient failures only are retried."""
    url = public_endpoint(board, include_compensation)
    request = Request(url, headers={
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "User-Agent": "ProofLoop-Ashby-Search/0.2 (+public job board research)",
    }, method="GET")
    errors: list[dict] = []
    for attempt in range(1, retries + 2):
        try:
            with urlopen(request, timeout=timeout) as response:
                final_url = response.geturl()
                check_final_url(final_url)
                status = response.status
                if status != 200:
                    raise ValueError(f"Unexpected HTTP status {status}")
                if not _json_media_type(response.headers):
                    raise ValueError("Response Content-Type is not JSON")
                encoding = (response.headers.get("Content-Encoding") or "identity").lower()
                if encoding != "identity":
                    raise ValueError(f"Unexpected Content-Encoding: {encoding}")
                raw = _bounded_read(response, max_bytes)
                return raw, {
                    "endpoint": url, "final_url": final_url, "http_status": status,
                    "content_type": response.headers.get("Content-Type"),
                    "content_encoding": encoding, "attempts": attempt,
                    "transient_failures": errors,
                }
        except HTTPError as exc:
            retryable = exc.code in RETRY_HTTP
            errors.append({"attempt": attempt, "http_status": exc.code, "retryable": retryable})
            if not retryable or attempt > retries:
                raise RuntimeError(f"HTTP {exc.code} while fetching public Ashby board") from exc
        except (URLError, TimeoutError, ConnectionError) as exc:
            errors.append({"attempt": attempt, "network_error": type(exc).__name__, "retryable": True})
            if attempt > retries:
                raise RuntimeError(f"Network retrieval failed after {attempt} attempt(s): {type(exc).__name__}") from exc
        sleep(min(2 ** (attempt - 1), 5))
    raise RuntimeError("Fetch failed without response")


def markdown_report(report: dict) -> str:
    a = report["snapshot_audit"]
    req = report["acquisition"]
    return "\n".join([
        "# ProofLoop Ashby — Acquisition Report", "",
        f"- **Status:** {report['status']}",
        f"- **Run ID:** `{report['run_id']}`",
        f"- **Generated UTC:** {report['generated_at_utc']}",
        f"- **Provider/board:** Ashby / `{report['board']}`",
        f"- **Acquisition:** `{report['mode']}`",
        f"- **API endpoint:** `{report['endpoint'] or 'not contacted (offline mode)'}`", "",
        "## Source artifact", "",
        f"- Saved: `{report['snapshot_file']}`",
        f"- Exact bytes: {report['snapshot_bytes']:,}",
        f"- SHA-256: `{report['snapshot_sha256']}`",
        f"- Postings: **{a['record_count']}** (unique IDs: **{a['unique_posting_ids']}**)",
        f"- Secondary locations: {a['secondary_location_count']}",
        f"- Compensation tiers: {a['compensation_tier_count']}",
        "", "## HTTP / original source", "",
        f"- HTTP status: `{req.get('http_status', 'N/A (frozen file)')}`",
        f"- Fetch attempts: {req.get('attempts', 0)}",
        f"- Final URL: `{req.get('final_url', 'N/A (frozen file)')}`",
        f"- Compensation requested: `{report['include_compensation'] if report['include_compensation'] is not None else 'not established for offline source'}`",
        "", "## Verification", "",
        "- The saved file is byte-for-byte equal to the accepted input bytes.",
        "- The complete snapshot passes the same structural checks as Stage 1.",
        "- This run does not change any existing output directory or input file.",
        "- Unexpected fields are retained; future changes are inventoried during normalization.",
        "", "**Not verified:** whether every posting remains open, candidate qualifications, actual work-location eligibility, or employer authorization to use private Ashby endpoints.", "",
    ])


def _failure_report(destination: Path, *, rid: str, board: str, mode: str, message: str) -> Path | None:
    path = destination.parent / f"{destination.name}.FAILED.{rid}.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as f:
            json.dump({"stage": "fetch", "status": "FAIL", "program_version": VERSION,
                       "run_id": rid, "generated_at_utc": now_utc(), "board": board,
                       "mode": mode, "error": message}, f, indent=2)
            f.write("\n")
        return path
    except OSError:
        return None


def execute(board: str, destination: Path, *, source_file: Path | None = None,
            include_compensation: bool = True, expected_count: int | None = None,
            allow_empty: bool = False, timeout: float = 25, retries: int = 2,
            max_bytes: int = DEFAULT_MAX_BYTES) -> dict:
    """Publish one newly created directory containing snapshot and both reports."""
    validate_board(board)
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Output directory already exists (will not overwrite): {destination}")
    if expected_count is not None and expected_count < 0:
        raise ValueError("--expected-count cannot be negative")
    if retries < 0 or retries > 5 or not (0 < timeout <= 120) or not (1024 <= max_bytes <= 512 * 1024 * 1024):
        raise ValueError("Invalid retries, timeout, or byte limit")
    endpoint = public_endpoint(board, include_compensation)
    if source_file is not None:
        if not source_file.is_file():
            raise ValueError(f"Frozen snapshot not found: {source_file}")
        if source_file.stat().st_size > max_bytes:
            raise ValueError("Frozen snapshot exceeds byte limit")
        raw = source_file.read_bytes()
        acquisition = {"source_file": source_file.name, "mode": "frozen_file", "attempts": 0}
        mode = "frozen_file"
    else:
        raw, acquisition = fetch_live(board, include_compensation=include_compensation,
                                      timeout=timeout, retries=retries, max_bytes=max_bytes)
        mode = "live_api"
    rows, audit = inspect_snapshot(raw, board=board, expected_count=expected_count, allow_empty=allow_empty)
    del rows  # Acquisition stage checks completeness; normalized rows are Stage 1's product.
    sha = hashlib.sha256(raw).hexdigest()
    rid = run_id()
    report = {
        "stage": "fetch", "status": "PASS", "program_version": VERSION,
        "run_id": rid, "generated_at_utc": now_utc(), "mode": mode,
        "provider": "ashby", "board": board, "endpoint": endpoint if mode == "live_api" else None,
        "expected_public_endpoint": endpoint,
        "include_compensation": include_compensation if mode == "live_api" else None,
        "snapshot_file": "raw/ashby_snapshot.json", "snapshot_bytes": len(raw),
        "snapshot_sha256": sha, "acquisition": acquisition,
        "validation_checks": {
            "stage1_structural_contract": True, "unique_ids": True,
            "expected_count_if_supplied": True, "source_body_preserved": True,
            "published_as_new_bundle": True,
        },
        "snapshot_audit": {
            "api_version": audit["api_version"],
            "record_count": audit["record_count"],
            "unique_posting_ids": audit["unique_posting_ids"],
            "secondary_location_count": audit["secondary_location_count"],
            "compensation_tier_count": audit["compensation_tier_count"],
            "unrecognized_source_fields": audit["unrecognized_source_fields"],
            "warning_counts": audit["warning_counts"],
        },
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent))
    try:
        (staging / "raw").mkdir()
        (staging / "reports").mkdir()
        saved = staging / "raw" / "ashby_snapshot.json"
        saved.write_bytes(raw)
        if hashlib.sha256(saved.read_bytes()).hexdigest() != sha:
            raise OSError("Written snapshot digest mismatch")
        (staging / "reports" / "fetch_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (staging / "reports" / "fetch_report.md").write_text(markdown_report(report), encoding="utf-8")
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"Output appeared during staging: {destination}")
        staging.rename(destination)
        return report
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--board", default="openai", help="Ashby public job-board slug")
    p.add_argument("--output-dir", required=True, type=Path, help="New directory; never overwrites")
    p.add_argument("--source-file", type=Path, help="Optional offline frozen source; otherwise fetch from API")
    p.add_argument("--expected-count", type=int, help="Optional only for known historical snapshots")
    p.add_argument("--allow-empty", action="store_true", help="Explicitly permit zero jobs")
    p.add_argument("--no-compensation", action="store_true", help="Do not request compensation in LIVE mode")
    p.add_argument("--timeout", type=float, default=25, help="Network timeout in seconds, default 25")
    p.add_argument("--retries", type=int, default=2, help="Retries for transient failures, default 2")
    p.add_argument("--max-mib", type=int, default=128, help="Max source size in MiB, default 128")
    args = p.parse_args(argv)
    rid = run_id()
    try:
        result = execute(args.board, args.output_dir, source_file=args.source_file,
                         include_compensation=not args.no_compensation,
                         expected_count=args.expected_count, allow_empty=args.allow_empty,
                         timeout=args.timeout, retries=args.retries,
                         max_bytes=args.max_mib * 1024 * 1024)
        print(f"PASS: acquired and structurally checked {result['snapshot_audit']['record_count']} jobs")
        print(f"Mode: {result['mode']}")
        print(f"Output: {args.output_dir}")
        print(f"Source SHA-256: {result['snapshot_sha256']}")
        print("Reports: reports/fetch_report.json and .md")
        return 0
    except (ValueError, OSError, RuntimeError, TypeError) as exc:
        fail = _failure_report(args.output_dir, rid=rid, board=args.board,
                               mode="frozen_file" if args.source_file else "live_api", message=str(exc))
        print(f"FAIL: {exc}", file=sys.stderr)
        if fail:
            print(f"Failure report: {fail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
