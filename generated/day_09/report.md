# Day 09 — Multi-Segment Decline Curve Analysis (DCA) & EUR Forecaster

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Traditional Arps hyperbolic equations severely over-predict Estimated Ultimate Recovery (EUR) in unconventional low-permeability reservoirs by ignoring late-stage boundary-dominated flow transitions.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Implement **Arps Modified Hyperbolic** (with terminal decline rate D_t), **Duong**, and **Stretched Exponential (SEPD)** models with auto-fitting via Nelder-Mead optimization: q(t) = \frac{q_i}{(1 + b D_i t)^{1/b}} \quad \text{for } D(t) > D_t; \quad q(t) = q_{lim} e^{-D_t (t - t_{lim})} \quad \text{for } D(t) \le D_t

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 09 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 09** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 09/30 — Multi-Segment Decline Curve Analysis (DCA) & EUR Forecaster

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Traditional Arps hyperbolic equations severely over-predict Estimated Ultimate Recovery (EUR) in unconventional low-permeability reservoirs by ignoring late-stage boundary-dominated flow transitions.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Implement **Arps Modified Hyperbolic** (with terminal decline rate D_t), **Duong**, and **Stretched Exponential (SEPD)** models with auto-fitting via Nelder-Mead optimization: q(t) = \frac{q_i}{(1 + b D_i t)^{1/b}} \quad \text{for } D(t) > D_t; \quad q(t) = q_{lim} e^{-D_t (t - t_{lim})} \quad \text{for } D(t) \le D_t

Reference dataset: EIA Eagle Ford Public Production Time-Series Data.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
