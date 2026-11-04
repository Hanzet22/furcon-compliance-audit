"""Evidence-linked factual claims and conservative corroboration summaries."""
from __future__ import annotations

import re
import uuid
from typing import Any


RELATIONSHIPS = {"supports", "contradicts", "qualifies", "context"}
CLAIM_TYPES = {"organizer_statement", "observed_practice", "event_fact",
               "user_supplied_fact", "other"}


def create_claim(
    statement: str,
    actor: str,
    evidence_relations: list[dict[str, str]],
    *,
    claim_type: str = "other",
    activity: str | None = None,
    claim_id: str | None = None,
) -> dict[str, Any]:
    """Create a claim with explicit evidence relationships; never infer legal status."""
    if not isinstance(statement, str) or not statement.strip():
        raise ValueError("statement must be non-empty")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("actor must be non-empty")
    if claim_type not in CLAIM_TYPES:
        raise ValueError("unsupported claim_type")
    if not isinstance(evidence_relations, list):
        raise ValueError("evidence_relations must be a list")
    normalized = []
    seen = set()
    for relation in evidence_relations:
        evidence_id = relation.get("evidence_id")
        relationship = relation.get("relationship")
        if not isinstance(evidence_id, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", evidence_id):
            raise ValueError("each relation requires a valid evidence_id")
        if evidence_id in seen:
            raise ValueError("duplicate evidence_id in claim")
        if relationship not in RELATIONSHIPS:
            raise ValueError("unsupported evidence relationship")
        seen.add(evidence_id)
        normalized.append({"evidence_id": evidence_id, "relationship": relationship})
    identifier = claim_id or "claim_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", identifier):
        raise ValueError("claim_id must be a valid opaque ID")
    return {
        "schema_version": "1.0.0",
        "claim_id": identifier,
        "statement": statement.strip(),
        "actor": actor.strip(),
        "activity": activity,
        "claim_type": claim_type,
        "evidence_ids": [item["evidence_id"] for item in normalized],
        "evidence_relations": normalized,
        "verification_status": "unverified",
    }


def summarize_evidence_independence(claim: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    """Count distinct source identities, not provider hits, as corroborating sources."""
    evidence_by_id = {item.get("evidence_id"): item for item in report.get("evidence", [])}
    retrieval_by_id = {item.get("retrieval_id"): item for item in report.get("retrievals", [])}
    relations = claim.get("evidence_relations", [])
    counts = {name: set() for name in RELATIONSHIPS}
    unresolved = []
    for relation in relations:
        evidence_id = relation.get("evidence_id")
        evidence = evidence_by_id.get(evidence_id)
        if evidence is None:
            unresolved.append(evidence_id)
            continue
        retrieval = retrieval_by_id.get(evidence.get("retrieval_id"))
        if retrieval is None:
            unresolved.append(evidence_id)
            continue
        source_id = retrieval.get("source_id")
        if source_id:
            counts[relation.get("relationship", "context")].add(source_id)
    return {
        "distinct_source_counts": {key: len(value) for key, value in counts.items()},
        "unresolved_evidence_ids": sorted(set(unresolved)),
        "note": "Multiple providers locating the same source count as one source; counts do not establish truth or legal significance.",
    }
