import streamlit as st
from google import genai
from google.genai import types

# पेज सेटअप
st.set_page_config(page_title="साइबर सुरक्षा सहायक", page_icon="🛡️", layout="centered")

st.title("🛡️ साइबर सुरक्षा जागरूकता बॉट साइबर क्राइम सेल कमिश्नरेट वाराणसी")
st.warning(
    "⚠️ यह एक AI जागरूकता सहायक है, आधिकारिक शिकायत पोर्टल नहीं। "
    "यहाँ कभी भी अपना OTP, पासवर्ड या बैंक खाता नंबर न लिखें। "
    "वित्तीय धोखाधड़ी होने पर तुरंत **1930** पर कॉल करें या **cybercrime.gov.in** पर शिकायत दर्ज करें।"
)

# पोर्टल के अनुसार मुख्य श्रेणियां और उनके सब-ऑप्शन
CATEGORIES = {
    "💰 मेरे पैसे कट गए / वित्तीय धोखाधड़ी": [
        "किसी ने कॉल/मैसेज करके मुझे पैसे ट्रांसफर करने के लिए बहकाया (UPI/निवेश/जॉब/डिजिटल अरेस्ट)",
        "बिना मेरी अनुमति या जानकारी के मेरे खाते से पैसे कट गए",
        "मैं किसी अवैध सट्टेबाजी (Betting) या ऑनलाइन जुआ वेबसाइट की रिपोर्ट करना चाहता हूँ"
    ],
    "🚫 ऑनलाइन उत्पीड़न, ब्लैकमेलिंग या अश्लील सामग्री": [
        "कोई ऑनलाइन पीछा कर रहा है, लोकेशन ट्रैक कर रहा है या धमकी भरे/गाली-गलौज मैसेज भेज रहा है",
        "मेरे नाम से फर्जी अकाउंट (Fake Profile) बनाया गया है या मेरी बदनामी की जा रही है",
        "मेरी निजी फोटो/वीडियो वायरल करने की धमकी देकर पैसे मांगे जा रहे हैं (ब्लैकमेलिंग / Sextortion)",
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
        "ऑनलाइन मेरे या किसी समूह के बारे में झूठी खबर, नफरत या हिंसा फैलाने वाली पोस्ट की जा रही है",
        "किसी ने स्कूल, एयरपोर्ट या सार्वजनिक स्थान के लिए फर्जी धमकी (Bomb/Emergency threat) दी है"
    ],
    "🏢 कंपनी या संस्था के सिस्टम पर साइबर हमला": [
        "कंप्यूटर या फाइलों में वायरस/मैलवेयर आ गया है",
        "फाइलें लॉक (Ransomware) हो गई हैं और खोलने के लिए पैसे मांगे जा रहे हैं",
        "संस्था की वेबसाइट हैक कर ली गई है या ट्रैफिक भेजकर बंद (DDoS) कर दी गई है",
        "संस्था के नेटवर्क या AI सिस्टम में अनाधिकृत प्रवेश (Unauthorised Access) हुआ है"
    ],
    "🎲 ऑनलाइन जुआ, साइबर स्लेवरी, पायरेसी या डीपफेक": [
        "डीपफेक (Deepfake) — किसी असली व्यक्ति का नकली वीडियो या ऑडियो बनाया गया है",
        "ऑनलाइन प्लेटफॉर्म के जरिए किसी को फंसाकर शोषण/तस्करी (Cyber Slavery) की जा रही है",
        "फिल्मों, किताबों या सॉफ्टवेयर की ऑनलाइन पायरेसी की जा रही है",
        "अवैध ऑनलाइन जुआ या सट्टेबाजी वेबसाइट की शिकायत करनी है"
    ],
    "❓ कुछ और हुआ है (अन्य साइबर अपराध)": [
        "मेरी समस्या ऊपर दिए गए विकल्पों में नहीं है, मुझे सामान्य साइबर शिकायत की जानकारी चाहिए"
    ]
}

# AI के लिए हिंदी नियम (System Instruction)
rules = """
आप भारत के नागरिकों के लिए एक विनम्र और स्पष्ट 'साइबर सुरक्षा जागरूकता सहायक' हैं।
- हमेशा सरल, शुद्ध और समझने में आसान हिंदी भाषा में जवाब दें।
- जब कोई यूज़र किसी साइबर अपराध की श्रेणी चुने, तो उसे इन 3 बिंदुओं में साफ-साफ समझाएं:
  1. **तुरंत क्या करें (Immediate Steps):** घबराएं नहीं और सबसे पहले क्या कदम उठाएं।
  2. **कौन से सबूत तैयार रखें:** शिकायत दर्ज करने के लिए क्या-क्या जरूरी है (जैसे: ट्रांजैक्शन आईडी/UTR, बैंक स्टेटमेंट, कॉल रिकॉर्ड/नंबर, चैट के स्क्रीनशॉट, वेबसाइट का URL आदि)।
  3. **शिकायत कैसे दर्ज करें:** वित्तीय धोखाधड़ी के लिए तुरंत **1930** पर कॉल करना और सभी साइबर अपराधों के लिए **cybercrime.gov.in** पोर्टल (या नजदीकी साइबर थाना) पर रिपोर्ट करने का तरीका बताएं।
- कभी भी यूज़र से OTP, पासवर्ड, PIN या बैंक खाता नंबर न मांगें।
- जवाब को बुलेट पॉइंट्स में और संक्षिप्त रखें।
"""

# Session State सेटअप
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(system_instruction=rules)
    )
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "नमस्ते! 🙏 मैं आपका **साइबर सुरक्षा सहायक** हूँ।\n\nशुरू करने के लिए नीचे **'Hi'** या **'नमस्ते'** लिखें, या ऊपर दिए गए **'📋 मुख्य मेन्यू खोलें'** बटन पर क्लिक करें।"
        }
    ]

if "menu_step" not in st.session_state:
    st.session_state.menu_step = "idle"  # idle, main, sub
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# AI से जवाब लाने का फंक्शन
def ask_bot(user_text):
    st.session_state.messages.append({"role": "user", "content": user_text})
    try:
        response = st.session_state.chat.send_message(user_text)
        bot_reply = response.text
    except Exception:
        # अगर सर्वर व्यस्त हो तो दोबारा सेशन बनाकर कोशिश करें
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(system_instruction=rules)
        )
        response = st.session_state.chat.send_message(user_text)
        bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ऊपर मेन्यू खोलने का शॉर्टकट बटन
if st.button("📋 मुख्य मेन्यू खोलें (शिकायत श्रेणी चुनें)"):
    st.session_state.menu_step = "main"
    st.session_state.selected_category = None

# पुरानी चैट दिखाएं
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- पॉपअप / सिलेक्शन मेन्यू सेक्शन ---
if st.session_state.menu_step == "main":
    st.info("👇 **यह किस प्रकार की शिकायत है? कृपया नीचे से एक विकल्प चुनें:**")
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES.keys()):
        if cols[i % 2].button(category, use_container_width=True, key=f"cat_{i}"):
            st.session_state.selected_category = category
            st.session_state.menu_step = "sub"
            st.rerun()

elif st.session_state.menu_step == "sub" and st.session_state.selected_category:
    cat = st.session_state.selected_category
    st.info(f"📂 **{cat}**\n\n👇 **कृपया अपनी समस्या का सटीक प्रकार चुनें:**")
    for j, sub_option in enumerate(CATEGORIES[cat]):
        if st.button(f"🔹 {sub_option}", use_container_width=True, key=f"sub_{j}"):
            st.session_state.menu_step = "idle"
            prompt_text = f"मेरी शिकायत की श्रेणी '{cat}' है और समस्या यह है: '{sub_option}'। कृपया मुझे सरल हिंदी में बताएं कि मुझे तुरंत क्या करना चाहिए, कौन से सबूत रखने चाहिए और शिकायत कैसे दर्ज करनी है?"
            ask_bot(prompt_text)
            st.rerun()

    if st.button("⬅️ वापस मुख्य मेन्यू पर जाएं"):
        st.session_state.menu_step = "main"
        st.rerun()

# --- नीचे चैट इनपुट बॉक्स ---
if prompt := st.chat_input("यहाँ 'Hi' या अपना कोई भी सवाल हिंदी में लिखें..."):
    clean_prompt = prompt.strip().lower()
    greetings = ["hi", "hello", "hey", "hii", "नमस्ते", "नमस्कार", "menu", "मेन्यू", "help", "मदद"]

    if clean_prompt in greetings:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({
            "role": "assistant",
            "content": "नमस्ते! 🙏 कृपया नीचे दिए गए विकल्पों में से अपनी समस्या चुनें ताकि मैं आपको सही जानकारी दे सकूँ:"
        })
        st.session_state.menu_step = "main"
        st.rerun()
    else:
        st.session_state.menu_step = "idle"
        ask_bot(prompt)
        st.rerun()
