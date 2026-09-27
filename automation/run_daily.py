from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from subsurface_lab.content import linkedin_post
from subsurface_lab.roadmap import load_roadmap
from subsurface_lab.schedule import load_schedule


def materialize(day: int) -> Path:
    roadmap = load_roadmap(ROOT / "Project.md")
    schedule, config = load_schedule(ROOT / "project_config.json")
    spec = roadmap[day]
    out = ROOT / "generated" / f"day_{day:02d}"
    out.mkdir(parents=True, exist_ok=True)
    metadata = {
        "day": day,
        "title": spec.title,
        "pillar": spec.pillar,
        "dataset": spec.dataset,
        "scheduled_release": schedule.release_datetime(day).isoformat(),
        "materialized_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "released",
        "streamlit_entrypoint": "app.py",
        "navigation_hint": f"Preview / browse → Day {day:02d}",
        "source_of_truth": "Project.md",
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    report = f"""# Day {day:02d} — {spec.title}

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
{spec.problem}

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
{spec.physics}

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day {day:02d} to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day {day:02d}** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
{linkedin_post(spec)}
"""
    (out / "report.md").write_text(report, encoding="utf-8")
    return out


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--force-day", type=int, default=None, help="Materialize a specific day (1-30).")
    parser.add_argument("--materialize-all", action="store_true", help="Build release artifacts for all 30 days.")
    args = parser.parse_args()
    schedule, _ = load_schedule(ROOT / "project_config.json")
    if args.materialize_all:
        days = range(1, schedule.duration_days + 1)
    else:
        day = args.force_day if args.force_day is not None else schedule.day_for()
        if day == 0:
            print("Project has not reached Day 01 release time; nothing to materialize.")
            return 0
        if not 1 <= day <= schedule.duration_days:
            raise SystemExit("day must be between 1 and 30")
        days = [day]
    for day in days:
        out = materialize(day)
        print(f"Materialized Day {day:02d}: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())