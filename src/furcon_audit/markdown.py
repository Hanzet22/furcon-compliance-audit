"""Deterministic Markdown renderer for complete evidence-led audit reports."""
from __future__ import annotations
import re

DISCLAIMER = (
    "Preliminary compliance/risk review aid only. Not legal advice, legal opinion, "
    "certification, or guarantee of compliance. Seek qualified local counsel for consequential decisions."
)

def _safe(value) -> str:
    if value is None:
        return "Not recorded"
    text = str(value).replace("\\", "\\\\")
    for char in (chr(96), "*", "_", "[", "]", "#", "|", "<", ">"):
        text = text.replace(char, "\\" + char)
    return re.sub(r"\s+", " ", text).strip()

def _section(lines, title, rows):
    lines.extend(["", "## " + title, ""])
    lines.extend(rows or ["- None recorded."])

def render_markdown(report: dict) -> str:
    event, scope = report.get("event", {}), report.get("scope", {})
    lines = [
        "# Preliminary Review — " + _safe(event.get("name", "Unnamed event")), "",
        "- Report ID: " + _safe(report.get("report_id")),
        "- Audit ID: " + _safe(report.get("audit_id")),
        "- Revision: " + _safe(report.get("report_revision")),
        "- Generated: " + _safe(report.get("generated_at")), "",
        "> Disclaimer: " + DISCLAIMER, "",
        "## Scope", "", _safe(scope.get("description", "Scope not supplied.")),
    ]
    rows = []
    for task in report.get("research_tasks", []):
        rows.append("- Task " + _safe(task.get("research_task_id")) + " — " +
                    _safe(task.get("status")) + " — " + _safe(task.get("blocked_reason")))
    for attempt in report.get("research_attempts", []):
        rows.append("- Attempt " + _safe(attempt.get("attempt_id")) + " — " +
                    _safe(attempt.get("provider_id")) + " / " + _safe(attempt.get("capability_id")) +
                    " — " + _safe(attempt.get("status")))
    _section(lines, "Research coverage", rows)

    rows = ["- " + _safe(x.get("source_id")) + " — " + _safe(x.get("title")) +
            " — " + _safe(x.get("source_type")) + " / " + _safe(x.get("verification_status")) +
            " — " + _safe(x.get("canonical_url")) for x in report.get("sources", [])]
    _section(lines, "Source register", rows)

    rows = ["- " + _safe(x.get("retrieval_id")) + " — source " + _safe(x.get("source_id")) +
            " — " + _safe(x.get("method")) + " / " + _safe(x.get("outcome")) +
            " — " + _safe(x.get("retrieved_at")) + " — hash " + _safe(x.get("content_hash")) +
            " — error " + _safe(x.get("error_code")) for x in report.get("retrievals", [])]
    _section(lines, "Retrieval history", rows)

    rows = []
    for x in report.get("evidence", []):
        rows.extend([
            "- Evidence " + _safe(x.get("evidence_id")) + " — retrieval " + _safe(x.get("retrieval_id")),
            "  - Kind/locator/language: " + _safe(x.get("kind")) + " / " +
            _safe(x.get("locator")) + " / " + _safe(x.get("original_language")),
            "  - Captured: " + _safe(x.get("captured_at")) + " — source: " + _safe(x.get("source_url")),
            "  - Content hash: " + _safe(x.get("content_hash")),
            "  - Excerpt: " + _safe(x.get("excerpt"))
        ])
    _section(lines, "Evidence register", rows)

    rows = []
    for x in report.get("claims", []):
        rows.append("- Claim " + _safe(x.get("claim_id")) + " — " + _safe(x.get("statement")) +
                    " — actor/activity: " + _safe(x.get("actor")) + " / " + _safe(x.get("activity")))
        for rel in x.get("evidence_relations", []):
            rows.append("  - Evidence " + _safe(rel.get("evidence_id")) + ": " +
                        _safe(rel.get("relationship")))
    _section(lines, "Claims", rows)

    rows = ["- " + _safe(x.get("authority_id")) + " — " + _safe(x.get("title")) +
            " — " + _safe(x.get("authority_type")) + " — jurisdiction: " +
            _safe(x.get("jurisdiction")) + " — issuer: " + _safe(x.get("issuing_body")) +
            " — status: " + _safe(x.get("authority_status")) + " — effective: " +
            _safe(x.get("effective_date")) + " — URL: " + _safe(x.get("official_url"))
            for x in report.get("legal_authorities", [])]
    _section(lines, "Legal authorities", rows)

    rows = ["- " + _safe(x.get("proposition_id")) + " — " + _safe(x.get("statement")) +
            " — authorities: " + _safe(", ".join(x.get("authority_ids", []))) +
            " — binding status: " + _safe(x.get("binding_status")) +
            " — provision: " + _safe(x.get("provision_reference"))
            for x in report.get("legal_propositions", [])]
    _section(lines, "Legal propositions", rows)

    rows = []
    for x in report.get("jurisdiction_assessments", []):
        rows.extend([
            "- " + _safe(x.get("regime")) + " — actor: " + _safe(x.get("actor")) +
            " — activity: " + _safe(x.get("activity")),
            "  - Applicability: " + _safe(x.get("applicability_status")),
            "  - Territorial/material scope: " + _safe(x.get("territorial_scope")) +
            " / " + _safe(x.get("material_scope")),
            "  - Threshold/exemption: " + _safe(x.get("threshold_status")) +
            " / " + _safe(x.get("exemption_status")),
            "  - Propositions: " + _safe(", ".join(x.get("legal_proposition_ids", []))),
            "  - Rationale: " + _safe(x.get("rationale")),
            "  - Unresolved facts: " + _safe("; ".join(x.get("unresolved_facts", [])))
        ])
    _section(lines, "Jurisdiction applicability", rows)

    rows = ["- " + _safe(x.get("assessment_id")) + " — " +
            _safe(x.get("assessment_status")) + " — confidence: " +
            _safe(x.get("confidence")) + " — " + _safe(x.get("rationale"))
            for x in report.get("assessments", [])]
    _section(lines, "Assessments", rows)

    rows = []
    for x in report.get("findings", []):
        rows.extend([
            "- " + _safe(x.get("finding_id")) + " — " + _safe(x.get("title")) +
            " — category: " + _safe(x.get("category")),
            "  - Assessment/severity/confidence: " + _safe(x.get("assessment_status")) +
            " / " + _safe(x.get("severity")) + " / " + _safe(x.get("confidence")),
            "  - Affected actor/activity: " + _safe(x.get("affected_actor")) +
            " / " + _safe(x.get("affected_activity")),
            "  - Rationale: " + _safe(x.get("rationale")),
            "  - Supporting evidence: " + _safe(", ".join(x.get("supporting_evidence_ids", []))),
            "  - Contrary evidence: " + _safe(", ".join(x.get("contrary_evidence_ids", []))),
            "  - Assessment/jurisdiction refs: " + _safe(", ".join(x.get("assessment_ids", []))) +
            " / " + _safe(", ".join(x.get("jurisdiction_assessment_ids", []))),
            "  - Recommendation: " + _safe(x.get("recommendation"))
        ])
    _section(lines, "Findings", rows)

    rows = ["- " + _safe(x.get("review_id")) + " — targets: " +
            _safe(", ".join(x.get("target_ids", []))) + " — " +
            _safe(x.get("review_status")) + " / " + _safe(x.get("decision")) +
            " — revision: " + _safe(x.get("revision")) +
            " — reviewer role: " + _safe(x.get("reviewer_role"))
            for x in report.get("human_reviews", [])]
    _section(lines, "Human review", rows)
    _section(lines, "Limitations", ["- " + _safe(x) for x in report.get("limitations", [])])
    _section(lines, "Unresolved questions", ["- " + _safe(x) for x in report.get("unresolved_questions", [])])
    lines.extend(["", "---", "", DISCLAIMER, ""])
    return "\n".join(lines)
