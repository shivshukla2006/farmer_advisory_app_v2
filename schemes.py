import pandas as pd
import os
from models import translate_to_hindi

# Path to schemes dataset
SCHEMES_FILE = "data/schemes.csv"

# 📚 Load schemes
def load_schemes():
    if os.path.exists(SCHEMES_FILE):
        return pd.read_csv(SCHEMES_FILE)
    return pd.DataFrame(columns=["scheme_name", "crop", "region", "category", "description"])

# 🔍 Find schemes by crop, region, or category
def find_schemes(crop=None, region=None, category=None, language="english"):
    df = load_schemes()

    if crop:
        df = df[df["crop"].str.contains(crop, case=False, na=False)]
    if region:
        df = df[df["region"].str.contains(region, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]

    if df.empty:
        return [{"scheme_name": "No schemes found", "description": "Try different filters"}]

    results = df[["scheme_name", "description"]].to_dict(orient="records")

    if language == "hindi":
        for r in results:
            r["description"] = translate_to_hindi(r["description"])

    return results

# 🆕 Add a new scheme (admin use)
def add_scheme(scheme_name, crop, region, category, description):
    df = load_schemes()
    new_entry = {
        "scheme_name": scheme_name,
        "crop": crop,
        "region": region,
        "category": category,
        "description": description
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(SCHEMES_FILE, index=False)
    return "✅ Scheme added successfully."