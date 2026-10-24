# Day 28 — Horizontal Well Inflow Control Device (ICD) Equalization Profiler

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Heel-to-toe wellbore friction in long horizontal completions causes uneven inflow, leading to premature water or gas breakthrough at the heel.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Model fluid inflow along segmented horizontal wellbores using coupled reservoir influx and pipe hydraulic pressure-drop equations, comparing open-hole completions against autonomous ICDs (AICD).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 28 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 28** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 28/30 — Horizontal Well Inflow Control Device (ICD) Equalization Profiler

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Heel-to-toe wellbore friction in long horizontal completions causes uneven inflow, leading to premature water or gas breakthrough at the heel.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Model fluid inflow along segmented horizontal wellbores using coupled reservoir influx and pipe hydraulic pressure-drop equations, comparing open-hole completions against autonomous ICDs (AICD).

Reference dataset: SPE Horizontal Completion & ICD Benchmark Suite.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
