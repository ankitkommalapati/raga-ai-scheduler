# Technical Approach: AI Scheduling Agent (RagaAI Case Study)

## 1. Objective

Build a **production-grade scheduling assistant** that:

- Collects patient details (new vs returning)
- Recommends appointment duration (60 mins new, 30 mins returning)
- Checks doctor availability
- Books slots without double-booking
- Sends confirmation + intake form
- Automates reminders (72h, 24h, 2h before)
- Provides admin exports for reporting

The goal is to balance **human-friendly UX** with **robust engineering practices**.

---

## 2. System Architecture

Streamlit Frontend
↓
Scheduling Logic
↓
Data Persistence (CSV)

- Forms UI
- doctor_schedule.csv
- patients.csv
- appointments.csv
- reminders.csv

- **Streamlit**: conversational UI
- **CSV files**: lightweight data store for demo
- **Outbox folder**: simulated email system
- **Exports folder**: admin reports (.xlsx/.csv)
- **Templates folder**: email templates

---

## 3. Workflow

1. **Greeting & Lookup**

   - Input: Name, DOB
   - Check in `patients.csv`
   - Output: new vs returning

2. **Scheduling**

   - Duration decided automatically (60 vs 30)
   - Check `doctor_schedule.csv` for available slots
   - New patients → require 2 consecutive slots

3. **Confirmation**

   - Collect insurance info
   - Save appointment to `appointments.csv`
   - Block chosen slots in `doctor_schedule.csv`

4. **Communication**

   - Generate `.ics` file for calendar
   - Place simulated emails in `outbox/`
   - Attach intake form PDF

5. **Reminders**

   - Add 3 reminder entries to `reminders.csv`
   - Admin can trigger “Run Due Reminders Now”

6. **Admin Tools**
   - Export appointments as Excel/CSV
   - Regenerate doctor schedule (for demos/testing)

---

## 4. Data Model

### patients.csv

| patient_id | first | last | dob | email |

### doctor_schedule.csv

| doctor_id | doctor_name | slot_start | slot_end | available |

### appointments.csv

| appointment_id | patient_id | doctor_name | slot_start | slot_end | insurance_carrier | status |

### reminders.csv

| reminder_id | appointment_id | send_time | status |

---

## 5. Edge Cases Handled

- **Double-booking prevention** → 60 min blocks two consecutive 30-min slots.
- **DOB picker range** → 1940 to current year (fixes UX issue).
- **Unavailable slots** → friendly warning instead of crash.
- **Admin regeneration** → one-click schedule reset in sidebar.

---

## 6. Design Decisions

- **Streamlit over Flask/Django** → faster prototyping, interactive UI.
- **CSV for persistence** → transparent for demo; replaceable with DB.
- **Simulated email system** → ensures self-contained project, no SMTP/API setup required.
- **Modular design** → each concern split into its own file:
  - `scheduling.py`
  - `messaging.py`
  - `data_loader.py`
  - `calendar_utils.py`

---

## 7. Future Expansion

This project is structured so real-world integrations can be added without major rewrites:

- **Database migration**: Replace CSV with SQLite/Postgres.
- **Email/SMS integration**:
  - Swap `simulate_email()` with `send_real_email()` (SMTP, SendGrid, AWS SES, Twilio).
  - Credentials via environment variables.
- **Authentication & roles**: Secure login for admin vs front-desk staff.
- **Multi-clinic scaling**: Filter schedules by clinic.
- **Analytics dashboard**: Show patient load, doctor utilization, cancellations.

---

## 8. Success Criteria

- ✅ New & returning patients handled correctly
- ✅ Smart slot duration (60 vs 30 mins)
- ✅ Double-booking prevented
- ✅ Confirmation + reminders generated
- ✅ Admin exports work reliably
- ✅ Demo runs end-to-end without external dependencies

---

## 9. Demo Walkthrough (3–5 min)

1. New patient → 60 min slot booked, intake form sent
2. Returning patient → 30 min slot booked
3. Admin regenerates schedule
4. Trigger reminders
5. Export report
