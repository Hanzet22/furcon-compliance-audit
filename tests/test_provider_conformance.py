"""Mocked adapter contract checks; these are not live-provider certifications."""
import json
import unittest

from furcon_audit.providers import ExaAdapter, FirecrawlAdapter, HttpResponse


class ProviderConformanceTests(unittest.TestCase):
    def test_exa_declares_search_capability_and_normalized_result_shape(self):
        def transport(url, headers, body, timeout):
            return HttpResponse(200, {"x-request-id": "mock-req"},
                json.dumps({"results": [{"url": "https://example.org/policy",
                                         "title": "Policy", "publishedDate": "2026-01-01"}]}).encode())
        adapter = ExaAdapter(api_key="mock-secret", transport=transport)
        result = adapter.execute("search", {"query": "policy"})
        self.assertEqual(adapter.declaration.capability_id, "search.web")
        self.assertIn("search", adapter.declaration.operations)
        self.assertEqual(result["results"][0]["source_provider"], "exa")
        self.assertNotIn("mock-secret", json.dumps(result))

    def test_firecrawl_declares_search_capability_and_normalized_result_shape(self):
        def transport(url, headers, body, timeout):
            return HttpResponse(200, {}, json.dumps({"success": True, "data": {
                "web": [{"url": "https://example.org/terms", "title": "Terms",
                         "description": "Terms page"}]}}).encode())
        adapter = FirecrawlAdapter(api_key="mock-secret", transport=transport)
        result = adapter.execute("search", {"query": "terms"})
        self.assertEqual(adapter.declaration.capability_id, "search.web")
        self.assertEqual(result["results"][0]["source_provider"], "firecrawl")
        self.assertEqual(result["result_count"], 1)
        self.assertNotIn("mock-secret", json.dumps(result))

    def test_unsupported_operations_are_rejected(self):
        for adapter in (ExaAdapter(api_key="mock"), FirecrawlAdapter(api_key="mock")):
            with self.subTest(provider=adapter.provider_id), self.assertRaises(ValueError):
                adapter.execute("retrieve", {"url": "https://example.org"})


if __name__ == "__main__":
    unittest.main()
