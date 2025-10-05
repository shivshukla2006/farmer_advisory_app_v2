import os
import joblib
from types import SimpleNamespace

# Get absolute path of models folder
BASE_DIR = os.path.dirname(__file__)

def load_model(filename):
    """
    Load a model from a .pkl file and wrap it for safe calling.
    If it's a scikit-learn model, use .predict().
    If it's a Hugging Face pipeline, call directly.
    """
    model = joblib.load(os.path.join(BASE_DIR, filename))

    def wrapper(*args, **kwargs):
        try:
            # Try sklearn .predict()
            features = args[0]
            # Ensure features is 2D if sklearn
            if not isinstance(features, list) or (len(features) > 0 and not isinstance(features[0], list)):
                features = [features]
            return model.predict(features)
        except AttributeError:
            # Likely Hugging Face pipeline
            return model(*args, **kwargs)

    # Attach original model and wrapper
    ns = SimpleNamespace()
    ns.model = model
    ns.call = wrapper
    return ns

# Load models
crop_advisory = load_model("crop_advisory_model.pkl")
pest_predictor = load_model("pest_predictor.pkl")
price_predictor = load_model("price_predictor.pkl")
translator_model = joblib.load(os.path.join(BASE_DIR, "translator_model.pkl"))
weather_alert_model = load_model("weather_alert_model.pkl")


def translate_to_hindi(text: str) -> str:
    """
    Translate English text to Hindi using translator_model.
    Adjust this depending on your translator_model implementation.
    Example for Hugging Face pipeline:
        translator_model(text)
    """
    try:
        if hasattr(translator_model, "translate"):
            return translator_model.translate(text, target_language="hi")
        elif callable(translator_model):
            # Hugging Face pipeline style
            result = translator_model(text)
            if isinstance(result, list) and len(result) > 0 and "translation_text" in result[0]:
                return result[0]["translation_text"]
            return str(result)
        else:
            return str(translator_model)
    except Exception:
        return text  # fallback to original text if translation fails
