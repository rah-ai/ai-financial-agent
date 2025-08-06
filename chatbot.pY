# chatbot.py
from localization import LANGUAGES
import data_manager

def get_bot_response(user_input, user_profile, lang='en'):
    user_input_lower = user_input.lower()
    text = LANGUAGES[lang]
    
    # Intent Detection
    if any(keyword in user_input_lower for keyword in ["namaste", "hello", "hi", "नमस्ते", "हैलो"]):
        intent = "greeting"
    elif any(keyword in user_input_lower for keyword in ["kisan", "farmer", "kheti", "agriculture", "किसान", "खेती"]):
        intent = "inform_occupation"; entities = {"occupation": "farmer"}
    elif any(keyword in user_input_lower for keyword in ["student", "padhai", "college", "scholarship", "छात्र", "पढ़ाई"]):
        intent = "inform_occupation"; entities = {"occupation": "student"}
    elif any(keyword in user_input_lower for keyword in ["business", "vyapar", "loan", "startup", "व्यापार", "लोन"]):
        intent = "inform_need"; entities = {"need": "business loan"}
    elif any(keyword in user_input_lower for keyword in ["scheme", "yojana", "show schemes", "योजना", "योजनाएं"]):
        intent = "request_schemes"
    else:
        intent = "unknown"
    
    # Response Generation
    if intent == "greeting":
        return {"text": text['greeting_response']}
    elif intent == "inform_occupation":
        occupation = entities.get("occupation")
        user_profile["occupation"] = occupation
        return {"text": text['occupation_response'].format(occupation=occupation)}
    elif intent == "inform_need":
        need = entities.get("need")
        user_profile["need"] = need
        return {"text": text['need_response'].format(need=need)}
    elif intent == "request_schemes":
        return {"text": text['request_schemes_response'], "action": "calculate_schemes"}
    else: # Default/Unknown intent
        return {"text": text['unknown_response']}

def get_eligibility_explanation(scheme_id, user_profile, lang='en'):
    text = LANGUAGES[lang]
    all_schemes = data_manager.load_schemes()
    scheme_data = all_schemes.get(scheme_id)

    if not scheme_data:
        return "Sorry, I could not find that scheme."

    profile_keywords = set()
    for value in user_profile.values():
        if isinstance(value, str):
            profile_keywords.update(value.lower().split())

    scheme_tags = set(tag.lower() for tag in scheme_data.get("tags", []))
    
    matching_reasons = profile_keywords.intersection(scheme_tags)
    
    if not matching_reasons:
        return f"I couldn't find a specific reason for {scheme_data['name'][lang]} in your profile, but it is generally for people interested in {scheme_data['category']}."

    reasons_str = ", ".join(list(matching_reasons))
    
    return text['eligibility_explanation'].format(
        scheme_name=scheme_data['name'][lang],
        reasons=reasons_str
    )