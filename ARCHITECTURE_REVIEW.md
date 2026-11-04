# Architecture Review — FurCon Compliance Audit

> **Review type:** Baseline inventory and architecture risk assessment  
> **Repository:** `Hanzet22/furcon-compliance-audit`  
> **Reviewed branch:** `main`  
> **Baseline tree:** `c762286f49ddd6e4353232f1e73b6348e6709e14`  
> **Review date:** 2026-11-05  
> **Current release identified in repository:** `1.2.0`  
> **Status:** Phase 0 — reconnaissance; no implementation changes proposed by this document.

## 1. Executive Summary

The current repository is a compact, Hermes-oriented Agent Skill. It combines convention-source discovery instructions, jurisdiction selection, compliance review guidance, and a DOCX report generator.

The repository is small and understandable, but its responsibilities are coupled to one agent environment and one report format. The main architectural concerns are:

1. **Agent portability:** `SKILL.md` uses custom `triggers` and `requires_tools` frontmatter fields. These are not universal Agent Skills metadata and cannot be assumed to work identically across Claude Code, Codex, Cursor, Hermes, or other agents.
2. **Workflow/rendering mismatch:** the skill promises a Source Discovery Trail in the report, but the current DOCX renderer does not render a dedicated discovery-trail section.
3. **Weak input validation:** the Python wrapper checks only four required keys. It does not validate types, enums, nested objects, URLs, or cross-field consistency against a formal schema.
4. **Insufficient evidence provenance:** findings do not have a structured, per-claim legal-source record. A convention clause and the legal authority used to assess it are not represented as separate, traceable evidence objects.
5. **Jurisdiction overreach risk:** the current tiering instructions can treat participant nationality or broad international reach as enough to trigger laws such as GDPR or CCPA. Applicability requires a fact-specific territorial and material-scope analysis.
6. **Single-output coupling:** DOCX generation is embedded in the main workflow instead of being one replaceable renderer.
7. **Unverified dependency health:** the lockfile records exact package versions, but this repository review has not run a live package vulnerability, deprecation, maintenance, or license-policy scan. No claim that the dependency tree is vulnerability-free is made here.

**Conclusion:** retain the product mission and useful audit workflow, but redesign the implementation around a platform-neutral core, explicit evidence and jurisdiction models, capability-based integrations, schema validation, and independent renderers.

## 2. Repository Inventory

The reviewed recursive Git tree was not truncated and contained these tracked paths:

| Path | Current responsibility | Initial assessment |
|---|---|---|
| `SKILL.md` | Main agent instructions and audit workflow | Useful entry point; too much workflow detail and platform-specific metadata |
| `README.md` | Product description, installation, usage | Hermes-specific claims and instructions |
| `CHANGELOG.md` | Release history | Keep and update during migration |
| `LICENSE` | Project license | Preserve unless maintainers intentionally change licensing |
| `.gitignore` | Local output and environment exclusions | Review when the new build/test layout is defined |
| `examples/sample-audit-data.json` | Example audit payload | Useful migration fixture; does not define a complete schema |
| `scripts/build_report.py` | Python wrapper and minimal validation | Coupled to a Node subprocess |
| `scripts/docx-report.mjs` | DOCX renderer | Report-only responsibility is good, but it currently contains report structure and assumptions directly |
| `scripts/package.json` | Node package metadata | One direct runtime dependency is declared |
| `scripts/package-lock.json` | Locked transitive dependency graph | Must be re-audited against current advisories and package metadata |

No dedicated engine, integration, adapter, schema, test, documentation-reference, or renderer-interface directories are present in the baseline tree.

## 3. Existing Architecture

### 3.1 Current execution flow

```text
User request
   |
   v
Hermes Agent reads SKILL.md
   |
   +--> Search for convention website and T&C/CoC
   |
   +--> Fetch source and infer relevant jurisdictions
   |
   +--> Perform checklist-based compliance analysis
   |
   v
Structured JSON audit payload
   |
   v
scripts/build_report.py
   |
   v
Node.js subprocess
   |
   v
scripts/docx-report.mjs
   |
   v
DOCX report
```

The workflow is primarily instruction-driven. Search, fetching, legal research, evidence handling, and jurisdiction analysis are not implemented as independently testable modules in this repository.

### 3.2 Existing audit categories

The current skill defines nine review categories:

1. Data Privacy and PII handling
2. Refund and Cancellation Policy
3. Liability Waiver and Indemnification
4. Code of Conduct enforcement
5. Age and Minor Protection
6. IP and Content Rights
7. Anti-discrimination and Harassment Policy
8. Dispute Resolution Clause
9. Terms Update and Amendment Clause

These are useful baseline categories. The new design should allow versioned category sets and clearly mark items as applicable, not applicable, or not assessed, with reasons.

### 3.3 Current report structure

The DOCX generator currently renders a cover, disclaimer, executive summary, jurisdiction tier table, detailed findings, optional cross-law comparison, and appendix/methodology.

**Observed mismatch:** the skill explicitly requires a Source Discovery Trail section, but `scripts/docx-report.mjs` does not render that section. The current payload example also lacks a dedicated structured discovery-trail object.

### 3.4 Current validation

`scripts/build_report.py` checks for the presence of `con_name`, `audit_date`, `findings`, and `jurisdiction_tiers`. It does not enforce a formal JSON schema or validate nested finding properties and value types.

The DOCX generator assumes many nested values have expected shapes. Invalid or incomplete data can therefore fail late during rendering or produce incomplete output.

## 4. Findings and Risk Register

Severity here describes architecture and methodology risk, not a legal finding against any convention.

| ID | Area | Finding | Risk | Recommended direction |
|---|---|---|---|---|
| ARC-001 | Agent metadata | `triggers` and `requires_tools` are custom fields, not universal cross-agent metadata | High | Keep portable instructions in the skill entry point; move platform-specific tool declarations into adapters/package guidance |
| ARC-002 | Workflow/report contract | Discovery trail is promised but not rendered or modelled as a dedicated object | High | Define a discovery record in the audit schema and render it consistently |
| ARC-003 | Evidence | Findings lack structured citations to the exact legal authority and source version | Critical | Introduce evidence objects with source identity, jurisdiction, pinpoint reference, access date, and confidence |
| ARC-004 | Jurisdiction | Participant nationality or broad international access is treated too readily as a trigger for specific laws | Critical | Add an applicability assessment with facts, scope tests, assumptions, and unresolved questions |
| ARC-005 | Validation | Minimal key-presence checks only | High | Add versioned JSON Schema validation and semantic validation |
| ARC-006 | Modularity | Discovery, legal research, analysis, and orchestration are mainly embedded in agent instructions | High | Separate workflow stages behind stable interfaces |
| ARC-007 | Output | DOCX is mandatory and is coupled to the main workflow | Medium | Make Markdown and JSON canonical outputs; provide DOCX as an optional renderer |
| ARC-008 | Report layout | US Letter page dimensions are hardcoded | Medium | Make page size and locale configurable; test pagination and table layout |
| ARC-009 | Runtime | Python wrapper launches Node for a single report-generation task | Medium | Choose and document one primary runtime for the core; isolate renderer runtime if justified |
| ARC-010 | Tests | No tracked automated test suite or fixtures beyond one sample payload are present | High | Add unit, schema, integration-contract, renderer, and regression tests |
| ARC-011 | Dependency assurance | Lockfile exists, but live advisory/deprecation/maintenance checks have not been run in this review | Medium / Unknown | Run reproducible package and license scans before selecting the new dependency baseline |
| ARC-012 | Source policy | Official convention sources are required for convention terms, but legal authorities need their own source policy | High | Distinguish convention primary sources, legislation, regulator guidance, and secondary commentary |
| ARC-013 | Translation | No explicit source-language preservation or translation provenance model | Medium | Preserve original text and label translations with provider, timestamp, and review status |
| ARC-014 | Uncertainty | Severity labels do not adequately separate legal applicability, evidence confidence, and assessment status | High | Model these as separate fields; never turn missing evidence into a compliance conclusion |

## 5. Dependency Inventory — Initial, Not a Security Certification

### 5.1 Direct dependency

| Package | Declaration | Lockfile version | Role |
|---|---|---|---|
| `docx` | `^9.6.1` | `9.7.1` | DOCX report generation |

The package metadata declares the package as private and uses ES modules. The lockfile uses lockfile version 3 and records transitive dependencies including `jszip`, `nanoid`, `xml-js`, `xml`, and supporting packages.

### 5.2 What has and has not been checked

Checked from repository files:
- Declared direct dependency and semver range.
- Locked package versions and package metadata present in the lockfile.
- Node engine metadata recorded for selected locked packages.

Not checked in this baseline pass:
- Current npm registry latest versions.
- Current deprecation notices.
- Current GitHub Security Advisories or OSV findings.
- Current maintainer activity and release cadence.
- Full license-policy compatibility review of every transitive dependency.
- Runtime compatibility against a declared minimum Node.js version.
- Reproducible install and report-generation execution.

These checks must be completed before dependency upgrades or a new runtime baseline are approved. A lockfile alone does not prove that dependencies are current or safe.

## 6. Legal-Methodology Corrections Required

The new architecture must avoid turning a screening workflow into an unsupported claim of universal legal compliance.

### 6.1 Jurisdiction applicability

Do not automatically apply a law merely because:
- an attendee is a national or resident of that country;
- a website can be accessed from that country; or
- a convention describes itself as international.

For each candidate law, record the facts relevant to territorial and material scope, the parties and processing activities involved, thresholds or exemptions where relevant, and the authority supporting the conclusion. The outcome should be one of:
- **Applicable** — sufficient facts support application.
- **Potentially applicable** — plausible, but one or more material facts remain unverified.
- **Not established** — available facts do not establish applicability.
- **Not applicable** — scope analysis supports exclusion.
- **Not assessed** — insufficient evidence or outside the review scope.

### 6.2 Source hierarchy

Keep these source classes distinct:
1. Official legislation, regulations, and court decisions.
2. Official regulator or government guidance.
3. Official convention terms, policies, and organizer disclosures.
4. Reputable secondary legal commentary.
5. Search snippets, social posts, forums, and other discovery leads.

Search results are discovery leads, not legal evidence. A convention's official website is the appropriate primary source for its own terms, but it is not the authority for what a statute means.

### 6.3 Evidence and uncertainty

Every material finding should be traceable to:
- the exact convention clause or policy text;
- the legal authority relied on, including jurisdiction and pinpoint provision;
- source publication/version and access date;
- original language and any translation;
- reasoning connecting facts to the authority;
- confidence and unresolved assumptions.

Do not treat a missing clause, unavailable page, or failed search as proof of non-compliance. Distinguish **not found**, **not provided**, **not verified**, **not applicable**, and **compliant**.

### 6.4 Scope and disclaimer

Describe the product as a structured preliminary compliance and risk review, not a full legal audit or legal opinion. A report should state its scope, date, sources, limitations, assumptions, and need for qualified local legal review before formal reliance.

## 7. Target Architecture Requirements

The next architecture should satisfy these requirements before implementation begins.

### 7.1 Platform-neutral core

- Keep `SKILL.md` as a concise entry point describing when to use the skill, safety boundaries, and how to load supporting references.
- Treat platform-specific installation paths, tool names, and invocation conventions as adapter/package concerns.
- Do not claim an agent is supported until its adapter has been tested against a documented version or capability contract.

### 7.2 Capability-based integrations

Define capabilities rather than hard-coding one vendor into the engine. Candidate capabilities include:
- web search and discovery;
- page fetch and structured scraping;
- browser interaction;
- translation;
- computation;
- document rendering.

Providers such as Exa, Tavily, Parallel Search, Firecrawl, Geekflare, Playwright, DeepL, and Wolfram may implement selected capabilities. They are not automatically interchangeable; each adapter must declare its supported operations, limits, and failure modes. The engine should support explicit fallback and report which provider produced each piece of evidence.

### 7.3 Versioned data contracts

Define and validate at least:
- audit request;
- source/discovery record;
- jurisdiction assessment;
- evidence record;
- finding;
- report metadata.

Include schema versioning and migration rules. The schema must distinguish source facts, legal authorities, analytical reasoning, confidence, severity, and applicability.

### 7.4 Independent renderers

Use a canonical structured report model. Markdown and JSON should be available as inspectable outputs. DOCX can remain a supported renderer, but it must not own audit logic or be the only way to access results.

### 7.5 Testability and reproducibility

- Unit-test jurisdiction and evidence logic.
- Validate every fixture against schemas.
- Test each provider adapter with mocked responses and explicit capability contracts.
- Test report renderers against stable fixtures.
- Include regression cases for the current discovery-trail mismatch and invalid payloads.
- Record dependency versions and test runtime versions.
- Never include private attendee data in public fixtures.

## 8. Proposed Migration Sequence

| Phase | Work | Exit condition |
|---|---|---|
| 0 — Reconnaissance | Inventory repository, identify architecture and methodology risks, record dependency review gaps | This review is committed and baseline is fixed |
| 1 — Specification | Define scope, evidence model, jurisdiction model, audit workflow, report contract, and compatibility targets | Specifications are reviewed and internally consistent |
| 2 — Core and schemas | Implement versioned schemas, validation, orchestration contracts, and core models | Fixtures pass schema and semantic validation |
| 3 — Integrations | Add provider capability interfaces and selected provider adapters | Each adapter passes contract tests and records provenance |
| 4 — Agent adapters | Package/test supported agent entry points and installation guidance | Compatibility claims match tested versions |
| 5 — Reporting | Implement Markdown, JSON, and optional DOCX renderers | All renderers consume the same canonical report model |
| 6 — Verification | Run regression, security, dependency, license, and compatibility checks | Release gates pass and limitations are documented |
| 7 — Cutover | Replace or retire legacy layout while retaining migration notes and history | New release is reproducible and old workflow is no longer the default |

## 9. Baseline Decisions

The following are recommended design decisions, not implementation changes:

- **Preserve:** the general FurCon audit mission, source discovery, nine baseline review categories, constructive tone, and preliminary-review disclaimer.
- **Redesign:** jurisdiction analysis, evidence capture, validation, orchestration, integration contracts, and report generation.
- **Make optional:** DOCX as the sole output and any provider-specific search or scraping dependency.
- **Do not assume:** every participant's country automatically creates legal applicability; every search provider supports the same operations; or every agent interprets custom skill metadata the same way.
- **Do not delete yet:** legacy scripts, sample data, or release history until replacement tests and migration mapping exist.

## 10. References and Review Boundaries

Relevant Agent Skills/platform documentation to verify during adapter design:

- [OpenAI — Skills in the API](https://developers.openai.com/api/docs/guides/tools-skills)
- [Claude — Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Cursor — Skills documentation](https://prod.cursor.com/docs/skills)
- [Hermes Agent — Skills system](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)

These references describe platform conventions; they do not establish that one package layout or metadata field works identically across all agents. Re-check official documentation at implementation time and record tested versions.

This document is a repository architecture review, not a legal opinion, security certification, or completed dependency vulnerability scan.
