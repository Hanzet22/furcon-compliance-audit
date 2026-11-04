"""Human review lifecycle with revision freshness and explicit decision gates."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


TRANSITIONS = {
    "not_required": set(),
    "pending": {"in_review", "not_required"},
    "in_review": {"accepted", "changes_requested", "rejected", "pending"},
    "changes_requested": {"in_review", "rejected"},
    "accepted": {"stale"},
    "rejected": {"stale"},
    "stale": {"in_review"},
}
DECISIONS = {"approve", "request_changes", "reject", "defer", "not_required"}


def requires_human_review(
    *, severity: str | None = None, assessment_status: str | None = None,
    applicability_status: str | None = None, external_publication: bool = False,
) -> bool:
    """Conservative gate for consequential or uncertain interpretations."""
    return (
        severity in {"critical", "high"}
        or assessment_status == "supported_concern"
        or applicability_status in {"applicable_supported", "potentially_applicable", "not_established"}
        or external_publication
    )


def create_review(
    *, target_ids: list[str], reviewer_role: str, revision: str,
    review_status: str = "pending", decision: str = "defer",
    rationale: str | None = None, review_id: str | None = None,
) -> dict[str, Any]:
    if not target_ids or len(target_ids) != len(set(target_ids)):
        raise ValueError("review requires unique target IDs")
    if not reviewer_role.strip() or not revision.strip():
        raise ValueError("reviewer_role and revision are required")
    if review_status not in TRANSITIONS or decision not in DECISIONS:
        raise ValueError("unsupported review status or decision")
    if review_status == "accepted" and decision != "approve":
        raise ValueError("accepted review requires approve decision")
    return {
        "schema_version": "1.0.0",
        "review_id": review_id or "review_" + uuid.uuid4().hex[:20],
        "target_ids": list(target_ids), "reviewer_role": reviewer_role.strip(),
        "review_status": review_status, "decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "revision": revision, "rationale": rationale,
    }


def transition_review(review: dict[str, Any], new_status: str, *,
                      decision: str | None = None, rationale: str | None = None) -> dict[str, Any]:
    current = review.get("review_status")
    if new_status not in TRANSITIONS.get(current, set()):
        raise ValueError(f"invalid review transition: {current} -> {new_status}")
    selected_decision = decision or review.get("decision", "defer")
    if selected_decision not in DECISIONS:
        raise ValueError("unsupported review decision")
    if new_status == "accepted" and selected_decision != "approve":
        raise ValueError("accepted review requires approve decision")
    updated = dict(review)
    updated["review_status"] = new_status
    updated["decision"] = selected_decision
    updated["reviewed_at"] = datetime.now(timezone.utc).isoformat()
    if rationale is not None:
        updated["rationale"] = rationale
    return updated


def mark_review_stale(review: dict[str, Any], current_revision: str) -> dict[str, Any]:
    if not current_revision:
        raise ValueError("current_revision is required")
    if review.get("revision") == current_revision:
        return dict(review)
    status = review.get("review_status")
    if status in {"accepted", "rejected", "in_review"}:
        return transition_review(review, "stale", rationale="Target revision changed after review.")
    return dict(review)


def review_gate(target_id: str, current_revision: str,
                reviews: list[dict[str, Any]]) -> dict[str, Any]:
    matching = [item for item in reviews if target_id in item.get("target_ids", [])]
    accepted = any(item.get("review_status") == "accepted"
                   and item.get("decision") == "approve"
                   and item.get("revision") == current_revision for item in matching)
    return {
        "target_id": target_id,
        "revision": current_revision,
        "accepted": accepted,
        "reason": None if accepted else "No accepted human review matches the current target revision.",
    }
