"""
    une app pour repondre aux emails
"""

import streamlit as st
from openai import OpenAI



# Setting the title of the Streamlit application
st.title(":material/mail: FlemAI")


st.markdown("**F**aciliter **L**'**E**nvoi et le **M**anagement d'**E**mails par **I**ntelligence **A**rtificielle.")
st.markdown(""">    Entraîné pour être poli et serviable, je ne vais pas forcement répondre à ce qu'on te demande, mais
                    je vais ajouter des fioritures sémantiques et du blabla de courtoisie.
                    Tes réponses ne servirons toujours à rien, mais au moins, elles seront très appréciés.""")


client = OpenAI(api_key=st.session_state.openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

with st.form("src_email"):
    subject = st.text_input("Objet")
    body = st.text_area("Email reçu")
    submit = st.form_submit_button("Proposer une réponse")
    gen = False

    if submit:
        if not body or not subject :
            st.warning(f"indiques sujet et email reçu !", icon='⚠')
        elif not st.session_state.openai_api_key.startswith('sk-'):
                st.warning(f"Tu as besoin d'une clef API !", icon='⚠')
        else:
            gen = True


if gen:
    st.markdown("### Réponse :")
    stream = client.chat.completions.create(
                                messages=[ {"role": "system", "content": "formule une réponse brève et utile à l'email, tu signe Pierre et montre toi très sympathique, attentionné, serviable et courtoi. tutoiement"},
                                           {"role": "user", "content": f"subject: {subject}\n  {body}" }  ],  
                                model="gpt-4o-mini", 
                                temperature=0.7,
                                stream=True
            )
    response = st.write_stream(stream)

