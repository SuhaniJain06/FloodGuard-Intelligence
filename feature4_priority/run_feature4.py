import json
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# FEATURE 1 — FLOOD RISK
# ============================================================

FEATURE1_DIR = PROJECT_ROOT / "feature1_flood_risk"
sys.path.insert(0, str(FEATURE1_DIR))

from flood_risk import predict_flood_risk


# ============================================================
# FEATURE 2 — DRONE DETECTION
# ============================================================

FEATURE2_DIR = PROJECT_ROOT / "feature2_drone"
sys.path.insert(0, str(FEATURE2_DIR))

from feature2_detector import detect_people


# ============================================================
# FEATURE 3 — LYZR SOS
# ============================================================

FEATURE3_DIR = PROJECT_ROOT / "feature3_sos"
sys.path.insert(0, str(FEATURE3_DIR))

from extractor_llm import extract_sos_llm


# ============================================================
# FEATURE 4 — PRIORITY ENGINE
# ============================================================

from priority_engine import calculate_priority, safe_int


# ============================================================
# CONFIGURATION
# ============================================================

USE_LIVE_LYZR = True

# ============================================================
# FEATURE 2 — IMAGE
# ============================================================

IMAGE_PATH = Path(__file__).resolve().parent / "test_img2.jpg"


# ============================================================
# FEATURE 3 — GET SOS DATA
# ============================================================

print("=" * 70)
print("FEATURE 4 — MULTI-MODAL EMERGENCY PRIORITY")
print("=" * 70)

if USE_LIVE_LYZR:

    print()
    print("LIVE MODE — Lyzr Feature 3")

    sos_message = (
        "20-30 people are stuck with no contact for the last "
        "3 days near Maramon, Thottapuzha. "
        "They urgently need food, water and rescue. "
        "Contact 9876543210."
    )

    print()
    print("SOS message:")
    print(sos_message)

    sos_data = extract_sos_llm(sos_message)

else:

    print()
    print("DATASET MODE — extraction_results_v2.json")

    dataset_path = FEATURE3_DIR / "extraction_results_v2.json"

    with open(
        dataset_path,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    if not data:
        raise RuntimeError(
            "extraction_results_v2.json contains no cases."
        )

    sos_data = data[0]["extracted"]


# ============================================================
# FEATURE 2 — DRONE DETECTION
# ============================================================

print()
print("Running Feature 2 on:", IMAGE_PATH)

output, detections, feature2_people_count = detect_people(
    str(IMAGE_PATH)
)

print()
print(
    "Feature 2 detected people:",
    feature2_people_count
)


# ============================================================
# FEATURE 1 — FLOOD RISK
# ============================================================

print()
print("Running Feature 1 — Flood Risk")


# Demo IoT sensor values
water_level_cm = 130.0
water_level_rate_cm_per_min = 15.0
rainfall_mm_per_hr = 250.0
soil_moisture_pct = 90.0
elevation_m = 10.0


# Run Feature 1 model
flood_result = predict_flood_risk(
    water_level_cm=water_level_cm,
    water_level_rate_cm_per_min=water_level_rate_cm_per_min,
    rainfall_mm_per_hr=rainfall_mm_per_hr,
    soil_moisture_pct=soil_moisture_pct,
    elevation_m=elevation_m
)


print(
    "Feature 1 risk:",
    flood_result["risk_label"]
)

print(
    "Feature 1 confidence:",
    flood_result["confidence"]
)


# ============================================================
# FEATURE 1 → FEATURE 4
# ============================================================

risk_to_severity = {
    "LOW": 0.25,
    "MEDIUM": 0.50,
    "HIGH": 0.75,
    "CRITICAL": 1.00
}

flood_severity = risk_to_severity.get(
    flood_result["risk_label"],
    0.0
)

print(
    "Flood severity:",
    flood_severity
)


# ============================================================
# PEOPLE INFORMATION
# ============================================================

sos_people_raw = (
    sos_data
    .get("people", {})
    .get("total")
)

sos_people = safe_int(
    sos_people_raw
)

effective_people = max(
    sos_people,
    feature2_people_count
)

print()
print(
    "Feature 3 SOS people:",
    sos_people_raw
)

print(
    "Feature 2 drone people:",
    feature2_people_count
)

print(
    "Effective people:",
    effective_people
)


# ============================================================
# FEATURE 4 — PRIORITY ENGINE
# ============================================================

priority_result = calculate_priority(
    sos_data=sos_data,
    feature2_people_count=feature2_people_count,
    flood_severity=flood_severity
)


# ============================================================
# FEATURE 4 RESULT
# ============================================================

print()
print("=" * 70)
print("FEATURE 4 RESULT")
print("=" * 70)

print()

print(
    "Priority:",
    priority_result["priority"]
)

print(
    "Priority Score:",
    priority_result["priority_score"]
)


# ============================================================
# SCORE BREAKDOWN
# ============================================================

print()
print("Score Breakdown:")

for key, value in priority_result[
    "score_breakdown"
].items():

    print(
        f"  {key}: {value}"
    )


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

print()
print("Recommended Actions:")

for action in priority_result[
    "recommended_actions"
]:

    print(
        "  -",
        action
    )


# ============================================================
# FEATURE 1 DETAILS
# ============================================================

print()
print("=" * 70)
print("FEATURE 1 FLOOD RISK DETAILS")
print("=" * 70)

print()

print(
    "Water level:",
    water_level_cm,
    "cm"
)

print(
    "Water level rate:",
    water_level_rate_cm_per_min,
    "cm/min"
)

print(
    "Rainfall:",
    rainfall_mm_per_hr,
    "mm/hr"
)

print(
    "Soil moisture:",
    soil_moisture_pct,
    "%"
)

print(
    "Elevation:",
    elevation_m,
    "m"
)

print()

print(
    "Risk:",
    flood_result["risk_label"]
)

print(
    "Risk class:",
    flood_result["risk_class"]
)

print(
    "Confidence:",
    flood_result["confidence"]
)


# ============================================================
# FEATURE 3 — STRUCTURED SOS
# ============================================================

print()
print("=" * 70)
print("FEATURE 3 STRUCTURED SOS")
print("=" * 70)

print(
    json.dumps(
        sos_data,
        indent=2,
        ensure_ascii=False
    )
)