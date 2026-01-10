import sys
import os
from datetime import datetime
import streamlit as st

# ---------- FIX IMPORT PATH ----------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the integrated AI/Database logic
from backend.logic import ask_ai, assess_risk

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="MedPal - AI Health Companion",
    page_icon="🩺",
    layout="centered"
)

# ---------- PREMIUM DARK UI CSS ----------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: radial-gradient(circle at top left, #1f2937, #020617);
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    color: #f9fafb;
    font-weight: 700;
}

/* Cards */
section[data-testid="stVerticalBlock"] > div {
    background: rgba(17, 24, 39, 0.75);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 32px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: linear-gradient(145deg, #111827, #020617);
    color: #f9fafb;
    border-radius: 14px;
    border: 1px solid #1f2937;
    padding: 12px;
    font-size: 15px;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9ca3af;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 16px;
    border: none;
    padding: 12px 26px;
    font-size: 15px;
    font-weight: 600;
    box-shadow: 0 10px 26px rgba(37, 99, 235, 0.4);
    transition: all 0.25s ease-in-out;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 34px rgba(37, 99, 235, 0.6);
}

/* History text */
.stMarkdown p {
    font-size: 15px;
    color: #d1d5db;
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
if st.session_state.med_history:
    for med in st.session_state.med_history:
        st.write(med)
else:
    st.caption("No medications logged yet.")

# ================= SYMPTOMS SECTION =================
st.markdown("## 🤒 Log your Symptoms / Vitals")

symptom = st.text_input("Symptom / Vitals", placeholder="Headache and fever")

if st.button("Log Symptom"):
    if symptom:
        time_now = datetime.now().strftime("%H:%M")
        st.session_state.symptom_history.append(f"🤒 {symptom} at {time_now}")

st.markdown("**Symptom / Vitals History:**")
if st.session_state.symptom_history:
    for s in st.session_state.symptom_history:
        st.write(s)
else:
    st.caption("No symptoms logged yet.")

# ================= ASK MEDPAL (INTEGRATED) =================
st.markdown("## 🧠 Ask MedPal")
st.info("Powered by your medical database and AI for dynamic responses.")

question = st.text_input(
    "Type your health question",
    placeholder="What could be causing chest pain and a cough?"
)

if st.button("Ask MedPal"):
    if question:
        with st.spinner("Analyzing against medical database..."):
            # 1. Get the dynamic AI answer (RAG)
            ai_answer = ask_ai(question)
            
            # 2. Get the specific database metadata for UI styling
            db_data = assess_risk(question)
            
            # 3. Dynamic UI Coloring based on Risk
            if db_data:
                risk = db_data['risk']
                category = db_data['category']
                
                if risk == "High":
                    st.error(f"🚨 **URGENT: {category} Detection**")
                elif risk == "Medium":
                    st.warning(f"⚠️ **MODERATE: {category} Detection**")
                else:
                    st.success(f"✅ **LOGGED: {category} Detection**")
                
                st.markdown(f"**Detected Symptom:** {db_data['detected']}")
            
            # 4. Show the Dynamic AI Response
            st.markdown("### 👨‍⚕️ MedPal's Analysis")
            st.write(ai_answer)
            
            st.divider()
            st.caption("🚨 **Disclaimer:** MedPal provides informational guidance only. If you are experiencing a medical emergency, please call local emergency services immediately.")
    else:
        st.warning("Please enter a question or symptom to analyze.")