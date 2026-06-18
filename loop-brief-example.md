# Loop brief — add rate limiting to the public API

A **fully-worked, non-trivial** example of what the enhanced `pre-loop` skill
produces — the architecture section, a real verifier stack, anti-goals, safety,
and health signals all filled in. (The one in `example/pricing/` is the *minimal*
version for a tiny task; the skill scales depth to the work.) Blank template:
[`loop-brief-template.md`](loop-brief-template.md).

## 1. Intent
- **Goal:** add per-API-key token-bucket rate limiting to the public REST API (default 100 req/min, configurable per key).
- **Why it matters:** a few noisy keys are degrading p95 latency for everyone; we need fair-use limits without changing the public contract.

## 2. Scope
- **In scope:** a middleware in the request pipeline; per-key limits from config; `429` + `Retry-After` on breach; a metrics counter.
- **Out of scope / non-goals:** cluster-wide/distributed limiting (single-node for now); any dashboard/UI; billing; changing existing endpoint behavior under the limit.

## 3. Architecture foundations
- **Where it fits:** `api/middleware/` — runs **after** auth (needs the API key), **before** routing. Must NOT reach into handlers or the DB layer.
- **Patterns to follow:** mirror `api/middleware/auth.py` (same middleware shape, same error envelope). Errors go through the existing `problem+json` responder. Config via `settings.py`, not env reads in the middleware.
- **Stack & deps:** stdlib + the existing Redis client for the bucket store. Do NOT add a new rate-limit library or a second Redis.
- **Interfaces & contracts:** must not change any 2xx response body or existing status codes; only adds `429`. The public `openapi.yaml` must still validate.
- **Data / source of truth:** per-key limits in `settings.RATE_LIMITS`; counters in Redis (`rl:{api_key}`, TTL = window).
- **Non-negotiables:** O(1) per request; no added DB calls; **fail-open** if Redis is down (log + allow, never 500); no PII in keys or logs.
- **Avoid:** in-memory counters (won't survive restarts / multiple workers); any blocking call in the hot path.
- **Owner / reviewer / escalation:** @api-team owns · @hunter reviews · escalate latency regressions to #api-oncall.
- **Downstream surface (must not break):** the SDK's retry logic (honors `Retry-After`), the gateway's own limits, the CI contract tests.

## 4. Plan
1. Add `RATE_LIMITS` to `settings.py` + a typed loader. *(no deps)*
2. `RateLimiter` — token bucket over Redis, fail-open. *(1)*
3. `rate_limit_middleware`, mirroring `auth.py`; wire it **after** auth. *(2)*
4. `429` + `Retry-After` via the existing `problem+json` responder. *(3)*
5. Metrics counter `rate_limit_block_total{key_class}`. *(3)*

## 5. Definition of done + verifier stack
- **Done means:** limits enforced per the config; `429`+`Retry-After` on breach; existing endpoints unchanged; p95 overhead < 2 ms; fail-open verified.
- **Verifiers (all pass, independent of the agent):**
  - tests: `pytest api/tests/test_rate_limit.py -q` (under → 200; over → 429+Retry-After; Redis-down → allow)
  - types: `mypy api/`  ·  lint: `ruff check api/`
  - contract: `schemathesis run openapi.yaml` (no 2xx contract changed)
  - perf: `pytest api/tests/test_rate_limit_perf.py` (added p95 < 2 ms over 1k reqs)
  - review gate: @api-team approves the middleware ordering
- **Scaffolded:** wrote `test_rate_limit.py` (failing acceptance tests) + the perf test first.
- **Pre-flight:** ran `pytest api/tests/test_rate_limit.py -q` → fails for the right reason (middleware not wired); Redis reachable; `schemathesis` runs.

## 6. Anti-goals  (how it could "pass" without doing the work → guard each)
- Loosen / sky-high the limit to make tests pass → **guard:** limits come from the test fixture; tests assert the exact 429 boundary.
- Pass by disabling the limiter under test → **guard:** integration test hits the real middleware on the real app; diff must not touch test config to weaken it.
- Hard-code `Retry-After` → **guard:** test asserts it equals the *computed* remaining window.
- Fail-**closed** on Redis errors (count as limited) → **guard:** explicit fail-open test (Redis down → allowed).
- Add a sync round-trip in the hot path → **guard:** the perf test.

## 7. Safe execution
- **Isolation:** branch `feat/rate-limit` (worktree). Bad run → delete the branch.
- **Rollback:** ships behind flag `RATE_LIMIT_ENABLED` (default **off**) — dark launch, instant revert.

## 8. Budget, stop & loop health
- **Budget estimate:** ~8–15 turns / ~$3–6.
- **Stop:** all six verifiers green + review gate.  **Pause:** limit table or `Retry-After` semantics unclear.  **Abort:** >15 turns with the failing count not dropping, or any verifier can't run.
- **Decision log:** `.loop/rate-limit-notes.md` (each turn: what changed + why).
- **Stuck-detector:** failing-assert count must drop each turn; flat for 3 turns → abort and surface the blocker.

## 9. State & evidence
- **State across turns:** working tree on the branch + the decision log.
- **Evidence handed off:** green output for all six verifiers, the diff, the decision log, a p95 before/after note.

---

## Kickoff (the seed — not just the end-state)
- **First instruction:** read `api/middleware/auth.py`, `settings.py`, `openapi.yaml`, and the new `api/tests/test_rate_limit.py`. Follow the plan in §4. The contract is this brief. Work only under `api/`.
- **Golden example to mirror:** `api/middleware/auth.py` (middleware shape + error envelope).
- **Command:**
  ```
  /goal "rate-limit loop-brief done: pytest api/tests/test_rate_limit*.py, mypy api/, ruff check api/, and schemathesis all pass; existing 2xx responses unchanged; the diff does not weaken tests/ or fixtures"
  ```
