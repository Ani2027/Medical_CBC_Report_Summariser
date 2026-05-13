import os
import sys
import traceback
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.urls import reverse
from .forms import UploadPDFForm

# Step 1: Ensure the project root is on sys.path for model/utils imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Step 2: Import model logic
from models.predictor import predict_diseases
from utils.analyze_parameters import analyze_parameters
from utils.pdf_parser import extract_input_dict_from_pdf


# 🧾 Upload PDF view
def upload_pdf(request):
    print("📥 upload_pdf() view triggered")

    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            file_path = default_storage.save(f'reports/{pdf_file.name}', pdf_file)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            try:
                input_dict = extract_input_dict_from_pdf(full_path)
                print("🔬 Raw Lab Values from PDF:", input_dict)

                # Save to session and redirect to symptom input
                request.session['input_dict'] = input_dict
                return redirect(reverse("symptom_input"))

            except Exception as e:
                print("❌ Exception occurred:", str(e))
                traceback.print_exc()
                return render(request, 'predictor/error.html', {'error': str(e)})

        else:
            print("❌ Form is invalid. Errors:", form.errors)

    form = UploadPDFForm()
    return render(request, 'predictor/upload.html', {'form': form})


# 📄 Symptom Input View
SYMPTOM_FIELDS = [
    "Fatigue", "Dizziness", "Paleness", "Shortness_of_breath", "Tingling",
    "Bleeding_tendency", "Muscle_weakness", "Fever", "Chills",
    "Nausea", "Swelling", "Chest_discomfort"
]

def symptom_input(request):
    input_dict = request.session.get("input_dict")
    if not input_dict:
        return redirect("upload_pdf")  # fallback if session expired

    if request.method == "POST":
        for symptom in SYMPTOM_FIELDS:
            input_dict[symptom] = 1 if request.POST.get(symptom) == 'on' else 0


        # Final prediction
        cbc_explanations = analyze_parameters(input_dict)
        results = predict_diseases(input_dict)

        return render(request, "predictor/success.html", {
            "input_dict": input_dict,
            "cbc_explanations": cbc_explanations,
            "results": results,
            "symptom_keys": SYMPTOM_FIELDS  # 👈 Add this line
        })


    return render(request, "predictor/symptom_input.html", {
        "symptoms": SYMPTOM_FIELDS
    })


# ℹ️ Static pages
def about(request):
    return render(request, 'predictor/about.html')

def contact(request):
    return render(request, 'predictor/contact.html')
