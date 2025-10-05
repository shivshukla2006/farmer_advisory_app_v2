import joblib
import os

MODEL_PATH = "models/translator_model.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# 🌐 Translate English to Hindi
def translate_to_hindi(english_text):
    if model:
        return model.predict([english_text])[0]
    else:
        return "अनुवाद उपलब्ध नहीं है (model missing)"