import unittest

from furcon_audit.evidence import create_evidence


class EvidenceCaptureTests(unittest.TestCase):
    def setUp(self):
        self.capture = {
            "source": {"canonical_url": "https://example.org/terms"},
            "retrieval": {
                "retrieval_id": "retrieval_demo_001",
                "outcome": "success",
                "content_hash": "a" * 64
            },
            "content": {
                "extracted_text": "Refunds are available within 14 days.",
                "language": "en",
                "final_url": "https://example.org/terms"
            }
        }

    def test_explicit_excerpt_creates_linked_evidence(self):
        record = create_evidence(self.capture, "Refunds are available within 14 days.",
                                 locator="section 2", evidence_id="evidence_demo_001")
        self.assertEqual(record["retrieval_id"], "retrieval_demo_001")
        self.assertEqual(record["source_url"], "https://example.org/terms")
        self.assertEqual(record["content_hash"], "a" * 64)
        self.assertEqual(record["original_language"], "en")

    def test_excerpt_must_match_verbatim(self):
        with self.assertRaises(ValueError):
            create_evidence(self.capture, "Refunds are always available.")

    def test_failed_retrieval_cannot_create_evidence(self):
        failed = dict(self.capture)
        failed["retrieval"] = dict(self.capture["retrieval"], outcome="blocked")
        with self.assertRaises(ValueError):
            create_evidence(failed, "Refunds are available within 14 days.")

    def test_invalid_hash_rejected(self):
        bad = dict(self.capture)
        bad["retrieval"] = dict(self.capture["retrieval"], content_hash="not-a-hash")
        with self.assertRaises(ValueError):
            create_evidence(bad, "Refunds are available within 14 days.")


if __name__ == "__main__":
    unittest.main()
