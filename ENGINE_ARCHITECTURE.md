# Engine Rewrite Architecture

**Phase:** 3 — Engine Rewrite  
**Current slice:** 3.1 — Application boundary and migration seam  
**Status:** In progress  
**Interchange contract:** v1.0.0 remains frozen

## Objective

Replace the initial, function-oriented orchestration with a modular application engine while preserving the frozen JSON interchange contract. The rewrite is internal: report schemas, stable error codes, provider normalization, evidence provenance, and legal-methodology safeguards remain authoritative.

## Current-state assessment

The existing implementation has useful isolated modules for providers, retrieval, domain workflows, validation, and rendering. The main orchestration path is concentrated in `pipeline.py`, while the CLI directly composes validation and rendering. This is a workable prototype but does not yet provide a single application boundary or explicit ports for all external dependencies.

The rewrite must not discard the existing security work. In particular, the retrieval implementation remains the only approved public-page retrieval path until a replacement passes equivalent tests.

## Target dependency direction

```text
CLI / Agent / Future API
        |
        v
Application Engine (use cases)
        |
        +---- Domain workflows and policies
        |
        +---- Ports (protocols)
                 |
                 +---- Search provider adapters
                 +---- Public-page retrieval adapter
                 +---- Future storage / export adapters
```

Rules:

1. Domain modules must not import provider SDKs, CLI code, network clients, or agent-runtime packages.
2. Application services depend on ports and domain workflows, not concrete providers.
3. Infrastructure adapters implement ports and own network/provider-specific behavior.
4. The CLI is an adapter; it must not contain domain or orchestration rules.
5. JSON v1.0.0 is the canonical interchange boundary. Markdown remains a deterministic presentation export.
6. Search results and retrieved content remain untrusted input. Retrieval does not create Evidence or legal conclusions automatically.
7. Legal applicability remains fact-specific and requires human review for consequential conclusions.
8. Security controls must be preserved or strengthened; no rewrite may silently weaken URL validation, DNS pinning, redirect checks, robots handling, timeouts, or body limits.

## Migration strategy

The rewrite is incremental and strangler-style. Existing public functions remain compatibility entry points while the new engine takes ownership of application orchestration.

| Slice | Scope | Exit criteria |
|---|---|---|
| 3.1 | Engine boundary, configuration, and ports | Engine can invoke the existing workflow through explicit dependencies; contract and regression tests pass |
| 3.2 | Research workflow extraction | Orchestration moves behind application services; legacy function delegates without behavior drift |
| 3.3 | Domain service boundaries | Evidence, claims, jurisdiction, assessment, and review workflows expose consistent service interfaces |
| 3.4 | Infrastructure adapters | Search and retrieval adapters implement ports; provider-specific behavior remains isolated |
| 3.5 | CLI and report adapters | CLI becomes a thin adapter; JSON/Markdown outputs remain compatible |
| 3.6 | Legacy retirement and conformance | No internal dependency on legacy orchestration; full compatibility and security regression suite passes |

## Compatibility and rollout

- Keep API contract v1.0.0 frozen.
- Preserve existing import paths until an explicit deprecation and migration period is completed.
- Do not change report field meanings, IDs, status semantics, or error codes as part of an internal refactor.
- Add characterization tests before moving behavior.
- Run the full supported Python matrix and package build after each migration slice.
- Do not claim live provider, agent-runtime, network-isolation, legal, or security certification based on mocked tests.

## Phase 3.1 implementation

The first migration seam is `AuditEngine`. It receives a search-registry port, a page-retriever port, and validated configuration. In this slice it delegates to the characterized research workflow, keeping the existing `run_research_task` import path stable. Later slices will move orchestration into the engine and turn the legacy function into a compatibility wrapper.

This is an intentional transitional state, not the completed rewrite.
