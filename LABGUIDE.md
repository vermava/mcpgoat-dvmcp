# Lab guide — OWASP MCP / LLM security lab (students)

This guide is the **student-facing** path through the intentionally vulnerable local lab. It contains **no answers or mitigations**; those live only under [`solution-guide/`](solution-guide/).

## Who this is for

Students, developers, AppSec engineers, and anyone learning how **Model Context Protocol (MCP)** style tool hosts, agents, and UIs fail in ways that map to **OWASP MCP Top 10** and **OWASP Top 10 for LLM Applications (2025)**.

## Safety (required reading)

- Run the app on **localhost only**; do not expose it to untrusted networks.
- All data is **dummy data** (users, tokens, documents). Do not put real secrets in the lab.
- “Dangerous” behavior (execution, HTML) is **simulated or sandboxed** for teaching.
- Do **not** reuse lab payloads against real systems.

## What you will use

| Resource | Location | Purpose |
|----------|----------|---------|
| Web UI | `http://127.0.0.1:8080` after starting the app | Pick labs, run scenarios, read traces |
| Per-lab write-ups | [`vulnerable-app/docs/labs/`](vulnerable-app/docs/labs/) | Objectives, OWASP mapping, exercises, hints (no solutions) |
| Worksheets | [`vulnerable-app/docs/worksheets/`](vulnerable-app/docs/worksheets/) | `ws-01-student.md` … `ws-10-student.md` |
| OWASP mapping table | [`owasp-mapping.md`](owasp-mapping.md) (repo root) | Which MCP/LLM items each lab illustrates |

**Do not** look under `solution-guide/` until your instructor allows debrief or self-study with answers.

## Environment setup

### Option A — Python virtualenv (recommended for development)

```bash
cd vulnerable-app
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=.
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080`.

### Option B — Docker

From the repository root:

```bash
docker compose up --build
```

Then open `http://127.0.0.1:8080`.

### Optional MCP stdio server

From `vulnerable-app` with `PYTHONPATH=.`:

```bash
python -m mcp_server.server
```

Use only with **trusted local** MCP clients. Default persona is **Alice**.

## Using the web UI

1. Read the **warning banner** on each page.
2. Choose a **lab** from the list.
3. Set **Challenge level** to **Basic (1)**, **Medium (2)**, or **Advanced (3)**. Each level runs a **different canned scenario** (`challenge_level` in the API → `agent_client/scenarios.py`). **Labs 1, 7, 8, and 10** also swap the **suggested text** in the main textarea when you change level (injection phrasing, template, HTML snippet, or shadow target). For other labs, change the level and click **Run** again to see a different tool sequence even if the placeholder text looks the same.
4. Run the bundled **scenario** (and edit the user message, template, snippet, or target when your instructor asks—**Lab 1** needs wording that matches the level you picked; see the lab doc).
5. Inspect the trace: **reasoning summary**, **tool name**, **arguments**, **tool output** — this is how you connect UI behavior to MCP-style flows.
6. Turn on **Instructor mode** for **extra hints** only (hints are grouped by level; never full step-by-step solutions in the app).
7. For authorization labs (especially **Lab 05**), enable the **Bob** persona when the UI offers it so you exercise cross-user access patterns with dummy users.

**Try all three levels** on at least a few labs so you see single-step vs multi-step traces (for example, Lab 1 Advanced does a benign list then an export).

## Suggested lab order and artifacts

Complete labs in order **1 → 10** the first time through. For each lab: read the lab markdown, run the scenario at **each challenge level you have time for** (or at minimum Basic + Advanced), then complete the matching worksheet.

| Lab | Topic | Lab doc | Student worksheet |
|-----|--------|---------|-------------------|
| 01 | Prompt injection against MCP tools | [`vulnerable-app/docs/labs/lab-01.md`](vulnerable-app/docs/labs/lab-01.md) | [`vulnerable-app/docs/worksheets/ws-01-student.md`](vulnerable-app/docs/worksheets/ws-01-student.md) |
| 02 | Tool poisoning (metadata) | [`vulnerable-app/docs/labs/lab-02.md`](vulnerable-app/docs/labs/lab-02.md) | [`ws-02-student.md`](vulnerable-app/docs/worksheets/ws-02-student.md) |
| 03 | Excessive tool permissions | [`lab-03.md`](vulnerable-app/docs/labs/lab-03.md) | [`ws-03-student.md`](vulnerable-app/docs/worksheets/ws-03-student.md) |
| 04 | Secret exposure | [`lab-04.md`](vulnerable-app/docs/labs/lab-04.md) | [`ws-04-student.md`](vulnerable-app/docs/worksheets/ws-04-student.md) |
| 05 | Insecure authentication and authorization | [`lab-05.md`](vulnerable-app/docs/labs/lab-05.md) | [`ws-05-student.md`](vulnerable-app/docs/worksheets/ws-05-student.md) |
| 06 | Context poisoning | [`lab-06.md`](vulnerable-app/docs/labs/lab-06.md) | [`ws-06-student.md`](vulnerable-app/docs/worksheets/ws-06-student.md) |
| 07 | Unsafe tool execution (simulated) | [`lab-07.md`](vulnerable-app/docs/labs/lab-07.md) | [`ws-07-student.md`](vulnerable-app/docs/worksheets/ws-07-student.md) |
| 08 | Insecure output handling | [`lab-08.md`](vulnerable-app/docs/labs/lab-08.md) | [`ws-08-student.md`](vulnerable-app/docs/worksheets/ws-08-student.md) |
| 09 | Insufficient logging and monitoring | [`lab-09.md`](vulnerable-app/docs/labs/lab-09.md) | [`ws-09-student.md`](vulnerable-app/docs/worksheets/ws-09-student.md) |
| 10 | Unsafe default configuration | [`lab-10.md`](vulnerable-app/docs/labs/lab-10.md) | [`ws-10-student.md`](vulnerable-app/docs/worksheets/ws-10-student.md) |

## Time planning

- **Self-paced:** allow roughly **2–4 hours** for all ten labs, worksheets, and optional source reading in `vulnerable-app/mcp_server/` and `vulnerable-app/agent_client/`.
- **Instructor-led (~90 minutes):** see suggested segment timing in [`solution-guide/instructor-notes.md`](solution-guide/instructor-notes.md) (instructor resource).

## Learning outcomes (check yourself)

After the labs you should be able to:

- Map failures you observed to **OWASP MCP Top 10** and **OWASP LLM Top 10 (2025)** using [`owasp-mapping.md`](owasp-mapping.md).
- Explain how **tool choice**, **arguments**, and **outputs** move between user, host, tools, and UI — and where trust breaks.
- Name at least one **detect** and one **prevent** control per lab (formal mitigations are in the separate solution guide after debrief).

## External references

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)

## After the lab

When your course allows it, open [`solution-guide/SOLUTION_GUIDE.md`](solution-guide/SOLUTION_GUIDE.md) for a consolidated index of mitigations, code patterns, detection ideas, and worksheet keys.
