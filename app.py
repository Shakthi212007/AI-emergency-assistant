import streamlit as st
import requests
from gtts import gTTS
import io
import os

# ---- API KEY ----
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("API key not found. Please set OPENROUTER_API_KEY")
    st.stop()

# ---- UI ----
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

            if language =="tamil":
                system_prompt=""" You are a life-saving emergency assistant.
Your job:
- Respond to emergencies in simple, clear Tamil.
- Use short sentences.
- Give direct safety instructions.
- Do NOT use complex grammar or poetic Tamil.
- Always focus on actions like: call 112, move to safety, ask for help.

Rules:
1. Keep responses very short (3–6 lines max).
2. Use simple Tamil words that anyone can understand.
3. Do NOT translate word-by-word from English.
4. Always prioritize safety instructions first.
"""
            else:
                 system_prompt =f"""you are a life_saving emergency assistant .give short ,clear,step-by-step instruction
                 in simple{language}"""
                 
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
                            "content": f"You are a life-saving emergency assistant. Give short, clear, step-by-step instructions in simple {language}."
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

                # ---- 🔊 VOICE OUTPUT (STREAMLIT CLOUD FIX) ----
                tts = gTTS(text=result, lang=lang_code)

                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)

                st.audio(audio_fp, format="audio/mp3")

            else:
                st.error("API Error")
                st.write(data)

    else:
        st.error("Please enter an emergency description")
