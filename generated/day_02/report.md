# Day 02 — Interactive Mineral Triaxial Inversion & Matrix Deconvolver

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Complex mixed lithologies (quartz, calcite, dolomite, shale) distort apparent matrix density (\rho_{ma}), causing traditional porosity determinations to deviate by up to 8–12 p.u.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Set up the linear matrix inversion: \mathbf{A} \cdot \mathbf{V} = \mathbf{L} \quad \text{subject to} \quad \sum V_i = 1, \quad V_i \ge 0 where \mathbf{A} defines endmember responses (NPHI, RHOB, PEF), solved via Non-Negative Least Squares (NNLS).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 02 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 02** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 02/30 — Interactive Mineral Triaxial Inversion & Matrix Deconvolver

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Complex mixed lithologies (quartz, calcite, dolomite, shale) distort apparent matrix density (\rho_{ma}), causing traditional porosity determinations to deviate by up to 8–12 p.u.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Set up the linear matrix inversion: \mathbf{A} \cdot \mathbf{V} = \mathbf{L} \quad \text{subject to} \quad \sum V_i = 1, \quad V_i \ge 0 where \mathbf{A} defines endmember responses (NPHI, RHOB, PEF), solved via Non-Negative Least Squares (NNLS).

Reference dataset: USGS Digital Spectral & Well Log Repository / Kansas Geological Survey.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
