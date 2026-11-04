"""Optional REST provider adapters with bounded retries and normalized provenance."""
from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from .capabilities import CapabilityDeclaration

LOGGER = logging.getLogger(__name__)


class ProviderError(RuntimeError):
    def __init__(self, provider_id: str, message: str, *, status_code: int | None = None,
                 retryable: bool = False) -> None:
        super().__init__(message)
        self.provider_id = provider_id
        self.status_code = status_code
        self.retryable = retryable


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes


def _stdlib_transport(url: str, headers: dict[str, str], body: bytes,
                      timeout: int) -> HttpResponse:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return HttpResponse(response.status, dict(response.headers.items()), response.read())
    except urllib.error.HTTPError as exc:
        return HttpResponse(exc.code, dict(exc.headers.items()) if exc.headers else {}, exc.read())


class JsonSearchAdapter:
    provider_id = "abstract"
    base_url = ""
    key_env = ""
    auth_header = "Authorization"

    def __init__(self, *, api_key: str | None = None, timeout: int = 20,
                 max_retries: int = 2,
                 transport: Callable[[str, dict[str, str], bytes, int], HttpResponse] = _stdlib_transport,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        if timeout < 1 or max_retries < 0:
            raise ValueError("timeout must be positive and max_retries non-negative")
        self.api_key = api_key or os.getenv(self.key_env)
        self.timeout = timeout
        self.max_retries = max_retries
        self.transport = transport
        self.sleep = sleep
        self.declaration = CapabilityDeclaration(
            provider_id=self.provider_id, provider_version="REST-v1",
            capability_id="search.web", operations=("search",),
            auth_required=True, timeout_seconds=timeout,
            data_handling="External provider receives the submitted search query.",
            availability="available" if self.api_key else "unavailable",
            limitations=("Requires provider API key.", "External service terms and retention apply.")
        )

    def _request_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        query = payload.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("payload.query must be a non-empty string")
        limit = payload.get("limit", 5)
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
            raise ValueError("payload.limit must be an integer between 1 and 20")
        return {"query": query.strip(), "limit": limit}

    def _headers(self) -> dict[str, str]:
        raise NotImplementedError

    def _body(self, request: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def _results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError

    def execute(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        if operation != "search":
            raise ValueError(f"Unsupported operation: {operation}")
        if not self.api_key:
            raise ProviderError(self.provider_id, f"Missing {self.key_env}; adapter is unavailable.")
        request_payload = self._request_payload(payload)
        headers = self._headers()
        body = json.dumps(self._body(request_payload)).encode("utf-8")
        last_error: ProviderError | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.transport(self.base_url, headers, body, self.timeout)
                if response.status == 429 or response.status in {408, 500, 502, 503, 504}:
                    raise ProviderError(self.provider_id, f"Transient HTTP {response.status}",
                                        status_code=response.status, retryable=True)
                if response.status < 200 or response.status >= 300:
                    raise ProviderError(self.provider_id, f"HTTP {response.status}",
                                        status_code=response.status)
                try:
                    parsed = json.loads(response.body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ProviderError(self.provider_id, "Provider returned invalid JSON.") from exc
                results = self._results(parsed)
                return {
                    "provider_id": self.provider_id,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "request_id": response.headers.get("x-request-id") or response.headers.get("X-Request-Id"),
                    "query": request_payload["query"],
                    "results": results,
                    "result_count": len(results),
                }
            except ProviderError as exc:
                last_error = exc
                if not exc.retryable or attempt >= self.max_retries:
                    raise
                self.sleep(min(2 ** attempt, 8))
        assert last_error is not None
        raise last_error


class ExaAdapter(JsonSearchAdapter):
    provider_id = "exa"
    base_url = "https://api.exa.ai/search"
    key_env = "EXA_API_KEY"

    def _headers(self) -> dict[str, str]:
        return {"x-api-key": self.api_key or "", "Content-Type": "application/json"}

    def _body(self, request: dict[str, Any]) -> dict[str, Any]:
        return {"query": request["query"], "numResults": request["limit"],
                "type": "auto", "contents": {"highlights": True}}

    def _results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        rows = response.get("results", [])
        if not isinstance(rows, list):
            raise ProviderError(self.provider_id, "Unexpected Exa response: results is not a list.")
        return [{"url": row.get("url"), "title": row.get("title"),
                 "published_date": row.get("publishedDate"),
                 "highlights": row.get("highlights", []),
                 "source_provider": self.provider_id}
                for row in rows if isinstance(row, dict)]


class FirecrawlAdapter(JsonSearchAdapter):
    provider_id = "firecrawl"
    base_url = "https://api.firecrawl.dev/v2/search"
    key_env = "FIRECRAWL_API_KEY"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _body(self, request: dict[str, Any]) -> dict[str, Any]:
        return {"query": request["query"], "limit": request["limit"],
                "sources": ["web"], "scrapeOptions": {"formats": ["markdown"]}}

    def _results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        rows = response.get("data", [])
        if isinstance(rows, dict):
            rows = rows.get("web", [])
        if not isinstance(rows, list):
            raise ProviderError(self.provider_id, "Unexpected Firecrawl response: data is not a list.")
        return [{"url": row.get("url"), "title": row.get("title"),
                 "description": row.get("description"),
                 "markdown": row.get("markdown"),
                 "source_provider": self.provider_id}
                for row in rows if isinstance(row, dict)]
