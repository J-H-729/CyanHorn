from __future__ import annotations

from typing import Any

from ..retrieval import BM25Index, SearchResult
from .comparison_agent import ComparisonAgent
from .description_agent import DescriptionAgent
from .llm_client import LLMClient


class AnalysisOrchestrator:
    """Coordinates retrieval and the two report-producing workflows."""

    def __init__(self, projects: list[dict[str, Any]], llm: LLMClient):
        self.projects = projects
        self.index = BM25Index(projects)
        self.description_agent = DescriptionAgent(llm)
        self.comparison_agent = ComparisonAgent(llm)

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        return self.index.search(query, limit=limit)

    def describe(self, project: dict[str, Any], evidence: list[dict[str, Any]]):
        return self.description_agent.run(project, evidence)

    def compare(
        self,
        new_project: dict[str, Any],
        evidence_by_project: dict[str, list[dict[str, Any]]],
        *,
        historical_project_id: str | None = None,
        query: str | None = None,
    ):
        if historical_project_id:
            matches = [p for p in self.projects if p.get("project_id") == historical_project_id]
            if not matches:
                raise KeyError(f"Unknown historical project: {historical_project_id}")
            historical_project = matches[0]
        else:
            if not query:
                raise ValueError("query is required when historical_project_id is omitted")
            candidates = self.search(query, limit=1)
            if not candidates:
                raise LookupError("No historical project matched the query")
            historical_project = candidates[0].document
        evidence = list(evidence_by_project.get(str(new_project.get("project_id")), []))
        evidence.extend(evidence_by_project.get(str(historical_project.get("project_id")), []))
        return self.comparison_agent.run(new_project, historical_project, evidence)

