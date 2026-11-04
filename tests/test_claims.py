import unittest

from furcon_audit.claims import create_claim, summarize_evidence_independence


class ClaimLifecycleTests(unittest.TestCase):
    def test_claim_records_explicit_evidence_relationships(self):
        claim = create_claim("The event publishes refund terms.", "Organizer",
            [{"evidence_id": "evidence_demo_001", "relationship": "supports"}],
            claim_type="organizer_statement", claim_id="claim_demo_001")
        self.assertEqual(claim["verification_status"], "unverified")
        self.assertEqual(claim["evidence_ids"], ["evidence_demo_001"])
        self.assertEqual(claim["evidence_relations"][0]["relationship"], "supports")

    def test_duplicate_or_invalid_relationship_is_rejected(self):
        with self.assertRaises(ValueError):
            create_claim("A claim", "Actor", [
                {"evidence_id": "evidence_demo_001", "relationship": "supports"},
                {"evidence_id": "evidence_demo_001", "relationship": "contradicts"}])
        with self.assertRaises(ValueError):
            create_claim("A claim", "Actor", [
                {"evidence_id": "evidence_demo_001", "relationship": "proves_law"}])

    def test_same_source_is_counted_once_even_with_multiple_evidence_records(self):
        claim = {
            "evidence_relations": [
                {"evidence_id": "evidence_one", "relationship": "supports"},
                {"evidence_id": "evidence_two", "relationship": "supports"},
                {"evidence_id": "evidence_three", "relationship": "contradicts"}
            ]
        }
        report = {
            "evidence": [
                {"evidence_id": "evidence_one", "retrieval_id": "retrieval_one"},
                {"evidence_id": "evidence_two", "retrieval_id": "retrieval_two"},
                {"evidence_id": "evidence_three", "retrieval_id": "retrieval_three"}
            ],
            "retrievals": [
                {"retrieval_id": "retrieval_one", "source_id": "source_same"},
                {"retrieval_id": "retrieval_two", "source_id": "source_same"},
                {"retrieval_id": "retrieval_three", "source_id": "source_other"}
            ]
        }
        result = summarize_evidence_independence(claim, report)
        self.assertEqual(result["distinct_source_counts"]["supports"], 1)
        self.assertEqual(result["distinct_source_counts"]["contradicts"], 1)

    def test_missing_evidence_is_reported_not_assumed(self):
        result = summarize_evidence_independence(
            {"evidence_relations": [{"evidence_id": "evidence_missing", "relationship": "supports"}]},
            {"evidence": [], "retrievals": []})
        self.assertEqual(result["unresolved_evidence_ids"], ["evidence_missing"])
        self.assertEqual(result["distinct_source_counts"]["supports"], 0)


if __name__ == "__main__":
    unittest.main()
