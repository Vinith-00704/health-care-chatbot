"""
response_generator.py
Generates fully humanized, conversational, empathetic responses.
No templates. No rigid labels. Reads like a knowledgeable friend talking to you.
"""

import random

# ---------------------------------------------------------------------------
# Per-disease conversational response pools
# Each entry is a full natural-language paragraph for a given severity.
# Mild = reassuring, Moderate = concerned, Emergency = urgent.
# Placeholders: {sym} = symptom list string, {new} = newly added symptoms
# ---------------------------------------------------------------------------

RESPONSES = {

    "Flu": {
        "mild": [
            "Sounds like you've got the flu coming on — {sym} are pretty classic signs of it. Honestly, the best thing you can do right now is rest as much as possible and keep yourself hydrated. Warm fluids like ginger tea, broth, or even just hot water with lemon can really help. If your temperature spikes, paracetamol will bring it down. Most people start feeling noticeably better within 4–5 days, so try not to stress too much about it.",
            "Yeah, that combination of {sym} is very flu-like. Your body's fighting something right now, which is why everything feels so heavy. Do yourself a favour — stay home, wrap up warm, drink plenty of fluids, and let your immune system do its job. Paracetamol or ibuprofen can take the edge off the fever and body aches. Avoid going out if you can, flu spreads easily to others.",
            "Honestly? Sounds like a pretty textbook case of the flu. {sym} — your body is clearly in fight mode right now. The trick is not to fight it too hard yourself. Rest, fluids, maybe some warm soup, and paracetamol if the fever gets uncomfortable. Give it 4–6 days. If you're not improving or the fever gets very high, that's when you'd want to check in with a doctor.",
            "A bit of bad news — {sym} together really point toward the flu. The good news is most people bounce back just fine with some rest and TLC. Stay well hydrated, take paracetamol for the fever, and avoid anything physically demanding for a few days. If you've got a thermometer nearby, keep an eye on your temperature — anything above 39°C for more than two days deserves a doctor's opinion.",
        ],
        "moderate": [
            "I'm a little concerned hearing about {sym}. That's quite a few symptoms hitting at once, which is pretty typical of a more intense flu episode. You should really be resting properly right now — not just sitting at home, but genuinely in bed if possible. Paracetamol for the fever, electrolyte drinks to stay hydrated, and soft foods if you have any appetite at all. If you've had these symptoms for more than 3–4 days without improvement, please see a doctor.",
            "Okay, so {sym} all showing up together — that's your body sending a pretty strong signal. This looks like a moderate flu, and you need to take it seriously. Get proper rest, drink plenty of fluids throughout the day, and use paracetamol to manage the fever and body aches. Don't try to push through it. If things get worse — especially breathing — go to a clinic.",
        ],
    },

    "Viral Fever": {
        "mild": [
            "It sounds like you might be dealing with a viral fever. {sym} are all pretty consistent with that. Viral fevers are very common and usually pass on their own in a few days. The main thing is to stay hydrated — water, coconut water, ORS if you have it. Paracetamol will help manage the temperature. Rest as much as you can and avoid going out in the heat.",
            "Viral fevers can really knock you out, and it sounds like that's what's happening with the {sym} you're feeling. The good news is they're self-limiting, meaning your body will clear it on its own. Keep your fluid intake high, take paracetamol if your temperature is above 38.5°C, and just let yourself rest. Try to check your temperature every few hours to make sure it's not climbing too high.",
            "Sounds like a viral fever to me based on {sym}. These can come on quickly and make you feel really rough, but they usually resolve in 3–5 days. Don't push yourself — rest, hydration, and paracetamol are your best friends right now. Light foods like khichdi or rice are fine if you can manage them.",
        ],
        "moderate": [
            "Those symptoms — {sym} — suggest a viral fever that's hitting you reasonably hard. I'd strongly recommend proper bed rest, not just light rest. Keep monitoring your temperature every few hours. If it crosses 40°C or you've had a fever for more than 3 days, please don't wait — see a doctor. In the meantime, paracetamol, lots of fluids, and stay away from anything strenuous.",
            "A viral fever with {sym} can be draining and a bit worrying. Your body is clearly working hard to fight something off. Stay horizontal as much as possible, drink electrolyte drinks, and take paracetamol as directed. Do keep track of how long the fever has been going — anything lasting more than 4 days needs medical attention.",
        ],
    },

    "Common Cold": {
        "mild": [
            "Sounds like a classic common cold! {sym} — been there, done that. It's annoying but it'll pass. Steam inhalation can really help with congestion, and honey-lemon in warm water is brilliant for a sore throat. Stay warm, drink lots of fluids, and get a bit of extra sleep. You should start feeling better in 5–7 days. Saline nasal drops from the pharmacy can also really ease the stuffiness.",
            "Yeah, that sounds very much like a cold considering {sym}. Nothing too alarming here — just your classic upper respiratory bug. Drink warm fluids as often as you can, rest well, and if the sore throat is bad, gargling with warm salt water actually works wonders. Most colds are gone within a week. Zinc lozenges might help speed things along slightly.",
            "That's definitely a cold — {sym} are the tell-tale signs. Try not to stress about it; your immune system has got this one. Paracetamol can help with any discomfort, warm soups keep you hydrated and nourished, and steam inhalation helps a lot with the congestion. A week at most and you should be back to normal.",
            "Oh, sounds like you're in cold territory right now! {sym} — familiar story. Keep yourself warm and cosy, sip on warm liquids throughout the day, and try some steam inhalation for the congestion. Over-the-counter cold remedies can ease the symptoms, but honestly rest and fluids are the best medicine. You'll be right in a few days.",
        ],
        "moderate": [
            "A bad cold with {sym} can be surprisingly rough, especially if you've been feeling this way for more than a few days. Make sure you're getting genuine rest, not just resting between tasks. Warm fluids every hour or two, steam inhalation morning and night, and saline drops if the nose is very blocked. If you develop a high fever or the symptoms last more than 10 days, it might be worth checking for a sinus infection.",
        ],
    },

    "Migraine": {
        "mild": [
            "Oh, migraines are really rough — I'm sorry you're dealing with {sym} right now. The best thing you can do is find the darkest, quietest room you can and lie down. Screens are your enemy right now, phones included. A cold or warm compress on your forehead or the back of your neck can help. Ibuprofen or aspirin taken early in an attack tends to work better than waiting. If you haven't eaten, try a small snack — sometimes low blood sugar triggers or worsens migraines.",
            "Sounds like a migraine attack from what you're describing — {sym} are very characteristic. First things first: get off the screen and into a dark quiet room if possible. Painkillers work best if taken early, so if you have anything suitable, take it now rather than waiting. A cold compress, some rest, and no bright lights should help it pass. Do you know what triggered it this time?",
            "That headache with {sym} sounds like it could be a migraine. These are genuinely painful and I know they can be debilitating. Get yourself somewhere dark and quiet as quickly as you can. Stay away from strong smells, bright lights, and any noise. An over-the-counter migraine relief tablet can help if taken soon enough. Try to sleep it off if you can — sleep is often the best remedy.",
        ],
        "moderate": [
            "A migraine with {sym} that's this prolonged is something to take seriously. If it's been going on for several hours and painkillers aren't touching it, a doctor might be able to prescribe something stronger. In the meantime, dark room, cool compress, and complete quiet. Stay hydrated with small sips of water — dehydration makes it worse. Avoid coffee if you're not used to it as a remedy; it can backfire.",
            "What you're describing — {sym} — sounds like a significant migraine episode. It's hard to push through these, and honestly you shouldn't try to. Rest completely in a dark, quiet space. If this is a recurring pattern, it might be worth talking to a doctor about preventive treatments. For now, take your pain relief as soon as possible and try to sleep.",
        ],
    },

    "Food Poisoning": {
        "mild": [
            "Oof, that doesn't sound fun at all — {sym} really point toward food poisoning. The most important thing right now is keeping yourself hydrated. Your body is losing fluids and you need to replace them. Sip ORS, coconut water, or even just plain water little and often. Avoid solid food for a few hours, then start with bland things like rice, toast, or banana. Most cases clear up in 24–48 hours.",
            "I think what you might be dealing with is food poisoning based on {sym}. Did you eat anything unusual in the past few hours? Your gut is trying to expel whatever it doesn't like — frustrating, but it's actually your body doing the right thing. Stick to clear fluids for now, rest, and don't take anything to stop the vomiting unless a doctor recommends it. Your stomach needs to flush things out.",
            "Food poisoning is no joke when you're in the middle of it — {sym} is your body reacting to something it ingested. Hydration is everything right now. Keep sipping water or ORS even if you feel nauseous. Avoid dairy, fatty foods, and anything heavy. Plain crackers or rice when you feel ready. If symptoms don't ease within 24 hours or you notice blood, please see a doctor.",
        ],
        "moderate": [
            "Those symptoms — {sym} — suggest your body is dealing with a fairly significant stomach episode, possibly food poisoning. If this has been going on for more than a day, dehydration becomes a real concern. ORS is essential — please get some if you don't have it. Try to sip something every 10-15 minutes. If you're unable to keep any fluids down for more than 6-8 hours, you should go to a clinic for IV fluids.",
            "The combination of {sym} is telling me your gut is really struggling right now. This level of symptoms needs you to take hydration seriously — dehydration can creep up fast. Small sips of ORS or electrolyte drinks, rest completely, avoid all heavy food. If you feel your mouth getting very dry, you're getting dizzy, or you haven't urinated in hours, that's a sign you need medical help.",
        ],
    },

    "Heart Issue": {
        "emergency": [
            "I need you to take this seriously right now. Chest pain together with {sym} can be signs of a cardiac event, and that's not something to sit with. Please call 108 or 112 immediately, or have someone drive you to the nearest emergency room — do not drive yourself. While waiting for help, sit or lie down comfortably, loosen any tight clothing, and try to stay as calm as possible. Don't eat or drink anything.",
            "Okay, I have to be direct with you — {sym} including chest pain is a combination that needs immediate emergency care. Please don't wait to see if it gets better. Call 108 now or go to the ER. If you're alone, call someone to be with you. Sit down, don't exert yourself at all, and keep your phone with you. This is not the moment to be cautious about 'bothering' anyone.",
            "This is urgent. Chest pain and {sym} together are warning signs that your heart may be under significant stress. Get emergency help right now — call 108 or 112. While you wait, sit still, breathe slowly, and loosen any tight clothing. If you have aspirin and you're not allergic, chewing one (75–325mg) may help. But please — call for emergency help first.",
        ],
        "moderate": [
            "I don't want to alarm you, but {sym} along with chest discomfort is something I'd take seriously. Please don't ignore this. Sit down and rest right now — stop any physical activity. If the chest pain intensifies, spreads to your arm or jaw, or you feel short of breath, call 108 immediately. Even if it settles down, you should see a doctor today.",
        ],
    },

    "Snake Bite": {
        "emergency": [
            "This is an emergency and every second counts. If someone has been bitten by a snake, keep the bitten area completely still and as low as possible — below the level of the heart if you can. Remove any rings, watches, or tight clothing near the bite before swelling starts. Do NOT suck out the venom, cut the wound, or apply a tourniquet — these don't help and can cause more harm. Call 108 right now and describe the situation. Get to the nearest hospital with an emergency department immediately.",
            "A snake bite needs emergency care right away — please don't wait. Keep the person calm and still — movement speeds up venom absorption. Immobilize the affected limb as best you can. Don't apply a tourniquet or ice. Don't try to suck out the venom. If you can, note what the snake looked like — it helps doctors choose the right antivenom. Call 108 now and head to the nearest hospital.",
            "Right — this is serious. Snake bite symptoms like {sym} need immediate hospital treatment, specifically antivenom. Keep the person lying still, keep the bitten limb immobilized and below heart level, remove any jewelry near the bite site. Call emergency services or get to the ER immediately. Don't waste time on home remedies — antivenom is the only effective treatment.",
        ],
    },

    "Allergy": {
        "mild": [
            "Sounds like an allergic reaction based on {sym}. First thing — try to figure out what triggered it and remove yourself from that environment if possible. An antihistamine like cetirizine or loratadine from the pharmacy should help calm the itching and rash. Cool compresses on the skin can ease the discomfort too. Keep an eye on things — if any swelling appears around your lips, throat, or tongue, call emergency services immediately.",
            "An allergic reaction can be really uncomfortable, and {sym} are classic signs of one. The priority right now is avoiding or removing whatever triggered it. An antihistamine will help significantly — most pharmacies have them without a prescription. Don't scratch the rash as it can make it worse. Watch carefully for any signs of throat swelling or difficulty swallowing, as those would need emergency care fast.",
            "Yeah, {sym} — that's your body reacting to something it doesn't like. Allergic reactions can range from mild to serious, so pay attention to how it develops. An antihistamine is your first port of call. If you can work out what caused it, avoid it going forward. Apply calamine lotion or a cool compress for the itching. If the swelling starts involving your face, lips, or throat, call 108 immediately — that's anaphylaxis territory.",
        ],
        "emergency": [
            "If the swelling is in your throat or you're finding it hard to breathe alongside {sym}, this is a medical emergency. Call 108 right now. This can be anaphylaxis, which can close the airway very quickly. If you have an EpiPen, use it immediately. Don't wait for the symptoms to pass on their own — this needs emergency intervention now.",
        ],
    },

    "Stomach Infection": {
        "mild": [
            "That stomach upset you're describing — {sym} — sounds like a stomach infection, possibly from contaminated food or water. The most important thing is staying hydrated. Drink ORS or coconut water in small sips throughout the day. Avoid spicy, oily, or heavy food for now and stick to simple things like rice, banana, or plain toast (the BRAT diet). Most stomach infections clear up within 24–48 hours with proper rest and hydration.",
            "Stomach infections are miserable to deal with, and {sym} are telling me your gut is inflamed and irritated. Give it some rest — plain water and ORS only for a few hours, then bland foods. Probiotics (yoghurt if you can tolerate dairy, or sachets from the pharmacy) can help restore your gut bacteria. If there's blood in the stool or vomit, or you can't keep any liquids down, go to a doctor.",
            "Sounds like your stomach is having a rough time with {sym}. These infections usually pass but they need you to be patient and consistent with hydration. Small sips of water or ORS every few minutes, rest completely, and avoid anything that puts stress on your digestive system. Plain boiled rice or crackers when you're ready to try food. Two days without improvement means it's time to see a doctor.",
        ],
        "moderate": [
            "The symptoms you're describing — {sym} — suggest a stomach infection that's hit you fairly hard. If this has been going on for more than 12 hours without improvement, dehydration is a real risk. ORS sachets are essential right now — please get them from a nearby pharmacy if you haven't already. Bland food only, complete rest, and if you can't keep fluids down for 6+ hours, you need medical attention.",
        ],
    },

    "Severe Injury": {
        "emergency": [
            "This needs immediate action. If there's active bleeding from {sym}, apply firm, direct pressure with a clean cloth right now and don't let go. Keep the pressure on continuously — 10–15 minutes at least. If possible, raise the injured area above heart level. Call 108 or get to the ER immediately. Don't move the person unnecessarily in case of a spinal or neck injury. Keep them calm and warm.",
            "With {sym} indicating a serious injury, your first priority is controlling the bleeding — apply direct, firm pressure with whatever clean material you have. Don't remove an embedded object. Keep the person still, calm, and warm. Call 108 immediately. Time matters here — please don't delay seeking emergency help.",
        ],
    },

    "Critical Condition": {
        "emergency": [
            "This is a critical emergency. If someone is unconscious or unresponsive with {sym}, call 108 right now — don't wait. Check if they're breathing. If they're not breathing and have no pulse, begin CPR if you know how. If they are breathing, place them in the recovery position — on their side, so the airway stays clear. Stay on the line with emergency services and follow their instructions.",
            "I need you to call 108 immediately — what you're describing with {sym} is a life-threatening situation. Don't wait. While help is on the way: check their breathing, keep them in the recovery position if unconscious, and don't give them anything to eat or drink. If they stop breathing, start CPR only if you're trained. Stay calm and stay on the line with emergency services.",
        ],
    },

    "Dengue": {
        "mild": [
            "Based on {sym}, I'm wondering if this could be dengue fever — especially with the combination of fever, body pain, and rash. Dengue is serious but manageable if caught early. The most important thing right now: drink lots of fluids — water, coconut water, ORS. Take paracetamol for fever — NOT ibuprofen or aspirin, as they can make dengue-related bleeding worse. See a doctor soon so they can run a blood test to confirm and monitor your platelet count.",
            "The symptoms you've described — {sym} — are quite characteristic of dengue. Dengue can feel devastating in the first few days, but most people recover fully with proper care. Hydrate aggressively with water and coconut water. Paracetamol only for fever. Get to a doctor for a dengue test as soon as you can — monitoring platelet count is really important in dengue. Watch out for warning signs like bleeding gums or severe abdominal pain.",
        ],
        "moderate": [
            "Those symptoms — {sym} — are ringing dengue bells for me, and given the severity, you need a doctor today. Dengue can drop platelet counts dangerously if not monitored. Go get a blood test done — NS1 antigen test or dengue serology. In the meantime, drink fluids constantly, take paracetamol only for fever, and rest. No aspirin, no ibuprofen. If you notice any bleeding (gums, nose, skin), go to the emergency room immediately.",
        ],
    },

    "Typhoid": {
        "mild": [
            "The pattern of {sym} is concerning for typhoid fever, particularly if it's been going on for several days. Typhoid needs antibiotic treatment — you can't clear it on your own, so please see a doctor. In the meantime, drink boiled or filtered water only, eat light and easy-to-digest foods, and rest. Avoid raw food completely. If you get a test done, a Widal or typhidot test can confirm it.",
            "Based on {sym}, typhoid is a real possibility here. It's caused by contaminated food or water and needs antibiotic treatment to clear properly. Please see a doctor to get tested and get the right prescription. While you're waiting: boiled water only, light foods, rest. Don't stop antibiotics early even if you feel better — typhoid can relapse if the course isn't completed.",
        ],
        "moderate": [
            "I'm genuinely concerned about those symptoms — {sym} — especially if the fever has been around for more than 3–4 days. Typhoid fits this picture quite well. This is not something you can wait out — please see a doctor today for a blood test. Typhoid needs antibiotics to treat, and the sooner you start, the better. Stay hydrated with boiled water, eat only cooked foods, and rest completely.",
        ],
    },

    "COVID-19": {
        "mild": [
            "The combination of {sym} is something I'd associate with COVID-19, especially in the current climate. Please isolate yourself from others as soon as possible to avoid spreading it, even before getting tested. Get a rapid antigen test if you can — most pharmacies stock them. Rest, stay hydrated, and take paracetamol for fever or body aches. Check your oxygen levels if you have a pulse oximeter — anything below 94% needs a doctor's attention.",
            "Those symptoms — {sym} — are consistent with what we see in COVID-19. Whether or not you test positive, please treat this as you would COVID until you know for sure. Isolate, rest, drink plenty of fluids, and keep track of how you're feeling day by day. If you develop breathlessness, a persistent high fever, or feel very unwell, seek medical help. Let your close contacts know so they can get tested too.",
        ],
        "moderate": [
            "With {sym}, I'm thinking this could be COVID-19, and this level of symptoms needs monitoring. Please isolate immediately. Take a test if possible. Most importantly — watch your breathing carefully. If you feel any tightness in your chest, difficulty breathing, or your oxygen drops below 94% on a pulse oximeter, go to the hospital or call 108. Paracetamol for the fever, lots of fluids, and genuine rest.",
        ],
        "emergency": [
            "The breathing difficulty you're describing along with {sym} is very serious and could indicate COVID-19 pneumonia or a similar severe lung involvement. This needs emergency medical care right now. Call 108 or go to the nearest hospital immediately. Don't wait for it to improve on its own. If you have someone with you, have them go with you or call for help.",
        ],
    },

    "Anxiety": {
        "mild": [
            "It sounds like you might be going through some anxiety right now — {sym} are very common physical symptoms of anxiety, even though they can feel quite alarming. First, try to slow your breathing down deliberately — breathe in for 4 counts, hold for 4, out for 6. This activates your parasympathetic nervous system and starts to calm the physical symptoms. Try to get away from whatever is stressing you, even for a few minutes.",
            "What you're describing — {sym} — is something a lot of people experience with anxiety. Your body is in 'fight or flight' mode and producing symptoms that feel very real and uncomfortable. Try grounding yourself: name 5 things you can see, 4 you can touch, 3 you can hear. Slow breathing helps enormously. If anxiety is a recurring issue for you, speaking to a counsellor or doctor about it would be really worthwhile.",
            "Anxiety can produce surprisingly strong physical symptoms, and {sym} fit that pattern. I know it can feel frightening when your body reacts this way. Try to breathe slowly and deeply, find a calm environment, and remind yourself that these feelings will pass — they always do. Reducing caffeine, getting regular sleep, and some gentle movement can all help manage anxiety in the longer term.",
        ],
        "moderate": [
            "The symptoms you're experiencing — {sym} — sound like anxiety that's hitting you quite hard right now. This is real and it's valid, even though nothing physically dangerous is happening. Focus on your breath — slow, deliberate, deep breaths. Try to get away from whatever triggered this if you can. Once you're feeling more stable, it would be worth speaking to your GP or a mental health professional, especially if this is happening regularly.",
        ],
    },

    "Dehydration": {
        "mild": [
            "Based on {sym}, I think you might be dehydrated. This can really sneak up on you, especially in the heat or after exercise. Start drinking water or ORS right now — slowly and consistently, not all at once. Coconut water is brilliant for rehydration. Avoid caffeine and alcohol. Rest in a cool place. The headache and dizziness should improve as you rehydrate, usually within 30–60 minutes.",
            "Dehydration can make you feel absolutely rubbish — {sym} are telling me your body needs fluids urgently. Sip water or an electrolyte drink slowly over the next hour. Don't gulp it down quickly as that can upset your stomach. Some salty crackers or a banana can help your body absorb the fluids better. If you're in a hot environment, get to somewhere cool. You should start feeling better within the hour.",
            "That {sym} combination is a classic sign of dehydration. Your body is asking for water — please listen to it. Start drinking ORS or water right away. Small sips are better than big gulps if you feel nauseous. Avoid anything with caffeine. A pinch of salt and a teaspoon of sugar in water is a quick homemade ORS if you don't have sachets. Rest up and check on how you feel in 30–60 minutes.",
        ],
        "moderate": [
            "Those symptoms — {sym} — suggest moderate dehydration that needs attention soon. If you've been unable to keep fluids down, or if this has been going on for several hours, please see a doctor — you may need IV fluids. In the meantime, keep trying with ORS or water in small, frequent sips. Avoid all caffeine and alcohol. If you haven't urinated in more than 8 hours or your urine is very dark, please seek medical attention.",
        ],
    },

    "Unknown": {
        "mild": [
            "Hmm, I'm having a bit of trouble pinpointing exactly what this could be from {sym} alone. Could you tell me a bit more? For example, how long have these symptoms been going on, and did anything specific seem to trigger them? The more detail you can give me, the better I can help.",
            "I want to give you useful information, but I'm not confident enough in a diagnosis based on {sym} to point you in one specific direction. Could you describe what you're feeling in a bit more detail? Any other symptoms, even minor ones, would really help me narrow things down.",
            "Based on what you've shared — {sym} — I'm not getting a clear enough picture to be confident about what this might be. I'd genuinely recommend seeing a doctor if you're worried, as they can examine you properly. In the meantime, rest, stay hydrated, and monitor your symptoms closely. Is there anything else you can tell me about what you're experiencing?",
        ],
    },
}

# Follow-up questions — woven into naturally-sounding prompts
FOLLOWUP_PROMPTS = [
    "How long have you been feeling this way?",
    "Is this getting worse, or has it been about the same?",
    "Have you managed to take anything for it so far?",
    "Has anyone around you been sick recently with similar symptoms?",
    "Did anything seem to trigger this, or did it come on randomly?",
    "Have you eaten or drunk anything unusual in the last day or two?",
    "Any other symptoms you haven't mentioned yet, even small ones?",
    "Are you able to eat and drink normally, or is that difficult right now?",
    "Does anything make it better or worse?",
]

# Context-aware openers for follow-up turns in a session
MEMORY_OPENERS = [
    "So adding that on top of what you mentioned earlier —",
    "Together with {prev}, this is building a clearer picture.",
    "Right, so now with {sym} in the mix as well —",
    "Okay, so combining everything you've told me —",
    "Building on what we've been discussing —",
    "With all of that together now —",
]

def _fmt(symptoms: list) -> str:
    """Format a list of symptoms into natural readable text."""
    if not symptoms:
        return "the symptoms you've described"
    clean = [s.lower() for s in symptoms]
    if len(clean) == 1:
        return clean[0]
    if len(clean) == 2:
        return f"{clean[0]} and {clean[1]}"
    return ", ".join(clean[:-1]) + ", and " + clean[-1]


def _confidence_note(confidence: float) -> str:
    """Return a subtle inline note about confidence — not a badge, just natural language."""
    pct = int(confidence * 100)
    if pct >= 75:
        return ""  # High confidence — no caveat needed
    elif pct >= 50:
        return " (though I'd want you to get a proper diagnosis from a doctor to confirm this)"
    else:
        return " — though I'm not entirely certain, so please treat this as a starting point rather than a definitive answer"


def _confidence_badge(confidence: float) -> str:
    """Small visual badge still shown in UI for reference."""
    pct = int(confidence * 100)
    if pct >= 70:
        cls, lbl = "conf-high", f"~{pct}% confidence"
    elif pct >= 45:
        cls, lbl = "conf-medium", f"~{pct}% confidence"
    else:
        cls, lbl = "conf-low", f"~{pct}% confidence"
    return f'<span class="confidence-badge {cls}">{lbl}</span>'


def generate_response(
    disease: str,
    severity: str,
    all_symptoms: list,
    new_symptoms: list,
    confidence: float,
    conversation_history: list,
    original_text: str,
) -> str:
    """
    Generate a humanized, conversational, empathetic response.
    Returns an HTML string for rendering in the chat bubble.
    """
    is_first_turn = len(conversation_history) == 0
    sym_str = _fmt(all_symptoms)
    new_str = _fmt(new_symptoms) if new_symptoms else ""
    conf_note = _confidence_note(confidence)
    badge = _confidence_badge(confidence)

    # Pick severity key — map emergency diseases that only have emergency responses
    disease_pool = RESPONSES.get(disease, RESPONSES["Unknown"])

    # Determine which severity bucket to use
    if severity == "emergency" and "emergency" in disease_pool:
        sev_key = "emergency"
    elif severity == "moderate" and "moderate" in disease_pool:
        sev_key = "moderate"
    elif "mild" in disease_pool:
        sev_key = "mild"
    else:
        # Fallback: use whatever is available
        sev_key = list(disease_pool.keys())[0]

    # Pick a random response
    pool = disease_pool[sev_key]

    # Avoid repeating last response in session
    last_response_idx = None
    if conversation_history:
        last = conversation_history[-1]
        last_response_idx = last.get("response_idx")

    available = list(range(len(pool)))
    if last_response_idx is not None and len(pool) > 1:
        available = [i for i in available if i != last_response_idx]
    chosen_idx = random.choice(available)
    template = pool[chosen_idx]

    # Fill placeholders
    body = template.format(sym=sym_str, new=new_str)

    # Add subtle confidence caveat inline in body if needed
    if conf_note and disease not in ("Unknown",) and severity != "emergency":
        body = body.rstrip(".!") + conf_note + "."

    # Add memory context opener for follow-up turns
    if not is_first_turn and new_symptoms and severity != "emergency":
        prev_str = _fmt(conversation_history[-1].get("all_symptoms", []))
        opener_template = random.choice(MEMORY_OPENERS)
        opener = opener_template.format(prev=prev_str, sym=sym_str)
        body = f"{opener} {body}"

    # Add follow-up question naturally — 35% chance for non-emergency
    followup_html = ""
    show_followup = (len(all_symptoms) <= 2 or random.random() < 0.35) and severity != "emergency"
    if show_followup:
        question = random.choice(FOLLOWUP_PROMPTS)
        followup_html = f'<p class="chat-followup">{question}</p>'

    # Severity strip (tiny visual indicator, not the dominant UI element)
    severity_colors = {
        "emergency": ("🚨", "strip-emergency"),
        "moderate": ("⚠️", "strip-moderate"),
        "mild": ("💬", "strip-mild"),
    }
    icon, strip_cls = severity_colors.get(severity, ("💬", "strip-mild"))

    # Assemble final HTML — conversational bubble, not a report card
    html = f'''<div class="chat-response">
  <div class="severity-strip {strip_cls}">{icon} {badge}</div>
  <p class="chat-body">{body}</p>
  {followup_html}
</div>'''

    return html, chosen_idx