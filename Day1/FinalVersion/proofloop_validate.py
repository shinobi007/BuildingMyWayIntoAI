#!/usr/bin/env python3
"""ProofLoop Ashby Stage 4: independent read-only, source-to-SQLite validator.

No imports from the fetcher, normalizer, or database builder. Only writes a NEW
validation report directory. Checks original snapshot -> JSONL -> relational
SQLite data and separately checks normalization/store report claims.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import tempfile
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.4.0"
MAX_ERRORS = 35
TABLES = ("roles", "secondary_locations", "compensation_tiers", "compensation_components",
          "compensation_summary_components")
SOURCE_TO_CANONICAL = {
    "id": "id", "title": "title", "department": "department", "team": "team",
    "employmentType": "employment_type", "location": "location",
    "shouldDisplayCompensationOnJobPostings": "should_display_compensation",
    "secondaryLocations": "secondary_locations", "publishedAt": "published_at",
    "isListed": "is_listed", "isRemote": "is_remote", "workplaceType": "workplace_type",
    "address": "address", "jobUrl": "job_url", "applyUrl": "apply_url",
    "descriptionHtml": "description_html", "descriptionPlain": "description_plain",
    "compensation": "compensation",
}
SCALARS = {
    "title": "title", "department": "department", "team": "team",
    "employment_type": "employment_type", "location": "location", "published_at": "published_at",
    "is_listed": "is_listed", "is_remote": "is_remote", "workplace_type": "workplace_type",
    "should_display_compensation": "should_display_compensation", "job_url": "job_url",
    "apply_url": "apply_url", "description_plain": "description_plain",
    "description_html": "description_html",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024*1024), b""):
            h.update(part)
    return h.hexdigest()


def reject_nan(value: str):
    raise ValueError(f"Non-JSON numeric constant: {value}")


def read_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f, parse_constant=reject_nan)


def read_json_text(value: str):
    return json.loads(value, parse_constant=reject_nan)


def flag(value):
    return None if value is None else int(value) if type(value) is bool else "INVALID_BOOL"


class Audit:
    def __init__(self):
        self.checks: dict[str,bool] = {}
        self.details: dict[str,object] = {}
        self.errors: list[str] = []
        self.error_count = 0

    def check(self, name: str, success: bool, issue: str | None = None):
        self.checks[name] = bool(success)
        if not success:
            self.problem(issue or name)

    def problem(self, error: str):
        self.error_count += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(str(error)[:250])


def validate(snapshot: Path, jsonl: Path, database: Path,
             normalization_report: Path, store_report: Path) -> dict:
    audit = Audit()
    for name, path in (("snapshot",snapshot),("jsonl",jsonl),("database",database),
                       ("normalization_report",normalization_report),("store_report",store_report)):
        if not path.is_file():
            raise ValueError(f"Required {name} file does not exist")

    snapshot_hash, jsonl_hash, db_hash = hash_file(snapshot), hash_file(jsonl), hash_file(database)
    norm, store = read_json(normalization_report), read_json(store_report)
    if not isinstance(norm,dict) or not isinstance(store,dict):
        raise ValueError("Input reports must be JSON objects")

    audit.check("normalization_report_status", norm.get("stage") == "normalize" and norm.get("status") == "PASS")
    audit.check("store_report_status", store.get("stage") == "store" and store.get("status") == "PASS")
    audit.check("normalization_report_hashes", norm.get("normalized_sha256") == jsonl_hash and norm.get("audit",{}).get("source_sha256") == snapshot_hash)
    audit.check("store_report_hashes", store.get("input",{}).get("jsonl_sha256") == jsonl_hash and store.get("input",{}).get("source_sha256") == snapshot_hash and store.get("database",{}).get("sha256") == db_hash)
    audit.check("report_run_identity", norm.get("board") == store.get("board") == store.get("input",{}).get("board"))

    payload = read_json(snapshot)
    if not isinstance(payload, dict) or not isinstance(payload.get("jobs"), list):
        raise ValueError("Source snapshot must contain jobs array")
    source_jobs = payload["jobs"]
    normalized = []
    with jsonl.open("r",encoding="utf-8") as f:
        for line_number, line in enumerate(f,1):
            if not line.strip():
                raise ValueError(f"Blank JSONL line {line_number}")
            rec = read_json_text(line)
            if not isinstance(rec,dict) or not all(isinstance(rec.get(k),dict) for k in ("raw","canonical","provenance")):
                raise ValueError(f"JSONL line {line_number} lacks required objects")
            normalized.append(rec)
    audit.details["source_records"] = len(source_jobs)
    audit.details["normalized_records"] = len(normalized)
    audit.check("source_normalized_count",len(source_jobs) == len(normalized))
    audit.check("normalization_report_count",norm.get("audit",{}).get("record_count") == len(normalized))
    audit.check("store_report_count",store.get("input",{}).get("records") == len(normalized))

    raw_equal = canon_equal = ordinal_equal = prov_equal = True
    seen = set()
    seen_order = set()
    board = norm.get("board")
    for i,rec in enumerate(normalized):
        raw, can, prov = rec["raw"],rec["canonical"],rec["provenance"]
        if i < len(source_jobs) and raw != source_jobs[i]:
            raw_equal = False
        if prov.get("source_index") != i+1:
            ordinal_equal = False
        if prov.get("snapshot_sha256") != snapshot_hash or prov.get("board") != board or prov.get("provider") != "ashby":
            prov_equal = False
        if not isinstance(can.get("id"),str) or not can.get("id") or can["id"] in seen or can["id"] != raw.get("id"):
            canon_equal = False
        else:
            seen.add(can["id"])
        for source_key,canonical_key in SOURCE_TO_CANONICAL.items():
            # Stage 1 explicitly retains all observed fields in its canonical record.
            expected_value = raw.get(source_key)
            if source_key in ("title", "team", "department", "location") and isinstance(expected_value, str):
                expected_value = expected_value.strip()
            if can.get(canonical_key) != expected_value:
                canon_equal=False
                break
        seen_order.add(prov.get("source_index"))
    audit.check("source_raw_exact_parsed",raw_equal,"Source jobs differ from JSONL raw records")
    audit.check("canonical_projection_exact",canon_equal,"Canonical fields or IDs differ from raw source")
    audit.check("source_ordinal_exact",ordinal_equal and len(seen_order)==len(normalized),"Original job positions differ from provenance indices")
    audit.check("source_provenance_exact",prov_equal,"Provenance hash, provider, or board differs")
    audit.check("source_unique_ids",len(seen)==len(normalized))

    expected_counts = Counter({key:0 for key in TABLES})
    expected_counts["roles"] = len(normalized)
    for rec in normalized:
        can = rec["canonical"]
        locs=can.get("secondary_locations",[])
        comp=can.get("compensation",{})
        tiers=comp.get("compensationTiers",[])
        sums=comp.get("summaryComponents",[])
        if not isinstance(locs,list) or not isinstance(tiers,list) or not isinstance(sums,list):
            raise ValueError("Source normalized nested structure invalid")
        expected_counts["secondary_locations"] += len(locs)
        expected_counts["compensation_tiers"] += len(tiers)
        expected_counts["compensation_summary_components"] += len(sums)
        for t in tiers:
            if not isinstance(t,dict) or not isinstance(t.get("components"),list):
                raise ValueError("Source normalized compensation tier invalid")
            expected_counts["compensation_components"] += len(t["components"])

    # Connect with URI read-only plus query_only; never call the Stage 3 builder.
    uri=database.resolve().as_uri()+"?mode=ro"
    conn=sqlite3.connect(uri,uri=True)
    conn.row_factory=sqlite3.Row
    try:
        conn.execute("PRAGMA query_only=ON")
        audit.check("sqlite_integrity", conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
        audit.check("foreign_keys",len(conn.execute("PRAGMA foreign_key_check").fetchall())==0)
        objects={row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required=set(TABLES)|{"build_metadata"}
        audit.check("required_tables",required.issubset(objects))
        if not required.issubset(objects):
            audit.details["missing_tables"] = sorted(required - objects)
            return finalize(audit,snapshot_hash,jsonl_hash,db_hash,expected_counts)
        counts={name:conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] for name in TABLES}
        audit.details["database_counts"] = counts
        audit.details["expected_counts"] = dict(expected_counts)
        audit.check("relational_row_counts",counts==dict(expected_counts),"Child-table or role counts differ from source-derived totals")
        audit.check("store_report_database_counts",store.get("database",{}).get("counts")==counts)

        metadata={r["key"]:read_json_text(r["value_json"]) for r in conn.execute("SELECT key,value_json FROM build_metadata")}
        audit.check("build_metadata",metadata.get("normalized_sha256")==jsonl_hash and
                    metadata.get("snapshot_sha256")==snapshot_hash and
                    metadata.get("record_count")==len(normalized) and metadata.get("board")==board)
        rows=conn.execute("SELECT * FROM roles ORDER BY source_index").fetchall()
        raw_ok=canonical_ok=provenance_ok=scalar_ok=children_ok=True
        if len(rows) != len(normalized):
            raw_ok=canonical_ok=provenance_ok=scalar_ok=children_ok=False
        for i,(row, rec) in enumerate(zip(rows,normalized)):
            raw,can,prov=rec["raw"],rec["canonical"],rec["provenance"]
            rid=can.get("id")
            if row["id"]!=rid or row["source_index"]!=i+1 or row["source_sha256"]!=snapshot_hash or row["board"]!=board:
                provenance_ok=False
            for col,field in SCALARS.items():
                val=can.get(field)
                if field in ("is_listed","is_remote","should_display_compensation"):
                    val=flag(val)
                if row[col]!=val:
                    scalar_ok=False
                    break
            if read_json_text(row["raw_json"])!=raw:
                raw_ok=False
            if read_json_text(row["canonical_json"])!=can:
                canonical_ok=False
            if read_json_text(row["provenance_json"])!=prov:
                provenance_ok=False
            if read_json_text(row["address_json"])!=can.get("address") or read_json_text(row["compensation_json"])!=can.get("compensation"):
                scalar_ok=False
            expected_tables = (
                ("secondary_locations",can["secondary_locations"],None),
                ("compensation_tiers",can["compensation"]["compensationTiers"],None),
                ("compensation_summary_components",can["compensation"]["summaryComponents"],None),
            )
            for tab,expected,_ in expected_tables:
                got=conn.execute(f"SELECT * FROM {tab} WHERE role_id=? ORDER BY ordinal",(rid,)).fetchall()
                if len(got)!=len(expected):
                    children_ok=False
                for j,(child,source_obj) in enumerate(zip(got,expected)):
                    if child["ordinal"]!=j or read_json_text(child["raw_json"])!=source_obj:
                        children_ok=False
                    if tab=="secondary_locations" and (child["location"]!=source_obj.get("location") or read_json_text(child["address_json"])!=source_obj.get("address")):
                        children_ok=False
                    if tab=="compensation_tiers" and any(child[col]!=source_obj.get(src) for col,src in (("tier_id","id"),("tier_summary","tierSummary"),("title","title"),("additional_information","additionalInformation"))):
                        children_ok=False
                    if tab=="compensation_summary_components" and not match_component(child,source_obj):
                        children_ok=False
            for ti,tier in enumerate(can["compensation"]["compensationTiers"]):
                got=conn.execute("SELECT * FROM compensation_components WHERE role_id=? AND tier_ordinal=? ORDER BY ordinal",(rid,ti)).fetchall()
                expected=tier["components"]
                if len(got)!=len(expected):
                    children_ok=False
                for j,(child,source_obj) in enumerate(zip(got,expected)):
                    if child["ordinal"]!=j or child["tier_ordinal"]!=ti or read_json_text(child["raw_json"])!=source_obj or not match_component(child,source_obj):
                        children_ok=False
                    if child["component_id"]!=source_obj.get("id") or child["summary"]!=source_obj.get("summary"):
                        children_ok=False
        audit.check("db_source_raw_objects",raw_ok,"DB raw job content differs from source")
        audit.check("db_canonical_objects",canonical_ok,"DB canonical objects differ from JSONL")
        audit.check("db_provenance",provenance_ok,"DB identity, ordering, or provenance differs")
        audit.check("db_scalar_projection",scalar_ok,"DB scalar column differs from normalized source")
        audit.check("db_all_child_rows",children_ok,"DB child records differ from normalized source")
    finally:
        conn.close()
    return finalize(audit,snapshot_hash,jsonl_hash,db_hash,expected_counts)


def match_component(row, obj: dict) -> bool:
    for col,src in (("compensation_type","compensationType"),("interval","interval"),
                    ("currency_code","currencyCode"),("min_value","minValue"),("max_value","maxValue")):
        if row[col] != obj.get(src):
            return False
    return True


def finalize(audit: Audit, snapshot_hash: str,jsonl_hash: str,db_hash: str, expected: Counter) -> dict:
    return {"stage":"independent_validation","status":"PASS" if all(audit.checks.values()) else "FAIL",
            "program_version":VERSION,"generated_at_utc":now(),
            "checks":audit.checks,"passed":sum(audit.checks.values()),
            "failed":sum(not x for x in audit.checks.values()),
            "diagnostics":audit.errors,"diagnostics_truncated":audit.error_count>len(audit.errors),
            "files":{"snapshot_sha256":snapshot_hash,"jsonl_sha256":jsonl_hash,"sqlite_sha256":db_hash},
            "details":audit.details,"limitations":[
                "Verifies source-to-database data consistency, not current job availability or employer statements.",
                "Source-to-canonical field checks cover the 18 known Ashby source fields; unknown source fields are preserved in raw JSON.",
                "Does not assess candidate qualifications, location eligibility, or semantic truth of text."]}


def markdown(report: dict) -> str:
    lines=["# ProofLoop Stage 4 — Independent Validation Report","",
           f"**Status:** {report['status']}",
           f"- Checks: **{report['passed']} PASS / {report['failed']} FAIL**",
           f"- Generated (UTC): `{report['generated_at_utc']}`",
           "", "## Input fingerprints", ""]
    for k,v in report["files"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines += ["", "## Checks", "", "| Check | Result |", "| --- | --- |"]
    for k,v in report["checks"].items():
        lines.append(f"| `{k}` | {'PASS' if v else 'FAIL'} |")
    lines += ["", "## Expected table counts", ""]
    for k,v in report["details"].get("expected_counts",{}).items():
        lines.append(f"- `{k}`: {v}")
    if report["diagnostics"]:
        lines += ["", "## Failures", ""]
        lines += [f"- {item}" for item in report["diagnostics"]]
    lines += ["", "## Boundaries", ""]
    lines += [f"- {v}" for v in report["limitations"]]
    return "\n".join(lines)+"\n"


def write_report(report: dict, output: Path):
    if output.exists():
        raise FileExistsError("Report output directory already exists")
    output.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix=".proofloop-validation-",dir=output.parent))
    try:
        (staging/"validation_report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
        (staging/"validation_report.md").write_text(markdown(report),encoding="utf-8")
        if output.exists():
            raise FileExistsError("Report output directory appeared during validation")
        staging.rename(output)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description="Independent read-only Ashby snapshot/JSONL/SQLite verification")
    p.add_argument("--snapshot",type=Path,required=True)
    p.add_argument("--jsonl",type=Path,required=True)
    p.add_argument("--db",type=Path,required=True)
    p.add_argument("--normalization-report",type=Path,required=True)
    p.add_argument("--store-report",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output_dir.exists():
        print("FAIL: report directory already exists; choose a new output directory",file=sys.stderr)
        return 2
    try:
        report=validate(a.snapshot,a.jsonl,a.db,a.normalization_report,a.store_report)
    except (OSError,sqlite3.Error,UnicodeError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        report={"stage":"independent_validation","status":"FAIL","program_version":VERSION,
                "generated_at_utc":now(),"checks":{"validation_completed":False},"passed":0,"failed":1,
                "diagnostics":["Unable to complete validation: "+type(exc).__name__],
                "diagnostics_truncated":False,"files":{},"details":{},
                "limitations":["No independent consistency conclusion is possible for malformed or missing inputs."]}
        try:
            write_report(report,a.output_dir)
        except (OSError,FileExistsError):
            pass
        print(f"FAIL: unable to complete independent validation ({type(exc).__name__})",file=sys.stderr)
        return 2
    try:
        write_report(report,a.output_dir)
    except (OSError,FileExistsError) as exc:
        print(f"FAIL: unable to publish validation report ({type(exc).__name__})",file=sys.stderr)
        return 2
    print(f"{report['status']}: independent checks {report['passed']} passed, {report['failed']} failed")
    print(f"Output: {a.output_dir}")
    print("Reports: validation_report.json and .md")
    return 0 if report['status']=="PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
