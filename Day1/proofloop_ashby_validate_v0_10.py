#!/usr/bin/env python3
"""
ProofLoop Ashby API Artifact Validator v0.10

Validates the frozen Ashby/OpenAI API branch and its reconciliation artifacts.

This is validation of REAL artifacts, not synthetic testing.

Checks include:
- raw API snapshot structure/count
- normalized API JSONL structure/count/uniqueness
- field-for-field preservation from raw API -> normalized JSONL
- Ashby UUID consistency across id/job/apply URLs
- HTML-derived inventory count and Ashby IDs
- independent set reconciliation
- reconciliation report arithmetic and contents
- cosmetic-vs-substantive title/team change classification
- reconciler syntax
- full deterministic regeneration in a temporary directory
- regenerated normalized JSONL equality
- regenerated reconciliation report semantic equality

Produces:
    proofloop_ashby_validation_report.json
"""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


NORMALIZED_FIELDS = (
    "source_index",
    "source_snapshot",
    "ashby_id",
    "title",
    "department",
    "team",
    "employment_type",
    "primary_location",
    "secondary_locations",
    "published_at",
    "is_listed",
    "is_remote",
    "workplace_type",
    "address",
    "job_url",
    "apply_url",
    "description_plain",
    "description_html",
    "compensation",
)


def normalize_text(value):
    if value is None:
        return None
    return re.sub(r"\s+", " ", str(value)).strip()


def ashby_id_from_url(url: str | None) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0].lower() == "openai":
        return parts[1]
    return ""


def add_check(checks, name, passed, detail):
    checks.append({
        "name": name,
        "passed": bool(passed),
        "detail": str(detail),
    })


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, 1):
            line = raw.strip()
            if not line:
                raise ValueError(f"Blank JSONL line at {line_number}")
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: "
                    f"{exc.msg} column {exc.colno}"
                ) from exc
            if not isinstance(obj, dict):
                raise ValueError(
                    f"JSONL line {line_number} is not an object"
                )
            rows.append(obj)
    return rows


def normalized_from_raw(job: dict, index: int, snapshot_name: str):
    secondary = job.get("secondaryLocations")
    if not isinstance(secondary, list):
        secondary = []

    normalized_secondary = []
    for item in secondary:
        if isinstance(item, dict):
            normalized_secondary.append({
                "location": item.get("location"),
                "address": item.get("address"),
            })

    apply_url = job.get("applyUrl")
    job_url = job.get("jobUrl")

    return {
        "source_index": index,
        "source_snapshot": snapshot_name,
        "ashby_id": (
            job.get("id")
            or ashby_id_from_url(apply_url)
            or ashby_id_from_url(job_url)
        ),
        "title": job.get("title"),
        "department": job.get("department"),
        "team": job.get("team"),
        "employment_type": job.get("employmentType"),
        "primary_location": job.get("location"),
        "secondary_locations": normalized_secondary,
        "published_at": job.get("publishedAt"),
        "is_listed": job.get("isListed"),
        "is_remote": job.get("isRemote"),
        "workplace_type": job.get("workplaceType"),
        "address": job.get("address"),
        "job_url": job_url,
        "apply_url": apply_url,
        "description_plain": job.get("descriptionPlain"),
        "description_html": job.get("descriptionHtml"),
        "compensation": job.get("compensation"),
    }


def independent_reconciliation(html_rows, api_rows):
    html_by_id = {}
    api_by_id = {}

    html_missing = []
    api_missing = []

    for row in html_rows:
        aid = ashby_id_from_url(row.get("apply_url"))
        if aid:
            html_by_id[aid] = row
        else:
            html_missing.append(row)

    for row in api_rows:
        aid = row.get("ashby_id") or ashby_id_from_url(
            row.get("apply_url")
        )
        if aid:
            api_by_id[aid] = row
        else:
            api_missing.append(row)

    html_ids = set(html_by_id)
    api_ids = set(api_by_id)

    matched = html_ids & api_ids
    html_only = html_ids - api_ids
    api_only = api_ids - html_ids

    cosmetic = set()
    substantive = set()

    for aid in matched:
        h = html_by_id[aid]
        a = api_by_id[aid]

        raw_diff = False
        semantic_diff = False

        for field in ("title", "team"):
            hv = h.get(field)
            av = a.get(field)

            if hv != av:
                raw_diff = True

            if normalize_text(hv) != normalize_text(av):
                semantic_diff = True

        if semantic_diff:
            substantive.add(aid)
        elif raw_diff:
            cosmetic.add(aid)

    return {
        "html_by_id": html_by_id,
        "api_by_id": api_by_id,
        "matched": matched,
        "html_only": html_only,
        "api_only": api_only,
        "cosmetic": cosmetic,
        "substantive": substantive,
        "html_missing": html_missing,
        "api_missing": api_missing,
    }


def semantic_report_core(report):
    """Ignore provenance path spelling while comparing report meaning."""
    return {
        "summary": report.get("summary"),
        "html_only": report.get("html_only"),
        "api_only": report.get("api_only"),
        "matched_cosmetic_only_changes":
            report.get("matched_cosmetic_only_changes"),
        "matched_substantive_changes":
            report.get("matched_substantive_changes"),
        "html_records_without_ashby_id":
            report.get("html_records_without_ashby_id"),
        "api_records_without_ashby_id":
            report.get("api_records_without_ashby_id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ProofLoop's Ashby API artifacts."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root directory.",
    )
    parser.add_argument(
        "--snapshot",
        default="openai_ashby_snapshot_2026-10-07.json",
    )
    parser.add_argument(
        "--html-jsonl",
        default="openai_roles.jsonl",
    )
    parser.add_argument(
        "--api-jsonl",
        default="openai_ashby_roles.jsonl",
    )
    parser.add_argument(
        "--reconciliation-report",
        default="openai_ashby_reconciliation_report_v0_9_1.json",
    )
    parser.add_argument(
        "--reconciler",
        default="proofloop_ashby_reconcile_v0_9_1.py",
    )
    parser.add_argument(
        "--expected-api",
        type=int,
        default=815,
    )
    parser.add_argument(
        "--expected-html",
        type=int,
        default=817,
    )
    parser.add_argument(
        "--report",
        default="proofloop_ashby_validation_report.json",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    snapshot_path = root / args.snapshot
    html_path = root / args.html_jsonl
    api_jsonl_path = root / args.api_jsonl
    reconciliation_path = root / args.reconciliation_report
    reconciler_path = root / args.reconciler
    output_report = root / args.report

    checks = []
    metrics = {}

    paths = {
        "snapshot_exists": snapshot_path,
        "html_jsonl_exists": html_path,
        "api_jsonl_exists": api_jsonl_path,
        "reconciliation_report_exists": reconciliation_path,
        "reconciler_exists": reconciler_path,
    }

    for name, path in paths.items():
        add_check(checks, name, path.is_file(), path)

    if not all(path.is_file() for path in paths.values()):
        result = "FAIL"
        report = {
            "validator": "ProofLoop Ashby API Artifact Validator v0.10",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "checks": len(checks),
                "passed": sum(c["passed"] for c in checks),
                "failed": sum(not c["passed"] for c in checks),
                "result": result,
            },
            "checks": checks,
        }
        output_report.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        print("RESULT: FAIL - required artifact missing")
        return 1

    try:
        py_compile.compile(str(reconciler_path), doraise=True)
        add_check(
            checks,
            "reconciler_syntax",
            True,
            "Python syntax compiled successfully.",
        )
    except Exception as exc:
        add_check(checks, "reconciler_syntax", False, exc)

    # Load all real artifacts.
    try:
        snapshot = load_json(snapshot_path)
        raw_jobs = snapshot.get("jobs") if isinstance(snapshot, dict) else None
        ok = isinstance(raw_jobs, list)
        add_check(
            checks,
            "snapshot_jobs_array",
            ok,
            f"jobs type={type(raw_jobs).__name__}",
        )
        if not ok:
            raw_jobs = []
    except Exception as exc:
        raw_jobs = []
        add_check(checks, "snapshot_loads", False, exc)
    else:
        add_check(
            checks,
            "snapshot_loads",
            True,
            "Raw API snapshot parsed as JSON.",
        )

    try:
        html_rows = load_jsonl(html_path)
        add_check(
            checks,
            "html_jsonl_loads",
            True,
            f"Loaded {len(html_rows)} HTML-derived rows.",
        )
    except Exception as exc:
        html_rows = []
        add_check(checks, "html_jsonl_loads", False, exc)

    try:
        api_rows = load_jsonl(api_jsonl_path)
        add_check(
            checks,
            "api_jsonl_loads",
            True,
            f"Loaded {len(api_rows)} normalized API rows.",
        )
    except Exception as exc:
        api_rows = []
        add_check(checks, "api_jsonl_loads", False, exc)

    try:
        reconciliation = load_json(reconciliation_path)
        add_check(
            checks,
            "reconciliation_report_loads",
            isinstance(reconciliation, dict),
            "Reconciliation report parsed as JSON object.",
        )
    except Exception as exc:
        reconciliation = {}
        add_check(checks, "reconciliation_report_loads", False, exc)

    metrics["raw_api_jobs"] = len(raw_jobs)
    metrics["html_rows"] = len(html_rows)
    metrics["normalized_api_rows"] = len(api_rows)

    add_check(
        checks,
        "snapshot_expected_count",
        len(raw_jobs) == args.expected_api,
        f"Found {len(raw_jobs)}; expected {args.expected_api}.",
    )
    add_check(
        checks,
        "api_jsonl_expected_count",
        len(api_rows) == args.expected_api,
        f"Found {len(api_rows)}; expected {args.expected_api}.",
    )
    add_check(
        checks,
        "html_jsonl_expected_count",
        len(html_rows) == args.expected_html,
        f"Found {len(html_rows)}; expected {args.expected_html}.",
    )

    field_ok = all(
        tuple(row.keys()) == NORMALIZED_FIELDS
        for row in api_rows
    )
    add_check(
        checks,
        "api_jsonl_fields_exact",
        field_ok,
        "Every normalized API row uses the expected ordered field set.",
    )

    indexes = [row.get("source_index") for row in api_rows]
    add_check(
        checks,
        "api_source_indexes_sequential",
        indexes == list(range(1, len(api_rows) + 1)),
        f"Expected source_index 1..{len(api_rows)}.",
    )

    snapshot_names = {row.get("source_snapshot") for row in api_rows}
    add_check(
        checks,
        "api_source_snapshot_provenance",
        snapshot_names == {snapshot_path.name},
        f"Observed source_snapshot values: {sorted(str(x) for x in snapshot_names)}",
    )

    ids = [row.get("ashby_id") for row in api_rows]
    nonblank_ids = all(isinstance(x, str) and x.strip() for x in ids)
    unique_ids = len(set(ids)) == len(ids)
    add_check(
        checks,
        "api_ashby_ids_present",
        nonblank_ids,
        f"Nonblank IDs: {sum(bool(x) for x in ids)}/{len(ids)}.",
    )
    add_check(
        checks,
        "api_ashby_ids_unique",
        unique_ids,
        f"Unique IDs: {len(set(ids))}/{len(ids)}.",
    )

    apply_urls = [row.get("apply_url") for row in api_rows]
    job_urls = [row.get("job_url") for row in api_rows]
    add_check(
        checks,
        "api_apply_urls_unique",
        len(set(apply_urls)) == len(apply_urls),
        f"Unique apply URLs: {len(set(apply_urls))}/{len(apply_urls)}.",
    )
    add_check(
        checks,
        "api_job_urls_unique",
        len(set(job_urls)) == len(job_urls),
        f"Unique job URLs: {len(set(job_urls))}/{len(job_urls)}.",
    )

    url_id_consistency = all(
        row.get("ashby_id") == ashby_id_from_url(row.get("apply_url"))
        and row.get("ashby_id") == ashby_id_from_url(row.get("job_url"))
        for row in api_rows
    )
    add_check(
        checks,
        "api_url_ids_match_ashby_id",
        url_id_consistency,
        "Ashby ID matches both job_url and apply_url for every row.",
    )

    # Field-for-field preservation from raw snapshot to normalized JSONL.
    expected_rows = [
        normalized_from_raw(job, i, snapshot_path.name)
        for i, job in enumerate(raw_jobs, 1)
    ]
    add_check(
        checks,
        "normalized_api_matches_raw_snapshot_row_for_row",
        api_rows == expected_rows,
        (
            "Normalized API JSONL exactly matches independently normalized "
            "raw snapshot data."
        ),
    )

    rec = independent_reconciliation(html_rows, api_rows)
    metrics.update({
        "matched": len(rec["matched"]),
        "html_only": len(rec["html_only"]),
        "api_only": len(rec["api_only"]),
        "cosmetic_changes": len(rec["cosmetic"]),
        "substantive_changes": len(rec["substantive"]),
        "html_missing_ashby_id": len(rec["html_missing"]),
        "api_missing_ashby_id": len(rec["api_missing"]),
    })

    add_check(
        checks,
        "independent_reconciliation_arithmetic_html",
        len(rec["matched"]) + len(rec["html_only"]) == len(html_rows),
        (
            f"matched {len(rec['matched'])} + html_only "
            f"{len(rec['html_only'])} = {len(html_rows)}."
        ),
    )
    add_check(
        checks,
        "independent_reconciliation_arithmetic_api",
        len(rec["matched"]) + len(rec["api_only"]) == len(api_rows),
        (
            f"matched {len(rec['matched'])} + api_only "
            f"{len(rec['api_only'])} = {len(api_rows)}."
        ),
    )
    add_check(
        checks,
        "all_html_records_have_ashby_id",
        len(rec["html_missing"]) == 0,
        f"Missing HTML Ashby IDs: {len(rec['html_missing'])}.",
    )
    add_check(
        checks,
        "all_api_records_have_ashby_id",
        len(rec["api_missing"]) == 0,
        f"Missing API Ashby IDs: {len(rec['api_missing'])}.",
    )

    summary = reconciliation.get("summary", {})
    expected_summary = {
        "html_roles": len(html_rows),
        "api_roles": len(api_rows),
        "matched": len(rec["matched"]),
        "html_only": len(rec["html_only"]),
        "api_only": len(rec["api_only"]),
        "matched_cosmetic_only_changes": len(rec["cosmetic"]),
        "matched_substantive_title_or_team_changes":
            len(rec["substantive"]),
        "html_records_without_ashby_id": len(rec["html_missing"]),
        "api_records_without_ashby_id": len(rec["api_missing"]),
    }
    add_check(
        checks,
        "reconciliation_summary_matches_independent_calculation",
        summary == expected_summary,
        f"Report summary: {summary}",
    )

    report_html_only_ids = {
        item.get("ashby_id")
        for item in reconciliation.get("html_only", [])
    }
    report_api_only_ids = {
        item.get("ashby_id")
        for item in reconciliation.get("api_only", [])
    }
    report_cosmetic_ids = {
        item.get("ashby_id")
        for item in reconciliation.get(
            "matched_cosmetic_only_changes", []
        )
    }
    report_substantive_ids = {
        item.get("ashby_id")
        for item in reconciliation.get(
            "matched_substantive_changes", []
        )
    }

    add_check(
        checks,
        "report_html_only_ids_correct",
        report_html_only_ids == rec["html_only"],
        f"Report HTML-only IDs: {len(report_html_only_ids)}.",
    )
    add_check(
        checks,
        "report_api_only_ids_correct",
        report_api_only_ids == rec["api_only"],
        f"Report API-only IDs: {len(report_api_only_ids)}.",
    )
    add_check(
        checks,
        "report_cosmetic_change_ids_correct",
        report_cosmetic_ids == rec["cosmetic"],
        f"Report cosmetic IDs: {len(report_cosmetic_ids)}.",
    )
    add_check(
        checks,
        "report_substantive_change_ids_correct",
        report_substantive_ids == rec["substantive"],
        f"Report substantive IDs: {len(report_substantive_ids)}.",
    )

    add_check(
        checks,
        "no_substantive_title_or_team_changes",
        len(rec["substantive"]) == 0,
        f"Substantive matched changes: {len(rec['substantive'])}.",
    )

    # Re-run reconciler against the same frozen sources in a temp directory.
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            regen_jsonl = tmpdir / "regen_api.jsonl"
            regen_report = tmpdir / "regen_report.json"

            proc = subprocess.run(
                [
                    sys.executable,
                    str(reconciler_path),
                    str(snapshot_path),
                    str(html_path),
                    "--api-output",
                    str(regen_jsonl),
                    "--report",
                    str(regen_report),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            add_check(
                checks,
                "reconciler_regeneration_passes",
                proc.returncode == 0
                and regen_jsonl.is_file()
                and regen_report.is_file(),
                (
                    f"exit={proc.returncode}; "
                    f"jsonl={regen_jsonl.is_file()}; "
                    f"report={regen_report.is_file()}"
                ),
            )

            if regen_jsonl.is_file():
                canonical_bytes = api_jsonl_path.read_bytes()
                regen_bytes = regen_jsonl.read_bytes()
                add_check(
                    checks,
                    "regenerated_api_jsonl_byte_for_byte",
                    canonical_bytes == regen_bytes,
                    (
                        "Regenerated normalized API JSONL is "
                        "byte-for-byte identical."
                    ),
                )

            if regen_report.is_file():
                regen_obj = load_json(regen_report)
                add_check(
                    checks,
                    "regenerated_reconciliation_semantically_identical",
                    semantic_report_core(regen_obj)
                    == semantic_report_core(reconciliation),
                    (
                        "Regenerated reconciliation report matches all "
                        "semantic sections."
                    ),
                )

    except Exception as exc:
        add_check(
            checks,
            "reconciler_regeneration",
            False,
            f"Regeneration raised: {exc}",
        )

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    overall = "PASS" if failed == 0 else "FAIL"

    final_report = {
        "validator": "ProofLoop Ashby API Artifact Validator v0.10",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "api_snapshot": str(snapshot_path),
            "html_jsonl": str(html_path),
            "normalized_api_jsonl": str(api_jsonl_path),
            "reconciliation_report": str(reconciliation_path),
            "reconciler": str(reconciler_path),
        },
        "metrics": metrics,
        "summary": {
            "checks": len(checks),
            "passed": passed,
            "failed": failed,
            "result": overall,
        },
        "checks": checks,
    }

    output_report.write_text(
        json.dumps(final_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("ProofLoop Ashby API Artifact Validator v0.10")
    print(f"Project root:      {root}")
    print(f"Raw API jobs:      {len(raw_jobs)}")
    print(f"Normalized jobs:   {len(api_rows)}")
    print(f"HTML roles:        {len(html_rows)}")
    print(f"Matched:           {len(rec['matched'])}")
    print(f"HTML-only:         {len(rec['html_only'])}")
    print(f"API-only:          {len(rec['api_only'])}")
    print(f"Cosmetic changes:  {len(rec['cosmetic'])}")
    print(f"Substantive:       {len(rec['substantive'])}")
    print(f"Checks run:        {len(checks)}")
    print(f"Checks passed:     {passed}")
    print(f"Checks failed:     {failed}")
    print(f"Validation report: {output_report}")

    print("\nCheck results:")
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] {check['name']}: {check['detail']}")

    print(f"\nRESULT: {overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
