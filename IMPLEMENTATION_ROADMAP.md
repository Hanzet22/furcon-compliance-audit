# Phase 2B Implementation Roadmap

This roadmap divides the v2 implementation into independently testable increments. A phase is complete only after code review, deterministic tests, schema/semantic validation where applicable, and a successful GitHub Actions run.

| Phase | Scope | Exit criteria | Core status |
|---|---|---|
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

The phases are cumulative. Search results are discovery leads, retrieval is not evidence by itself, and evidence is not a legal conclusion. Provider integrations remain optional; tests use synthetic fixtures and mocks unless a separately authorized live test is configured.


## Core completion checkpoint

Core phases 2B.1–2B.10 are implemented on `main`. GitHub Actions run [#62](https://github.com/Hanzet22/furcon-compliance-audit/actions/runs/41913247351) completed successfully:
- 60 unit tests passed.
- The sample report passed JSON Schema and semantic validation.
- The CLI rendered the sample Markdown report successfully.

This checkpoint does not claim live Exa/Firecrawl service verification or compatibility with Claude Code, Codex, Cursor, or other agent runtimes. Those remain explicitly unverified in `COMPATIBILITY.md`. Live-provider tests require separately configured credentials and must remain opt-in.
