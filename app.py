import streamlit as st
import requests
from gtts import gTTS
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    st.error("API key not found.please set OPENROUTER_API_KEY")
    st.stop()
#UI    
st.title("🚨 AI Emergency Assistant")
st.warning("⚠️ This is AI guidance. Call emergency services if needed.")
st.info("📞 Emergency Number: 112")

# ---- LANGUAGE SELECT ----
language = st.selectbox("🌍 Select Language", ["English", "Tamil", "Hindi"])

lang_code = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi"
}[language]

# ---- SESSION STATE ----
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ---- QUICK BUTTONS ----
col1, col2, col3 = st.columns(3)

if col1.button("🔥 Fire"):
    st.session_state.user_input = "fire accident"

if col2.button("🩸 Injury"):
    st.session_state.user_input = "severe bleeding injury"

if col3.button("💓 Heart"):
    st.session_state.user_input = "person unconscious not breathing"

# ---- TEXT INPUT ----
text = st.text_input("Describe your emergency:", value=st.session_state.user_input)
st.session_state.user_input = text

# ---- GET HELP ----
if st.button("Get help"):
    if st.session_state.user_input.strip():

        with st.spinner("Getting help..."):

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are an emergency assistant. Give short, clear, step-by-step instructions in {language}."
                        },
                        {
                            "role": "user",
                            "content": st.session_state.user_input
                        }
                    ]
                }
            )

            data = response.json()

            if "choices" in data:
                result = data["choices"][0]["message"]["content"]

                st.success("🩺 Emergency Instructions:")
                st.write(result)

                # 🔊 VOICE OUTPUT
                tts = gTTS(text=result, lang=lang_code)
                tts.save("output.mp3")
                os.system("start output.mp3")  # Windows

            else:
                st.error("API Error")
                st.write(data)

    else:
        st.error("Please enter an emergency description")
