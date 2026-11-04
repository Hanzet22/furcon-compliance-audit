"""Explicit evidence capture from a successful retrieval.

Evidence is a deliberately selected excerpt/observation, never an automatic legal conclusion.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any
import uuid


def create_evidence(
    capture: dict[str, Any],
    excerpt: str,
    *,
    kind: str = "quotation",
    locator: str | None = None,
    original_language: str | None = None,
    evidence_id: str | None = None,
) -> dict[str, Any]:
    """Create one evidence record from an explicitly selected passage.

    The excerpt must occur verbatim in extracted text. Failed/blocked retrievals cannot
    produce evidence. The original source content remains in the retrieval bundle.
    """
    retrieval = capture.get("retrieval") or {}
    content = capture.get("content") or {}
    source = capture.get("source") or {}
    if retrieval.get("outcome") != "success" or not content:
        raise ValueError("Evidence requires a successful retrieval with content.")
    if kind not in {"quotation", "observation", "document_artifact", "metadata"}:
        raise ValueError("Unsupported evidence kind.")
    if not isinstance(excerpt, str) or not excerpt.strip():
        raise ValueError("excerpt must be a non-empty string.")
    extracted = content.get("extracted_text")
    if not isinstance(extracted, str) or excerpt not in extracted:
        raise ValueError("excerpt must match the retrieved extracted text verbatim.")
    source_url = source.get("canonical_url") or content.get("final_url")
    if not isinstance(source_url, str) or not source_url.startswith(("https://", "http://")):
        raise ValueError("A retrieved source URL is required.")
    record_id = evidence_id or "evidence_" + uuid.uuid4().hex[:20]
    if not re.fullmatch(r"[a-z][a-z0-9_-]{2,63}", record_id):
        raise ValueError("evidence_id must be a valid opaque ID.")
    digest = retrieval.get("content_hash")
    if digest is not None and not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("retrieval content_hash must be a SHA-256 hex digest.")
    return {
        "schema_version": "1.0.0",
        "evidence_id": record_id,
        "retrieval_id": retrieval.get("retrieval_id"),
        "kind": kind,
        "excerpt": excerpt,
        "locator": locator,
        "original_language": original_language or content.get("language"),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "content_hash": digest,
    }
