TEST_NAME_MAP = {
    # Core CBC Parameters
    "Haemoglobin": "HGB",
    "Hemoglobin": "HGB",
    "HGB": "HGB",

    "Total Leucocyte Count": "WBC",
    "Total Leukocyte Count": "WBC",
    "White Blood Cells": "WBC",
    "WBC": "WBC",
    "TLC": "WBC",

    "Red Blood Cell Count": "RBC",
    "RBC Count": "RBC",
    "RBC": "RBC",

    "Mean Corpuscular Volume": "MCV",
    "MCV (Mean Corpuscular Volume)": "MCV",
    "Mean Corpuscular Volume (MCV)": "MCV",
    "MCV": "MCV",

    "Platelet Count": "PLT",
    "Platelet": "PLT",
    "PLT": "PLT",
    "Thrombocyte Count": "PLT",

    "Neutrophils": "NEUTp",
    "Neutrophil %": "NEUTp",
    "NEUT %": "NEUTp",
    "NEU%": "NEUTp",
    "NEUT": "NEUTp",

    "Lymphocytes": "LYMp",
    "Lymphocyte %": "LYMp",
    "LYMPH %": "LYMp",
    "LYMP": "LYMp",
    "LYM%": "LYMp",

    "Hb": "HGB",
    "W.B.C.": "WBC",
    "R.B.C.": "RBC",
    "Total WBC": "WBC",
    "Total RBC": "RBC",

    "CBC": "CBC",
    "Complete Blood Count": "CBC"
}

def normalize_test_name(name):
    return TEST_NAME_MAP.get(name.strip().replace(":", "").replace(".", ""), name.strip())
