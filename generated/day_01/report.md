# Day 01 — Dynamic Shaly-Sand Water Saturation Matrix & Pickett Crossplot

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Clay electrical conductivity (CEC) causes Archie’s equation to drastically overestimate water saturation (S_w), leading operators to bypass commercial hydrocarbons in laminated or dispersed shaly sands.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Compute Gamma Ray shale volume (V_{sh} = \frac{GR - GR_{min}}{GR_{max} - GR_{min}} with Larionov correction), effective porosity (\phi_e = \phi_t (1 - V_{sh})), and run **Archie**, **Simandoux**: \frac{1}{R_t} = \frac{V_{sh} S_w}{R_{sh}} + \frac{\phi_e^m S_w^n}{a R_w (1 - V_{sh})} and **Indonesian (Poupon-Leveaux)** models side-by-side.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 01 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 01** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 01/30 — Dynamic Shaly-Sand Water Saturation Matrix & Pickett Crossplot

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Clay electrical conductivity (CEC) causes Archie’s equation to drastically overestimate water saturation (S_w), leading operators to bypass commercial hydrocarbons in laminated or dispersed shaly sands.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Compute Gamma Ray shale volume (V_{sh} = \frac{GR - GR_{min}}{GR_{max} - GR_{min}} with Larionov correction), effective porosity (\phi_e = \phi_t (1 - V_{sh})), and run **Archie**, **Simandoux**: \frac{1}{R_t} = \frac{V_{sh} S_w}{R_{sh}} + \frac{\phi_e^m S_w^n}{a R_w (1 - V_{sh})} and **Indonesian (Poupon-Leveaux)** models side-by-side.

Reference dataset: Equinor Volve Field Well `15/9-F-1 B` (Open LAS 2.0).

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
