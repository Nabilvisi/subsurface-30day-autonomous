from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

import pandas as pd
import streamlit as st

from subsurface_lab.content import linkedin_post
from subsurface_lab.labs import render_lab
from subsurface_lab.roadmap import load_roadmap
from subsurface_lab.schedule import load_schedule

ROOT = Path(__file__).resolve().parent
ROADMAP = load_roadmap(ROOT / "Project.md")
SCHEDULE, CONFIG = load_schedule(ROOT / "project_config.json")

st.set_page_config(
    page_title="30-Day Autonomous Subsurface Lab",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("30-Day Autonomous Subsurface Engineering Lab")
st.caption("Physics-first subsurface engineering • Streamlit • Plotly • autonomous daily release")

now = datetime.now(ZoneInfo(SCHEDULE.timezone))
auto_day = SCHEDULE.day_for(now)
allow_preview = bool(CONFIG.get("allow_preview_future_days", True))

with st.sidebar:
    st.header("Project Control")
    st.write(f"**Local time:** {now:%Y-%m-%d %H:%M} {SCHEDULE.timezone}")
    st.write(f"**Project:** {SCHEDULE.start_date.isoformat()} → {SCHEDULE.end_date.isoformat()}")
    progress = auto_day / SCHEDULE.duration_days
    st.progress(progress, text=f"Autonomous release progress: {auto_day}/{SCHEDULE.duration_days}")

    mode = st.radio("Navigation", ["Autonomous current day", "Preview / browse"] if allow_preview else ["Autonomous current day"])
    if mode == "Autonomous current day":
        selected_day = max(auto_day, 1)
    else:
        selected_day = st.selectbox(
            "Day",
            options=list(range(1, 31)),
            format_func=lambda d: f"Day {d:02d} — {ROADMAP[d].title}",
            index=max(auto_day - 1, 0),
        )

    st.divider()
    st.subheader("Data")
    if st.button("Load Benchmark / Demo Data", type="primary", use_container_width=True):
        st.session_state["data_mode"] = "benchmark"
        st.session_state.pop("uploaded_df", None)

    upload = st.file_uploader("Optional field data", type=["csv", "las"], help="CSV is read directly. LAS requires lasio and is converted to a DataFrame.")
    if upload is not None:
        try:
            if upload.name.lower().endswith(".csv"):
                st.session_state["uploaded_df"] = pd.read_csv(upload)
            else:
                import lasio
                las = lasio.read(upload)
                frame = las.df().reset_index()
                frame.columns = [str(c).upper() for c in frame.columns]
                if "DEPT" in frame.columns and "DEPTH" not in frame.columns:
                    frame = frame.rename(columns={"DEPT": "DEPTH"})
                st.session_state["uploaded_df"] = frame
            st.session_state["data_mode"] = "uploaded"
        except Exception as exc:
            st.error(f"Could not parse upload: {exc}")

    st.divider()
    st.subheader("Release Calendar")
    for day in range(1, 31):
        status = "LIVE" if day <= auto_day else "scheduled"
        when = SCHEDULE.release_datetime(day)
        st.caption(f"{day:02d} · {when:%d %b} · {status}")

spec = ROADMAP[selected_day]
if auto_day == 0 and mode == "Autonomous current day":
    st.info(f"Day 01 releases automatically on {SCHEDULE.release_datetime(1):%A, %d %B %Y at %H:%M} ({SCHEDULE.timezone}). Preview mode is already available.")
elif selected_day > auto_day and mode == "Preview / browse":
    st.warning(f"Previewing Day {selected_day:02d}; autonomous release is currently at Day {auto_day:02d}.")

st.subheader(f"Day {selected_day:02d} — {spec.title}")
st.caption(f"{spec.pillar} · Reference dataset: {spec.dataset}")

problem_tab, physics_tab, app_tab, social_tab, ops_tab = st.tabs([
    "1 · Technical Problem",
    "2 · Physics & Math",
    "3 · Interactive Application",
    "4 · LinkedIn Output",
    "Automation / Ops",
])

with problem_tab:
    st.markdown("### Technical problem & domain bottleneck")
    st.write(spec.problem)
    st.markdown("### Intended interactivity")
    st.write(spec.ui)

with physics_tab:
    st.markdown("### First-principles formulation")
    st.write(spec.physics)
    st.info("The live calculator below is an educational engineering implementation. Validate correlations, units, PVT assumptions, and calibration against field procedures before operational use.")

with app_tab:
    uploaded_df = st.session_state.get("uploaded_df") if st.session_state.get("data_mode") == "uploaded" else None
    render_lab(selected_day, uploaded_df)

with social_tab:
    st.markdown("### Ready-to-publish LinkedIn post")
    post = linkedin_post(spec)
    st.text_area("Post", value=post, height=330)
    st.download_button("Download post (.txt)", data=post, file_name=f"day_{selected_day:02d}_linkedin.txt", mime="text/plain")

with ops_tab:
    st.markdown("### Autonomous release mechanism")
    st.write(
        "The app derives the live day from `project_config.json`. A GitHub Actions cron job runs daily, materializes the day's report under `generated/`, runs tests/security checks, and commits the release artifact. Streamlit then reflects the new live day from the same repository."
    )
    manifest_path = ROOT / "generated" / f"day_{selected_day:02d}" / "metadata.json"
    if manifest_path.exists():
        st.success("Daily release artifact exists.")
        st.json(json.loads(manifest_path.read_text(encoding="utf-8")))
    else:
        st.info("No committed release artifact for this day yet. The interactive lab is still available in preview mode.")
    st.code(
        "python automation/run_daily.py --force-day 1\n"
        "streamlit run app.py\n"
        "python security_gate.py app.py",
        language="bash",
    )