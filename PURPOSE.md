# Why we built MCP Goat

This document explains **why** this lab exists, **what gap** it fills, and **how** it helps people internalize MCP and LLM security concepts not just read about them.

---

## The problem this lab solves

**Agents that call tools are becoming normal.** Model Context Protocol (MCP) and similar patterns connect language models to filesystems, APIs, databases, and internal UIs. That stack is powerful—and easy to get wrong.

Today, many practitioners learn LLM risks from checklists and blog posts. Few have a **safe, repeatable place** to see *the same failure modes* in a full flow: user message → (simulated) agent reasoning → tool selection → arguments → tool output → UI. Text alone rarely shows **where trust breaks** between host, tools, and presentation layer.

**MCP Goat** is an educational, **intentionally vulnerable** application that runs **entirely on your machine** with **dummy data** and a **simulated agent** (no cloud LLM required). It exists so you can **observe** OWASP-aligned failures in context, without attacking real systems or handling real secrets.

---

## Why we built it this way

1. **Hands-on beats abstraction for this topic.** MCP and LLM risks are often about *sequences*: injection changing which tool runs, metadata misleading the model, outputs rendered unsafely, weak auth across personas. A small running app with traces makes those sequences visible.

2. **Separation of “break” and “fix.”** The vulnerable application holds **attacks and scenarios only**. Mitigations, secure patterns, and worksheet answers live under `solution-guide/`. That mirrors how teams work: first understand the blast radius and evidence, then design controls— and it keeps classrooms honest about when debrief material is appropriate.

3. **Alignment with shared language.** Each lab maps to **OWASP MCP Top 10** and **OWASP Top 10 for LLM Applications (2025)** so learners can connect what they saw to industry frameworks, threat models, and peer conversations.

4. **Safety by design.** Localhost-only guidance, simulated “dangerous” behaviors, and no production dependencies reduce the chance that practice becomes accidental harm.

---

## How it helps people understand concepts

| Challenge when reading docs alone | What the lab does |
|-------------------------------------|---------------------|
| “I don’t know what an MCP-style failure *looks like* in practice.” | You run scenarios in the web UI and read **traces**: reasoning summary, tool name, arguments, output. |
| “I can’t tell host vs agent vs tool responsibility.” | The architecture and UI encourage you to **follow data and trust** across those boundaries lab by lab. |
| “OWASP items feel like a list, not a story.” | Each lab is a **small narrative** (e.g., prompt injection against tools, tool poisoning, excessive permissions) tied to explicit mappings in `owasp-mapping.md`. |
| “I need something to submit or discuss in class.” | **Worksheets** (`vulnerable-app/docs/worksheets/`) turn observation into short written reasoning before you open the solution guide. |

After working through the material, learners can typically **name where a control failed**, **map it to OWASP categories**, and **propose detect vs prevent ideas**—with the solution guide available for structured debrief and code-level patterns.

---

## Who benefits

- **Students and developers** building or integrating MCP-style hosts and tools.
- **AppSec and AI security practitioners** who need a consistent demo and exercise set for workshops or onboarding.
- **Instructors** who want a local, low-friction lab with a clear student path (`LABGUIDE.md`) and separate instructor assets (`solution-guide/`).

---

## Summary

We built MCP Goat because **MCP and agentic LLM security are easier to teach and learn when you can see the full chain of decisions and data** in a controlled environment. Its purpose is not to ship a product—it is to **make abstract risks concrete**, **tie them to OWASP guidance**, and **prepare people to design and review real systems** with clearer intuition about where things go wrong.

For how to run the lab and what to open first, see [`README.md`](README.md) and [`LABGUIDE.md`](LABGUIDE.md).
