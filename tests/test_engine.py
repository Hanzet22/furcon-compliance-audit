import unittest
from unittest.mock import patch

from furcon_audit.engine import AuditEngine, EngineConfig
from furcon_audit.research import ResearchTask


class SearchGateway:
    def execute_with_fallback(self, capability_id, operation, payload):
        return {"provider_id": "fixture", "results": []}


class EngineBoundaryTests(unittest.TestCase):
    def task(self):
        return ResearchTask(
            "task_engine_001",
            "audit_engine_001",
            "Find official event policies",
            ("identify official sources",),
        )

    def test_default_configuration(self):
        engine = AuditEngine(SearchGateway())
        self.assertEqual(engine.config, EngineConfig(max_candidates=5))

    def test_configuration_rejects_invalid_candidate_limits(self):
        for value in (0, 21, True, "5", 1.5):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    EngineConfig(max_candidates=value)

    def test_dependencies_are_required(self):
        with self.assertRaises(TypeError):
            AuditEngine(object())
        with self.assertRaises(TypeError):
            AuditEngine(SearchGateway(), page_retriever=None)

    def test_run_research_delegates_with_injected_dependencies(self):
        retriever = lambda url, **kwargs: {}
        engine = AuditEngine(
            SearchGateway(),
            page_retriever=retriever,
            config=EngineConfig(max_candidates=3),
            retrieval_options={"timeout_seconds": 12},
        )
        expected = {"research_task": {"status": "partial"}}
        with patch("furcon_audit.engine.run_research_task", return_value=expected) as run:
            result = engine.run_research(self.task(), "official event terms")

        self.assertIs(result, expected)
        args, kwargs = run.call_args
        self.assertEqual(args[1].__class__, SearchGateway)
        self.assertEqual(args[2], "official event terms")
        self.assertEqual(kwargs["max_candidates"], 3)
        self.assertIs(kwargs["page_retriever"], retriever)
        self.assertEqual(kwargs["retrieval_options"], {"timeout_seconds": 12})

    def test_retrieval_options_are_copied(self):
        options = {"timeout_seconds": 10}
        engine = AuditEngine(SearchGateway(), retrieval_options=options)
        options["timeout_seconds"] = 1
        self.assertEqual(dict(engine._retrieval_options), {"timeout_seconds": 10})


if __name__ == "__main__":
    unittest.main()
