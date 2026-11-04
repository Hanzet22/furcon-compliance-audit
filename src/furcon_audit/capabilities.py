"""Capability ports and provider registry. Provider SDKs stay in adapters."""
from dataclasses import dataclass
from typing import Any, Protocol

@dataclass(frozen=True)
class CapabilityDeclaration:
    provider_id: str
    provider_version: str
    capability_id: str
    operations: tuple[str, ...]
    input_schema_id: str | None = None
    output_schema_id: str | None = None
    auth_required: bool = False
    rate_limit_per_minute: int | None = None
    timeout_seconds: int = 30
    data_handling: str = "unspecified"
    availability: str = "unknown"
    limitations: tuple[str, ...] = ()

class CapabilityAdapter(Protocol):
    declaration: CapabilityDeclaration
    def execute(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]: ...

class CapabilityRegistry:
    """Resolve adapters by capability and operation, never by vendor similarity."""
    def __init__(self) -> None:
        self._adapters: list[CapabilityAdapter] = []

    def register(self, adapter: CapabilityAdapter) -> None:
        if adapter.declaration.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be positive")
        self._adapters.append(adapter)

    def candidates(self, capability_id: str, operation: str) -> list[CapabilityAdapter]:
        return [a for a in self._adapters
                if a.declaration.capability_id == capability_id
                and operation in a.declaration.operations
                and a.declaration.availability == "available"]

    def execute_first(self, capability_id: str, operation: str,
                      payload: dict[str, Any]) -> dict[str, Any]:
        candidates = self.candidates(capability_id, operation)
        if not candidates:
            raise LookupError(f"No available adapter for {capability_id}:{operation}")
        return candidates[0].execute(operation, payload)
