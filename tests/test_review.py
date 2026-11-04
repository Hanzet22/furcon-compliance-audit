import unittest

from furcon_audit.review import (
    create_review, mark_review_stale, requires_human_review, review_gate, transition_review
)


class HumanReviewTests(unittest.TestCase):
    def test_high_impact_and_legal_applicability_require_review(self):
        self.assertTrue(requires_human_review(severity="high"))
        self.assertTrue(requires_human_review(applicability_status="potentially_applicable"))
        self.assertFalse(requires_human_review(severity="low", assessment_status="no_issue_observed"))

    def test_review_transition_to_accepted_requires_approval(self):
        review = create_review(target_ids=["finding_demo_001"], reviewer_role="qualified reviewer",
                               revision="rev-1")
        review = transition_review(review, "in_review")
        with self.assertRaises(ValueError):
            transition_review(review, "accepted", decision="defer")
        accepted = transition_review(review, "accepted", decision="approve")
        self.assertEqual(accepted["review_status"], "accepted")

    def test_material_revision_change_marks_review_stale(self):
        review = create_review(target_ids=["finding_demo_001"], reviewer_role="reviewer",
                               revision="rev-1", review_status="accepted", decision="approve")
        stale = mark_review_stale(review, "rev-2")
        self.assertEqual(stale["review_status"], "stale")
        self.assertEqual(review["review_status"], "accepted")

    def test_review_gate_requires_current_revision(self):
        review = create_review(target_ids=["finding_demo_001"], reviewer_role="reviewer",
                               revision="rev-1", review_status="accepted", decision="approve")
        self.assertTrue(review_gate("finding_demo_001", "rev-1", [review])["accepted"])
        self.assertFalse(review_gate("finding_demo_001", "rev-2", [review])["accepted"])

    def test_invalid_transition_rejected(self):
        review = create_review(target_ids=["finding_demo_001"], reviewer_role="reviewer",
                               revision="rev-1")
        with self.assertRaises(ValueError):
            transition_review(review, "accepted")


if __name__ == "__main__":
    unittest.main()
