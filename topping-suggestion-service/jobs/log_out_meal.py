import sys

VALID_MEALS = ["breakfast", "lunch", "dinner"]
meal = sys.argv[1]

if meal not in VALID_MEALS:
    raise RuntimeError(f"Invalid meal {meal}")

if meal == "breakfast":
    print("🍳" * 50)
    print("🍕" * 50)
    print("☕" * 50)

if meal == "lunch":
    print("🥗" * 50)
    print("🍕" * 50)
    print("🍹" * 50)

if meal == "dinner":
    print("🥤" * 50)
    print("🍕" * 50)
    print("🍦" * 50)
