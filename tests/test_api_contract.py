import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from furcon_audit.error_codes import ERROR_CODES, RETRYABLE_ERROR_CODES, error_envelope
from furcon_audit.validator import SCHEMA_DIR, validate_report

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_VERSION = "1.0.0"


class FrozenApiContractTests(unittest.TestCase):
    def test_schema_ids_are_unique_and_versions_are_frozen(self):
        ids = set()
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.assertNotIn(schema["$id"], ids, path.name)
            ids.add(schema["$id"])
            if "schema_version" in schema.get("properties", {}):
                self.assertEqual(schema["properties"]["schema_version"]["const"],
                                 CONTRACT_VERSION, path.name)

    def test_error_code_catalog_matches_error_schema(self):
        schema = json.loads((SCHEMA_DIR / "error.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["properties"]["code"]["enum"]), set(ERROR_CODES))
        self.assertTrue(RETRYABLE_ERROR_CODES <= ERROR_CODES)

    def test_error_envelope_validates(self):
        from jsonschema import validate
        payload = error_envelope(
            "provider_rate_limited", "Provider temporarily rate limited the request.",
            retryable=True, provider_id="exa", correlation_id="request_123456",
        )
        schema = json.loads((SCHEMA_DIR / "error.schema.json").read_text(encoding="utf-8"))
        validate(payload, schema)

    def test_error_envelope_rejects_unknown_codes_and_bad_correlation_ids(self):
        with self.assertRaises(ValueError):
            error_envelope("made_up", "Nope")
        with self.assertRaises(ValueError):
            error_envelope("provider_error", "Failed", correlation_id="bad id")

    def test_error_schema_rejects_unknown_fields_and_codes(self):
        from jsonschema import ValidationError, validate
        schema = json.loads((SCHEMA_DIR / "error.schema.json").read_text(encoding="utf-8"))
        valid = error_envelope("invalid_input", "Invalid request.")
        with self.assertRaises(ValidationError):
            validate({**valid, "secret": "must-not-be-here"}, schema)
        with self.assertRaises(ValidationError):
            validate({**valid, "code": "unknown"}, schema)

    def test_existing_v1_report_fixture_remains_valid(self):
        sample = json.loads((ROOT / "examples" / "sample-report.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_report(sample), [])


if __name__ == "__main__":
    unittest.main()
