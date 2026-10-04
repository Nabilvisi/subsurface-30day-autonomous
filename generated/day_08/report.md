# Day 08 — Interactive Petrophysical Cutoffs & Pay-Summary Sandbox

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Net-Pay calculations depend heavily on arbitrary cutoffs (V_{sh,max}, \phi_{min}, S_{w,max}), leading to multi-million-dollar variance in reserves estimates.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Continuous integration of Net-to-Gross (NTG), Net Sand, and Net Pay across entire formations based on user-defined triple-parameter gates.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 08 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 08** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 08/30 — Interactive Petrophysical Cutoffs & Pay-Summary Sandbox

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Net-Pay calculations depend heavily on arbitrary cutoffs (V_{sh,max}, \phi_{min}, S_{w,max}), leading to multi-million-dollar variance in reserves estimates.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Continuous integration of Net-to-Gross (NTG), Net Sand, and Net Pay across entire formations based on user-defined triple-parameter gates.

Reference dataset: Equinor Volve Well `15/9-F-12` Clean Formation Interval.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
