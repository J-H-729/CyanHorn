import json
import unittest

from osinsight.agents import AnalysisOrchestrator


class FakeLLM:
    def ask(self, prompt, *, system=None, temperature=0.0):
        if "comparison" in prompt.lower():
            return json.dumps({
                "new_project_id": "new",
                "historical_project_id": "old",
                "differences": [{"dimension": "module", "status": "different"}],
            })
        return json.dumps({
            "project_id": "old",
            "overview": "A small kernel",
            "architecture": "RISC-V",
            "technical_features": ["page allocator"],
        })


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AnalysisOrchestrator(
            [
                {"project_id": "old", "project_name": "Old Kernel", "modules": ["memory", "process"]},
                {"project_id": "fs", "project_name": "File Kernel", "modules": ["filesystem"]},
            ],
            FakeLLM(),
        )

    def test_search_and_description(self):
        self.assertEqual(self.orchestrator.search("memory allocator", limit=1)[0].document_id, "old")
        report = self.orchestrator.describe(self.orchestrator.projects[0], [])
        self.assertEqual(report.project_id, "old")

    def test_compare_selects_candidate(self):
        report = self.orchestrator.compare(
            {"project_id": "new", "project_name": "New Kernel"},
            {},
            query="memory process",
        )
        self.assertEqual(report.historical_project_id, "old")


if __name__ == "__main__":
    unittest.main()

