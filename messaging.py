import os
from datetime import datetime, timedelta
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
OUTBOX_DIR = os.path.join(os.path.dirname(__file__), "outbox")

REMINDERS_CSV = os.path.join(DATA_DIR, "reminders.csv")

def render_template(template_name: str, context: dict):
    with open(os.path.join(TEMPLATES_DIR, template_name), "r", encoding="utf-8") as f:
        content = f.read()
    return content.format(**context)

def _write_outbox(to_email: str, subject_and_body: str, attachments=None):
    os.makedirs(OUTBOX_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(OUTBOX_DIR, f"{ts}_{to_email.replace('@','_at_')}.txt")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(subject_and_body)
        if attachments:
            f.write("\n\nAttachments:\n")
            for a in attachments:
                f.write(f"- {a}\n")
    return fname

def simulate_email(to_email: str, template: str, context: dict, attach_form: bool=False):
    body = render_template(template, context)
    attachments = []
    if attach_form:
        form_path = os.path.join(os.path.dirname(__file__), "forms", "New Patient Intake Form.pdf")
        if os.path.exists(form_path):
            attachments.append(form_path)
    return _write_outbox(to_email, body, attachments=attachments)

def schedule_reminders_for_appointment(appt_id: str, first_name: str, doctor_name: str, slot_dt, to_email: str):
    # Reminder schedule: 72h, 24h, 2h before
    plan = [72, 24, 2]
    rows = []
    for i, hrs in enumerate(plan, start=1):
        when = slot_dt - timedelta(hours=hrs)
        rows.append({
            "appointment_id": appt_id,
            "reminder_number": i,
            "scheduled_for": when.strftime("%Y-%m-%d %H:%M"),
            "sent_at": "",
            "channel": "email",
            "response_forms_filled": "",
            "response_confirmed": "",
            "response_cancel_reason": ""
        })
    df_new = pd.DataFrame(rows)
    if os.path.exists(REMINDERS_CSV):
        old = pd.read_csv(REMINDERS_CSV)
        out = pd.concat([old, df_new], ignore_index=True)
    else:
        out = df_new
    out.to_csv(REMINDERS_CSV, index=False)

def run_due_reminders() -> int:
    if not os.path.exists(REMINDERS_CSV):
        return 0
    df = pd.read_csv(REMINDERS_CSV)
    now = datetime.now()
    sent = 0
    for idx, row in df.iterrows():
        if not row["sent_at"] and datetime.strptime(row["scheduled_for"], "%Y-%m-%d %H:%M") <= now:
            # simulate sending
            content = f"Subject: Reminder #{row['reminder_number']}\n\nThis is an automated reminder."
            _write_outbox("patient@example.com", content)
            df.loc[idx, "sent_at"] = now.strftime("%Y-%m-%d %H:%M")
            sent += 1
    df.to_csv(REMINDERS_CSV, index=False)
    return sent
