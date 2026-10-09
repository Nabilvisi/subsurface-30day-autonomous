# Day 13 — 1D Buckley-Leverett Immiscible Displacement Shock-Wave Tracker

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Waterflood front advance calculations require solving hyperbolic PDEs with discontinuous saturation shocks that traditional finite-difference methods artificially smear.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Solve the **Buckley-Leverett equation** using Corey relative permeability models, constructing the Welge tangent line to evaluate shock-front saturation (S_{wf}): \left(\frac{\partial S_w}{\partial t}\right)_x + \frac{q_t}{A\phi} \left(\frac{df_w}{dS_w}\right) \left(\frac{\partial S_w}{\partial x}\right)_t = 0

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 13 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 13** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 13/30 — 1D Buckley-Leverett Immiscible Displacement Shock-Wave Tracker

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Waterflood front advance calculations require solving hyperbolic PDEs with discontinuous saturation shocks that traditional finite-difference methods artificially smear.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Solve the **Buckley-Leverett equation** using Corey relative permeability models, constructing the Welge tangent line to evaluate shock-front saturation (S_{wf}): \left(\frac{\partial S_w}{\partial t}\right)_x + \frac{q_t}{A\phi} \left(\frac{df_w}{dS_w}\right) \left(\frac{\partial S_w}{\partial x}\right)_t = 0

Reference dataset: SPE 10 Comparative Solution Layer 1 Petrophysical Matrix.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
