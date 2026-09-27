from __future__ import annotations

from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
import json

import numpy as np
import pandas as pd
import lasio

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "manifest.json"

ALIASES = {
    "DEPTH": ["DEPTH", "DEPT", "MD"],
    "GR": ["GR", "GR_EDTC", "GR_ARC", "GAMMA"],
    "RHOB": ["RHOB", "RHOZ", "ZDEN", "DEN"],
    "NPHI": ["NPHI", "TNPH", "NPOR", "NEUT"],
    "RT": ["RT", "RACEHM", "AT90", "ILD", "LLD", "RESD", "RDEP", "HDRS"],
    "CALI": ["CALI", "HCAL", "CAL", "C1", "C2"],
}


def load_manifest(path: str | Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _standardize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df.columns = [str(c).strip().upper() for c in df.columns]
    rename: dict[str, str] = {}
    for standard, candidates in ALIASES.items():
        if standard in df.columns:
            continue
        for candidate in candidates:
            if candidate in df.columns:
                rename[candidate] = standard
                break
    if rename:
        df = df.rename(columns=rename)
    return df


def _clean_frame(frame: pd.DataFrame, required: list[str]) -> pd.DataFrame:
    df = _standardize_columns(frame)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.replace([-999.25, -999.0, -9999.0, -99999.0], np.nan)
    if not all(col in df.columns for col in required):
        missing = [col for col in required if col not in df.columns]
        raise ValueError(f"Dataset is missing standardized columns: {missing}")
    df = df.dropna(subset=required).copy()
    if "RT" in df.columns:
        df = df[df["RT"] > 0]
    if "DEPTH" in df.columns:
        df = df.sort_values("DEPTH").drop_duplicates("DEPTH")
    return df.reset_index(drop=True)


def _read_las_text(text: str, required: list[str]) -> pd.DataFrame:
    las = lasio.read(StringIO(text), ignore_header_errors=True)
    frame = las.df().reset_index()
    return _clean_frame(frame, required)


def _read_local(path: Path, required: list[str]) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return _clean_frame(pd.read_csv(path), required)
    if path.suffix.lower() == ".las":
        return _read_las_text(path.read_text(encoding="utf-8", errors="replace"), required)
    raise ValueError(f"Unsupported dataset type: {path.suffix}")


@lru_cache(maxsize=8)
def _download_text(url: str) -> str:
    request = Request(
        url,
        headers={"User-Agent": "subsurface-30day-autonomous/1.0"},
    )
    with urlopen(request, timeout=45) as response:
        payload = response.read()
    return payload.decode("utf-8", errors="replace")


def load_day_dataset(day: int, allow_remote: bool = True) -> tuple[pd.DataFrame | None, dict[str, Any]]:
    manifest = load_manifest()
    entry = manifest.get(f"{day:02d}")
    if not entry:
        return None, {"status": "unconfigured", "day": day}

    required = [str(x).upper() for x in entry.get("required_columns", [])]
    local_rel = entry.get("local_path")
    local_path = ROOT / local_rel if local_rel else None

    if local_path and local_path.exists():
        try:
            frame = _read_local(local_path, required)
            frame.attrs["source_label"] = entry.get("label", f"Day {day:02d} persistent dataset")
            frame.attrs["source_kind"] = "repository"
            frame.attrs["source_url"] = entry.get("source_url", "")
            return frame, {
                "status": "repository",
                "path": local_rel,
                "rows": len(frame),
                "label": frame.attrs["source_label"],
                "source_url": frame.attrs["source_url"],
            }
        except Exception as exc:
            local_error = str(exc)
    else:
        local_error = "local dataset not materialized"

    if allow_remote and entry.get("remote_url"):
        try:
            text = _download_text(entry["remote_url"])
            frame = _read_las_text(text, required)
            frame.attrs["source_label"] = entry.get("label", f"Day {day:02d} verified remote dataset")
            frame.attrs["source_kind"] = "verified-remote"
            frame.attrs["source_url"] = entry.get("source_url", entry["remote_url"])
            return frame, {
                "status": "verified-remote",
                "rows": len(frame),
                "label": frame.attrs["source_label"],
                "source_url": frame.attrs["source_url"],
                "local_error": local_error,
            }
        except Exception as exc:
            return None, {
                "status": "fallback",
                "reason": f"repository: {local_error}; remote: {exc}",
                "label": entry.get("label", f"Day {day:02d} dataset"),
            }

    return None, {
        "status": "fallback",
        "reason": local_error,
        "label": entry.get("label", f"Day {day:02d} dataset"),
    }


def materialize_day_dataset(day: int, overwrite: bool = False) -> tuple[Path | None, dict[str, Any]]:
    manifest = load_manifest()
    entry = manifest.get(f"{day:02d}")
    if not entry or not entry.get("local_path"):
        return None, {"status": "unconfigured", "day": day}

    target = ROOT / entry["local_path"]
    if target.exists() and not overwrite:
        frame = _read_local(target, [str(x).upper() for x in entry.get("required_columns", [])])
        return target, {"status": "exists", "rows": len(frame)}

    frame, meta = load_day_dataset(day, allow_remote=True)
    if frame is None:
        return None, meta

    target.parent.mkdir(parents=True, exist_ok=True)
    export_columns = entry.get("export_columns") or list(frame.columns)
    export_columns = [c for c in export_columns if c in frame.columns]
    frame[export_columns].to_csv(target, index=False)
    return target, {**meta, "status": "materialized", "path": str(target.relative_to(ROOT))}
