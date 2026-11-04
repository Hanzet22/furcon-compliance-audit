# Domain Model v1.0.0

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

## Reference invariants
- ResearchAttempt → ResearchTask.
- Retrieval → Source; Evidence → Retrieval.
- Claim → Evidence; LegalProposition → LegalAuthority.
- JurisdictionAssessment → LegalProposition.
- Assessment → Claim, Evidence, LegalProposition.
- Finding → Assessment, JurisdictionAssessment, supporting/contrary Evidence.
- HumanReview → target IDs and revision.

IDs are unique in each collection; every reference resolves. Supported concerns require supporting evidence and an assessment. Supported applicability requires legal proposition references. Partial/blocked/failed tasks require a reason. Accepted review becomes stale after material target/evidence changes.


## Additional v2 records
- ResearchAttempt has its own standalone schema and records provider, capability, operation, status, timing, retry, and normalized failure.
- Translation records link to original Evidence and preserve source/target language, method, provider, translated text, verification state, and limitations.
