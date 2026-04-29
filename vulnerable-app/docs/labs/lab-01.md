# Lab 01 — Prompt injection against MCP tools

## Learning objective

Recognize how untrusted natural language can steer a simulated agent from a safe path (`list_documents`) to a high-impact tool (`export_all_user_data`).

## OWASP mapping

- **MCP:** MCP06 Intent Flow Subversion; MCP10 Context Injection & Over-Sharing
- **LLM:** LLM01 Prompt Injection

## Vulnerable behavior

The scenario agent treats substrings in the user message as operational guidance. When the message contains both `ignore previous` and `export`, it selects the export tool.

**Code:** `agent_client/scenarios.py` (`lab1_steps`), `mcp_server/tools.py` (`export_all_user_data`).

## Student exercise

1. Run the scenario with a benign message (for example: `What documents exist?`).
2. Run again with the default injection message on the lab page.
3. Compare tool names and outputs in the execution trace.

## Expected observation

Benign flow lists metadata only. Injection flow returns a full fake export payload.

## Hints (also available in Instructor mode in the UI)

- Read the simulated “reasoning” text before each tool call.
- Notice that policy is embedded in user content, not in a signed system channel.

## Defensive checklist (no solutions here)

- Treat user text as untrusted data, not instructions.
- Separate control plane from user content; require explicit human approval for exports.
