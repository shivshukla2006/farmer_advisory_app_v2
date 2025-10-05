import pandas as pd
from models import weather_alert_model

# Load fallback dataset
weather_df = pd.read_csv("data/weather_india_clean.csv")

# Region encoding for model input
region_map = {name: i for i, name in enumerate(weather_df["region"].unique())}

# 🌦️ Predict Weather Alert
def get_weather_alert(region, temperature, humidity, wind_kph):
    region_code = region_map.get(region, -1)
    features = [[region_code, temperature, humidity, wind_kph]]  # 2D for sklearn

    alert = None

    try:
        # ✅ Case 1: Scikit-learn model
        alert = weather_alert_model.predict(features)[0]
    except AttributeError:
        try:
            # ✅ Case 2: Hugging Face pipeline (classification)
            result = weather_alert_model(features)
            if isinstance(result, list) and "label" in result[0]:
                alert = result[0]["label"]
            else:
                alert = str(result)
        except Exception:
            # ✅ Case 3: Unknown object → force fallback
            alert = "FallbackAlert"

    # ✅ Fallback using dataset
    if alert in ["FallbackAlert", None]:
        filtered = weather_df[
            (weather_df["region"] == region) &
            (weather_df["temperature_c"].between(temperature - 2, temperature + 2)) &
            (weather_df["humidity"].between(humidity - 10, humidity + 10)) &
            (weather_df["wind_kph"].between(wind_kph - 5, wind_kph + 5))
        ]
        if not filtered.empty:
            return filtered["alert"].value_counts().idxmax()
        return "No alert found"

    return alert
