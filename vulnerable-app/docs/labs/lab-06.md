# Lab 06 — Context poisoning

## Learning objective

Show how concatenating untrusted document bodies into a single “context blob” can inject hidden instructions.

## OWASP mapping

- **MCP:** MCP10 Context Injection & Over-Sharing
- **LLM:** LLM04 Data and Model Poisoning

## Vulnerable behavior

`build_context_from_docs` joins all document bodies. Seed document 3 contains an HTML comment with adversarial instructions.

**Code:** `db.py` (seed data for document id 3), `mcp_server/tools.py` (`build_context_from_docs`).

## Student exercise

1. Run the scenario and scroll the `context_blob` field in the output.
2. Locate the hidden comment in `db.py` and describe how a RAG indexer might preserve it.

## Expected observation

The blob includes benign handbook text plus hidden directive text.

## Defensive checklist

- Sanitize and chunk retrieved text; strip HTML comments for plain-text channels.
- Maintain provenance metadata per chunk and drop unknown sources.
