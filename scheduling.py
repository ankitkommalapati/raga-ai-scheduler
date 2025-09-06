import pandas as pd

def duration_for_patient_type(patient_type):
    """Return appointment duration in minutes based on patient type."""
    return 60 if patient_type == "new" else 30


def get_available_slots(schedule, doctor_name, duration):
    """Return available slots depending on duration (30 or 60 minutes)."""
    slots = schedule.copy()
    if doctor_name != "Any":
        slots = slots[slots["doctor_name"] == doctor_name]

    # Ensure start and end are datetime
    slots["slot_start"] = pd.to_datetime(slots["slot_start"])
    slots["slot_end"] = pd.to_datetime(slots["slot_end"])

    available = []
    if duration == 30:
        # Return available slots
        available = slots[slots["available"]].copy()
    elif duration == 60:
        # Combine two consecutive slots into one 60-min slot
        slots = slots.sort_values(["doctor_id", "slot_start"])
        for i in range(len(slots) - 1):
            s1, s2 = slots.iloc[i], slots.iloc[i + 1]
            if (
                s1["doctor_id"] == s2["doctor_id"]
                and s1["available"] == True
                and s2["available"] == True
                and s2["slot_start"] == s1["slot_end"] 
            ):
                available.append({
                    "doctor_id": s1["doctor_id"],
                    "doctor_name": s1["doctor_name"],
                    "slot_start": s1["slot_start"],
                    "slot_end": s2["slot_end"],
                    "available": True,
                    "slot_indices": [i, i+1]
                })
        available = pd.DataFrame(available)

    return available


def book_slot(slot_row, duration, schedule_path="data/doctor_schedule.csv"):
    """
    Mark slots as booked (handles both 30- and 60-min cases).
    Updates doctor_schedule.csv to persist the change.
    """
    schedule = pd.read_csv(schedule_path)
    schedule["slot_start"] = pd.to_datetime(schedule["slot_start"])
    schedule["slot_end"] = pd.to_datetime(schedule["slot_end"])

    if duration == 30:
        # Match by doctor + start time
        schedule.loc[
            (schedule["doctor_id"] == slot_row["doctor_id"]) &
            (schedule["slot_start"] == pd.to_datetime(slot_row["slot_start"])),
            "available"
        ] = False
    elif duration == 60:
        # Block both consecutive slots
        schedule.loc[
            (schedule["doctor_id"] == slot_row["doctor_id"]) &
            (schedule["slot_start"] == pd.to_datetime(slot_row["slot_start"])),
            "available"
        ] = False
        schedule.loc[
            (schedule["doctor_id"] == slot_row["doctor_id"]) &
            (schedule["slot_end"] == pd.to_datetime(slot_row["slot_end"])),
            "available"
        ] = False

    # Save back
    schedule.to_csv(schedule_path, index=False)

    return slot_row
