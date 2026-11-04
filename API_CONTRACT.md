# API Contract — v1.0.0

**Status:** Frozen for the v2 core.  
**Contract version:** 1.0.0  
**Package source version:** 2.0.0 (unreleased)

This document defines the stable interchange boundary for the current core. It freezes JSON document contracts, the normalized provider result envelope, the error envelope, and compatibility rules. It does not claim that every optional provider or agent runtime is implemented or certified.

## 1. Contract surfaces

| Surface | Canonical form | Contract |
|---|---|---|
| Domain records | JSON objects | schemas/*.schema.json |
| Full audit report | JSON object | schemas/report.schema.json |
| Search adapter input | JSON object | query string; limit integer |
| Normalized search result | JSON object | provider_id, retrieved_at, request_id, query, results, result_count |
| Error interchange | JSON object | schemas/error.schema.json |
| Human-readable report | UTF-8 Markdown | Deterministic renderer output |

JSON is the machine-readable source of truth. Markdown is a presentation export and must not be parsed back as the canonical report.

## 2. Schema rules

- All domain schemas use JSON Schema Draft 2020-12.
- Every versioned record carries schema_version: "1.0.0".
- IDs are lowercase strings matching ^[a-z][a-z0-9_-]{2,63}$.
- Timestamps use RFC 3339 date-time strings.
- Unknown fields are rejected where a schema declares additionalProperties: false.
- A report must pass schema validation before semantic cross-reference validation.
- A search result is a discovery lead, not Evidence, a Claim, a legal proposition, or a Finding.
- A successful retrieval is not automatically Evidence. Evidence capture remains explicit.
- Missing source material or a failed retrieval is not proof of a policy breach or legal non-compliance.

The schema files are normative. Examples and prose explain them but do not override them.

## 3. Provider adapter contract

A capability adapter declares its provider, capability, supported operations, availability, timeout, and limitations. For search.web:search, input is an object with a non-empty query and optional integer limit from 1 through 20. Query length is limited to 4000 characters.

A normalized successful search response contains:
- provider_id: stable provider identifier.
- retrieved_at: UTC RFC 3339 timestamp.
- request_id: provider request identifier or null.
- query: submitted query.
- results: array of normalized result objects.
- result_count: number of normalized results.

Provider-specific fields may remain inside each result object. Credentials, authorization headers, and secret values must never appear in normalized output, logs, reports, or errors.

Fallback is limited to adapters declaring the requested capability and operation. Registration order determines candidate order. A failed provider must not silently change the requested capability.

## 4. Error contract

The stable error envelope is defined by schemas/error.schema.json. Stable codes are defined in src/furcon_audit/error_codes.py.

Errors must:
- expose a stable machine-readable code;
- provide a concise, non-sensitive message;
- identify retryability explicitly;
- avoid credentials, tokens, raw authorization headers, and sensitive request bodies;
- avoid presenting a retrieval or provider failure as evidence of non-compliance.

Unknown provider-specific failures map to provider_error. Consumers must tolerate additional diagnostic metadata only on extension points that explicitly allow it.

## 5. Validation and conformance

The repository conformance suite checks:
- every schema is valid Draft 2020-12;
- schema IDs are unique and all domain record versions match the frozen version;
- the sample report validates;
- valid and invalid error envelopes behave as specified;
- normalized provider result and capability fallback contracts remain covered by mocked tests.

Passing local/mock conformance does not certify live API availability, provider terms or retention, browser behavior, network isolation, or compatibility with Claude Code, Codex, Cursor, or other agent runtimes.

## 6. Change control

The v1.0.0 contract is frozen. Do not edit a frozen schema or change a public field's meaning in place.

- Additive optional fields are non-breaking only where the relevant schema permits additional properties and consumers are documented to ignore unknown metadata.
- New optional fields in strict schemas require a new contract minor version and explicit consumer migration guidance; existing v1.0.0 payloads remain valid.
- Removing/renaming fields, changing types/enums/semantics, tightening required fields, or changing identity/reference rules is breaking and requires a new major contract version plus migration tooling.
- A bug fix may tighten implementation validation only when it does not invalidate a payload previously valid under the published schema.
- Package version and contract version are separate. A package release does not silently change the contract version.

Any proposed contract change must include updated schemas, compatibility notes, positive/negative fixtures, migration notes where needed, and passing CI before merge.
