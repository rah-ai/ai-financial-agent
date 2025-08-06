# data_manager.py
import json
import streamlit as st

@st.cache_data
def load_schemes():
    """Loads scheme data from the JSON file."""
    with open('schemes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_matching_schemes(user_profile):
    """
    Finds schemes that match the user's profile based on keywords and tags.
    This is the robust, working version of the matching logic.
    """
    all_schemes = load_schemes()
    eligible_schemes = []

    # Create a comprehensive set of keywords from the user's profile
    profile_keywords = set()
    for key, value in user_profile.items():
        if isinstance(value, str) and value:
            # Add the value itself (e.g., "Business Owner") and its parts ("business", "owner")
            profile_keywords.update(value.lower().split())

    if not profile_keywords:
        return []

    for scheme_id, scheme_data in all_schemes.items():
        # Get all tags for the current scheme
        scheme_tags = set(tag.lower() for tag in scheme_data.get("tags", []))

        # Find the keywords from the user's profile that are present in the scheme's tags
        common_tags = profile_keywords.intersection(scheme_tags)

        # If there is at least one match, the scheme is eligible
        if common_tags:
            # A simple scoring logic: more matches = higher score
            score = min(len(common_tags) * 35, 100) # Capped at 100

            eligible_schemes.append({
                'id': scheme_id,
                'data': scheme_data,
                'score': score,
                'reasons': [tag.capitalize() for tag in common_tags] # Store the reasons for eligibility
            })

    # Sort the results by the highest score first
    eligible_schemes.sort(key=lambda x: x['score'], reverse=True)
    return eligible_schemes