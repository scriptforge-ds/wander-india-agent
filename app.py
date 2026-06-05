import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="WanderIndia",
    page_icon="🏕️",
    layout="centered"
)

st.title("WanderIndia")
st.caption("Your budget travel planning companion for India")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# Render existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Hey! I'm your WanderIndia travel companion.\n\n"
            "Tell me what kind of trip you're dreaming of — a trek in the Himalayas, "
            "a road trip through Rajasthan, camping in Coorg, or a beach escape in Goa?\n\n"
            "I'll suggest the best places based on weather, crowd levels, and your budget. "
            "Just tell me:\n"
            "- 📍 Where you're starting from\n"
            "- 📅 When you want to travel\n"
            "- 💰 Your total budget (in ₹)\n"
            "- 👥 Who's travelling"
        )

# Chat input
user_input = st.chat_input("E.g. 5 day trek from Bangalore in October, budget ₹8000...")

if user_input:
    # Add user_input message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Render user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            from agent.orchestrator import get_response
            reply = get_response(st.session_state.messages)
            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })