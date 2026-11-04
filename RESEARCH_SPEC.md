# Research Specification v2

## Lifecycle
ResearchTask has objective, question, completion criteria, status, and audit ID. ResearchAttempt records one provider/method execution, timestamps, outcome, retry number, sanitized query/action summary, and normalized error. Source is normalized identity. Retrieval is a timestamped capture/version.

Task: queued, running, completed, partial, blocked, failed, cancelled. Attempt: succeeded, no_results, failed, rate_limited, blocked, skipped. Partial/blocked/failed requires reason. Completion requires declared criteria met.

## Discovery and verification
Search is discovery only. Verify official ownership through multiple signals such as event-owned links, organizer identity, and direct navigation. Do not rely on TLD, branding, or search rank alone. Record source classification and rationale. Keep excluded/failed candidates with reasons.

Record canonical URL, title, publication/update date if available, retrieval time, language, content hash, and version notes. Keep each retrieval distinct. Same page found by multiple providers is one source with multiple attempts, not independent corroboration. Track page changes by content hash.

## Retry and safety
Retries are bounded and recorded. Respect rate limits/access restrictions. Fallback is by capability, not brand. Read-only access only; no form submission, account changes, organizer contact, or access-control bypass. Avoid attendee personal data.

## Report trail
Include tasks, attempts, provider/capability, timestamps, source dispositions, retrievals, errors, verification, and unresolved gaps. Never expose secrets.

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