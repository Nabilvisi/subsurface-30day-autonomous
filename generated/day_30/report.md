# Day 30 — Capstone: Integrated Asset Production Digital Twin

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Siloed workflows between Petrophysics, Reservoir, Drilling, and Production obscure systemic asset bottlenecks.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Build an end-to-end subsurface dashboard uniting formation properties (Day 01), material balance pressures (Day 10), trajectory clearances (Day 18), and wellhead nodal curves (Day 24).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 30 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 30** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 30/30 — Capstone: Integrated Asset Production Digital Twin

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Siloed workflows between Petrophysics, Reservoir, Drilling, and Production obscure systemic asset bottlenecks.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Build an end-to-end subsurface dashboard uniting formation properties (Day 01), material balance pressures (Day 10), trajectory clearances (Day 18), and wellhead nodal curves (Day 24).

Reference dataset: Equinor Volve Field Integrated Asset Consolidated Dataset.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
