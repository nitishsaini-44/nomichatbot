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

if "personality" not in st.session_state:
    st.session_state.personality = "Savage 😈"

# -------------------- SIDEBAR --------------------
st.sidebar.title("🎭 Choose Sagar's Personality")

personality = st.sidebar.radio(
    "Select Mode:",
    ["Savage 😈", "Friendly 😎"]
)

st.session_state.personality = personality

# Clear chat button
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------- TITLE --------------------
st.title("🤖 Sagar's Multiverse Bot 🔥")
st.caption(f"Current Mode: {st.session_state.personality}")

# -------------------- PERSONALITY PROMPTS --------------------
PERSONALITY_PROMPTS = {
    "Savage 😈": """
        You are Sagar in Savage Roast Mode.
        Roast playfully, sarcastic but NOT toxic or offensive.
        Keep it witty and funny.
    """,
    "Friendly 😎": """
        You are Sagar in Friendly Mode.
        Be chill, warm, and supportive.
    """
}

# -------------------- GEMINI RESPONSE FUNCTION --------------------
def gemini_response(user_input):

    # Limit memory to last 8 messages
    recent_messages = st.session_state.messages[-8:]

    # Convert to Gemini chat history format
    history = []
    for role, message in recent_messages:
        if role == "User":
            history.append({"role": "user", "parts": [message]})
        else:
            history.append({"role": "model", "parts": [message]})

    # Start chat with trimmed history
    chat = model.start_chat(history=history)

    prompt = f"""
    {PERSONALITY_PROMPTS[st.session_state.personality]}

    Respond in first person as Sagar.
    Keep response under 120 words.
    Use emojis appropriately.

    User says: {user_input}
    """

    try:
        time.sleep(1)  # small delay to prevent rate limit spam
        response = chat.send_message(prompt)
        return response.text

    except ResourceExhausted:
        return "⚠️ Brooooo chill 😭 API quota exhausted. Try again later."

    except Exception:
        return "⚠️ Something went wrong. Even Sagar needs coffee ☕"

# -------------------- DISPLAY CHAT --------------------
for role, message in st.session_state.messages:
    with st.chat_message("user" if role == "User" else "assistant"):
        st.markdown(message)

# -------------------- USER INPUT --------------------
if user_input := st.chat_input("Type your message..."):

    # Display user message
    st.session_state.messages.append(("User", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate reply
    reply = gemini_response(user_input)

    st.session_state.messages.append(("Sagar", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
