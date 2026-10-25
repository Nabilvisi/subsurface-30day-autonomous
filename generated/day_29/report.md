# Day 29 — Gas Well Liquid Loading Critical Velocity Profiler

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
As gas flow rates decline, the gas phase can no longer lift liquid droplets to the surface, causing hydrostatic column loading and well death.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Implement the **Turner, Coleman, and Li models** to calculate critical superficial gas velocity profiles along tubing depth strings.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 29 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 29** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 29/30 — Gas Well Liquid Loading Critical Velocity Profiler

Today I built an interactive subsurface engineering workflow around a practical bottleneck: As gas flow rates decline, the gas phase can no longer lift liquid droplets to the surface, causing hydrostatic column loading and well death.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Implement the **Turner, Coleman, and Li models** to calculate critical superficial gas velocity profiles along tubing depth strings.

Reference dataset: Eagle Ford / Barnett Shale Gas Production Records.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
