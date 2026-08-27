import joblib
import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best_flood_risk_model.joblib"
FEATURE_NAMES_PATH = BASE_DIR / "feature_names.joblib"
LABEL_MAPPING_PATH = BASE_DIR / "label_mapping.joblib"


# ============================================================
# LOAD MODEL ARTIFACTS
# ============================================================

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)
label_mapping = joblib.load(LABEL_MAPPING_PATH)

# Convert:
# {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
#
# into:
# {0: "LOW", 1: "MEDIUM", 2: "HIGH", 3: "CRITICAL"}

inverse_mapping = {
    value: key
    for key, value in label_mapping.items()
}


# ============================================================
# VALID INPUT RANGES
# ============================================================

RANGES = {
    "water_level_cm": (2.0, 136.8),
    "water_level_rate_cm_per_min": (-8.0, 18.0),
    "rainfall_mm_per_hr": (0.075, 299.6),
    "soil_moisture_pct": (5.0, 98.0),
    "elevation_m": (5.0, 250.0),
}


# ============================================================
# FEATURE 1 PREDICTION
# ============================================================

def predict_flood_risk(
    water_level_cm,
    water_level_rate_cm_per_min,
    rainfall_mm_per_hr,
    soil_moisture_pct,
    elevation_m,
):

    # --------------------------------------------------------
    # Convert inputs to float
    # --------------------------------------------------------

    water_level_cm = float(water_level_cm)
    water_level_rate_cm_per_min = float(
        water_level_rate_cm_per_min
    )
    rainfall_mm_per_hr = float(rainfall_mm_per_hr)
    soil_moisture_pct = float(soil_moisture_pct)
    elevation_m = float(elevation_m)

    # --------------------------------------------------------
    # Build raw feature dictionary
    # --------------------------------------------------------

    row = {
        "water_level_cm": water_level_cm,
        "water_level_rate_cm_per_min":
            water_level_rate_cm_per_min,
        "rainfall_mm_per_hr": rainfall_mm_per_hr,
        "soil_moisture_pct": soil_moisture_pct,
        "elevation_m": elevation_m,
    }

    # --------------------------------------------------------
    # ENGINEERED FEATURES
    # --------------------------------------------------------

    row["rain_x_rate"] = (
        rainfall_mm_per_hr
        * water_level_rate_cm_per_min
    )

    row["level_div_elevation"] = (
        water_level_cm
        / (elevation_m + 1.0)
    )

    row["soil_x_rain"] = (
        soil_moisture_pct
        * rainfall_mm_per_hr
    )

    row["level_x_rate"] = (
        water_level_cm
        * water_level_rate_cm_per_min
    )

    row["rain_div_soil"] = (
        rainfall_mm_per_hr
        / (soil_moisture_pct + 1.0)
    )

    # --------------------------------------------------------
    # CREATE DATAFRAME IN EXACT MODEL FEATURE ORDER
    # --------------------------------------------------------

    input_df = pd.DataFrame(
        [row]
    )[feature_names]

    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    predicted_class = int(
        model.predict(input_df)[0]
    )

    probabilities = model.predict_proba(
        input_df
    )[0]

    # --------------------------------------------------------
    # CONVERT CLASS → LABEL
    # --------------------------------------------------------

    predicted_label = inverse_mapping[
        predicted_class
    ]

    # Probability of predicted class
    confidence = float(
        probabilities[predicted_class]
    )

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "risk_class": predicted_class,
        "risk_label": predicted_label,
        "confidence": round(confidence, 4),
    }