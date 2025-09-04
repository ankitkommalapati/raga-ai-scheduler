import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
APPTS_CSV = os.path.join(DATA_DIR, "appointments.csv")
SCHEDULE_CSV = os.path.join(DATA_DIR, "doctor_schedule.csv")

def load_patients() -> pd.DataFrame:
    return pd.read_csv(PATIENTS_CSV)

def find_patient_by_name_dob(patients: pd.DataFrame, first: str, last: str, dob: str):
    df = patients.copy()
    m = df[(df["first_name"].str.lower()==first.lower()) &
           (df["last_name"].str.lower()==last.lower()) &
           (df["dob"]==dob)]
    if len(m):
        return m.iloc[0].to_dict()
    return None

def load_schedule():
    return pd.read_csv(SCHEDULE_CSV)

def save_appointments(records: list):
    df = pd.DataFrame(records)
    if os.path.exists(APPTS_CSV):
        old = pd.read_csv(APPTS_CSV)
        out = pd.concat([old, df], ignore_index=True)
    else:
        out = df
    out.to_csv(APPTS_CSV, index=False)

def load_appointments():
    if os.path.exists(APPTS_CSV):
        return pd.read_csv(APPTS_CSV)
    return pd.DataFrame()
