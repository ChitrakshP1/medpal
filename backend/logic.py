from .data_loader import load_data

df = load_data()

def assess_risk(user_input):
    user_input = user_input.lower().strip()
    # Simple matching logic for the prototype
    match = df[df['symptom'].str.contains(user_input, case=False, na=False)]
    
    if not match.empty:
        row = match.iloc[0]
        return {"status": "found", "risk": row['risk_level'], "advice": row['advice']}
    
    return {"status": "unknown", "risk": "Unknown", "advice": "Please consult a medical professional."}