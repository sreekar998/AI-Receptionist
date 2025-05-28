"""
Streamlit chatbot app for Multi-Agent Receptionist System.
"""
import streamlit as st
from ai_service.agents.supervisor_agent import route_to_agent

st.set_page_config(page_title="Multi-Agent Receptionist Chatbot", page_icon="🤖")
st.title("🏥 Multi-Agent Receptionist Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("How can I help you today?", "")

if st.button("Send") and user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        try:
            response = route_to_agent(user_input)
            output = response.get("output") if isinstance(response, dict) else str(response)
        except Exception as e:
            output = f"Sorry, an error occurred: {e}"
        st.session_state.chat_history.append(("bot", output))

for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Receptionist:** {msg}")
