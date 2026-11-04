# Phase 2C.1 — Full Repository Audit

**Audit status:** Implementation fixes committed; final CI verification pending.  
**Scope:** Validator, provider adapters, capability registry, research pipeline, public-page retrieval, CI, packaging metadata, and release-state clarity.  
**Method:** Read-only repository inspection followed by targeted regression tests and incremental fixes.

## Findings and disposition

| ID | Area | Severity | Finding | Disposition |
|---|---|---:|---|---|
| 2C1-01 | Validator | High | Semantic validation assumed nested collections and rows were correctly shaped. Direct semantic calls could fail on malformed values. | Fixed: schema validation gates report semantics; semantic validator now checks collection and row shapes and guards status values. Regression tests added. |
| 2C1-02 | Provider transport | High | Standard-library transport read provider response bodies without an explicit byte ceiling. | Fixed: transport reads at most 2 MB + 1 byte; oversized responses are rejected. |
| 2C1-03 | Provider contract | Medium | JSON payloads and adapter outputs were not fully checked for object shape. | Fixed: non-object JSON payloads, invalid transport responses, and non-object adapter outputs are rejected; fallback diagnostics retain the underlying error. |
| 2C1-04 | Research pipeline | Medium | Malformed provider fallback metadata, non-object search responses, and malformed source capture records could cause runtime errors. | Fixed: defensive shape checks and unresolved-gap reporting added. |
| 2C1-05 | Retrieval boundary | High | Custom fetchers could return bodies larger than the configured retrieval limit. | Fixed: response type and byte length are checked before decoding or extraction. Existing public-IP checks, pinned connections, redirect validation, robots fail-closed behavior, media-type checks, and response limits were reviewed. |
| 2C1-06 | CI coverage | Medium | CI tested only Python 3.11 despite declaring Python 3.10+. | Fixed: matrix expanded to Python 3.10, 3.11, 3.12, and 3.13. |
| 2C1-07 | Packaging | Medium | CI did not verify that a distributable wheel could be built. | Fixed: wheel build and isolated target installation added to CI. |
| 2C1-08 | Release metadata | Low | Source metadata used 2.0.0 while no published GitHub release was present in the release listing. | Clarified: README and changelog identify 2.0.0 as an unreleased source version. No tag or public release was created. |

## Verification boundaries

The following are deliberately **not** represented as complete:

- Live Exa and Firecrawl API verification. Current provider tests use deterministic mocked HTTP responses.
- Compatibility certification for Claude Code, Codex, Cursor, or other agent runtimes.
- A technical LLM prompt-injection isolation boundary. Retrieved content is documented and handled as untrusted data, but the core has no sandboxed LLM execution environment.
- Network-layer egress enforcement. DNS pinning and application checks reduce SSRF risk but do not replace deployment firewall rules and worker isolation.
- External security review or legal review.

## Release recommendation

Do not publish a stable release based only on unit tests. First obtain a successful complete Python matrix and wheel build, review the resulting diff, then arrange external review and opt-in live-provider conformance checks where credentials and provider terms permit.

This repository remains a preliminary review aid, not legal advice, legal opinion, certification, or guarantee.
