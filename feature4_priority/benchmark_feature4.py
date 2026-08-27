import json

from priority_engine import calculate_priority


# ============================================================
# LOAD FEATURE 3 CASES
# ============================================================

with open(
    "extraction_results_v2.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


print("=" * 80)
print("FEATURE 4 — 300 CASE BENCHMARK")
print("=" * 80)

print("Total cases:", len(data))


# ============================================================
# BENCHMARK
# ============================================================

results = []

priority_counts = {
    "CRITICAL": 0,
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
}


for index, case in enumerate(data, start=1):

    try:

        sos_data = case["extracted"]

        # ----------------------------------------------------
        # Feature 2 is not available for every historical SOS.
        #
        # For this benchmark we test Feature 4's
        # Feature-3-only fallback.
        # ----------------------------------------------------

        result = calculate_priority(
            sos_data=sos_data,
            feature2_people_count=None,
            flood_severity=0.0
        )

        priority = result["priority"]

        priority_counts[priority] += 1

        results.append({
            "case": index,
            "case_id": case.get("case_id", index),
            "priority": priority,
            "score": result["priority_score"],
            "people_score":
                result["score_breakdown"]["people_score"],
            "vulnerability_score":
                result["score_breakdown"]["vulnerability_score"],
            "needs_score":
                result["score_breakdown"]["needs_score"],
            "request_score":
                result["score_breakdown"]["request_score"],
            "location_score":
                result["score_breakdown"]["location_score"]
        })

    except Exception as e:

        print()
        print("ERROR in case:", index)
        print("Error:", e)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 80)
print("BENCHMARK SUMMARY")
print("=" * 80)

print()

print("CRITICAL :", priority_counts["CRITICAL"])
print("HIGH     :", priority_counts["HIGH"])
print("MEDIUM   :", priority_counts["MEDIUM"])
print("LOW      :", priority_counts["LOW"])

print()
print("Successfully processed:", len(results))
print("Errors:", len(data) - len(results))


# ============================================================
# SAVE RESULTS
# ============================================================

with open(
    "feature4_benchmark_results.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False
    )


print()
print("✅ Saved: feature4_benchmark_results.json")