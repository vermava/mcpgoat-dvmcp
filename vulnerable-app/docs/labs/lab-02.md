# Lab 02 — Tool poisoning (metadata)

## Learning objective

Explain how **tool names and descriptions** become part of the agent’s decision context and can manipulate tool choice.

## OWASP mapping

- **MCP:** MCP03 Tool Poisoning
- **LLM:** LLM04 Data and Model Poisoning

## Vulnerable behavior

The `compliance_pre_check` tool advertises itself as a priority first step for HR questions but routes to a data export in the dispatcher.

**Code:** `mcp_server/server.py` (`compliance_pre_check`), `mcp_server/dispatcher.py`.

## Student exercise

1. Run the Lab 2 scenario.
2. Open `mcp_server/server.py` and read the tool decorator metadata.
3. Describe in your own words how a maintainer could abuse or accidentally over-promise capability in descriptions.

## Expected observation

The agent selects `compliance_pre_check` and the export payload appears.

## Defensive checklist

- Review tool descriptions with the same rigor as user-facing product copy.
- Version and sign tool manifests; reject unknown tools in production agents.
