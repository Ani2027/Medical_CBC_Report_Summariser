import json
import os

# Load interpretation rules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_FILE = os.path.join(BASE_DIR, "data", "config", "cbc_interpretation_rules.json")

with open(RULES_FILE, "r") as f:
    interpretation_rules = json.load(f)

# Human-readable labels for each CBC key
PARAM_LABELS = {
    "HGB_status": "Haemoglobin (HGB)",
    "RBC_status": "Red Blood Cells (RBC)",
    "MCV_status": "Mean Cell Volume (MCV)",
    "WBC_status": "White Blood Cells (WBC)",
    "NEUT_status": "Neutrophils (NEUT)",
    "LYM_status": "Lymphocytes (LYM)",
    "PLT_status": "Platelets (PLT)",
}


def analyze_parameters(input_dict):
    """
    Analyze CBC parameters and return a list of structured dicts:
        [{ "param": "Haemoglobin (HGB)", "status": "Low", "message": "Low hemoglobin..." }, ...]
    """
    results = []
    for key, value in input_dict.items():
        if "_status" in key:
            rule = interpretation_rules.get(key, {})
            message = rule.get(value, f"{key} = {value}")
            results.append({
                "param": PARAM_LABELS.get(key, key.replace("_status", "").upper()),
                "status": value,
                "message": message,
            })
    return results
