# Lab 03 — Excessive tool permissions

## Learning objective

Map a single “admin” tool that bundles read and export actions to **least privilege** violations and agent overreach.

## OWASP mapping

- **MCP:** MCP02 Privilege Escalation via Scope Creep
- **LLM:** LLM06 Excessive Agency

## Vulnerable behavior

`admin_workspace_action` implements multiple unrelated capabilities behind one MCP tool.

**Code:** `mcp_server/tools.py` (`admin_workspace_action`).

## Student exercise

1. Run the scenario and list the two actions taken.
2. Argue whether a read-only assistant should ever call the export branch automatically.

## Expected observation

The trace shows read followed by organization-wide export using the same tool surface.

## Defensive checklist

- Split tools by risk class; require separate approval for exports.
- Rate-limit and scope exports to explicit tenant identifiers.
