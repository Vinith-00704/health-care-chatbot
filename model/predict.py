"""
predict.py — MLP neural network prediction with confidence scores.
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(model_path)

FEATURES = [
    "fever", "cough", "headache", "fatigue",
    "body pain", "chest pain", "vomiting", "dizziness",
    "snake bite", "itching", "rash", "stomach ache",
    "shortness of breath", "bleeding", "unconscious", "swelling",
    "sore throat", "runny nose", "loss of appetite", "chills"
]


def predict_disease(symptoms: list) -> tuple[str, float]:
    """
    Predict disease from a list of symptoms using the MLP neural network.

    Args:
        symptoms: List of symptom strings (from all accumulated session symptoms)

    Returns:
        Tuple of (disease_name, confidence_score 0.0–1.0)
    """
    if not symptoms:
        return "Unknown", 0.0

    input_data = [0] * len(FEATURES)
    for symptom in symptoms:
        if symptom in FEATURES:
            index = FEATURES.index(symptom)
            input_data[index] = 1

    # If no symptoms matched the features, return unknown
    if sum(input_data) == 0:
        return "Unknown", 0.0

    input_df = pd.DataFrame([input_data], columns=FEATURES)
    prediction = model.predict(input_df)[0]

    # Get probability confidence if model supports it
    try:
        proba = model.predict_proba(input_df)[0]
        confidence = float(max(proba))
    except AttributeError:
        confidence = 0.75  # Fallback if model has no predict_proba

    return prediction, confidence