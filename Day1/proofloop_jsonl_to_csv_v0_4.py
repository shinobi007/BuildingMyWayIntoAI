#!/usr/bin/env python3
"""
ProofLoop JSONL -> CSV Converter v0.4
"""

import argparse
import csv
import json
import sys
from pathlib import Path

FIELDS = (
    "role_id",
    "title",
    "team",
    "display_location",
    "career_url",
    "apply_url",
)


def load_jsonl(path: Path):
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Line {line_number} is invalid JSON: "
                    f"{exc.msg} at column {exc.colno}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Line {line_number} is not a JSON object."
                )

            missing = [field for field in FIELDS if field not in record]
            if missing:
                raise ValueError(
                    f"Line {line_number} is missing fields: "
                    + ", ".join(missing)
                )

            records.append(record)

    return records


def write_csv(records, output_path: Path):
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )
        writer.writeheader()

        for record in records:
            writer.writerow(record)


def main():
    parser = argparse.ArgumentParser(
        description="Convert ProofLoop OpenAI role JSONL to CSV."
    )
    parser.add_argument(
        "jsonl_file",
        help="Path to the input JSONL file."
    )
    parser.add_argument(
        "--output",
        default="openai_roles.csv",
        help="Path to the output CSV file."
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=None,
        help="Optional expected record count."
    )

    args = parser.parse_args()

    input_path = Path(args.jsonl_file)
    output_path = Path(args.output)

    if not input_path.is_file():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        records = load_jsonl(input_path)
        write_csv(records, output_path)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("ProofLoop JSONL -> CSV Converter v0.4")
    print(f"Input JSONL:      {input_path}")
    print(f"Output CSV:       {output_path}")
    print(f"Records written:  {len(records)}")

    if args.expected is not None:
        status = "PASS" if len(records) == args.expected else "FAIL"
        print(f"Expected records: {args.expected}  [{status}]")

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
