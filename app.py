import os
import streamlit as st
from google import genai
from google.genai import types

# पेज सेटअप
st.set_page_config(
    page_title="Cyber Crime Cell - Commissionerate Varanasi",
    page_icon="🛡️",
    layout="centered"
)

# --- 1. ऊपर लोगो और हेडर ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    else:
        st.markdown("# 🛡️")

with col_title:
    st.markdown("## Cyber Crime Cell, Commissionerate Varanasi")
    st.caption("साइबर सुरक्षा जागरूकता सहायक | Cyber Safety Awareness Bot")

st.divider()

# --- 2. हिंदी और इंग्लिश दोनों का डेटा ---
CONTENT = {
    "hi": {
        "warning": "⚠️ यह एक AI जागरूकता सहायक है, आधिकारिक शिकायत पोर्टल नहीं। यहाँ कभी भी OTP, पासवर्ड या बैंक खाता नंबर न लिखें। वित्तीय धोखाधड़ी होने पर तुरंत **1930** पर कॉल करें या **cybercrime.gov.in** पर शिकायत दर्ज करें।",
        "welcome": "नमस्ते! 🙏 मैं **साइबर क्राइम सेल, कमिश्नरेट वाराणसी** का जागरूकता सहायक हूँ।\n\nनीचे दिए गए विकल्पों में से अपनी समस्या चुनें, या अपना सवाल लिखें।",
        "menu_btn": "📋 मुख्य मेन्यू खोलें",
        "lang_btn": "🌐 Change Language (English)",
        "main_prompt": "👇 **यह किस प्रकार की शिकायत है? कृपया नीचे से एक विकल्प चुनें:**",
        "sub_prompt": "👇 **कृपया अपनी समस्या का सटीक प्रकार चुनें:**",
        "back_btn": "⬅️ वापस मुख्य मेन्यू पर जाएं",
        "chat_placeholder": "यहाँ 'Hi' या अपना कोई भी सवाल हिंदी में लिखें...",
        "hi_reply": "नमस्ते! 🙏 कृपया नीचे दिए गए विकल्पों में से अपनी समस्या चुनें:",
        "rules": """
आप साइबर क्राइम सेल, कमिश्नरेट वाराणसी की ओर से एक विनम्र और स्पष्ट 'साइबर सुरक्षा जागरूकता सहायक' हैं।
- हमेशा सरल, शुद्ध और समझने में आसान हिंदी भाषा में जवाब दें।
- जब कोई यूज़र किसी साइबर अपराध की श्रेणी चुने, तो उसे इन 3 बिंदुओं में साफ-साफ समझाएं:
  1. **तुरंत क्या करें (Immediate Steps):** घबराएं नहीं और सबसे पहले क्या कदम उठाएं।
  2. **कौन से सबूत तैयार रखें:** शिकायत के लिए क्या जरूरी है (जैसे: UTR/ट्रांजैक्शन आईडी, बैंक स्टेटमेंट, कॉल रिकॉर्ड, चैट स्क्रीनशॉट, वेबसाइट URL आदि)।
  3. **शिकायत कैसे दर्ज करें:** वित्तीय धोखाधड़ी के लिए तुरंत **1930** पर कॉल करें और सभी साइबर अपराधों के लिए **cybercrime.gov.in** या नजदीकी साइबर थाना/सेल में रिपोर्ट करें।
- कभी भी OTP, पासवर्ड, PIN या बैंक खाता नंबर न मांगें।
- जवाब बुलेट पॉइंट्स में और संक्षिप्त रखें।
""",
        "categories": {
            "💰 मेरे पैसे कट गए / वित्तीय धोखाधड़ी": [
                "किसी ने कॉल/मैसेज करके मुझे पैसे ट्रांसफर करने के लिए बहकाया (UPI/निवेश/जॉब/डिजिटल अरेस्ट)",
                "बिना मेरी अनुमति या जानकारी के मेरे खाते से पैसे कट गए",
                "अवैध सट्टेबाजी (Betting) या ऑनलाइन जुआ वेबसाइट की रिपोर्ट करनी है"
            ],
            "🚫 ऑनलाइन उत्पीड़न, ब्लैकमेलिंग या अश्लील सामग्री": [
                "कोई ऑनलाइन पीछा कर रहा है, लोकेशन ट्रैक कर रहा है या धमकी भरे मैसेज भेज रहा है",
                "मेरे नाम से फर्जी अकाउंट (Fake Profile) बनाया गया है या बदनामी की जा रही है",
                "निजी फोटो/वीडियो वायरल करने की धमकी देकर पैसे मांगे जा रहे हैं (Sextortion)",
                "AI या फोटो एडिटिंग से मेरी नकली अश्लील फोटो/वीडियो बनाई गई है",
                "बच्चों (18 वर्ष से कम) से जुड़ी अश्लील सामग्री की रिपोर्ट करनी है"
            ],
            "📱 फोन, सोशल मीडिया, ईमेल या डिवाइस हैक होना": [
                "मेरा सोशल मीडिया अकाउंट (Facebook, Instagram, WhatsApp, X आदि) हैक हो गया है",
                "मेरा ईमेल (Gmail) अकाउंट हैक हो गया है",
                "मेरा मोबाइल फोन, कंप्यूटर या लैपटॉप हैक या लॉक हो गया है",
                "मेरा बैंक अकाउंट, UPI या पेमेंट वॉलेट हैक हो गया है",
                "मेरा निजी डेटा (आधार, पैन, फोटो, कॉन्टैक्ट्स) चोरी या लीक हो गया है"
            ],
            "📞 फर्जी/धमकी भरे कॉल या झूठी जानकारी": [
                "पुलिस, कोर्ट या सरकारी अधिकारी बनकर फर्जी धमकी भरा कॉल आया (पैसे नहीं मांगे गए)",
                "ऑनलाइन झूठी खबर, नफरत या हिंसा फैलाने वाली पोस्ट की जा रही है",
                "किसी ने स्कूल, एयरपोर्ट या सार्वजनिक स्थान के लिए फर्जी धमकी दी है"
            ],
            "🏢 कंपनी या संस्था के सिस्टम पर साइबर हमला": [
                "कंप्यूटर या फाइलों में वायरस/मैलवेयर आ गया है",
                "फाइलें लॉक (Ransomware) हो गई हैं और खोलने के लिए पैसे मांगे जा रहे हैं",
                "संस्था की वेबसाइट हैक या बंद (DDoS) कर दी गई है",
                "संस्था के नेटवर्क या AI सिस्टम में अनाधिकृत प्रवेश हुआ है"
            ],
            "🎲 ऑनलाइन जुआ, साइबर स्लेवरी, पायरेसी या डीपफेक": [
                "डीपफेक (Deepfake) — किसी व्यक्ति का नकली वीडियो या ऑडियो बनाया गया है",
                "ऑनलाइन प्लेटफॉर्म के जरिए शोषण/तस्करी (Cyber Slavery) की जा रही है",
                "फिल्मों, किताबों या सॉफ्टवेयर की ऑनलाइन पायरेसी की जा रही है",
                "अवैध ऑनलाइन जुआ या सट्टेबाजी वेबसाइट की शिकायत करनी है"
            ],
            "❓ कुछ और हुआ है (अन्य साइबर अपराध)": [
                "मेरी समस्या ऊपर दिए गए विकल्पों में नहीं है, मुझे सामान्य साइबर शिकायत की जानकारी चाहिए"
            ]
        }
    },
    "en": {
        "warning": "⚠️ This is an AI awareness assistant, not an official complaint portal. Never share OTPs, passwords, or bank details here. For financial fraud, immediately call **1930** or report at **cybercrime.gov.in**.",
        "welcome": "Hello! 🙏 I am the **Cyber Crime Cell, Commissionerate Varanasi** Awareness Assistant.\n\nPlease select your issue from the menu below, or type your question.",
        "menu_btn": "📋 Open Main Menu",
        "lang_btn": "🌐 भाषा बदलें (हिंदी)",
        "main_prompt": "👇 **What type of complaint is this? Please select an option below:**",
        "sub_prompt": "👇 **Please select the exact issue:**",
        "back_btn": "⬅️ Back to Main Menu",
        "chat_placeholder": "Type 'Hi' or ask any cyber safety question in English...",
        "hi_reply": "Hello! 🙏 Please choose your issue from the options below:",
        "rules": """
You are a polite and clear 'Cyber Safety Awareness Assistant' representing Cyber Crime Cell, Commissionerate Varanasi.
- Always reply in simple, clear English.
- When a user selects a cyber crime category, explain clearly in these 3 points:
  1. **Immediate Steps:** What to do right away without panicking.
  2. **Evidence to Keep Ready:** What is needed for a complaint (e.g., UTR/Transaction ID, bank statement, call logs, chat screenshots, website URL, etc.).
  3. **How to Report:** For financial fraud, immediately call **1930**, and for all cyber crimes, file a complaint on **cybercrime.gov.in** or visit the nearest Cyber Police Station/Cell.
- Never ask for OTPs, passwords, PINs, or bank account numbers.
- Keep answers concise and in bullet points.
""",
        "categories": {
            "💰 I lost money / Financial Fraud": [
                "Someone contacted me and convinced me to pay or transfer money (UPI/Investment/Job/Digital Arrest)",
                "Money was taken from my account without my permission or authorization",
                "I want to report an illegal betting / gambling website"
            ],
            "🚫 Online Harassment, Blackmail or Obscene Content": [
                "Someone is stalking me, tracking my location, or sending abusive/threatening messages",
                "Someone created a fake account pretending to be me or is defaming me online",
                "Someone is using my private photos/videos to threaten or demand money (Blackmail / Sextortion)",
                "Someone made a fake intimate image or video using AI or photo editing",
                "I want to report child sexual content or something involving a minor under 18"
            ],
            "📱 Phone, Social Media, Email or Device Hacked": [
                "My social media account (Facebook, Instagram, WhatsApp, X, etc.) was hacked",
                "My email account (Gmail, etc.) was hacked",
                "My mobile phone, computer, or laptop was hacked or locked",
                "My bank account, UPI, or payment wallet was compromised",
                "My personal data (Aadhaar, PAN, photos, contacts) was stolen or leaked"
            ],
            "📞 Fake / Threatening Calls or False Information": [
                "Fake/threatening call pretending to be police, court, or govt agency (no money demanded)",
                "Someone is spreading fake news, hatred, or content promoting violence online",
                "Fake emergency threat (bomb/fire/kidnapping) to a school, airport, or public place"
            ],
            "🏢 Company or Organisation System Cyber Attack": [
                "Computer or files infected with virus/malware",
                "Files locked/encrypted and money demanded to unlock them (Ransomware)",
                "Website tampered with, defaced, or flooded with traffic (DDoS)",
                "Unauthorised access to organisation's network or AI system"
            ],
            "🎲 Online Gambling, Cyber Slavery, Piracy or Deepfakes": [
                "Deepfake — fake realistic video or audio of a real person",
                "Someone is being lured, trafficked, or exploited online (Cyber Slavery)",
                "Online piracy of movies, music, software, or books",
                "Report an illegal online gambling or betting website"
            ],
            "❓ Something else happened (Other Cyber Crime)": [
                "My issue is not listed above; I need general guidance on filing a cyber complaint"
            ]
        }
    }
}

# --- 3. Session State सेटअप ---
if "lang" not in st.session_state:
    st.session_state.lang = None
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
if "menu_step" not in st.session_state:
    st.session_state.menu_step = "main"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

def start_session(lang_code):
    st.session_state.lang = lang_code
    st.session_state.menu_step = "main"
    st.session_state.selected_category = None
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(system_instruction=CONTENT[lang_code]["rules"])
    )
    st.session_state.messages = [
        {"role": "assistant", "content": CONTENT[lang_code]["welcome"]}
    ]

# --- 4. सबसे पहले भाषा चुनने का पॉपअप (Language Selection Screen) ---
if st.session_state.lang is None:
    with st.container(border=True):
        st.markdown("### 🌐 कृपया अपनी भाषा चुनें / Please Select Your Language")
        st.write("आगे बढ़ने के लिए नीचे दी गई किसी एक भाषा पर क्लिक करें / Click a language below to continue:")
        c1, c2 = st.columns(2)
        if c1.button("🇮🇳 हिंदी (Hindi)", use_container_width=True, type="primary"):
            start_session("hi")
            st.rerun()
        if c2.button("🇬🇧 English", use_container_width=True, type="primary"):
            start_session("en")
            st.rerun()
    st.stop()

# --- 5. चुनी हुई भाषा के अनुसार मुख्य इंटरफ़ेस ---
lang = st.session_state.lang
ui = CONTENT[lang]

st.warning(ui["warning"])

# ऊपर दो शॉर्टकट बटन: मुख्य मेन्यू और भाषा बदलें
b1, b2 = st.columns(2)
if b1.button(ui["menu_btn"], use_container_width=True):
    st.session_state.menu_step = "main"
    st.session_state.selected_category = None
    st.rerun()
if b2.button(ui["lang_btn"], use_container_width=True):
    st.session_state.lang = None
    st.rerun()

# AI से जवाब लाने का फंक्शन
def ask_bot(user_text):
    st.session_state.messages.append({"role": "user", "content": user_text})
    try:
        response = st.session_state.chat.send_message(user_text)
        bot_reply = response.text
    except Exception:
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(system_instruction=ui["rules"])
        )
        response = st.session_state.chat.send_message(user_text)
        bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# पुरानी चैट दिखाएं
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. सिलेक्शन मेन्यू ---
if st.session_state.menu_step == "main":
    st.info(ui["main_prompt"])
    cols = st.columns(2)
    for i, category in enumerate(ui["categories"].keys()):
        if cols[i % 2].button(category, use_container_width=True, key=f"cat_{lang}_{i}"):
            st.session_state.selected_category = category
            st.session_state.menu_step = "sub"
            st.rerun()

elif st.session_state.menu_step == "sub" and st.session_state.selected_category:
    cat = st.session_state.selected_category
    st.info(f"📂 **{cat}**\n\n{ui['sub_prompt']}")
    for j, sub_option in enumerate(ui["categories"][cat]):
        if st.button(f"🔹 {sub_option}", use_container_width=True, key=f"sub_{lang}_{j}"):
            st.session_state.menu_step = "idle"
            if lang == "hi":
                prompt_text = f"मेरी शिकायत की श्रेणी '{cat}' है और समस्या यह है: '{sub_option}'। कृपया सरल हिंदी में बताएं कि तुरंत क्या करें, कौन से सबूत रखें और शिकायत कैसे दर्ज करें?"
            else:
                prompt_text = f"My complaint category is '{cat}' and the issue is: '{sub_option}'. Please explain in simple English what immediate steps to take, what evidence to keep, and how to file the complaint."
            ask_bot(prompt_text)
            st.rerun()

    if st.button(ui["back_btn"]):
        st.session_state.menu_step = "main"
        st.rerun()

# --- 7. चैट इनपुट बॉक्स ---
if prompt := st.chat_input(ui["chat_placeholder"]):
    clean_prompt = prompt.strip().lower()
    greetings = ["hi", "hello", "hey", "hii", "नमस्ते", "नमस्कार", "menu", "मेन्यू", "help", "मदद"]

    if clean_prompt in greetings:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": ui["hi_reply"]})
        st.session_state.menu_step = "main"
        st.rerun()
    else:
        st.session_state.menu_step = "idle"
        ask_bot(prompt)
        st.rerun()
