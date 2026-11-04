"""Application-facing ports for external capabilities and retrieval."""
from __future__ import annotations

from typing import Any, Protocol


class SearchGateway(Protocol):
    """Port implemented by a capability registry or a compatible search gateway."""

    def execute_with_fallback(
        self, capability_id: str, operation: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        ...


class PageRetriever(Protocol):
    """Port for the controlled public-page retrieval implementation."""

    def __call__(
        self, url: str, *, attempt_id: str, **options: Any
    ) -> dict[str, Any]:
        ...
