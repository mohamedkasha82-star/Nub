#!/usr/bin/env python3
"""Validate NŪB record JSON against the draft record schema.

This is a deterministic structure check, not a rights, consent, authenticity,
community-review, or scholarly-verification decision.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: cannot read valid JSON: {exc}") from exc


def validate_records(schema_path: Path, record_paths: list[Path]) -> int:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    failures = 0

    for path in record_paths:
        try:
            record = load_json(path)
        except ValueError as exc:
            print(f"FAIL {exc}", file=sys.stderr)
            failures += 1
            continue

        errors = sorted(validator.iter_errors(record), key=lambda error: list(map(str, error.absolute_path)))
        if errors:
            failures += 1
            print(f"FAIL {path}")
            for error in errors:
                location = ".".join(str(part) for part in error.absolute_path) or "$"
                print(f"  - {location}: {error.message}")
        else:
            print(f"PASS {path}")

    if failures:
        print(f"\n{failures} record file(s) failed validation.", file=sys.stderr)
        return 1
    print(f"\nValidated {len(record_paths)} record file(s); no schema errors found.")
    print("Reminder: schema validity does not establish rights, consent, authenticity, or review.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=Path("schemas/nub-record.schema.json"))
    parser.add_argument("records", nargs="+", type=Path, help="JSON record file(s) to validate")
    args = parser.parse_args()
    return validate_records(args.schema, args.records)


if __name__ == "__main__":
    raise SystemExit(main())
