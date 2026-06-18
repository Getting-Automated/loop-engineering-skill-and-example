#!/usr/bin/env bash
#
# Reset the goal-loop demo to its starting state — run this between takes.
# It restores the three intentional bugs in pricing.py, clears caches, and
# confirms the suite is red again (3 failed) so you know you're demo-ready.
#
# Self-contained: no git required (works on a fresh clone, before a commit, or
# after you've hand-edited). The canonical buggy pricing.py is embedded below —
# if you ever change pricing.py's shape, update this heredoc to match.
#
set -euo pipefail
cd "$(dirname "$0")"

cat > pricing.py <<'PY'
"""A tiny pricing library with three intentional bugs.

This is a demo target for an agent loop. Run the tests to see three failures,
then point a goal loop at it:

    pytest -q                                                    # 3 failed
    claude
    /goal "every test in this folder passes: run pytest -q and it exits 0"

The agent reads the failing tests, fixes the functions below, re-runs pytest,
and stops when the suite is green. That is the whole loop: action -> verifier
-> stop. The tests in test_pricing.py are the source of truth — fix the code,
not the tests.
"""


def apply_discount(price: float, percent: float) -> float:
    """Return ``price`` reduced by ``percent`` percent.

    apply_discount(100, 20) -> 80.0
    """
    # BUG: treats ``percent`` as a fraction, not a percentage (missing / 100).
    return price * (1 - percent)


def add_tax(price: float, rate: float) -> float:
    """Return ``price`` with tax ``rate`` applied.

    add_tax(100, 0.1) -> 110.0
    """
    # BUG: adds the rate instead of scaling the price by it.
    return price + rate


def cart_total(items: list[dict]) -> float:
    """Total an itemized cart of ``{"price", "qty"}`` dicts.

    cart_total([{"price": 10.0, "qty": 2}, {"price": 5.0, "qty": 3}]) -> 35.0
    """
    # BUG: ignores quantity.
    return sum(item["price"] for item in items)
PY

# Clear test caches so the next run is clean.
rm -rf __pycache__ .pytest_cache

echo "✓ Restored the 3 bugs in pricing.py and cleared caches."

# Confirm the demo is red again (the verifier should report 3 failures).
if python3 -c "import pytest" >/dev/null 2>&1; then
  out=$(python3 -m pytest -q 2>&1 || true)
  echo "${out##*$'\n'}"
  if printf '%s' "$out" | grep -q "3 failed"; then
    echo "✓ Demo-ready: 3 failing tests. Point a loop at it again."
  else
    echo "✗ Expected 3 failures — check the output above."
    exit 1
  fi
else
  echo "• pytest not installed — skipping the check (run: pip install -r requirements.txt)."
fi
