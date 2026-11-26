from __future__ import annotations

import json
from typing import Any

from .description_agent import _json_payload
from .llm_client import LLMClient
from ..schemas import ComparisonReport


class ComparisonAgent:
    """Compares two structured projects while retaining source evidence."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(
        self,
        new_project: dict[str, Any],
        historical_project: dict[str, Any],
        evidence: list[dict[str, Any]],
    ) -> ComparisonReport:
        prompt = (
            "Create a JSON-only comparison of two operating-system projects. "
            "Compare architecture, modules, functions, code similarity, and history. "
            "Do not claim originality or copying. Put uncertain findings in "
            "potential_novelty with a needs_review status and cite evidence.\n\n"
            f"New project:\n{json.dumps(new_project, ensure_ascii=False, indent=2)}\n\n"
            f"Historical project:\n{json.dumps(historical_project, ensure_ascii=False, indent=2)}\n\n"
            f"Evidence:\n{json.dumps(evidence, ensure_ascii=False, indent=2)}\n\n"
            "Return fields new_project_id, historical_project_id, architecture_comparison, "
            "module_comparison, function_comparison, code_similarity, history_comparison, "
            "differences, potential_novelty, evidence."
        )
        response = self.llm.ask(prompt, system="You are a conservative code comparison analyst.")
        return ComparisonReport.model_validate(_json_payload(response))

