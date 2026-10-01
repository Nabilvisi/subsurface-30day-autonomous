# Day 05 — Dynamic Rock Physics Shear Velocity ($V_s$) & Anisotropy Simulator

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Shear velocity logs (V_s) are missing in over 70% of legacy wells, preventing pre-drill geomechanical stress analysis and seismic AVO modeling.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Estimate V_s from V_p, density, and mineral fractions using Castagna's Mudrock line (V_p = 1.16 V_s + 1.36), Greenberg-Castagna, and an optimized Random Forest regressor.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 05 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 05** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 05/30 — Dynamic Rock Physics Shear Velocity ($V_s$) & Anisotropy Simulator

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Shear velocity logs (V_s) are missing in over 70% of legacy wells, preventing pre-drill geomechanical stress analysis and seismic AVO modeling.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Estimate V_s from V_p, density, and mineral fractions using Castagna's Mudrock line (V_p = 1.16 V_s + 1.36), Greenberg-Castagna, and an optimized Random Forest regressor.

Reference dataset: Kansas Geological Survey (KGS) Dipole Sonic Database.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
