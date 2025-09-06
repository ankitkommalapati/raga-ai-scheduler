import sys, os
import pandas as pd
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduling import duration_for_patient_type, get_available_slots, book_slot
from data_loader import load_patients, find_patient_by_name_dob


def test_duration_for_patient_type():
    assert duration_for_patient_type("new") == 60
    assert duration_for_patient_type("returning") == 30


def test_find_patient_by_name_dob(tmp_path):
    # Ssample patients.csv
    patients_path = tmp_path / "patients.csv"
    patients = pd.DataFrame([
        {"patient_id": "P001", "first_name": "Amit", "last_name": "Sharma", "dob": "1985-03-22", "email": "amit@example.com"},
        {"patient_id": "P002", "first_name": "Neha", "last_name": "Verma", "dob": "1992-07-15", "email": "neha@example.com"},
    ])
    patients.to_csv(patients_path, index=False)

    # Load and test
    df = pd.read_csv(patients_path)
    found = find_patient_by_name_dob(df, "Amit", "Sharma", "1985-03-22")
    assert found is not None
    assert found["patient_id"] == "P001"

    not_found = find_patient_by_name_dob(df, "John", "Doe", "1990-01-01")
    assert not_found is None


def test_get_available_slots_returns_dataframe():
    # Fake schedule
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    schedule = pd.DataFrame([
        {"doctor_id": "D1", "doctor_name": "Dr. Maya Rao",
         "slot_start": now, "slot_end": now + timedelta(minutes=30), "available": True},
        {"doctor_id": "D1", "doctor_name": "Dr. Maya Rao",
         "slot_start": now + timedelta(minutes=30), "slot_end": now + timedelta(minutes=60), "available": True},
    ])

    # Returning patient: 30 min slots
    slots_30 = get_available_slots(schedule, "Dr. Maya Rao", 30)
    assert not slots_30.empty
    assert all(slots_30["available"])

    # New patient: 60 min slots (combine 2 consecutive 30 min slots)
    slots_60 = get_available_slots(schedule, "Dr. Maya Rao", 60)
    assert not slots_60.empty
    assert (slots_60.iloc[0]["slot_end"] - slots_60.iloc[0]["slot_start"]).seconds == 3600


def test_book_slot_marks_unavailable(tmp_path):
    # Temporary CSV path
    csv_path = tmp_path / "doctor_schedule.csv"

    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    schedule = pd.DataFrame([
        {"doctor_id": "D1", "doctor_name": "Dr. Maya Rao",
         "slot_start": now.strftime("%Y-%m-%d %H:%M"), "slot_end": (now + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"), "available": True},
        {"doctor_id": "D1", "doctor_name": "Dr. Maya Rao",
         "slot_start": (now + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"), "slot_end": (now + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M"), "available": True},
    ])
    schedule.to_csv(csv_path, index=False)

    # New patient (60 mins), should block 2 slots
    booked_slot = {
        "doctor_id": "D1",
        "doctor_name": "Dr. Maya Rao",
        "slot_start": now,
        "slot_end": now + timedelta(minutes=60),
    }
    book_slot(booked_slot, 60, schedule_path=str(csv_path))

    updated = pd.read_csv(csv_path)
    assert updated["available"].sum() == 0