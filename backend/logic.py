# backend/logic.py
import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def ask_ai(question: str):
    # Fallback logic (VERY important)
    if not HF_API_KEY:
        return rule_based_answer(question)

    try:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}"
        }

        payload = {
            "inputs": f"Answer medically safely: {question}"
        }

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            return rule_based_answer(question)

        return response.json()[0]["generated_text"]

    except Exception:
        return rule_based_answer(question)


def rule_based_answer(question: str):
    q = question.lower()

    if "fever" in q and "headache" in q:
        return (
            "Fever and headache may be caused by viral infections, flu, dehydration, "
            "or sinus infections. If symptoms persist or worsen, consult a doctor."
        )

    if "fever" in q:
        return (
            "Fever is commonly caused by infections. Rest, hydration, and monitoring "
            "temperature is advised."
        )

    return "Please consult a healthcare professional for accurate diagnosis."
