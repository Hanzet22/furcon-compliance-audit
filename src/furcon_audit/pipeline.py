"""Orchestrate search discovery and public-page retrieval without auto-creating evidence."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from .providers import ProviderError
from .research import ResearchTask
from .retrieval import retrieve_page


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _attempt(task_id: str, provider_id: str, capability_id: str, operation: str,
             status: str, started_at: str, *, error_code: str | None = None,
             error_summary: str | None = None, query_summary: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "attempt_id": "attempt_" + uuid.uuid4().hex[:20],
        "research_task_id": task_id,
        "provider_id": provider_id,
        "capability_id": capability_id,
        "operation": operation,
        "status": status,
        "started_at": started_at,
        "ended_at": _now(),
        "query_summary": query_summary,
        "retry_number": 0,
        "error_code": error_code,
        "error_summary": error_summary,
    }


def run_research_task(
    task: ResearchTask,
    registry,
    query: str,
    *,
    max_candidates: int = 5,
    page_retriever: Callable = retrieve_page,
    retrieval_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Search, record provider attempts, retrieve distinct candidate URLs, and retain gaps.

    This function intentionally stops before evidence and claim creation. A person or
    downstream workflow must select and validate excerpts explicitly.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be non-empty")
    if not 1 <= max_candidates <= 20:
        raise ValueError("max_candidates must be between 1 and 20")
    if task.status not in {"queued", "partial", "blocked", "failed"}:
        raise ValueError("research task is not in a runnable state")
    task.transition("running")
    attempts: list[dict[str, Any]] = []
    sources, retrievals, captures, unresolved = [], [], [], []
    started = _now()
    try:
        search_result = registry.execute_with_fallback(
            "search.web", "search", {"query": query.strip(), "limit": max_candidates}
        )
    except (LookupError, ProviderError) as exc:
        attempts.append(_attempt(task.research_task_id, "registry", "search.web", "search",
                                 "failed", started, error_code=type(exc).__name__,
                                 error_summary=str(exc), query_summary=query.strip()))
        task.transition("failed", "Search providers were unavailable or failed.")
        return {"research_task": task, "research_attempts": attempts, "sources": [],
                "retrievals": [], "captures": [], "unresolved": [str(exc)]}

    for failure in search_result.get("fallback_attempts", []):
        attempts.append(_attempt(
            task.research_task_id, failure.get("provider_id", "unknown"),
            "search.web", "search", "failed", started,
            error_code=str(failure.get("status_code") or "provider_error"),
            error_summary=failure.get("error"), query_summary=query.strip()
        ))
    provider_id = search_result.get("provider_id", "unknown")
    results = search_result.get("results", [])
    search_status = "succeeded" if results else "no_results"
    attempts.append(_attempt(task.research_task_id, provider_id, "search.web", "search",
                             search_status, started, query_summary=query.strip()))
    if not results:
        task.transition("partial", "Search completed but returned no candidate sources.")
        return {"research_task": task, "research_attempts": attempts, "sources": [],
                "retrievals": [], "captures": [], "unresolved": ["No search candidates returned."]}

    seen_urls = set()
    for candidate in results[:max_candidates]:
        url = candidate.get("url") if isinstance(candidate, dict) else None
        if not isinstance(url, str) or not url.strip():
            unresolved.append("Search candidate omitted a usable URL.")
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        attempt_started = _now()
        retrieval_attempt_id = "attempt_" + uuid.uuid4().hex[:20]
        try:
            capture = page_retriever(url, attempt_id=retrieval_attempt_id,
                                     **(retrieval_options or {}))
        except (ValueError, TypeError, RetrievalError) as exc:
            attempts.append(_attempt(task.research_task_id, "stdlib-http", "retrieve.page",
                                     "retrieve", "failed", attempt_started,
                                     error_code=type(exc).__name__, error_summary=str(exc)))
            unresolved.append(f"Retrieval could not be initialized for candidate: {type(exc).__name__}")
            continue
        outcome = capture.get("retrieval", {}).get("outcome", "failed")
        attempt_status = {"success": "succeeded", "blocked": "blocked",
                          "partial": "failed", "failed": "failed",
                          "not_modified": "succeeded"}.get(outcome, "failed")
        error = capture.get("error", {})
        attempts.append(_attempt(
            task.research_task_id, "stdlib-http", "retrieve.page", "retrieve",
            attempt_status, attempt_started, error_code=error.get("code"),
            error_summary=error.get("message")
        ))
        # Keep the attempt reference stable and consistent with the retrieval record.
        capture["retrieval"]["attempt_id"] = attempts[-1]["attempt_id"]
        if capture.get("source"):
            source_id = capture["source"].get("source_id")
            if source_id and all(item.get("source_id") != source_id for item in sources):
                sources.append(capture["source"])
        if capture.get("retrieval"):
            retrievals.append(capture["retrieval"])
        captures.append(capture)
        if outcome != "success":
            unresolved.append(error.get("message") or f"Retrieval outcome: {outcome}")

    successes = sum(1 for item in retrievals if item.get("outcome") == "success")
    failures = len(retrievals) - successes
    if successes and failures == 0 and not unresolved:
        task.transition("completed")
    elif successes:
        task.transition("partial", "Some candidates could not be retrieved or verified.")
    elif retrievals and all(item.get("outcome") == "blocked" for item in retrievals):
        task.transition("blocked", "All candidate retrievals were blocked by access or safety policy.")
    else:
        task.transition("partial", "No candidate retrieval succeeded; source absence is not established.")
    return {
        "research_task": task,
        "research_attempts": attempts,
        "sources": sources,
        "retrievals": retrievals,
        "captures": captures,
        "unresolved": unresolved,
        "evidence": [],
        "claims": [],
    }
