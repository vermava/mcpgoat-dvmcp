# Instructor notes

## Safety (read aloud)

- This software is **intentionally vulnerable** and must run **localhost only**.
- No real credentials, cloud accounts, or customer data belong in this lab.
- Do not encourage students to port payloads to real systems.

## Suggested timing (90 minutes)

| Segment | Minutes | Activity |
|---------|---------|----------|
| Intro MCP + agents | 10 | Whiteboard data flow: user → host → tools → UI |
| Labs 1–3 | 25 | Prompt injection, metadata poisoning, excessive agency |
| Labs 4–6 | 25 | Secrets, authZ, context poisoning |
| Labs 7–8 | 15 | Simulated execution + output sinks |
| Labs 9–10 | 10 | Logging, defaults |
| Debrief | 5 | Map to OWASP tables; preview solution-guide |

## Threat model (technical baseline)

Use this once at intro; it anchors all labs.

- **Trust boundaries**: untrusted user text, retrieved corpus, tool metadata, and model output each cross a boundary into privileged execution (Python handlers, filesystem, browser DOM).
- **Control plane vs data plane**: MCP tool names, schemas, and descriptions are **control-plane** inputs; document bodies and logs are **data-plane**; conflation is the root of most lab failures.
- **Deterministic stack**: no live LLM; attacks are replayable. Students should trace **call graph** from `agent_client/scenarios.py` → `mcp_server/tools.py` / `server.py` → `web_ui` where applicable.

## Challenge level selector (student UI)

- Each lab page has **Basic (1)**, **Medium (2)**, and **Advanced (3)**. The choice is sent as `challenge_level` on every **Run** and selects the canned steps in `vulnerable-app/agent_client/scenarios.py`.
- **Suggested starter text** in the scenario textarea updates when you change level for **Labs 1, 7, 8, and 10** (`DEFAULT_MESSAGES_BY_LEVEL` in `vulnerable-app/main.py`). For **Labs 2–6 and 9**, changing the level still changes the tool trace; students should switch the dropdown and **Run** again (and edit the user message for Lab 1 so it matches the trigger phrases for that level—see matrix below).

## Implemented scenario shapes (challenge level 1–3)

Authoritative implementation: `vulnerable-app/agent_client/scenarios.py`. Use this table in debrief when comparing traces.

| Lab | Level 1 (Basic) | Level 2 (Medium) | Level 3 (Advanced) |
|-----|-----------------|------------------|---------------------|
| **1** | If user text matches basic injection (`ignore previous` + `export`): one step → `export_all_user_data`. Else → `list_documents`. | If `disregard` or `override policy` plus export-style wording → one step → `export_all_user_data`. | If `inventory`/`catalog` plus `then export`/`follow with export` → `list_documents` then `export_all_user_data` (cross-step intent subversion). |
| **2** | `compliance_pre_check` (metadata-steered). | `list_documents` then `compliance_pre_check`. | Single step → `export_all_user_data` with `hr_bundle_alias_metadata_collision` (supply-chain style alias narrative). |
| **3** | `admin_workspace_action` read doc 1 → same tool `export`. | Read doc 1 → `rename` doc 2 → `export`. | Single call → `admin_workspace_action` `export` only. |
| **4** | `get_server_env_snapshot`. | `list_documents` then `get_server_env_snapshot`. | `get_document` (id 1) then `get_server_env_snapshot`. |
| **5** | `get_document` id 1 (no ownership check). | `get_document` id 2 (cross-owner / horizontal IDOR). | Two steps: `get_document` ids 1 then 2 (enumeration). |
| **6** | `build_context_from_docs` query `handbook`. | Same tool; query pulls broader policy/SYSTEM-markup framing. | `build_context_from_docs` then `export_all_user_data` (`reason: context_blob_handbook_compliance`)—retrieval steers a high-impact tool. |
| **7** | Always one step → `run_report_generator` with the template from the UI. **Level** only changes the **default example template** in the UI (SQL-ish vs pipes vs multiline). | Same shape. | Same shape. |
| **8** | Always one step → `format_user_snippet`. **Level** changes default snippet and appears in reasoning text; same insecure UI sink. | Same shape. | Same shape. |
| **9** | `get_document` id 2 (audit path unused). | `get_document` id 2 then `list_documents` (still no audit). | `admin_workspace_action` read doc 1 → `export` (high impact, still no `append_audit_event` on vulnerable path). |
| **10** | `shadow_mcp_ping` with UI target. | `shadow_mcp_ping` then `list_documents`. | `shadow_mcp_ping` with metadata-URL-shaped default target (SSRF class discussion; still simulated). |

## Vulnerability depth levels (per lab)

For each theme, calibrate discussion and assessment to **Basic**, **Medium**, or **Advanced**. Basic is recognition and single-control fixes; Medium ties attack mechanics to code paths and composite failures; Advanced covers bypass thinking, policy, and production-grade patterns.

### Lab 1 — Prompt injection / intent flow subversion (MCP06, MCP10; LLM01)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Identify when natural-language instructions override intended tool policy. | User text co-located with system or agent instructions; first-token / delimiter confusion; `export_all_user_data`-style exfiltration triggered by steered prompts. |
| **Medium** | Map steering to concrete tool-selection or argument-binding logic. | Separation of **instruction channel** vs **data channel**; allowlists for tools; structured outputs that do not re-parse free text as commands. |
| **Advanced** | Relate the in-app **two-step** trace (`list_documents` → `export_all_user_data` on inventory/audit phrasing) to cross-turn policy and intent subversion. | Extend to indirect injection via retrieved or third-party content; privilege boundaries per tool session; human-in-the-loop for exports; monitoring for anomalous tool graphs. |

### Lab 2 — Tool poisoning via metadata (MCP03; LLM04)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Recognize that tool **name + description + schema** are attacker-influenced in supply-chain or compromised-server scenarios. | `compliance_pre_check`-style misleading descriptions; trust assumptions in UI and agent prompts. |
| **Medium** | Compare metadata integrity to package signing and SBOM verification. | Pinning server versions; diffing tool manifests in CI; least-capability tool registration. |
| **Advanced** | Model split-view attacks; relate **Level 3** to manifest/alias collision leading straight to `export_all_user_data`. | Attestation of running server; network egress policy; capability-based OS sandboxing around tool workers. |

### Lab 3 — Excessive agency / scope creep (MCP02; LLM06)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | See that a single high-privilege tool widens blast radius. | `admin_workspace_action` combined with weak prompt boundaries. |
| **Medium** | Design **scoped tokens** and per-request capability sets. | Separate admin MCP servers; OAuth-style scopes per tool; deny-by-default tool lists per agent role. |
| **Advanced** | Reason about confused-deputy; **Level 3** shows export with **no** prior read (single high-impact call). | Binding consent to resource IDs; temporal limits on elevated sessions; audit of tool call DAGs for privilege jumps. |

### Lab 4 — Token mismanagement / secret exposure (MCP01; LLM02)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Spot secrets in logs, traces, and tool return payloads. | `SENSITIVE_LOG_EXAMPLE`, `get_server_env_snapshot`; redaction at sink. |
| **Medium** | Classify PII vs configuration vs runtime secrets; define log taxonomy. | Structured logging with field-level scrubbers; sampling policies; never echoing env to models or clients. |
| **Advanced** | **Level 3** chains `get_document` with env snapshot—correlating content with config leaks; plus secret rotation and aggregation blast radius. | KMS-backed references; log shipping encryption; threat of log-based training or RAG re-ingestion of secrets. |

### Lab 5 — Insufficient authentication / authorization (MCP07; LLM02)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Understand IDOR-style reads when the agent passes user-controlled IDs. | `get_document` without server-side subject binding. |
| **Medium** | Implement **authorize-then-fetch** with session-bound principals. | `get_document_secure` pattern; pytest for horizontal escalation; defense in depth vs prompt-only rules. |
| **Advanced** | **Level 3** back-to-back IDOR reads; tie to ABAC and document-level ACLs in RAG pipelines. | Embedding stores that leak neighbors; policy engines outside the LLM; cryptographic object capabilities. |

### Lab 6 — Context injection / RAG poisoning (MCP10; LLM04)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | See poisoned corpus lines change agent behavior without a traditional exploit. | Seeded document in `db.py`; `build_context_from_docs` concatenation. |
| **Medium** | Treat retrieved chunks as **untrusted data** with provenance and scoring. | Source attribution; max chunk size; instruction markers that cannot be closed by user text; retrieval filters by clearance. |
| **Advanced** | **Level 3** retrieval then `export_all_user_data`; connect to data poisoning and lack of sandbox between RAG output and tools. | Corpus hygiene pipelines; anomaly detection on retrieval sets; isolation of “system” blocks from “user” blocks in model APIs. |

### Lab 7 — Command injection / unsafe execution (MCP05; LLM06)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Recognize when tool arguments become shell or process invocation. | `run_report_generator` (simulated); never pass model output to `shell=True`. |
| **Medium** | Prefer **fixed command templates** and parameterized APIs; separate read-only jobs. | Allowlisted binaries; argv arrays not strings; seccomp / containers per invocation. |
| **Advanced** | Same single-tool graph as other levels; use **UI default templates** by level to discuss depth of injection payloads and job-runner hardening. | CPU/memory quotas; job identity; proof-of-work or rate limits for expensive tools. |

### Lab 8 — Improper output handling / DOM XSS (MCP10 data path; LLM05)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Distinguish `textContent` from `innerHTML` when rendering model output. | `unsafe_html_fragment` in `lab.html`; attacker-controlled HTML reaching the sink. |
| **Medium** | Contextual encoding, CSP, and Trusted Types as **defense in depth**. | Nonces for script-src; sanitization allowlists; treating MCP JSON fields as data, not markup. |
| **Advanced** | **Level 3** default uses nested `iframe`/`srcdoc`; discuss mutation XSS, parser differentials, SSRF from rendered URLs. | Strict MIME types; URL schemes blocklist; postMessage origin checks if embedding widgets. |

### Lab 9 — Lack of audit and telemetry (MCP08)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Notice missing or unused audit hooks on sensitive paths. | `append_audit_event` unused in happy path; `audit_log_count` in runner. |
| **Medium** | Define events: who, which tool, arguments hash, outcome, correlation ID. | Tamper-evident logs; centralized SIEM mapping for MCP sessions. |
| **Advanced** | **Level 3** admin read + export with no audit events; forensics under adversarial log injection and volume attacks. | Signed append-only stores; retention vs privacy (GDPR); redaction pipeline consistency with Lab 4. |

### Lab 10 — Unsafe defaults / shadow surfaces (MCP09, MCP01/MCP02; LLM10)

| Level | Learning objectives | Technical focus |
|-------|---------------------|-----------------|
| **Basic** | Enumerate debug flags, permissive CORS, and hidden tools. | `config.py`, `main.py`, `shadow_mcp_ping`; `max_tool_calls_per_request = 0` as unbounded narrative. |
| **Medium** | Hardening checklist per environment (dev/stage/prod). | Explicit bind addresses; tool registration visibility; rate limits and quotas. |
| **Advanced** | **Level 3** metadata-URL-shaped `shadow_mcp_ping` target; supply-chain of configuration (IaC drift, feature flags, break-glass). | Kill switches for MCP; canary deployments; chaos testing for misconfiguration alerts. |

## Facilitation tips

- Have students run **at least two levels** (for example Basic + Advanced) on Labs **1, 2, 6, and 9** so multi-step traces are not missed.
- Keep students in the **vulnerable-app** UI until debrief.
- Use **Instructor mode** hints sparingly; reward source navigation (`mcp_server/tools.py`).
- For Lab 8, remind students that browser mitigations are **not** a substitute for encoding.
- When a cohort skews senior, skip Basic table rows aloud and assign Medium as pre-read; reserve Advanced for table discussions or post-lab reading.

## Assessment ideas

- **Basic**: Short reflection — pick two labs; one **detect** control and one **prevent** control, tied to a specific file/function.
- **Medium**: Sequence diagram of a single lab’s exploit path with trust boundaries labeled.
- **Advanced**: Implement `get_document_secure` in a fork with pytest IDOR cases **and** document one residual threat (e.g., prompt-layer bypass) your tests do not cover.

## Common questions

- **Why no real LLM?** Determinism and classroom fairness; you may bolt on a local model later behind explicit env flags.
- **Is FastMCP required?** The lab uses `mcp.server.fastmcp.FastMCP` from the official SDK; the web path calls the same Python handlers directly.
