import json

from priority_engine import calculate_priority


# ============================================================
# LOAD FEATURE 3 OUTPUTS
# ============================================================

with open("extraction_results_v2.json", "r", encoding="utf-8") as f:
    data = json.load(f)


print("=" * 80)
print("FEATURE 4 — EMERGENCY PRIORITY ENGINE")
print("=" * 80)

print(f"Total Feature 3 cases: {len(data)}")
print()


# ============================================================
# TEST FIRST 10 CASES
# ============================================================

for i, case in enumerate(data[:10], start=1):

    sos_data = case["extracted"]

    # Feature 1 is not ready yet.
    flood_severity = 0.0

    # Feature 2 is not connected yet.
    feature2_people_count = None

    result = calculate_priority(
        sos_data=sos_data,
        feature2_people_count=feature2_people_count,
        flood_severity=flood_severity
    )

    print("-" * 80)
    print(f"CASE {i}")
    print(f"Message: {case.get('input', '')[:150]}")

    print()
    print(f"SOS people: {result['inputs']['sos_people']}")
    print(f"Priority: {result['priority']}")
    print(f"Score: {result['priority_score']}")

    print()
    print("Score breakdown:")
    for key, value in result["score_breakdown"].items():
        print(f"  {key}: {value}")

    print()
    print("Recommended actions:")
    for action in result["recommended_actions"]:
        print(f"  - {action}")

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)