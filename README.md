# CyanHorn

Evidence-grounded analysis and comparison for small operating systems.

## Member B development branch

This branch contains the agent and report foundation. It defines the data contracts
used by the parser module and provides one OpenAI-compatible client for future
description and comparison workflows.

## Local setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
Copy-Item .env.example .env
```

Fill in `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL` in `.env`. Never commit
`.env` or raw source datasets.

## Member B foundation

`osinsight.retrieval.BM25Index` ranks parser-produced project records without a
vector database. `DescriptionAgent` and `ComparisonAgent` use the shared LLM
client and validate JSON responses against the report schemas. `EvidenceValidator`
checks that report references point to files and line ranges inside a project.

`AnalysisOrchestrator` connects retrieval, candidate selection, description, and
comparison into one callable workflow.

Run the offline tests from PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

