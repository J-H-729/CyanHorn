from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    """Stable project metadata exchanged with the parser module."""

    project_id: str = Field(min_length=1)
    year: int | None = None
    project_name: str
    team: str | None = None
    university: str | None = None
    repository_url: str | None = None
    commit_sha: str
    language: list[str] = Field(default_factory=list)
    base_kernel: str | None = None
    architecture: str | None = None
    license: str | None = None

