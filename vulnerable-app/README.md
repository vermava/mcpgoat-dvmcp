# Vulnerable MCP lab application

This directory contains an **intentionally insecure** local training application. It ships dummy data only: users, documents, and example API keys.

## Requirements

- Python **3.10+** (3.12 recommended; required by the `mcp` SDK)
- No cloud LLM keys; the bundled **simulated agent** drives scenarios deterministically

## Run locally

```bash
cd vulnerable-app
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=.
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080`.

## Optional MCP stdio server

From `vulnerable-app` with `PYTHONPATH=.`:

```bash
python -m mcp_server.server
```

Use this only with local MCP clients you trust. The server uses a fixed default persona (Alice).

## Mitigations

**Do not** look for secure fixes in this tree. Use the separate [`../solution-guide/`](../solution-guide/) directory.
