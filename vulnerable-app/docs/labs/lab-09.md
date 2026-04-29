# Lab 09 — Insufficient logging and monitoring

## Learning objective

Correlate **missing audit rows** with high-risk tool activity that should be observable in production.

## OWASP mapping

- **MCP:** MCP08 Lack of Audit and Telemetry
- **LLM:** (supporting control; pair with LLM02/LLM06 in discussion)

## Vulnerable behavior

Normal tool paths do not call `append_audit_event`. The UI shows `audit_log_count_before` and `audit_log_count_after` staying flat.

**Code:** `mcp_server/tools.py` (`append_audit_event`, `audit_log_count`), `agent_client/runner.py`.

## Student exercise

1. Run Lab 9 and inspect the `meta` object in the JSON response.
2. List three fields you would require in a production MCP audit event.

## Expected observation

Counts remain unchanged despite sensitive reads.

## Defensive checklist

- Emit structured audit events for tool name, args hash, actor, tenant, outcome, and latency.
- Ship dashboards for anomalous tool sequences (for example export after retrieval).
