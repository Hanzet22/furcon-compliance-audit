# Evidence Specification v2

## Distinct entities
Source, Retrieval, Evidence, Claim, LegalAuthority, LegalProposition, Assessment, and Finding are separate. Organizer content is not legal authority; law does not prove organizer conduct.

## Provenance
Evidence identifies retrieval, exact excerpt/observation, locator, original language, capture time, and content hash where available. Preserve context and redact unnecessary personal data.

## Claims and corroboration
A Claim is a factual proposition linked to evidence IDs. Record support, contradiction, qualification, or context. Multiple providers finding the same page are not independent corroboration.

## Legal authorities and propositions
LegalAuthority records type, jurisdiction, title, issuing body, citation, dates, official URL, language, and retrieval. LegalProposition extracts a specific rule and references authorities/provisions. Distinguish binding law, court interpretation, regulator guidance, and commentary.

## Translation and assessment
Preserve original text/language. Record target language, method, provider, timestamp, reviewer/verification state, and limitations. Machine translation is not authoritative legal text. Assessment links claims, evidence, legal propositions, reasoning, outcome, confidence, and limitations. Confidence measures evidentiary support, not severity or applicability.

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