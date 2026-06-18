# Loop brief — pricing example

The eight inputs a reliable loop needs, filled in for this demo. This is what the
`pre-loop` skill writes before you run `/goal`.

| Input | Value |
|-------|-------|
| **Task** | Make the failing tests in this folder pass |
| **Source of truth** | `test_pricing.py` (the asserted behavior) + the docstrings in `pricing.py` |
| **Done means** | `pytest -q` exits 0 — all tests green |
| **Verifier** | `pytest -q` (exits 0) |
| **Guard (anti-gaming)** | Fix the bugs in `pricing.py`; do **not** edit `test_pricing.py` — passing by changing the check doesn't count |
| **State** | The working tree (`pricing.py` edits) — no external state |
| **Stop when** | Success: `pytest` exits 0. Abort: 6 turns with no fewer failures. |
| **Human review** | None — local code + tests, fully reversible, no side effects |
| **Evidence** | Final `pytest -q` output + `git diff pricing.py` |

## The command  (Claude Code or Codex Goal mode — same line)

```
/goal "every test passes — pytest -q exits 0 — by fixing the bugs in pricing.py, not by editing test_pricing.py"
```

Why this works: the **definition of done is machine-checkable** (`pytest` exit
code) and the **verifier is independent of the agent** (it can't fake green).
That single line is what turns "keep going" into an operable loop.

> This is the **minimal** brief for a tiny task. For a non-trivial one with the
> full architecture / verifier-stack / anti-goals depth, see
> [`loop-brief-example.md`](../../loop-brief-example.md).
