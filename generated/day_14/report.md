# Day 14 — Waterflood Conformance Diagnostic (Chan Plots & Interactive Hall Plot)

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Determining whether premature water production is driven by mechanical channeling (thief zones) or normal coning dictates whether costly polymer-shutoff treatments are required.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Calculate **Chan’s Water-Oil Ratio (WOR) and WOR derivative curves** (d(\text{WOR})/dt) coupled with **Hall plot slope tracking**: \int p_{inj} dt \quad \text{vs.} \quad W_i

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 14 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 14** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 14/30 — Waterflood Conformance Diagnostic (Chan Plots & Interactive Hall Plot)

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Determining whether premature water production is driven by mechanical channeling (thief zones) or normal coning dictates whether costly polymer-shutoff treatments are required.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Calculate **Chan’s Water-Oil Ratio (WOR) and WOR derivative curves** (d(\text{WOR})/dt) coupled with **Hall plot slope tracking**: \int p_{inj} dt \quad \text{vs.} \quad W_i

Reference dataset: Equinor Volve Field Water Injection & Production Logs.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
