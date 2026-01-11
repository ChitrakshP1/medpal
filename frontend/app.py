from datetime import datetime
import requests
import streamlit as st

# ---------- BACKEND CONFIG ----------
BACKEND_URL = "https://medpal-qkvf.onrender.com"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="MedPal - AI Health Companion",
    page_icon="🩺",
    layout="centered"
)

# ---------- PREMIUM DARK UI CSS ----------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1f2937, #020617);
    color: #e5e7eb;
}
h1, h2, h3 {
    color: #f9fafb;
    font-weight: 700;
}
section[data-testid="stVerticalBlock"] > div {
    background: rgba(17, 24, 39, 0.75);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 32px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}
.stTextInput input, .stTextArea textarea {
    background: linear-gradient(145deg, #111827, #020617);
    color: #f9fafb;
    border-radius: 14px;
    border: 1px solid #1f2937;
    padding: 12px;
    font-size: 15px;
}
.stButton button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 16px;
    border: none;
    padding: 12px 26px;
    font-size: 15px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "med_history" not in st.session_state:
    st.session_state.med_history = []

if "symptom_history" not in st.session_state:
    st.session_state.symptom_history = []

# ---------- HEADER ----------
st.title("🩺 MedPal - AI Health Companion")
st.write("Your personal AI-powered health assistant")

# ================= MEDICATION SECTION =================
st.markdown("## 💊 Log your Medication")

med_name = st.text_input("Medication Name", placeholder="Paracetamol")
dose = st.text_input("Dose", placeholder="500 mg")

if st.button("Save Medication"):
    if med_name and dose:
        time_now = datetime.now().strftime("%H:%M")
        st.session_state.med_history.append(f"💊 {med_name} ({dose}) at {time_now}")

st.markdown("**Medication History:**")
for med in st.session_state.med_history:
    st.write(med)

# ================= SYMPTOMS SECTION =================
st.markdown("## 🤒 Log your Symptoms / Vitals")

symptom = st.text_input("Symptom / Vitals", placeholder="Headache and fever")

if st.button("Log Symptom"):
    if symptom:
        time_now = datetime.now().strftime("%H:%M")
        st.session_state.symptom_history.append(f"🤒 {symptom} at {time_now}")

st.markdown("**Symptom / Vitals History:**")
for s in st.session_state.symptom_history:
    st.write(s)

# ================= ASK MEDPAL =================
st.markdown("## 🧠 Ask MedPal")
st.info("Powered by MedPal AI backend.")

question = st.text_input(
    "Type your health question",
    placeholder="What could be causing chest pain and a cough?"
)

if st.button("Ask MedPal"):
    if question:
        with st.spinner("Analyzing with MedPal AI..."):
            try:
                # 1️⃣ Call AI answer endpoint
                ai_res = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"question": question},
                    timeout=30
                )
                ai_answer = ai_res.json().get("answer")

                # 2️⃣ Call risk assessment endpoint
                risk_res = requests.post(
                    f"{BACKEND_URL}/assess-risk",
                    json={"question": question},
                    timeout=30
                )
                db_data = risk_res.json()

                # 3️⃣ Risk-based UI
                if db_data:
                    risk = db_data.get("risk")
                    category = db_data.get("category")

                    if risk == "High":
                        st.error(f"🚨 **URGENT: {category} Detection**")
                    elif risk == "Medium":
                        st.warning(f"⚠️ **MODERATE: {category} Detection**")
                    else:
                        st.success(f"✅ **LOGGED: {category} Detection**")

                    st.markdown(f"**Detected Symptom:** {db_data.get('detected')}")

                # 4️⃣ AI Response
                st.markdown("### 👨‍⚕️ MedPal's Analysis")
                st.write(ai_answer)

                st.caption(
                    "🚨 **Disclaimer:** MedPal provides informational guidance only. "
                    "If you are experiencing a medical emergency, contact emergency services."
                )

            except Exception as e:
                st.error("Unable to reach MedPal backend.")
                st.code(str(e))
    else:
        st.warning("Please enter a question to analyze.")
