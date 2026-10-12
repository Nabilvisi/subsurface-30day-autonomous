# Day 16 — Gas-Condensate Well Deliverability & Liquid Loading Estimator

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Liquid loading in gas-condensate wells abruptly kills flow when bottomhole gas velocities drop below critical droplet lifting thresholds.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Couple Cullender-Smith wellbore pressure traverse equations with the **Turner and Coleman critical gas velocity formulations**: v_c = \frac{1.593 \cdot \sigma^{1/4} (\rho_L - \rho_g)^{1/4}}{\rho_g^{1/2}}

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 16 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 16** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 16/30 — Gas-Condensate Well Deliverability & Liquid Loading Estimator

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Liquid loading in gas-condensate wells abruptly kills flow when bottomhole gas velocities drop below critical droplet lifting thresholds.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Couple Cullender-Smith wellbore pressure traverse equations with the **Turner and Coleman critical gas velocity formulations**: v_c = \frac{1.593 \cdot \sigma^{1/4} (\rho_L - \rho_g)^{1/4}}{\rho_g^{1/2}}

Reference dataset: Offshore Gas-Condensate Production Test Repository.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
