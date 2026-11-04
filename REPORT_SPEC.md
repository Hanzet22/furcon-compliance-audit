# Report Specification v2

## Canonical artifacts
JSON is canonical machine data; Markdown is canonical human-readable source. DOCX, HTML, PDF are optional renderers. Renderers cannot add findings, change statuses, omit material limitations, or imply legal advice.

## Contents and relationships
Report includes IDs/version, event, scope, generation metadata, research tasks/attempts, source registry, retrievals, evidence, claims, legal authorities/propositions, jurisdiction assessments, assessments, findings, human reviews, limitations, unresolved questions, and timestamp. All references use stable IDs. Findings link to assessments/jurisdiction assessments; do not embed duplicate jurisdiction objects.

## Narrative sections
Scope/event context; methodology and labels; research coverage/discovery trail; jurisdiction applicability; category assessments/findings; supporting/contrary evidence; human review/unresolved questions; source/evidence register.

## Validation
Draft 2020-12 plus semantic checks: unique IDs, resolved references, evidence-backed supported findings, rationale and authority references for supported applicability, reasons for partial/blocked research, timezone-aware timestamps, scope/limitations, and review freshness.

## Renderers and versioning
Markdown works offline. Optional renderers consume validated data only. Page size, margins, language, and styles are configurable. Renderer failure does not invalidate JSON/Markdown. Breaking changes require major schema version and tested migration; unknown fields are not silently dropped.

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