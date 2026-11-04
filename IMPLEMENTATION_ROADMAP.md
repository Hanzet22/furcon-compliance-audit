# Implementation Roadmap

This roadmap records completed core implementation work and the next major engineering milestones. A phase is complete only after code review, deterministic tests, schema/semantic validation where applicable, and a successful GitHub Actions run.

| Phase | Scope | Exit criteria | Core status |
|---|---|---|---|
| 2B.1 | Capability registry and Exa/Firecrawl search adapters | Provider contracts, bounded retries, normalized errors, mock tests | Complete — mock contract tests |
| 2B.2 | Evidence retrieval pipeline | Safe public-page retrieval, robots policy, bounded payloads, hashes, source/retrieval records, failure provenance | Complete — search-to-retrieval orchestration |
| 2B.3 | Evidence capture and excerpt lifecycle | Explicit evidence creation, locators, language, content hash linkage, no automatic legal inference | Complete — explicit excerpt capture |
| 2B.4 | Claim and corroboration model | Claim support/contradiction/qualification links; deduplicate same-source discoveries | Complete — source-level corroboration summary |
| 2B.5 | Legal authority and proposition workflow | Authority classification, provisions, issuer/status/date provenance, separate propositions | Complete — separate authority/proposition records |
| 2B.6 | Jurisdiction applicability engine | Actor/activity/territorial/material scope/threshold/exemption factors; no nationality-only inference | Complete — factor-based record model |
| 2B.7 | Assessment and finding workflow | Independent status/severity/confidence, rationale, contrary evidence, recommendations | Complete — constructors and validation |
| 2B.8 | Human review lifecycle | Target/revision tracking, stale detection, review gates for high-impact conclusions | Complete — review transitions and revision gate |
| 2B.9 | Canonical report and renderer expansion | Complete traceability, coverage/limitations, deterministic Markdown and optional renderer ports | Complete — deterministic Markdown |
| 2B.10 | Agent/provider conformance and security hardening | Contract tests, safe URL and secret handling, prompt-injection isolation, compatibility claims only after tests | Core complete — mocked provider tests; agent/live conformance pending |
| 2C.1 | Full repository audit | Findings recorded, fixes applied, Python matrix, wheel checks | Complete — see RELEASE_READINESS_AUDIT.md |
| 2C.2 | Dedicated security review | Defensive input/network/provider hardening, static scans, residual risks documented | Complete — code-level review, not security certification |
| 2C.3 | API contract freeze | Frozen schemas, stable error envelope, versioning policy, conformance tests | Implemented — awaiting CI verification |
| 3 | Engine rewrite | Replace legacy orchestration with modular, testable engine behind frozen contracts | Planned — design begins after Phase 2C.3 verification |

## Phase 2C.3 contract checkpoint

The v1.0.0 interchange contract is documented in API_CONTRACT.md. Versioning and migration rules are in VERSIONING.md. The stable error envelope is defined by schemas/error.schema.json and src/furcon_audit/error_codes.py. CI conformance tests verify schema version consistency, unique schema IDs, error code alignment, valid/invalid error payloads, and preservation of the existing sample report.

Phase 3 must preserve the frozen v1.0.0 boundary unless a separately versioned contract change is approved. No legacy engine behavior should be silently carried forward where it conflicts with the documented domain and safety invariants.
