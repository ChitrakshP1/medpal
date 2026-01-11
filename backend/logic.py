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
        return pd.DataFrame(columns=['symptom', 'risk_level', 'category', 'advice'])

def assess_risk(user_input):
    """Scans for multiple symptoms and returns the one with the highest priority."""
    df = load_data()
    user_input = user_input.lower().strip()
    
    priority_map = {"High": 3, "Medium": 2, "Low": 1, "Unknown": 0}
    found_matches = []

    for _, row in df.iterrows():
        if str(row['symptom']).lower() in user_input:
            found_matches.append(row)

    if not found_matches:
        return None

    # Returns the highest risk row found
    best_match = max(found_matches, key=lambda x: priority_map.get(x['risk_level'], 0))
    
    return {
        "risk": best_match['risk_level'],
        "category": best_match.get('category', 'General'),
        "advice": best_match['advice'],
        "detected": best_match['symptom']
    }

def ask_ai(question: str):
    """Connects Database to AI for dynamic, informed responses."""
    
    # 1. Search Database
    db_match = assess_risk(question)
    
    # 2. Construct a Dynamic Prompt
    if db_match:
        # Feed DB data to the AI
        prompt = (
            f"Context: A user says they have '{question}'. Our database identifies this as '{db_match['detected']}' "
            f"with a {db_match['risk']} risk level in the {db_match['category']} category. "
            f"Our medical advice is: {db_match['advice']}. "
            f"Task: Provide a natural, empathetic, and concise response to the user based on this advice."
        )
    else:
        # Dynamic fallback for items not in DB
        prompt = (
            f"User Question: '{question}'. This symptom is not in our database. "
            f"Task: Provide safe, general medical advice and strongly recommend consulting a professional."
        )

    # 3. Call AI with higher 'temperature' for dynamic output
    if not HF_API_KEY:
        return db_match['advice'] if db_match else "Consult a doctor."

    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        # Added temperature and top_p for more natural variability
        payload = {
            "inputs": f"<s>[INST] {prompt} [/INST]",
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7, 
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()[0]["generated_text"].strip()
            
    except Exception:
        pass

    # Final hard-coded fallback if API fails
    return db_match['advice'] if db_match else "Please consult a healthcare professional."