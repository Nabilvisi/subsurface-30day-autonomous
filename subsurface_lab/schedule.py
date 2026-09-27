from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import json


@dataclass(frozen=True)
class ProjectSchedule:
    start_date: date
    timezone: str
    duration_days: int = 30
    release_hour_local: int = 0
    release_minute_local: int = 5

    @property
    def end_date(self) -> date:
        return self.start_date + timedelta(days=self.duration_days - 1)

    def release_datetime(self, day: int) -> datetime:
        if day < 1 or day > self.duration_days:
            raise ValueError("day outside project duration")
        d = self.start_date + timedelta(days=day - 1)
        return datetime.combine(
            d,
            time(self.release_hour_local, self.release_minute_local),
            tzinfo=ZoneInfo(self.timezone),
        )

    def day_for(self, when: datetime | None = None) -> int:
        tz = ZoneInfo(self.timezone)
        now = when.astimezone(tz) if when else datetime.now(tz)
        if now < self.release_datetime(1):
            return 0
        if now >= self.release_datetime(self.duration_days):
            return self.duration_days
        delta = now.date() - self.start_date
        day = delta.days + 1
        if now < self.release_datetime(day):
            day -= 1
        return max(0, min(self.duration_days, day))


def load_schedule(config_path: str | Path) -> tuple[ProjectSchedule, dict]:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    schedule = ProjectSchedule(
        start_date=date.fromisoformat(config["start_date"]),
        timezone=config.get("timezone", "Asia/Jakarta"),
        duration_days=int(config.get("duration_days", 30)),
        release_hour_local=int(config.get("release_hour_local", 0)),
        release_minute_local=int(config.get("release_minute_local", 5)),
    )
    return schedule, config
