# Instructor guide — what to tell students (plain language)

This document is for **you**, the instructor. It explains **MCP Goat** in everyday terms so you can introduce the lab confidently, even if students are new to MCP or AI security.

For timing, facilitation tips, safety reminders, and a **per-lab / per-level scenario matrix** (matches `agent_client/scenarios.py`), see [`solution-guide/instructor-notes.md`](solution-guide/instructor-notes.md). For the student path through the app (no solutions), point them to [`LABGUIDE.md`](LABGUIDE.md).

---

## One sentence you can use on day one

**“This is a practice website that *pretends* to be unsafe on purpose. It shows how ‘AI assistants that use tools’ can go wrong—so you learn to design and test safer systems. Everything is fake and runs only on your computer.”**

---

## What this application actually is

**MCP Goat** is a **local training lab**, not a product and not something to deploy on the internet.

- **“MCP”** stands for **Model Context Protocol**. In simple terms: a **standard way** for an assistant (or “agent”) to talk to **tools**—things like “read a file,” “call an API,” “run a report,” and so on.
- In real life, companies are wiring LLMs and agents to **databases, tickets, email, and internal APIs**. MCP is one pattern for how that wiring works.
- This lab **shrinks that idea** into a small Python app with a **web page** and **fake** users, documents, and tokens. Students see **which tool ran**, **what arguments were sent**, and **what came back**—like a flight recorder for agent behavior.

**Important:** There is **no cloud LLM required**. A **simulated agent** follows scripted steps so every student sees **predictable** results. That keeps class fair and reproducible.

---

## Why we teach this (the “so what?”)

Students already hear about “prompt hacking.” This lab adds what matters for **real systems**:

1. **Tools are code paths.** If the agent picks the wrong tool or passes bad data, impact can be **worse than a wrong chat answer**—because tools can read data, change state, or trigger other systems.
2. **Trust boundaries are fuzzy.** The **user**, the **host app**, the **agent**, and **each tool** all touch the same story. Security fails when someone assumes “the AI will behave.”
3. **OWASP lists give a shared vocabulary.** Each lab maps to items from **OWASP MCP Top 10** and **OWASP Top 10 for LLM Applications (2025)** so learners can talk to security and engineering teams using the same words. The mapping table is in [`owasp-mapping.md`](owasp-mapping.md) at the repository root.

---

## How the pieces fit together (use a whiteboard if you like)

Tell students to picture a **line**:

**User message → (host / agent decides) → tool runs → result goes back → maybe shown in the UI**

- **Host:** The application that owns the session (here, the FastAPI app and lab page).
- **Agent:** The part that chooses *which* tool to call and *with what arguments* (here, **scripted** for teaching).
- **Tools:** Python functions exposed like MCP tools (export data, read a document, run a “report,” etc.).
- **UI:** Where outputs appear—including places where **unsafe handling** of output can bite.

Stress: **bugs can live in any hop on that line**, not only “in the model.”

---

## What students do in class

1. Run the app on **localhost** (Python venv or Docker—see root `README.md`).
2. Open the **web UI**, pick a **lab**, set **Challenge level** to Basic (1), Medium (2), or Advanced (3), and run the bundled **scenario** (Labs **1, 7, 8, and 10** load different **suggested starter text** per level; other labs still change the tool trace when the level changes).
3. Read the **trace**: reasoning summary, tool name, arguments, output.
4. Use the **lab markdown** and **worksheets** under `vulnerable-app/docs/` (see `LABGUIDE.md`).

**Instructor mode** in the UI gives **extra hints** (including level-tagged tips from `main.py`), not full solutions—use it when the room is stuck.

**Bob persona:** For **authorization** scenarios (especially Lab 5), toggling **Bob** switches the fake user context so students can see **cross-user** mistakes with harmless data.

---

## Ground rules (say this clearly)

- **Intentionally vulnerable:** The code is *meant* to show bad patterns. **Do not** copy patterns into real apps.
- **Localhost only:** Do not expose the container to the internet or a shared untrusted network.
- **Dummy data only:** No real passwords, API keys, or customer data in the lab.
- **No “try this on Discord / Slack / work”:** The point is **defensive** understanding, not attacking real services.

---

## The ten labs — what each is *about* in simple words

Use this as a **cheat sheet** when you introduce each lab. Official titles and exercises live in `vulnerable-app/docs/labs/`.

| Lab | What to tell students (plain language) |
|-----|----------------------------------------|
| **1** | **Words can steer the robot.** If the user message tricks the system, the agent may call a **dangerous tool** (for example, “export everything”) when it should have done something safe. That’s **prompt injection** hitting **tool choice**. |
| **2** | **Names and descriptions matter.** If a tool’s **description** lies or manipulates (“always pick me first”), the agent can be misled—like a **fake label on a medicine bottle**. That’s **tool poisoning** via metadata. |
| **3** | **Too much power in one switch.** One tool might be allowed to do **admin-level** things when a normal user should only **read**. That’s **excessive permission** / **too much agency** for one action. |
| **4** | **Secrets shouldn’t appear in chat or logs.** Fake keys or tokens might leak through **logs**, **errors**, or **tool output**. Students learn to spot **where sensitive data leaves** the safe place it belongs. |
| **5** | **Who is allowed to see what?** Without proper checks, **Alice** might read **Bob’s** document. That’s broken **authorization** (IDOR-style thinking) in an agent workflow. |
| **6** | **Bad content in the library poisons the answer.** If a **document** or retrieved snippet hides malicious instructions, those lines can end up in the **context** the agent “reads.” That’s **context poisoning** / data poisoning in a RAG-like path. |
| **7** | **Don’t let untrusted input drive powerful actions.** A “run report” style tool might **build a command** from user text. Here execution is **simulated**, but the lesson is real: **command injection** class of problems. |
| **8** | **What the tool returns is not automatically safe.** If the web page **drops raw HTML/JS** into the page, you get **cross-site scripting**-style issues. Browser protections are **not** the same as **server-side safe output** handling. |
| **9** | **If nobody wrote it down, nobody can investigate.** Missing **audit logs** for tool calls means abuse is **invisible**. Students think about what to log and what to alert on. |
| **10** | **Defaults should be boring and safe.** Debug flags, wide **CORS**, extra endpoints, or “hidden” tools mirror **unsafe defaults** in real deployments—great for attackers, bad for production. |

**Optional narrative link:** **Supply chain** (tampered packages, unexpected tools in a release) connects to **Labs 2 and 3**—see the MCP04 discussion in `owasp-mapping.md`. **Lab 2 Advanced** drives that home with a simulated metadata collision that calls export directly.

---

## What “success” looks like after the course

Students do **not** need to memorize CVEs. They *should* be able to:

- **Follow** a request from UI → agent → tool → UI.
- **Name** the risk family using OWASP MCP / LLM language.
- Propose at least one **detect** idea and one **prevent** idea per lab (logging, allowlists, least privilege, output encoding, human approval, etc.).

Full defender material lives only under **`solution-guide/`** (`mitigations.md`, `SOLUTION_GUIDE.md`, secure examples, detection ideas, worksheet answers). Keep students out of that folder until **debrief** or assigned self-study with answers. For **what changes at each challenge level**, use the scenario table in `solution-guide/instructor-notes.md`.

---

## If students ask common questions

- **“Why isn’t ChatGPT running?”** So everyone gets the **same** steps and outputs; a real model might “behave” differently. You *could* extend the lab later with a local model behind a flag—advanced optional work.
- **“Is this real MCP?”** The lab uses the same **ideas** as MCP (tools, descriptions, host). The web UI calls the same Python handlers as the optional **stdio MCP server** path—good bridge to real MCP clients later.
- **“Will I learn to hack?”** You learn how **defenders** and **builders** **find** and **fix** weaknesses. Offensive skill without ethics and scope is out of scope; **safe, local, dummy data** only.

---

## Where to point students vs yourself

| Audience | Document / folder |
|----------|-------------------|
| Students (path, UI, worksheets) | [`LABGUIDE.md`](LABGUIDE.md), `vulnerable-app/docs/labs/`, `vulnerable-app/docs/worksheets/` |
| You (timing, read-aloud safety, scenario matrix) | [`solution-guide/instructor-notes.md`](solution-guide/instructor-notes.md) |
| You (this narrative) | **This file** |
| Debrief / answers | [`solution-guide/SOLUTION_GUIDE.md`](solution-guide/SOLUTION_GUIDE.md), [`solution-guide/mitigations.md`](solution-guide/mitigations.md), [`solution-guide/worksheet-answers/`](solution-guide/worksheet-answers/) |

You’ve got this: **one vulnerable toy app**, **ten clear stories**, **OWASP as a map**, **solutions separate**. That’s the whole arc in simple words.
