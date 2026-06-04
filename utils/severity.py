"""
severity.py — Evaluate severity using accumulated session symptoms and raw text.
"""

# Emergency-level symptoms
EMERGENCY_SYMPTOMS = {
    "chest pain", "shortness of breath", "unconscious", "bleeding",
    "snake bite",
}

# Moderate-level symptoms
MODERATE_SYMPTOMS = {
    "fever", "vomiting", "dizziness", "stomach ache", "itching",
    "rash", "swelling", "body pain", "chills",
}

# Mild-level symptoms
MILD_SYMPTOMS = {
    "headache", "cough", "fatigue", "sore throat", "runny nose",
    "loss of appetite",
}

# Escalation phrases in raw text
ESCALATION_PHRASES = [
    "severe", "extreme", "unbearable", "can't handle", "very bad",
    "getting worse", "worsening", "emergency", "critical",
    "don't stop", "won't stop", "since days", "for days", "since weeks",
]


def check_severity(all_symptoms: list, current_symptoms: list, original_text: str) -> str:
    """
    Determine severity level using accumulated symptoms and current message.

    Args:
        all_symptoms: Full accumulated symptom list for this session
        current_symptoms: Symptoms detected in the current turn only
        original_text: Raw user text (for escalation phrases)

    Returns:
        'emergency', 'moderate', or 'mild'
    """
    text_lower = original_text.lower()
    sym_set = set(all_symptoms)

    # Emergency check — any emergency symptom present
    if sym_set & EMERGENCY_SYMPTOMS:
        return "emergency"

    # Escalation phrase check — words like "severe", "can't breathe harder"
    for phrase in ESCALATION_PHRASES:
        if phrase in text_lower:
            # If already moderate symptoms, escalate
            if sym_set & MODERATE_SYMPTOMS:
                return "emergency"
            return "moderate"

    # Moderate check — any moderate symptom (or 3+ symptoms total)
    if sym_set & MODERATE_SYMPTOMS or len(sym_set) >= 3:
        return "moderate"

    # Mild default
    return "mild"