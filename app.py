import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import requests
import os

translator = Translator()
API_KEY = "fa4d9b9acdd142cb4b745c54244caf83"

# ---------- Voice Functions ----------
def listen_telugu():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 మాట్లాడండి...")
        audio = r.listen(source)
        return r.recognize_google(audio, language="te-IN")

def speak_telugu(text):
    tts = gTTS(text=text, lang="te")
    tts.save("reply.mp3")
    os.system("start reply.mp3")

def te_to_en(text):
    return translator.translate(text, src="te", dest="en").text

def en_to_te(text):
    return translator.translate(text, src="en", dest="te").text

# ---------- Weather ----------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    return f"{city} లో ఉష్ణోగ్రత {data['main']['temp']}°C, వాతావరణం {data['weather'][0]['description']}"

# ---------- Farming Logic ----------
def farming_bot(q):
    q = q.lower()
    if "crop" in q:
        return "ఈ కాలంలో వరి, మక్క, పత్తి మంచి పంటలు"
    if "fertilizer" in q:
        return "సేంద్రియ ఎరువులు మరియు NPK సరైనవి"
    if "pest" in q:
        return "నిమ్మ నూనె సహజ కీటకనాశిని"
    if "irrigation" in q:
        return "డ్రిప్ సాగు నీటిని ఆదా చేస్తుంది"
    return "వ్యవసాయం గురించి అడగండి"

# ---------- UI ----------
st.set_page_config(page_title="Raitu Mitra", layout="centered")

menu = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🌦 Weather Assistant",
    "🌾 Farming Assistant",
    "🤖 Ask Anything"
])

# ---------- Screen 1 ----------
if menu == "🏠 Home":
    st.image("assets/logo.jpg", width=300)
    st.markdown("## 🌾 Raitu Mitra")
    st.markdown("### Digital Farmer’s Friend")
    st.success("Continue from the sidebar")

# ---------- Screen 2 ----------
elif menu == "🌦 Weather Assistant":
    st.header("🌦️ వాతావరణ సహాయకుడు")
    city = st.text_input("నగరం పేరు")
    if st.button("🎤 మాట్లాడండి"):
        telugu = listen_telugu()
        eng = te_to_en(telugu)
        weather = get_weather(city)
        reply = en_to_te(weather)
        st.success(reply)
        speak_telugu(reply)

# ---------- Screen 3 ----------
elif menu == "🌾 Farming Assistant":
    st.header("🌾 వ్యవసాయ సహాయకుడు")
    if st.button("🎤 ప్రశ్న అడగండి"):
        telugu = listen_telugu()
        eng = te_to_en(telugu)
        ans = farming_bot(eng)
        tel_ans = en_to_te(ans)
        st.success(tel_ans)
        speak_telugu(tel_ans)

# ---------- Screen 4 ----------
elif menu == "🤖 Ask Anything":
    st.header("🤖 రైతు సందేహాలు")
    if st.button("🎤 మాట్లాడండి"):
        telugu = listen_telugu()
        eng = te_to_en(telugu)
        reply = en_to_te(farming_bot(eng))
        st.success(reply)
        speak_telugu(reply)
