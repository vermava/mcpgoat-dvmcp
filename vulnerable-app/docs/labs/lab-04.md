# Lab 04 — Secret exposure

## Learning objective

Identify fake secrets returned through tool output and log lines that could leak in real deployments.

## OWASP mapping

- **MCP:** MCP01 Token Mismanagement & Secret Exposure
- **LLM:** LLM02 Sensitive Information Disclosure

## Vulnerable behavior

`get_server_env_snapshot` returns rows from the `secrets` table. Logging helpers may print reasons and payload sizes.

**Code:** `mcp_server/tools.py` (`get_server_env_snapshot`, `SENSITIVE_LOG_EXAMPLE`, `export_all_user_data` logging).

## Student exercise

1. Run the scenario and copy the JSON field that contains fake keys.
2. Search the codebase for `logger.` calls near tool handlers.

## Expected observation

Structured “secrets” appear in the tool output; log warnings may include export reasons.

## Defensive checklist

- Never return long-lived secrets to models; use short-lived scoped tokens.
- Redact structured logs; keep secrets out of model-visible tool results.
