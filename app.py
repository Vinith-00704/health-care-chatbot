from flask import Flask, render_template, request, jsonify
import uuid
import os

from utils.preprocessing import preprocess_text
from utils.symptom_extractor import extract_symptoms
from model.predict import predict_disease
from utils.severity import check_severity
from utils.response_generator import generate_response
from utils.llm_responder import call_llm_api

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nlp-healthcare-session-key-2025")

# ── SYSTEM PROMPT FOR LLM INTEGRATION ────────────────────────────────────
HEALTHCARE_SYSTEM_PROMPT = """You are a professional healthcare assistant chatbot. Your role is to provide clear, calm, and medically appropriate guidance based on user symptoms.

Communication Style:
- Use a professional, neutral, and reassuring tone
- Avoid dramatic, emotional, or exaggerated language
- Do NOT use humor, slang, or casual phrases
- Be concise and structured in your responses
- Avoid phrases like "your body is dealing with something significant" or anything vague/emotional

Medical Responsibility:
- Do NOT provide definitive diagnoses
- Clearly state that the response is informational, not a medical diagnosis
- Use phrases like:
  - "These symptoms may be associated with..."
  - "It is advisable to..."
  - "Please consult a healthcare professional if..."

Response Structure (VERY IMPORTANT):
Always follow this format:
1. Possible Causes: List 2–3 likely conditions briefly.
2. Immediate Care Suggestions: Practical, safe steps (hydration, rest, etc.).
3. When to Seek Medical Help: Clear warning signs (specific, not vague).
4. Disclaimer: Short and professional.

Safety Rules:
- If symptoms suggest urgency (e.g., severe dehydration, chest pain, unconsciousness), clearly recommend seeking immediate medical care.
- Do not express uncertainty in a casual way like "I'm not entirely sure".
- Instead say: "A proper diagnosis requires evaluation by a qualified healthcare professional".
"""
# ─────────────────────────────────────────────────────────────────────────

# In-memory session store: { session_id: { symptoms, history } }
_SESSION_STORE: dict = {}


def _get_session(session_id: str) -> dict:
    if session_id not in _SESSION_STORE:
        _SESSION_STORE[session_id] = {"symptoms": [], "history": []}
    return _SESSION_STORE[session_id]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"response": "<p>Please describe your symptoms.</p>", "session_id": session_id})

    sess = _get_session(session_id)
    prior_symptoms = sess["symptoms"]
    conversation_history = sess["history"]

    # ── NLP Pipeline ──────────────────────────────────────────
    preprocessed = preprocess_text(user_input)
    all_symptoms, new_symptoms = extract_symptoms(preprocessed, prior_symptoms)
    disease, confidence = predict_disease(all_symptoms)
    severity = check_severity(all_symptoms, new_symptoms, user_input)
    
    # ── Optional LLM Prompting Setup ─────────────────────────
    llm_context_prompt = (
        f"User Input: {user_input}\n"
        f"Identified Symptoms: {', '.join(all_symptoms) if all_symptoms else 'None'}\n"
        f"Predicted Condition: {disease} (Confidence: {confidence:.2f})\n"
        f"Calculated Severity: {severity}\n"
        "Please generate a response following the required structure."
    )
    
    # Check if Gemini key is available and get response
    import os
    if os.environ.get("GEMINI_API_KEY"):
        response_html = call_llm_api(HEALTHCARE_SYSTEM_PROMPT, llm_context_prompt, severity, confidence)
        response_idx = -1  # Placeholder since LLMs don't have static response indices
    else:
        # Fallback to Current Template-Based Generator if no API key is present
        response_html, response_idx = generate_response(
            disease=disease,
            severity=severity,
            all_symptoms=all_symptoms,
            new_symptoms=new_symptoms,
            confidence=confidence,
            conversation_history=conversation_history,
            original_text=user_input,
        )
    # ─────────────────────────────────────────────────────────

    # Persist session state
    sess["symptoms"] = all_symptoms
    sess["history"].append({
        "user": user_input,
        "disease": disease,
        "severity": severity,
        "all_symptoms": all_symptoms,
        "response_idx": response_idx,
    })

    return jsonify({
        "response": response_html,
        "session_id": session_id,
        "disease": disease,
        "severity": severity,
        "symptoms": all_symptoms,
        "confidence": round(confidence * 100, 1),
    })


@app.route("/reset_session", methods=["POST"])
def reset_session():
    session_id = request.json.get("session_id", "")
    if session_id in _SESSION_STORE:
        del _SESSION_STORE[session_id]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)