from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from subsurface_lab.data import materialize_day_dataset


def main() -> int:
    target, meta = materialize_day_dataset(1)
    if target is None:
        print(f"Day-01 data bootstrap failed: {meta}")
        return 1
    print(f"Day-01 data ready: {target} | {meta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
