# 30-Day Autonomous Subsurface Engineering Lab

This repository converts `Project.md` into a 30-day autonomous Streamlit project. All 30 interactive labs are prebuilt; a date-based scheduler releases one per day and a GitHub Actions cron materializes the corresponding report under `generated/`.

## What is autonomous

- Project start: **2026-09-28, 00:05 Asia/Jakarta** by default.
- Day 01 through Day 30 are derived from the local calendar, not from manual commands.
- GitHub Actions runs every day at **00:05 Asia/Jakarta** using a timezone-aware schedule and calls `automation/run_daily.py`.
- The job runs tests and the static security gate before committing the daily artifact.
- Streamlit reads the same configuration and automatically opens the current live day.
- Future days remain available through Preview mode if `allow_preview_future_days` is true.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Test the automation now

```bash
pytest -q
python security_gate.py app.py subsurface_lab/labs.py automation/run_daily.py
python automation/run_daily.py --force-day 1
python automation/run_daily.py --materialize-all
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload this project.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the entry point to `app.py`.
4. Keep GitHub Actions enabled so the daily cron can write release artifacts.
5. Pushes made by the release workflow update the repository; the Streamlit app continues to determine the live day from `project_config.json`.

No API key is required. The project is deterministic and based on the engineering roadmap already supplied in `Project.md`.

## Change the start date

Edit `project_config.json`:

```json
{
  "start_date": "2026-09-28",
  "timezone": "Asia/Jakarta",
  "duration_days": 30,
  "release_hour_local": 0,
  "release_minute_local": 5
}
```

If the timezone changes, also update the timezone-aware schedule in `.github/workflows/daily_release.yml`.

## Architecture

- `app.py` — master Streamlit UI and current-day routing.
- `subsurface_lab/roadmap.py` — parses all 30 day specifications directly from `Project.md`.
- `subsurface_lab/labs.py` — interactive engineering labs for Days 01–30.
- `subsurface_lab/schedule.py` — timezone-aware daily release logic.
- `automation/run_daily.py` — creates daily report/metadata artifacts.
- `security_gate.py` — scans for hardcoded secrets, dangerous builtins, unsafe imports, and `shell=True`.
- `.github/workflows/daily_release.yml` — autonomous daily runner.
- `generated/day_XX/` — released report artifacts.

## Engineering-use note

The applications are portfolio/research-grade interactive implementations. They are not substitutes for field-validated commercial simulators, calibrated PVT/SCAL models, well-control procedures, or approved operating envelopes. Validate equations, units, correlations, and calibration before operational use.
