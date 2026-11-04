# Audit Specification

**Status:** Draft specification  
**Target:** FurCon Compliance Audit v2  
**Scope:** Preliminary compliance, governance and operational-risk review; not legal advice or certification.

## 1. Objective

Provide a repeatable method to identify documented controls, potential gaps, unresolved questions and practical risk-reduction actions for furry conventions and related events. The system evaluates available evidence; it does not certify an event as legally compliant.

## 2. Scope definition

Every audit request MUST identify, where known:

- event/convention name and official web presence;
- event dates, venue and relevant operating locations;
- organizer entity/entities and known roles;
- activities under review (ticketing, registration, vendors, photography, online services, staff/volunteers, accessibility, safety, sponsorship, etc.);
- target review period and evidence cut-off date;
- requested jurisdictions and reasons for considering them;
- exclusions, assumptions and access limitations.

Unknown information MUST be marked unknown, not guessed. The scope MUST distinguish organizer-controlled activities from venue, vendor, ticketing-platform and sponsor activities.

## 3. Review categories

Categories are configurable and may be expanded when relevant:

1. Governance, organizer identity and accountability.
2. Privacy notices, personal-data handling and retention.
3. Registration, ticketing, payment and refund information.
4. Photography, recording, consent and media publication.
5. Accessibility, accommodations and inclusive participation.
6. Venue, event safety and incident-management information.
7. Staff, volunteers, vendors and contractor terms.
8. Community conduct, harassment reporting and moderation.
9. Sponsorship, advertising, disclosures and partner claims.
10. Online services, security disclosures and account practices.

A category may be `in_scope`, `out_of_scope`, `not_assessed` or `not_applicable`, with rationale.

## 4. Assessment lifecycle

For each category/control:

1. Define the question being tested.
2. Identify potentially relevant actors and activities.
3. Identify potentially applicable legal or contractual requirements.
4. Discover authoritative and contextual sources.
5. Verify source identity, currency, jurisdiction and relevance.
6. Record what the evidence directly establishes.
7. Compare observed evidence with the stated criterion.
8. Assign assessment status and confidence separately.
9. Draft a proportionate recommendation.
10. Route legal or high-impact uncertainty for human review.

A missing webpage, failed search, inaccessible policy or absent public statement is not proof that an internal process does not exist.

## 5. Finding states and severity

### 5.1 Assessment status

Use one of:

- `supported_concern`: evidence supports a potential gap or risk.
- `no_issue_observed`: reviewed evidence did not reveal the tested issue; this is not proof of full compliance.
- `needs_clarification`: relevant facts are missing or ambiguous.
- `not_assessed`: insufficient review was performed.
- `not_applicable`: the criterion does not apply, with rationale.

### 5.2 Severity

Severity describes potential impact if the concern is real; it is not a legal verdict.

- `critical`: credible potential for severe harm or major legal/operational exposure requiring urgent human attention.
- `high`: substantial impact or broad exposure.
- `moderate`: meaningful but bounded impact.
- `low`: limited impact or primarily documentation/process weakness.
- `informational`: observation or improvement opportunity without a demonstrated material risk.

Severity MUST be accompanied by rationale. Do not derive severity from confidence or legal applicability.

### 5.3 Confidence

Confidence describes support for the factual assessment:

- `high`: direct, current, authoritative evidence with corroboration where appropriate.
- `medium`: relevant evidence exists but has limitations or incomplete corroboration.
- `low`: indirect, ambiguous, stale or weakly supported evidence.

Confidence is not a probability and MUST NOT be presented as one.

## 6. Recommendations

Recommendations SHOULD be specific, feasible, prioritized and linked to the concern. Distinguish:
- immediate containment or clarification;
- policy/documentation improvements;
- operational process improvements;
- specialist legal/security/accessibility review.

Do not prescribe a single legal solution when facts or local law remain unresolved. Avoid requesting unnecessary attendee personal data.

## 7. Coverage and limitations

The report MUST show:
- categories in scope and out of scope;
- categories assessed, partially assessed and not assessed;
- sources and dates reviewed;
- inaccessible or unavailable sources;
- assumptions and unresolved questions;
- review cut-off date;
- whether human legal review occurred.

No aggregate “compliance score” SHOULD be generated unless a separately documented, validated methodology exists. A score must never imply certification.

## 8. Quality gates

Before release, verify:
- every concern has a clear criterion and evidence trail;
- status, severity and confidence are separate fields;
- applicability is justified per relevant law;
- absence of evidence is not treated as evidence of absence;
- recommendations are proportionate;
- scope and limitations are visible;
- no unsupported claim of full legal compliance is made.
