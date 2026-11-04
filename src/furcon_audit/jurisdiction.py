"""Factor-based jurisdiction applicability records; no nationality-only shortcuts."""
from __future__ import annotations

import re
import uuid
from typing import Any


FACTOR_STATES = {"supported", "not_met", "unclear", "not_assessed"}
EXEMPTION_STATES = {"identified", "not_identified", "unclear", "not_assessed"}
APPLICABILITY = {"applicable_supported", "potentially_applicable", "not_established",
                 "not_applicable_supported", "not_assessed"}


def create_jurisdiction_assessment(
    *,
    regime: str,
    actor: str,
    activity: str,
    applicability_status: str,
    rationale: str,
    legal_proposition_ids: list[str] | None = None,
    territorial_scope: str = "not_assessed",
    material_scope: str = "not_assessed",
    threshold_status: str = "not_assessed",
    exemption_status: str = "not_assessed",
    unresolved_facts: list[str] | None = None,
    jurisdiction_assessment_id: str | None = None,
) -> dict[str, Any]:
    """Record explicit applicability reasoning without calculating legal coverage."""
    for label, value in (("regime", regime), ("actor", actor), ("activity", activity),
                         ("rationale", rationale)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} must be non-empty")
    if applicability_status not in APPLICABILITY:
        raise ValueError("unsupported applicability_status")
    if territorial_scope not in FACTOR_STATES or material_scope not in FACTOR_STATES:
        raise ValueError("scope factors must use supported/not_met/unclear/not_assessed")
    if threshold_status not in FACTOR_STATES:
        raise ValueError("threshold_status must use a supported factor state")
    if exemption_status not in EXEMPTION_STATES:
        raise ValueError("unsupported exemption_status")
    propositions = list(legal_proposition_ids or [])
    if len(propositions) != len(set(propositions)):
        raise ValueError("duplicate legal proposition references")
    if applicability_status in {"applicable_supported", "not_applicable_supported"} and not propositions:
        raise ValueError("supported applicability requires legal proposition references")
    if any(not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", item) for item in propositions):
        raise ValueError("invalid legal proposition ID")
    identifier = jurisdiction_assessment_id or "jurisdiction_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", identifier):
        raise ValueError("invalid jurisdiction_assessment_id")
    return {
        "schema_version": "1.0.0",
        "jurisdiction_assessment_id": identifier,
        "regime": regime.strip(), "actor": actor.strip(), "activity": activity.strip(),
        "applicability_status": applicability_status, "rationale": rationale.strip(),
        "legal_proposition_ids": propositions,
        "territorial_scope": territorial_scope, "material_scope": material_scope,
        "threshold_status": threshold_status, "exemption_status": exemption_status,
        "unresolved_facts": list(unresolved_facts or []),
        "methodology_note": "Do not infer applicability solely from nationality, residence, or website accessibility.",
    }
