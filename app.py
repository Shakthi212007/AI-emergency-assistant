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
st.set_page_config(page_title="AI Emergency Assistant", page_icon="🚨")

st.title("🚨 AI Emergency Assistant")

st.warning("⚠️ This is AI guidance. Call emergency services immediately if needed.")

st.info("""
📞 Emergency Help (India)

- 🚨 112 – National Emergency Helpline  
- 🚑 108 – Ambulance  
- 🔥 101 – Fire Service  
- 👮 100 – Police  

⚠️ Stay calm • Share location clearly • Act fast
""")

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

            # ---- SYSTEM PROMPT ----
            if language == "Tamil":
                system_prompt = """
நீங்கள் அவசர உதவி வழங்கும் AI.

பதில் எப்படி இருக்க வேண்டும்:
- மிகவும் எளிய பேசும் தமிழில் பேசவும்
- புத்தக தமிழ் பயன்படுத்தாதீர்கள்
- மக்கள் புரிந்துக்கொள்ளும் மாதிரி இருக்க வேண்டும்

விதிகள்:
1. 3–5 வரிகள் மட்டும்
2. ஒவ்வொரு வரியும் ஒரு action
3. உடனடி உதவி சொல்ல வேண்டும்
4. எப்போதும் முதல் வரி: "112க்கு உடனே call பண்ணுங்க"

உதாரணம்:
- 112க்கு call பண்ணுங்க
- அங்க இருந்து விலகுங்க
- அருகில உள்ளவங்கல help கேளுங்க
- safe இடத்துக்கு போங்க
"""
            else:
                system_prompt = f"""
You are a life-saving emergency assistant.

Rules:
- Give very short, clear instructions
- Use simple {language}
- 3 to 5 lines only
- Each line = one action
- First step must be calling emergency number
"""

            # ---- API CALL ----
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": st.session_state.user_input}
                    ]
                }
            )

            data = response.json()

            if "choices" in data:

                result = data["choices"][0]["message"]["content"]

                # ---- OPTIONAL TAMIL CLEANUP ----
                if language == "Tamil":
                    result = result.replace("அழைக்கவும்", "call பண்ணுங்க")
                    result = result.replace("உடனடியாக", "உடனே")
                    result = result.replace("தயவு செய்து", "")

                st.success("🩺 Emergency Instructions:")
                st.write(result)

                # ---- VOICE OUTPUT ----
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

