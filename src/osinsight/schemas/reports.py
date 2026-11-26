from typing import Any, Literal

from pydantic import BaseModel, Field


class EvidenceRef(BaseModel):
    """A source location supporting one generated claim."""

    project_id: str
    file_path: str
    symbol: str | None = None
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    claim: str
    evidence_status: Literal["verified", "needs_review", "unsupported"] = "needs_review"


class DescriptionReport(BaseModel):
    project_id: str
    overview: str
    architecture: str
    modules: list[dict[str, Any]] = Field(default_factory=list)
    key_functions: list[dict[str, Any]] = Field(default_factory=list)
    development_history: list[dict[str, Any]] = Field(default_factory=list)
    technical_features: list[str] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(default_factory=list)


class ComparisonReport(BaseModel):
    new_project_id: str
    historical_project_id: str
    architecture_comparison: dict[str, Any] = Field(default_factory=dict)
    module_comparison: list[dict[str, Any]] = Field(default_factory=list)
    function_comparison: list[dict[str, Any]] = Field(default_factory=list)
    code_similarity: dict[str, Any] = Field(default_factory=dict)
    history_comparison: dict[str, Any] = Field(default_factory=dict)
    differences: list[dict[str, Any]] = Field(default_factory=list)
    potential_novelty: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(default_factory=list)

