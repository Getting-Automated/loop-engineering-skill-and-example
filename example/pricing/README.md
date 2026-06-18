# Goal-loop demo: make the failing tests pass

A tiny, self-contained example for showing an agent loop on screen. `pricing.py`
ships with **three intentional bugs**; `test_pricing.py` pins the correct
behavior. Point a goal loop at it and watch it drive the suite to green — and
stop on its own.

## 1. See the three failures

```bash
cd example/pricing
pip install -r requirements.txt
pytest -q          # 3 failed
```

## 2. Run the loop  (Claude Code or Codex — same command)

**Claude Code:**
```bash
claude
/goal "every test in this folder passes: run pytest -q and it exits 0"
```

**Codex** (Goal mode — identical loop):
```bash
codex
/goal "every test in this folder passes: run pytest -q and it exits 0"
```

The agent reads the failing tests, fixes `pricing.py`, re-runs `pytest`, and
**STOPS** when the suite is green. That's the whole loop: **action → verifier → stop.**

## What to point at on screen

- The **verifier** is `pytest` — proof that's independent of the agent's claim.
- The agent is not prompted five times; it's given a checkable **definition of done**.
- It stops by itself when the condition holds — no babysitting.

## Reset between takes

```bash
./reset.sh
```

Restores the three bugs, clears caches, and **confirms the suite is red again
(3 failed)** — so you know you're demo-ready. Self-contained, no git required.

See [`loop-brief.md`](./loop-brief.md) for the brief behind this run — the same
brief the `pre-loop` skill produces.
