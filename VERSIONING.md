# Versioning and Compatibility Policy

## Separate version tracks

The project uses independent version tracks:

- **Package version**: Python distribution and CLI release, currently source version 2.0.0 (unreleased).
- **Contract version**: JSON interchange format, currently 1.0.0.
- **Provider adapter version**: adapter implementation/declaration version, currently labelled REST-v1 for the initial REST adapters.

A package patch/minor release must not silently change a frozen contract. A contract version is carried by each versioned record's schema_version.

## Contract semantic versioning

- **MAJOR**: incompatible change, including removal/rename, type change, enum narrowing, required-field addition, changed meaning, or changed reference semantics.
- **MINOR**: backward-compatible extension that existing consumers can ignore safely. For strict schemas, publish a new schema version rather than mutating v1.0.0.
- **PATCH**: clarification or correction that does not change validation outcomes or field semantics. The immutable published schema artifact should still be identified by its exact version and checksum.

## Compatibility promises

- Existing v1.0.0 payloads remain valid for the v1.0.0 validator.
- Consumers should ignore unknown diagnostic metadata only on extension points that explicitly allow it.
- Strict domain schemas reject unknown fields.
- Provider-specific result fields are not guaranteed to be portable between providers; use normalized fields for cross-provider logic.
- Provider availability, network access, and third-party service behavior are not guaranteed by the local contract.
- No agent runtime is certified until a separate runtime conformance suite is run and documented.

## Deprecation and migration

1. Announce the affected contract and replacement before removal.
2. Keep the old reader available for a documented transition window where feasible.
3. Provide a deterministic migration tool or migration instructions.
4. Publish old/new fixtures and compatibility test results.
5. Remove the old contract only in a major contract version.

## Release gate

A package release requires the full supported-Python CI matrix, schema and semantic tests, wheel build/install, CLI sample validation, static security checks, changelog review, and an explicit statement of remaining unverified integrations. Contract changes additionally require the contract-change evidence listed in API_CONTRACT.md.
