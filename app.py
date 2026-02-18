import streamlit as st
import google.generativeai as genai

# -------------------- CONFIG --------------------
GOOGLE_APIKEY = st.secrets['API_KEYS']
genai.configure(api_key=GOOGLE_APIKEY)

model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "Savage 😈"

# -------------------- PERSONALITY SELECTOR --------------------
st.sidebar.title("🎭 Choose Sagar's Personality")

personality = st.sidebar.radio(
    "Select Mode:",
    ["Savage 😈", "Friendly 😎", "Motivational 💪", "Professor 🎓"]
)

st.session_state.personality = personality

# -------------------- TITLE --------------------
st.title("🤖 Sagar's Multiverse Bot 🔥")
st.caption(f"Current Mode: {st.session_state.personality}")

# -------------------- RESPONSE FUNCTION --------------------
def gemini_response():

    conversation_history = ""
    for role, message in st.session_state.messages:
        conversation_history += f"{role}: {message}\n"

    personality_prompt = {
        "Savage 😈": """
            You are Sagar in Savage Roast Mode.
            Roast the user playfully, sarcastic but not offensive.
            Be dramatic, confident, witty.
            """,
        "Friendly 😎": """
            You are Sagar in Friendly Mode.
            Be warm, chill, supportive, humorous.
            """,
        "Motivational 💪": """
            You are Sagar in Motivational Mode.
            Be inspiring, energetic, uplifting like a life coach.
            """,
        "Professor 🎓": """
            You are Sagar in Professor Mode.
            Be clear, intelligent, slightly witty but informative.
            Explain concepts deeply but simply.
            """
    }

    prompt = f"""
    {personality_prompt[st.session_state.personality]}
    
    Respond in first person as Sagar.
    Use emojis appropriately.
    Use previous conversation context.

    Conversation so far:
    {conversation_history}

    Now respond to the latest message.
    """

    response = model.generate_content(prompt)
    return response.text

# -------------------- DISPLAY CHAT --------------------
for role, message in st.session_state.messages:
    with st.chat_message("user" if role == "User" else "assistant"):
        st.markdown(message)

# -------------------- USER INPUT --------------------
if user_input := st.chat_input("Type your message..."):

    st.session_state.messages.append(("User", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = gemini_response()
    st.session_state.messages.append(("Sagar", reply))

    with st.chat_message("assistant"):
        st.markdown(reply)
