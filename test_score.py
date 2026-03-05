"""
Tests for update_score() in app.py.
Covers final score after winning/losing, zero scores, negatives, and bad inputs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import only the pure function — no Streamlit needed
from app import update_score


passed = 0
failed = 0


def check(label, actual, expected):
    global passed, failed
    if actual == expected:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        print(f"        expected: {expected!r}")
        print(f"        got:      {actual!r}")
        failed += 1


def check_raises(label, fn):
    global passed, failed
    try:
        fn()
        print(f"  FAIL  {label}  (no exception raised)")
        failed += 1
    except Exception as e:
        print(f"  PASS  {label}  ({type(e).__name__}: {e})")
        passed += 1


# ---------------------------------------------------------------------------
# Win — points formula: 100 - 10*(attempt+1), floored at 10
# ---------------------------------------------------------------------------
print("=== Win: Final Score ===")

check("win attempt 1,  score 0   → 80",  update_score(0,   "Win", 1),  80)
check("win attempt 2,  score 0   → 70",  update_score(0,   "Win", 2),  70)
check("win attempt 3,  score 0   → 60",  update_score(0,   "Win", 3),  60)
check("win attempt 4,  score 0   → 50",  update_score(0,   "Win", 4),  50)
check("win attempt 5,  score 0   → 40",  update_score(0,   "Win", 5),  40)
check("win attempt 6,  score 0   → 30",  update_score(0,   "Win", 6),  30)
check("win attempt 7,  score 0   → 20",  update_score(0,   "Win", 7),  20)
check("win attempt 8,  score 0   → 10",  update_score(0,   "Win", 8),  10)
check("win attempt 9,  score 0   → 10 (floor)", update_score(0, "Win", 9),  10)
check("win attempt 10, score 0   → 10 (floor)", update_score(0, "Win", 10), 10)
check("win attempt 99, score 0   → 10 (floor)", update_score(0, "Win", 99), 10)

# accumulated score carries in
check("win attempt 1,  score 100 → 180", update_score(100, "Win", 1), 180)
check("win attempt 8,  score 50  → 60",  update_score(50,  "Win", 8),  60)

# ---------------------------------------------------------------------------
# Win — zero and negative starting scores
# ---------------------------------------------------------------------------
print("\n=== Win: Zero and Negative Starting Scores ===")

check("win attempt 1, score  0  → 80",  update_score(0,   "Win", 1), 80)
check("win attempt 1, score -80 → 0",   update_score(-80, "Win", 1), 0)   # exactly zero result
check("win attempt 1, score -90 → -10", update_score(-90, "Win", 1), -10) # still negative after win
check("win attempt 9, score -5  → 5",   update_score(-5,  "Win", 9), 5)   # floor still adds 10

# ---------------------------------------------------------------------------
# Loss path — Too Low and Too High penalties
# ---------------------------------------------------------------------------
print("\n=== Loss: Too Low Penalties ===")

check("too low,  score 100 → 95",   update_score(100, "Too Low", 1),  95)
check("too low,  score  10 → 5",    update_score(10,  "Too Low", 2),   5)
check("too low,  score   5 → 0",    update_score(5,   "Too Low", 3),   0)  # reaches zero
check("too low,  score   0 → -5",   update_score(0,   "Too Low", 4),  -5)  # goes negative
check("too low,  score  -5 → -10",  update_score(-5,  "Too Low", 5), -10)  # deepens negative

print("\n=== Loss: Too High Penalties / Bonuses ===")

check("too high even attempt, score 100 → 105", update_score(100, "Too High", 2), 105)
check("too high odd  attempt, score 100 → 95",  update_score(100, "Too High", 1),  95)
check("too high even attempt, score 0   → 5",   update_score(0,   "Too High", 4),   5)
check("too high odd  attempt, score 0   → -5",  update_score(0,   "Too High", 3),  -5)
check("too high even attempt, score -10 → -5",  update_score(-10, "Too High", 6),  -5)

# ---------------------------------------------------------------------------
# Edge: final score exactly zero
# ---------------------------------------------------------------------------
print("\n=== Edge: Score Reaches Exactly Zero ===")

check("score 5, too low  → 0",     update_score(5,  "Too Low",  1),  0)
check("score 5, too high odd → 0", update_score(5,  "Too High", 1),  0)

# ---------------------------------------------------------------------------
# Edge: non-integer attempt_number
# ---------------------------------------------------------------------------
print("\n=== Edge: Non-Integer attempt_number ===")

# float attempt: 100 - 10*(1.5+1) = 75; 75 >= 10 so no floor
check("win, attempt=1.5 (float) → 75", update_score(0, "Win", 1.5), 75)
# 1.5 % 2 = 1.5 (not 0), so odd branch: -5
check("too high, attempt=2.0 (even float) → +5", update_score(0, "Too High", 2.0), 5)
check("too high, attempt=1.5 (odd  float) → -5", update_score(0, "Too High", 1.5), -5)

# ---------------------------------------------------------------------------
# Edge: unknown / bad outcome string
# ---------------------------------------------------------------------------
print("\n=== Edge: Unknown Outcome (no change expected) ===")

check("unknown outcome 'Draw'   → unchanged", update_score(50, "Draw",   1), 50)
check("unknown outcome ''       → unchanged", update_score(50, "",       1), 50)
check("unknown outcome None     → unchanged", update_score(50, None,     1), 50)
check("outcome misspelled 'win' → unchanged", update_score(50, "win",    1), 50)

# ---------------------------------------------------------------------------
# Edge: bad types for current_score
# ---------------------------------------------------------------------------
print("\n=== Edge: Non-Integer current_score ===")

check("float score 10.5, win attempt 1 → 90.5", update_score(10.5, "Win", 1), 90.5)
check("float score  0.0, win attempt 1 → 80.0", update_score(0.0,  "Win", 1), 80.0)

check_raises("string score raises TypeError",
             lambda: update_score("100", "Win", 1))

# ---------------------------------------------------------------------------
# Edge: negative attempt_number
# ---------------------------------------------------------------------------
print("\n=== Edge: Negative attempt_number ===")

# attempt -1: 100 - 10*(-1+1) = 100 - 0 = 100; 100 >= 10 so no floor
check("win, attempt=-1 → 100", update_score(0, "Win", -1), 100)
# attempt 0:  100 - 10*(0+1) = 90
check("win, attempt=0  → 90",  update_score(0, "Win", 0),  90)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n{'='*40}")
print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
if failed == 0:
    print("All tests passed!")
else:
    print(f"{failed} test(s) FAILED — review output above.")
