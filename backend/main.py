# backend/main.py
from fastapi import FastAPI, Query
from backend.data_loader import (
    save_medication, get_medications,
    save_symptom, get_symptoms
)
from backend.logic import ask_ai

app = FastAPI(title="MedPal Backend")

@app.get("/")
def root():
    return {"status": "MedPal backend running"}

@app.post("/medication")
def log_medication(name: str, dose: str):
    save_medication(name, dose)
    return {"message": "Medication saved"}

@app.get("/medication")
def medication_history():
    return get_medications()

@app.post("/symptom")
def log_symptom(symptom: str):
    save_symptom(symptom)
    return {"message": "Symptom logged"}

@app.get("/symptom")
def symptom_history():
    return get_symptoms()

@app.post("/ask")
def ask(question: str = Query(...)):
    answer = ask_ai(question)
    return {"answer": answer}