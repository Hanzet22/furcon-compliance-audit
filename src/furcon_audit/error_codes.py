"""Stable error codes for API and adapter boundaries.

Messages are intentionally non-sensitive. Never include credentials, authorization
headers, or raw secret-bearing request payloads in error metadata.
"""

SCHEMA_VERSION = "1.0.0"

ERROR_CODES = frozenset({
    "invalid_input",
    "schema_validation_failed",
    "reference_validation_failed",
    "provider_unavailable",
    "provider_rate_limited",
    "provider_error",
    "retrieval_blocked",
    "retrieval_failed",
    "capability_unavailable",
    "operation_unsupported",
    "human_review_required",
    "internal_error",
})

RETRYABLE_ERROR_CODES = frozenset({
    "provider_rate_limited",
    "provider_error",
    "retrieval_failed",
})

def error_envelope(code: str, message: str, *, retryable: bool = False,
                   provider_id: str | None = None,
                   correlation_id: str | None = None) -> dict:
    """Build a stable, schema-versioned error document."""
    if code not in ERROR_CODES:
        raise ValueError(f"Unknown error code: {code}")
    if not isinstance(message, str) or not message.strip() or len(message) > 1000:
        raise ValueError("message must contain 1 to 1000 characters")
    if not isinstance(retryable, bool):
        raise ValueError("retryable must be a boolean")
    if provider_id is not None and not isinstance(provider_id, str):
        raise ValueError("provider_id must be a string or None")
    if correlation_id is not None:
        if (not isinstance(correlation_id, str)
                or not 8 <= len(correlation_id) <= 80
                or not all(c.isalnum() or c in "_-" for c in correlation_id)):
            raise ValueError("correlation_id must be 8-80 safe identifier characters")
    return {
        "schema_version": SCHEMA_VERSION,
        "code": code,
        "message": message.strip(),
        "retryable": retryable,
        "provider_id": provider_id,
        "correlation_id": correlation_id,
    }
