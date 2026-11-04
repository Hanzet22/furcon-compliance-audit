import json
import unittest

from furcon_audit.capabilities import CapabilityDeclaration, CapabilityRegistry
from furcon_audit.providers import ExaAdapter, FirecrawlAdapter, HttpResponse, ProviderError


class ProviderAdapterTests(unittest.TestCase):
    def test_exa_request_and_normalized_provenance(self):
        calls = []
        def transport(url, headers, body, timeout):
            calls.append((url, headers, json.loads(body), timeout))
            return HttpResponse(200, {"x-request-id": "exa-123"},
                json.dumps({"results": [{"url": "https://example.org",
                                         "title": "Example",
                                         "highlights": ["Relevant passage"]}]}).encode())
        adapter = ExaAdapter(api_key="test-key", transport=transport)
        result = adapter.execute("search", {"query": "event privacy notice", "limit": 3})
        self.assertEqual(calls[0][0], "https://api.exa.ai/search")
        self.assertEqual(calls[0][1]["x-api-key"], "test-key")
        self.assertEqual(calls[0][2]["numResults"], 3)
        self.assertEqual(result["provider_id"], "exa")
        self.assertEqual(result["request_id"], "exa-123")
        self.assertEqual(result["results"][0]["url"], "https://example.org")

    def test_firecrawl_uses_v2_bearer_contract(self):
        captured = {}
        def transport(url, headers, body, timeout):
            captured.update(url=url, headers=headers, body=json.loads(body))
            return HttpResponse(200, {}, json.dumps({"success": True, "data": [
                {"url": "https://example.org", "title": "Example", "markdown": "# Source"}
            ]}).encode())
        result = FirecrawlAdapter(api_key="test-key", transport=transport).execute(
            "search", {"query": "event terms"})
        self.assertEqual(captured["url"], "https://api.firecrawl.dev/v2/search")
        self.assertEqual(captured["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(captured["body"]["scrapeOptions"]["formats"], ["markdown"])
        self.assertEqual(result["results"][0]["markdown"], "# Source")

    def test_transient_status_retries(self):
        statuses = [503, 200]
        sleeps = []
        def transport(url, headers, body, timeout):
            status = statuses.pop(0)
            body = b'{"results": []}'
            return HttpResponse(status, {}, body)
        adapter = ExaAdapter(api_key="key", transport=transport, sleep=sleeps.append)
        adapter.execute("search", {"query": "test"})
        self.assertEqual(sleeps, [1])

    def test_non_retryable_status_fails_without_retry(self):
        calls = []
        def transport(url, headers, body, timeout):
            calls.append(1)
            return HttpResponse(401, {}, b'{"error":"unauthorized"}')
        adapter = ExaAdapter(api_key="key", transport=transport, sleep=lambda _: None)
        with self.assertRaises(ProviderError):
            adapter.execute("search", {"query": "test"})
        self.assertEqual(len(calls), 1)

    def test_missing_key_marks_adapter_unavailable(self):
        adapter = ExaAdapter(api_key="")
        self.assertEqual(adapter.declaration.availability, "unavailable")
        with self.assertRaises(ProviderError):
            adapter.execute("search", {"query": "test"})

    def test_registry_falls_back_only_within_same_capability(self):
        class Failing:
            declaration = CapabilityDeclaration("first", "1", "search.web", ("search",),
                                                 availability="available")
            def execute(self, operation, payload):
                raise ProviderError("first", "temporary", retryable=True)
        class Working:
            declaration = CapabilityDeclaration("second", "1", "search.web", ("search",),
                                                 availability="available")
            def execute(self, operation, payload):
                return {"provider_id": "second", "results": []}
        class Other:
            declaration = CapabilityDeclaration("browser", "1", "browser.inspect", ("inspect",),
                                                 availability="available")
            def execute(self, operation, payload):
                return {}
        registry = CapabilityRegistry()
        registry.register(Failing())
        registry.register(Working())
        registry.register(Other())
        result = registry.execute_with_fallback("search.web", "search", {"query": "x"})
        self.assertEqual(result["provider_id"], "second")
        self.assertEqual(result["fallback_attempts"][0]["provider_id"], "first")
        self.assertEqual(len(registry.candidates("search.web", "search")), 2)

    def test_oversized_provider_response_is_rejected(self):
        from furcon_audit.providers import MAX_PROVIDER_RESPONSE_BYTES
        adapter = ExaAdapter(
            api_key="key",
            transport=lambda *args: HttpResponse(200, {}, b"x" * (MAX_PROVIDER_RESPONSE_BYTES + 1)),
        )
        with self.assertRaisesRegex(ProviderError, "2 MB limit"):
            adapter.execute("search", {"query": "test"})

    def test_registry_rejects_non_object_adapter_result(self):
        class Broken:
            declaration = CapabilityDeclaration("broken", "1", "search.web", ("search",),
                                                 availability="available")
            def execute(self, operation, payload):
                return ["not", "an", "object"]
        registry = CapabilityRegistry()
        registry.register(Broken())
        with self.assertRaisesRegex(ProviderError, "non-object"):
            registry.execute_with_fallback("search.web", "search", {})

    def test_non_object_json_response_is_reported_as_provider_error(self):
        adapter = ExaAdapter(api_key="key", transport=lambda *args: HttpResponse(200, {}, b"[]"))
        with self.assertRaisesRegex(ProviderError, "non-object JSON"):
            adapter.execute("search", {"query": "test"})

    def test_invalid_search_input_is_rejected(self):
        adapter = ExaAdapter(api_key="key")
        for payload in ({"query": " "}, {"query": "x" * 4001}, None):
            with self.subTest(payload_type=type(payload).__name__):
                with self.assertRaises(ValueError):
                    adapter.execute("search", payload)

    def test_provider_redirects_are_not_followed(self):
        from furcon_audit.providers import _NoRedirectHandler
        import urllib.request
        handler = _NoRedirectHandler()
        request = urllib.request.Request("https://api.exa.ai/search")
        self.assertIsNone(handler.redirect_request(
            request, None, 302, "Found", {"Location": "https://attacker.example/"},
            "https://attacker.example/"
        ))

    def test_provider_resource_limits_are_bounded(self):
        for kwargs in ({"timeout": 61}, {"timeout": True},
                       {"max_retries": 6}, {"max_retries": True}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    ExaAdapter(api_key="key", **kwargs)


if __name__ == "__main__":
    unittest.main()
