# Day 17 — Mechanical Specific Energy (MSE) & Real-Time Bit Founder Optimizer

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Inefficient drilling operations waste mechanical energy through bit vibrations and thermal balling, drastically inflating Non-Productive Time (NPT).

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Calculate **Teale’s Mechanical Specific Energy**: \text{MSE} = \frac{\text{WOB}}{A_B} + \frac{120\pi \cdot \text{RPM} \cdot T}{A_B \cdot \text{ROP}} benchmarked against formation unconfined compressive strength (UCS).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 17 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 17** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 17/30 — Mechanical Specific Energy (MSE) & Real-Time Bit Founder Optimizer

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Inefficient drilling operations waste mechanical energy through bit vibrations and thermal balling, drastically inflating Non-Productive Time (NPT).

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Calculate **Teale’s Mechanical Specific Energy**: \text{MSE} = \frac{\text{WOB}}{A_B} + \frac{120\pi \cdot \text{RPM} \cdot T}{A_B \cdot \text{ROP}} benchmarked against formation unconfined compressive strength (UCS).

Reference dataset: Equinor Volve High-Frequency 1-Hz Drilling Parameter Records.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
