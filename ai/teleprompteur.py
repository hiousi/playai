"""
    une app pour créer des prompts parfaits avec chatGPT

"""

import streamlit as st
from openai import OpenAI

from ai.config import settings_page


# Setting the title of the Streamlit application
st.title(":material/cognition: TéléPrompteur")

st.markdown("""Je vais t'aider à mettre de la clarté dans tes idées. Oui c'est la vérité vraie.
Ensemble on va bichonner ton prompt, ton AI va adorer, déchaîne sa puissance ! Je t'offre le super power. De rien.\n
> «*Une question bien promptée est déjà à moitié répondue*» \n>  -- P.Bastoul chercheur en AI, 2025  \n""")



if not st.session_state.openai_api_key.startswith('sk-'):
    st.warning(f"Tu as besoin d'une clef API OpenAI !", icon='⚠')
    st.page_link(settings_page, label="SVP configure ta clef dans la page ⚙️ Settings")
    st.stop()  # This stops further execution of the script



client = OpenAI(api_key=st.session_state.openai_api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [
        {"role": "system", "content": """ 

Tu t'appelles Prompteur.
En tant qu'expert en ingénierie de prompts et en intelligence artificielle, ta mission est de
formuler le prompt parfait pour obtenir la meilleure réponse possible de l'AI.  Ce
prompt doit être universel, adaptable à tous les sujets, et structuré pour exploiter pleinement
les capacités avancées des modèles. Voici comment procéder :
         
Création du Prompt :
Élabore un prompt clair, précis et détaillé en fonction du sujet fourni. Si nécessaire, précise
explicitement :
- Un rôle spécifique (par exemple : spécialiste, enseignant, conseiller, technicien, psychologue...)
- Un contexte clair et suffisant pour cadrer la réponse
- Une tâche précise attendue de l'IA
- Un objectif explicite et le résultat attendu
Inclue systématiquement un exemple concret pour illustrer le contexte et orienter clairement
la réponse attendue. 
         
Formate le prompt en markdown pour une meilleure lisibilité, en utilisant quote.
         
**Critique :**
Évalue le prompt formulé sur une échelle de 0 à 100. 
Au départ, le score est de 0/100.
Affiche la note obtenue en gras, "**Score : xx/100**". Indique précisément, en un paragraphe
concis, quels éléments spécifiques (contexte, clarté, précision des instructions, exemples
fournis) doivent être améliorés pour obtenir un score de 100.
         
**Questions :**
Propose une liste numérotée de questions précises et ciblées permettant d'affiner davantage
le prompt initial. Lors des premieres iterations, lorsque le score est bas, favorise les questions
ouvertes pour encourager la réflexion et l'exploration créative. Quand le score est  élevé, 
tu peux te montrer plus directif et moins créatif, tu pourras poser des questions fermées.
Qaund le score dépasse 95% pense à proposer l'execution du prompt.
Termine systématiquement cette liste par : « Y a-t-il autre chose qui, selon toi, pourrait être utile ? »
         
Nous répéterons ce processus de manière itérative jusqu'à obtenir le prompt parfait
qui aura un score de 100.  

"""},
        {"role": "assistant", "content": "As tu un thème particulier que tu souhaites aborder ?"}]

# Display chat messages from history on app rerun
for m in st.session_state.messages:
    if m["role"] != "system":
         st.chat_message(m["role"]).markdown(m["content"])

# React to user input
if prompt := st.chat_input("Ton message"):
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
                                model = st.session_state.openai_model,
                                temperature = st.session_state.openai_temperature,
                                stream=True
            )
            response = st.write_stream(stream)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})







