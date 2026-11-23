import streamlit as st
from google import genai
from google.genai import types

st.title("🛡️ Cyber Safety Awareness Bot")   # <--- THIS IS st.title
st.warning("⚠️ This is an AI awareness assistant, not an official complaint portal. Never share OTPs, passwords, or bank details here. For financial fraud, call 1930 or visit cybercrime.gov.in.")
st.caption("Ask me about online scams, staying safe, or how to report cyber crime.")

rules = """
You are a helpful Cyber Safety Awareness Assistant for citizens in India.
- Explain cyber threats in simple, calm language.
- For financial fraud, always highlight the 1930 helpline and cybercrime.gov.in.
- Never ask for OTPs, passwords, or personal banking details.
"""

# Keep BOTH the client and the chat session alive in session_state
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(system_instruction=rules)
    )
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Wait for new user input
if prompt := st.chat_input("Ask a cyber safety question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Sorry, the server is busy right now. Please try again. ({e})"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)