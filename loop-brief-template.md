
# Loop brief — <task>

The contract the loop runs on. The `pre-loop` skill fills this in (inferring most
of it from the repo). Fill only what the task warrants — a one-file fix needs
§1, §5, §7; a new subsystem needs all of it. See
[`loop-brief-example.md`](loop-brief-example.md) for this template filled in for a
real, non-trivial task.

## 1. Intent
- **Goal:** <the outcome>
- **Why it matters:** <so the loop makes good tradeoffs, not just compiling ones>

## 2. Scope
- **In scope:** <what to change>
- **Out of scope / non-goals:** <what to leave alone — this is what stops drift>

## 3. Architecture foundations  (what the work must FIT)
- **Where it fits:** <module / layer / boundary; what it must not reach across>
- **Patterns to follow:** <existing files to mirror + conventions>
- **Stack & deps:** approved → <…>  ·  do NOT introduce → <…>
- **Interfaces & contracts:** <APIs, schemas, types, events to honor without breaking callers>
- **Data / source of truth:** <where the authoritative data lives>
- **Non-negotiables:** <security · performance · accessibility · compliance · backward-compat>
- **Avoid:** <known anti-patterns / past mistakes>
- **Owner / reviewer / escalation:** <who>
- **Downstream surface (must not break):** <callers · CI · other services>

## 4. Plan  (for non-trivial work)
1. <step> — depends on <…>
2. <step>

## 5. Definition of done + verifier stack
- **Done means:** <acceptance criteria, in checkable terms>
- **Verifiers (all must pass, independent of the agent's claim):**
  - tests: `<cmd>`  ·  types: `<cmd>`  ·  lint/format: `<cmd>`  ·  build: `<cmd>`  ·  contract/schema: `<cmd>`
  - review gate: <human / rubric, if any>
- **Scaffolded?** <if no verifier existed, the acceptance test/schema we wrote>
- **Pre-flight:** <ran the verifier once → it executes and fails for the right reason; deps/env/fixtures present>

## 6. Anti-goals  (how the agent could "pass" WITHOUT doing the work → guard each)
- <e.g. weakening or deleting tests> → **guard:** tests are read-only; diff must touch the implementation.
- <e.g. hard-coding expected output> → **guard:** verifier uses fresh/random inputs.
- <e.g. silencing types/lint> → **guard:** no new `# type: ignore` / `eslint-disable`; coverage can't drop.
- <e.g. mocking the thing under test> → **guard:** integration check on the real path.

## 7. Safe execution
- **Isolation:** branch / worktree `<name>` (a bad run is one `git checkout` away).
- **Rollback:** <how to undo>

## 8. Budget, stop & loop health
- **Budget estimate:** <turns / tokens / $>
- **Stop:** <success exit>  ·  **Pause:** <missing context>  ·  **Abort:** <budget / risk / no progress over N turns>
- **Decision log:** <where the loop appends its reasoning each turn>
- **Progress signal / stuck-detector:** <fewer failures each run; abort if flat for N turns>

## 9. State & evidence
- **State across turns:** <working tree; the decision log>
- **Evidence handed off:** <final verifier output + the diff + the decision log>

---

## Kickoff (the seed — not just the end-state)
- **First instruction:** read <files>; follow the plan in §4; the contract is this brief.
- **Golden examples to mirror:** <similar file / the PR that did the last one right>
- **Memory (recurring loops):** <file the run reads/updates so it learns across runs>

```
/goal "<verifiable end state — reference this brief + the verifier stack>"
```
e.g. `/goal "loop-brief.md done: pytest -q, mypy, and ruff all pass; the public API in api.py is unchanged; the diff does not touch tests/"`
