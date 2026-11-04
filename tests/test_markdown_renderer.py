import json
import unittest
from pathlib import Path
from furcon_audit.markdown import render_markdown

ROOT = Path(__file__).resolve().parents[1]

class MarkdownRendererTests(unittest.TestCase):
    def test_renderer_includes_traceability_sections(self):
        report = json.loads((ROOT / "examples/sample-report.v1.json").read_text())
        output = render_markdown(report)
        for heading in ("Source register", "Retrieval history", "Evidence register",
                        "Claims", "Legal authorities", "Legal propositions",
                        "Jurisdiction applicability", "Assessments", "Findings",
                        "Human review", "Limitations"):
            self.assertIn("## " + heading, output)

    def test_renderer_is_deterministic(self):
        report = json.loads((ROOT / "examples/sample-report.v1.json").read_text())
        self.assertEqual(render_markdown(report), render_markdown(report))

    def test_untrusted_markup_is_escaped(self):
        report = {"event":{"name":"# Injected heading"},"scope":{"description":"<script>alert(1)</script>"},
                  "limitations":["[external](https://bad.example)"]}
        output = render_markdown(report)
        self.assertIn("\\# Injected heading", output)
        self.assertIn("\\<script\\>", output)
        self.assertIn("\\[external\\]", output)

if __name__ == "__main__":
    unittest.main()
