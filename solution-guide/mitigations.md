# Mitigations and secure design notes

This guide explains **why** each vulnerability matters in MCP and agentic deployments, **what** to change at a high level, and **how** to detect issues. It pairs with the per-lab markdown in `vulnerable-app/docs/labs/`.

**Challenge levels:** Every lab supports **Basic (1)**, **Medium (2)**, and **Advanced (3)**. The vulnerable app selects different tool sequences (and, for some labs, different default user payloads) via `challenge_level` → `agent_client/scenarios.py`. When debriefing, use the **lab × level** table in [`instructor-notes.md`](instructor-notes.md) so your narrative matches the trace students actually ran.

---

## Lab 01 — Prompt injection vs tools

**Issue:** User text steers tool selection (`lab1_steps` substring checks).

**Why it matters:** MCP agents fuse system instructions, retrieved context, and user prompts. Any channel that treats user text as instructions collapses trust boundaries.

**Secure direction:**

- Hard-separate **policy** from **data**; never parse user text for control verbs.
- Add **human approval** or step-up auth for exports and bulk reads.
- Maintain an **allowlisted** set of tools per workflow with explicit escalation.

**Before / after (conceptual):**

- Before: `if "export" in user_message: call_export()`
- After: export only when `explicit_intent_token` signed by your policy service matches the session.

**Detection ideas:** alert on `export_all_user_data` correlated with high-entropy user prompts; monitor reasoning summaries if you log them internally (never log raw secrets).

**Discussion questions:**

1. Where does your product store the canonical “system prompt” versus user-visible chat?
2. Who can update tool manifests mid-session?

---

## Lab 02 — Tool poisoning (metadata)

**Issue:** `compliance_pre_check` description pressures ordering and hides export side effects.

**Why it matters:** MCP hosts advertise tools to models; poisoned metadata is similar to compromised package README instructions.

**Controls:**

- Code review for tool descriptions with **security + technical writing**.
- **Pin** server versions; verify hashes.
- **Deny unknown tools** by default in client configs.

**Detection:** new tool names appearing outside change windows; descriptions containing imperative “always/call first”.

**Discussion:** How does your org review third-party MCP connectors?

---

## Lab 03 — Excessive tool permissions

**Issue:** `admin_workspace_action` bundles read/write/delete/export.

**Controls:** split tools; scope tokens per action; add **MCP authorization** at the transport layer where possible.

**Detection:** single tool invoked with diverse `action` values in one session.

---

## Lab 04 — Secret exposure

**Issue:** Secrets returned to model context and verbose logs.

**Controls:** vault-backed short-lived tokens; **redact** logs; never echo environment dumps to models.

**Detection:** log regex for `sk-` patterns in application logs (tune heavily to avoid noise in real envs).

---

## Lab 05 — Insecure authorization

**Issue:** `get_document` lacks ownership checks.

**Controls:** object-level authz with tenant id; unit tests per tool for IDOR.

**Detection:** user A token retrieving objects owned by user B (synthetic tests).

---

## Lab 06 — Context poisoning

**Issue:** `build_context_from_docs` concatenates unsanitized bodies.

**Controls:** strip HTML comments for text channels; chunk with provenance; **drop** unknown sources.

**Detection:** retrieval returning chunks with high ratio of imperative verbs / policy keywords.

---

## Lab 07 — Unsafe tool execution (simulated)

**Issue:** User template flows into a command-like transcript.

**Controls:** structured arguments; **no shell**; sandbox with syscall filtering if you must run binaries.

**Detection:** templates containing shell metacharacters passed to tools with execution semantics.

---

## Lab 08 — Insecure output handling

**Issue:** Browser `innerHTML` with tool-derived HTML.

**Controls:** contextual encoding, CSP, React/Vue text nodes, DOMPurify if HTML is required.

**Detection:** DOM sinks in frontends that render model output; SAST rules for `innerHTML`.

---

## Lab 09 — Insufficient logging

**Issue:** no `append_audit_event` calls in normal paths.

**Controls:** structured audit pipeline; immutable store; alerts on export-after-read sequences.

**Detection:** missing audit events where policy requires them (continuous control testing).

---

## Lab 10 — Unsafe defaults

**Issue:** debug endpoints, permissive CORS, shadow tools.

**Controls:** secure profiles by default; explicit env to enable diagnostics; separate **maintenance** network plane.

**Detection:** exposure of `/debug` routes in production URLs; CORS `*` on APIs with credentials.

---

## Cross-cutting MCP04 supply chain

Discuss dependency pinning, SBOM, and CI verification of MCP packages. Tie back to Lab 02 metadata poisoning as a **human-readable** supply chain risk.
