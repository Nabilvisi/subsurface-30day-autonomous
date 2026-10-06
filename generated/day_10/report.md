# Day 10 — Havlena-Odeh Dynamic Material Balance Diagnostic Engine

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Identifying reservoir drive mechanisms (solution-gas, gas-cap expansion, water drive, pore volume compaction) from production histories is prone to mathematical non-uniqueness.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Formulate the generalized Havlena-Odeh material balance equation: F = N(E_o + m E_g + E_{fw}) + W_e and fit linear regression coordinates (F/E_t vs. W_e/E_t).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 10 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 10** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 10/30 — Havlena-Odeh Dynamic Material Balance Diagnostic Engine

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Identifying reservoir drive mechanisms (solution-gas, gas-cap expansion, water drive, pore volume compaction) from production histories is prone to mathematical non-uniqueness.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Formulate the generalized Havlena-Odeh material balance equation: F = N(E_o + m E_g + E_{fw}) + W_e and fit linear regression coordinates (F/E_t vs. W_e/E_t).

Reference dataset: Equinor Volve Field Static Pressure & Cumulative Production Reports.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
