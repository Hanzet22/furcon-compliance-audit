# Audit Specification v2

## Scope and categories
Review public event terms, privacy notices, registration rules, codes of conduct, safety rules, refunds, and related policies. Categories: privacy; refund/payment; liability/waivers; CoC enforcement; age/minor safeguards; IP/photography; discrimination/harassment/accessibility; disputes/governing law; terms changes; event safety/emergency response.

Categories are prompts, not automatic legal requirements. Record omitted categories and reasons.

## Finding contract
A finding has stable ID, title, category, assessment status, severity, confidence, rationale, supporting and contrary evidence IDs, affected actor/activity, recommendations, and jurisdiction assessment references. Facts, legal analysis, and recommendations remain distinct.

Assessment status: supported_concern, no_issue_observed, needs_clarification, not_assessed, not_applicable. no_issue_observed means no issue established within scope, not legally compliant. Supported concern requires evidence and an assessment.

## Human review and ethics
Require review for high-impact legal interpretations, critical/high findings, uncertain applicability, and external publication. Record target IDs, reviewer role, decision, rationale, timestamp, and reviewed revision. Material changes stale prior review. Minimize personal data. Use neutral constructive language; no harassment, doxxing, personal attacks, or unsupported allegations.

State scope, missing sources, assumptions, language limits, unresolved questions, and need for qualified counsel.

## Shared contract
Schema dialect: JSON Schema Draft 2020-12; contract version 1.0.0. IDs are stable opaque strings. Timestamps use RFC 3339 with timezone.

Entity graph: Source → Retrieval → Evidence → Claim → Assessment → Finding; LegalAuthority → LegalProposition → Assessment. Organizer statements are not legal authorities; legal authority does not prove organizer conduct.

Distinct status namespaces:
- Workflow: not_started, in_progress, completed, partial, blocked, not_applicable.
- Assessment: supported_concern, no_issue_observed, needs_clarification, not_assessed, not_applicable.
- Applicability: applicable_supported, potentially_applicable, not_established, not_applicable_supported, not_assessed.
- Research task: queued, running, completed, partial, blocked, failed, cancelled.
- Research attempt: succeeded, no_results, failed, rate_limited, blocked, skipped.
- Human review: not_required, pending, in_review, changes_requested, accepted, rejected, stale.
- Severity: critical, high, moderate, low, informational. Confidence: low, medium, high.

Never conflate these namespaces. Severity and confidence are independent.

Legal applicability is assessed per regime, actor, activity, territorial/material scope, thresholds, and exemptions. Nationality or website accessibility alone is insufficient. Search results are discovery leads, not legal evidence. Missing clauses, failed searches, and inaccessible pages do not prove non-compliance. Preserve original-language material and translation provenance. Reports are preliminary review aids, not legal advice, opinions, certifications, or guarantees.

Versioning: major may break; minor adds backward-compatible optional fields; patch clarifies without changing intended meaning. Migrations are explicit, deterministic, tested, and never silently discard unknown fields. Semantic reference validation supplements JSON Schema.