import streamlit as st
import requests
from gtts import gTTS
import os

# ---------------- API KEY ----------------
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("API key not found. Set OPENROUTER_API_KEY in secrets/environment.")
    st.stop()

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="AI Emergency Assistant", page_icon="🚨")

st.title("🚨 AI Emergency Assistant")
st.warning("⚠️ This is AI guidance only. Call 112 immediately in real emergencies.")
st.info("📞 Emergency Number: 112")

# ---------------- SESSION STATE ----------------
if "response" not in st.session_state:
    st.session_state.response = ""

# STEP 1: PANIC MODE STATE
if "panic_mode" not in st.session_state:
    st.session_state.panic_mode = False

# ---------------- AI FUNCTION ----------------
def get_help(emergency_type):
    prompt = f"""
    You are an emergency response assistant.

    Situation: {emergency_type}

    Give response in STRICT format:
    1. Immediate Safety Action
    2. What to do next
    3. When to call emergency (112)

    Keep it short, clear, and step-by-step.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except:
        return "⚠️ Error. Immediately call 112 and stay safe."

# ---------------- STEP 2: PANIC BUTTONS ----------------
st.subheader("🚨 Emergency Control")

if st.button("🔴 ACTIVATE PANIC MODE"):
    st.session_state.panic_mode = True

if st.button("🟢 EXIT PANIC MODE"):
    st.session_state.panic_mode = False

# ---------------- PANIC MODE SCREEN ----------------
if st.session_state.panic_mode:
    st.error("🚨 PANIC MODE ACTIVE 🚨")

    st.subheader("⚠️ Stay calm and follow instructions")

    panic_help = get_help("User is in panic emergency situation. Provide urgent guidance.")

    st.subheader("🧠 Instant AI Guidance")
    st.write(panic_help)

    # Voice output
    try:
        tts = gTTS(panic_help, lang="en")
        tts.save("panic.mp3")
        audio_file = open("panic.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    except:
        st.warning("Voice not available, text shown above.")

    st.stop()

# ---------------- NORMAL MODE ----------------
st.subheader("Quick Emergency Help")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔥 Fire"):
        st.session_state.response = get_help("Fire accident in home or building")

with col2:
    if st.button("🚑 Medical"):
        st.session_state.response = get_help("Medical emergency, person unconscious or injured")

with col3:
    if st.button("🚗 Accident"):
        st.session_state.response = get_help("Road accident emergency situation")

# ---------------- CUSTOM INPUT ----------------
st.subheader("Or Describe Emergency")
user_input = st.text_input("Type your emergency here:")

if st.button("Get Help"):
    if user_input.strip():
        st.session_state.response = get_help(user_input)

# ---------------- OUTPUT ----------------
if st.session_state.response:
    st.subheader("🧠 AI Guidance")
    st.write(st.session_state.response)

    # Voice output
    try:
        tts = gTTS(st.session_state.response, lang="en")
        tts.save("emergency.mp3")
        audio_file = open("emergency.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    except:
        st.warning("Voice output failed, but text is available.")
             
