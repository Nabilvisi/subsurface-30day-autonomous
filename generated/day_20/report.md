# Day 20 — Soft-String Torque & Drag (T&D) Tension & Buckling Simulator

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Excessive frictional drag in extended-reach horizontal wells can induce sinusoidal or helical drillpipe buckling, causing drillstring lockup.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Execute the **Johancsik Soft-String Model** along 3D survey stations for tripping-in, tripping-out, and rotating-on-bottom operations: \Delta T = \pm \mu \sqrt{F_n^2 + (T \Delta \alpha \sin \theta)^2} + w_b \Delta L \cos \theta

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 20 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 20** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 20/30 — Soft-String Torque & Drag (T&D) Tension & Buckling Simulator

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Excessive frictional drag in extended-reach horizontal wells can induce sinusoidal or helical drillpipe buckling, causing drillstring lockup.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Execute the **Johancsik Soft-String Model** along 3D survey stations for tripping-in, tripping-out, and rotating-on-bottom operations: \Delta T = \pm \mu \sqrt{F_n^2 + (T \Delta \alpha \sin \theta)^2} + w_b \Delta L \cos \theta

Reference dataset: Real High-Angle Directional Wellbore Drillstring Specs (SPE Compendium).

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
