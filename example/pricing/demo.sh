#!/usr/bin/env bash
#
# Live-demo helper for the loop engineering video.
#
#   ./demo.sh   →  reset to the buggy start, show the setup on screen, and print
#                  the exact goal to hand to a loop.
#
# Then start your agent (claude / codex), paste the /goal it prints, and record
# the loop fixing the bugs and stopping on green. Run ./demo.sh again between takes.
#
set -euo pipefail
cd "$(dirname "$0")"

# Restore the buggy starting state + clear caches (reset.sh is self-contained).
bash reset.sh >/dev/null 2>&1 || true

clear
b=$(tput bold 2>/dev/null || true); d=$(tput dim 2>/dev/null || true); o=$(tput sgr0 2>/dev/null || true)

echo "${b}── LOOP ENGINEERING · live demo ──────────────────────────────${o}"
echo "  example/pricing — a tiny library with 3 intentional bugs."
echo
echo "${b}The bugs the loop has to fix${o} (pricing.py):"
echo "  ${d}•${o} apply_discount()  treats percent as a fraction (missing / 100)"
echo "  ${d}•${o} add_tax()         adds the rate instead of scaling by it"
echo "  ${d}•${o} cart_total()      ignores quantity"
echo
echo "${b}1.${o} The suite is red right now:"
echo "   ${d}\$ pytest -q${o}"
python3 -m pytest -q --tb=no || true
echo
echo "${b}2.${o} Hand it to a loop. Start your agent and paste this goal:"
echo
echo "   ${d}\$ claude${o}        ${d}# or: codex${o}"
echo "   ${b}/goal \"make pytest -q pass by fixing pricing.py — don't edit the tests\"${o}"
echo
echo "   Watch: run tests → edit pricing.py → re-run → all green → ${b}STOP${o}."
echo
echo "${b}3.${o} When it stops, prove it on camera:"
echo "   ${d}\$ pytest -q${o}            ${d}# all green${o}"
echo "   ${d}\$ git diff pricing.py${o}   ${d}# exactly what it changed${o}"
echo
echo "${d}Run ./demo.sh again to reset for the next take.${o}"
echo "──────────────────────────────────────────────────────────────"
