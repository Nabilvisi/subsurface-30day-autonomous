# Day 21 — Real-Time Kick Detection & Driller’s Method Well-Kill Simulator

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Influx of formation fluids (kicks) must be circulated out using precise drillpipe pressure schedules; mistakes lead to casing shoe fracture or blowouts.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Simulate dynamic two-phase kick migration and pressure responses during the two circulations of the **Driller's Method**.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 21 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 21** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 21/30 — Real-Time Kick Detection & Driller’s Method Well-Kill Simulator

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Influx of formation fluids (kicks) must be circulated out using precise drillpipe pressure schedules; mistakes lead to casing shoe fracture or blowouts.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Simulate dynamic two-phase kick migration and pressure responses during the two circulations of the **Driller's Method**.

Reference dataset: Managed Pressure Drilling (MPD) Influx Simulation Suite.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
