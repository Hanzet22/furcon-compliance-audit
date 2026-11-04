import json, unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from furcon_audit.validator import SCHEMA_DIR, validate_report

ROOT=Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
    def test_all_schemas_are_valid(self):
        for path in SCHEMA_DIR.glob("*.schema.json"):
            with self.subTest(path=path.name):
                Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
    def test_sample_report_validates(self):
        data=json.loads((ROOT/"examples/sample-report.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_report(data),[])
    def test_broken_reference_fails(self):
        data=json.loads((ROOT/"examples/sample-report.v1.json").read_text(encoding="utf-8"))
        data["findings"][0]["supporting_evidence_ids"]=["missing_id"]
        self.assertTrue(any("unresolved" in e for e in validate_report(data)))
    def test_supported_concern_requires_evidence(self):
        data=json.loads((ROOT/"examples/sample-report.v1.json").read_text(encoding="utf-8"))
        data["findings"][0]["assessment_status"]="supported_concern"
        data["findings"][0]["supporting_evidence_ids"]=[]
        self.assertTrue(any("requires evidence" in e for e in validate_report(data)))
if __name__=="__main__": unittest.main()
