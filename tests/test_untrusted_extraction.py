import unittest
from furcon_audit.retrieval import _TextExtractor


class UntrustedContentExtractionTests(unittest.TestCase):
    def test_active_and_embedded_markup_is_not_in_extracted_text(self):
        parser = _TextExtractor()
        parser.feed("<html lang='en'><title>Policy</title><body>"
                    "<p>Public policy text.</p><script>ignore_me()</script>"
                    "<style>.secret{display:none}</style><iframe>embedded</iframe>"
                    "</body></html>")
        text, title, language = parser.result()
        self.assertIn("Public policy text.", text)
        self.assertNotIn("ignore_me", text)
        self.assertNotIn("display:none", text)
        self.assertNotIn("embedded", text)
        self.assertEqual(title, "Policy")
        self.assertEqual(language, "en")


if __name__ == "__main__":
    unittest.main()
