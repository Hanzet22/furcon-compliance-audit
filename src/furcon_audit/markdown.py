DISCLAIMER = ("Preliminary compliance/risk review aid only. Not legal advice, legal opinion, "
              "certification, or guarantee of compliance. Seek qualified local counsel for consequential decisions.")

def render_markdown(report):
    event, scope = report.get("event", {}), report.get("scope", {})
    lines = [f"# Preliminary Review — {event.get('name', 'Unnamed event')}", "",
             f"- Report ID: {report.get('report_id', 'unknown')}",
             f"- Audit ID: {report.get('audit_id', 'unknown')}",
             f"- Generated: {report.get('generated_at', 'unknown')}", "",
             f"> **Disclaimer:** {DISCLAIMER}", "", "## Scope", "",
             scope.get("description", "Scope not supplied."), "", "## Limitations", ""]
    lines += [f"- {x}" for x in report.get("limitations", [])] or ["- None recorded."]
    lines += ["", "## Findings", ""]
    for f in report.get("findings", []):
        lines += [f"### {f.get('title', f.get('finding_id'))}", "",
                  f"- Category: {f.get('category', 'Unspecified')}",
                  f"- Assessment: **{f.get('assessment_status')}**",
                  f"- Severity: **{f.get('severity')}**",
                  f"- Confidence: **{f.get('confidence')}**", "",
                  f.get("rationale", "No rationale supplied."), "",
                  "Supporting evidence: " + ", ".join(f.get("supporting_evidence_ids", [])),
                  "Contrary evidence: " + ", ".join(f.get("contrary_evidence_ids", [])), ""]
    lines += ["## Research trail", ""]
    lines += [f"- {a.get('attempt_id')} — {a.get('capability_id')} — {a.get('status')}" for a in report.get("research_attempts", [])]
    lines += ["", "## Unresolved questions", ""]
    lines += [f"- {x}" for x in report.get("unresolved_questions", [])] or ["- None recorded."]
    lines += ["", "---", "", DISCLAIMER, ""]
    return "\n".join(lines)
