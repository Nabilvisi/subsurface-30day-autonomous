from __future__ import annotations

from .roadmap import DaySpec


def linkedin_post(spec: DaySpec) -> str:
    return (
        f"Day {spec.day:02d}/30 — {spec.title}\n\n"
        f"Today I built an interactive subsurface engineering workflow around a practical bottleneck: "
        f"{spec.problem}\n\n"
        f"The implementation is physics-first, with the governing formulation encoded directly into a "
        f"reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load "
        f"benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation "
        f"as a static spreadsheet.\n\n"
        f"Technical focus: {spec.physics}\n\n"
        f"Reference dataset: {spec.dataset}\n\n"
        "#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering "
        "#ProductionEngineering #DataScience #Python #Streamlit #Plotly"
    )
