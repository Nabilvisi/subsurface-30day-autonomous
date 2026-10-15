# Day 19 — Dynamic Wellbore Hydraulics & Surge/Swab Pressure Window Solver

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Tripping drillstrings too quickly causes swab pressures that pull hydrocarbons into the well (kicks) or surge pressures that fracture the formation (losses).

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Solve non-Newtonian **Herschel-Bulkley and Bingham Plastic** fluid flow through concentric and eccentric drillpipe-casing annuli.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 19 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 19** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 19/30 — Dynamic Wellbore Hydraulics & Surge/Swab Pressure Window Solver

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Tripping drillstrings too quickly causes swab pressures that pull hydrocarbons into the well (kicks) or surge pressures that fracture the formation (losses).

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Solve non-Newtonian **Herschel-Bulkley and Bingham Plastic** fluid flow through concentric and eccentric drillpipe-casing annuli.

Reference dataset: SPE Drilling Hydraulics & Rheology Benchmark Tables.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
