import pandas as pd
import os

MEDICATION_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'medications.csv')
SYMPTOM_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'symptoms_log.csv')

# --- Medication functions ---
def save_medication(name: str, dose: str):
    df = pd.DataFrame([{"name": name, "dose": dose}])
    if os.path.exists(MEDICATION_FILE):
        df_old = pd.read_csv(MEDICATION_FILE)
        df = pd.concat([df_old, df], ignore_index=True)
    df.to_csv(MEDICATION_FILE, index=False)

def get_medications():
    if os.path.exists(MEDICATION_FILE):
        return pd.read_csv(MEDICATION_FILE).to_dict(orient="records")
    return []

# --- Symptom functions ---
def save_symptom(symptom: str):
    df = pd.DataFrame([{"symptom": symptom}])
    if os.path.exists(SYMPTOM_FILE):
        df_old = pd.read_csv(SYMPTOM_FILE)
        df = pd.concat([df_old, df], ignore_index=True)
    df.to_csv(SYMPTOM_FILE, index=False)

def get_symptoms():
    if os.path.exists(SYMPTOM_FILE):
        return pd.read_csv(SYMPTOM_FILE).to_dict(orient="records")
    return []
