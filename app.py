import streamlit as st
import google.generativeai as genai
import time
from google.api_core.exceptions import ResourceExhausted

# -------------------- CONFIG --------------------
GOOGLE_APIKEY = st.secrets["API_KEYS"]
genai.configure(api_key=GOOGLE_APIKEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- TITLE --------------------

# Centered chatbot name
st.markdown("""
<h1 style='text-align: center;'>🤖 Nomi </h1>
<p style='text-align: center;'>Convo? Crushed it.</p>
""", unsafe_allow_html=True)

# Clear chat button
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------- GEMINI RESPONSE FUNCTION --------------------
def gemini_response(user_input):

    # Limit memory to last 8 messages (prevents quota exhaustion)
    recent_messages = st.session_state.messages[-8:]

    history = []
    for role, message in recent_messages:
        if role == "User":
            history.append({"role": "user", "parts": [message]})
        else:
            history.append({"role": "model", "parts": [message]})

    chat = model.start_chat(history=history)

    prompt = f"""
    Reply to the user in a funny humorous, friendly tone. Add emojis to make the response more fun.
    Keep response under 120 words.

    User says: {user_input}
    """

    try:
        time.sleep(1)  # small delay to reduce rate limit issues
        response = chat.send_message(prompt)
        return response.text

    except ResourceExhausted:
        return "⚠️ Arre bhai 😭 API quota khatam ho gaya. Thoda break lete hain!"

    except Exception:
        return "⚠️ Something went wrong. Even Sagar needs chai ☕"

# -------------------- DISPLAY CHAT --------------------
for role, message in st.session_state.messages:
    with st.chat_message("user" if role == "User" else "assistant"):
        st.markdown(message)

# -------------------- USER INPUT --------------------
if user_input := st.chat_input("Type your message..."):

    st.session_state.messages.append(("User", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = gemini_response(user_input)

    st.session_state.messages.append(("Sagar", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
