import unittest

from furcon_audit.retrieval import (
    FetchResponse, RetrievalError, _validate_public_url, retrieve_page
)


class RetrievalPipelineTests(unittest.TestCase):
    def test_success_preserves_raw_and_extracted_content_with_hash(self):
        body = b"<html lang='en'><head><title>Event Terms</title></head><body><h1>Terms</h1><p>Refunds apply.</p></body></html>"
        def fetcher(url, timeout, max_bytes):
            return FetchResponse(200, {"Content-Type": "text/html; charset=utf-8"}, body, url)
        result = retrieve_page("https://example.org/terms", attempt_id="attempt_demo_01",
                               fetcher=fetcher, robots_checker=lambda *_: True)
        self.assertEqual(result["retrieval"]["outcome"], "success")
        self.assertEqual(result["source"]["title"], "Event Terms")
        self.assertIn("Refunds apply.", result["content"]["extracted_text"])
        self.assertEqual(result["content"]["raw_text"], body.decode())
        self.assertEqual(len(result["retrieval"]["content_hash"]), 64)
        self.assertEqual(result["retrieval"]["attempt_id"], "attempt_demo_01")

    def test_robots_disallow_is_recorded_as_blocked(self):
        result = retrieve_page("https://example.org/policy",
                               fetcher=lambda *_: self.fail("must not fetch page"),
                               robots_checker=lambda *_: False)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "robots_disallowed")

    def test_robots_policy_failure_fails_closed(self):
        def broken(*_):
            raise RetrievalError("network_error", "offline")
        result = retrieve_page("https://example.org/policy",
                               fetcher=lambda *_: self.fail("must not fetch page"),
                               robots_checker=broken)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "robots_unavailable")

    def test_private_and_local_targets_are_blocked(self):
        for url in ("http://127.0.0.1/", "http://localhost/", "file:///etc/passwd"):
            with self.subTest(url=url), self.assertRaises(RetrievalError):
                _validate_public_url(url)

    def test_non_global_dns_answer_is_blocked(self):
        def private_dns(*_):
            return [(None, None, None, None, ("10.0.0.5", 443))]
        with self.assertRaises(RetrievalError):
            _validate_public_url("https://internal.example", resolver=private_dns)

    def test_access_restriction_is_not_misreported_as_missing_source(self):
        def forbidden(url, timeout, max_bytes):
            return FetchResponse(403, {}, b"", url)
        result = retrieve_page("https://example.org/private", fetcher=forbidden,
                               robots_checker=lambda *_: True)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "access_restricted")

    def test_unsupported_media_type_is_blocked(self):
        def pdf(url, timeout, max_bytes):
            return FetchResponse(200, {"Content-Type": "application/pdf"}, b"%PDF", url)
        result = retrieve_page("https://example.org/file.pdf", fetcher=pdf,
                               robots_checker=lambda *_: True)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "unsupported_media_type")

    def test_invalid_attempt_id_rejected(self):
        with self.assertRaises(ValueError):
            retrieve_page("https://example.org", attempt_id="INVALID!",
                          robots_checker=lambda *_: True)


if __name__ == "__main__":
    unittest.main()
