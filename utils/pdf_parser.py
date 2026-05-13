import fitz  # PyMuPDF
import re
import os

# Project root (two levels up from utils/)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_input_dict_from_pdf(filepath):
    text = ""

    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()

    # Save raw text for debugging (written to project root, not CWD)
    _debug_path = os.path.join(_BASE_DIR, "debug_text_output.txt")
    with open(_debug_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Clean and split into lines
    lines = text.replace('\xa0', ' ').splitlines()

    def extract_value_from_lines(keyword, after_lines=4, multiplier=1):
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                for j in range(1, after_lines + 1):
                    if i + j < len(lines):
                        try:
                            val = float(lines[i + j].strip())
                            return round(val * multiplier, 2)
                        except ValueError:
                            continue
        return None

    def classify(value, normal_range, default="Unknown"):
        if value is None:
            return default
        if value < normal_range[0]:
            return "Low"
        elif value > normal_range[1]:
            return "High"
        else:
            return "Normal"

    # Extract values
    hgb  = extract_value_from_lines("Haemoglobin")
    rbc  = extract_value_from_lines("Total RBC Count")
    mcv  = extract_value_from_lines("Mean Corpuscular Volume", after_lines=2)
    wbc  = extract_value_from_lines("Total Leucocyte Count")
    neut = extract_value_from_lines("Neutrophils")
    lym  = extract_value_from_lines("Lymphocytes")
    plt  = extract_value_from_lines("Platelet Count", multiplier=100000)

    # Compile result
    input_dict = {
        "HGB": hgb,
        "HGB_status": classify(hgb, (12.0, 16.0)),
        "RBC": rbc,
        "RBC_status": classify(rbc, (3.9, 4.8)),
        "MCV": mcv,
        "MCV_status": classify(mcv, (83.0, 101.0)),
        "WBC": wbc,
        "WBC_status": classify(wbc, (4000, 11000)),
        "NEUT": neut,
        "NEUT_status": classify(neut, (45.0, 70.0), default="Normal"),  # ✅ Fixed here
        "LYM": lym,
        "LYM_status": classify(lym, (20.0, 40.0)),
        "PLT": plt,
        "PLT_status": classify(plt, (150000, 450000)),
    }

    return input_dict
