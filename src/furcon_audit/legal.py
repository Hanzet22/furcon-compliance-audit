"""Structured legal authority and proposition records.

This module records source classification and paraphrased propositions; it does not
determine whether a regime applies to an event or provide legal advice.
"""
from __future__ import annotations

import re
import uuid
from typing import Any


AUTHORITY_TYPES = {"legislation", "regulation", "court_decision",
                   "official_regulator_guidance", "official_interpretation",
                   "secondary_commentary"}
AUTHORITY_STATUSES = {"current", "amended", "repealed", "historical", "unknown"}
BINDING_STATUSES = {"binding", "persuasive", "guidance", "commentary", "uncertain"}


def _identifier(value: str | None, prefix: str) -> str:
    result = value or prefix + "_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", result):
        raise ValueError("invalid opaque identifier")
    return result


def create_legal_authority(
    *, jurisdiction: str, authority_type: str, title: str,
    retrieval_id: str | None = None, citation: str | None = None,
    issuing_body: str | None = None, official_url: str | None = None,
    publication_date: str | None = None, effective_date: str | None = None,
    end_date: str | None = None, authority_status: str = "unknown",
    original_language: str | None = None, authority_id: str | None = None,
) -> dict[str, Any]:
    if not jurisdiction.strip() or not title.strip():
        raise ValueError("jurisdiction and title are required")
    if authority_type not in AUTHORITY_TYPES:
        raise ValueError("unsupported authority_type")
    if authority_status not in AUTHORITY_STATUSES:
        raise ValueError("unsupported authority_status")
    for date_value in (publication_date, effective_date, end_date):
        if date_value is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
            raise ValueError("dates must use YYYY-MM-DD")
    if official_url is not None and not official_url.startswith(("https://", "http://")):
        raise ValueError("official_url must be HTTP(S)")
    if retrieval_id is not None and not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", retrieval_id):
        raise ValueError("invalid retrieval_id")
    return {
        "schema_version": "1.0.0", "authority_id": _identifier(authority_id, "authority"),
        "jurisdiction": jurisdiction.strip(), "authority_type": authority_type,
        "title": title.strip(), "citation": citation, "issuing_body": issuing_body,
        "official_url": official_url, "retrieval_id": retrieval_id,
        "publication_date": publication_date, "effective_date": effective_date,
        "end_date": end_date, "authority_status": authority_status,
        "original_language": original_language,
    }


def create_legal_proposition(
    *, statement: str, authority_ids: list[str], binding_status: str = "uncertain",
    provision_reference: str | None = None, proposition_id: str | None = None,
) -> dict[str, Any]:
    if not isinstance(statement, str) or not statement.strip():
        raise ValueError("statement must be a non-empty paraphrase")
    if not authority_ids or len(authority_ids) != len(set(authority_ids)):
        raise ValueError("at least one unique authority_id is required")
    if any(not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", item) for item in authority_ids):
        raise ValueError("invalid authority_id")
    if binding_status not in BINDING_STATUSES:
        raise ValueError("unsupported binding_status")
    return {
        "schema_version": "1.0.0", "proposition_id": _identifier(proposition_id, "proposition"),
        "statement": statement.strip(), "authority_ids": list(authority_ids),
        "provision_reference": provision_reference, "binding_status": binding_status,
    }
