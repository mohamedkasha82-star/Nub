import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "nub-record.schema.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "record-valid-unknown.json"


class RecordSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema, format_checker=FormatChecker()
        )
        cls.valid_record = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_schema_is_valid_draft_2020_12(self):
        self.assertEqual(
            self.schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_synthetic_unknown_record_is_valid(self):
        self.assertEqual(list(self.validator.iter_errors(self.valid_record)), [])

    def test_required_rights_field_cannot_be_omitted(self):
        record = json.loads(json.dumps(self.valid_record))
        del record["rights"]
        self.assertTrue(list(self.validator.iter_errors(record)))

    def test_unknown_values_are_valid_and_preserved(self):
        self.assertEqual(self.valid_record["rights"]["status"], "unknown")
        self.assertEqual(self.valid_record["provenance"]["source_status"], "unknown")
        self.assertEqual(self.valid_record["access"]["level"], "not_decided")
        self.assertEqual(self.valid_record["review_state"]["status"], "unreviewed")
        self.assertEqual(list(self.validator.iter_errors(self.valid_record)), [])

    def test_rights_and_consent_are_separate_fields(self):
        record = json.loads(json.dumps(self.valid_record))
        record["consent"] = {"status": "unknown"}
        self.assertEqual(list(self.validator.iter_errors(record)), [])
        self.assertEqual(record["rights"]["status"], "unknown")
        self.assertEqual(record["consent"]["status"], "unknown")

    def test_unknown_enum_value_is_rejected(self):
        record = json.loads(json.dumps(self.valid_record))
        record["access"]["level"] = "public-by-default"
        self.assertTrue(list(self.validator.iter_errors(record)))

    def test_unrecognized_fields_are_rejected(self):
        record = json.loads(json.dumps(self.valid_record))
        record["verified"] = True
        self.assertTrue(list(self.validator.iter_errors(record)))

    def test_malformed_date_format_is_rejected(self):
        record = json.loads(json.dumps(self.valid_record))
        record["provenance"]["date_created"] = "not-a-date"
        self.assertTrue(list(self.validator.iter_errors(record)))


if __name__ == "__main__":
    unittest.main()
