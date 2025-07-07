import streamlit as st
import google.generativeai as genai
import os

# --- Config ---
GOOGLE_API_KEY = st.secrets['API_KEYS'] 
genai.configure(api_key=GOOGLE_API_KEY)

# --- Initialize Gemini-2.5-flash Model ---
model = genai.GenerativeModel(model_name="gemini-2.5-flash")  

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Get Gemini Response ---
def get_gemini_response(user_message):
    prompt = f"""Reply to the user in a funny humorous, friendly tone. Add emojis to make the response more fun.
    User: {user_message}"""
    response = model.generate_content(prompt)
    return response.text

# --- UI ---
st.title(f"🤖 Nomi 🤝")
st.markdown("Convo 💬✨? Crushed it 🤜🏻💥.")

# Chat input
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

# Handle input and get response
if submitted and user_input:
    st.session_state.messages.append(("user", user_input))
    bot_reply = get_gemini_response(user_input)
    st.session_state.messages.append(("bot", bot_reply))

# Display chat history
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")

