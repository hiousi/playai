import streamlit as st
import ai.config as config

# session values 
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

if "openai_model" not in st.session_state:
    st.session_state.openai_model= config.OPENAI_MODEL

if "openai_temperature" not in st.session_state:
    st.session_state.openai_temperature = config.OPENAI_TEMPERATURE

if "tontub_max_comments" not in st.session_state:
    st.session_state.tontub_max_comments = config.TONTUB_MAX_COMMENTS



pg = st.navigation({
    "Apps": config.main_pages,
    "Admin" : [config.settings_page]

}) 
pg.run()

