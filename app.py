from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from subsurface_lab.data import load_day_dataset
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
    if "data_mode" not in st.session_state:
        st.session_state["data_mode"] = "auto"

    c_auto, c_demo = st.columns(2)
    with c_auto:
        if st.button("Use Auto Data", type="primary", use_container_width=True):
            st.session_state["data_mode"] = "auto"
            st.session_state.pop("uploaded_df", None)
    with c_demo:
        if st.button("Use Demo Data", use_container_width=True):
            st.session_state["data_mode"] = "benchmark"
            st.session_state.pop("uploaded_df", None)

    upload = st.file_uploader("Optional field data", type=["csv", "las"], help="Uploaded CSV/LAS overrides the automatic dataset for this session.")
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

problem_tab, app_tab = st.tabs([
    "1 · Technical Problem",
    "3 · Interactive Application",
])

with problem_tab:
    st.markdown("### Technical problem & domain bottleneck")
    st.write(spec.problem)
    st.markdown("### Intended interactivity")
    st.write(spec.ui)

with app_tab:
    data_mode = st.session_state.get("data_mode", "auto")
    external_df = None

    if data_mode == "uploaded":
        external_df = st.session_state.get("uploaded_df")
        if external_df is not None:
            external_df.attrs["source_label"] = "user-uploaded field data"
            external_df.attrs["source_kind"] = "upload"
        st.caption("Dataset mode: user upload")
    elif data_mode == "benchmark":
        st.caption("Dataset mode: deterministic built-in benchmark")
    else:
        external_df, dataset_meta = load_day_dataset(selected_day, allow_remote=True)
        if external_df is not None:
            if dataset_meta.get("status") == "repository":
                st.success(f"Automatic dataset: {dataset_meta.get('label')} · {dataset_meta.get('rows', 0):,} rows · repository copy")
            else:
                st.success(f"Automatic dataset: {dataset_meta.get('label')} · {dataset_meta.get('rows', 0):,} rows · verified remote source")
                st.caption("The repository copy has not been materialized yet; the app is using the verified source directly and caching it for this process.")
        else:
            st.warning("Automatic real dataset unavailable. The lab has fallen back to its deterministic synthetic benchmark.")
            if dataset_meta.get("reason"):
                st.caption(dataset_meta["reason"])

    render_lab(selected_day, external_df)
