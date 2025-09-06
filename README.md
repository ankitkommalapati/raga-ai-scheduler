# 🩺 AI Scheduling Agent (RagaAI Case Study)

An intelligent **clinic scheduling assistant** that behaves like a smart front-desk staff member.  
It books patient appointments, prevents double-booking, sends confirmations, and schedules reminders — all through a conversational **Streamlit UI**.

⚡ Self-contained • 💻 Runs locally • 🧑‍⚕️ Clinic-like experience

---

## ✨ Features
- **Conversational booking flow** (Streamlit UI)
- **Smart duration logic**:  
  - New patients → 60 mins  
  - Returning patients → 30 mins  
- **Doctor schedule management** with one-click reset
- **Conflict-free booking** (blocks consecutive slots automatically)
- **Automatic confirmation & intake form delivery** (simulated emails → `outbox/`)
- **Calendar integration**: generates `.ics` files
- **Automated reminders**: 72h, 24h, 2h before appointment
- **Admin tools**:  
  - Export all appointments (Excel/CSV)  
  - Trigger reminders manually  
  - Regenerate schedules  

---

## 🗂️ Project Structure
```
raga-ai-scheduler/
├── app.py # Streamlit frontend
├── scheduling.py # Slot logic (duration, booking, conflict prevention)
├── data_loader.py # CSV load/save helpers
├── messaging.py # Simulated email + reminders
├── calendar_utils.py # Generate .ics files
│
├── data/ # Data persistence
│ ├── patients.csv # (empty → populated on new bookings)
│ ├── doctor_schedule.csv # (empty → regenerate via Admin)
│ ├── appointments.csv # (empty → populated on bookings)
│ └── reminders.csv # (empty → populated on reminders)
│
├── forms/ # Intake form PDFs
├── templates/ # Email templates
├── exports/ # Admin exports (Excel/CSV) - starts empty
├── outbox/ # Simulated sent emails - starts empty
│
├── tests/ # Unit tests (pytest)
│
├── docs/ # Documentation
│ └── technical_approach.md
│
└── README.md
```

## 🚀 Getting Started

### 1. Clone Repo
```bash
git clone https://github.com/ankitkommalapati/raga-ai-scheduler.git
cd raga-ai-scheduler
```

### 2. Create Virtual Environment (Python 3.10+ recommended)
```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run app.py
```

## 🎮 Demo Flow

### 1. First-time Setup
- The `doctor_schedule.csv` is empty by default.
- Go to the **sidebar** and click **“Regenerate Doctor Schedule”** to create a fresh 7-day calendar of slots.

### 2. New Patient
- Enter name + DOB not in system.
- System assigns 60-min slot.
- Patient is added to  `patients.csv`.
- Confirmation email + intake form appear in `outbox/`.

### 3. Returning Patient
- Enter existing name + DOB.
- System assigns 30-min slot.
- Booking saved in `appointments.csv`.

### 4. Admin Tools (Sidebar)
- Export appointments to Excel/CSV.
- Trigger due reminders.
- Regenerate doctor schedule anytime.

## 🧪 Running Tests

```bash
pytest -q
```

- Includes tests for:
- - Scheduling logic (durations, double-booking prevention).
- - Patient lookup (`first_name` / `last_name`).

## 📂 Data Model

- `patients.csv` → patient registry
- `doctor_schedule.csv` → doctor availability (starts empty, regenerate via Admin)
- `appointments.csv` → booked slots
- `reminders.csv` → pending reminders

## 🚧 Limitations

- Data stored in CSV (not persistent DB).
- Emails are simulated (saved to `outbox/` as `.txt`).
- Authentication not implemented.

## 🔮 Future Expansion

- Replace CSV with **SQLite/Postgres**.
- Swap simulated emails with **real SMTP / SendGrid / AWS SES**.
- SMS reminders via Twilio.
- Multi-clinic scaling.
- Analytics dashboard for doctors/admins.

## 🙌 Acknowledgements

Built as part of **RagaAI Data Science Intern Case Study**.
Designed to feel like a real-world system while staying self-contained for easy demo.
