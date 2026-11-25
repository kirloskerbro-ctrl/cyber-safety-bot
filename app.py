import os
import base64
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(
    page_title="Cyber Crime Cell - Commissionerate Varanasi",
    page_icon="🛡️",
    layout="centered"
)

# --- 1. UP Police Logo Watermark Background + Dark Bold Button Styling ---
def apply_custom_styling():
    possible_logos = [
        "up_ police_ logo.jpeg",
        "up_police_logo.jpeg",
        "up_police_logo.jpg",
        "up_police_logo.png",
        "Uttar Pradesh Police logo.jpeg",
        "Uttar Pradesh Police logo.jpg",
        "Uttar Pradesh Police logo.png"
    ]
    watermark_css = ""
    for fname in possible_logos:
        if os.path.exists(fname):
            ext = fname.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            with open(fname, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            watermark_css = f"""
            .stApp::before {{
                content: "";
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 480px;
                height: 480px;
                background-image: url("data:{mime};base64,{encoded}");
                background-repeat: no-repeat;
                background-position: center center;
                background-size: contain;
                opacity: 0.14;
                pointer-events: none;
                z-index: 0;
            }}
            """
            break

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #f8f9fc;
        }}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        .block-container {{
            position: relative;
            z-index: 1;
        }}
        {watermark_css}

        /* Dark Navy Bold Buttons (Standard & Secondary Link Buttons) */
        div.stButton > button,
        a[data-testid="stBaseLinkButton-secondary"] {{
            background-color: #0F2C59 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 14px !important;
            border-radius: 8px !important;
            border: 2px solid #0A1D3D !important;
            box-shadow: 0 3px 6px rgba(0,0,0,0.18) !important;
            text-decoration: none !important;
            transition: all 0.2s ease-in-out !important;
        }}
        div.stButton > button:hover,
        a[data-testid="stBaseLinkButton-secondary"]:hover {{
            background-color: #1A4380 !important;
            border-color: #D4AF37 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }}

        /* Active / Primary Buttons (Police Crimson Red) */
        div.stButton > button[kind="primary"],
        a[data-testid="stBaseLinkButton-primary"] {{
            background-color: #B71C1C !important;
            color: #FFFFFF !important;
            border: 2px solid #7F0000 !important;
            font-weight: 800 !important;
            font-size: 15px !important;
            padding: 12px 14px !important;
            border-radius: 8px !important;
            box-shadow: 0 3px 6px rgba(0,0,0,0.18) !important;
            text-decoration: none !important;
        }}
        div.stButton > button[kind="primary"]:hover,
        a[data-testid="stBaseLinkButton-primary"]:hover {{
            background-color: #D32F2F !important;
            border-color: #FFD700 !important;
            color: #FFFFFF !important;
        }}

        /* Semi-transparent crisp cards */
        div[data-testid="stExpander"] {{
            background-color: rgba(255, 255, 255, 0.90) !important;
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
        }}
        div[data-testid="stChatMessage"] {{
            background-color: rgba(255, 255, 255, 0.90) !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_styling()

# --- 2. Header with Cyber Crime Cell Logo ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    else:
        st.markdown("# 🛡️")

with col_title:
    st.markdown("## Cyber Crime Cell, Commissionerate Varanasi")
    st.caption("आत्रेय Cyber Saathi | Quick cybercrime help, complaint guidance, and online safety awareness. Bot")

st.divider()

# Official Links
CHECK_STATUS_LINK = "https://www.cybercrime.gov.in/check-status"
REPORT_SUSPECT_LINK = "https://www.cybercrime.gov.in/cyber_suspect"
SUSPECT_SEARCH_LINK = "https://www.cybercrime.gov.in/suspect-search"
MRM_LINK = "https://mrm-ncrp.mha.gov.in/raise-request"
SANCHAR_SAATHI_LINK = "https://www.sancharsaathi.gov.in/"
NCRP_LINK = "https://www.cybercrime.gov.in/"
SOCIAL_MEDIA_LINKS = {
    "Facebook": "https://www.facebook.com/help/contact/295309487309948/",
    "WhatsApp": "https://www.whatsapp.com/contact/forms/1534459096974129",
    "Instagram": "https://help.instagram.com/contact/636276399721841",
    "Other": None
}

# --- 3. Awareness Booklet Content (Hindi & English) ---
AWARENESS_SCAMS = {
    "hi": [
        ("🚨 1. डिजिटल अरेस्ट (Digital Arrest)",
         "साइबर अपराधी खुद को पुलिस, CBI, ED, RBI, कस्टम, नारकोटिक्स या TRAI अधिकारी बताकर वीडियो कॉल करते हैं और झूठे केस में फंसाने का डर दिखाकर 'डिजिटल अरेस्ट' का नाटक करते हैं।\n\n**बचाव:** भारत के कानून में 'डिजिटल अरेस्ट' जैसी कोई प्रक्रिया नहीं है। ऐसे कॉल से न डरें, तुरंत कॉल काटें और **1930** पर रिपोर्ट करें।"),
        ("📈 2. इन्वेस्टमेंट स्कैम (Investment Scam)",
         "क्रिप्टो करेंसी, शेयर मार्केट, रियल एस्टेट या फर्जी ट्रेडिंग ऐप के जरिए कम समय में दोगुना/बड़ा मुनाफा कमाने का लालच देकर पैसे ठगे जाते हैं।\n\n**बचाव:** सोशल मीडिया के लालच भरे विज्ञापनों और अनजान निवेश ग्रुप से दूर रहें। केवल SEBI पंजीकृत प्लेटफॉर्म पर ही निवेश करें।"),
        ("💳 3. फर्जी लोन ऐप स्कैम (Loan App Scam)",
         "बिना कागजी कार्रवाई के तुरंत लोन देने वाले फर्जी ऐप डाउनलोड करवाकर आपके फोन के कॉन्टैक्ट्स और गैलरी का एक्सेस ले लिया जाता है, फिर ब्लैकमेल कर पैसे वसूले जाते हैं।\n\n**बचाव:** अनजान APK या गैर-मान्यता प्राप्त लोन ऐप कभी डाउनलोड न करें।"),
        ("📹 4. सेक्सटॉर्शन स्कैम (Sextortion Scam)",
         "ठग अनजान नंबर से अश्लील वीडियो कॉल करते हैं और स्क्रीन रिकॉर्डिंग कर उसे वायरल करने की धमकी देकर पैसे मांगते हैं।\n\n**बचाव:** अनजान नंबर से आने वाले वीडियो कॉल कभी न उठाएं। शिकार होने पर डरें नहीं, पैसे न दें और तुरंत **cybercrime.gov.in** पर शिकायत करें।"),
        ("💼 5. ऑनलाइन नौकरी स्कैम (Online Job Scam)",
         "फर्जी जॉब पोर्टल या मैसेज के जरिए घर बैठे मोटी सैलरी का झांसा देकर रजिस्ट्रेशन, इंटरव्यू या प्रोसेसिंग फीस के नाम पर पैसे ऐंठे जाते हैं।\n\n**बचाव:** कोई भी असली कंपनी नौकरी देने के लिए पैसे नहीं मांगती। कंपनी की आधिकारिक वेबसाइट पर जाकर जांच करें।"),
        ("🎟️ 6. लॉटरी स्कैम (Lottery Scam)",
         "ईमेल, SMS या कॉल के जरिए बताया जाता है कि आपने बड़ी लॉटरी जीती है और इनाम पाने के लिए टैक्स या प्रोसेसिंग शुल्क जमा करने को कहा जाता है।\n\n**बचाव:** बिना टिकट खरीदे कोई लॉटरी नहीं लगती। ऐसे कॉल या लिंक पर भरोसा न करें।"),
        ("🔍 7. गूगल सर्च / फर्जी कस्टमर केयर स्कैम",
         "बैंक या ई-कॉमर्स का कस्टमर केयर नंबर गूगल पर सर्च करने पर ठगों के फर्जी नंबर मिल जाते हैं, जो रिफंड के नाम पर लिंक या APK फाइल भेजकर खाता खाली कर देते हैं।\n\n**बचाव:** कस्टमर केयर नंबर हमेशा कंपनी की आधिकारिक वेबसाइट या ऐप से ही लें।"),
        ("💸 8. फेक पेमेंट स्कैम (Fake Payment Scam)",
         "ठग रिश्तेदार या दोस्त बनकर फर्जी SMS भेजते हैं कि गलती से आपके खाते में पैसे आ गए हैं और तुरंत वापस भेजने को कहते हैं।\n\n**बचाव:** केवल SMS पर भरोसा न करें। पहले अपना बैंक बैलेंस/स्टेटमेंट चेक करें।"),
        ("✈️ 9. टेलीग्राम / व्हाट्सएप टास्क स्कैम",
         "घर बैठे वीडियो लाइक, कमेंट या रिव्यू करके पैसे कमाने का झांसा दिया जाता है। शुरुआत में भरोसा जीतने के लिए ₹1000-₹2000 देते हैं, फिर बड़े टास्क के नाम पर लाखों ठग लेते हैं।\n\n**बचाव:** घर बैठे आसान कमाई के लालच में कभी न फंसें।"),
        ("🛒 10. OLX / ऑनलाइन खरीद-बिक्री स्कैम",
         "सस्ती बाइक, कार, फ्रिज या AC का विज्ञापन डालकर एडवांस पेमेंट या आर्मी/पुलिस कर्मी बनकर QR कोड स्कैन करवाकर ठगी की जाती है।\n\n**बचाव:** सामान देखे बिना एडवांस पैसे न दें। पैसे **प्राप्त करने** के लिए कभी QR कोड स्कैन या UPI PIN नहीं डालना होता।"),
        ("💳 11. क्रेडिट कार्ड स्कैम (Credit Card Scam)",
         "कार्ड की लिमिट बढ़ाने, रिवॉर्ड पॉइंट भुनाने या कार्ड बंद होने का डर दिखाकर कार्ड नंबर, CVV और OTP मांग लिया जाता है।\n\n**बचाव:** बैंक कभी भी फोन पर CVV या OTP नहीं मांगता।"),
        ("⚡ 12. बिजली / गैस बिल पेमेंट स्कैम",
         "बिजली या गैस कनेक्शन कटने का डर दिखाकर WhatsApp पर मैसेज या कॉल किया जाता है और बिल अपडेट करने के नाम पर फर्जी APK फाइल भेजकर फोन हैक कर लिया जाता है।\n\n**बचाव:** बिल हमेशा आधिकारिक ऐप या वेबसाइट से ही भरें। किसी अनजान APK फाइल को इंस्टॉल न करें।")
    ],
    "en": [
        ("🚨 1. Digital Arrest Scam",
         "Fraudsters pose as Police, CBI, ED, RBI, Customs, Narcotics, or TRAI officers on video calls, threatening victims with false cases and 'Digital Arrest'.\n\n**Safety:** There is NO 'Digital Arrest' under Indian law. Disconnect immediately and report on **1930**."),
        ("📈 2. Investment Scam",
         "Scammers promise huge returns in crypto, stock trading, or fake investment apps to steal your savings.\n\n**Safety:** Avoid tempting social media ads and unknown trading groups. Invest only through SEBI-registered platforms."),
        ("💳 3. Fake Loan App Scam",
         "Fraudulent instant loan apps steal access to your contacts and gallery, then blackmail you for money.\n\n**Safety:** Never download unverified loan apps or unknown APK files."),
        ("📹 4. Sextortion Scam",
         "Scammers make indecent video calls from unknown numbers, record your screen, and threaten to make it viral unless you pay.\n\n**Safety:** Never answer video calls from unknown numbers. Do not pay; report immediately at **cybercrime.gov.in**."),
        ("💼 5. Online Job Scam",
         "Fake job offers promise high work-from-home salaries and demand registration or processing fees.\n\n**Safety:** Genuine employers never ask for money to give a job. Verify on the official company website."),
        ("🎟️ 6. Lottery Scam",
         "Fake emails or calls claim you won a huge lottery and ask for tax or processing fees to release the prize.\n\n**Safety:** You cannot win a lottery you never entered. Ignore and block such contacts."),
        ("🔍 7. Google Search / Fake Customer Care Scam",
         "Scammers list fake helpline numbers on Google for banks/e-commerce and send malicious links or APK files to drain accounts.\n\n**Safety:** Always get customer care numbers only from the official website or app."),
        ("💸 8. Fake Payment / Wrong Transfer Scam",
         "Fraudsters pretend to be a friend/relative, send a fake credit SMS, and ask you to refund money sent 'by mistake'.\n\n**Safety:** Never trust an SMS alone; always check your actual bank balance first."),
        ("✈️ 9. Telegram / WhatsApp Task Scam",
         "Scammers offer money for liking videos or reviewing products. They pay ₹1,000–₹2,000 initially to build trust, then steal lakhs via 'prepaid tasks'.\n\n**Safety:** Avoid easy work-from-home task offers on Telegram/WhatsApp."),
        ("🛒 10. OLX / Marketplace Scam",
         "Fake ads for cheap bikes, cars, or appliances demand advance payment or trick sellers into scanning QR codes.\n\n**Safety:** Never pay in advance without inspecting the item. You NEVER need to scan a QR code or enter UPI PIN to receive money."),
        ("💳 11. Credit Card Scam",
         "Callers claim to increase your card limit or prevent card blocking and ask for Card Number, CVV, or OTP.\n\n**Safety:** Banks never ask for CVV, Expiry, or OTP over phone calls."),
        ("⚡ 12. Electricity / Gas Bill APK Scam",
         "Scammers threaten disconnection via WhatsApp/calls and send fake APK files to 'update' your bill, hacking your phone.\n\n**Safety:** Pay bills only via official apps. Never install APK files received on WhatsApp.")
    ]
}

AWARENESS_GUIDES = {
    "hi": [
        ("💬 व्हाट्सएप हैक होने से कैसे बचें (WhatsApp Safety)",
         "* **कॉल फॉरवर्डिंग से बचें:** किसी के कहने पर `*401*<नंबर>` या `**21*<नंबर>#` कभी डायल न करें।\n* **कॉल मर्जर से बचें:** अनजान कॉल पर बात करते समय दूसरी अनजान कॉल को कॉन्फ्रेंस (Merge) पर न लें।\n* **APK फाइल न खोलें:** व्हाट्सएप पर आने वाली शादी के कार्ड, चालान या बिल जैसी अनजान `.apk` फाइल डाउनलोड न करें।\n* **सुरक्षा:** व्हाट्सएप में हमेशा **Two-Step Verification (PIN)** चालू रखें।"),
        ("💳 UPI और क्रेडिट/डेबिट कार्ड सुरक्षा",
         "* पैसे **प्राप्त करने** के लिए कभी UPI PIN डालने या QR कोड स्कैन करने की आवश्यकता नहीं होती।\n* भुगतान से पहले प्राप्तकर्ता का नाम जरूर जांचें।\n* कार्ड नंबर, एक्सपायरी डेट और **CVV** किसी के साथ साझा न करें।\n* मोबाइल बैंकिंग ऐप में अपने कार्ड की **लेनदेन सीमा (Transaction Limit)** तय करके रखें।"),
        ("🔐 पासवर्ड और सामान्य इंटरनेट सुरक्षा",
         "* **क्या करें:** हर अकाउंट के लिए अलग और मजबूत पासवर्ड (अपरकेस, लोअरकेस, नंबर और स्पेशल कैरेक्टर) रखें और समय-समय पर बदलें।\n* **क्या न करें:** जन्मतिथि, नाम या फोन नंबर को पासवर्ड न बनाएं। सार्वजनिक Wi-Fi या साइबर कैफे के कंप्यूटर पर बैंकिंग न करें और 'Remember Password' न चुनें।"),
        ("🛡️ साइबर बुलिंग, महिला एवं बाल सुरक्षा",
         "* **महिलाएं:** सोशल मीडिया की प्राइवेसी सेटिंग मजबूत रखें, **2-Factor Authentication (MFA)** ऑन करें, अनजान फ्रेंड रिक्वेस्ट स्वीकार न करें और निजी जानकारी/लोकेशन ओवर-शेयर न करें।\n* **माता-पिता (बच्चों के लिए):** बच्चों से खुलकर बात करें, पैरेंटल कंट्रोल लगाएं, स्क्रीन टाइम तय करें और उन्हें अजनबियों से ऑनलाइन दोस्ती न करने की सीख दें।"),
        ("📱 मोबाइल गुम या चोरी होने पर (संचार साथी पोर्टल)",
         "अगर आपका मोबाइल गुम या चोरी हो गया है, तो **www.sancharsaathi.gov.in** पोर्टल या **Sanchar Saathi** ऐप पर जाकर:\n* अपने गुम/चोरी हुए मोबाइल को **ब्लॉक और ट्रेस** करें।\n* अपने आधार पर कितने सिम रजिस्टर्ड हैं, यह जांचें और अनजान सिम को बंद कराएं।\n* संदिग्ध धोखाधड़ी कॉल (Chakshu) की रिपोर्ट करें।")
    ],
    "en": [
        ("💬 How to Prevent WhatsApp Hacking",
         "* **Avoid Call Forwarding:** Never dial `*401*<number>` or `**21*<number>#` on anyone's request.\n* **Avoid Call Merging:** Do not merge an unknown incoming call into a conference call.\n* **No Unknown APKs:** Never install `.apk` files (like fake wedding cards, challans, or bills) sent on WhatsApp.\n* **Enable Security:** Always turn on **Two-Step Verification** in WhatsApp Settings."),
        ("💳 UPI & Credit/Debit Card Safety",
         "* You **NEVER** need to enter a UPI PIN or scan a QR code to **receive** money.\n* Always verify the receiver's name before paying.\n* Keep your Card Number, Expiry Date, and **CVV** strictly confidential.\n* Set daily **transaction limits** on your cards via your mobile banking app."),
        ("🔐 Password & General Internet Safety",
         "* **Do's:** Use strong, unique passwords (uppercase, lowercase, numbers, symbols) for each account and update them regularly.\n* **Don'ts:** Never use your DOB, name, or phone number as a password. Avoid banking on public Wi-Fi or shared computers, and never click 'Remember Password'."),
        ("🛡️ Cyber Bullying, Women & Child Safety",
         "* **For Women:** Lock social media privacy settings, enable **Multi-Factor Authentication (MFA)**, avoid unknown friend requests, and do not overshare personal details or live location.\n* **For Parents:** Talk openly with children, enable parental controls, set screen-time limits, and teach them never to share personal details with online strangers."),
        ("📱 Lost or Stolen Mobile (Sanchar Saathi Portal)",
         "Visit **www.sancharsaathi.gov.in** or use the **Sanchar Saathi** app to:\n* **Block and trace** your lost or stolen mobile phone.\n* Check how many SIM cards are registered in your name and report unauthorized ones.\n* Report suspected fraud calls and international calls showing Indian numbers.")
    ]
}

# --- 4. Main UI Content (Hindi & English) ---
CONTENT = {
    "hi": {
        "warning": "⚠️ यह एक AI जागरूकता सहायक है, आधिकारिक शिकायत पोर्टल नहीं। यहाँ कभी भी OTP, पासवर्ड या बैंक खाता नंबर न लिखें। वित्तीय धोखाधड़ी होने पर तुरंत **1930** पर कॉल करें या **cybercrime.gov.in** पर शिकायत दर्ज करें।",
        "welcome": "नमस्ते! 🙏 मैं **साइबर क्राइम सेल, कमिश्नरेट वाराणसी** का जागरूकता सहायक हूँ। अपनी समस्या चुनें या नीचे अपना सवाल लिखें।",
        "lang_btn": "🌐 Change Language (English)",
        "reset_btn": "🔄 मुख्य मेन्यू रीसेट करें",
        "sec_complaint": "📝 1. शिकायत सेक्शन",
        "sec_services": "⚡ 2. त्वरित सेवाएं",
        "sec_awareness": "📚 3. साइबर जागरूकता",
        "btn_status": "📋 शिकायत स्थिति जांचें",
        "btn_report_suspect": "🚨 संदिग्ध की रिपोर्ट करें",
        "btn_search_suspect": "🔎 संदिग्ध खोजें (Search)",
        "grm_btn": "🏦 अन्य राज्य पुलिस द्वारा खाता फ्रीज़ (GRM सूचना)",
        "mrm_btn": "💸 मनी रिस्टोरेशन मॉड्यूल (MRM) — रिफंड अपडेट",
        "mrm_caption": "अपना 14 अंकों का NCRP Acknowledgement No. डालकर फ्रीज़ राशि की वापसी (Refund) का अनुरोध/अपडेट देखें।",
        "sanchar_btn": "📱 संचार साथी पोर्टल (गुम मोबाइल ब्लॉक / सिम जांच)",
        "ncrp_btn": "🌐 राष्ट्रीय साइबर क्राइम पोर्टल (cybercrime.gov.in)",
        "varanasi_contacts": """
### 📞 वाराणसी कमिश्नरेट साइबर संपर्क सूत्र
* **आपातकालीन वित्तीय धोखाधड़ी हेल्पलाइन:** **1930** (24×7)
* **साइबर क्राइम पुलिस थाना** (₹5 लाख से अधिक धोखाधड़ी हेतु): पुलिस लाइन गेट नं. 2, पाण्डेयपुर, वाराणसी — **7839876645**
* **साइबर क्राइम सेल:** पुलिस लाइन गेट नं. 2, पाण्डेयपुर, वाराणसी — **7839856954**
*(₹5 लाख से कम के मामलों में अपने नजदीकी थाने की साइबर हेल्प डेस्क पर भी संपर्क कर सकते हैं।)*
""",
        "grm_notice": """
### 🏦 GRM (Grievance Redressal Mechanism) संबंधी महत्वपूर्ण सूचना

यदि आपका बैंक खाता किसी **अन्य राज्य/जनपद की पुलिस अथवा साइबर थाना** द्वारा फ्रीज़ (**Freeze/LIEN**) किया गया है, तो **साइबर क्राइम सेल, वाराणसी द्वारा NOC जारी नहीं की जाती।**

**ऐसी स्थिति में क्या करें?**
* ✔️ अपने बैंक की संबंधित शाखा (**Home Branch**) में जाकर **GRM (Grievance Redressal Mechanism)** के माध्यम से अपना आवेदन दर्ज कराएं।
* ✔️ बैंक द्वारा दर्ज किया गया GRM **स्वतः (Automatically)** उस संबंधित पुलिस इकाई अथवा राज्य के पास भेज दिया जाता है, जहाँ से आपके खाते पर फ्रीज़/लियन लगाया गया है।
* ✔️ संबंधित जांच अधिकारी/साइबर थाना आपके आवेदन का परीक्षण कर नियमानुसार आवश्यक कार्रवाई करेगा।

**कृपया ध्यान दें:** साइबर क्राइम सेल, वाराणसी किसी अन्य राज्य द्वारा फ्रीज़ किए गए खाते के संबंध में NOC जारी करने के लिए अधिकृत नहीं है।

*जनहित में जारी — साइबर क्राइम सेल, वाराणसी कमिश्नरेट, उत्तर प्रदेश पुलिस*
""",
        "awareness_intro": "### 📚 साइबर ज्ञान पुस्तिका — पुलिस कमिश्नरेट वाराणसी\n*सावधान रहें, सतर्क रहें; साइबर सुरक्षित रहें।*",
        "scams_header": "#### 🚨 प्रमुख साइबर धोखाधड़ी के तरीके (क्लिक करके पढ़ें)",
        "guides_header": "#### 🛡️ साइबर सुरक्षा के महत्वपूर्ण उपाय (क्लिक करके पढ़ें)",
        "main_prompt": "👇 **यह किस प्रकार की शिकायत है? कृपया नीचे से एक विकल्प चुनें:**",
        "sub_prompt": "👇 **कृपया अपनी समस्या का सटीक प्रकार चुनें:**",
        "social_prompt": "📱 **सोशल मीडिया हैक / फर्जी अकाउंट (Impersonation) रिपोर्टिंग:**\n\nनीचे सीधे कंपनी के आधिकारिक लिंक पर क्लिक करके रिपोर्ट करें, या गाइड व सुरक्षा सावधानियां जानने के लिए प्लेटफॉर्म चुनें:",
        "back_btn": "⬅️ वापस मुख्य श्रेणियों पर जाएं",
        "back_sub_btn": "⬅️ पीछे जाएं",
        "chat_placeholder": "यहाँ 'Hi' या अपना कोई भी साइबर सवाल हिंदी में लिखें...",
        "hi_reply": "नमस्ते! 🙏 कृपया ऊपर **'📝 1. शिकायत सेक्शन'** से अपनी समस्या चुनें या अपना सवाल लिखें।",
        "social_triggers": [
            "मेरा सोशल मीडिया अकाउंट (Facebook, Instagram, WhatsApp, X आदि) हैक हो गया है",
            "मेरे नाम से फर्जी अकाउंट (Fake Profile) बनाया गया है या बदनामी की जा रही है"
        ],
        "social_buttons": [
            ("📘 Facebook गाइड व सावधानियां", "🔗 Facebook पर सीधे रिपोर्ट करें", "Facebook"),
            ("💬 WhatsApp गाइड व सावधानियां", "🔗 WhatsApp पर सीधे रिपोर्ट करें", "WhatsApp"),
            ("📸 Instagram गाइड व सावधानियां", "🔗 Instagram पर सीधे रिपोर्ट करें", "Instagram"),
            ("🌐 अन्य सोशल मीडिया (X, YouTube आदि)", None, "Other")
        ],
        "rules": """
आप साइबर क्राइम सेल, कमिश्नरेट वाराणसी की ओर से एक विनम्र और स्पष्ट 'साइबर सुरक्षा जागरूकता सहायक' हैं।
- हमेशा सरल, शुद्ध और समझने में आसान हिंदी भाषा में जवाब दें।
- जब कोई यूज़र किसी साइबर अपराध की श्रेणी चुने, तो उसे साफ-साफ बिंदुओं में समझाएं:
  1. **तुरंत क्या करें (Immediate Steps)**
  2. **कौन से सबूत तैयार रखें** (UTR/ट्रांजैक्शन आईडी, बैंक स्टेटमेंट, कॉल रिकॉर्ड, चैट स्क्रीनशॉट, प्रोफाइल/वेबसाइट URL आदि)
  3. **शिकायत कैसे दर्ज करें:** वित्तीय धोखाधड़ी के लिए तुरंत **1930** पर कॉल करें और सभी साइबर अपराधों के लिए **cybercrime.gov.in** या नजदीकी साइबर थाना/सेल में रिपोर्ट करें।
  4. **भविष्य के लिए सुरक्षा सावधानियां (Safety Precautions)**
- कभी भी OTP, पासवर्ड, PIN या बैंक खाता नंबर न मांगें।
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
        "welcome": "Hello! 🙏 I am the **Cyber Crime Cell, Commissionerate Varanasi** Awareness Assistant. Select your issue or type your question below.",
        "lang_btn": "🌐 भाषा बदलें (हिंदी)",
        "reset_btn": "🔄 Reset Main Menu",
        "sec_complaint": "📝 1. Complaint Section",
        "sec_services": "⚡ 2. Quick Services",
        "sec_awareness": "📚 3. Awareness Section",
        "btn_status": "📋 Check Complaint Status",
        "btn_report_suspect": "🚨 Report Suspect",
        "btn_search_suspect": "🔎 Suspect Search",
        "grm_btn": "🏦 Account Freeze by Other State Police (GRM Notice)",
        "mrm_btn": "💸 Money Restoration Module (MRM) — Refund Update",
        "mrm_caption": "Search with your 14-digit NCRP Acknowledgement No. to raise or check your frozen money refund request.",
        "sanchar_btn": "📱 Sanchar Saathi Portal (Block Lost Mobile / Check SIMs)",
        "ncrp_btn": "🌐 National Cyber Crime Portal (cybercrime.gov.in)",
        "varanasi_contacts": """
### 📞 Varanasi Commissionerate Cyber Contacts
* **Emergency Financial Fraud Helpline:** **1930** (24×7)
* **Cyber Crime Police Station** (For frauds above ₹5 Lakh): Police Line Gate No. 2, Pandeypur, Varanasi — **7839876645**
* **Cyber Crime Cell:** Police Line Gate No. 2, Pandeypur, Varanasi — **7839856954**
*(For frauds below ₹5 Lakh, you may also visit the Cyber Help Desk at your nearest Police Station.)*
""",
        "grm_notice": """
### 🏦 Important Notice Regarding GRM (Grievance Redressal Mechanism)

If your bank account has been frozen (**Freeze/LIEN**) by the **police or cyber police station of any other state or district**, **Cyber Crime Cell, Varanasi does not issue an NOC.**

**What to do in this situation?**
* ✔️ Visit your bank's **Home Branch** and submit your application through the **GRM (Grievance Redressal Mechanism)**.
* ✔️ The GRM application filed by the bank is **automatically forwarded** to the concerned police unit or state that placed the freeze/lien on your account.
* ✔️ The concerned Investigating Officer / Cyber Police Station will examine your application and take necessary action as per rules.

**Please Note:** Cyber Crime Cell, Varanasi is not authorized to issue an NOC for bank accounts frozen by any other state.

*Issued in Public Interest — Cyber Crime Cell, Commissionerate Varanasi, Uttar Pradesh Police*
""",
        "awareness_intro": "### 📚 Cyber Awareness Booklet — Police Commissionerate Varanasi\n*Stay Alert, Stay Vigilant; Stay Cyber Safe.*",
        "scams_header": "#### 🚨 Common Types of Cyber Scams (Click to Read)",
        "guides_header": "#### 🛡️ Essential Cyber Safety Guides (Click to Read)",
        "main_prompt": "👇 **What type of complaint is this? Please select an option below:**",
        "sub_prompt": "👇 **Please select the exact issue:**",
        "social_prompt": "📱 **Hacked / Impersonated Social Media Reporting:**\n\nClick the direct official link below to report to the company, or select a platform for step-by-step guidance & safety precautions:",
        "back_btn": "⬅️ Back to Main Categories",
        "back_sub_btn": "⬅️ Go Back",
        "chat_placeholder": "Type 'Hi' or ask any cyber safety question in English...",
        "hi_reply": "Hello! 🙏 Please choose your issue from the **'📝 1. Complaint Section'** above or type your question.",
        "social_triggers": [
            "My social media account (Facebook, Instagram, WhatsApp, X, etc.) was hacked",
            "Someone created a fake account pretending to be me or is defaming me online"
        ],
        "social_buttons": [
            ("📘 Facebook Guide & Precautions", "🔗 Report Hacked Facebook", "Facebook"),
            ("💬 WhatsApp Guide & Precautions", "🔗 Report Hacked / Fake WhatsApp", "WhatsApp"),
            ("📸 Instagram Guide & Precautions", "🔗 Report Hacked / Fake Instagram", "Instagram"),
            ("🌐 Other Social Media (X, YouTube, etc.)", None, "Other")
        ],
        "rules": """
You are a polite and clear 'Cyber Safety Awareness Assistant' representing Cyber Crime Cell, Commissionerate Varanasi.
- Always reply in simple, clear English.
- When a user selects a cyber crime category, explain clearly in these points:
  1. **Immediate Steps**
  2. **Evidence to Keep Ready** (UTR/Transaction ID, bank statement, call logs, chat screenshots, profile/website URL, etc.)
  3. **How to Report:** For financial fraud, immediately call **1930**, and for all cyber crimes, file a complaint on **cybercrime.gov.in** or visit the nearest Cyber Police Station/Cell.
  4. **Safety Precautions**
- Never ask for OTPs, passwords, PINs, or bank account numbers.
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

# --- 5. Session State Setup ---
if "lang" not in st.session_state:
    st.session_state.lang = None
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
if "active_section" not in st.session_state:
    st.session_state.active_section = "complaint"
if "menu_step" not in st.session_state:
    st.session_state.menu_step = "main"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "show_grm" not in st.session_state:
    st.session_state.show_grm = False

def start_session(lang_code):
    st.session_state.lang = lang_code
    st.session_state.active_section = "complaint"
    st.session_state.menu_step = "main"
    st.session_state.selected_category = None
    st.session_state.show_grm = False
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(system_instruction=CONTENT[lang_code]["rules"])
    )
    st.session_state.messages = [
        {"role": "assistant", "content": CONTENT[lang_code]["welcome"]}
    ]

# --- 6. Language Selection Screen ---
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

# --- 7. Main Page ---
lang = st.session_state.lang
ui = CONTENT[lang]

# Top bar: Reset & Language switch
b1, b2 = st.columns(2)
if b1.button(ui["reset_btn"], use_container_width=True):
    st.session_state.active_section = "complaint"
    st.session_state.menu_step = "main"
    st.session_state.selected_category = None
    st.rerun()
if b2.button(ui["lang_btn"], use_container_width=True):
    st.session_state.lang = None
    st.rerun()

# Row 1: 3 Big Bold Section Buttons
s_col1, s_col2, s_col3 = st.columns(3)
if s_col1.button(
    ui["sec_complaint"],
    use_container_width=True,
    type="primary" if st.session_state.active_section == "complaint" else "secondary"
):
    st.session_state.active_section = "complaint"
    st.rerun()

if s_col2.button(
    ui["sec_services"],
    use_container_width=True,
    type="primary" if st.session_state.active_section == "services" else "secondary"
):
    st.session_state.active_section = "services"
    st.rerun()

if s_col3.button(
    ui["sec_awareness"],
    use_container_width=True,
    type="primary" if st.session_state.active_section == "awareness" else "secondary"
):
    st.session_state.active_section = "awareness"
    st.rerun()

# Row 2: 3 Direct NCRP Action Buttons (Dark Bold Style)
p_col1, p_col2, p_col3 = st.columns(3)
p_col1.link_button(ui["btn_status"], CHECK_STATUS_LINK, use_container_width=True, type="secondary")
p_col2.link_button(ui["btn_report_suspect"], REPORT_SUSPECT_LINK, use_container_width=True, type="secondary")
p_col3.link_button(ui["btn_search_suspect"], SUSPECT_SEARCH_LINK, use_container_width=True, type="secondary")

st.divider()

def ask_bot(user_text, prefix_markdown=""):
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
    final_reply = f"{prefix_markdown}{bot_reply}" if prefix_markdown else bot_reply
    st.session_state.messages.append({"role": "assistant", "content": final_reply})

# ==================== SECTION 1: COMPLAINT SECTION ====================
if st.session_state.active_section == "complaint":
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
                if sub_option in ui["social_triggers"]:
                    st.session_state.menu_step = "social_media"
                    st.rerun()
                else:
                    st.session_state.menu_step = "idle"
                    if lang == "hi":
                        prompt_text = f"मेरी शिकायत की श्रेणी '{cat}' है और समस्या यह है: '{sub_option}'। कृपया सरल हिंदी में बताएं कि तुरंत क्या करें, कौन से सबूत रखें, शिकायत कैसे दर्ज करें और भविष्य में क्या सावधानियां रखें?"
                    else:
                        prompt_text = f"My complaint category is '{cat}' and the issue is: '{sub_option}'. Please explain in simple English what immediate steps to take, what evidence to keep, how to file the complaint, and safety precautions."
                    ask_bot(prompt_text)
                    st.rerun()

        if st.button(ui["back_btn"]):
            st.session_state.menu_step = "main"
            st.rerun()

    elif st.session_state.menu_step == "social_media":
        st.info(ui["social_prompt"])
        for k, (guide_label, link_label, platform) in enumerate(ui["social_buttons"]):
            report_link = SOCIAL_MEDIA_LINKS[platform]
            col1, col2 = st.columns(2)
            if col1.button(guide_label, use_container_width=True, key=f"sm_{lang}_{k}"):
                st.session_state.menu_step = "idle"
                if lang == "hi":
                    link_box = f"🔗 **{platform} आधिकारिक रिपोर्टिंग लिंक:** [{report_link}]({report_link})\n\n---\n" if report_link else ""
                    prompt_text = f"मेरा {platform} अकाउंट हैक या फर्जी (Impersonate) हुआ है। कृपया सरल हिंदी में बताएं कि तुरंत क्या करें, कंपनी को कैसे रिपोर्ट करें, cybercrime.gov.in पर शिकायत कैसे करें और सुरक्षा सावधानियां क्या रखें?"
                else:
                    link_box = f"🔗 **Official {platform} Reporting Link:** [{report_link}]({report_link})\n\n---\n" if report_link else ""
                    prompt_text = f"My {platform} account has been hacked or impersonated. Please explain in simple English immediate steps, how to report to {platform} and cybercrime.gov.in, and safety precautions."
                ask_bot(prompt_text, prefix_markdown=link_box)
                st.rerun()

            if report_link and link_label:
                col2.link_button(link_label, report_link, use_container_width=True, type="primary")

        if st.button(ui["back_sub_btn"]):
            st.session_state.menu_step = "sub"
            st.rerun()

    st.divider()
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==================== SECTION 2: QUICK SERVICES ====================
elif st.session_state.active_section == "services":
    with st.container(border=True):
        if st.button(ui["grm_btn"], use_container_width=True):
            st.session_state.show_grm = not st.session_state.show_grm

        if st.session_state.show_grm:
            st.info(ui["grm_notice"])

        st.divider()
        st.link_button(ui["mrm_btn"], MRM_LINK, use_container_width=True, type="primary")
        st.caption(ui["mrm_caption"])

        st.divider()
        s1, s2 = st.columns(2)
        s1.link_button(ui["sanchar_btn"], SANCHAR_SAATHI_LINK, use_container_width=True, type="secondary")
        s2.link_button(ui["ncrp_btn"], NCRP_LINK, use_container_width=True, type="secondary")

    with st.container(border=True):
        st.markdown(ui["varanasi_contacts"])

# ==================== SECTION 3: AWARENESS SECTION ====================
elif st.session_state.active_section == "awareness":
    st.markdown(ui["awareness_intro"])
    st.markdown(ui["scams_header"])
    for scam_title, scam_body in AWARENESS_SCAMS[lang]:
        with st.expander(scam_title):
            st.markdown(scam_body)

    st.divider()
    st.markdown(ui["guides_header"])
    for guide_title, guide_body in AWARENESS_GUIDES[lang]:
        with st.expander(guide_title):
            st.markdown(guide_body)

# --- 8. Warning Placed Below the Main Menu ---
st.divider()
st.warning(ui["warning"])

# --- 9. Chat Input ---
if prompt := st.chat_input(ui["chat_placeholder"]):
    clean_prompt = prompt.strip().lower()
    greetings = ["hi", "hello", "hey", "hii", "नमस्ते", "नमस्कार", "menu", "मेन्यू", "help", "मदद"]
    st.session_state.active_section = "complaint"
    if clean_prompt in greetings:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": ui["hi_reply"]})
        st.session_state.menu_step = "main"
        st.rerun()
    else:
        st.session_state.menu_step = "idle"
        ask_bot(prompt)
        st.rerun()
