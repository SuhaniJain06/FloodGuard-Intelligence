from feature1_predict import predict_flood_risk


# ============================================================
# TEST CASES
# ============================================================

test_cases = [

    {
        "name": "LOW / Normal Conditions",
        "water_level_cm": 30.0,
        "water_level_rate_cm_per_min": 0.2,
        "rainfall_mm_per_hr": 10.0,
        "soil_moisture_pct": 20.0,
        "elevation_m": 180.0,
    },

    {
        "name": "MEDIUM / Rising Water",
        "water_level_cm": 50.0,
        "water_level_rate_cm_per_min": 1.5,
        "rainfall_mm_per_hr": 40.0,
        "soil_moisture_pct": 40.0,
        "elevation_m": 120.0,
    },

    {
        "name": "HIGH / Heavy Rainfall",
        "water_level_cm": 85.0,
        "water_level_rate_cm_per_min": 5.0,
        "rainfall_mm_per_hr": 100.0,
        "soil_moisture_pct": 65.0,
        "elevation_m": 80.0,
    },

    {
        "name": "CRITICAL / Extreme Flood",
        "water_level_cm": 130.0,
        "water_level_rate_cm_per_min": 15.0,
        "rainfall_mm_per_hr": 250.0,
        "soil_moisture_pct": 90.0,
        "elevation_m": 10.0,
    },

    {
        "name": "BOUNDARY / Maximum Values",
        "water_level_cm": 136.8,
        "water_level_rate_cm_per_min": 18.0,
        "rainfall_mm_per_hr": 299.6,
        "soil_moisture_pct": 98.0,
        "elevation_m": 5.0,
    },
]


# ============================================================
# RUN TESTS
# ============================================================

print("=" * 70)
print("FEATURE 1 — FLOOD RISK MODEL TEST")
print("=" * 70)


for i, case in enumerate(test_cases, start=1):

    name = case.pop("name")

    print()
    print("-" * 70)
    print(f"TEST CASE {i}: {name}")
    print("-" * 70)

    print("Inputs:")

    for key, value in case.items():
        print(f"  {key}: {value}")

    try:

        result = predict_flood_risk(
            **case
        )

        print()
        print("Prediction:")
        print(
            "  Risk class:",
            result["risk_class"]
        )
        print(
            "  Risk label:",
            result["risk_label"]
        )
        print(
            "  Confidence:",
            result["confidence"]
        )

    except Exception as e:

        print()
        print("❌ ERROR:")
        print(e)


print()
print("=" * 70)
print("FEATURE 1 TEST COMPLETE")
print("=" * 70)