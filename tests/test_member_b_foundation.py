import tempfile
import unittest
from pathlib import Path

from osinsight.retrieval import BM25Index
from osinsight.schemas import EvidenceRef
from osinsight.verification import EvidenceValidator


class MemberBFoundationTests(unittest.TestCase):
    def test_bm25_ranks_matching_project(self):
        index = BM25Index([
            {"project_id": "memory", "modules": ["physical page allocator", "kalloc"]},
            {"project_id": "filesystem", "modules": ["inode", "directory"]},
        ])
        self.assertEqual(index.search("physical page kalloc", limit=1)[0].document_id, "memory")

    def test_evidence_validator_checks_line_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "kernel.c").write_text("int main()\n{}\n", encoding="utf-8")
            evidence = EvidenceRef(
                project_id="demo", file_path="kernel.c", start_line=1, end_line=2, claim="main"
            )
            result = EvidenceValidator(root).validate(evidence)
            self.assertTrue(result.valid)


if __name__ == "__main__":
    unittest.main()

