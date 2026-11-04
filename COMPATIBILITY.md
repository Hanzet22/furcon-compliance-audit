# Compatibility and Conformance Status

Compatibility claims are deliberately conservative.

| Component | Status | Evidence |
|---|---|---|
| Python core | Implemented | Unit tests and GitHub Actions CI |
| JSON Schema Draft 2020-12 | Implemented | Schema self-validation and report contract tests |
| Exa REST adapter | Mock-contract tested | Request/authentication and normalized response fixtures |
| Firecrawl REST adapter | Mock-contract tested | Request/authentication and normalized response fixtures |
| Public-page retrieval | Mocked tests | URL policy, retrieval outcomes, content extraction, provenance |
| Markdown renderer | Unit tested | Deterministic output and untrusted-markup escaping |
| Claude Code, Codex, Cursor, other agent runtimes | Not yet verified | Requires separate runtime conformance tests |
| Live Exa/Firecrawl accounts | Not yet verified | No live credentials or live calls used in CI |
| Browser, translation, computation, DOCX/HTML/PDF providers | Not yet implemented or verified | Candidate capabilities only |

A mocked adapter test verifies the local request/response contract; it does not certify live service availability, provider terms, retention behavior, or compatibility with an agent platform. Do not describe an untested runtime/provider as supported.
