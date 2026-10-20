# Day 24 — Dynamic Integrated Nodal Analysis Engine (Inflow vs. Outflow)

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Sizing production tubing without accounting for reservoir depletion causes severe liquid loading and premature well shut-in.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Couple reservoir inflow performance relationships (**Vogel's solution-gas drive**: \frac{q}{q_{max}} = 1 - 0.2\frac{P_{wf}}{P_R} - 0.8\left(\frac{P_{wf}}{P_R}\right)^2 and Darcy's single-phase IPR) with **Beggs-Brill multi-phase vertical lift performance (VLP)**.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 24 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 24** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 24/30 — Dynamic Integrated Nodal Analysis Engine (Inflow vs. Outflow)

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Sizing production tubing without accounting for reservoir depletion causes severe liquid loading and premature well shut-in.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Couple reservoir inflow performance relationships (**Vogel's solution-gas drive**: \frac{q}{q_{max}} = 1 - 0.2\frac{P_{wf}}{P_R} - 0.8\left(\frac{P_{wf}}{P_R}\right)^2 and Darcy's single-phase IPR) with **Beggs-Brill multi-phase vertical lift performance (VLP)**.

Reference dataset: Stanford Open Petroleum Engineering Toolbox / North Sea Production Database.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
