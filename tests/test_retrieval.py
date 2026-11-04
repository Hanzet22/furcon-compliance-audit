import unittest

from furcon_audit.retrieval import (
    FetchResponse, RetrievalError, _validate_public_url, retrieve_page
)


class RetrievalPipelineTests(unittest.TestCase):
    @staticmethod
    def public_dns(*_, **__):
        return [(None, None, None, None, ("93.184.216.34", 443))]

    def test_success_preserves_raw_and_extracted_content_with_hash(self):
        body = b"<html lang='en'><head><title>Event Terms</title></head><body><h1>Terms</h1><p>Refunds apply.</p></body></html>"
        def fetcher(url, timeout, max_bytes):
            return FetchResponse(200, {"Content-Type": "text/html; charset=utf-8"}, body, url)
        result = retrieve_page("https://example.org/terms", attempt_id="attempt_demo_01",
                               fetcher=fetcher, robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["outcome"], "success")
        self.assertEqual(result["source"]["title"], "Event Terms")
        self.assertIn("Refunds apply.", result["content"]["extracted_text"])
        self.assertEqual(result["content"]["raw_text"], body.decode())
        self.assertEqual(len(result["retrieval"]["content_hash"]), 64)
        self.assertEqual(result["retrieval"]["attempt_id"], "attempt_demo_01")

    def test_robots_disallow_is_recorded_as_blocked(self):
        result = retrieve_page("https://example.org/policy",
                               fetcher=lambda *_: self.fail("must not fetch page"),
                               robots_checker=lambda *_: False, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "robots_disallowed")

    def test_robots_policy_failure_fails_closed(self):
        def broken_fetch(*_):
            raise RetrievalError("network_error", "offline")
        result = retrieve_page("https://example.org/policy",
                               fetcher=broken_fetch, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "robots_unavailable")

    def test_private_and_local_targets_are_blocked(self):
        for url in ("http://127.0.0.1/", "http://localhost/", "file:///etc/passwd"):
            with self.subTest(url=url), self.assertRaises(RetrievalError):
                _validate_public_url(url)

    def test_non_global_dns_answer_is_blocked(self):
        def private_dns(*_, **__):
            return [(None, None, None, None, ("10.0.0.5", 443))]
        with self.assertRaises(RetrievalError):
            _validate_public_url("https://internal.example", resolver=private_dns)

    def test_access_restriction_is_not_misreported_as_missing_source(self):
        def forbidden(url, timeout, max_bytes):
            return FetchResponse(403, {}, b"", url)
        result = retrieve_page("https://example.org/private", fetcher=forbidden,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "access_restricted")

    def test_unsupported_media_type_is_blocked(self):
        def pdf(url, timeout, max_bytes):
            return FetchResponse(200, {"Content-Type": "application/pdf"}, b"%PDF", url)
        result = retrieve_page("https://example.org/file.pdf", fetcher=pdf,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["outcome"], "blocked")
        self.assertEqual(result["retrieval"]["error_code"], "unsupported_media_type")

    def test_redirected_capture_uses_final_canonical_source_identity(self):
        body = b"<html><title>Final</title><body>Final policy.</body></html>"
        def fetcher(url, timeout, max_bytes):
            return FetchResponse(200, {"Content-Type": "text/html"}, body,
                                 "https://example.org/canonical")
        result = retrieve_page("https://example.org/alias", fetcher=fetcher,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["source"]["canonical_url"], "https://example.org/canonical")
        self.assertEqual(result["source"]["source_id"], result["retrieval"]["source_id"])

    def test_oversized_custom_fetcher_response_is_blocked(self):
        body = b"x" * 32
        response = FetchResponse(200, {"Content-Type": "text/plain"}, body,
                                 "https://example.org")
        result = retrieve_page("https://example.org", max_bytes=16,
                               fetcher=lambda *args: response,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["error_code"], "payload_too_large")

    def test_invalid_port_and_control_character_urls_are_blocked(self):
        for url in ("https://example.org:bad/path", "https://example.org:8443/",
                    "http://example.org:443/", "https://example.org/\nheader"):
            with self.subTest(url=url):
                with self.assertRaises(RetrievalError):
                    _validate_public_url(url, resolver=self.public_dns)

    def test_invalid_fetch_response_shape_is_recorded_not_raised(self):
        malformed = FetchResponse(200, [], b"ok", "https://example.org")
        result = retrieve_page("https://example.org", fetcher=lambda *_: malformed,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["error_code"], "invalid_fetch_response")

    def test_https_redirect_downgrade_is_blocked_before_fetch(self):
        from furcon_audit.retrieval import _validate_redirect_url
        with self.assertRaisesRegex(RetrievalError, "HTTPS redirects"):
            _validate_redirect_url("https://example.org/start", "http://example.net/target", self.public_dns)

    def test_https_redirect_to_https_is_allowed(self):
        from furcon_audit.retrieval import _validate_redirect_url
        result = _validate_redirect_url("https://example.org/start", "https://example.net/target", self.public_dns)
        self.assertEqual(result, "https://example.net/target")

    def test_https_downgrade_is_blocked(self):
        response = FetchResponse(200, {"Content-Type": "text/plain"}, b"ok",
                                 "http://example.org/final")
        result = retrieve_page("https://example.org/start", fetcher=lambda *_: response,
                               robots_checker=lambda *_: True, resolver=self.public_dns)
        self.assertEqual(result["retrieval"]["error_code"], "https_downgrade")

    def test_resource_limits_are_bounded(self):
        for kwargs in ({"max_bytes": 10_000_001}, {"max_bytes": True},
                       {"timeout": 61}, {"timeout": True}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    retrieve_page("https://example.org", **kwargs)

    def test_invalid_attempt_id_rejected(self):
        with self.assertRaises(ValueError):
            retrieve_page("https://example.org", attempt_id="INVALID!",
                          robots_checker=lambda *_: True)


if __name__ == "__main__":
    unittest.main()
