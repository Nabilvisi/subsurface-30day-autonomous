# Day 26 — Constrained Field-Scale Gas Lift Allocation Optimizer

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Distributing compression gas evenly among wells is inefficient; gas must be allocated based on marginal production gains to maximize recovery.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Construct non-linear Gas Lift Performance Curves (GLPC) for multi-well pads and solve the allocation problem: \max \sum Q_{o,i}(q_{inj,i}) \quad \text{subject to} \quad \sum q_{inj,i} \le Q_{gas,max} using Sequential Least Squares Programming (SLSQP).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 26 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 26** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 26/30 — Constrained Field-Scale Gas Lift Allocation Optimizer

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Distributing compression gas evenly among wells is inefficient; gas must be allocated based on marginal production gains to maximize recovery.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Construct non-linear Gas Lift Performance Curves (GLPC) for multi-well pads and solve the allocation problem: \max \sum Q_{o,i}(q_{inj,i}) \quad \text{subject to} \quad \sum q_{inj,i} \le Q_{gas,max} using Sequential Least Squares Programming (SLSQP).

Reference dataset: Equinor Volve Field Gas Lift Production Well Tests.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
