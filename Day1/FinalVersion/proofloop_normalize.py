#!/usr/bin/env python3
r"""ProofLoop Ashby Stage 1: offline, source-preserving snapshot normalization.

Usage (PowerShell):
    python .\proofloop_normalize.py --snapshot '.\openai_ashby_snapshot.json' \
        --board openai --output-dir '.\runs\openai_2026-10-07'

Stdlib only; supports Python 3.10+. Does not access the network or modify the input.
The accepted output directory is never overwritten. Failing runs receive a
separate JSON failure report and do not publish partial normalized output.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

VERSION = "0.1.0"
PROVIDER = "ashby"
SOURCE_KEYS = (
    "id", "title", "department", "team", "employmentType", "location",
    "shouldDisplayCompensationOnJobPostings", "secondaryLocations", "publishedAt",
    "isListed", "isRemote", "workplaceType", "address", "jobUrl", "applyUrl",
    "descriptionHtml", "descriptionPlain", "compensation",
)
# (source_name, canonical_name, expected Python type); null is permitted except essentials.
FIELDS = (
    ("id", "id", str),
    ("title", "title", str),
    ("department", "department", str),
    ("team", "team", str),
    ("employmentType", "employment_type", str),
    ("location", "location", str),
    ("shouldDisplayCompensationOnJobPostings", "should_display_compensation", bool),
    ("secondaryLocations", "secondary_locations", list),
    ("publishedAt", "published_at", str),
    ("isListed", "is_listed", bool),
    ("isRemote", "is_remote", bool),
    ("workplaceType", "workplace_type", str),
    ("address", "address", dict),
    ("jobUrl", "job_url", str),
    ("applyUrl", "apply_url", str),
    ("descriptionHtml", "description_html", str),
    ("descriptionPlain", "description_plain", str),
    ("compensation", "compensation", dict),
)
REQUIRED = ("id", "title")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]


def source_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def typename(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return type(value).__name__
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def check_url(value: str, index: int, key: str) -> None:
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise ValueError(f"Job #{index}: {key} must be an HTTPS URL without embedded credentials")


def verify_nested(value: dict, index: int) -> None:
    if value.get("address") is not None:
        a = value["address"]
        if not isinstance(a, dict) or (a.get("postalAddress") is not None and not isinstance(a["postalAddress"], dict)):
            raise ValueError(f"Job #{index}: address.postalAddress must be an object or null")
    locs = value.get("secondaryLocations")
    if locs is not None:
        for j, loc in enumerate(locs, 1):
            if not isinstance(loc, dict):
                raise ValueError(f"Job #{index}: secondaryLocations[{j}] must be an object")
            if loc.get("address") is not None and not isinstance(loc["address"], dict):
                raise ValueError(f"Job #{index}: secondaryLocations[{j}].address must be an object")
    comp = value.get("compensation")
    if comp is not None:
        for list_name in ("compensationTiers", "summaryComponents"):
            items = comp.get(list_name)
            if items is not None:
                if not isinstance(items, list) or any(not isinstance(x, dict) for x in items):
                    raise ValueError(f"Job #{index}: compensation.{list_name} must be an array of objects")
                if list_name == "compensationTiers":
                    for j, tier in enumerate(items, 1):
                        cs = tier.get("components")
                        if cs is not None and (not isinstance(cs, list) or any(not isinstance(x, dict) for x in cs)):
                            raise ValueError(f"Job #{index}: compensationTiers[{j}].components must be an array of objects")


def inspect_snapshot(raw: bytes, *, board: str, expected_count: int | None = None, allow_empty: bool = False) -> tuple[list[dict], dict]:
    """Validate structural fidelity and return canonical+raw records with data audit."""
    try:
        payload = json.loads(raw.decode("utf-8-sig"), parse_constant=lambda constant: (_ for _ in ()).throw(ValueError(f"Non-JSON numeric constant {constant}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Snapshot is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Snapshot root must be an object")
    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise ValueError("Snapshot must contain a jobs array")
    if not jobs and not allow_empty:
        raise ValueError("Snapshot jobs array is empty; use --allow-empty only if this is intended")
    if expected_count is not None and len(jobs) != expected_count:
        raise ValueError(f"Job count {len(jobs)} does not match --expected-count {expected_count}")

    hashes = source_hash(raw)
    ids: set[str] = set()
    out: list[dict] = []
    keys = collections.Counter()
    field_presence = collections.Counter()
    field_nulls = collections.Counter()
    field_types: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    extras = collections.Counter()
    warning_counts = collections.Counter()
    flag_counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    nested_keys: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    secondary_count = 0
    compensation_tiers = 0
    compensation_components = 0

    for i, job in enumerate(jobs, 1):
        if not isinstance(job, dict):
            raise ValueError(f"Job #{i}: expected object, got {typename(job)}")
        canon: dict = {}
        keys.update(job.keys())
        for source, target, expected in FIELDS:
            if source not in job:
                warning_counts[f"missing_optional.{source}"] += 1
                canon[target] = None
                continue
            field_presence[source] += 1
            val = job[source]
            field_types[source][typename(val)] += 1
            if val is None:
                field_nulls[source] += 1
            elif not isinstance(val, expected):
                raise ValueError(f"Job #{i} ({job.get('id','?')}): {source} expected {expected.__name__} or null, got {typename(val)}")
            # Keep original nested structures and source strings; trim only display/search scalars.
            canon[target] = val.strip() if isinstance(val, str) and source in ("title", "team", "department", "location") else val
        for required in REQUIRED:
            if not isinstance(job.get(required), str) or not job[required].strip():
                raise ValueError(f"Job #{i}: missing or blank required field {required}")
        id_ = job["id"].strip()
        if id_ in ids:
            raise ValueError(f"Job #{i}: duplicate posting ID {id_!r}")
        ids.add(id_)
        if not re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}", id_):
            warning_counts["non_uuid_posting_id"] += 1
        for u in ("jobUrl", "applyUrl"):
            url = job.get(u)
            if isinstance(url, str) and url.strip():
                check_url(url, i, u)
            else:
                warning_counts[f"missing_url.{u}"] += 1
        if job.get("isListed") is False:
            warning_counts["unlisted_posting"] += 1
        if job.get("descriptionPlain") in (None, ""):
            warning_counts["missing_description_plain"] += 1
        verify_nested(job, i)

        for key in job:
            if key not in SOURCE_KEYS:
                extras[key] += 1
        for flag in ("isRemote", "workplaceType", "isListed", "shouldDisplayCompensationOnJobPostings", "employmentType"):
            flag_counts[flag][str(job.get(flag))] += 1
        for section in ("address", "compensation"):
            value = job.get(section)
            if isinstance(value, dict):
                nested_keys[section].update(value.keys())
        primary = job.get("address") or {}
        if isinstance(primary.get("postalAddress"), dict):
            nested_keys["primary_postal_address"].update(primary["postalAddress"].keys())
        locs = job.get("secondaryLocations") or []
        secondary_count += len(locs)
        for loc in locs:
            nested_keys["secondary_location"].update(loc.keys())
            addr = loc.get("address") or {}
            if isinstance(addr, dict):
                nested_keys["secondary_address"].update(addr.keys())
        comp = job.get("compensation") or {}
        tiers = comp.get("compensationTiers") or []
        summaries = comp.get("summaryComponents") or []
        compensation_tiers += len(tiers)
        for tier in tiers:
            nested_keys["compensation_tier"].update(tier.keys())
            cs = tier.get("components") or []
            compensation_components += len(cs)
            for c in cs:
                nested_keys["compensation_component"].update(c.keys())
        for c in summaries:
            nested_keys["compensation_summary_component"].update(c.keys())

        out.append({
            "provenance": {"provider": PROVIDER, "board": board, "snapshot_sha256": hashes, "source_index": i},
            "canonical": canon,
            "raw": job,  # lossless source-field preservation, even when API schema evolves
        })

    audit = {
        "api_version": payload.get("apiVersion"),
        "root_fields": sorted(payload),
        "record_count": len(out),
        "unique_posting_ids": len(ids),
        "source_sha256": hashes,
        "source_bytes": len(raw),
        "source_fields": dict(sorted(keys.items())),
        "unrecognized_source_fields": dict(sorted(extras.items())),
        "field_presence": dict(sorted(field_presence.items())),
        "field_null_count": dict(sorted(field_nulls.items())),
        "field_types": {k: dict(sorted(v.items())) for k, v in sorted(field_types.items())},
        "flag_distributions": {k: dict(sorted(v.items())) for k, v in sorted(flag_counts.items())},
        "nested_field_occurrences": {k: dict(sorted(v.items())) for k, v in sorted(nested_keys.items())},
        "secondary_location_count": secondary_count,
        "compensation_tier_count": compensation_tiers,
        "compensation_component_count": compensation_components,
        "warning_counts": dict(sorted(warning_counts.items())),
    }
    return out, audit


def report_markdown(report: dict) -> str:
    audit = report["audit"]
    summary = [
        "# ProofLoop Ashby — Normalization Report", "",
        f"- **Status:** {report['status']}",
        f"- **Run:** `{report['run_id']}`", f"- **Generated (UTC):** {report['generated_at_utc']}",
        f"- **Source:** `{report['source_file']}`", f"- **Board:** `{report['board']}`",
        f"- **Source SHA-256:** `{audit['source_sha256']}`", "",
        "## Structural results", "",
        f"- API version: `{audit['api_version']}`",
        f"- Parsed postings: **{audit['record_count']}**",
        f"- Unique posting IDs: **{audit['unique_posting_ids']}**",
        f"- Secondary-location records: **{audit['secondary_location_count']}**",
        f"- Compensation tiers: **{audit['compensation_tier_count']}**",
        f"- Tier components: **{audit['compensation_component_count']}**",
        f"- JSONL SHA-256: `{report['normalized_sha256']}`", "",
        "## Unexpected source fields", "",
    ]
    if audit["unrecognized_source_fields"]:
        summary.extend(f"- `{k}`: {v} postings" for k, v in audit["unrecognized_source_fields"].items())
    else:
        summary.append("None. Unknown future fields would be preserved in `raw` and reported here.")
    summary.extend(["", "## Warnings and missing information", ""])
    if audit["warning_counts"]:
        summary.extend(f"- `{k}`: {v}" for k, v in audit["warning_counts"].items())
    else:
        summary.append("No warnings.")
    for name in ("isRemote", "workplaceType", "isListed", "shouldDisplayCompensationOnJobPostings"):
        summary.extend(["", f"## {name}", ""])
        summary.extend(f"- `{k}`: {v}" for k,v in audit["flag_distributions"].get(name,{}).items())
    summary.extend(["", "## Validation contract", "", "Required IDs and titles are nonblank; IDs are unique; included URLs are HTTPS; known fields have expected types; nested location/compensation arrays are structurally valid. Source records remain verbatim in `raw`. Nullable fields remain null and are not interpreted as negatives.", "", "**Not checked:** current job availability, whether a hybrid role permits remote residence, semantic truth of job descriptions, compensation eligibility, or candidate qualifications.", ""])
    return "\n".join(summary)


def write_failure(destination: Path, *, run_id: str, error: str, board: str, source: Path) -> Path | None:
    """Best-effort failure sidecar. Never clobber an accepted output directory."""
    fail = destination.parent / f"{destination.name}.FAILED.{run_id}.json"
    payload = {"status": "FAIL", "run_id": run_id, "generated_at_utc": now_utc(), "stage": "normalize", "source_file": source.name, "board": board, "error": error, "program_version": VERSION}
    try:
        fail.parent.mkdir(parents=True, exist_ok=True)
        with fail.open("x", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return fail
    except OSError:
        return None


def execute(snapshot: Path, destination: Path, *, board: str, expected_count: int | None = None, allow_empty: bool = False) -> dict:
    """Atomically publish a complete, new output directory or leave it absent."""
    if not board or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", board):
        raise ValueError("--board must be an Ashby board slug (letters, digits, underscores, hyphens)")
    if expected_count is not None and expected_count < 0:
        raise ValueError("--expected-count must be nonnegative")
    if not snapshot.is_file():
        raise ValueError(f"Snapshot does not exist: {snapshot}")
    if destination.exists():
        raise ValueError(f"Output directory already exists (refusing overwrite): {destination}")
    if destination.resolve() == snapshot.resolve() or destination == destination.parent:
        raise ValueError("Unsafe output location")
    raw = snapshot.read_bytes()
    jobs, audit = inspect_snapshot(raw, board=board, expected_count=expected_count, allow_empty=allow_empty)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent))
    try:
        normalized = stage / "normalized" / "jobs.jsonl"
        normalized.parent.mkdir(parents=True, exist_ok=True)
        h = hashlib.sha256()
        with normalized.open("wb") as out:
            for row in jobs:
                line = (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
                out.write(line)
                h.update(line)
        report = {
            "stage": "normalize", "status": "PASS", "program_version": VERSION,
            "run_id": safe_run_id(), "generated_at_utc": now_utc(), "board": board,
            "source_file": snapshot.name, "normalized_file": "normalized/jobs.jsonl",
            "normalized_bytes": normalized.stat().st_size, "normalized_sha256": h.hexdigest(),
            "validation_checks": {"root_jobs_array": True, "record_structures_valid": True, "unique_ids": True, "nested_types_valid": True, "expected_count_ok": True, "accepted_output_unmodified": True},
            "audit": audit,
        }
        report_dir = stage / "reports"
        report_dir.mkdir()
        (report_dir / "normalization_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        (report_dir / "normalization_report.md").write_text(report_markdown(report), encoding="utf-8")
        # Direct rename publishes the *entire* directory, not partial individual files.
        if destination.exists():
            raise ValueError(f"Destination appeared during processing: {destination}")
        stage.rename(destination)
        return report
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--snapshot", required=True, type=Path, help="Frozen Ashby JSON response; read-only")
    parser.add_argument("--board", required=True, help="Ashby public job-board slug, e.g. openai")
    parser.add_argument("--output-dir", required=True, type=Path, help="New run directory; never overwritten")
    parser.add_argument("--expected-count", type=int, help="Optional historical fixture count, not a live-board assumption")
    parser.add_argument("--allow-empty", action="store_true", help="Explicitly permit a board with zero jobs")
    args = parser.parse_args(argv)
    run_id = safe_run_id()
    try:
        result = execute(args.snapshot, args.output_dir, board=args.board, expected_count=args.expected_count, allow_empty=args.allow_empty)
        print(f"PASS: normalized {result['audit']['record_count']} jobs")
        print(f"Output: {args.output_dir}")
        print(f"Source SHA-256: {result['audit']['source_sha256']}")
        print("Reports: reports/normalization_report.json and .md")
        return 0
    except (ValueError, OSError, TypeError, OverflowError) as exc:
        path = write_failure(args.output_dir, run_id=run_id, error=str(exc), board=args.board, source=args.snapshot)
        print(f"FAIL: {exc}", file=sys.stderr)
        if path:
            print(f"Failure report: {path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
