import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
APPTS_CSV = os.path.join(DATA_DIR, "appointments.csv")
SCHEDULE_CSV = os.path.join(DATA_DIR, "doctor_schedule.csv")

def load_patients() -> pd.DataFrame:
    """Load patients.csv as DataFrame (empty if missing)."""
    if os.path.exists(PATIENTS_CSV):
        return pd.read_csv(PATIENTS_CSV)
    return pd.DataFrame(columns=["patient_id", "first_name", "last_name", "dob", "email"])

def find_patient_by_name_dob(patients: pd.DataFrame, first: str, last: str, dob: str):
    """Find patient record by first_name, last_name, and DOB (YYYY-MM-DD)."""
    if patients.empty:
        return None
    df = patients.copy()
    m = df[
        (df["first_name"].str.lower() == first.lower()) &
        (df["last_name"].str.lower() == last.lower()) &
        (df["dob"] == dob)
    ]
    if len(m):
        return m.iloc[0].to_dict()
    return None

def load_schedule() -> pd.DataFrame:
    """Load doctor_schedule.csv as DataFrame (empty if missing)."""
    if os.path.exists(SCHEDULE_CSV):
        return pd.read_csv(SCHEDULE_CSV)
    return pd.DataFrame(columns=["doctor_id", "doctor_name", "slot_start", "slot_end", "available"])

def save_appointments(records: list):
    """Append new appointment(s) to appointments.csv."""
    df = pd.DataFrame(records)
    if os.path.exists(APPTS_CSV):
        old = pd.read_csv(APPTS_CSV)
        out = pd.concat([old, df], ignore_index=True)
    else:
        out = df
    out.to_csv(APPTS_CSV, index=False)

def load_appointments() -> pd.DataFrame:
    """Load appointments.csv as DataFrame (empty if missing)."""
    if os.path.exists(APPTS_CSV):
        return pd.read_csv(APPTS_CSV)
    return pd.DataFrame(columns=[
        "appointment_id", "patient_id", "patient_name", "dob", "patient_type",
        "doctor_id", "doctor_name", "slot_start", "slot_end", "clinic_location",
        "insurance_carrier", "member_id", "group_number", "intake_form_sent",
        "confirmation_sent", "status"
    ])
