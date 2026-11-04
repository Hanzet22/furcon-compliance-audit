"""Assessment and finding constructors with independent status dimensions."""
from __future__ import annotations

import re
import uuid
from typing import Any


ASSESSMENT_STATUSES = {"supported_concern", "no_issue_observed", "needs_clarification",
                       "not_assessed", "not_applicable"}
SEVERITIES = {"critical", "high", "moderate", "low", "informational"}
CONFIDENCE = {"low", "medium", "high"}


def _ids(values: list[str], label: str) -> list[str]:
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {label} IDs")
    if any(not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", item) for item in values):
        raise ValueError(f"invalid {label} ID")
    return list(values)


def create_assessment(
    *, question: str, assessment_status: str, rationale: str, confidence: str,
    claim_ids: list[str] | None = None, evidence_ids: list[str] | None = None,
    legal_proposition_ids: list[str] | None = None, assessment_id: str | None = None,
) -> dict[str, Any]:
    if not question.strip() or not rationale.strip():
        raise ValueError("question and rationale are required")
    if assessment_status not in ASSESSMENT_STATUSES:
        raise ValueError("unsupported assessment_status")
    if confidence not in CONFIDENCE:
        raise ValueError("unsupported confidence")
    identifier = assessment_id or "assessment_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", identifier):
        raise ValueError("invalid assessment_id")
    return {
        "schema_version": "1.0.0",
        "assessment_id": identifier,
        "question": question.strip(), "assessment_status": assessment_status,
        "rationale": rationale.strip(), "confidence": confidence,
        "claim_ids": _ids(claim_ids or [], "claim"),
        "evidence_ids": _ids(evidence_ids or [], "evidence"),
        "legal_proposition_ids": _ids(legal_proposition_ids or [], "legal proposition"),
    }


def create_finding(
    *, title: str, category: str, assessment_status: str, severity: str,
    confidence: str, rationale: str, assessment_ids: list[str],
    jurisdiction_assessment_ids: list[str] | None = None,
    supporting_evidence_ids: list[str] | None = None,
    contrary_evidence_ids: list[str] | None = None,
    affected_actor: str | None = None, affected_activity: str | None = None,
    recommendation: str | None = None, finding_id: str | None = None,
) -> dict[str, Any]:
    if not title.strip() or not category.strip() or not rationale.strip():
        raise ValueError("title, category, and rationale are required")
    if assessment_status not in ASSESSMENT_STATUSES:
        raise ValueError("unsupported assessment_status")
    if severity not in SEVERITIES or confidence not in CONFIDENCE:
        raise ValueError("severity and confidence must use their independent enums")
    assessments = _ids(assessment_ids, "assessment")
    supporting = _ids(supporting_evidence_ids or [], "supporting evidence")
    contrary = _ids(contrary_evidence_ids or [], "contrary evidence")
    if assessment_status == "supported_concern" and (not assessments or not supporting):
        raise ValueError("supported_concern requires an assessment and supporting evidence")
    identifier = finding_id or "finding_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", identifier):
        raise ValueError("invalid finding_id")
    return {
        "schema_version": "1.0.0",
        "finding_id": identifier,
        "title": title.strip(), "category": category.strip(),
        "assessment_status": assessment_status, "severity": severity,
        "confidence": confidence, "rationale": rationale.strip(),
        "assessment_ids": assessments,
        "jurisdiction_assessment_ids": _ids(jurisdiction_assessment_ids or [], "jurisdiction assessment"),
        "supporting_evidence_ids": supporting, "contrary_evidence_ids": contrary,
        "affected_actor": affected_actor, "affected_activity": affected_activity,
        "recommendation": recommendation,
    }
