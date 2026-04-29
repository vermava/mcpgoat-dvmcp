# Solution guide — instructors and defenders

This file is the **master index** for everyone debriefing or hardening against the issues shown in [`../vulnerable-app/`](../vulnerable-app/). Students should start from [`../LABGUIDE.md`](../LABGUIDE.md) and the app’s own docs until you release this material.

## Principles

1. **Separation of duties:** attacks and vulnerable patterns live under `vulnerable-app/`; mitigations, answers, and secure examples live **only** here.
2. **No real targets:** all fixes and detection ideas are framed for **local, dummy-data** teaching; adapt responsibly for production telemetry and privacy rules.

## How to run a debrief

1. Confirm learners finished (or attempted) labs **1–10** and worksheets. Where time allows, confirm they ran **more than one challenge level** on key labs (the traces differ per `challenge_level`; see the matrix in [`instructor-notes.md`](instructor-notes.md)).
2. Walk [`mitigations.md`](mitigations.md) **lab by lab** — each section has issue, why it matters, controls, detection, and discussion prompts.
3. Optionally demo hardened snippets from [`secure-code-examples/`](secure-code-examples/) and review [`testing-checklists/mcp-lab-hardening.md`](testing-checklists/mcp-lab-hardening.md).
4. Use [`worksheet-answers/answer-key.md`](worksheet-answers/answer-key.md) to grade or normalize discussion (distribute answer keys according to your policy).
5. Tie **MCP04 supply chain** themes to Labs **02** and **03** using the cross-cutting section at the end of `mitigations.md` and [`../owasp-mapping.md`](../owasp-mapping.md).

## Challenge levels (Basic / Medium / Advanced)

The web UI sends `challenge_level` **1–3** on every run. **`vulnerable-app/agent_client/scenarios.py`** is the source of truth for which tools fire at each level. A consolidated **lab × level** description (for debrief and grading) lives in [`instructor-notes.md`](instructor-notes.md) under *Challenge level selector* and *Implemented scenario shapes*.

## Lab → solution assets (quick map)

| Lab | Primary write-up | Worksheet key (spoilers) | Code / pattern examples |
|-----|------------------|--------------------------|-------------------------|
| 01 Prompt injection vs tools | [`mitigations.md`](mitigations.md) § Lab 01 | [`worksheet-answers/answer-key.md`](worksheet-answers/answer-key.md) § Lab 01 | Policy vs data separation; human approval for exports |
| 02 Tool poisoning | `mitigations.md` § Lab 02 | Answer key § Lab 02 | Manifest review, pinning, deny unknown tools |
| 03 Excessive permissions | `mitigations.md` § Lab 03 | Answer key § Lab 03 | Split tools; scoped capability tokens |
| 04 Secret exposure | `mitigations.md` § Lab 04 | Answer key § Lab 04 | Redaction, vault, no env dumps to model context |
| 05 Insecure authZ | `mitigations.md` § Lab 05 | Answer key § Lab 05 | [`secure-code-examples/get_document_secure.py`](secure-code-examples/get_document_secure.py) |
| 06 Context poisoning | `mitigations.md` § Lab 06 | Answer key § Lab 06 | Chunking, provenance, strip risky text patterns |
| 07 Unsafe execution (simulated) | `mitigations.md` § Lab 07 | Answer key § Lab 07 | Structured args; no shell; sandboxing narrative |
| 08 Insecure output handling | `mitigations.md` § Lab 08 | Answer key § Lab 08 | Encoding, CSP, avoid `innerHTML` for tool output |
| 09 Insufficient logging | `mitigations.md` § Lab 09 | Answer key § Lab 09 | [`secure-code-examples/tool_audit_helper.py`](secure-code-examples/tool_audit_helper.py); audit design |
| 10 Unsafe defaults | `mitigations.md` § Lab 10 | Answer key § Lab 10 | Secure-by-default config; no shadow tools in prod |

## Detection and verification

| Resource | Use |
|----------|-----|
| [`detection-rules/mcp-lab-pseudo-sigma.md`](detection-rules/mcp-lab-pseudo-sigma.md) | Starter ideas for tool-abuse style alerts (pseudo–Sigma); tune before production |
| [`testing-checklists/mcp-lab-hardening.md`](testing-checklists/mcp-lab-hardening.md) | Verification after you fork and fix the vulnerable app |

## Facilitation and assessment

| Resource | Use |
|----------|-----|
| [`instructor-notes.md`](instructor-notes.md) | Safety script, ~90 min agenda, tips, common questions, **per-lab scenario matrix (levels 1–3)** |
| [`README.md`](README.md) | Short directory map of this folder |

## Secure code examples (reference implementations)

See [`secure-code-examples/README.md`](secure-code-examples/README.md) for how the snippets relate to labs and how to run them in isolation (they are **not** wired into the vulnerable app by design).

## Discussion prompts (course-level)

After per-lab discussion in `mitigations.md`, consider:

- Where does your organization draw the line between **user data** and **control plane** for agent routing?
- Who may publish or update **tool descriptions** and server manifests, and how are changes reviewed?
- What **minimum audit fields** must every high-risk tool call record for incident response?

---

For project setup and student flow, see the root [`README.md`](../README.md) and [`../LABGUIDE.md`](../LABGUIDE.md).
