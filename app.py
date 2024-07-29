import streamlit as st

# Creating a sidebar input widget for the OpenAI API key, input type is password for security
with st.sidebar:
    st.session_state.openai_api_key = st.text_input('API Key', type='password')
    "[créer une clef API](https://platform.openai.com/account/api-keys)"

pg = st.navigation([
       st.Page("ai/zutgpt.py", title="chat avec zutGPT", icon=":material/chat:"),
       st.Page("ai/flemai.py",  title="email avec FlemAI", icon=":material/mail:")
    ])
pg.run()


