#!/usr/bin/env python3
"""ProofLoop Ashby Stage 3 (v0.3.0): offline JSONL -> SQLite.

Standalone standard-library importer. Keeps every parsed source object in
roles.raw_json, every normalized object in roles.canonical_json and the full
provenance object in roles.provenance_json. Child tables expose secondary
locations, compensation tiers, tier components, and summary components.

No network use. Does not change the JSONL input or replace an existing output
folder. Builds and verifies the database in an unpublished staging folder,
then moves the complete bundle into place.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

VERSION = "0.3.0"
MAX_INPUT_BYTES = 500 * 1024 * 1024
SHA256_RX = re.compile(r"^[0-9a-f]{64}$")


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def compact(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as file:
        for part in iter(lambda: file.read(1024 * 1024), b""):
            sha.update(part)
    return sha.hexdigest()


def load_json_no_nan(path: Path) -> object:
    def reject_constant(value: str):
        raise ValueError(f"Invalid JSON number: {value}")
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file, parse_constant=reject_constant)


def expect_text(obj: dict, key: str, *, required: bool = False) -> str | None:
    value = obj.get(key)
    if value is None:
        if required:
            raise ValueError(f"Missing required {key}")
        return None
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{key} must be nonblank text" if required else f"{key} must be text or null")
    return value


def as_flag(value: object, field: str) -> int | None:
    if value is None:
        return None
    if type(value) is not bool:
        raise ValueError(f"{field}: must be boolean or null")
    return int(value)


def require_https(value: str | None, field: str) -> None:
    if value is None:
        return
    u = urlsplit(value)
    if u.scheme.lower() != "https" or not u.hostname or u.username or u.password:
        raise ValueError(f"{field}: expected HTTPS URL")


def as_array(value: object, field: str) -> list:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def as_object(value: object, field: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def amount(value: object, field: str) -> float | None:
    if value is None:
        return None
    if type(value) not in (int, float):
        raise ValueError(f"{field} must be a number or null")
    if not (-1e15 < value < 1e15):
        raise ValueError(f"{field} unreasonable / not finite")
    return value


def check_and_read_jsonl(path: Path, *, allow_empty: bool, expected_count: int | None,
                         normalization_report: Path | None) -> tuple[list[dict], dict]:
    if not path.is_file():
        raise ValueError(f"JSONL input not found: {path.name}")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("JSONL input exceeds 500 MiB safety limit")
    sha = digest(path)
    report = None
    if normalization_report is not None:
        report = load_json_no_nan(normalization_report)
        if not isinstance(report, dict) or report.get("status") != "PASS" or report.get("stage") != "normalize":
            raise ValueError("Normalization report is not a successful Stage 1 report")
        if report.get("normalized_sha256") != sha:
            raise ValueError("Input JSONL SHA-256 differs from normalization report")
    seen_ids: set[str] = set()
    seen_positions: set[tuple[str, int]] = set()
    boards: set[str] = set()
    source_hashes: set[str] = set()
    records: list[dict] = []
    def reject_constant(value: str):
        raise ValueError(f"Invalid JSON constant {value}")
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                raise ValueError(f"Blank JSONL line at {line_number}")
            record = json.loads(line, parse_constant=reject_constant)
            rec = as_object(record, f"JSONL line {line_number}")
            can = as_object(rec.get("canonical"), "canonical")
            raw = as_object(rec.get("raw"), "raw")
            prov = as_object(rec.get("provenance"), "provenance")
            ident = expect_text(can, "id", required=True)
            if ident != raw.get("id"):
                raise ValueError(f"Line {line_number}: canonical and raw IDs differ")
            if ident in seen_ids:
                raise ValueError(f"Duplicate job ID {ident}")
            seen_ids.add(ident)
            expect_text(can, "title", required=True)
            for field in ("job_url", "apply_url"):
                require_https(expect_text(can, field), field)
            for field in ("is_listed", "is_remote", "should_display_compensation"):
                as_flag(can.get(field), field)
            for field in ("description_html", "description_plain", "department", "team",
                          "employment_type", "location", "workplace_type", "published_at"):
                expect_text(can, field)
            if can.get("address") is not None:
                as_object(can["address"], "address")
            sec = as_array(can.get("secondary_locations"), "secondary_locations")
            for i, v in enumerate(sec):
                loc = as_object(v, f"secondary_locations[{i}]")
                expect_text(loc, "location")
                if loc.get("address") is not None:
                    as_object(loc["address"], "secondary location address")
            comp = as_object(can.get("compensation"), "compensation")
            for i, tier in enumerate(as_array(comp.get("compensationTiers"), "compensationTiers")):
                tier = as_object(tier, f"compensationTiers[{i}]")
                for j, component in enumerate(as_array(tier.get("components"), "components")):
                    component = as_object(component, f"component[{i}][{j}]")
                    amount(component.get("minValue"), "minValue")
                    amount(component.get("maxValue"), "maxValue")
            for i, component in enumerate(as_array(comp.get("summaryComponents"), "summaryComponents")):
                component = as_object(component, f"summaryComponents[{i}]")
                amount(component.get("minValue"), "minValue")
                amount(component.get("maxValue"), "maxValue")
            board = expect_text(prov, "board", required=True)
            provider = expect_text(prov, "provider", required=True)
            source_sha = expect_text(prov, "snapshot_sha256", required=True)
            source_index = prov.get("source_index")
            if provider != "ashby" or not SHA256_RX.fullmatch(source_sha):
                raise ValueError(f"Line {line_number}: invalid provider or source hash")
            if type(source_index) is not int or source_index < 1:
                raise ValueError(f"Line {line_number}: invalid source index")
            if (board, source_index) in seen_positions:
                raise ValueError(f"Line {line_number}: duplicate source index")
            seen_positions.add((board, source_index))
            boards.add(board)
            source_hashes.add(source_sha)
            records.append(rec)
    if not records and not allow_empty:
        raise ValueError("Empty input must be acknowledged with --allow-empty")
    if expected_count is not None and len(records) != expected_count:
        raise ValueError(f"Expected {expected_count} records, got {len(records)}")
    if len(boards) > 1 or len(source_hashes) > 1:
        raise ValueError("A run must contain one board and one source snapshot")
    if report is not None:
        if report.get("audit", {}).get("record_count") != len(records):
            raise ValueError("JSONL record count differs from normalization report")
        if records and report.get("audit", {}).get("source_sha256") != next(iter(source_hashes)):
            raise ValueError("Input source hash differs from normalization report")
    return records, {"jsonl_sha256": sha, "board": next(iter(boards), None),
                     "source_sha256": next(iter(source_hashes), None),
                     "normalization_report_verified": report is not None}


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE build_metadata(key TEXT PRIMARY KEY, value_json TEXT NOT NULL);
CREATE TABLE roles(
 id TEXT PRIMARY KEY NOT NULL,
 board TEXT NOT NULL,
 source_index INTEGER NOT NULL CHECK(source_index > 0),
 source_sha256 TEXT NOT NULL,
 title TEXT NOT NULL CHECK(length(trim(title))>0),
 department TEXT, team TEXT, employment_type TEXT, location TEXT, published_at TEXT,
 is_listed INTEGER CHECK(is_listed IN (0,1) OR is_listed IS NULL),
 is_remote INTEGER CHECK(is_remote IN (0,1) OR is_remote IS NULL),
 workplace_type TEXT,
 should_display_compensation INTEGER CHECK(should_display_compensation IN (0,1) OR should_display_compensation IS NULL),
 job_url TEXT, apply_url TEXT,
 description_plain TEXT, description_html TEXT,
 address_json TEXT NOT NULL, compensation_json TEXT NOT NULL,
 canonical_json TEXT NOT NULL, raw_json TEXT NOT NULL, provenance_json TEXT NOT NULL,
 UNIQUE(board, source_index)
);
CREATE INDEX idx_roles_location ON roles(location);
CREATE INDEX idx_roles_team ON roles(team);
CREATE INDEX idx_roles_workplace ON roles(workplace_type);
CREATE TABLE secondary_locations(
 role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
 ordinal INTEGER NOT NULL CHECK(ordinal >= 0),
 location TEXT, address_json TEXT NOT NULL, raw_json TEXT NOT NULL,
 PRIMARY KEY(role_id,ordinal)
);
CREATE TABLE compensation_tiers(
 role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
 ordinal INTEGER NOT NULL CHECK(ordinal >= 0),
 tier_id TEXT, tier_summary TEXT, title TEXT, additional_information TEXT,
 raw_json TEXT NOT NULL,
 PRIMARY KEY(role_id,ordinal)
);
CREATE TABLE compensation_components(
 role_id TEXT NOT NULL, tier_ordinal INTEGER NOT NULL,
 ordinal INTEGER NOT NULL CHECK(ordinal >= 0),
 component_id TEXT, compensation_type TEXT, interval TEXT, currency_code TEXT,
 min_value REAL, max_value REAL, summary TEXT, raw_json TEXT NOT NULL,
 PRIMARY KEY(role_id,tier_ordinal,ordinal),
 FOREIGN KEY(role_id,tier_ordinal) REFERENCES compensation_tiers(role_id,ordinal) ON DELETE CASCADE
);
CREATE TABLE compensation_summary_components(
 role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
 ordinal INTEGER NOT NULL CHECK(ordinal >= 0),
 compensation_type TEXT, interval TEXT, currency_code TEXT,
 min_value REAL, max_value REAL, raw_json TEXT NOT NULL,
 PRIMARY KEY(role_id,ordinal)
);
CREATE VIEW role_overview AS
SELECT id,title,team,department,location,workplace_type,is_remote,
       should_display_compensation,published_at,job_url,apply_url
FROM roles;
"""


def initialize(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def insert_records(conn: sqlite3.Connection, records: list[dict], input_data: dict) -> dict:
    counts = {"roles": 0, "secondary_locations": 0, "compensation_tiers": 0,
              "compensation_components": 0, "compensation_summary_components": 0}
    for rec in records:
        can, raw, prov = rec["canonical"], rec["raw"], rec["provenance"]
        conn.execute("""INSERT INTO roles(id,board,source_index,source_sha256,title,department,team,employment_type,
 location,published_at,is_listed,is_remote,workplace_type,should_display_compensation,job_url,apply_url,
 description_plain,description_html,address_json,compensation_json,canonical_json,raw_json,provenance_json)
 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            can["id"], prov["board"], prov["source_index"], prov["snapshot_sha256"],can["title"],
            can.get("department"),can.get("team"),can.get("employment_type"),can.get("location"),
            can.get("published_at"), as_flag(can.get("is_listed"),"is_listed"),
            as_flag(can.get("is_remote"),"is_remote"),can.get("workplace_type"),
            as_flag(can.get("should_display_compensation"),"should_display_compensation"),
            can.get("job_url"),can.get("apply_url"),can.get("description_plain"),can.get("description_html"),
            compact(can.get("address")),compact(can.get("compensation")),compact(can),compact(raw),compact(prov)))
        counts["roles"] += 1
        for ordinal, loc in enumerate(can["secondary_locations"]):
            conn.execute("INSERT INTO secondary_locations VALUES(?,?,?,?,?)", (
                can["id"],ordinal,loc.get("location"),compact(loc.get("address")),compact(loc)))
            counts["secondary_locations"] += 1
        comp=can["compensation"]
        for ti, tier in enumerate(comp["compensationTiers"]):
            conn.execute("INSERT INTO compensation_tiers VALUES(?,?,?,?,?,?,?)",(
                can["id"],ti,tier.get("id"),tier.get("tierSummary"),tier.get("title"),
                tier.get("additionalInformation"),compact(tier)))
            counts["compensation_tiers"] += 1
            for ci, component in enumerate(tier["components"]):
                conn.execute("INSERT INTO compensation_components VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                    can["id"],ti,ci,component.get("id"),component.get("compensationType"),
                    component.get("interval"),component.get("currencyCode"),
                    amount(component.get("minValue"),"minValue"),amount(component.get("maxValue"),"maxValue"),
                    component.get("summary"),compact(component)))
                counts["compensation_components"] += 1
        for ci, component in enumerate(comp["summaryComponents"]):
            conn.execute("INSERT INTO compensation_summary_components VALUES(?,?,?,?,?,?,?,?)",(
                can["id"],ci,component.get("compensationType"),component.get("interval"),
                component.get("currencyCode"),amount(component.get("minValue"),"minValue"),
                amount(component.get("maxValue"),"maxValue"),compact(component)))
            counts["compensation_summary_components"] += 1
    for k,v in {"program_version":VERSION,"board":input_data["board"],
                "normalized_sha256":input_data["jsonl_sha256"],
                "snapshot_sha256":input_data["source_sha256"],
                "record_count":len(records)}.items():
        conn.execute("INSERT INTO build_metadata VALUES (?,?)",(k,compact(v)))
    return counts


def verify_database(db: Path, records: list[dict], expected: dict) -> dict:
    conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro",uri=True)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = conn.execute("PRAGMA foreign_key_check").fetchall()
        checks={"sqlite_integrity":integrity == "ok", "foreign_keys":not foreign_keys}
        tables=["roles","secondary_locations","compensation_tiers","compensation_components",
                "compensation_summary_components"]
        counts={name:conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] for name in tables}
        checks["child_counts"] = all(counts[k]==expected[k] for k in tables)
        checks["role_count"] = counts["roles"] == len(records)
        checks["json_roundtrip"] = True
        checks["source_ordinal_roundtrip"] = True
        checks["nested_json_roundtrip"] = True
        for rec in records:
            ident=rec["canonical"]["id"]
            row=conn.execute("SELECT canonical_json,raw_json,provenance_json,source_index FROM roles WHERE id=?",(ident,)).fetchone()
            if row is None or any(json.loads(row[i])!=rec[key] for i,key in enumerate(("canonical","raw","provenance"))):
                checks["json_roundtrip"]=False
                continue
            if row[3] != rec["provenance"]["source_index"]:
                checks["source_ordinal_roundtrip"]=False
            nested=(
                ("secondary_locations","raw_json",rec["canonical"]["secondary_locations"]),
                ("compensation_tiers","raw_json",rec["canonical"]["compensation"]["compensationTiers"]),
                ("compensation_summary_components","raw_json",rec["canonical"]["compensation"]["summaryComponents"]),
            )
            for tab,field,items in nested:
                db_items=[json.loads(r[0]) for r in conn.execute(
                    f"SELECT {field} FROM {tab} WHERE role_id=? ORDER BY ordinal",(ident,))]
                if db_items != items:checks["nested_json_roundtrip"]=False
            tiers=rec["canonical"]["compensation"]["compensationTiers"]
            for ti,tier in enumerate(tiers):
                db_comps=[json.loads(r[0]) for r in conn.execute(
                    "SELECT raw_json FROM compensation_components WHERE role_id=? AND tier_ordinal=? ORDER BY ordinal",
                    (ident,ti))]
                if db_comps!=tier["components"]:checks["nested_json_roundtrip"]=False
        if not all(checks.values()):
            raise ValueError(f"Post-build verification failed: {', '.join(k for k,v in checks.items() if not v)}")
        return {"counts":counts,"checks":checks,"integrity_result":integrity}
    finally:
        conn.close()


def markdown_report(report: dict) -> str:
    lines=["# ProofLoop Stage 3 — SQLite Build Report", "",
        f"- **Status:** {report['status']}",
        f"- **Run ID:** `{report['run_id']}`",
        f"- **Generated (UTC):** {report['generated_at_utc']}",
        f"- **Board:** `{report['board']}`",
        f"- **Input JSONL SHA-256:** `{report['input']['jsonl_sha256']}`",
        f"- **Source snapshot SHA-256:** `{report['input']['source_sha256']}`",
        f"- **Normalization report verified:** {report['input']['normalization_report_verified']}",
        "", "## Persisted records", "",
        "| Table | Records |", "| --- | ---: |"]
    lines += [f"| `{k}` | {v} |" for k,v in report["database"]["counts"].items()]
    lines += ["", "## Verification", ""]
    lines += [f"- {'PASS' if v else 'FAIL'}: `{k}`" for k,v in report["database"]["checks"].items()]
    lines += ["", "**Not evaluated:** semantic accuracy of role qualifications, current availability, or work-location eligibility.",""]
    return "\n".join(lines)


def write_failure_sidecar(output: Path, run_id: str, reason: str) -> None:
    # Do not include exception traceback, input contents, paths, query strings, or credentials.
    report={"stage":"store","status":"FAIL","run_id":run_id,"generated_at_utc":timestamp(),
            "error_type": "IMPORT_FAILED", "reason": reason[:180]}
    # The caller sets this from a controlled exception class, so no raw file data is written.
    try:
        output.parent.mkdir(parents=True,exist_ok=True)
        path=output.parent/(output.name+f".FAILED.{run_id}.json")
        path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    except OSError:
        pass


def build(input_jsonl: Path, output_dir: Path, normalization_report: Path | None,
          expected_count: int | None, allow_empty: bool) -> dict:
    if output_dir.exists():
        raise FileExistsError("Output directory already exists; choose a new output directory")
    records, input_data = check_and_read_jsonl(input_jsonl, allow_empty=allow_empty,
                                                expected_count=expected_count,
                                                normalization_report=normalization_report)
    parent=output_dir.parent
    parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix=".proofloop-stage3-",dir=parent))
    try:
        (staging/"db").mkdir()
        (staging/"reports").mkdir()
        db=staging/"db"/"jobs.sqlite3"
        conn=sqlite3.connect(db)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            initialize(conn)
            with conn:
                counts=insert_records(conn, records, input_data)
        finally:
            conn.close()
        checked=verify_database(db,records,counts)
        run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
        report={"stage":"store","status":"PASS","program_version":VERSION,
                "run_id":run_id,"generated_at_utc":timestamp(),
                "board":input_data["board"],
                "input":{"file":input_jsonl.name,**input_data,"records":len(records)},
                "database":{"file":"db/jobs.sqlite3","size_bytes":db.stat().st_size,
                            "sha256":digest(db),**checked},
                "warnings":[],
                "limitations":["Source fields are parsed-data equivalent, not a replacement for the raw original HTTP bytes.",
                               "Current job availability, eligibility and qualifications are not analyzed here."]}
        (staging/"reports"/"store_report.json").write_text(
            json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
        (staging/"reports"/"store_report.md").write_text(markdown_report(report),encoding="utf-8")
        if output_dir.exists():
            raise FileExistsError("Output directory appeared before publication")
        staging.rename(output_dir)
        return report
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description="Build verified offline Ashby SQLite bundle from Stage 1 JSONL")
    parser.add_argument("--jsonl",required=True,type=Path,help="Stage 1 normalized/jobs.jsonl")
    parser.add_argument("--output-dir",required=True,type=Path,help="New output bundle directory; must not exist")
    parser.add_argument("--normalization-report",type=Path,help="Stage 1 reports/normalization_report.json")
    parser.add_argument("--expected-count",type=int,help="Optional frozen dataset check; omit for live data")
    parser.add_argument("--allow-empty",action="store_true",help="Explicitly permit zero rows")
    args=parser.parse_args(argv)
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    try:
        out=build(args.jsonl,args.output_dir,args.normalization_report,args.expected_count,args.allow_empty)
    except (ValueError,FileNotFoundError,FileExistsError,sqlite3.Error,UnicodeError,OSError,TypeError,KeyError,json.JSONDecodeError) as e:
        # Failures are reported on stderr; only sanitized, constant error reasons in sidecar.
        print(f"FAIL: {e}",file=sys.stderr)
        code="output_exists" if isinstance(e,FileExistsError) else "input_validation_or_build_failed"
        write_failure_sidecar(args.output_dir,run_id,code)
        return 1
    print(f"PASS: SQLite stored and verified {out['database']['counts']['roles']} jobs")
    print(f"Output: {args.output_dir}")
    print(f"Input SHA-256: {out['input']['jsonl_sha256']}")
    print("Reports: reports/store_report.json and .md")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
