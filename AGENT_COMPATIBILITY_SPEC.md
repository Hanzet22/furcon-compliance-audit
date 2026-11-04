# Agent Compatibility Specification

**Status:** Draft specification  
**Purpose:** Portable distribution across agent runtimes and coding assistants.

## 1. Compatibility objective

Keep audit methodology and domain contracts independent of a specific agent platform. Platform-specific packaging belongs in thin adapters and manifests.

## 2. Portable core

The portable core consists of:
- this specification set;
- versioned schemas;
- deterministic validation and domain rules;
- provider capability contracts;
- prompt/workflow instructions expressed without vendor-only metadata;
- test fixtures and examples.

The core MUST remain usable when no optional provider is connected. Missing capabilities must produce explicit unavailable states.

## 3. Platform adapters

Adapters MAY include platform-native manifests, tool declarations, slash commands, hooks or skill metadata. Each adapter MUST:
- declare supported platform and tested version range;
- map platform tools to internal capability contracts;
- document required permissions;
- avoid duplicating legal methodology;
- preserve canonical output schemas;
- declare unsupported features and fallbacks.

Custom frontmatter fields such as `triggers` or `requires_tools` MUST NOT be assumed to be universally understood. Put portable requirements in ordinary documentation and platform-specific metadata in the relevant adapter.

## 4. Agent behavior contract

An agent using this skill MUST:
1. Confirm scope and material assumptions.
2. Use only available, authorized capabilities.
3. Distinguish discovery from verified evidence.
4. Record research queries and retrieval outcomes.
5. Assess applicability per legal regime and activity.
6. Separate assessment status, severity and confidence.
7. Preserve uncertainty and contradictory evidence.
8. Validate structured outputs before reporting.
9. Identify when human specialist review is needed.
10. Never claim certification or legal opinion.

The agent MUST NOT fabricate sources, dates, legal provisions, provider results, test outcomes or repository state.

## 5. Tool permission tiers

- **Read-only research:** search, fetch, browser inspection and document reading.
- **Local processing:** schema validation, parsing, translation and rendering.
- **External side effects:** account creation, submissions, purchases, messages, uploads or configuration changes.

The default authorization covers only read-only research and local processing. External side effects require separate, explicit user authorization and may remain prohibited by the deployment policy.

## 6. Platform matrix

Maintain a tested matrix rather than asserting universal compatibility:

| Platform | Adapter location | Manifest/version | Tested status |
|---|---|---|---|
| Claude Code | platform adapter | Record exact supported format | Not yet verified |
| Codex | platform adapter | Record exact supported format | Not yet verified |
| Cursor | platform adapter | Record exact supported format | Not yet verified |
| Hermes | platform adapter | Record exact supported format | Not yet verified |
| Agent Skills-compatible hosts | portable package | Record spec/version | Not yet verified |

Do not label a platform “supported” until a reproducible smoke test passes on a documented version.

## 7. Packaging and versioning

- Version the portable core independently from platform adapters.
- Document compatibility and breaking changes.
- Pin or constrain provider dependencies in adapter manifests.
- Keep secrets out of package files and examples.
- Include license, attribution and security notes in every distribution package.
- Provide a minimal no-provider mode for local schema validation and report drafting.

## 8. Conformance tests

A platform adapter conforms when it:
- loads the correct instructions;
- exposes only declared capabilities;
- produces canonical schema-valid output;
- handles unavailable tools without fabricating results;
- preserves evidence provenance;
- passes safety and prompt-injection fixtures;
- documents platform-specific limitations.
