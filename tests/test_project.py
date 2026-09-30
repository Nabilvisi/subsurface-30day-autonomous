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


def test_day30_dataset_excludes_following_project_sections():
    roadmap = load_roadmap(ROOT / "Project.md")
    assert roadmap[30].dataset == "Equinor Volve Field Integrated Asset Consolidated Dataset."


def test_schedule_boundaries():
    schedule, _ = load_schedule(ROOT / "project_config.json")
    tz = ZoneInfo(schedule.timezone)
    assert schedule.day_for(datetime(2026, 9, 27, 23, 0, tzinfo=tz)) == 0
    assert schedule.day_for(datetime(2026, 9, 28, 0, 5, tzinfo=tz)) == 1
    assert schedule.day_for(datetime(2026, 10, 27, 12, 0, tzinfo=tz)) == 30


def test_day01_dataset_registry():
    from subsurface_lab.data import load_manifest

    manifest = load_manifest(ROOT / "data" / "manifest.json")
    day1 = manifest["01"]
    assert day1["well"] == "15/9-F-1 B"
    assert set(["DEPTH", "GR", "RHOB", "NPHI", "RT"]).issubset(day1["required_columns"])
    assert day1["curve_mapping"]["RACEHM"] == "RT"
