---
name: pre-loop
description: Run BEFORE a loop (/goal, /loop, or a Routine) to design its full operating context. An interactive wizard that reads your repo to infer architecture/conventions/constraints, confirms the gaps via the question UI, solidifies the architecture foundations, builds and guards a real verifier (anti-gaming + pre-flight run), sets up safe/reversible execution and loop-health signals, writes loop-brief.md, and hands back a ready-to-run /goal command. Use when the user wants to set up a loop, run a goal, automate a recurring task, says "loop this" / "keep going until…", or asks how to loop something.
---

# Pre-Loop: design the loop's full context before you run it

A loop is only as good as the contract it executes against — and a contract is more
than a goal. It's the **architecture the work must fit**, a **verifier that can't be
gamed**, a **safe place to run**, and the **signals that tell you it's progressing**.
Gather all of that up front and the loop produces work that fits your system. Skip
it and the loop confidently drifts into something you'll have to rip out.

## How to run this — an interactive wizard
1. **Read the repo first.** Infer from `CLAUDE.md`/`AGENTS.md`, README,
   ARCHITECTURE/CONTRIBUTING/`docs/`, package manifests + scripts, lint/format/
   test/CI config, and the code nearest the work: stack, conventions, build/test
   commands, and where the work fits.
2. **Then run as a short wizard.** Present what you inferred, then confirm and fill
   the gaps. **Use the `AskUserQuestion` tool** so the discrete choices render in
   Claude Code's question UI — e.g. *fit: loop it / fix first / don't loop*,
   *scope boundary*, *run on a branch or in place?*, *what needs human approval?*,
   *which verifier?* Keep genuinely open-ended items (describe the architecture)
   conversational. Ask only for what you couldn't infer — don't interrogate.
3. **Scale depth to the task.** A one-file fix is a light pass; a new feature or
   subsystem needs the full architecture review + a plan.

## Step 1 — Architecture foundations (do FIRST)
Establish what the work must FIT. Infer; confirm the gaps:
- **Where it fits** — module / layer / boundary, and what it must not reach across.
- **Patterns to follow** — existing files to mirror (refs) + conventions (naming, structure, error handling, logging, dependency direction).
- **Stack & deps** — approved language/framework/libraries, and what NOT to introduce.
- **Interfaces & contracts** — APIs, schemas, types, events to honor without breaking callers.
- **Data / source of truth** — where the authoritative data/state lives.
- **Non-negotiables** — security, performance, accessibility, compliance, backward compatibility.
- **Avoid** — known anti-patterns / past mistakes here.
- **Ownership & escalation** — who owns this code, who reviews, who's the human escalation point.
- **Downstream / integration surface** — what depends on this that the loop must not break (callers, CI, other services).

> If the repo has no durable context file (`CLAUDE.md` / `AGENTS.md`) or it's thin,
> **offer to write or strengthen it** — it's the foundation every future loop reads.

## Step 2 — The contract
- **Intent** — the goal, and *why* it matters (so the loop makes good tradeoffs, not just compiling ones).
- **Scope** — in scope, and explicitly **out of scope / non-goals** (what stops drift and over-building).
- **Plan** — for non-trivial work, decompose into ordered steps / milestones with dependencies.
- **State & evidence** — what survives between turns (working tree, a decision log), and what's handed off as proof.
- **Guardrails** — permissions (tools/paths the loop may touch), the approval gate for any destructive or external side effect, and what to do on ambiguity (ask vs. assume). (Budget + stop conditions are set in Step 4.)

## Step 3 — The verifier: prove it, scaffold it, guard it
This is the load-bearing step. A loop with a weak or gameable verifier is the #1 failure mode.
- **Verifier stack** — every check that proves "good," *independent of the agent's claim*: tests, type-check, lint/format, build, schema/contract checks, and any human/rubric review gate. "Tests pass" is rarely the whole bar.
- **Scaffold it if missing** — if there's no check for the area, **write the acceptance test now** (a failing test that encodes "done"), or the schema/rubric. Turn "can't loop this" into "now you can." Never loop blind.
- **Anti-goal catalog (prevent gaming)** — name how the agent could "pass" *without doing the work*, and add a guard for each: e.g. *tests are read-only · the diff must touch the implementation, not the tests · coverage can't drop · no new `# type: ignore` / `eslint-disable` · don't mock the thing under test · don't hard-code the expected output.* A gamed verifier is **worse** than no verifier — it hands you false confidence.
- **Pre-flight** — actually **run the verifier once** before kicking off the loop. Confirm it executes, fails for the *right* reason, and that deps / env / fixtures / credentials are present. Half of "the loop did nothing useful" is "the verifier never ran."

## Step 4 — Safe, reversible, observable execution
- **Isolate** — run the loop on a dedicated **git branch or worktree** so a bad run is one `git checkout` / branch-delete away from gone. Define the **rollback**.
- **Budget & stop** — set a grounded **budget estimate** (turns / tokens / $ for a task this size) and the **stop / pause / abort / escalate** conditions: stop on green; pause on missing context; abort on budget, risk, or no progress.
- **Loop health** — a **decision/notes log** the loop appends each turn; a **stuck-detector** (no fewer failures / no progress over N turns → abort); the intermediate signals to watch so you can see *progress vs. thrash*.

## Step 5 — Fitness check (when NOT to loop)
STOP and say a loop is the wrong tool if **any** hold:
- **No real verifier and you can't scaffold one** — done isn't checkable independent of the agent.
- **No source of truth, or the foundations are too unclear** to execute safely.
- **It's a deterministic rule** → write code, not a loop.
- **Irreversible side effects with no approval gate.**
- **No one will review the output** → review debt.
If not a fit, say so plainly and fix the missing piece first (often: write the verifier, the spec, or the architecture doc).

## Step 6 — Write the artifacts + the kickoff
1. **`loop-brief.md`** in the working dir — the full contract (Steps 1–4): architecture, contract, the verifier stack + anti-goals + pre-flight result, safety/rollback, and the health signals. Use `loop-brief-template.md`; fill only what the task warrants.
2. **Durable context** — note any `CLAUDE.md` / `AGENTS.md` you wrote.
3. **The seed (not just the end-state)** — hand back the full kickoff: the `/goal` end-state **plus** the first instruction (which files to read, the plan, the brief) and **golden examples** to mirror ("follow `cache.py`'s structure; here's the PR that did the last one right").
   - Completion → `/goal "<verifiable end state, pointed at the verifier stack>"`
   - Time-triggered → `/loop <interval> "<prompt>"`; scheduled / event-triggered → a **Routine** (`claude.ai/code/routines`).
4. **Recurring loops** — add a **memory file** so each run learns from the last; and if the task is really *several* loops, **decompose into sub-loops** with clean handoffs instead of one mega-loop that drifts.

## Rules
- Infer before you ask; ask via the question UI; never interrogate.
- The architecture foundations are the point — a clear contract produces work that fits.
- **Never ship a verifier you can game.** If you can pass it without doing the work, fix the verifier (Step 3) before looping.
- Keep every side effect behind the approval boundary from Step 2.
- Prefer the smallest loop that produces verifiable progress against the contract.
