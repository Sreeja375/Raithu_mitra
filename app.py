
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import requests
import os
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Raitu Mitra", layout="centered")

translator = Translator()
WEATHER_API_KEY = "fa4d9b9acdd142cb4b745c54244caf83"

# ---------------- VOICE FUNCTIONS ----------------
def listen_telugu():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 మాట్లాడండి...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="te-IN")
            return text
        except:
            return "క్షమించండి, మళ్లీ ప్రయత్నించండి"

def speak_telugu(text):
    tts = gTTS(text=text, lang="te")
    tts.save("reply.mp3")
    os.system("start reply.mp3")  # Windows
    time.sleep(2)

def te_to_en(text):
    return translator.translate(text, src="te", dest="en").text

def en_to_te(text):
    return translator.translate(text, src="en", dest="te").text

# ---------------- WEATHER ----------------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        return "నగరం కనుగొనబడలేదు"

    return f"""
{city} లో:
ఉష్ణోగ్రత {data['main']['temp']}°C
ఆర్ద్రత {data['main']['humidity']}%
వాతావరణం {data['weather'][0]['description']}
"""

# ---------------- FARMING BOT ----------------
def farming_bot(q):
    q = q.lower()
    if "crop" in q:
        return "ఈ కాలంలో వరి, మక్క మరియు పత్తి మంచి పంటలు"
    elif "fertilizer" in q:
        return "సేంద్రియ ఎరువులు మరియు NPK సరైనవి"
    elif "pest" in q:
        return "నిమ్మ నూనె సహజ కీటకనాశిని"
    elif "irrigation" in q:
        return "డ్రిప్ సాగు నీటిని ఆదా చేస్తుంది"
    elif "weather" in q:
        return "వాతావరణ వివరాల కోసం వాతావరణ విభాగాన్ని ఉపయోగించండి"
    else:
        return "వ్యవసాయం లేదా వాతావరణం గురించి అడగండి"

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📱 స్క్రీన్ ఎంచుకోండి",
    ["🏠 Home", "🌦 Weather", "🌾 Farming", "🤖 Ask Anything"]
)

# ---------------- SCREEN 1 : HOME ----------------
if menu == "🏠 Home":
    st.image("assets/logo.jpeg", width=300)
    st.markdown("## 🌾 Raitu Mitra")
    st.markdown("### Digital Farmer’s Friend")
    st.success("ఎడమ వైపు మెనూ ద్వారా కొనసాగండి")

# ---------------- SCREEN 2 : WEATHER ----------------
elif menu == "🌦 Weather":
    st.header("🌦️ వాతావరణ సహాయకుడు")

    city = st.text_input("నగరం పేరు నమోదు చేయండి")

    if st.button("🎤 వాతావరణం అడగండి"):
        spoken_telugu = listen_telugu()
        st.write("మీ ప్రశ్న:", spoken_telugu)

        if city:
            weather_info = get_weather(city)
            st.success(weather_info)
            speak_telugu(weather_info)
        else:
            st.warning("దయచేసి నగరం పేరు నమోదు చేయండి")

# ---------------- SCREEN 3 : FARMING ----------------
elif menu == "🌾 Farming":
    st.header("🌾 వ్యవసాయ సహాయకుడు")

    if st.button("🎤 వ్యవసాయ ప్రశ్న అడగండి"):
        spoken_telugu = listen_telugu()
        st.write("మీ ప్రశ్న:", spoken_telugu)

        english = te_to_en(spoken_telugu)
        answer = farming_bot(english)
        telugu_answer = en_to_te(answer)

        st.success(telugu_answer)
        speak_telugu(telugu_answer)

# ---------------- SCREEN 4 : ASK ANYTHING ----------------
elif menu == "🤖 Ask Anything":
    st.header("🤖 రైతు మిత్రుడు")

    if st.button("🎤 మాట్లాడండి"):
        spoken_telugu = listen_telugu()
        st.write("మీ ప్రశ్న:", spoken_telugu)

        english = te_to_en(spoken_telugu)
        answer = farming_bot(english)
        telugu_answer = en_to_te(answer)

        st.success(telugu_answer)
        speak_telugu(telugu_answer)
