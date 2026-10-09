#!/usr/bin/env python3
"""
ProofLoop OpenAI Role Validator v0.3.1

Independent validator for the canonical JSONL role inventory.

Fix in v0.3.1:
- an --expected count mismatch is now a real validation failure
- the process exits nonzero when the expected count does not match
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = (
    "role_id",
    "title",
    "team",
    "display_location",
    "career_url",
    "apply_url",
)


def load_jsonl(path: Path):
    records = []
    errors = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            if not line:
                errors.append(f"Line {line_number}: blank line")
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(
                    f"Line {line_number}: invalid JSON "
                    f"({exc.msg} at column {exc.colno})"
                )
                continue

            if not isinstance(record, dict):
                errors.append(
                    f"Line {line_number}: expected a JSON object, "
                    f"got {type(record).__name__}"
                )
                continue

            records.append(record)

    return records, errors


def validate_records(records):
    issues = []
    career_urls = []
    apply_urls = []

    for index, record in enumerate(records, start=1):
        for field in REQUIRED_FIELDS:
            if field not in record:
                issues.append(f"Record {index}: missing field '{field}'")
            elif record[field] is None or str(record[field]).strip() == "":
                issues.append(f"Record {index}: blank field '{field}'")

        role_id = record.get("role_id")
        if role_id != index:
            issues.append(
                f"Record {index}: role_id is {role_id!r}; expected {index}"
            )

        career_url = str(record.get("career_url", ""))
        if "openai.com/careers/" not in career_url:
            issues.append(
                f"Record {index}: unexpected career_url: {career_url!r}"
            )

        apply_url = str(record.get("apply_url", ""))
        if "jobs.ashbyhq.com/openai/" not in apply_url:
            issues.append(
                f"Record {index}: unexpected apply_url: {apply_url!r}"
            )

        if career_url:
            career_urls.append(career_url)
        if apply_url:
            apply_urls.append(apply_url)

    if len(career_urls) != len(set(career_urls)):
        issues.append("Duplicate career_url values detected")

    if len(apply_urls) != len(set(apply_urls)):
        issues.append("Duplicate apply_url values detected")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Independently validate a ProofLoop OpenAI JSONL role inventory."
    )
    parser.add_argument("jsonl_file", help="Path to the JSONL role inventory.")
    parser.add_argument(
        "--expected",
        type=int,
        default=None,
        help="Optional expected number of valid records.",
    )
    args = parser.parse_args()

    jsonl_path = Path(args.jsonl_file)

    if not jsonl_path.is_file():
        print(f"ERROR: File not found: {jsonl_path}", file=sys.stderr)
        return 2

    records, parse_errors = load_jsonl(jsonl_path)
    validation_issues = validate_records(records)

    count_matches = (
        args.expected is None or len(records) == args.expected
    )

    print("ProofLoop OpenAI Role Validator v0.3.1")
    print(f"JSONL file:       {jsonl_path}")
    print(f"Parsed records:   {len(records)}")

    if args.expected is not None:
        status = "PASS" if count_matches else "FAIL"
        print(f"Expected records: {args.expected}  [{status}]")

    print(f"JSON parse errors:    {len(parse_errors)}")
    print(f"Validation issues:    {len(validation_issues)}")

    problems = list(parse_errors) + list(validation_issues)

    if not count_matches:
        problems.append(
            f"Record count mismatch: found {len(records)}, "
            f"expected {args.expected}"
        )

    if problems:
        print("\nProblems:")
        for problem in problems:
            print(f"- {problem}")
        print("\nRESULT: FAIL")
        return 1

    print("\nRESULT: PASS")
    print("The saved JSONL passed all current v0.3.1 integrity checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
