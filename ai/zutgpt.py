"""
    une app pour chatter avec chatGPT

"""

import streamlit as st
from openai import OpenAI




# Setting the title of the Streamlit application
st.title("💬 zutGPT")


   
st.write("Je suis plus fort qu'un chat. D'une intelligente à décorner les boeufs, je flatule de vrais réponses sur la vraie vie.")

client = OpenAI(api_key=st.session_state.openai_api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [
        {"role": "system", "content": "tu es un assistant, tu t'exprime de façon grossière. "},
        {"role": "assistant", "content": "Comment puis-je t'aider ?"}]

# Display chat messages from history on app rerun
for m in st.session_state.messages:
    if m["role"] != "system":
         st.chat_message(m["role"]).markdown(m["content"])

# React to user input
if prompt := st.chat_input("Your message"):
    if not st.session_state.openai_api_key.startswith('sk-'):
        st.warning(f"Tu as besoin d'une clef API !", icon='⚠')
    else:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                                messages=[ {"role": m["role"], "content": m["content"]} for m in st.session_state.messages],  
                                model="gpt-4o-mini", 
                                temperature=0.7,
                                stream=True
            )
            response = st.write_stream(stream)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})







