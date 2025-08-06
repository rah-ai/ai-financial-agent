# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from localization import LANGUAGES
import data_manager
import chatbot
import ui_components

# --- Page Configuration ---
if 'lang' not in st.session_state: st.session_state.lang = 'en'
text = LANGUAGES[st.session_state.lang]

st.set_page_config(
    page_title=text['page_title'], page_icon="✨", layout="wide", initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
def initialize_session_state():
    # Set a default active_tab on the very first run
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = text['dashboard_tab']
    
    defaults = {
        'chat_history': [], 'user_profile': {}, 'recommended_schemes': [],
        'audio_to_play': None, 'light_mode': False, 'explain_scheme_id': None
    }
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value

# --- Main Application ---
def main():
    initialize_session_state()
    lang = st.session_state.lang
    text = LANGUAGES[lang]

    # --- Sidebar (Language and Theme) ---
    with st.sidebar:
        selected_lang_display = "English" if lang == "en" else "हिंदी"
        lang_options = ["English", "हिंदी"]
        new_lang_display = st.selectbox(label=text['lang_select'], options=lang_options, index=lang_options.index(selected_lang_display))
        new_lang = 'en' if new_lang_display == "English" else 'hi'
        if new_lang != lang:
            st.session_state.lang = new_lang
            st.rerun()
        st.toggle(text['theme_toggle'], key='light_mode')

    current_theme = "light" if st.session_state.light_mode else "dark"
    ui_components.apply_custom_css(current_theme)

    find_schemes_clicked = ui_components.display_profile_sidebar(lang)
    if find_schemes_clicked:
        schemes = data_manager.find_matching_schemes(st.session_state.user_profile)
        st.session_state.recommended_schemes = schemes
        st.toast(text['toast_schemes_found'], icon="🎉")
        st.session_state.active_tab = text['dashboard_tab'] # Set active tab after finding schemes

    st.title(text['main_title'])
    st.caption(text['caption'])

    # --- "Why am I eligible?" Button Logic ---
    if st.session_state.explain_scheme_id:
        explanation = chatbot.get_eligibility_explanation(st.session_state.explain_scheme_id, st.session_state.user_profile, lang)
        st.session_state.chat_history.append({'type': 'assistant', 'message': explanation})
        st.session_state.active_tab = text['chat_tab'] # Set the desired tab
        st.session_state.explain_scheme_id = None
        st.rerun() # Rerun to switch to the chat tab
    
    # --- Main Tab Menu (THE FIX IS HERE) ---
    tab_options = [text['dashboard_tab'], text['chat_tab']]
    
    # This logic now reliably finds the correct index for the menu
    try:
        default_index = tab_options.index(st.session_state.active_tab)
    except (ValueError, KeyError):
        default_index = 0

    selected = option_menu(
        menu_title=None, 
        options=tab_options, 
        icons=["grid-1x2-fill", "robot"],
        key='main_menu', # A static key helps Streamlit
        default_index=default_index, # We now control this perfectly
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#262730", "border-radius": "10px"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "font-family": "Manrope, sans-serif", "font-weight": "bold", "color": "#aaa", "text-align": "center", "margin":"0px", "--hover-color": "#3a3b44"},
            "nav-link-selected": {"background-color": "#ef4444", "color": "white"},
        }
    )

    # If the user clicks a different tab, update the state and rerun once
    if selected != st.session_state.active_tab:
        st.session_state.active_tab = selected
        st.rerun()

    # --- Display content based on the reliable active_tab state ---
    if st.session_state.active_tab == text['dashboard_tab']:
        st.header(text['dashboard_header'])
        st.write(text['dashboard_subheader'])
        st.divider()
        if st.session_state.recommended_schemes:
            cols = st.columns(2 if len(st.session_state.recommended_schemes) > 1 else 1)
            for i, scheme in enumerate(st.session_state.recommended_schemes):
                with cols[i % 2]: ui_components.display_scheme_card(scheme, lang)
        else:
            st.info(text['dashboard_info'])
    
    elif st.session_state.active_tab == text['chat_tab']:
        st.header(text['chat_header'])
        ui_components.display_chat_history()
        if st.session_state.chat_history and st.session_state.chat_history[-1]['type'] == 'user':
            with st.chat_message("assistant", avatar="assistant"):
                with st.spinner("Bot is thinking..."):
                    response = chatbot.get_bot_response(st.session_state.chat_history[-1]['message'], st.session_state.user_profile, lang)
                    st.session_state.chat_history.append({'type': 'assistant', 'message': response['text']})
                    audio_bytes = ui_components.text_to_audio(response['text'], lang)
                    if audio_bytes: st.session_state.audio_to_play = audio_bytes
                    if response.get("action") == "calculate_schemes":
                        schemes = data_manager.find_matching_schemes(st.session_state.user_profile)
                        st.session_state.recommended_schemes = schemes
                        st.toast(text['toast_schemes_updated'], icon="✅")
                    st.rerun()
        text_input = st.chat_input(text['chat_input_prompt'])
        st.divider()
        voice_input = ui_components.voice_input_ui(lang, text)
        user_input = text_input or voice_input
        if user_input:
            st.session_state.chat_history.append({'type': 'user', 'message': user_input})
            st.rerun()

    if st.session_state.get('audio_to_play'):
        st.audio(st.session_state.audio_to_play, autoplay=True)
        st.session_state.audio_to_play = None

if __name__ == "__main__":
    main()
