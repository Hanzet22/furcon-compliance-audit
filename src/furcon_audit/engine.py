"""Application engine boundary for the Phase 3 incremental rewrite."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .application.research import run_research_workflow
from .ports import PageRetriever, SearchGateway
from .research import ResearchTask
from .retrieval import retrieve_page


@dataclass(frozen=True)
class EngineConfig:
    """Validated runtime configuration for application workflows."""

    max_candidates: int = 5

    def __post_init__(self) -> None:
        if (
            isinstance(self.max_candidates, bool)
            or not isinstance(self.max_candidates, int)
            or not 1 <= self.max_candidates <= 20
        ):
            raise ValueError("max_candidates must be an integer between 1 and 20")


class AuditEngine:
    """Stable application entry point with explicitly injected dependencies.

    Phase 3.1 deliberately delegates to the characterized legacy workflow.
    Subsequent slices will move that orchestration into application services
    without changing the v1.0.0 interchange contract.
    """

    def __init__(
        self,
        search_gateway: SearchGateway,
        *,
        page_retriever: PageRetriever = retrieve_page,
        config: EngineConfig | None = None,
        retrieval_options: Mapping[str, Any] | None = None,
    ) -> None:
        if not callable(getattr(search_gateway, "execute_with_fallback", None)):
            raise TypeError("search_gateway must implement execute_with_fallback")
        if not callable(page_retriever):
            raise TypeError("page_retriever must be callable")

        self._search_gateway = search_gateway
        self._page_retriever = page_retriever
        self._config = config or EngineConfig()
        self._retrieval_options = MappingProxyType(dict(retrieval_options or {}))

    @property
    def config(self) -> EngineConfig:
        return self._config

    def run_research(
        self, task: ResearchTask, query: str
    ) -> dict[str, Any]:
        """Run search and controlled retrieval without auto-creating evidence."""
        return run_research_workflow(
            task,
            self._search_gateway,
            query,
            max_candidates=self._config.max_candidates,
            page_retriever=self._page_retriever,
            retrieval_options=dict(self._retrieval_options),
        )
