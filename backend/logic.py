import os
import requests
import pandas as pd

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def load_data():
    """Loads the symptoms database from the CSV file."""
    try:
        # Assumes database/symptoms_data.csv exists relative to project root
        return pd.read_csv("database/symptoms_data.csv")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=['symptom', 'risk_level', 'advice'])

def assess_risk(user_input):
    """
    Scans for multiple symptoms and returns the one with the highest priority.
    Returns a dictionary or None if no symptoms found.
    """
    df = load_data()
    user_input = user_input.lower().strip()
    
    # Priority mapping for precision
    priority_map = {"High": 3, "Medium": 2, "Low": 1, "Unknown": 0}
    
    found_matches = []

    # Check for all symptoms in the database within the user's sentence
    for _, row in df.iterrows():
        if str(row['symptom']).lower() in user_input:
            found_matches.append(row)

    if not found_matches:
        return None

    # Sort matches by risk priority so the most dangerous advice is shown
    best_match = max(found_matches, key=lambda x: priority_map.get(x['risk_level'], 0))
    
    return {
        "risk": best_match['risk_level'],
        "advice": best_match['advice'],
        "detected": best_match['symptom']
    }

def ask_ai(question: str):
    """Primary entry point: Checks database first, then falls back to AI."""
    
    # 1. Try Precise Database/Rule-Based Lookup First
    database_result = assess_risk(question)
    
    if database_result:
        # Formulate a structured response from your database data
        response = (f"Detected: **{database_result['detected']}** (Risk: {database_result['risk']})\n\n"
                    f"**Advice:** {database_result['advice']}")
        return response

    # 2. Fallback to Rule-Based Manual Logic (from your original code)
    manual_fallback = rule_based_answer(question)
    if manual_fallback != "Consult a healthcare professional":
        return manual_fallback

    # 3. Fallback to Hugging Face AI
    if not HF_API_KEY:
        return "Please consult a healthcare professional for accurate diagnosis."

    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": f"Give brief, safe medical advice for: {question}"}
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()[0]["generated_text"]
    except Exception:
        pass

    return "Please consult a healthcare professional for accurate diagnosis."

def rule_based_answer(question: str):
    """Your original manual fallback logic."""
    q = question.lower()
    if "fever" in q and "headache" in q:
        return "Fever and headache may be caused by viral infections. Rest and hydrate."
    if "fever" in q:
        return "Fever is commonly caused by infections. Rest and monitoring is advised."
    
    return "Consult a healthcare professional"