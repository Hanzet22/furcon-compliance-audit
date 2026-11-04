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
    """Resolve adapters by capability and operation, with capability-scoped fallback."""

    def __init__(self) -> None:
        self._adapters: list[CapabilityAdapter] = []

    def register(self, adapter: CapabilityAdapter) -> None:
        if adapter.declaration.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be positive")
        if any(a.declaration.provider_id == adapter.declaration.provider_id
               and a.declaration.capability_id == adapter.declaration.capability_id
               for a in self._adapters):
            raise ValueError("duplicate provider/capability registration")
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
        result = candidates[0].execute(operation, payload)
        if not isinstance(result, dict):
            raise TypeError("Capability adapter returned a non-object result.")
        return result

    def execute_with_fallback(self, capability_id: str, operation: str,
                              payload: dict[str, Any]) -> dict[str, Any]:
        """Try providers in registration order; malformed outputs are treated as provider failures."""
        from .providers import ProviderError

        failures = []
        last_error = None
        for adapter in self.candidates(capability_id, operation):
            try:
                result = adapter.execute(operation, payload)
                if not isinstance(result, dict):
                    raise ProviderError(adapter.declaration.provider_id,
                                        "Provider returned a non-object result.")
                normalized = dict(result)
                normalized["fallback_attempts"] = list(failures)
                return normalized
            except ProviderError as exc:
                last_error = exc
                failures.append({
                    "provider_id": exc.provider_id,
                    "status_code": exc.status_code,
                    "error": str(exc),
                    "retryable": exc.retryable,
                })
        if failures:
            details = "; ".join(item["provider_id"] for item in failures)
            reason = f"; last error: {last_error}" if last_error else ""
            raise ProviderError("registry", f"All candidate providers failed: {details}{reason}")
        raise LookupError(f"No available adapter for {capability_id}:{operation}")
