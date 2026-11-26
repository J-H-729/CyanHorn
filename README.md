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

