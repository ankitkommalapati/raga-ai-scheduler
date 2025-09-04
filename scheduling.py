import os
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SCHEDULE_CSV = os.path.join(DATA_DIR, "doctor_schedule.csv")

def duration_for_patient_type(patient_type: str) -> int:
    return 60 if patient_type == "new" else 30

def load_schedule_df():
    return pd.read_csv(SCHEDULE_CSV)

def get_available_slots(schedule_df, preferred_doctor: str, required_minutes: int):
    df = schedule_df.copy()
    if preferred_doctor != "Any":
        df = df[df["doctor_name"] == preferred_doctor]
    df = df[df["available"] == True]
    return df[["doctor_id","doctor_name","date","slot_start","slot_end","available"]].reset_index(drop=True)

def book_slot(chosen_row, duration_minutes: int):
    df = load_schedule_df()
    start = chosen_row["slot_start"]
    doc = chosen_row["doctor_id"]
    df.loc[(df["doctor_id"] == doc) & (df["slot_start"] == start), "available"] = False
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    if duration_minutes == 60:
        next_start = (start_dt + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
        df.loc[(df["doctor_id"] == doc) & (df["slot_start"] == next_start), "available"] = False
        final_end = (start_dt + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M")
    else:
        final_end = (start_dt + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    df.to_csv(SCHEDULE_CSV, index=False)
    return {"doctor_id": doc, "doctor_name": chosen_row["doctor_name"], "slot_start": start_dt.strftime("%Y-%m-%d %H:%M"), "slot_end": final_end}
