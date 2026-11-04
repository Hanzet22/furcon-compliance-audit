# Phase 2B Implementation Roadmap

This roadmap divides the v2 implementation into independently testable increments. A phase is complete only after code review, deterministic tests, schema/semantic validation where applicable, and a successful GitHub Actions run.

| Phase | Scope | Exit criteria |
|---|---|---|
| 2B.1 | Capability registry and Exa/Firecrawl search adapters | Provider contracts, bounded retries, normalized errors, mock tests |
| 2B.2 | Evidence retrieval pipeline | Safe public-page retrieval, robots policy, bounded payloads, hashes, source/retrieval records, failure provenance |
| 2B.3 | Evidence capture and excerpt lifecycle | Explicit evidence creation, locators, language, content hash linkage, no automatic legal inference |
| 2B.4 | Claim and corroboration model | Claim support/contradiction/qualification links; deduplicate same-source discoveries |
| 2B.5 | Legal authority and proposition workflow | Authority classification, provisions, issuer/status/date provenance, separate propositions |
| 2B.6 | Jurisdiction applicability engine | Actor/activity/territorial/material scope/threshold/exemption factors; no nationality-only inference |
| 2B.7 | Assessment and finding workflow | Independent status/severity/confidence, rationale, contrary evidence, recommendations |
| 2B.8 | Human review lifecycle | Target/revision tracking, stale detection, review gates for high-impact conclusions |
| 2B.9 | Canonical report and renderer expansion | Complete traceability, coverage/limitations, deterministic Markdown and optional renderer ports |
| 2B.10 | Agent/provider conformance and security hardening | Contract tests, safe URL and secret handling, prompt-injection isolation, compatibility claims only after tests |

The phases are cumulative. Search results are discovery leads, retrieval is not evidence by itself, and evidence is not a legal conclusion. Provider integrations remain optional; tests use synthetic fixtures and mocks unless a separately authorized live test is configured.
