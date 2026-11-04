"""Capability ports and provider registry. No provider SDK is imported here."""
from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass(frozen=True)
class CapabilityDeclaration:
    provider_id: str
    provider_version: str
    capability_id: str
    operations: tuple[str, ...]
    auth_required: bool = False
    rate_limit_per_minute: int | None = None
    availability: str = "unknown"
    limitations: tuple[str, ...] = ()

class CapabilityAdapter(Protocol):
    declaration: CapabilityDeclaration
    def execute(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]: ...

class CapabilityRegistry:
    """Resolve only adapters that provide the requested capability and operation."""
    def __init__(self) -> None:
        self._adapters: list[CapabilityAdapter] = []

    def register(self, adapter: CapabilityAdapter) -> None:
        self._adapters.append(adapter)

    def candidates(self, capability_id: str, operation: str) -> list[CapabilityAdapter]:
        return [
            adapter for adapter in self._adapters
            if adapter.declaration.capability_id == capability_id
            and operation in adapter.declaration.operations
            and adapter.declaration.availability == "available"
        ]

    def execute_first(self, capability_id: str, operation: str,
                      payload: dict[str, Any]) -> dict[str, Any]:
        candidates = self.candidates(capability_id, operation)
        if not candidates:
            raise LookupError(f"No available adapter for {capability_id}:{operation}")
        # Routing order is registration order; policy-based ranking belongs to the host.
        return candidates[0].execute(operation, payload)
