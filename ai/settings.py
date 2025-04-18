import streamlit as st

import ai.config as config


# Setting the title of the Streamlit application
st.title("⚙️ Settings")



# Create tabs for different settings categories
tab1, tab2 = st.tabs(["API Keys", "Turbo tuning"])


with tab1:
    st.header("API Configuration")
    
    # OpenAI API Key
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.get('openai_api_key', ''),
        help="Enter your OpenAI API key. Get it from https://platform.openai.com/account/api-keys"
    )
    if openai_key:
        st.session_state['openai_api_key'] = openai_key

    # YouTube API Key
    youtube_key = st.text_input(
        "YouTube API Key",
        type="password",
        value=st.session_state.get('youtube_api_key', ''),
        help="Enter your YouTube API key. Get it from Google Cloud Console"
    )
    if youtube_key:
        st.session_state['youtube_api_key'] = youtube_key

    # Show API status
    st.subheader("API Status")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('openai_api_key', '').startswith('sk-'):
            st.success("OpenAI API Key: Configured ✅")
        else:
            st.error("OpenAI API Key: Not Configured ❌")
    
    with col2:
        if st.session_state.get('youtube_api_key', ''):
            st.success("YouTube API Key: Configured ✅")
        else:
            st.error("YouTube API Key: Not Configured ❌")

with tab2:
    st.header("Turbo ⚡ tuning")
    
    # Model Selection
    current_model =  st.session_state.openai_model
    model_option = st.selectbox(
        'Choisir un modèle OpenAI',
        config.OPENAI_MODEL_OPTIONS,
        config.OPENAI_MODEL_OPTIONS.index(current_model) if current_model in config.OPENAI_MODEL_OPTIONS else 0,
        help="Choisir un modèle OpenAI : https://platform.openai.com/docs/models/compare",
    )
    if model_option:
        st.session_state['openai_model'] = model_option

    # Temperature Setting
    temperature = st.slider(
        'Model Temperature',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('openai_temperature', config.OPENAI_TEMPERATURE),
        step=0.1,
        help="Plus c'est haut, plus c'est créatif"
    )
    if temperature:
        st.session_state['openai_temperature'] = temperature

    # Max Comments Setting
    max_comments = st.number_input(
        'Nbre max de comments pour TonTub',
        min_value=10,
        max_value=500,
        value=st.session_state.get('tontub_max_comments', config.TONTUB_MAX_COMMENTS),
        step=10,
        help="Nombre max de comments de TonTub videos"
    )
    if max_comments:
        st.session_state['max_comments'] = max_comments

# Save Settings Button
if st.button("Enregistrer", type="primary"):
    st.success("Settings enregistrés ! ✨")
    


