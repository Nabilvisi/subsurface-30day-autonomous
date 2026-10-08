# Day 12 — Peng-Robinson Compositional PVT & Dynamic Phase Envelope

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Empirical black-oil correlations fail near retrograde gas-condensate and volatile oil regimes, causing severe errors in surface separator allocation.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Solve the cubic **Peng-Robinson Equation of State (PR-EOS)** using Rachford-Rice flash equilibrium routines across pressure-temperature grids: P = \frac{RT}{v - b} - \frac{a(T)}{v(v + b) + b(v - b)}

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 12 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 12** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 12/30 — Peng-Robinson Compositional PVT & Dynamic Phase Envelope

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Empirical black-oil correlations fail near retrograde gas-condensate and volatile oil regimes, causing severe errors in surface separator allocation.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Solve the cubic **Peng-Robinson Equation of State (PR-EOS)** using Rachford-Rice flash equilibrium routines across pressure-temperature grids: P = \frac{RT}{v - b} - \frac{a(T)}{v(v + b) + b(v - b)}

Reference dataset: Standing-Katz / Glasø Open Thermodynamic Laboratory Benchmarks.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
