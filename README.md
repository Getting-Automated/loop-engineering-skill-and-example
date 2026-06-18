# Loop Engineering — skill + runnable example

Companion repo to the Getting Automated **Loop Engineering** explainer. It ships
two things you can actually run:

## 1. The `pre-loop` skill — for **Claude Code AND Codex**

Run it **before** a loop (`/goal`, `/loop`, Codex Goal, or an Automation). It does
the thinking that makes a loop produce work that *fits your system* instead of
drifting into something you have to rip out:

- **Runs as an interactive wizard** — reads your repo first (`CLAUDE.md`/`AGENTS.md`,
  README, architecture docs, manifests, lint/test/CI config, nearby code), then asks
  only for the gaps — via Claude Code's question UI, or concise prompts in Codex.
- **Solidifies the architecture foundations** — where the work fits, patterns to
  follow, interfaces/contracts, constraints, anti-patterns, ownership/escalation,
  and the downstream surface it must not break. Offers to write a durable
  `CLAUDE.md`/`AGENTS.md` if you lack one.
- **Builds and guards the verifier** — assembles the full **verifier stack**
  (tests · types · lint · build · review), **scaffolds one if it's missing**
  (writes the failing acceptance test), names how an agent could **game** it and
  adds guards, and **pre-flights** it (runs it once to confirm it actually works).
- **Sets up safe, observable execution** — an isolated **branch/worktree** + rollback,
  a budget estimate, stop/abort conditions, and a **decision log + stuck-detector**.
- **Writes the full contract** (`loop-brief.md`) + the **kickoff seed** (the `/goal`
  + first instruction + golden examples), and tells you plainly **when not to loop**.

Full contract structure: [`loop-brief-template.md`](loop-brief-template.md) — and a
filled, non-trivial example: [`loop-brief-example.md`](loop-brief-example.md).

Claude Code and Codex use the **same skill format** (`SKILL.md` with `name` +
`description` frontmatter) — only the install directory and the command it emits
differ. This repo ships one for each:

| Tool | Skill file | Install (global) | Invoke |
|------|-----------|------------------|--------|
| **Claude Code** | [`.claude/skills/pre-loop/`](.claude/skills/pre-loop/SKILL.md) | `cp -r .claude/skills/pre-loop ~/.claude/skills/` | `/pre-loop` |
| **Codex** | [`.agents/skills/pre-loop/`](.agents/skills/pre-loop/SKILL.md) | `cp -r .agents/skills/pre-loop ~/.agents/skills/` | `/skills` → pre-loop, or `$pre-loop` |

…or just open this repo in the tool and it's available as a project skill.
The Claude Code version emits `/loop` · `/goal` · Routines; the Codex version emits
`/goal` (Goal mode) · Automations. The `loop-brief.md` it writes is identical and
works either way.

## 2. Goal-loop demo → [`example/pricing/`](example/pricing/README.md)

A tiny project with three failing tests, so you can run a real loop on screen:

```bash
cd example/pricing
pip install -r requirements.txt
pytest -q          # 3 failed
```

Then run the loop in **Claude Code** (`claude`) or **Codex** (`codex`) — same command:

```
/goal "every test in this folder passes: run pytest -q and it exits 0"
```

The agent reads the failing tests, fixes the code, re-runs `pytest`, and stops
when the suite is green — **action → verifier → stop.**

Reset between takes with **`example/pricing/reset.sh`** — it restores the bugs,
clears caches, and confirms 3 failures (self-contained, no git required).

---

## The idea in one line

A loop is only as good as the contract it executes against. The `pre-loop` skill
writes that contract; the example shows the loop honoring it. Generation is easy
— **verified, self-correcting progress is the whole point.**
