from advisory import recommend_crop, diagnose_pest
from alerts import get_weather_alert
from schemes import find_schemes
from translate import translate_to_hindi

# 📩 Generate SMS message
def generate_sms_response(query_type, user_input, language="english"):
    if query_type == "crop":
        rainfall = user_input.get("rainfall")
        temperature = user_input.get("temperature")
        soil = user_input.get("soil")
        crop = recommend_crop(rainfall, temperature, soil)
        msg = f"Recommended crop: {crop}"

    elif query_type == "pest":
        crop = user_input.get("crop")
        symptoms = user_input.get("symptoms")
        pest, treatment = diagnose_pest(crop, symptoms)
        msg = f"Pest: {pest}\nTreatment: {treatment}"

    elif query_type == "weather":
        region = user_input.get("region")
        temp = user_input.get("temperature")
        humidity = user_input.get("humidity")
        wind = user_input.get("wind_kph")
        alert = get_weather_alert(region, temp, humidity, wind)
        msg = f"Weather Alert for {region}: {alert}"

    elif query_type == "scheme":
        crop = user_input.get("crop")
        region = user_input.get("region")
        category = user_input.get("category")
        schemes = find_schemes(crop, region, category, language)
        msg = "\n".join([f"{s['scheme_name']}: {s['description']}" for s in schemes[:2]])

    else:
        msg = "Invalid query type."

    return translate_to_hindi(msg) if language == "hindi" else msg