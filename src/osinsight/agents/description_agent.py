from __future__ import annotations

import json
from typing import Any

from .llm_client import LLMClient
from ..schemas import DescriptionReport


def _json_payload(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(cleaned)


class DescriptionAgent:
    """Generates a source-grounded description from parser output."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, project: dict[str, Any], evidence: list[dict[str, Any]]) -> DescriptionReport:
        prompt = (
            "Create a JSON-only operating-system project description. "
            "Use only the supplied metadata and evidence. Every technical claim "
            "must reference an evidence item. Mark uncertain claims as needs_review.\n\n"
            f"Project:\n{json.dumps(project, ensure_ascii=False, indent=2)}\n\n"
            f"Evidence:\n{json.dumps(evidence, ensure_ascii=False, indent=2)}\n\n"
            "Return fields project_id, overview, architecture, modules, key_functions, "
            "development_history, technical_features, evidence."
        )
        response = self.llm.ask(prompt, system="You are a careful operating-system source analyst.")
        return DescriptionReport.model_validate(_json_payload(response))

