# Day 27 — Multiphase Choke Flow Regimes & API RP 14E Erosional Velocity Alarms

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Operating surface chokes above critical velocities induces sand and fluid droplet impingement that erodes surface flowlines, risking containment loss.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Solve the **Perkins / Gilbert multiphase critical flow boundaries** cross-referenced against the **API RP 14E erosional velocity threshold**: v_e = \frac{c}{\sqrt{\rho_m}}

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 27 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 27** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 27/30 — Multiphase Choke Flow Regimes & API RP 14E Erosional Velocity Alarms

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Operating surface chokes above critical velocities induces sand and fluid droplet impingement that erodes surface flowlines, risking containment loss.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Solve the **Perkins / Gilbert multiphase critical flow boundaries** cross-referenced against the **API RP 14E erosional velocity threshold**: v_e = \frac{c}{\sqrt{\rho_m}}

Reference dataset: Offshore Wellhead Manifold Testing Records (SPE Surface Operations).

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
