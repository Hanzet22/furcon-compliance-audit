# Jurisdiction Specification v2

## Applicability
Assess each regime by actor, activity, territorial connection, material scope, thresholds, exemptions, relevant dates, and facts. Nationality, website accessibility, TLD, language, or broad international reach alone do not establish applicability.

## Status
Use only applicable_supported, potentially_applicable, not_established, not_applicable_supported, not_assessed. Every decision has rationale. Supported applicability and supported non-applicability require legal proposition references. If facts are insufficient, use not_established/not_assessed.

## Prioritization
Event location and organizer establishment are starting points only where evidenced. Other regimes are assessed when facts show targeting, processing, sales, establishment, or another relevant connection. Tiering is research prioritization, never a legal test. Do not assume GDPR/CCPA universally applies.

## Many-to-many links
JurisdictionAssessment has a stable ID. Findings reference jurisdiction assessment IDs; do not duplicate embedded jurisdiction objects. One assessment may inform multiple findings and one finding may reference multiple assessments.

## Authorities
Prefer legislation, regulations, official court decisions, and official regulator materials. Label binding law, guidance, event policy, and commentary distinctly. Never fabricate citations. Recommend qualified local counsel for consequential decisions.

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