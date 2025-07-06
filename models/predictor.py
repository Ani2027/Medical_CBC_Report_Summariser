import joblib
import numpy as np
import pandas as pd
import json
import os

# -------- CONFIG --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Points to 'Version 4/'

MODEL_PATH = os.path.join(BASE_DIR, "models", "lightgbm_disease_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
FEATURE_ENCODERS_PATH = os.path.join(BASE_DIR, "models", "feature_encoders.pkl")
RULES_PATH = os.path.join(BASE_DIR, "data", "config", "disease_rules.json")


#? Debug Statement
# print("📁 Loading rules from:", RULES_PATH)

# ------------------------

# ✅ Load components
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
feature_encoders = joblib.load(FEATURE_ENCODERS_PATH)

# ✅ Load and normalize rules
if os.path.exists(RULES_PATH):
    with open(RULES_PATH, "r") as f:
        raw_rules = json.load(f)
        disease_rules = {k.strip().lower(): v for k, v in raw_rules.items()}
else:
    disease_rules = {}

# ✅ Encode input
def encode_input(input_dict):
    encoded = {}
    for key, value in input_dict.items():
        if key in feature_encoders:
            le = feature_encoders[key]
            encoded[key] = le.transform([value])[0]
        else:
            encoded[key] = int(value)
    return pd.DataFrame([encoded])

# ✅ Predict function with normalized rule matching
def predict_diseases(input_dict, top_n=3, closeness_threshold=0.1):
    X = encode_input(input_dict)
    probs = model.predict(X)[0]
    indices = np.argsort(probs)[-top_n:][::-1]
    diseases = label_encoder.inverse_transform(indices)
    percentages = [round(probs[i] * 100, 2) for i in indices]

    results = []

    # Optional warning
    if len(percentages) >= 3:
        diff1 = abs(percentages[0] - percentages[1])
        # diff2 = abs(percentages[1] - percentages[2])
        # if diff1 < closeness_threshold * 100 and diff2 < closeness_threshold * 100:
        if diff1 < closeness_threshold * 100:
            results.append({
                "condition": "⚠️ Multiple similar likelihood conditions detected",
                "probability": "",
                "advice": "Consult your doctor for proper diagnosis.",
                "diet": "",
                "follow_up_tests": []
            })

    for disease, prob in zip(diseases, percentages):
        key = disease.strip().lower()
        rule = disease_rules.get(key, {})

        #? Debug Statements
        # if key not in disease_rules:
        #     print(f"⚠️ Warning: Disease rule not found for: '{disease}' → key used: '{key}'")
        # for k in disease_rules.keys():
        #     print(f"[{k}]")


        results.append({
            "condition": disease,
            "probability": f"{prob}%",
            "advice": rule.get("advice", "Consult your doctor for further testing."),
            "diet": rule.get("diet", "Maintain a healthy diet."),
            "follow_up_tests": rule.get("follow_up_tests", [])
        })

    return results
