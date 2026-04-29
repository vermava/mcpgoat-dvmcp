# Lab 05 — Insecure authentication and authorization

## Learning objective

Demonstrate an IDOR-style read: **Bob** fetches **Alice’s** document because ownership is not enforced.

## OWASP mapping

- **MCP:** MCP07 Insufficient Authentication & Authorization
- **LLM:** LLM02 Sensitive Information Disclosure; LLM01 (indirect via agent)

## Vulnerable behavior

`get_document` does not compare `owner_user_id` to `ctx.user_id`.

**Code:** `mcp_server/tools.py` (`get_document`), `mcp_server/context.py`.

## Student exercise

1. Switch persona to **Bob** in the UI and run the Lab 5 scenario.
2. Note which `document_id` the simulated agent requests.

## Expected observation

Bob receives Alice’s document body in the tool output.

## Defensive checklist

- Enforce object-level authorization on every tool argument that names a resource.
- Log denied attempts with stable identifiers for detection.
