from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from subsurface_lab.roadmap import load_roadmap
from subsurface_lab.schedule import load_schedule

ROOT = Path(__file__).resolve().parents[1]


def test_roadmap_has_30_days():
    roadmap = load_roadmap(ROOT / "Project.md")
    assert list(roadmap) == list(range(1, 31))
    assert all(roadmap[d].title for d in roadmap)


def test_schedule_boundaries():
    schedule, _ = load_schedule(ROOT / "project_config.json")
    tz = ZoneInfo(schedule.timezone)
    assert schedule.day_for(datetime(2026, 9, 27, 23, 0, tzinfo=tz)) == 0
    assert schedule.day_for(datetime(2026, 9, 28, 0, 5, tzinfo=tz)) == 1
    assert schedule.day_for(datetime(2026, 10, 27, 12, 0, tzinfo=tz)) == 30
