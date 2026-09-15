import streamlit as st

from database import SessionLocal
from ai_query import ask_energy_question
from crud import get_business_language
from translations import t

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id

session = SessionLocal()
language = get_business_language(session, business_id)

st.title(t("ask_ai_title", language))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(text)

question = st.chat_input(t("ask_ai_chat_placeholder", language))

if question:
    st.session_state.chat_history.append(("user", question))
    with st.chat_message("user"):
        st.write(question)

    answer = ask_energy_question(session, business_id, question)

    st.session_state.chat_history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.write(answer)

session.close()
