import os
import uuid
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from scheduling import get_available_slots, book_slot, duration_for_patient_type
from data_loader import load_patients, find_patient_by_name_dob, load_schedule, save_appointments, load_appointments
from messaging import simulate_email, schedule_reminders_for_appointment, run_due_reminders
from calendar_utils import create_ics_for_appointment

st.set_page_config(page_title="AI Scheduling Agent", page_icon="🩺", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FORMS_DIR = os.path.join(os.path.dirname(__file__), "forms")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "exports")

st.title("🩺 AI Scheduling Agent - Clinic Booking")

# Sidebar: Admin actions
with st.sidebar:
    st.header("Admin")
    if st.button("Export Admin Report (Excel)"):
        appts = load_appointments()
        export_path = os.path.join(EXPORTS_DIR, f"admin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        try:
            appts.to_excel(export_path, index=False)
            st.success(f"Exported to {export_path}")
        except Exception as e:
            csv_path = export_path.replace(".xlsx", ".csv")
            appts.to_csv(csv_path, index=False)
            st.warning(f"openpyxl/xlsxwriter not found. Exported CSV instead: {csv_path}")
    st.divider()
    if st.button("Run Due Reminders Now"):
        n = run_due_reminders()
        st.info(f"Sent {n} due reminders. Check 'outbox/' and 'data/reminders.csv'.")

# Conversation-like flow
st.subheader("Patient Greeting")
with st.form("greeting_form"):
    first = st.text_input("First Name *")
    last = st.text_input("Last Name *")
    dob = st.date_input("Date of Birth *", format="YYYY-MM-DD")
    preferred_doctor = st.selectbox("Preferred Doctor", ["Any", "Dr. Maya Rao", "Dr. Arvind Nair", "Dr. Leena Kapoor"])
    clinic_location = st.selectbox("Clinic Location", ["Main Clinic - Bengaluru", "Satellite - Indiranagar"])
    submitted = st.form_submit_button("Continue")

if submitted:
    patients = load_patients()
    found = find_patient_by_name_dob(patients, first, last, dob.strftime("%Y-%m-%d"))
    if found is not None:
        patient_type = "returning"
        st.success(f"Welcome back, {first}! We've found your record. (Returning patient)")
        patient_id = found["patient_id"]
        email = found["email"]
    else:
        patient_type = "new"
        st.info("You're a new patient. We'll create a record after booking.")
        patient_id = None
        email = None

    st.session_state["greeting"] = {
        "first": first, "last": last, "dob": dob.strftime("%Y-%m-%d"),
        "patient_type": patient_type, "preferred_doctor": preferred_doctor,
        "clinic_location": clinic_location, "patient_id": patient_id, "email": email
    }

if "greeting" in st.session_state:
    g = st.session_state["greeting"]
    st.subheader("Smart Scheduling")
    duration = duration_for_patient_type(g["patient_type"])  # 60 for new, 30 for returning
    st.write(f"Recommended duration: **{duration} minutes** for a **{g['patient_type']}** patient.")

    schedule = load_schedule()
    slots = get_available_slots(schedule, g["preferred_doctor"], duration)
    st.write("Available slots:")
    st.dataframe(slots.head(25))

    with st.form("slot_select"):
        slot_idx = st.number_input("Enter row index of desired slot", min_value=0, max_value=len(slots)-1, step=1)
        insurance_carrier = st.text_input("Insurance Carrier *")
        member_id = st.text_input("Member ID *")
        group_number = st.text_input("Group Number *")
        confirm = st.form_submit_button("Confirm Appointment")

    if confirm:
        chosen = slots.iloc[int(slot_idx)]
        appointment_id = str(uuid.uuid4())[:8]

        # Book slot & write appointment
        booked = book_slot(chosen, duration)
        appt_record = {
            "appointment_id": appointment_id,
            "patient_id": g["patient_id"] or "",
            "patient_name": f"{g['first']} {g['last']}",
            "dob": g["dob"],
            "patient_type": g["patient_type"],
            "doctor_id": booked["doctor_id"],
            "doctor_name": booked["doctor_name"],
            "slot_start": booked["slot_start"],
            "slot_end": booked["slot_end"],
            "clinic_location": g["clinic_location"],
            "insurance_carrier": insurance_carrier,
            "member_id": member_id,
            "group_number": group_number,
            "intake_form_sent": False,
            "confirmation_sent": False,
            "status": "Booked"
        }
        save_appointments([appt_record])

        # Send confirmation & intake (simulated email)
        slot_dt = datetime.strptime(booked["slot_start"], "%Y-%m-%d %H:%M")
        slot_date = slot_dt.strftime("%b %d, %Y")
        slot_time = slot_dt.strftime("%I:%M %p")
        simulate_email(
            to_email=g.get("email") or "new.patient@example.com",
            template="email_confirm.txt",
            context={
                "first_name": g["first"],
                "doctor_name": booked["doctor_name"],
                "slot_date": slot_date,
                "slot_time": slot_time,
                "clinic_location": g["clinic_location"],
            },
            attach_form=True
        )
        simulate_email(
            to_email=g.get("email") or "new.patient@example.com",
            template="email_intake_form.txt",
            context={
                "first_name": g["first"],
                "doctor_name": booked["doctor_name"],
                "slot_date": slot_date,
                "slot_time": slot_time,
            },
            attach_form=True
        )

        # Create ICS calendar file
        ics_path = create_ics_for_appointment(appointment_id, booked["doctor_name"], slot_dt, duration, g["clinic_location"])

        # Schedule reminders
        schedule_reminders_for_appointment(appointment_id, g["first"], booked["doctor_name"], slot_dt, g.get("email"))

        st.success(f"Appointment confirmed! (ID: {appointment_id})")
        st.write(f"Calendar file created: {ics_path}")
        st.info("Confirmation & intake form emails placed in 'outbox/'. Three reminders scheduled automatically.")
        st.balloons()
