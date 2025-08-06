# ui_components.py
import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text
import io
from localization import LANGUAGES

# This function is unchanged and preserves your UI
def apply_custom_css(theme):
    css = """
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes background_pan { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes avatar_glow { 0% { box-shadow: 0 0 5px #00aaff, 0 0 10px #00aaff; } 50% { box-shadow: 0 0 20px #667eea, 0 0 30px #667eea; } 100% { box-shadow: 0 0 5px #00aaff, 0 0 10px #00aaff; } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
        .stApp { font-family: 'Manrope', sans-serif; }
        h1, h2, h3 { font-family: 'Orbitron', sans-serif; }
        h1 { font-weight: 900; text-align: center; animation: fadeIn 1s ease-out forwards; }
        div[data-testid="chatAvatarIcon-assistant"] > div { background: radial-gradient(circle, #667eea 0%, #0f0c29 70%); border: 2px solid #667eea; animation: avatar_glow 3s linear infinite; }
        div[data-testid="chatAvatarIcon-assistant"] > div > svg { display: none; }
        .stChatMessage { animation: slideIn 0.5s ease-out forwards; }
        div[data-testid="stContainer"][border=true] { border-radius: 20px; backdrop-filter: blur(15px); transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.5s ease; transform-style: preserve-3d; animation: fadeIn 1s ease-out forwards; opacity: 0; animation-delay: 0.2s; }
        @media (min-width: 768px) { div[data-testid="stContainer"][border=true]:hover { transform: perspective(1200px) rotateY(15deg) rotateX(5deg) scale(1.08); box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 30px #667eea; } }
    """
    if theme == "light":
        theme_css = """
            .stApp { background: linear-gradient(45deg, #e0eafc, #cfdef3); }
            body, .stApp, h1, h2, h3, p, label, div[data-testid="stMarkdownContainer"], .st-emotion-cache-16txtl3 { color: #1a1a2e !important; }
            div[data-testid="stContainer"][border=true] { background-color: rgba(255, 255, 255, 0.7); border-color: rgba(0,0,0,0.1); }
            .st-emotion-cache-16txtl3 { background-color: rgba(255,255,255,0.4); }
        """
    else:  # Dark theme
        theme_css = """
            .stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #004e92); background-size: 400% 400%; animation: background_pan 15s ease-in-out infinite; }
            body, .stApp, h1, h2, h3, p, label, div[data-testid="stMarkdownContainer"], .st-emotion-cache-16txtl3 { color: #ffffff !important; }
            div[data-testid="stContainer"][border=true] { background-color: rgba(20, 25, 60, 0.6); border-color: rgba(102, 126, 234, 0.5); }
            .st-emotion-cache-16txtl3 { background-color: rgba(0,0,0,0.4); }
        """
    st.markdown(f"<style>{css}{theme_css}</style>", unsafe_allow_html=True)

# --- All other functions are unchanged ---
def text_to_audio(text, lang='en'):
    try:
        tts_lang = 'en-IN' if lang == 'en' else lang
        audio_bytes = io.BytesIO()
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e: return None

def voice_input_ui(lang, text):
    st.markdown(f"<h3 style='text-align: center;'>{text.get('voice_prompt_header', 'Or Ask With Your Voice')}</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        stt_lang = 'en-IN' if lang == 'en' else 'hi-IN'
        speech_text = speech_to_text(language=stt_lang, key=f'speech_input_{lang}')
    return speech_text

def display_profile_sidebar(lang):
    text = LANGUAGES[lang]
    with st.sidebar:
        st.header(text['sidebar_header'])
        st.markdown(text['sidebar_subheader'])
        st.subheader(text['basic_info'])
        st.session_state.user_profile['name'] = st.text_input(text['full_name'], st.session_state.user_profile.get('name', ''))
        st.session_state.user_profile['age'] = st.number_input(text['age'], 1, 120, st.session_state.user_profile.get('age', 25))
        st.session_state.user_profile['gender'] = st.selectbox(text['gender'], [text['male'], text['female'], text['other']])
        all_states_and_uts = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"]
        st.session_state.user_profile['state'] = st.selectbox(text['state'], all_states_and_uts)
        st.session_state.user_profile['category'] = st.selectbox(text['category'], ["General", "OBC", "SC", "ST"])
        st.subheader(text['economic_profile'])
        st.session_state.user_profile['income'] = st.number_input(text['income'], value=200000, step=10000)
        
        ### THIS IS THE ONLY CHANGE: "Salaried" has been added ###
        occupations = ["Farmer", "Student", "Business Owner", "Salaried", "Unemployed", "Other"]
        st.session_state.user_profile['occupation'] = st.selectbox(text['occupation'], occupations)
        
        if st.button(text['find_schemes_button'], use_container_width=True):
            return True
    return False

# --- All other functions are unchanged ---
def display_scheme_card(scheme, lang):
    text = LANGUAGES[lang]
    data = scheme['data']
    with st.container(border=True):
        st.subheader(data['name'][lang])
        st.markdown(f"**{text['benefit']}:** {data['benefit']} | **{text['match_score']}:** `{scheme['score']}%`")
        st.write(data['description'][lang])
        if st.button(text['explain_eligibility'], key=f"explain_{scheme['id']}", use_container_width=True):
            st.session_state.explain_scheme_id = scheme['id']
        col1, col2 = st.columns(2)
        with col1: st.link_button(text['apply_now'], data['application_link'], use_container_width=True)
        with col2: st.link_button(text['call_helpline'], data['contact_link'], use_container_width=True)

def display_chat_history():
    for chat in st.session_state.chat_history:
        avatar = "👤" if chat['type'] == 'user' else "assistant"
        with st.chat_message(name=chat['type'], avatar=avatar):
            st.write(chat['message'])
