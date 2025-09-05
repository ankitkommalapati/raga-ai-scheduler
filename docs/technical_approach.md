## Architecture Overview

A modular Streamlit app orchestrates the full workflow:

- **Data Layer**: CSV/Excel simulate EMR & calendar (`data/`).
- **Business Logic**: `scheduling.py` implements new/returning durations and slot blocking.
- **Orchestration/UI**: `app.py` guides the patient from greeting → lookup → scheduling → confirmation → reminders.
- **Integrations**: `calendar_utils.py` generates `.ics`; `messaging.py` simulates Email/SMS via `outbox/`. Intake form PDF is attached from `forms/`.

## Framework Choice

**LangChain/LangGraph-ready design**: The UI uses deterministic steps for reliability. Hooks can be added to call an LLM for free-text parsing (intent/entity extraction). We favor rule-based parsing for MVP stability, with optional LLM later.

## Integration Strategy

- **Patient DB (EMR)**: `patients.csv` (50 synthetic records) for lookup.
- **Doctor Schedules**: `doctor_schedule.csv` + `.xlsx` with availability. Bookings update availability atomically.
- **Communication**: Simulated email to files under `outbox/` with intake form attached.
- **Data Export**: Admin report export to Excel/CSV in `exports/`.

## Challenges & Solutions

- **No-shows risk**: Three reminders at 72h/24h/2h; the 2nd/3rd are actionable to collect form/confirmation.
- **Excel dependencies**: Graceful fallback to CSV if `openpyxl/xlsxwriter` is missing.
- **Calendar integration**: `.ics` files work cross-calendar without external APIs.
- **Privacy**: No PHI leaves disk; synthetic data only.

## Edge Cases

- New vs returning detection by (name, DOB) exact match; UI allows new record creation automatically if not found.
- Double-booking prevented by atomic availability updates in `doctor_schedule.csv`.
- Input validation for insurance fields (non-empty format) shown in UI.

## Success Criteria

End-to-end booking visible in UI, `.ics` created, emails generated, reminders scheduled, admin export generated — matching the case-study deliverables.
