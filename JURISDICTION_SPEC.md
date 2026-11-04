# Jurisdiction Specification

**Status:** Draft specification  
**Purpose:** Structured, cautious assessment of whether a particular legal regime may apply to a particular actor and activity.

## 1. Core rule

Jurisdictional applicability MUST be evaluated law by law, actor by actor and processing/activity by processing/activity. It MUST NOT be inferred solely from attendee nationality, website accessibility, international participation, currency, language or a broad claim that an event is “global”.

This specification defines a research framework, not legal advice.

## 2. Required dimensions

For each potentially relevant legal regime, assess:

1. **Territorial nexus:** establishment, place of conduct, targeted market, affected persons, territorial effects or other statutory connecting factors.
2. **Material scope:** whether the activity and subject matter fall within the law's defined scope.
3. **Actor/role:** controller, processor, business, service provider, employer, venue operator, organizer, vendor or other legally defined role, as applicable.
4. **Thresholds and exemptions:** revenue, size, volume, activity type, nonprofit status, household/personal-use exclusions or other statutory tests.
5. **Activity nexus:** which specific processing, transaction, employment, consumer interaction or event operation is involved.
6. **Timing:** law in force at the relevant date, transitional provisions and amendments.
7. **Evidence quality:** facts supporting or contradicting each element.

The exact tests differ by legal regime; do not mechanically apply one jurisdiction's criteria to another.

## 3. Applicability statuses

Use:
- `applicable_supported`: available facts support that the legal regime applies to the actor/activity.
- `potentially_applicable`: a plausible nexus exists but one or more material elements need verification.
- `not_established`: evidence is insufficient to determine applicability.
- `not_applicable_supported`: evidence supports that a required element is absent or an exclusion applies.
- `not_assessed`: no meaningful assessment was completed.

These labels describe the evidence-based review state, not a binding legal determination.

## 4. Per-law assessment record

Each record SHOULD include:
- regime name and jurisdiction;
- version/effective date reviewed;
- actor and role;
- activity/processing under review;
- territorial nexus facts;
- material-scope analysis;
- threshold/exemption analysis;
- supporting and contrary evidence IDs;
- unresolved questions;
- status and rationale;
- confidence;
- human-review requirement and reviewer outcome.

## 5. Common reasoning errors to avoid

- Treating nationality of a participant as sufficient to trigger a law.
- Treating public website accessibility as sufficient targeting or establishment.
- Assuming a foreign organizer has no obligations because it lacks a local office, without checking the law's extraterritorial rules.
- Assuming a nonprofit or volunteer-run event is automatically exempt.
- Applying a business threshold without checking definitions, aggregation rules or relevant time period.
- Treating a vendor's legal role as identical to the organizer's role.
- Applying current law retroactively without examining the event date and transitional rules.

## 6. Cross-border processing

Map data flows and roles where relevant:
- who collects the information;
- on whose behalf;
- where parties are established;
- where individuals are located;
- where data is stored or accessed;
- which vendors/subprocessors participate;
- whether transfers or disclosures occur.

Do not infer data location or transfer solely from a vendor's brand or headquarters. Seek contractual and technical evidence, and mark unknowns.

## 7. Legal authority

Use primary legal text and official legal sources for legal propositions. Regulator guidance can clarify interpretation but must be labeled as guidance. Secondary commentary is contextual and cannot replace primary authority where the legal text is available.

Record the exact provision/section, version, effective date and URL. If authoritative text cannot be verified, lower confidence and flag specialist review.

## 8. Human review

Escalate material ambiguity, conflicting authorities, uncertain statutory interpretation, high-impact findings or proposed legal conclusions to a qualified lawyer in the relevant jurisdiction. The system MUST NOT represent its output as a legal opinion.
