# Specification Review

**Review date:** 2026-11-05  
**Review baseline:** `main` at `b716ef8dcc151e8a879e878aa4b87e149a6e2e75`  
**Scope:** The eight v2 specification documents listed below.  
**Review type:** Internal architecture and specification consistency review.

## 1. Executive Summary

The v2 specification set establishes a sound direction: a platform-neutral core, capability-based integrations, cautious legal-applicability analysis, traceable research, and JSON/Markdown as canonical outputs with DOCX as an optional renderer.

The documents are not yet sufficiently aligned to serve as implementation contracts. Several concepts are described consistently in isolation but lack shared definitions, formal data relationships, or machine-validatable contracts.

**Decision: Do not begin core implementation until all P0 findings are resolved and the acceptance criteria in Section 7 are met.**

This is a design/specification review only. It is not a legal opinion, security certification, dependency audit, or proof that any implementation is compliant.

## 2. Documents Reviewed

1. [ARCHITECTURE_SPEC.md](ARCHITECTURE_SPEC.md)
2. [AUDIT_SPEC.md](AUDIT_SPEC.md)
3. [RESEARCH_SPEC.md](RESEARCH_SPEC.md)
4. [JURISDICTION_SPEC.md](JURISDICTION_SPEC.md)
5. [EVIDENCE_SPEC.md](EVIDENCE_SPEC.md)
6. [INTEGRATION_SPEC.md](INTEGRATION_SPEC.md)
7. [AGENT_COMPATIBILITY_SPEC.md](AGENT_COMPATIBILITY_SPEC.md)
8. [REPORT_SPEC.md](REPORT_SPEC.md)

The review also uses the repository's [ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md) as baseline context.

## 3. Document-Level Assessment

| Document | Assessment | Required action |
|---|---|---|
| ARCHITECTURE_SPEC.md | Needs revision | Define module boundaries, shared terminology, and contracts between layers. |
| AUDIT_SPEC.md | Needs revision | Align finding, assessment, and workflow status concepts. |
| RESEARCH_SPEC.md | Direction is sound | Formalize discovery-trail entities and lifecycle. |
| JURISDICTION_SPEC.md | Direction is sound | Preserve cautious applicability reasoning and formalize links to findings. |
| EVIDENCE_SPEC.md | Needs revision | Define Source, Evidence, Claim, Assessment, and Legal Authority as distinct entities. |
| INTEGRATION_SPEC.md | Direction is sound | Specify capability-provider declarations and fallback behavior. |
| AGENT_COMPATIBILITY_SPEC.md | Direction is sound | Keep portability claims provisional until conformance tests exist. |
| REPORT_SPEC.md | Needs revision | Define a complete canonical report contract and validation rules. |

## 4. Findings

### ARC-SPEC-001 — Status namespaces are not explicitly separated

**Priority:** P0  
**Affected documents:** ARCHITECTURE_SPEC.md, AUDIT_SPEC.md, JURISDICTION_SPEC.md, REPORT_SPEC.md

The specifications use several status sets for different concepts:

- Workflow progress: `not_started`, `in_progress`, `completed`, `partial`, `blocked`, `not_applicable`.
- Finding or assessment outcome: `supported_concern`, `no_issue_observed`, `needs_clarification`, `not_assessed`, `not_applicable`.
- Jurisdiction applicability: `applicable_supported`, `potentially_applicable`, `not_established`, `not_applicable_supported`, `not_assessed`.

These are not interchangeable. Define separate, named enums for at least:
1. Workflow status.
2. Assessment status or outcome.
3. Jurisdiction applicability status.
4. Human-review status, once introduced.

Document allowed transitions where lifecycle matters. Avoid a generic `status` field when its namespace is ambiguous; use explicit names such as `workflow_status` and `applicability_status`.

### ARC-SPEC-002 — Evidence and legal reasoning entities need explicit relationships

**Priority:** P0  
**Affected documents:** EVIDENCE_SPEC.md, AUDIT_SPEC.md, JURISDICTION_SPEC.md, REPORT_SPEC.md

The model must distinguish:

- **Source:** A location or publication from which material was retrieved.
- **Retrieval:** A particular capture of source content at a time, through a provider or method.
- **Evidence:** A preserved excerpt, observation, or artifact from a retrieval.
- **Claim:** A proposition about the convention, organizer, participant-facing process, or observed practice.
- **Legal authority:** A statute, regulation, court decision, or other legally relevant authority.
- **Legal proposition:** A specific rule or interpretation drawn from an authority.
- **Assessment:** A reasoned evaluation connecting claims and evidence to criteria or legal propositions.
- **Finding:** A reportable conclusion, including its scope, status, rationale, and limitations.

Recommended conceptual relationships:

`Source → Retrieval → Evidence → Claim → Assessment → Finding`

and separately:

`Legal Authority → Legal Proposition → Assessment`

An organizer's statement is not itself a legal authority. A legal authority does not prove that an organizer follows a particular practice. Assessments must show how the relevant evidence and criteria support the conclusion.

### ARC-SPEC-003 — Formal schema contracts are missing

**Priority:** P0  
**Affected documents:** ARCHITECTURE_SPEC.md, EVIDENCE_SPEC.md, RESEARCH_SPEC.md, REPORT_SPEC.md

Narrative descriptions are not sufficient for interoperable implementation. Define a versioned schema registry with explicit required, optional, and nullable fields; types; enums; identifier formats; reference integrity; and validation expectations.

Initial schema set recommended:

- `audit-request.schema.json`
- `research-task.schema.json`
- `source.schema.json`
- `retrieval.schema.json`
- `evidence.schema.json`
- `claim.schema.json`
- `legal-authority.schema.json`
- `legal-proposition.schema.json`
- `jurisdiction-assessment.schema.json`
- `assessment.schema.json`
- `finding.schema.json`
- `human-review.schema.json`
- `report.schema.json`

The specifications should state the schema dialect, versioning policy, compatibility rules, and migration approach. A schema-valid object must also satisfy documented cross-reference and semantic validation rules.

### ARC-SPEC-004 — Finding-to-jurisdiction relationships are underspecified

**Priority:** P1  
**Affected documents:** AUDIT_SPEC.md, JURISDICTION_SPEC.md, REPORT_SPEC.md

A single finding may concern more than one legal regime, and one jurisdiction assessment may inform more than one finding. Define this as an explicit many-to-many relationship using stable identifiers, rather than copying jurisdiction objects into each finding.

The report must preserve the basis and scope of each applicability assessment. Do not infer applicability solely from attendee nationality, website accessibility, or broad international reach.

### ARC-SPEC-005 — Research-trail lifecycle is incomplete

**Priority:** P1  
**Affected documents:** RESEARCH_SPEC.md, ARCHITECTURE_SPEC.md, REPORT_SPEC.md

The discovery trail needs a lifecycle model that can explain what was searched, what was retrieved, what failed, and what remains unresolved.

At minimum, define:
- `research_task_id`: a planned research unit and its objective.
- `attempt_id`: an individual provider or method attempt.
- `source_id`: a normalized source identity.
- `retrieval_id`: a specific captured version or retrieval event.
- Status, timestamps, provider/method, query or action summary, outcome, and failure/retry information where applicable.

Also specify task completion criteria, retry behavior, source deduplication, page-change handling, merging results across providers, and rediscovery across separate audit runs. Multiple providers returning the same page are not independent corroboration.

### ARC-SPEC-006 — Capability-provider contract needs more precision

**Priority:** P1  
**Affected documents:** INTEGRATION_SPEC.md, ARCHITECTURE_SPEC.md

Providers must declare capabilities, not merely appear in a list of supported tools. Search, page retrieval, browser automation, translation, computation, and rendering are distinct capabilities.

Each provider adapter should declare:
- Capability identifier and supported operations.
- Input and output contract or schema.
- Authentication requirements (without exposing secrets).
- Rate limits and relevant quotas, when known.
- Data handling and retention considerations, when known.
- Known limitations and failure modes.
- Availability or health state.

Fallback selection must be capability-based. For example, a browser automation provider is not a drop-in replacement for a search provider simply because both contribute to research. Provider names in the specification are candidate integrations, not mandatory dependencies.

### ARC-SPEC-007 — Human-review lifecycle is underspecified

**Priority:** P1  
**Affected documents:** AUDIT_SPEC.md, EVIDENCE_SPEC.md, REPORT_SPEC.md

Define a review record that captures:
- Review identifier and target item identifiers.
- Reviewer role, without requiring unnecessary personal data.
- Review status and decision.
- Comments or rationale.
- Review timestamp.
- Specification/schema or report revision reviewed.

Clarify which findings require human review, how requested changes are tracked, and how a reviewed report becomes stale after material changes. Human review must not be represented as legal certification.

### ARC-SPEC-008 — Compatibility claims need a conformance procedure

**Priority:** P2  
**Affected documents:** AGENT_COMPATIBILITY_SPEC.md, ARCHITECTURE_SPEC.md

The compatibility matrix is currently a planning artifact. Before claiming support for Claude Code, Codex, Cursor, Hermes, or another agent environment, define repeatable conformance tests.

Tests should verify skill discovery, metadata handling, tool/capability invocation boundaries, input/output behavior, error handling, and graceful operation when optional tools are unavailable. Distinguish tested compatibility from intended compatibility.

## 5. Design Decisions to Preserve

The following decisions are sound and should remain stable unless new evidence justifies a change:

1. **Platform-neutral core:** Keep business logic independent from agent-specific skill formats.
2. **Thin platform adapters:** Put platform-specific metadata and invocation behavior at the boundary.
3. **Capability-based integrations:** Providers implement defined capabilities; no provider should be a hard dependency without a clear reason.
4. **Canonical outputs:** JSON and Markdown are canonical; DOCX is an optional renderer.
5. **Cautious legal applicability:** Evaluate territorial and material scope, parties, processing activities, thresholds, and exemptions. Do not guess applicability from nationality or website accessibility.
6. **Evidence discipline:** Search results are discovery leads, not legal evidence. Preserve source context and retrieval provenance.
7. **Human review:** Require appropriate review for high-impact legal interpretations and consequential findings.
8. **Honest scope:** Describe the tool as a preliminary compliance/risk review aid, not a legal opinion, certification, or guarantee of compliance.
9. **No adverse inference from silence:** Missing clauses, failed searches, or unavailable pages must not automatically be treated as proof of non-compliance.
10. **Translation provenance:** Preserve original-language material and record whether a translation is machine-generated, human-produced, or otherwise verified.

## 6. Revision Plan

| Priority | Required work | Exit condition |
|---|---|---|
| P0 | Separate and align status namespaces | All documents use the same named enums for the same concepts. |
| P0 | Formalize Source–Retrieval–Evidence–Claim–Authority–Assessment–Finding model | Entity definitions and relationship rules are consistent across specifications. |
| P0 | Define schema registry and validation policy | Required initial schemas and versioning rules are specified. |
| P1 | Define finding/jurisdiction linkage | Stable many-to-many references and reporting rules are documented. |
| P1 | Formalize research-trail lifecycle | Task, attempt, source, and retrieval lifecycle is testable. |
| P1 | Define provider capability declarations | Provider discovery and fallback are capability-driven. |
| P1 | Define human-review lifecycle | Review records, triggers, and stale-review behavior are specified. |
| P2 | Define compatibility conformance tests | Compatibility claims can be reproduced and evidenced. |

## 7. Acceptance Criteria Before Phase 2

The specification set is ready for schema and core implementation only when all of the following are true:

- [ ] All status concepts have distinct names, documented enums, and consistent usage.
- [ ] Source, Retrieval, Evidence, Claim, Legal Authority, Legal Proposition, Assessment, and Finding are defined without conflation.
- [ ] Entity relationships and identifier/reference rules are documented.
- [ ] Initial JSON Schema contracts, schema dialect, and versioning policy are agreed.
- [ ] Jurisdiction assessments link to findings through stable references.
- [ ] Research tasks and attempts have defined lifecycle states and completion criteria.
- [ ] Provider adapters declare capabilities through a common contract.
- [ ] Human review has a defined record and lifecycle.
- [ ] Canonical JSON and Markdown reports can represent provenance, uncertainty, limitations, and review state.
- [ ] Compatibility statements distinguish tested support from planned support.
- [ ] Legal and compliance wording avoids implying certification or legal advice.

## 8. Recommended Phase Order

1. Revise the eight specification documents against all P0 and P1 findings.
2. Cross-review the revised documents for terminology and reference consistency.
3. Define and validate the initial JSON Schemas.
4. Build the platform-neutral domain model and validation layer.
5. Add research and provider adapters behind capability contracts.
6. Add canonical JSON/Markdown report generation.
7. Add optional DOCX rendering.
8. Establish automated tests and compatibility conformance checks before publishing support claims.

## 9. Review Limitations

This review evaluates the specification text available at the stated baseline. It does not execute the repository, install dependencies, test integrations, validate legal sources, or perform a security assessment. Findings describe specification gaps and design risks, not confirmed runtime vulnerabilities.
