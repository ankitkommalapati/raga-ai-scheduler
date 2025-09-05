import os
from datetime import datetime, timedelta

EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "exports")

def create_ics_for_appointment(appointment_id: str, doctor_name: str, start_dt: datetime, duration_minutes: int, location: str):
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Clinic//AI Scheduler//EN
BEGIN:VEVENT
UID:{appointment_id}
DTSTAMP:{start_dt.strftime('%Y%m%dT%H%M%S')}
DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}
SUMMARY:Clinic Appointment with {doctor_name}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
"""
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    path = os.path.join(EXPORTS_DIR, f"appointment_{appointment_id}.ics")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ics)
    return path
