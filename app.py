import streamlit as st
import pandas as pd

# Import functions from individual modules
from advisory import recommend_crop, diagnose_pest
from alerts import get_weather_alert
from schemes import find_schemes
from community import post_message, get_recent_messages
from translate import translate_to_hindi

# Load dataset to extract regions dynamically
weather_df = pd.read_csv("data/weather_india_clean.csv")
regions = sorted(weather_df["region"].unique())

# Wrapper functions for UI
def get_crop_advice(rainfall, temperature, soil, language="english"):
    crop = recommend_crop(rainfall, temperature, soil)
    return translate_to_hindi(f"✅ Recommended crop: {crop}") if language == "hindi" else f"✅ Recommended crop: {crop}"

def get_pest_advice(crop, symptoms, language="english"):
    pest, treatment = diagnose_pest(crop, symptoms)
    msg = f"🐛 Pest Detected: {pest}\n💊 Suggested Treatment: {treatment}"
    return translate_to_hindi(msg) if language == "hindi" else msg

def get_alert(region, temperature, humidity, wind_kph, language="english"):
    alert = get_weather_alert(region, temperature, humidity, wind_kph)
    msg = f"⚠️ Weather Alert for {region}: {alert}"
    return translate_to_hindi(msg) if language == "hindi" else msg

def get_scheme_info(crop=None, region=None, category=None, language="english"):
    return find_schemes(crop, region, category, language)

def post_to_community(name, region, message, language="english"):
    return post_message(name, region, message, language)

def view_community_feed(limit=5, language="english"):
    return get_recent_messages(limit, language)

# Streamlit UI
st.set_page_config(page_title="🌾 Farmer Advisory Platform", layout="wide")
st.markdown("<h1 style='text-align: center;'>🌾 Farmer Advisory Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your one-stop hub for crop advice, pest alerts, weather warnings, schemes, and community wisdom.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("🌐 Choose Language", ["english", "hindi"], help="Switch to Hindi for translated advice")
    st.markdown("---")
    st.info("💡 Tip: You can interact with each section independently.")

# 🌱 Crop Advisory
st.subheader("🌱 Crop Advisory")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        rainfall = st.slider("🌧️ Rainfall (mm)", 0, 1000, 50)
    with col2:
        temperature = st.slider("🌡️ Temperature (°C)", -10, 50, 25)
    with col3:
        soil = st.selectbox("🪨 Soil Type", ["Loamy", "Sandy", "Clay", "Red"])

    if st.button("📊 Get Crop Advice"):
        result = get_crop_advice(rainfall, temperature, soil, language)
        st.success(result)

st.markdown("---")

# 🐛 Pest Diagnosis
st.subheader("🐛 Pest Diagnosis")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        crop = st.text_input("🌾 Crop Name")
    with col2:
        symptoms = st.text_area("📝 Describe Symptoms")

    if st.button("🔍 Diagnose Pest"):
        result = get_pest_advice(crop, symptoms, language)
        st.warning(result)

st.markdown("---")

# 🌦️ Weather Alerts
st.subheader("🌦️ Weather Alerts")
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        region = st.selectbox("📍 Select Region", regions)
    with col2:
        temp = st.slider("🌡️ Temperature (°C)", -10, 50, 25, key="weather_temp_slider")

    with col3:
        humidity = st.slider("💧 Humidity (%)", 0, 100, 50)
    with col4:
        wind = st.slider("🌬️ Wind Speed (kph)", 0, 200, 10)

    if st.button("⚠️ Get Weather Alert"):
        result = get_alert(region, temp, humidity, wind, language)
        st.info(result)

st.markdown("---")

# 🏛️ Government Schemes
st.subheader("🏛️ Government Schemes")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        crop_s = st.selectbox("🌾 Crop (optional)", ["", "Cotton", "Wheat", "Rice", "Maize", "Sugarcane", "Pulses", "Oilseeds"])
    with col2:
        region_s = st.selectbox("📍 Region (optional)", [""] + regions)
    with col3:
        category_s = st.selectbox("📂 Category (optional)", ["", "Subsidy", "Loan", "Insurance", "Training", "Other"])

    if st.button("🔎 Find Schemes"):
        results = get_scheme_info(
            crop_s if crop_s else None,
            region_s if region_s else None,
            category_s if category_s else None,
            language
        )
        if results:
            for r in results:
                st.markdown(f"✅ **{r['scheme_name']}**\n> {r['description']}")
        else:
            st.info("🚫 No schemes found for the selected filters.")

st.markdown("---")

# 🗣️ Community Feed
st.subheader("🗣️ Community Feed")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Your Name")
    with col2:
        region_c = st.selectbox("📍 Your Region", regions)
    message = st.text_area("💬 Share your tip or question")

    if st.button("📢 Post to Community"):
        st.success(post_to_community(name, region_c, message, language))

    st.markdown("### 📌 Recent Messages")
    feed = view_community_feed(language=language)
    for msg in feed:
        st.markdown(f"**👤 {msg['name']} ({msg['region']})**\n> {msg['message']}")

st.markdown("---")

# 🌐 Translation Tool
st.subheader("🌐 Translate to Hindi")
with st.container():
    english_text = st.text_input("✍️ Enter English text")
    if st.button("➡️ Translate"):
        st.markdown(f"**🈶 Hindi Translation:**\n> {translate_to_hindi(english_text)}")

st.markdown("---")
st.caption("🧑‍🌾 Built to empower farmers with real-time, multilingual insights. Jai Kisaan!")
