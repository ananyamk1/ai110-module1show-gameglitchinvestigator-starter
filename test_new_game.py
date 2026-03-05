"""
Tests for the New Game button logic in app.py.
Simulates st.session_state with a plain namespace and runs the same
handler code to verify status resets to "playing" and history clears.
"""

import random
from types import SimpleNamespace


def simulate_new_game(session_state, low=1, high=100):
    """Mirrors the new_game handler in app.py (lines 134-140)."""
    session_state.attempts = 1
    session_state.secret = random.randint(low, high)
    session_state.status = "playing"
    session_state.history = []


def make_state(**kwargs):
    defaults = dict(attempts=1, secret=42, score=0, status="playing", history=[])
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def check(label, actual, expected):
    if actual == expected:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}")
        print(f"        expected: {expected!r}")
        print(f"        got:      {actual!r}")


# ---------------------------------------------------------------------------
# Core behaviour
# ---------------------------------------------------------------------------

print("=== Core New Game Behaviour ===")

# 1. status resets from "won" to "playing"
state = make_state(status="won", history=[10, 20, 30])
simulate_new_game(state)
check("status resets from 'won' to 'playing'", state.status, "playing")

# 2. status resets from "lost" to "playing"
state = make_state(status="lost", history=[5, 15, 25, 35])
simulate_new_game(state)
check("status resets from 'lost' to 'playing'", state.status, "playing")

# 3. history clears after win
state = make_state(status="won", history=[7, 14, 42])
simulate_new_game(state)
check("history clears to [] after win", state.history, [])

# 4. history clears after loss
state = make_state(status="lost", history=[1, 2, 3, 4, 5, 6, 7, 8])
simulate_new_game(state)
check("history clears to [] after loss", state.history, [])

# 5. attempts resets to 1
state = make_state(attempts=8)
simulate_new_game(state)
check("attempts resets to 1", state.attempts, 1)

# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

print("\n=== Edge Cases ===")

# 6. history already empty — stays empty
state = make_state(history=[])
simulate_new_game(state)
check("history stays [] when already empty", state.history, [])

# 7. status already "playing" — stays "playing"
state = make_state(status="playing")
simulate_new_game(state)
check("status stays 'playing' when already 'playing'", state.status, "playing")

# 8. secret stays within Easy range (1–20)
results = []
for _ in range(200):
    state = make_state()
    simulate_new_game(state, low=1, high=20)
    results.append(state.secret)
in_range = all(1 <= s <= 20 for s in results)
check("new secret is always within Easy range (1–20)", in_range, True)

# 9. secret stays within Hard range (1–50)
results = []
for _ in range(200):
    state = make_state()
    simulate_new_game(state, low=1, high=50)
    results.append(state.secret)
in_range = all(1 <= s <= 50 for s in results)
check("new secret is always within Hard range (1–50)", in_range, True)

# 10. score is preserved across new game (intentional — cumulative)
state = make_state(score=250)
simulate_new_game(state)
check("score is preserved (cumulative across games)", state.score, 250)

# 11. new game called multiple times in a row
state = make_state(status="won", history=[1, 2, 3])
simulate_new_game(state)
simulate_new_game(state)
simulate_new_game(state)
check("status 'playing' after 3 consecutive new games", state.status, "playing")
check("history [] after 3 consecutive new games", state.history, [])
check("attempts 1 after 3 consecutive new games", state.attempts, 1)

# 12. large history clears completely
big_history = list(range(1, 101))
state = make_state(history=big_history)
simulate_new_game(state)
check("large history (100 items) clears to []", state.history, [])

print("\nDone.")
