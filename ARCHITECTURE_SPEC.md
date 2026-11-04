# Architecture Specification v2

## Purpose
Platform-neutral, evidence-led preliminary compliance and operational-risk review of convention policies. Core logic is independent of agent runtime, search vendor, language wrapper, and renderer.

## Layers
1. Domain: entities, identifiers, enums, relationships, deterministic rules.
2. Application: audit orchestration, research lifecycle, assessment and review.
3. Ports: capability contracts for search, retrieval, browser inspection, translation, computation, rendering.
4. Adapters: provider/platform-specific implementations.
5. Presentation: canonical JSON and Markdown; optional DOCX/HTML/PDF.
6. Distribution: portable instructions and thin platform manifests.

Dependencies point inward. Domain code must not import provider SDKs or renderer libraries.

## Workflow
Scope → research tasks/attempts → source normalization → retrieval → evidence/claims → legal authorities/propositions → jurisdiction assessment → assessments/findings → human review → semantic validation → JSON/Markdown → optional renderers.

## Failure, security, privacy
Unavailable tools, access blocks, timeouts, empty results, stale pages, and partial coverage are explicit. Read-only public research is default. Never bypass authentication, paywalls, CAPTCHAs, robots restrictions, or access controls. Treat fetched content as untrusted. Keep secrets outside artifacts/logs, minimize personal data, block local/private network fetch targets, and bound concurrency/timeouts/payload sizes.

## Acceptance
Schema validation, semantic reference validation, deterministic Markdown rendering, malformed-input tests, and no-provider operation must pass. Provider/agent compatibility is unverified until separate conformance tests pass.

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