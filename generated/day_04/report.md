# Day 04 — Continuous NMR $T_2$ Spectral Deconvolution & Fluid Partitioner

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Raw NMR echo decays mask pore throat distributions; choosing arbitrary static T_2 cutoffs misclassifies movable hydrocarbons as capillary-bound water.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Invert raw spin-echo decay series M(t) = \sum f_i e^{-t/T_{2,i}} using Non-Negative Least Squares with Tikhonov regularization across 64 logarithmic bins (0.1\text{ to }3000\text{ ms}). Compute permeability via the Timur-Coates equation: k = c \cdot \phi^a \cdot \left(\frac{\text{FFI}}{\text{BVI}}\right)^b

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 04 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 04** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 04/30 — Continuous NMR $T_2$ Spectral Deconvolution & Fluid Partitioner

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Raw NMR echo decays mask pore throat distributions; choosing arbitrary static T_2 cutoffs misclassifies movable hydrocarbons as capillary-bound water.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Invert raw spin-echo decay series M(t) = \sum f_i e^{-t/T_{2,i}} using Non-Negative Least Squares with Tikhonov regularization across 64 logarithmic bins (0.1\text{ to }3000\text{ ms}). Compute permeability via the Timur-Coates equation: k = c \cdot \phi^a \cdot \left(\frac{\text{FFI}}{\text{BVI}}\right)^b

Reference dataset: SPWLA Open NMR Benchmark / Volve Core-Log Calibration Library.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
