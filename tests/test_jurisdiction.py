import unittest

from furcon_audit.jurisdiction import create_jurisdiction_assessment


class JurisdictionAssessmentTests(unittest.TestCase):
    def test_assessment_records_separate_scope_factors(self):
        item = create_jurisdiction_assessment(
            regime="Example privacy regime", actor="Organizer",
            activity="Collecting attendee registration data",
            applicability_status="potentially_applicable",
            rationale="Territorial and material scope require confirmation.",
            territorial_scope="unclear", material_scope="supported",
            threshold_status="not_assessed", exemption_status="unclear",
            unresolved_facts=["Organizer establishment", "Processing volume"])
        self.assertEqual(item["territorial_scope"], "unclear")
        self.assertEqual(item["material_scope"], "supported")
        self.assertEqual(item["applicability_status"], "potentially_applicable")

    def test_supported_status_requires_legal_proposition(self):
        with self.assertRaises(ValueError):
            create_jurisdiction_assessment(
                regime="R", actor="A", activity="P",
                applicability_status="applicable_supported", rationale="Supported.")

    def test_nationality_only_reasoning_is_not_encoded_as_a_factor(self):
        item = create_jurisdiction_assessment(
            regime="R", actor="Organizer", activity="Processing",
            applicability_status="not_established",
            rationale="Attendee nationality alone is insufficient.")
        self.assertEqual(item["territorial_scope"], "not_assessed")
        self.assertIn("not infer applicability solely", item["methodology_note"])

    def test_invalid_factor_rejected(self):
        with self.assertRaises(ValueError):
            create_jurisdiction_assessment(
                regime="R", actor="A", activity="P",
                applicability_status="not_assessed", rationale="Pending",
                territorial_scope="yes")


if __name__ == "__main__":
    unittest.main()
