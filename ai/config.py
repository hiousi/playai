
import streamlit as st



OPENAI_MODEL_OPTIONS = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4o', 'gpt-4o-mini']
OPENAI_MODEL = 'gpt-4o-mini'
OPENAI_TEMPERATURE = 0.7

TONTUB_MAX_COMMENTS = 100


# First define the settings page
settings_page = st.Page("ai/settings.py", title='settings', icon=":material/settings:")

main_pages = [ 
    st.Page("ai/zutgpt.py", title="chat avec zutGPT", icon=":material/chat:"),
    st.Page("ai/flemai.py",  title="email avec FlemAI", icon=":material/mail:"),
    st.Page("ai/tontub.py",  title="vidéo de TonTub", icon=":material/videocam:")
]





