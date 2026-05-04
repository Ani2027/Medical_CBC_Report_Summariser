
# AI-Powered CBC Report Summarizer & Disease Predictor

An intelligent diagnostic system that interprets CBC test results and user symptoms to identify possible conditions, explain abnormal test parameters, recommend diets, and suggest follow-up tests — in plain, understandable language.

---

## Features

- CBC parameter explanation (rule-based)  
- ML-based disease prediction (LightGBM classifier)  
- Hybrid diagnosis: rule + model  
- Diet & 🧪 test recommendations per condition  
- Patient-friendly explanations  

---

## How It Works

1. **Input:**
   - CBC test statuses (Low, Normal, High)
   - Symptoms (Fatigue, Fever, etc.)

2. **Step 1: Rule-based CBC Analysis**  
   Each parameter interpreted based on clinical rules

3. **Step 2: Disease Prediction (ML Model)**  
   Predicts top 3 possible diseases using trained LightGBM classifier

4. **Step 3: Advice & Recommendations**  
   For each predicted condition, provides:  
   - Medical advice  
   - Diet suggestions  
   - Follow-up test list  

---

## Project Structure
 
![image](https://github.com/user-attachments/assets/807d7c66-64bf-47d2-bffa-e8df7cc08362)

---

## How to Run

Install dependencies:

```
pip install -r requirements.txt
```

Then run:

```
python app.py
```

---

## Sample Output

**CBC Interpretation Based on Status:**

    - HGB_status = Low → Low hemoglobin - could indicate anemia or nutritional deficiency.  
    - WBC_status = Low → Low WBC - may suggest viral infection.  

**Predicting Most Likely Conditions...**  

    - Condition: Iron Deficiency (Anemia) - 78.61%  
    - Advice: Low hemoglobin and RBC levels may indicate iron deficiency.  
    - Diet: Add spinach, legumes, eggs, fortified cereals to your diet.  
    - Follow-Up Tests: Serum Ferritin, Serum Iron, TIBC 
     
 

---

## 🗂️ Dataset

Covers 15+ conditions:  
- Anemia, Dengue, Malaria, Typhoid  
- Viral/Bacterial infections, Sepsis, Pancytopenia  
- Immunity issues, Nutrition deficiency, and more  

---

## ⚠️ Disclaimer

This tool is **not a diagnostic device**. It is intended for **educational and preliminary support** only. Always consult a certified physician for clinical decisions.

---

## 👨‍💻 Developed By

Built by **Aniket** and **Harshit**  
Inspired by real-world healthcare needs and diagnostic workflows
