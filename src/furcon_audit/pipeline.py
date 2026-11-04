"""Backward-compatible entry point for the pre-engine research workflow.

New application code should use AuditEngine. This function remains available
for callers using the original v2 import path during the Phase 3 migration.
"""
from __future__ import annotations

from typing import Any, Callable

from .application.research import run_research_workflow
from .research import ResearchTask
from .retrieval import retrieve_page


def run_research_task(
    task: ResearchTask,
    registry,
    query: str,
    *,
    max_candidates: int = 5,
    page_retriever: Callable = retrieve_page,
    retrieval_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compatibility wrapper preserving the original call signature."""
    return run_research_workflow(
        task,
        registry,
        query,
        max_candidates=max_candidates,
        page_retriever=page_retriever,
        retrieval_options=retrieval_options,
    )
