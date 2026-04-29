# Lab 10 — Unsafe default configuration

## Learning objective

Review default flags that are dangerous outside a classroom: debug introspection, permissive CORS, shadow tools, and verbose errors.

## OWASP mapping

- **MCP:** MCP09 Shadow MCP Servers (narrative: extra tool surface); MCP01/MCP02 secondary
- **LLM:** LLM10 Unbounded Consumption (narrative: missing limits)

## Vulnerable behavior

`config.py` enables debug flags by default. `/api/debug/settings` exposes internal paths. CORS allows all origins when configured. `shadow_mcp_ping` models an unapproved connector.

**Code:** `config.py`, `main.py` (middleware and handlers), `mcp_server/server.py`.

## Student exercise

1. Open `/api/debug/settings` while logged in locally.
2. Run the shadow ping scenario and read the JSON output.
3. Trigger a handled server error path (optional) and observe verbose JSON when `expose_stack_traces` is true.

## Expected observation

Internal configuration and shadow tool activity are easy to reach.

## Defensive checklist

- Secure-by-default profiles; explicit env vars to enable diagnostics.
- Disable shadow or experimental tools in production manifests.
