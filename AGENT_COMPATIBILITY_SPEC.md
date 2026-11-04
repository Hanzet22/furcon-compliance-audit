# Agent Compatibility Specification v2

## Portable core
Schemas, domain rules, tests, examples, capability contracts, and instructions are platform-neutral. Platform manifests, hooks, commands, and tool mappings belong in thin adapters.

## Agent behavior
Confirm scope; use authorized capabilities; distinguish discovery from evidence; preserve provenance/uncertainty; assess applicability per regime; separate status/severity/confidence; validate outputs; escalate high-impact issues. Never fabricate sources, law, tool results, test results, or repository state.

## Permission tiers
Read-only research; local processing; external side effects. External side effects require separate explicit authorization and may remain disallowed.

## Conformance
For each host/version record date, adapter revision, environment, tests, results, and limitations. Test skill discovery, metadata parsing, capability mapping, input/output, unavailable-tool fallback, errors, provenance, prompt-injection fixtures, and schema-valid output.

Labels: Planned (not tested), Partially tested (gaps stated), Tested (all required tests pass on documented version), Unsupported (known incompatibility).

| Host | Status |
|---|---|
| Claude Code | Planned / not tested |
| Codex | Planned / not tested |
| Cursor | Planned / not tested |
| Hermes | Planned / not tested |
| Agent Skills-compatible hosts | Planned / not tested |

Never claim universal support without reproducible tests.

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