from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..schemas import EvidenceRef


@dataclass(frozen=True)
class ValidationResult:
    evidence: EvidenceRef
    valid: bool
    reason: str


class EvidenceValidator:
    """Checks that report references point to real files and valid line ranges."""

    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root).resolve()

    def validate(self, evidence: EvidenceRef) -> ValidationResult:
        path = (self.project_root / evidence.file_path).resolve()
        try:
            path.relative_to(self.project_root)
        except ValueError:
            return ValidationResult(evidence, False, "file path escapes project root")
        if not path.is_file():
            return ValidationResult(evidence, False, "file does not exist")
        with path.open("r", encoding="utf-8", errors="replace") as source_file:
            line_count = sum(1 for _ in source_file)
        if evidence.start_line > evidence.end_line:
            return ValidationResult(evidence, False, "start_line is after end_line")
        if evidence.end_line > line_count:
            return ValidationResult(evidence, False, "end_line exceeds file length")
        return ValidationResult(evidence, True, "file and line range verified")

