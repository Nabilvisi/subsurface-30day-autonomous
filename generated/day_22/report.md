# Day 22 — Time-Series Stuck Pipe Early Warning Anomaly Radar

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Mechanical pack-off and differential pipe sticking give subtle advance warnings on surface sensors that human operators often overlook.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Stream high-frequency sensor traces (Hookload, SPP, Torque, ROP, FlowRate) through rolling sliding-window extractors into an **Isolation Forest anomaly engine**.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 22 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 22** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 22/30 — Time-Series Stuck Pipe Early Warning Anomaly Radar

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Mechanical pack-off and differential pipe sticking give subtle advance warnings on surface sensors that human operators often overlook.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Stream high-frequency sensor traces (Hookload, SPP, Torque, ROP, FlowRate) through rolling sliding-window extractors into an **Isolation Forest anomaly engine**.

Reference dataset: Equinor Volve Real-Time Drilling WITSML Timeseries.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
