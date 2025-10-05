import pandas as pd
from models import crop_advisory, pest_predictor

# Load fallback dataset
crop_df = pd.read_csv("data/crop_recommendation_clean.csv")
pest_df = pd.read_csv("data/pest_diseases_clean.csv")

# Soil encoding for model input
soil_map = {"Loamy": 0, "Sandy": 1, "Clay": 2, "Red": 3}

import pandas as pd
from models import crop_advisory, pest_predictor

# Load fallback datasets
crop_df = pd.read_csv("data/crop_recommendation_clean.csv")
pest_df = pd.read_csv("data/pest_diseases_clean.csv")

# Soil encoding
soil_map = {"Loamy": 0, "Sandy": 1, "Clay": 2, "Red": 3}

# 🌾 Crop Recommendation
def recommend_crop(rainfall, temperature, soil):
    soil_code = soil_map.get(soil, -1)
    features = [rainfall, temperature, soil_code]

    crop = crop_advisory.call(features)[0]  # Use .call() wrapper

    # Fallback
    if crop in [None, "FallbackCrop"]:
        filtered = crop_df[
            (crop_df["rainfall_mm"].between(rainfall - 100, rainfall + 100)) &
            (crop_df["temperature_c"].between(temperature - 2, temperature + 2)) &
            (crop_df["soil_type"] == soil)
        ]
        if not filtered.empty:
            return filtered["crop"].value_counts().idxmax()
        return "No suitable crop found"

    return crop


# 🐛 Pest Diagnosis
def diagnose_pest(crop, symptoms):
    features = f"{crop} {symptoms}"  # combine for sklearn/HF

    result = pest_predictor.call(features)

    # Extract pest and treatment
    if isinstance(result, list):
        pest = result[0].get("label", "Unknown")
        treatment = result[0].get("treatment", "No treatment info")
    else:
        pest = result[0] if hasattr(result, "__getitem__") else str(result)
        treatment = "Treatment info not available"

    # Fallback dataset
    if pest in ["Unknown", "Not found", None]:
        match = pest_df[
            (pest_df["crop"] == crop) &
            (pest_df["symptoms"].str.contains(symptoms, case=False, na=False))
        ]
        if not match.empty:
            pest = match.iloc[0]["pest"]
            treatment = match.iloc[0]["treatment"]
        else:
            pest = "Not found"
            treatment = "No treatment available"

    return pest, treatment
