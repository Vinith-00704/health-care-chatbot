"""
symptom_extractor.py
Extracts symptoms from preprocessed tokens and accumulates them across session history.
"""

# Expanded symptom keyword dictionary
SYMPTOM_KEYWORDS = {
    "fever": [
        "fever", "high fever", "temperature", "high temperature", "feverish",
        "hot", "burning up", "running a fever", "pyrexia"
    ],
    "cough": [
        "cough", "coughing", "dry cough", "wet cough", "persistent cough",
        "coughing up", "hacking cough", "whooping"
    ],
    "headache": [
        "headache", "migraine", "head pain", "head ache", "throbbing head",
        "head hurts", "head is pounding", "pressure in head", "head pressure"
    ],
    "fatigue": [
        "fatigue", "tiredness", "weakness", "tired", "exhausted", "weak",
        "lethargic", "no energy", "drained", "worn out", "sluggish"
    ],
    "body pain": [
        "body pain", "muscle pain", "joint pain", "body ache", "aching",
        "sore body", "muscles hurt", "whole body hurts", "myalgia", "pain all over"
    ],
    "chest pain": [
        "chest pain", "chest hurts", "chest tightness", "tight chest",
        "pain in chest", "chest discomfort", "pressure on chest", "heart pain"
    ],
    "vomiting": [
        "vomiting", "vomit", "nausea", "nauseated", "nauseous", "puke", "puking",
        "throwing up", "threw up", "feeling sick", "queasy", "want to vomit"
    ],
    "dizziness": [
        "dizziness", "dizzy", "lightheaded", "light headed", "faint", "faintness",
        "vertigo", "spinning", "off balance", "unsteady", "giddy"
    ],
    "snake bite": [
        "snake bite", "snakebite", "bitten by snake", "bitten by a snake",
        "snake attacked", "snake wound", "snake venom", "bitten by serpent"
    ],
    "itching": [
        "itching", "itchy", "scratchy", "scratch", "itch", "pruritus",
        "skin itching", "feel itchy", "constant itching"
    ],
    "rash": [
        "rash", "red spots", "hives", "skin rash", "red bumps", "spot on skin",
        "welts", "urticaria", "skin eruption", "bumps on skin"
    ],
    "stomach ache": [
        "stomach ache", "belly ache", "abdominal pain", "tummy ache", "stomach pain",
        "stomach cramps", "cramping", "gut pain", "lower abdomen pain", "belly pain",
        "stomach hurts", "tummy hurts"
    ],
    "shortness of breath": [
        "shortness of breath", "breathing difficulty", "hard to breathe",
        "can't breathe", "cannot breathe", "breathless", "difficulty breathing",
        "out of breath", "labored breathing", "dyspnea", "gasping"
    ],
    "bleeding": [
        "bleeding", "blood", "cut", "blood loss", "hemorrhage", "bleeding out",
        "bleeding heavily", "wound is bleeding", "blood coming out"
    ],
    "unconscious": [
        "unconscious", "passed out", "fainted", "coma", "unresponsive",
        "blacked out", "collapsed", "lost consciousness", "not responding"
    ],
    "swelling": [
        "swelling", "swollen", "puffiness", "puffy", "inflammation",
        "inflamed", "edema", "bloating", "bloated", "swelled up"
    ],
    "sore throat": [
        "sore throat", "throat pain", "throat hurts", "painful throat",
        "difficulty swallowing", "scratchy throat", "throat infection",
        "tonsils", "pharyngitis"
    ],
    "runny nose": [
        "runny nose", "runny", "nasal discharge", "nose running",
        "stuffy nose", "nasal congestion", "congested", "blocked nose",
        "rhinorrhea", "dripping nose"
    ],
    "loss of appetite": [
        "loss of appetite", "no appetite", "not hungry", "lost appetite",
        "don't want to eat", "can't eat", "refusing food", "anorexia",
        "not eating", "reduced appetite"
    ],
    "chills": [
        "chills", "shivering", "shaking", "trembling", "cold chills",
        "rigor", "feeling cold", "goosebumps", "shivery", "cold sweats"
    ],
}

# Pre-build a flat lookup for O(1) multi-word phrase matching
_ALL_KEYWORDS: dict[str, str] = {}
for sym, kws in SYMPTOM_KEYWORDS.items():
    for kw in kws:
        _ALL_KEYWORDS[kw] = sym


def _levenshtein(a: str, b: str) -> int:
    """Compute edit distance between two strings."""
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


def extract_symptoms(preprocessed: dict, session_symptoms: list | None = None) -> list:
    """
    Extract symptoms from preprocessed text and accumulate with session history.

    Args:
        preprocessed: dict returned by preprocess_text()
        session_symptoms: list of symptoms already recorded this session

    Returns:
        Deduplicated list of all known symptoms (current + session).
    """
    text = preprocessed['original_lower']
    tokens = preprocessed['tokens']
    negated = preprocessed['negated_zones']

    detected = set()

    # --- Phase 1: Multi-word phrase matching on original text ---
    for phrase, symptom in sorted(_ALL_KEYWORDS.items(), key=lambda x: -len(x[0])):
        if phrase in text:
            # Check that main word is not negated
            phrase_main_word = phrase.split()[0]
            if phrase_main_word not in negated:
                detected.add(symptom)

    # --- Phase 2: Token-level matching + fuzzy fallback ---
    for token in tokens:
        if token in negated:
            continue
        # Direct match
        if token in _ALL_KEYWORDS:
            detected.add(_ALL_KEYWORDS[token])
            continue
        # Fuzzy match (edit distance ≤ 2, only for longer tokens to avoid false positives)
        if len(token) >= 5:
            for kw, sym in _ALL_KEYWORDS.items():
                if len(kw.split()) == 1 and abs(len(kw) - len(token)) <= 2:
                    if _levenshtein(token, kw) <= 2:
                        detected.add(sym)
                        break

    # --- Phase 3: Accumulate session symptoms ---
    all_symptoms = set(detected)
    if session_symptoms:
        all_symptoms.update(session_symptoms)

    return list(all_symptoms), list(detected)  # (all_accumulated, new_this_turn)