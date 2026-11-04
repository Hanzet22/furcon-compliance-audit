# Evidence Specification

**Status:** Draft specification  
**Purpose:** Define provenance, source quality, claim support and uncertainty.

## 1. Evidence model

A report claim MUST be traceable to one or more evidence records. Evidence records and findings are separate entities: a source may support multiple claims, and a claim may require multiple sources.

### 1.1 Evidence record fields

Minimum recommended fields:

| Field | Meaning |
|---|---|
| `evidence_id` | Stable unique identifier |
| `source_id` | Link to source registry record |
| `claim_supported` | Proposition the evidence is used to assess |
| `locator` | Page, section, paragraph, timestamp or fragment |
| `excerpt` | Short relevant quotation or faithful paraphrase |
| `language` | Language of original material |
| `retrieved_at` | Timestamp with timezone |
| `published_at` | Publication date, if known |
| `effective_from/to` | Applicable period, if known |
| `source_role` | Legal authority, policy, operational material, etc. |
| `support_type` | Supports, contradicts, qualifies or contextualizes |
| `limitations` | Missing context, stale content, ambiguity, access limits |
| `integrity` | Hash or snapshot reference when feasible |

## 2. Source provenance

A source record SHOULD preserve:
- canonical and final URL;
- title and issuing organization;
- source class and authority type;
- content type;
- original language;
- publication/update/effective dates;
- retrieval timestamp and method;
- provider/adapter;
- redirect chain where material;
- archived/snapshot location or hash where permitted.

Do not treat the retrieval provider as the source author.

## 3. Claim-to-evidence relationship

For each material factual or legal proposition:
- state the claim narrowly;
- link supporting evidence;
- link contrary or qualifying evidence;
- identify whether the claim is directly stated or inferred;
- explain the inference;
- record confidence and limitations.

A source that merely mentions a topic does not necessarily support a specific conclusion. Search snippets are discovery leads, not final evidence.

## 4. Authority hierarchy

Authority depends on the proposition being tested:
- binding legislation and court decisions for legal rules;
- official regulator material for regulator position/guidance;
- signed terms/contracts and official policies for contractual or operational statements;
- official event/venue pages for public representations;
- secondary commentary for context;
- social media and forums for leads or attributed observations only.

Do not collapse all “official” material into one legal authority tier.

## 5. Confidence model

Confidence is an assessment of evidence quality, not probability:
- **High:** direct, current, authoritative and clearly relevant; corroboration where appropriate.
- **Medium:** credible and relevant but incomplete, indirect or limited.
- **Low:** ambiguous, stale, unverified or weakly connected.

Record why confidence was assigned. Conflicting sources should be preserved and explained, not silently resolved.

## 6. Translation provenance

For translated material, record:
- original text or source reference;
- original language;
- target language;
- translation provider/tool and version if known;
- translation timestamp;
- whether machine or human translated;
- reviewer status;
- terms whose meaning is legally material.

Machine translation MUST NOT silently replace the original. Material legal wording requires qualified review.

## 7. Evidence handling and privacy

Collect only the minimum excerpt necessary. Respect copyright; do not reproduce entire policies or large source passages. Redact personal data not required for the claim. Avoid storing attendee lists, identity documents, private messages or sensitive information unless explicitly necessary, authorized and governed by a documented retention basis.

Evidence snapshots MUST be access-controlled and retention-limited. Logs MUST NOT contain secrets.

## 8. Validation rules

A material finding cannot be marked evidence-supported unless:
- at least one valid evidence ID is linked;
- the cited locator is usable;
- the evidence supports the stated proposition;
- source identity and retrieval time are present or explicitly unknown;
- limitations and contrary evidence are considered.

If no evidence is available, use an appropriate clarification/not-assessed status rather than inventing support.
