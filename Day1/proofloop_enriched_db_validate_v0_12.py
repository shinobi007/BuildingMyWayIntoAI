#!/usr/bin/env python3
"""
ProofLoop Enriched SQLite Validator v0.12

Validates the REAL enriched database produced by:
    proofloop_build_enriched_db_v0_11.py

Inputs:
- proofloop_enriched.db
- openai_roles.jsonl
- openai_ashby_roles.jsonl
- openai_ashby_reconciliation_report_v0_9_1.json
- proofloop_enriched_db_build_report.json

This validator:
- does not modify the real database
- independently reconstructs expected cross-source relationships
- validates schema, indexes, integrity, foreign keys, counts, provenance,
  source preservation, canonical-role derivation, locations, compensation,
  reconciliation status, constraints, and deterministic rebuild behavior
- writes proofloop_enriched_db_validation_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_TABLES = {
    "build_metadata",
    "roles",
    "html_roles",
    "api_roles",
    "api_secondary_locations",
    "api_compensation_components",
}

EXPECTED_USER_INDEXES = {
    "idx_roles_title",
    "idx_roles_team",
    "idx_roles_department",
    "idx_roles_location",
    "idx_roles_source_status",
    "idx_api_published_at",
    "idx_comp_type",
}


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


def bool_to_int(value):
    if value is None:
        return None
    return 1 if bool(value) else 0


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, start=1):
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


def add_check(checks, name, passed, detail):
    checks.append({
        "name": name,
        "passed": bool(passed),
        "detail": str(detail),
    })


def json_compact(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def expected_canonical_rows(html_rows, api_rows):
    html_by_id = {}
    api_by_id = {}

    for row in html_rows:
        aid = ashby_id_from_url(row.get("apply_url"))
        if not aid:
            raise ValueError(
                f"HTML role_id={row.get('role_id')} has no Ashby UUID"
            )
        if aid in html_by_id:
            raise ValueError(f"Duplicate HTML Ashby UUID: {aid}")
        html_by_id[aid] = row

    for row in api_rows:
        aid = row.get("ashby_id") or ashby_id_from_url(
            row.get("apply_url")
        )
        if not aid:
            raise ValueError(
                f"API source_index={row.get('source_index')} "
                "has no Ashby UUID"
            )
        if aid in api_by_id:
            raise ValueError(f"Duplicate API Ashby UUID: {aid}")
        api_by_id[aid] = row

    result = []

    for aid in sorted(set(html_by_id) | set(api_by_id)):
        h = html_by_id.get(aid)
        a = api_by_id.get(aid)

        if h and a:
            status = "matched"
        elif h:
            status = "html_only"
        else:
            status = "api_only"

        result.append((
            aid,
            h.get("role_id") if h else None,
            normalize_text(a.get("title")) if a else normalize_text(h.get("title")),
            normalize_text(a.get("team")) if a else normalize_text(h.get("team")),
            a.get("department") if a else None,
            a.get("employment_type") if a else None,
            (
                a.get("primary_location")
                if a and a.get("primary_location")
                else h.get("display_location") if h else None
            ),
            a.get("published_at") if a else None,
            bool_to_int(a.get("is_listed")) if a else None,
            bool_to_int(a.get("is_remote")) if a else None,
            a.get("workplace_type") if a else None,
            h.get("career_url") if h else None,
            a.get("job_url") if a else None,
            (
                a.get("apply_url")
                if a and a.get("apply_url")
                else h.get("apply_url")
            ),
            a.get("description_plain") if a else None,
            a.get("description_html") if a else None,
            1 if h else 0,
            1 if a else 0,
            status,
        ))

    return result


def expected_html_rows(html_rows):
    return sorted(
        [
            (
                row["role_id"],
                ashby_id_from_url(row["apply_url"]),
                row["title"],
                row["team"],
                row["display_location"],
                row["career_url"],
                row["apply_url"],
            )
            for row in html_rows
        ],
        key=lambda x: x[0],
    )


def expected_api_rows(api_rows):
    return sorted(
        [
            (
                row["ashby_id"],
                row["source_index"],
                row["source_snapshot"],
                row.get("title"),
                normalize_text(row.get("title")),
                row.get("department"),
                row.get("team"),
                normalize_text(row.get("team")),
                row.get("employment_type"),
                row.get("primary_location"),
                row.get("published_at"),
                bool_to_int(row.get("is_listed")),
                bool_to_int(row.get("is_remote")),
                row.get("workplace_type"),
                json_compact(row.get("address")),
                row.get("job_url"),
                row.get("apply_url"),
                row.get("description_plain"),
                row.get("description_html"),
                json_compact(row.get("compensation")),
            )
            for row in api_rows
        ],
        key=lambda x: x[1],
    )


def expected_secondary_rows(api_rows):
    rows = []
    for row in api_rows:
        aid = row["ashby_id"]
        for index, location in enumerate(
            row.get("secondary_locations") or [], start=1
        ):
            rows.append((
                aid,
                index,
                location.get("location"),
                json_compact(location.get("address")),
            ))
    return sorted(rows)


def expected_compensation_rows(api_rows):
    rows = []
    for row in api_rows:
        aid = row["ashby_id"]
        compensation = row.get("compensation") or {}
        for index, component in enumerate(
            compensation.get("summaryComponents") or [],
            start=1,
        ):
            rows.append((
                aid,
                index,
                component.get("compensationType"),
                component.get("interval"),
                component.get("currencyCode"),
                component.get("minValue"),
                component.get("maxValue"),
            ))
    return sorted(rows)


def database_snapshot(db_path: Path):
    conn = sqlite3.connect(db_path)
    try:
        return {
            "roles": conn.execute(
                """
                SELECT
                    ashby_id, html_role_id, title, team, department,
                    employment_type, display_location, published_at,
                    is_listed, is_remote, workplace_type, career_url,
                    job_url, apply_url, description_plain,
                    description_html, present_in_html, present_in_api,
                    source_status
                FROM roles
                ORDER BY ashby_id
                """
            ).fetchall(),
            "html_roles": conn.execute(
                """
                SELECT
                    html_role_id, ashby_id, title, team,
                    display_location, career_url, apply_url
                FROM html_roles
                ORDER BY html_role_id
                """
            ).fetchall(),
            "api_roles": conn.execute(
                """
                SELECT
                    ashby_id, source_index, source_snapshot,
                    title_raw, title_normalized, department,
                    team_raw, team_normalized, employment_type,
                    primary_location, published_at, is_listed,
                    is_remote, workplace_type, address_json,
                    job_url, apply_url, description_plain,
                    description_html, compensation_json
                FROM api_roles
                ORDER BY source_index
                """
            ).fetchall(),
            "secondary": conn.execute(
                """
                SELECT
                    ashby_id, location_index, location, address_json
                FROM api_secondary_locations
                ORDER BY ashby_id, location_index
                """
            ).fetchall(),
            "compensation": conn.execute(
                """
                SELECT
                    ashby_id, component_index, compensation_type,
                    interval, currency_code, min_value, max_value
                FROM api_compensation_components
                ORDER BY ashby_id, component_index
                """
            ).fetchall(),
            "metadata": dict(
                conn.execute(
                    "SELECT key, value FROM build_metadata"
                ).fetchall()
            ),
        }
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ProofLoop's enriched SQLite database."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--db",
        default="proofloop_enriched.db",
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
        "--build-report",
        default="proofloop_enriched_db_build_report.json",
    )
    parser.add_argument(
        "--builder",
        default="proofloop_build_enriched_db_v0_11.py",
    )
    parser.add_argument(
        "--report",
        default="proofloop_enriched_db_validation_report.json",
    )
    parser.add_argument("--expected-html", type=int, default=817)
    parser.add_argument("--expected-api", type=int, default=815)
    parser.add_argument("--expected-union", type=int, default=818)
    args = parser.parse_args()

    root = args.root.resolve()

    db_path = root / args.db
    html_path = root / args.html_jsonl
    api_path = root / args.api_jsonl
    reconciliation_path = root / args.reconciliation_report
    build_report_path = root / args.build_report
    builder_path = root / args.builder
    report_path = root / args.report

    required = {
        "db_exists": db_path,
        "html_jsonl_exists": html_path,
        "api_jsonl_exists": api_path,
        "reconciliation_report_exists": reconciliation_path,
        "build_report_exists": build_report_path,
        "builder_exists": builder_path,
    }

    checks = []
    metrics = {}

    for name, path in required.items():
        add_check(checks, name, path.is_file(), path)

    if not all(path.is_file() for path in required.values()):
        final = {
            "validator": "ProofLoop Enriched SQLite Validator v0.12",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "checks": len(checks),
                "passed": sum(c["passed"] for c in checks),
                "failed": sum(not c["passed"] for c in checks),
                "result": "FAIL",
            },
            "checks": checks,
        }
        report_path.write_text(
            json.dumps(final, indent=2) + "\n",
            encoding="utf-8",
        )
        print("RESULT: FAIL - required artifact missing")
        return 1

    try:
        html_rows = load_jsonl(html_path)
        api_rows = load_jsonl(api_path)
        reconciliation = load_json(reconciliation_path)
        build_report = load_json(build_report_path)
    except Exception as exc:
        add_check(checks, "source_artifacts_load", False, exc)
        html_rows = []
        api_rows = []
        reconciliation = {}
        build_report = {}
    else:
        add_check(
            checks,
            "source_artifacts_load",
            True,
            (
                f"HTML={len(html_rows)}, API={len(api_rows)}, "
                "reports parsed."
            ),
        )

    conn = sqlite3.connect(db_path)
    try:
        integrity = conn.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]
        add_check(
            checks,
            "sqlite_integrity",
            integrity == "ok",
            f"PRAGMA integrity_check returned {integrity!r}.",
        )

        fk_issues = conn.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()
        add_check(
            checks,
            "foreign_key_check",
            len(fk_issues) == 0,
            f"Foreign-key issue rows: {len(fk_issues)}.",
        )

        tables = {
            row[0]
            for row in conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                """
            )
            if not row[0].startswith("sqlite_")
        }
        add_check(
            checks,
            "expected_tables_exact",
            tables == EXPECTED_TABLES,
            f"Observed tables: {sorted(tables)}",
        )

        indexes = {
            row[0]
            for row in conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='index'
                  AND sql IS NOT NULL
                """
            )
        }
        add_check(
            checks,
            "expected_user_indexes_present",
            EXPECTED_USER_INDEXES.issubset(indexes),
            f"Observed user indexes: {sorted(indexes)}",
        )

        counts = {}
        for table in sorted(EXPECTED_TABLES):
            counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        metrics["table_counts"] = counts

        add_check(
            checks,
            "roles_count",
            counts.get("roles") == args.expected_union,
            f"roles={counts.get('roles')}; expected={args.expected_union}",
        )
        add_check(
            checks,
            "html_roles_count",
            counts.get("html_roles") == args.expected_html,
            f"html_roles={counts.get('html_roles')}; expected={args.expected_html}",
        )
        add_check(
            checks,
            "api_roles_count",
            counts.get("api_roles") == args.expected_api,
            f"api_roles={counts.get('api_roles')}; expected={args.expected_api}",
        )

        status_counts = dict(
            conn.execute(
                """
                SELECT source_status, COUNT(*)
                FROM roles
                GROUP BY source_status
                """
            ).fetchall()
        )
        metrics["status_counts"] = status_counts

        expected_status = {
            "matched": 814,
            "html_only": 3,
            "api_only": 1,
        }
        add_check(
            checks,
            "source_status_counts",
            status_counts == expected_status,
            f"Observed: {status_counts}",
        )

        flag_counts = {
            (h, a): count
            for h, a, count in conn.execute(
                """
                SELECT present_in_html, present_in_api, COUNT(*)
                FROM roles
                GROUP BY present_in_html, present_in_api
                """
            ).fetchall()
        }
        expected_flags = {
            (1, 1): 814,
            (1, 0): 3,
            (0, 1): 1,
        }
        add_check(
            checks,
            "presence_flag_counts",
            flag_counts == expected_flags,
            f"Observed: {flag_counts}",
        )

        status_flag_consistency = conn.execute(
            """
            SELECT COUNT(*)
            FROM roles
            WHERE NOT (
                (source_status='matched'
                 AND present_in_html=1 AND present_in_api=1)
                OR
                (source_status='html_only'
                 AND present_in_html=1 AND present_in_api=0)
                OR
                (source_status='api_only'
                 AND present_in_html=0 AND present_in_api=1)
            )
            """
        ).fetchone()[0]
        add_check(
            checks,
            "status_flags_consistent",
            status_flag_consistency == 0,
            f"Inconsistent rows: {status_flag_consistency}.",
        )

        blank_required = conn.execute(
            """
            SELECT COUNT(*)
            FROM roles
            WHERE ashby_id IS NULL OR TRIM(ashby_id)=''
               OR title IS NULL OR TRIM(title)=''
               OR team IS NULL OR TRIM(team)=''
               OR apply_url IS NULL OR TRIM(apply_url)=''
            """
        ).fetchone()[0]
        add_check(
            checks,
            "canonical_required_fields_present",
            blank_required == 0,
            f"Rows with blank required canonical fields: {blank_required}.",
        )

        duplicate_apply = conn.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT apply_url
                FROM roles
                GROUP BY apply_url
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]
        add_check(
            checks,
            "canonical_apply_urls_unique",
            duplicate_apply == 0,
            f"Duplicate canonical apply_url groups: {duplicate_apply}.",
        )

        api_id_url_mismatch = conn.execute(
            """
            SELECT ashby_id, job_url, apply_url
            FROM api_roles
            """
        ).fetchall()
        mismatches = [
            aid for aid, job_url, apply_url in api_id_url_mismatch
            if aid != ashby_id_from_url(job_url)
            or aid != ashby_id_from_url(apply_url)
        ]
        add_check(
            checks,
            "api_url_ids_match",
            len(mismatches) == 0,
            f"URL/UUID mismatches: {len(mismatches)}.",
        )

        metadata = dict(
            conn.execute(
                "SELECT key, value FROM build_metadata"
            ).fetchall()
        )
        metrics["metadata"] = metadata

        metadata_expected = {
            "builder": "ProofLoop Enriched SQLite Builder v0.11",
            "html_source": html_path.name,
            "api_source": api_path.name,
            "reconciliation_source": reconciliation_path.name,
            "html_role_count": str(args.expected_html),
            "api_role_count": str(args.expected_api),
            "canonical_union_count": str(args.expected_union),
        }
        metadata_ok = all(
            metadata.get(k) == v
            for k, v in metadata_expected.items()
        )
        add_check(
            checks,
            "build_metadata_matches_sources",
            metadata_ok,
            f"Observed metadata keys: {metadata}",
        )

        # Constraint tests happen only in an in-memory copy.
        mem = sqlite3.connect(":memory:")
        try:
            mem.execute("PRAGMA foreign_keys = ON")
            conn.backup(mem)

            sample = mem.execute(
                """
                SELECT ashby_id, apply_url
                FROM roles
                ORDER BY ashby_id
                LIMIT 1
                """
            ).fetchone()

            rejected_duplicate_pk = False
            try:
                mem.execute(
                    """
                    INSERT INTO roles (
                        ashby_id, html_role_id, title, team,
                        apply_url, present_in_html, present_in_api,
                        source_status
                    )
                    VALUES (?, NULL, 'x', 'x', ?, 0, 1, 'api_only')
                    """,
                    (sample[0], "https://example.invalid/unique-1"),
                )
            except sqlite3.IntegrityError:
                rejected_duplicate_pk = True

            add_check(
                checks,
                "reject_duplicate_canonical_primary_key",
                rejected_duplicate_pk,
                "Duplicate canonical Ashby UUID rejected.",
            )

            rejected_duplicate_apply = False
            try:
                mem.execute(
                    """
                    INSERT INTO roles (
                        ashby_id, html_role_id, title, team,
                        apply_url, present_in_html, present_in_api,
                        source_status
                    )
                    VALUES (
                        '00000000-0000-0000-0000-000000000001',
                        NULL, 'x', 'x', ?, 0, 1, 'api_only'
                    )
                    """,
                    (sample[1],),
                )
            except sqlite3.IntegrityError:
                rejected_duplicate_apply = True

            add_check(
                checks,
                "reject_duplicate_canonical_apply_url",
                rejected_duplicate_apply,
                "Duplicate canonical apply_url rejected.",
            )

            rejected_bad_status = False
            try:
                mem.execute(
                    """
                    INSERT INTO roles (
                        ashby_id, html_role_id, title, team,
                        apply_url, present_in_html, present_in_api,
                        source_status
                    )
                    VALUES (
                        '00000000-0000-0000-0000-000000000002',
                        NULL, 'x', 'x',
                        'https://example.invalid/unique-2',
                        0, 1, 'invalid_status'
                    )
                    """
                )
            except sqlite3.IntegrityError:
                rejected_bad_status = True

            add_check(
                checks,
                "reject_invalid_source_status",
                rejected_bad_status,
                "Invalid source_status rejected by CHECK constraint.",
            )

            rejected_bad_flag = False
            try:
                mem.execute(
                    """
                    INSERT INTO roles (
                        ashby_id, html_role_id, title, team,
                        apply_url, present_in_html, present_in_api,
                        source_status
                    )
                    VALUES (
                        '00000000-0000-0000-0000-000000000003',
                        NULL, 'x', 'x',
                        'https://example.invalid/unique-3',
                        2, 1, 'matched'
                    )
                    """
                )
            except sqlite3.IntegrityError:
                rejected_bad_flag = True

            add_check(
                checks,
                "reject_invalid_presence_flag",
                rejected_bad_flag,
                "Invalid present_in_html value rejected.",
            )

        finally:
            mem.close()

    finally:
        conn.close()

    # Source-preservation and canonical derivation.
    try:
        snap = database_snapshot(db_path)

        expected_roles = expected_canonical_rows(
            html_rows,
            api_rows,
        )
        expected_html = expected_html_rows(html_rows)
        expected_api = expected_api_rows(api_rows)
        expected_secondary = expected_secondary_rows(api_rows)
        expected_comp = expected_compensation_rows(api_rows)

        add_check(
            checks,
            "canonical_roles_match_independent_derivation",
            snap["roles"] == expected_roles,
            (
                f"Database canonical rows={len(snap['roles'])}; "
                f"independently derived={len(expected_roles)}."
            ),
        )

        add_check(
            checks,
            "html_source_preserved_row_for_row",
            snap["html_roles"] == expected_html,
            (
                f"Database HTML rows={len(snap['html_roles'])}; "
                f"source rows={len(expected_html)}."
            ),
        )

        add_check(
            checks,
            "api_source_preserved_row_for_row",
            snap["api_roles"] == expected_api,
            (
                f"Database API rows={len(snap['api_roles'])}; "
                f"source rows={len(expected_api)}."
            ),
        )

        add_check(
            checks,
            "secondary_locations_match_source",
            snap["secondary"] == expected_secondary,
            (
                f"Database secondary locations={len(snap['secondary'])}; "
                f"derived={len(expected_secondary)}."
            ),
        )

        add_check(
            checks,
            "compensation_components_match_source",
            snap["compensation"] == expected_comp,
            (
                f"Database compensation components="
                f"{len(snap['compensation'])}; "
                f"derived={len(expected_comp)}."
            ),
        )

    except Exception as exc:
        add_check(
            checks,
            "independent_source_derivation",
            False,
            exc,
        )

    # Reconciliation report must agree with database status.
    rec_summary = reconciliation.get("summary", {})
    db_status = metrics.get("status_counts", {})

    reconciliation_ok = (
        rec_summary.get("matched") == db_status.get("matched")
        and rec_summary.get("html_only") == db_status.get("html_only")
        and rec_summary.get("api_only") == db_status.get("api_only")
        and rec_summary.get(
            "matched_substantive_title_or_team_changes"
        ) == 0
    )
    add_check(
        checks,
        "database_agrees_with_reconciliation_report",
        reconciliation_ok,
        f"Reconciliation summary: {rec_summary}",
    )

    # Build report must agree with current database.
    build_report_ok = (
        build_report.get("result") == "PASS"
        and build_report.get("observed", {}).get("html_roles")
            == args.expected_html
        and build_report.get("observed", {}).get("api_roles")
            == args.expected_api
        and build_report.get("observed", {}).get("canonical_union")
            == args.expected_union
        and build_report.get("table_counts", {}).get("roles")
            == args.expected_union
        and build_report.get("status_counts") == {
            "api_only": 1,
            "html_only": 3,
            "matched": 814,
        }
    )
    add_check(
        checks,
        "build_report_matches_database_expectations",
        build_report_ok,
        (
            f"Build report result={build_report.get('result')}; "
            f"observed={build_report.get('observed')}"
        ),
    )

    # Rebuild in a temporary directory and compare semantic DB content.
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            regen_db = tmpdir / "proofloop_enriched_regenerated.db"
            regen_report = tmpdir / "build_report.json"

            proc = subprocess.run(
                [
                    sys.executable,
                    str(builder_path),
                    "--html-jsonl",
                    str(html_path),
                    "--api-jsonl",
                    str(api_path),
                    "--reconciliation-report",
                    str(reconciliation_path),
                    "--output",
                    str(regen_db),
                    "--report",
                    str(regen_report),
                    "--expected-html",
                    str(args.expected_html),
                    "--expected-api",
                    str(args.expected_api),
                    "--expected-union",
                    str(args.expected_union),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            regen_exists = regen_db.is_file()
            add_check(
                checks,
                "builder_regeneration_passes",
                proc.returncode == 0 and regen_exists,
                (
                    f"exit={proc.returncode}; "
                    f"database exists={regen_exists}"
                ),
            )

            if regen_exists:
                original_snap = database_snapshot(db_path)
                regen_snap = database_snapshot(regen_db)

                # generated_at_utc is intentionally different.
                original_meta = dict(original_snap["metadata"])
                regen_meta = dict(regen_snap["metadata"])
                original_meta.pop("generated_at_utc", None)
                regen_meta.pop("generated_at_utc", None)

                same = (
                    original_snap["roles"] == regen_snap["roles"]
                    and original_snap["html_roles"]
                        == regen_snap["html_roles"]
                    and original_snap["api_roles"]
                        == regen_snap["api_roles"]
                    and original_snap["secondary"]
                        == regen_snap["secondary"]
                    and original_snap["compensation"]
                        == regen_snap["compensation"]
                    and original_meta == regen_meta
                )

                add_check(
                    checks,
                    "regenerated_database_semantically_identical",
                    same,
                    (
                        "All domain tables and stable metadata match "
                        "the original enriched database."
                    ),
                )

    except Exception as exc:
        add_check(
            checks,
            "builder_regeneration",
            False,
            f"Regeneration raised: {exc}",
        )

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    result = "PASS" if failed == 0 else "FAIL"

    final_report = {
        "validator": "ProofLoop Enriched SQLite Validator v0.12",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": str(db_path),
        "sources": {
            "html_jsonl": str(html_path),
            "api_jsonl": str(api_path),
            "reconciliation_report": str(reconciliation_path),
            "build_report": str(build_report_path),
            "builder": str(builder_path),
        },
        "expected": {
            "html_roles": args.expected_html,
            "api_roles": args.expected_api,
            "canonical_union": args.expected_union,
        },
        "metrics": metrics,
        "summary": {
            "checks": len(checks),
            "passed": passed,
            "failed": failed,
            "result": result,
        },
        "checks": checks,
    }

    report_path.write_text(
        json.dumps(final_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("ProofLoop Enriched SQLite Validator v0.12")
    print(f"Database:          {db_path}")
    print(f"Expected HTML:     {args.expected_html}")
    print(f"Expected API:      {args.expected_api}")
    print(f"Expected union:    {args.expected_union}")
    print(f"Checks run:        {len(checks)}")
    print(f"Checks passed:     {passed}")
    print(f"Checks failed:     {failed}")
    print(f"Validation report: {report_path}")

    print("\nCheck results:")
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] {check['name']}: {check['detail']}")

    print(f"\nRESULT: {result}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
