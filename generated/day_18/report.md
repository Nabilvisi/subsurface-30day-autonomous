# Day 18 — 3D Directional Wellbore Trajectory & Anti-Collision Ellipse Radar

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Complex pad drilling risks borehole collisions; positional uncertainty grows downhole, requiring strict clearance monitoring.

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Implement the **Minimum Curvature Method** to convert Measured Depth (MD), Inclination (INC), and Azimuth (AZI) into True Vertical Depth (TVD), Northing, and Easting, calculating ISCWSA error ellipses.

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 18 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 18** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 18/30 — 3D Directional Wellbore Trajectory & Anti-Collision Ellipse Radar

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Complex pad drilling risks borehole collisions; positional uncertainty grows downhole, requiring strict clearance monitoring.

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Implement the **Minimum Curvature Method** to convert Measured Depth (MD), Inclination (INC), and Azimuth (AZI) into True Vertical Depth (TVD), Northing, and Easting, calculating ISCWSA error ellipses.

Reference dataset: Equinor Volve Directional Wellbore Surveys (All Wells).

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
