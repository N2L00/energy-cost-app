import streamlit as st

from database import SessionLocal
from ai_query import ask_energy_question

st.set_page_config(page_title="Ask AI", page_icon="🤖")
st.title("🤖 Ask About Your Energy Costs")

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(text)

question = st.chat_input("Ask a question about your energy costs...")

if question:
    st.session_state.chat_history.append(("user", question))
    with st.chat_message("user"):
        st.write(question)

    session = SessionLocal()
    answer = ask_energy_question(session, business_id, question)
    session.close()

    st.session_state.chat_history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.write(answer)