# app.py

import streamlit as st
from backend2 import DevNovaAssistant
import pandas as pd
import speech_recognition as sr
import threading
import pyttsx3

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="NovaSense AI",
    layout="wide",
    page_icon="🤖"
)

# ---------------- LOAD BOT ----------------
@st.cache_resource
def load_bot():
    return DevNovaAssistant("university_faq_v2.csv")

bot = load_bot()

# ---------------- ASYNC TEXT-TO-SPEECH ----------------
def speak_async(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)

            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except:
            pass

    thread = threading.Thread(target=run_speech)
    thread.start()

# ---------------- THEME ----------------
theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    body {background-color: #0E1117; color: white;}
    </style>
    """, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align:center; padding: 20px;">
    <h1 style="color:#0A66C2; font-size:42px;">🤖 Customizable MultiModal Intelligent Assistant</h1>
    <p style="font-size:18px; color:gray;">Development Meets Innovation</p>
    <hr style="border:1px solid #ddd;">
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Control Panel")

# Voice toggle
speak_toggle = st.sidebar.checkbox("🔊 Enable Voice Output", value=True)

# Clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []

mode = st.sidebar.selectbox("Mode", ["FAQ", "Smart AI"])

st.sidebar.markdown("---")

# ---------------- 🎤 VOICE INPUT ----------------
st.sidebar.subheader("🎤 Voice Input")

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.sidebar.info("Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return "Sorry, could not understand."

if st.sidebar.button("🎤 Speak"):
    voice_text = get_voice_input()

    st.session_state.messages.append({
        "role": "user",
        "content": voice_text
    })

    response = bot.get_response(voice_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    if speak_toggle:
        speak_async(response)

    st.rerun()

# ---------------- ➕ ADD NEW FAQ ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("➕ Add Knowledge")

# Initialize session state
if "success_msg" not in st.session_state:
    st.session_state.success_msg = ""

# Callback function
def add_qa():
    new_q = st.session_state.new_q
    new_a = st.session_state.new_a

    if new_q and new_a:
        df = pd.read_csv("university_faq_v2.csv")

        new_row = {}
        for col in df.columns:
            if col.lower() == "question":
                new_row[col] = new_q
            elif col.lower() == "answer":
                new_row[col] = new_a
            else:
                new_row[col] = ""

        df.loc[len(df)] = new_row
        df.to_csv("university_faq_v2.csv", index=False)

        # Store success message
        st.session_state.success_msg = "✅ Added Successfully"

        # Clear fields SAFELY
        st.session_state.new_q = ""
        st.session_state.new_a = ""

        # Reload model
        st.cache_resource.clear()

# Input fields
st.sidebar.text_input("Enter Question", key="new_q")
st.sidebar.text_input("Enter Answer", key="new_a")

# Button with callback
st.sidebar.button("➕ Add Knowledge", on_click=add_qa)

# Show success message AFTER action
if st.session_state.success_msg:
    st.sidebar.success(st.session_state.success_msg)
    st.session_state.success_msg = ""

# ---------------- CHAT STYLE ----------------
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #0A66C2;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    text-align: right;
}
.chat-bubble-bot {
    background-color: #F1F1F1;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I am your intelligent assistant. How can I help you today?"
    })

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-bubble-user">
        👤 {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble-bot">
        🤖 {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("💬 Type your message here...")

if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate response
    with st.spinner("🤖 Thinking..."):
        response = bot.get_response(user_input)

    # Save response FIRST (important for UI)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Speak in parallel (FIXED)
    if speak_toggle:
        speak_async(response)

    st.rerun()