# Integration Specification v2

## Capability-first
Providers are optional adapters. Capabilities: search.web, retrieve.page, browser.inspect, translate.text, compute.general, render.markdown/docx/html/pdf. Browser automation is not a search substitute; translation is not legal verification.

## Provider declaration
Each adapter declares capability ID, provider ID/version, operations, input/output schemas, authentication needs, rate limits/quotas when known, data handling/retention when known, service limits, timeout/retry behavior, normalized errors, and health state. Unknown properties remain unknown.

## Candidate providers
Exa, Tavily, Parallel Search, Firecrawl, Geekflare, Playwright, DeepL, and Wolfram are possible integrations only. This list does not imply installation, access, availability, authority, or successful tests.

## Routing, fallback, security
Application requests a capability and operation. Registry selects only authorized, healthy adapters satisfying the contract. Fallback must match capability. Every attempt is recorded. Keep secrets in host secret storage. Validate URLs, block private/local network targets, bound timeouts and sizes, redact logs, and isolate prompt injection.

## Testing
Adapter tests cover schemas, malformed responses, timeouts, rate limits, redaction, and fixtures. Live tests are opt-in and use public non-sensitive fixtures.

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