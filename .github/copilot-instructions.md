# Copilot Instructions for Farmer Advisory App

## Project Overview
This is a modular Python application for agricultural advisory services. It provides crop recommendations, market price info, pest/disease alerts, weather updates, and translation features for farmers. Data is loaded from CSV files in `data/`, and ML models are loaded from `models/`.

## Architecture & Major Components
- **Entry Point:** `app.py` orchestrates the main workflow and integrates all modules.
- **Modules:**
  - `advisory.py`: Crop recommendations using ML model (`models/crop_advisory_model.pkl`).
  - `market.py`: Market price predictions (`models/price_predictor.pkl`).
  - `alerts.py`: Weather and pest/disease alerts (`models/weather_alert_model.pkl`, `models/pest_predictor.pkl`).
  - `community.py`: Community messaging features, uses `data/community_messages.csv`.
  - `schemes.py`: Government schemes info.
  - `translate.py`: Language translation using `models/translator_model.pkl` and `data/translation_pairs_hindi_clean.csv`.
  - `sms_ivr.py`: SMS/IVR integration (if present).
- **Config:** `config.yaml` for runtime configuration.
- **Data:** All CSVs in `data/` are loaded as pandas DataFrames.
- **Models:** All `.pkl` files in `models/` are loaded via `pickle`.

## Developer Workflows
- **Run the app:**
  ```pwsh
  python app.py
  ```
- **Dependencies:**
  - Install with:
    ```pwsh
    pip install -r requirements.txt
    ```
- **Testing:**
  - No standard test suite detected. Add tests in a `tests/` folder if needed.
- **Debugging:**
  - Use print/logging in individual modules. Main logic is in `app.py`.

## Project-Specific Patterns
- **Modular Design:** Each feature is a separate Python file. Shared data/models are loaded at module level.
- **Data Loading:** Use pandas for CSVs, pickle for models. Example:
  ```python
  import pandas as pd
  df = pd.read_csv('data/crop_recommendation_clean.csv')
  ```
- **Model Usage:**
  ```python
  import pickle
  with open('models/crop_advisory_model.pkl', 'rb') as f:
      model = pickle.load(f)
  ```
- **No web framework detected.** All logic is script-based.

## Integration Points
- **External:** SMS/IVR (see `sms_ivr.py`), translation (see `translate.py`).
- **Internal:** All modules interact via function calls in `app.py`.

## Conventions
- Keep new features as separate modules.
- Place new data in `data/`, new models in `models/`.
- Update `config.yaml` for new config options.

---
_If any section is unclear or missing, please provide feedback for improvement._
