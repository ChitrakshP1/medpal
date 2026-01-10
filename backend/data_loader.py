import pandas as pd
import os

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'database', 'symptoms_data.csv')
    try:
        return pd.read_csv(db_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["symptom", "risk_level", "advice"])