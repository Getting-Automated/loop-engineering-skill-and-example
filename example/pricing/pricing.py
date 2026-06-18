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
