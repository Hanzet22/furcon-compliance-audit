import unittest

from furcon_audit.application.research import run_research_workflow
from furcon_audit.capabilities import CapabilityDeclaration, CapabilityRegistry
from furcon_audit.research import ResearchTask


class SearchFixture:
    declaration = CapabilityDeclaration(
        "application-fixture", "1.0", "search.web", ("search",),
        availability="available",
    )

    def execute(self, operation, payload):
        return {"provider_id": "application-fixture", "results": [
            {"url": "https://example.org/policy"}
        ]}


class ApplicationResearchTests(unittest.TestCase):
    def test_application_service_owns_workflow_and_keeps_evidence_explicit(self):
        registry = CapabilityRegistry()
        registry.register(SearchFixture())
        task = ResearchTask(
            "task_app_001",
            "audit_app_001",
            "Find official event policy",
            ("identify official policy",),
        )

        def retriever(url, *, attempt_id, **options):
            return {
                "source": {
                    "source_id": "source_app_001",
                    "canonical_url": url,
                    "source_type": "unverified",
                    "verification_status": "unverified",
                },
                "retrieval": {
                    "retrieval_id": "retrieval_app_001",
                    "source_id": "source_app_001",
                    "attempt_id": attempt_id,
                    "outcome": "success",
                },
                "content": {"extracted_text": "Synthetic policy text."},
            }

        result = run_research_workflow(
            task, registry, "official event policy", page_retriever=retriever
        )

        self.assertEqual(task.status, "completed")
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(len(result["retrievals"]), 1)
        self.assertEqual(result["evidence"], [])
        self.assertEqual(result["claims"], [])


if __name__ == "__main__":
    unittest.main()
