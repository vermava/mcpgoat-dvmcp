# OWASP mapping — MCP Security Lab / MCP Got / Dam Vulnerable MCP App

This project maps each hands-on lab to the **OWASP MCP Top 10 (2025)** and the **OWASP Top 10 for LLM Applications (2025)**. All behavior is simulated with dummy data.

Sources (external):

- [OWASP GenAI — Top 10 for LLM Applications](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)

## Hands-on labs (1–10)

| Lab | Topic | OWASP MCP Top 10 (2025) | OWASP LLM Top 10 (2025) | Primary code / docs pointers |
|-----|--------|-------------------------|--------------------------|------------------------------|
| 1 | Prompt injection steering tool choice | MCP06 Intent Flow Subversion; MCP10 Context Injection & Over-Sharing | LLM01 Prompt Injection | `agent_client/scenarios.py` (`lab1_steps`), `mcp_server/tools.py` (`export_all_user_data`) |
| 2 | Tool poisoning via misleading metadata | MCP03 Tool Poisoning | LLM04 Data and Model Poisoning | `mcp_server/server.py` (`compliance_pre_check` tool description) |
| 3 | Excessive tool permissions / combined surface | MCP02 Privilege Escalation via Scope Creep | LLM06 Excessive Agency | `mcp_server/tools.py` (`admin_workspace_action`) |
| 4 | Secret exposure in logs and tool output | MCP01 Token Mismanagement & Secret Exposure | LLM02 Sensitive Information Disclosure | `mcp_server/tools.py` (`SENSITIVE_LOG_EXAMPLE`, `get_server_env_snapshot`) |
| 5 | Insecure authorization on document reads | MCP07 Insufficient Authentication & Authorization | LLM02 Sensitive Information Disclosure; LLM01 (indirect) | `mcp_server/tools.py` (`get_document`) |
| 6 | Context poisoning via retrieved text | MCP10 Context Injection & Over-Sharing | LLM04 Data and Model Poisoning | `db.py` (seed document 3 body), `mcp_server/tools.py` (`build_context_from_docs`) |
| 7 | Unsafe tool execution (simulated) | MCP05 Command Injection & Execution | LLM06 Excessive Agency | `mcp_server/tools.py` (`run_report_generator`) |
| 8 | Insecure output handling in the web UI | MCP10 Context Injection & Over-Sharing (data path) | LLM05 Improper Output Handling | `main.py` (response field), `web_ui/templates/lab.html` (`unsafe_html_fragment` + `innerHTML`) |
| 9 | Insufficient logging and telemetry | MCP08 Lack of Audit and Telemetry | (supporting control — pair with LLM06/LLM02 in discussion) | `mcp_server/tools.py` (`append_audit_event` unused in happy path), `agent_client/runner.py` (`audit_log_count`) |
| 10 | Unsafe defaults (debug, CORS, shadow tools) | MCP09 Shadow MCP Servers (narrative); MCP01/MCP02 as secondary | LLM10 Unbounded Consumption (optional angle: missing limits) | `config.py`, `main.py` (CORS, debug endpoint, exception handler), `mcp_server/server.py` (`shadow_mcp_ping`) |

## MCP04 — Software supply chain (reading topic)

**MCP04:2025 Software Supply Chain Attacks & Dependency Tampering** is not isolated as an eleventh interactive lab. Instead, instructors should connect Labs **2** and **3** to supply-chain themes: poisoned tool metadata resembles tampered package READMEs, and over-broad tools resemble compromised build plugins with excess capability.

Discussion prompts:

- How would you verify MCP server packages and lockfiles in CI?
- What signals would indicate an unexpected new tool appearing in a release?

## LLM Top 10 coverage notes

| LLM item | Where learners see it |
|----------|------------------------|
| LLM01 Prompt Injection | Labs 1, 5, 6 |
| LLM02 Sensitive Information Disclosure | Labs 4, 5 |
| LLM03 Supply Chain | Reading: MCP04 section above |
| LLM04 Data and Model Poisoning | Labs 2, 6 |
| LLM05 Improper Output Handling | Lab 8 |
| LLM06 Excessive Agency | Labs 3, 7 |
| LLM07 System Prompt Leakage | Not demoed in-tool (use discussion: compare to Lab 1 steering) |
| LLM08 Vector and Embedding Weaknesses | Not demoed (out of scope for this small SQLite RAG stub) |
| LLM09 Misinformation | Optional discussion only |
| LLM10 Unbounded Consumption | Lab 10 (`max_tool_calls_per_request = 0` narrative) |
