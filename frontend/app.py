import streamlit as st
import sys
import os

# Link frontend to backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.logic import assess_risk

st.title("🩺 MedPal: AI Health Assistant")
st.write("Enter your symptom for a quick risk assessment.")

user_input = st.text_input("How are you feeling?", placeholder="e.g., fever")

if st.button("Analyze"):
    if user_input:
        result = assess_risk(user_input)
        if result['status'] == "found":
            st.subheader(f"Risk Level: {result['risk']}")
            st.info(f"Advice: {result['advice']}")
        else:
            st.warning(result['advice'])