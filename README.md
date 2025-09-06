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
