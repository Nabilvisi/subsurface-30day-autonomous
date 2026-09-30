from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class DaySpec:
    day: int
    title: str
    pillar: str
    problem: str
    physics: str
    ui: str
    dataset: str


def _clean(value: str) -> str:
    value = re.sub(r"\$\$(.*?)\$\$", lambda m: m.group(1), value, flags=re.S)
    value = re.sub(r"\$(.*?)\$", lambda m: m.group(1), value)
    return re.sub(r"\s+", " ", value).strip()


def load_roadmap(project_md: str | Path) -> dict[int, DaySpec]:
    text = Path(project_md).read_text(encoding="utf-8")
    lines = text.splitlines()
    specs: dict[int, DaySpec] = {}
    current_pillar = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("### Pillar "):
            current_pillar = line.removeprefix("### ").strip()
        m = re.match(r"#### Day (\d{2}): (.+)", line)
        if not m:
            i += 1
            continue
        day = int(m.group(1))
        title = m.group(2).strip()
        block: list[str] = []
        i += 1
        while i < len(lines) and not re.match(r"^#{1,4}\s|^---\s*$", lines[i]):
            block.append(lines[i])
            i += 1
        joined = "\n".join(block)

        def field(name: str) -> str:
            p = re.search(rf"\* \*\*{re.escape(name)}:\*\*\s*(.*?)(?=\n\* \*\*|\Z)", joined, flags=re.S)
            return _clean(p.group(1)) if p else ""

        specs[day] = DaySpec(
            day=day,
            title=title,
            pillar=current_pillar,
            problem=field("Problem"),
            physics=field("Physics & Math"),
            ui=field("UI & Interactivity"),
            dataset=field("Dataset"),
        )
    if len(specs) != 30:
        raise ValueError(f"Expected 30 roadmap days, parsed {len(specs)}")
    return specs
