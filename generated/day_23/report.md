# Day 23 — 1D Pore Pressure Prediction & Safe Mud Weight Operating Window

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Under-balanced drilling risks wellbore influxes, while over-balanced drilling causes differential sticking and formation damage.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Build continuous Overburden Stress profiles via density integration and calculate formation pore pressure (P_p) via **Eaton’s sonic and resistivity models**: P_p = \sigma_v - (\sigma_v - P_h)\left(\frac{\Delta t_n}{\Delta t}\right)^3

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 23 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 23** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 23/30 — 1D Pore Pressure Prediction & Safe Mud Weight Operating Window

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Under-balanced drilling risks wellbore influxes, while over-balanced drilling causes differential sticking and formation damage.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Build continuous Overburden Stress profiles via density integration and calculate formation pore pressure (P_p) via **Eaton’s sonic and resistivity models**: P_p = \sigma_v - (\sigma_v - P_h)\left(\frac{\Delta t_n}{\Delta t}\right)^3

Reference dataset: BOEM Gulf of Mexico Deepwater Well Log Library.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
