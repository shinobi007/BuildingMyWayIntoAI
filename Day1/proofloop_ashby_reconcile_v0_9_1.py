#!/usr/bin/env python3
"""
ProofLoop Ashby API Snapshot Reconciler v0.9.1

Refines v0.9 reconciliation by distinguishing cosmetic whitespace
differences from substantive title/team changes.

Reads:
- frozen Ashby/OpenAI API snapshot JSON
- canonical HTML-derived OpenAI role JSONL

Produces:
- normalized API JSONL
- reconciliation report with:
  * matched roles
  * HTML-only roles
  * API-only roles
  * cosmetic-only title/team differences
  * substantive title/team differences

This script does NOT call the network.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def normalize_url(url: str | None) -> str:
    if not url:
        return ""
    return url.strip().rstrip("/")


def normalize_text(value):
    """
    Normalize presentation-only whitespace for comparison while preserving
    the original source values elsewhere in the report.
    """
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


def load_html_jsonl(path: Path) -> list[dict]:
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            if not line:
                raise ValueError(f"Blank line in HTML JSONL at line {line_number}")

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSONL at line {line_number}: "
                    f"{exc.msg} at column {exc.colno}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"HTML JSONL line {line_number} is not a JSON object"
                )

            records.append(record)

    return records


def load_api_snapshot(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError("API snapshot root must be a JSON object")

    jobs = payload.get("jobs")

    if not isinstance(jobs, list):
        raise ValueError("API snapshot does not contain a 'jobs' array")

    for index, job in enumerate(jobs, start=1):
        if not isinstance(job, dict):
            raise ValueError(f"API job #{index} is not a JSON object")

    return jobs


def normalize_secondary_locations(value) -> list[dict]:
    if not isinstance(value, list):
        return []

    normalized = []

    for item in value:
        if not isinstance(item, dict):
            continue

        normalized.append({
            "location": item.get("location"),
            "address": item.get("address"),
        })

    return normalized


def normalize_api_jobs(jobs: list[dict], snapshot_name: str) -> list[dict]:
    normalized = []

    for source_index, job in enumerate(jobs, start=1):
        apply_url = job.get("applyUrl")
        job_url = job.get("jobUrl")

        normalized.append({
            "source_index": source_index,
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
            "secondary_locations": normalize_secondary_locations(
                job.get("secondaryLocations")
            ),
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
        })

    return normalized


def write_jsonl(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def reconcile(html_roles: list[dict], api_roles: list[dict]) -> dict:
    html_by_id = {}
    api_by_id = {}
    html_missing_ids = []
    api_missing_ids = []

    for role in html_roles:
        ashby_id = ashby_id_from_url(role.get("apply_url"))
        if ashby_id:
            html_by_id[ashby_id] = role
        else:
            html_missing_ids.append(role)

    for role in api_roles:
        ashby_id = role.get("ashby_id") or ashby_id_from_url(
            role.get("apply_url")
        )
        if ashby_id:
            api_by_id[ashby_id] = role
        else:
            api_missing_ids.append(role)

    html_ids = set(html_by_id)
    api_ids = set(api_by_id)

    matched_ids = sorted(html_ids & api_ids)
    html_only_ids = sorted(html_ids - api_ids)
    api_only_ids = sorted(api_ids - html_ids)

    cosmetic_only = []
    substantive = []

    for ashby_id in matched_ids:
        html_role = html_by_id[ashby_id]
        api_role = api_by_id[ashby_id]

        raw_changes = {}
        substantive_changes = {}

        for field in ("title", "team"):
            html_value = html_role.get(field)
            api_value = api_role.get(field)

            if html_value != api_value:
                raw_changes[field] = {
                    "html": html_value,
                    "api": api_value,
                    "html_normalized": normalize_text(html_value),
                    "api_normalized": normalize_text(api_value),
                }

                if normalize_text(html_value) != normalize_text(api_value):
                    substantive_changes[field] = raw_changes[field]

        if substantive_changes:
            substantive.append({
                "ashby_id": ashby_id,
                "html_role_id": html_role.get("role_id"),
                "changes": substantive_changes,
            })
        elif raw_changes:
            cosmetic_only.append({
                "ashby_id": ashby_id,
                "html_role_id": html_role.get("role_id"),
                "changes": raw_changes,
            })

    html_only = [
        {
            "ashby_id": ashby_id,
            "role_id": html_by_id[ashby_id].get("role_id"),
            "title": html_by_id[ashby_id].get("title"),
            "team": html_by_id[ashby_id].get("team"),
            "display_location": html_by_id[ashby_id].get("display_location"),
            "career_url": html_by_id[ashby_id].get("career_url"),
            "apply_url": html_by_id[ashby_id].get("apply_url"),
        }
        for ashby_id in html_only_ids
    ]

    api_only = [
        {
            "ashby_id": ashby_id,
            "title": api_by_id[ashby_id].get("title"),
            "team": api_by_id[ashby_id].get("team"),
            "primary_location": api_by_id[ashby_id].get("primary_location"),
            "published_at": api_by_id[ashby_id].get("published_at"),
            "is_remote": api_by_id[ashby_id].get("is_remote"),
            "workplace_type": api_by_id[ashby_id].get("workplace_type"),
            "job_url": api_by_id[ashby_id].get("job_url"),
            "apply_url": api_by_id[ashby_id].get("apply_url"),
        }
        for ashby_id in api_only_ids
    ]

    return {
        "summary": {
            "html_roles": len(html_roles),
            "api_roles": len(api_roles),
            "matched": len(matched_ids),
            "html_only": len(html_only_ids),
            "api_only": len(api_only_ids),
            "matched_cosmetic_only_changes": len(cosmetic_only),
            "matched_substantive_title_or_team_changes": len(substantive),
            "html_records_without_ashby_id": len(html_missing_ids),
            "api_records_without_ashby_id": len(api_missing_ids),
        },
        "html_only": html_only,
        "api_only": api_only,
        "matched_cosmetic_only_changes": cosmetic_only,
        "matched_substantive_changes": substantive,
        "html_records_without_ashby_id": html_missing_ids,
        "api_records_without_ashby_id": api_missing_ids,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize a frozen OpenAI Ashby API snapshot and reconcile it "
            "against the HTML-derived ProofLoop role inventory."
        )
    )
    parser.add_argument(
        "api_snapshot",
        type=Path,
        help="Frozen Ashby API snapshot JSON file.",
    )
    parser.add_argument(
        "html_jsonl",
        type=Path,
        help="Canonical HTML-derived OpenAI role JSONL.",
    )
    parser.add_argument(
        "--api-output",
        type=Path,
        default=Path("openai_ashby_roles.jsonl"),
        help="Normalized API JSONL output path.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("openai_ashby_reconciliation_report_v0_9_1.json"),
        help="Reconciliation report output path.",
    )
    args = parser.parse_args()

    for path in (args.api_snapshot, args.html_jsonl):
        if not path.is_file():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            return 2

    try:
        html_roles = load_html_jsonl(args.html_jsonl)
        raw_api_jobs = load_api_snapshot(args.api_snapshot)

        api_roles = normalize_api_jobs(
            raw_api_jobs,
            snapshot_name=args.api_snapshot.name,
        )

        write_jsonl(api_roles, args.api_output)

        report = reconcile(html_roles, api_roles)
        report["source"] = {
            "api_snapshot": str(args.api_snapshot),
            "html_jsonl": str(args.html_jsonl),
            "normalized_api_jsonl": str(args.api_output),
        }

        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    s = report["summary"]

    print("ProofLoop Ashby API Snapshot Reconciler v0.9.1")
    print(f"API snapshot:      {args.api_snapshot}")
    print(f"HTML JSONL:        {args.html_jsonl}")
    print(f"API roles parsed:  {s['api_roles']}")
    print(f"HTML roles:        {s['html_roles']}")
    print(f"Matched roles:     {s['matched']}")
    print(f"HTML-only roles:   {s['html_only']}")
    print(f"API-only roles:    {s['api_only']}")
    print(f"Cosmetic changes:  {s['matched_cosmetic_only_changes']}")
    print(
        "Substantive title/team changes: "
        f"{s['matched_substantive_title_or_team_changes']}"
    )
    print(
        "Missing Ashby IDs: "
        f"HTML={s['html_records_without_ashby_id']} "
        f"API={s['api_records_without_ashby_id']}"
    )
    print(f"API JSONL output:  {args.api_output}")
    print(f"Report:            {args.report}")

    if report["html_only"]:
        print("\nHTML-only roles:")
        for role in report["html_only"]:
            print(
                f"- #{role['role_id']} | {role['title']} | "
                f"{role['team']} | {role['ashby_id']}"
            )

    if report["api_only"]:
        print("\nAPI-only roles:")
        for role in report["api_only"]:
            print(
                f"- {role['title']} | {role['team']} | "
                f"{role['ashby_id']}"
            )

    if report["matched_substantive_changes"]:
        print("\nSubstantive matched changes:")
        for item in report["matched_substantive_changes"]:
            print(
                f"- HTML role #{item['html_role_id']} | "
                f"{item['ashby_id']} | {item['changes']}"
            )

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
