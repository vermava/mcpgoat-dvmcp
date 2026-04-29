# Solution guide (instructor / defender)

This directory contains **mitigations, secure patterns, detection ideas, and answer keys** for the intentionally vulnerable application in [`../vulnerable-app/`](../vulnerable-app/).

Students should work from the vulnerable UI and markdown under `vulnerable-app/docs/` only.

**Start here for a full index:** [`SOLUTION_GUIDE.md`](SOLUTION_GUIDE.md) (lab → mitigations, examples, keys, debrief flow).

## Contents

| Path | Purpose |
|------|---------|
| [mitigations.md](mitigations.md) | Vulnerability explanations, controls, before/after discussion |
| [secure-code-examples/](secure-code-examples/) | Hardened Python snippets illustrating fixes |
| [detection-rules/](detection-rules/) | Pseudo–Sigma style ideas for tool abuse |
| [testing-checklists/](testing-checklists/) | Verification steps for a secured fork |
| [INSTRUCTOR_GUIDE.md](../INSTRUCTOR_GUIDE.md) | Plain-language “what to tell students” overview of the lab |
| [instructor-notes.md](instructor-notes.md) | Timing, facilitation, safety reminders, **scenario matrix (levels 1–3)** |
| [worksheet-answers/](worksheet-answers/) | Keys for student worksheets |

## Usage

1. Run the lab locally or via Docker (see root `README.md`).
2. Let students explore each lab page and complete worksheets without this folder.
3. Debrief using `mitigations.md` and discussion questions at the end of each lab section.
