"""The verifier. These pin the correct behavior — fix pricing.py, not these."""

from pytest import approx

from pricing import add_tax, apply_discount, cart_total


def test_apply_discount():
    assert apply_discount(100, 20) == approx(80.0)
    assert apply_discount(50, 0) == approx(50.0)


def test_add_tax():
    assert add_tax(100, 0.1) == approx(110.0)
    assert add_tax(200, 0.25) == approx(250.0)


def test_cart_total():
    cart = [
        {"price": 10.0, "qty": 2},
        {"price": 5.0, "qty": 3},
    ]
    assert cart_total(cart) == approx(35.0)
