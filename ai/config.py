
import streamlit as st



OPENAI_MODEL_OPTIONS = ['gpt-4.1-mini', 'gpt-4.1', 'o1-mini','o1','o3-mini']
OPENAI_MODEL = 'gpt-4.1-mini'
OPENAI_TEMPERATURE = 0.7

TONTUB_MAX_COMMENTS = 100


# First define the settings page
settings_page = st.Page("ai/settings.py", title='settings', icon=":material/settings:")

main_pages = [ 
    st.Page("ai/teleprompteur.py", title="TéléPrompteur", icon=":material/cognition:"),
    st.Page("ai/zutgpt.py", title="chat avec ZutGPT", icon=":material/chat:"),
    st.Page("ai/flemai.py",  title="email avec FlemAI", icon=":material/mail:"),
    st.Page("ai/tontub.py",  title="vidéo de TonTub", icon=":material/videocam:")
]





