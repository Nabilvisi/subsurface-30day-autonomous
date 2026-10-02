# Day 06 — Capillary Pressure ($P_c$) & Dynamic Saturation-Height Modeler

### 1. TECHNICAL PROBLEM & DOMAIN BOTTLENECK
Laboratory Mercury Injection Capillary Pressure (MICP) curves do not directly scale to reservoir conditions due to variable interfacial tension (\sigma) and contact angles (\theta).

### 2. FIRST-PRINCIPLES PHYSICS & MATHEMATICAL FORMULATION
Scale disparate laboratory P_c curves into universal **Leverett J-Functions**: J(S_w) = \frac{P_c}{\sigma \cos\theta}\sqrt{\frac{k}{\phi}} and fit Brooks-Corey parameters via non-linear optimization to map the Free Water Level (FWL).

### 3. COMPLETE, RUNNABLE STREAMLIT APPLICATION
The executable application is the repository root `app.py`. It routes Day 06 to the corresponding prebuilt engineering lab in `subsurface_lab/labs.py`, with Plotly interactivity, demo data, CSV/LAS ingestion, and KPI cards.

Run:
```bash
streamlit run app.py
```
Then select **Day 06** or use autonomous mode on/after the scheduled release.

### 4. READY-TO-PUBLISH LINKEDIN POST
Day 06/30 — Capillary Pressure ($P_c$) & Dynamic Saturation-Height Modeler

Today I built an interactive subsurface engineering workflow around a practical bottleneck: Laboratory Mercury Injection Capillary Pressure (MICP) curves do not directly scale to reservoir conditions due to variable interfacial tension (\sigma) and contact angles (\theta).

The implementation is physics-first, with the governing formulation encoded directly into a reactive Streamlit + Plotly application. Users can change the core engineering assumptions, load benchmark or field data, and immediately inspect KPI sensitivity instead of treating the calculation as a static spreadsheet.

Technical focus: Scale disparate laboratory P_c curves into universal **Leverett J-Functions**: J(S_w) = \frac{P_c}{\sigma \cos\theta}\sqrt{\frac{k}{\phi}} and fit Brooks-Corey parameters via non-linear optimization to map the Free Water Level (FWL).

Reference dataset: Equinor Volve Special Core Analysis (SCAL) Benchmark.

#PetroleumEngineering #ReservoirEngineering #Petrophysics #DrillingEngineering #ProductionEngineering #DataScience #Python #Streamlit #Plotly
