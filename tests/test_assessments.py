import unittest

from furcon_audit.assessments import create_assessment, create_finding


class AssessmentFindingTests(unittest.TestCase):
    def test_assessment_keeps_confidence_separate_from_status(self):
        item = create_assessment(question="Is the policy clear?",
            assessment_status="needs_clarification", rationale="The wording is ambiguous.",
            confidence="high", evidence_ids=["evidence_demo_001"])
        self.assertEqual(item["assessment_status"], "needs_clarification")
        self.assertEqual(item["confidence"], "high")

    def test_supported_concern_requires_assessment_and_evidence(self):
        with self.assertRaises(ValueError):
            create_finding(title="Concern", category="privacy",
                assessment_status="supported_concern", severity="high",
                confidence="medium", rationale="Reason", assessment_ids=[])

    def test_finding_preserves_contrary_evidence_and_affected_activity(self):
        item = create_finding(title="Notice clarity", category="privacy",
            assessment_status="supported_concern", severity="moderate",
            confidence="medium", rationale="Evidence supports a limited concern.",
            assessment_ids=["assessment_demo_001"],
            supporting_evidence_ids=["evidence_support_001"],
            contrary_evidence_ids=["evidence_context_001"],
            affected_actor="Organizer", affected_activity="Registration data collection",
            recommendation="Clarify the notice.")
        self.assertEqual(item["contrary_evidence_ids"], ["evidence_context_001"])
        self.assertEqual(item["affected_activity"], "Registration data collection")

    def test_no_issue_observed_is_not_a_compliance_certificate(self):
        item = create_finding(title="Refund policy", category="refund",
            assessment_status="no_issue_observed", severity="informational",
            confidence="low", rationale="No issue established within this scope.",
            assessment_ids=[])
        self.assertEqual(item["assessment_status"], "no_issue_observed")


if __name__ == "__main__":
    unittest.main()
