# Architecture Specification

**Status:** Draft specification  
**Target:** FurCon Compliance Audit v2 architecture  
**Baseline:** `ARCHITECTURE_REVIEW.md`  
**Normative language:** MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are used as requirements terms.

## 1. Purpose

Define a platform-neutral, evidence-led system for preliminary compliance and operational-risk reviews of furry conventions and related events. The core MUST remain independent of any single agent runtime, search vendor, programming language wrapper or report renderer.

This document defines boundaries and contracts. It does not claim that the current implementation already conforms.

## 2. Design principles

1. **Evidence before conclusions:** every material finding must trace to reviewed evidence.
2. **Jurisdiction before legal conclusion:** applicability is assessed per law, actor, activity and territory.
3. **Provider neutrality:** integrations implement capability contracts; no vendor is mandatory.
4. **Fail visibly:** unavailable, blocked, stale or incomplete research is recorded, never silently treated as a negative result.
5. **Reproducibility:** preserve query, retrieval time, source identity, transformations and schema versions.
6. **Human review:** legal interpretation and high-impact conclusions require qualified human review.
7. **Privacy by design:** collect the minimum data needed; avoid attendee-level personal data unless strictly necessary and authorized.
8. **Accessible, portable outputs:** canonical JSON and Markdown; optional renderers such as DOCX and HTML.
9. **Safe defaults:** read-only research, no account creation, form submission, purchases, contact or access-control bypass.

## 3. Logical architecture

```text
Agent / CLI / UI adapters
          |
       Use cases
          |
   Domain core + policies
     /       |        \
Schemas   Evidence   Audit rules
     \       |        /
       Capability ports
          |
   Provider adapters
(search / fetch / browser / translate / compute / render)
          |
    External sources
```

### 3.1 Layers

- **Adapters:** accept platform-specific input and expose results in the host's expected format. They MUST NOT own legal rules.
- **Application/use cases:** orchestrate audit stages, state transitions, retries, checkpoints and cancellation.
- **Domain core:** contains audit concepts, applicability logic, finding states, evidence relationships and policy rules.
- **Schemas/contracts:** versioned machine-readable definitions and validation rules.
- **Ports:** capability interfaces for search, fetch, browser, translation, computation, storage and rendering.
- **Providers:** concrete implementations for individual tools/services.
- **Renderers:** transform canonical report data into human-readable formats.

### 3.2 Core modules

| Module | Responsibility | Must not do |
|---|---|---|
| Intake | Normalize event scope and constraints | Infer legal applicability |
| Planner | Create research plan and coverage checklist | Invent sources or findings |
| Discovery | Find candidate sources | Treat snippets as proof |
| Acquisition | Retrieve source content safely | Bypass access controls |
| Verification | Assess authority, identity, date and relevance | Guarantee source truth |
| Jurisdiction | Assess law-specific applicability | Infer from nationality alone |
| Audit | Map evidence to controls and findings | Convert unknown into compliant/non-compliant |
| Validation | Enforce schemas and cross-field invariants | Silently repair material facts |
| Reporting | Produce canonical and rendered outputs | Add unsupported conclusions |

## 4. Workflow and state

The default workflow is:

1. Intake and scope confirmation.
2. Risk and privacy constraints.
3. Research planning.
4. Source discovery.
5. Source acquisition and verification.
6. Jurisdiction-specific applicability assessment.
7. Control/category review.
8. Finding drafting and evidence linkage.
9. Coverage and consistency validation.
10. Human review.
11. Canonical report generation and optional rendering.

Each stage MUST emit a structured status: `not_started`, `in_progress`, `completed`, `partial`, `blocked` or `not_applicable`. A blocked stage MUST include a reason. Partial work MUST identify what remains unknown.

## 5. Data flow and trust boundaries

External pages, search results, files and tool output are untrusted data. They MUST be treated as content, not instructions. Prompt injection or embedded instructions in retrieved material MUST NOT alter system policy, invoke tools, or expand scope.

Secrets and credentials MUST never be written into reports, logs, examples or source-control. Provider credentials belong in the host's secret manager or environment configuration.

Personal data SHOULD be redacted or excluded from evidence snapshots unless needed to substantiate a specific issue. Retention and deletion rules MUST be configurable and documented.

## 6. Cross-cutting requirements

- Every artifact MUST carry a schema version and generation timestamp.
- Dates MUST include timezone or be explicitly marked unknown.
- Locale, language and translation status MUST be represented.
- All network operations MUST have timeouts, bounded retries and rate-limit handling.
- Provider failures MUST be visible and must not be interpreted as evidence of absence.
- Deterministic transformations SHOULD be separated from probabilistic model judgments.
- Audit runs SHOULD support checkpoints and resumability without duplicating evidence.
- Logs MUST avoid unnecessary personal data and secrets.

## 7. Architecture decisions

- Canonical formats: JSON for interchange and Markdown for readable source report.
- DOCX, HTML and PDF are optional renderers, not the source of truth.
- No fixed page size in domain logic; renderer configuration controls paper size and locale.
- No mandatory Python-to-Node subprocess for core validation or orchestration.
- JSON Schema (or an equivalent formally versioned schema system) is the baseline contract.
- Vendor integrations are optional adapters behind capability ports.

## 8. Acceptance criteria

The architecture is acceptable when:
- the domain core can run without a specific agent platform;
- a missing provider can be replaced by another provider or an explicit unavailable state;
- canonical JSON validates independently of rendering;
- reports can be generated as Markdown without DOCX dependencies;
- every finding has traceable evidence or an explicit no-evidence/assessment-needed state;
- jurisdiction decisions preserve uncertainty and rationale;
- tests cover domain rules, schemas, adapters and renderer behavior;
- retrieved content cannot act as executable instructions.

## 9. Related specifications

See `AUDIT_SPEC.md`, `RESEARCH_SPEC.md`, `JURISDICTION_SPEC.md`, `EVIDENCE_SPEC.md`, `INTEGRATION_SPEC.md`, `AGENT_COMPATIBILITY_SPEC.md` and `REPORT_SPEC.md`.
