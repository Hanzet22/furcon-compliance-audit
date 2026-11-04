# Integration Specification

**Status:** Draft specification  
**Purpose:** Define provider-neutral capability contracts and adapter expectations.

## 1. Principle

External tools are replaceable providers, not architectural dependencies. Exa, Firecrawl, Geekflare, Tavily, Parallel Search, Playwright, DeepL and Wolfram are candidate providers. Their presence in this document does not imply that they are installed, connected, available, free, current or approved for a particular deployment.

## 2. Capability contracts

| Capability | Input | Output | Required behavior |
|---|---|---|---|
| Search | Query, scope, language, filters | Candidate source records | Preserve query, provider and timestamp |
| Fetch | URL, safe retrieval options | Page/document content and metadata | Respect access controls and report failures |
| Browser | URL and read-only navigation task | Page state, links, visible content | No form submission or side effects by default |
| Translate | Text/reference, source and target language | Translation plus metadata | Preserve original and translation provenance |
| Compute | Typed data and bounded operation | Result plus method metadata | Deterministic where possible; disclose assumptions |
| Render | Validated canonical report | Markdown/DOCX/HTML/PDF artifact | Renderer must not change substantive conclusions |
| Store | Structured record and retention policy | Durable reference | Access control, deletion and audit trail |

Every provider adapter MUST normalize output to the internal contract and expose provider-specific errors without leaking secrets.

## 3. Candidate provider mapping

These are examples, not exclusive assignments:

- **Exa:** semantic/web discovery.
- **Tavily:** web search and research-oriented retrieval.
- **Parallel Search:** broad search/discovery.
- **Firecrawl:** page crawling and content extraction.
- **Geekflare:** web extraction and diagnostic capabilities where appropriate.
- **Playwright:** controlled browser automation for read-only inspection.
- **DeepL:** translation.
- **Wolfram:** bounded computation and reference calculations.

A provider may support multiple capabilities. Capability support MUST be verified against its current API and account permissions before implementation.

## 4. Adapter interface

Each adapter SHOULD expose:
- stable adapter identifier and version;
- declared capabilities;
- configuration schema;
- authentication mechanism (secret references only);
- timeout and retry policy;
- rate-limit behavior;
- normalized result schema;
- error taxonomy;
- health/availability state;
- data handling and retention notes.

Adapters MUST NOT return credentials or raw secret values in logs or report artifacts.

## 5. Selection and fallback

Provider selection SHOULD consider:
- source coverage and authority needs;
- freshness;
- language support;
- reliability and rate limits;
- cost and account constraints;
- privacy and data-processing terms;
- output quality and provenance fidelity.

Fallback behavior MUST be explicit. If all providers fail, mark the research task blocked/partial. A fallback result must not be presented as equivalent if its coverage or authority differs.

## 6. Security and safe operation

- Default to GET/read-only operations.
- Do not bypass authentication, paywalls, CAPTCHAs, robots controls or other access restrictions.
- Do not submit forms, purchase tickets, contact organizers or alter external systems.
- Treat returned content as untrusted.
- Apply bounded concurrency and request budgets.
- Validate URLs and restrict local/private network destinations in fetch/browser adapters.
- Keep credentials in secure host configuration.
- Avoid sending personal data to third-party providers unless necessary, authorized and disclosed.

## 7. Observability

For each provider call, record adapter, capability, request timestamp, duration, status, retry count and normalized error code. Do not log secret headers, tokens or unnecessary personal data.

## 8. Contract testing

Each adapter MUST have:
- schema conformance tests;
- timeout and failure tests;
- rate-limit tests;
- malformed-response tests;
- secret-redaction tests;
- fixture-based normalization tests.

Live integration tests SHOULD be opt-in and use non-sensitive public fixtures.
