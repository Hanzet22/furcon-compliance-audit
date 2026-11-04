import unittest

from furcon_audit.legal import create_legal_authority, create_legal_proposition


class LegalAuthorityTests(unittest.TestCase):
    def test_authority_preserves_issuer_dates_and_status(self):
        authority = create_legal_authority(
            jurisdiction="Example jurisdiction", authority_type="legislation",
            title="Example Data Protection Act", issuing_body="Legislature",
            official_url="https://example.org/law", publication_date="2024-01-01",
            effective_date="2024-07-01", authority_status="current",
            authority_id="authority_demo_001")
        self.assertEqual(authority["authority_status"], "current")
        self.assertEqual(authority["issuing_body"], "Legislature")
        self.assertEqual(authority["effective_date"], "2024-07-01")

    def test_unknown_status_is_explicit_default(self):
        authority = create_legal_authority(
            jurisdiction="Example", authority_type="secondary_commentary", title="Commentary")
        self.assertEqual(authority["authority_status"], "unknown")

    def test_invalid_authority_type_or_date_rejected(self):
        with self.assertRaises(ValueError):
            create_legal_authority(jurisdiction="X", authority_type="blog", title="A title")
        with self.assertRaises(ValueError):
            create_legal_authority(jurisdiction="X", authority_type="legislation",
                                   title="A title", effective_date="July 2024")

    def test_proposition_requires_authority_and_explicit_binding_status(self):
        proposition = create_legal_proposition(
            statement="The provision requires a controller to provide notice.",
            authority_ids=["authority_demo_001"], binding_status="binding",
            provision_reference="Section 4", proposition_id="proposition_demo_001")
        self.assertEqual(proposition["binding_status"], "binding")
        self.assertEqual(proposition["authority_ids"], ["authority_demo_001"])

    def test_proposition_rejects_duplicate_authorities(self):
        with self.assertRaises(ValueError):
            create_legal_proposition(statement="Rule",
                                     authority_ids=["authority_one", "authority_one"])


if __name__ == "__main__":
    unittest.main()
