# Day 25 — Electrical Submersible Pump (ESP) Hydraulic Viscosity Derating Sandbox

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Pumping viscous crudes degrades water-calibrated manufacturer pump curves, drastically lowering head capacity and overheating motors.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Apply the **Hydraulic Institute (ANSI/HI) ESP viscosity correction standard** to recalculate head factor (C_H), rate factor (C_Q), and efficiency factor (C_\eta).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 25 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 25** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 25/30 — Electrical Submersible Pump (ESP) Hydraulic Viscosity Derating Sandbox

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Pumping viscous crudes degrades water-calibrated manufacturer pump curves, drastically lowering head capacity and overheating motors.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Apply the **Hydraulic Institute (ANSI/HI) ESP viscosity correction standard** to recalculate head factor (C_H), rate factor (C_Q), and efficiency factor (C_\eta).

Reference dataset: SPE Artificial Lift ESP Public Performance Testing Data.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
