import unittest

from furcon_audit.capabilities import CapabilityDeclaration, CapabilityRegistry
from furcon_audit.research import ResearchTask
from furcon_audit.pipeline import run_research_task


class SearchAdapter:
    declaration = CapabilityDeclaration("fixture-search", "1", "search.web", ("search",),
                                         availability="available")
    def __init__(self, results):
        self.results = results
    def execute(self, operation, payload):
        return {"provider_id": "fixture-search", "results": self.results}


class ResearchPipelineTests(unittest.TestCase):
    def registry(self, results):
        registry = CapabilityRegistry()
        registry.register(SearchAdapter(results))
        return registry

    def task(self):
        return ResearchTask("task_demo_001", "audit_demo_001", "Find event policy",
                            ("identify official policy sources",))

    def retriever(self, url, *, attempt_id, **kwargs):
        source_id = "source_" + ("one" if url.endswith("/one") else "two")
        return {
            "source": {"source_id": source_id, "canonical_url": url,
                       "source_type": "unverified", "verification_status": "unverified"},
            "retrieval": {"retrieval_id": "retrieval_" + source_id[-3:],
                          "source_id": source_id, "attempt_id": attempt_id,
                          "outcome": "success"},
            "content": {"extracted_text": "Synthetic content."}
        }

    def test_pipeline_records_search_and_retrieval_without_auto_evidence(self):
        task = self.task()
        result = run_research_task(task, self.registry([
            {"url": "https://example.org/one"}, {"url": "https://example.org/one"}
        ]), "official event terms", page_retriever=self.retriever)
        self.assertEqual(task.status, "completed")
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(len(result["retrievals"]), 1)
        self.assertEqual(result["evidence"], [])
        self.assertEqual(result["claims"], [])
        self.assertEqual(result["research_attempts"][-1]["capability_id"], "retrieve.page")

    def test_no_search_results_is_partial_not_source_absence(self):
        task = self.task()
        result = run_research_task(task, self.registry([]), "event terms")
        self.assertEqual(task.status, "partial")
        self.assertIn("No search candidates returned.", result["unresolved"][0])

    def test_all_blocked_retrievals_block_task(self):
        def blocked(url, *, attempt_id, **kwargs):
            return {"source": {"source_id": "source_one", "canonical_url": url},
                    "retrieval": {"retrieval_id": "retrieval_one", "source_id": "source_one",
                                  "attempt_id": attempt_id, "outcome": "blocked"},
                    "error": {"code": "robots_disallowed", "message": "Blocked"}}
        task = self.task()
        result = run_research_task(task, self.registry([{"url": "https://example.org/one"}]),
                                   "event terms", page_retriever=blocked)
        self.assertEqual(task.status, "blocked")
        self.assertEqual(result["retrievals"][0]["outcome"], "blocked")

    def test_invalid_query_rejected(self):
        with self.assertRaises(ValueError):
            run_research_task(self.task(), self.registry([]), " ")


if __name__ == "__main__":
    unittest.main()
