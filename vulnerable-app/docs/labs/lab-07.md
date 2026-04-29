# Lab 07 — Unsafe tool execution (simulated)

## Learning objective

See how user-controlled strings flow into a **simulated command transcript** without invoking a real shell.

## OWASP mapping

- **MCP:** MCP05 Command Injection & Execution
- **LLM:** LLM06 Excessive Agency

## Vulnerable behavior

`run_report_generator` concatenates the user template into a transcript string. This lab uses **fake output only**.

**Code:** `mcp_server/tools.py` (`run_report_generator`).

## Student exercise

1. Supply a template containing SQL-like text or metacharacters.
2. Explain the difference between this simulation and a real command execution bug.

## Expected observation

The transcript echoes attacker-controlled text, illustrating taint flow.

## Defensive checklist

- Never pass user text to shells; use structured arguments and allowlisted operations.
- Keep high-risk tools off the default tool allowlist.
