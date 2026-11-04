# Report Specification

**Status:** Draft specification  
**Purpose:** Define canonical report structure, validation and optional output renderers.

## 1. Canonical output

JSON is the canonical machine-readable artifact. Markdown is the canonical human-readable source report. DOCX, HTML and PDF are optional renderings generated from validated canonical data.

A renderer MUST NOT introduce new findings, alter applicability statuses or silently omit material limitations.

## 2. Top-level report structure

Recommended top-level fields:

- `schema_version`
- `report_id`
- `audit_id`
- `event`
- `organizers`
- `scope`
- `audit_metadata`
- `jurisdiction_assessments`
- `category_assessments`
- `findings`
- `source_registry`
- `evidence_records`
- `research_trail`
- `limitations`
- `unresolved_questions`
- `human_review`
- `generated_at`

All timestamps MUST use ISO 8601 with timezone. Unknown values should be null or an explicit unknown state, not guessed.

## 3. Finding structure

Each finding SHOULD include:
- stable finding ID;
- title and concise description;
- category/control reference;
- affected actor/activity;
- assessment status;
- severity and rationale;
- confidence and rationale;
- jurisdiction assessment references, if relevant;
- criterion or requirement and its source;
- supporting evidence IDs;
- contrary/qualifying evidence IDs;
- recommendation;
- unresolved questions;
- human-review status.

Findings MUST distinguish observed facts from analysis and recommendations.

## 4. Research trail

The report MUST include a Source Discovery Trail generated from structured research records. It SHOULD show:
- research task and question;
- query/provider/timestamp;
- candidate source and disposition;
- retrieval status;
- verification outcome;
- reason for exclusion or unresolved state.

Do not expose secrets, private query data or unnecessary personal information.

## 5. Report sections

A readable report SHOULD contain:

1. Cover and report metadata.
2. Executive summary with scope and limitations.
3. Event and organizer context.
4. Methodology and assessment labels.
5. Jurisdiction applicability summary.
6. Category-by-category assessment.
7. Findings and recommendations.
8. Source Discovery Trail.
9. Evidence/source register.
10. Unresolved questions and human-review items.
11. Appendices and glossary, where useful.

The executive summary MUST NOT imply a complete legal compliance determination.

## 6. Validation

Validate JSON against a versioned schema and run semantic checks, including:
- unique IDs;
- all referenced evidence/source IDs exist;
- each finding has a valid status;
- severity and confidence use separate enumerations;
- jurisdiction references resolve;
- dates are well-formed;
- required rationale exists for applicability decisions;
- no finding marked supported lacks evidence;
- partial/blocked research has a reason;
- report scope and limitations are present.

Schema validation alone is not sufficient; cross-reference and semantic validation are required.

## 7. Renderer requirements

- **Markdown:** must be available without external document-generation dependencies.
- **DOCX:** optional; paper size, margins, language and styles configurable.
- **HTML:** optional; semantic structure and accessible headings.
- **PDF:** optional; generated from a validated source artifact with selectable text where feasible.

Renderers MUST support long URLs, multilingual text, tables and pagination without assuming US Letter. Renderer failure must not invalidate canonical JSON/Markdown.

## 8. Versioning and migration

Every report declares its schema version. Breaking field or semantic changes require a major schema version and migration guidance. Migrations MUST be explicit and tested; unknown fields must not be silently discarded.

## 9. Distribution checklist

Before release:
- canonical JSON validates;
- Markdown contains all required sections;
- source and evidence references resolve;
- renderer output is checked for truncation and layout defects;
- limitations and human-review status are visible;
- no personal data or secrets leak;
- output format and schema version are declared.
