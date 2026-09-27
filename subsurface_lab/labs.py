from __future__ import annotations

import math
from typing import Callable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit, minimize, nnls
from scipy.special import exp1
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

EPS = 1e-9
RNG = np.random.default_rng(42)


def _metric_row(items: list[tuple[str, str, str | None]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta=delta)


def _use_data(uploaded: pd.DataFrame | None, benchmark: pd.DataFrame, required: list[str]) -> pd.DataFrame:
    if uploaded is not None and all(c in uploaded.columns for c in required):
        st.success("Using uploaded data for this lab.")
        return uploaded.copy()
    if uploaded is not None:
        st.info("Uploaded data does not contain the required columns for this day; benchmark data is being used.")
    return benchmark.copy()


def _depth(n: int = 450, start: float = 2500.0, stop: float = 2750.0) -> np.ndarray:
    return np.linspace(start, stop, n)


def _day1_benchmark() -> pd.DataFrame:
    d = _depth()
    gr = 55 + 35 * np.sin(d / 22) + RNG.normal(0, 6, len(d))
    rhob = 2.42 - 0.12 * np.sin(d / 31) + RNG.normal(0, 0.025, len(d))
    nphi = 0.22 + 0.06 * np.sin(d / 27) + RNG.normal(0, 0.015, len(d))
    rt = np.exp(2.2 + 1.4 * np.sin(d / 19) + RNG.normal(0, 0.25, len(d)))
    cali = 8.5 + RNG.normal(0, 0.15, len(d))
    return pd.DataFrame({"DEPTH": d, "GR": gr, "RHOB": rhob, "NPHI": nphi, "RT": rt, "CALI": cali})


def _render_day_01(uploaded: pd.DataFrame | None) -> None:
    df = _use_data(uploaded, _day1_benchmark(), ["DEPTH", "GR", "RHOB", "NPHI", "RT"])
    with st.sidebar:
        st.subheader("Petrophysical controls")
        rw = st.slider("Rw (ohm·m)", 0.02, 0.30, 0.08, 0.01)
        m = st.slider("Cementation exponent m", 1.5, 2.8, 2.0, 0.05)
        n = st.slider("Saturation exponent n", 1.5, 3.0, 2.0, 0.05)
        rsh = st.slider("Rsh (ohm·m)", 0.5, 8.0, 2.0, 0.1)
        gr_min = st.slider("GR clean", 10.0, 60.0, 25.0)
        gr_max = st.slider("GR shale", 80.0, 180.0, 120.0)
    igr = np.clip((df.GR - gr_min) / max(gr_max - gr_min, EPS), 0, 1)
    vsh = np.clip(0.083 * (2 ** (3.7 * igr) - 1), 0, 1)
    phi_t = np.clip((2.65 - df.RHOB) / (2.65 - 1.0), 0.01, 0.45)
    phie = np.clip(phi_t * (1 - vsh), 0.01, 0.45)
    a = 1.0
    sw_archie = np.clip(((a * rw) / (np.maximum(df.RT, EPS) * phie**m)) ** (1 / n), 0, 1)
    # Simandoux quadratic for n=2, generalized afterward via exponent scaling.
    A = phie**m / np.maximum(a * rw * (1 - vsh), EPS)
    B = vsh / max(rsh, EPS)
    C = -1 / np.maximum(df.RT, EPS)
    sw2 = np.maximum((-B + np.sqrt(np.maximum(B * B - 4 * A * C, 0))) / np.maximum(2 * A, EPS), 0)
    sw_sim = np.clip(sw2 ** (2 / n), 0, 1)
    term = vsh ** np.maximum(1 - vsh / 2, 0.1) / np.sqrt(max(rsh, EPS)) + np.sqrt(phie**m / max(a * rw, EPS))
    sw_ind = np.clip((1 / np.sqrt(np.maximum(df.RT, EPS)) / np.maximum(term, EPS)) ** (4 / n), 0, 1)
    _metric_row([
        ("Mean Vsh", f"{vsh.mean():.2f}", None),
        ("Mean Φe", f"{phie.mean():.3f}", None),
        ("Archie mean Sw", f"{sw_archie.mean():.2f}", None),
        ("Shaly-sand ΔSw", f"{(sw_archie.mean()-sw_sim.mean()):+.2f}", "Archie − Simandoux"),
    ])
    left, right = st.columns([1.55, 1])
    with left:
        fig = make_subplots(rows=1, cols=4, shared_yaxes=True, horizontal_spacing=0.03,
                            subplot_titles=("GR / CALI", "Resistivity", "Porosity", "Water Saturation"))
        fig.add_trace(go.Scatter(x=df.GR, y=df.DEPTH, name="GR"), 1, 1)
        if "CALI" in df:
            fig.add_trace(go.Scatter(x=df.CALI, y=df.DEPTH, name="CALI"), 1, 1)
        fig.add_trace(go.Scatter(x=df.RT, y=df.DEPTH, name="RT"), 1, 2)
        fig.add_trace(go.Scatter(x=phie, y=df.DEPTH, name="PHIE"), 1, 3)
        fig.add_trace(go.Scatter(x=df.NPHI, y=df.DEPTH, name="NPHI"), 1, 3)
        fig.add_trace(go.Scatter(x=sw_archie, y=df.DEPTH, name="Archie"), 1, 4)
        fig.add_trace(go.Scatter(x=sw_sim, y=df.DEPTH, name="Simandoux"), 1, 4)
        fig.add_trace(go.Scatter(x=sw_ind, y=df.DEPTH, name="Indonesian"), 1, 4)
        fig.update_yaxes(autorange="reversed", title="Depth")
        fig.update_xaxes(type="log", row=1, col=2)
        fig.update_layout(height=650, legend_orientation="h", margin=dict(l=20, r=20, t=70, b=20))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        pickett = go.Figure()
        pickett.add_trace(go.Scatter(x=phie, y=df.RT, mode="markers", marker=dict(size=6, color=vsh, colorscale="Viridis"), name="Samples"))
        ph = np.linspace(max(phie.min(), 0.02), phie.max(), 100)
        water_line = a * rw / np.maximum(ph**m, EPS)
        pickett.add_trace(go.Scatter(x=ph, y=water_line, mode="lines", name="Sw=100% line"))
        pickett.update_xaxes(type="log", title="Effective porosity")
        pickett.update_yaxes(type="log", title="Rt (ohm·m)")
        pickett.update_layout(height=650, title="Interactive Pickett Crossplot")
        st.plotly_chart(pickett, use_container_width=True)


def _day2_benchmark() -> pd.DataFrame:
    n = 260
    d = _depth(n, 1800, 1960)
    raw = RNG.dirichlet([3, 2, 1.5, 2], size=n)
    # quartz, calcite, dolomite, shale responses: NPHI, RHOB, PEF
    A = np.array([[-0.04, 0.00, 0.02, 0.35], [2.65, 2.71, 2.87, 2.45], [1.8, 5.1, 3.1, 3.5]])
    logs = raw @ A.T + RNG.normal(0, [0.008, 0.015, 0.06], size=(n, 3))
    return pd.DataFrame({"DEPTH": d, "NPHI": logs[:, 0], "RHOB": logs[:, 1], "PEF": logs[:, 2]})


def _render_day_02(uploaded: pd.DataFrame | None) -> None:
    df = _use_data(uploaded, _day2_benchmark(), ["DEPTH", "NPHI", "RHOB", "PEF"])
    with st.sidebar:
        st.subheader("Mineral endmembers")
        rho_q = st.slider("Quartz density", 2.55, 2.75, 2.65, 0.01)
        rho_c = st.slider("Calcite density", 2.62, 2.82, 2.71, 0.01)
        rho_d = st.slider("Dolomite density", 2.75, 3.00, 2.87, 0.01)
        rho_s = st.slider("Shale density", 2.30, 2.70, 2.45, 0.01)
    A = np.array([[-0.04, 0.00, 0.02, 0.35], [rho_q, rho_c, rho_d, rho_s], [1.8, 5.1, 3.1, 3.5], [1, 1, 1, 1]])
    vols = []
    residuals = []
    for row in df[["NPHI", "RHOB", "PEF"]].to_numpy():
        x, r = nnls(A, np.r_[row, 1.0])
        x = x / max(x.sum(), EPS)
        vols.append(x)
        residuals.append(r)
    v = np.asarray(vols)
    _metric_row([
        ("Quartz", f"{v[:,0].mean():.1%}", None), ("Calcite", f"{v[:,1].mean():.1%}", None),
        ("Dolomite", f"{v[:,2].mean():.1%}", None), ("Mean inversion residual", f"{np.mean(residuals):.3f}", None),
    ])
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        cum = np.zeros(len(df))
        for idx, name in enumerate(["Quartz", "Calcite", "Dolomite", "Shale"]):
            fig.add_trace(go.Scatter(x=cum + v[:, idx], y=df.DEPTH, mode="lines", fill="tonextx" if idx else "tozerox", name=name))
            cum += v[:, idx]
        fig.update_yaxes(autorange="reversed", title="Depth")
        fig.update_xaxes(range=[0, 1], title="Volume fraction")
        fig.update_layout(height=620, title="Continuous Mineral Deconvolution")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        tern = go.Figure(go.Scatterternary(a=v[:,0], b=v[:,1], c=v[:,2], mode="markers", marker=dict(size=6, color=v[:,3], colorscale="Cividis")))
        tern.update_layout(height=620, title="Quartz–Calcite–Dolomite Ternary (color = shale)", ternary=dict(aaxis_title="Quartz", baxis_title="Calcite", caxis_title="Dolomite"))
        st.plotly_chart(tern, use_container_width=True)


def _day3_benchmark() -> pd.DataFrame:
    n = 600
    d = _depth(n, 2200, 2600)
    facies = RNG.integers(0, 4, n)
    centers = np.array([[35, .12, 2.55, 70, 2.0], [80, .24, 2.35, 90, 3.5], [120,.32,2.25,110,4.3], [55,.18,2.65,62,5.0]])
    noise = np.array([10, .025, .04, 6, .25])
    X = centers[facies] + RNG.normal(0, noise, size=(n,5))
    return pd.DataFrame(X, columns=["GR","NPHI","RHOB","DT","PEF"]).assign(DEPTH=d)


def _render_day_03(uploaded: pd.DataFrame | None) -> None:
    req = ["DEPTH","GR","NPHI","RHOB","DT","PEF"]
    df = _use_data(uploaded, _day3_benchmark(), req)
    with st.sidebar:
        algo = st.selectbox("Clustering algorithm", ["k-Means", "GMM", "DBSCAN"])
        k = st.slider("Cluster count k", 2, 8, 4)
        eps = st.slider("DBSCAN eps", 0.2, 2.0, 0.7, 0.1)
    X = StandardScaler().fit_transform(df[req[1:]])
    pcs = PCA(n_components=3, random_state=42).fit_transform(X)
    if algo == "k-Means": labels = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(X)
    elif algo == "GMM": labels = GaussianMixture(n_components=k, random_state=42).fit_predict(X)
    else: labels = DBSCAN(eps=eps, min_samples=12).fit_predict(X)
    valid = labels >= 0
    unique = np.unique(labels[valid])
    sil = silhouette_score(X[valid], labels[valid]) if len(unique) > 1 and valid.sum() > len(unique) else float("nan")
    _metric_row([("Clusters", str(len(unique)), None), ("Silhouette", f"{sil:.3f}" if np.isfinite(sil) else "N/A", None), ("Noise points", str(int((labels<0).sum())), None)])
    c1, c2 = st.columns([1.25, 1])
    with c1:
        fig = go.Figure(go.Scatter3d(x=pcs[:,0], y=pcs[:,1], z=pcs[:,2], mode="markers", marker=dict(size=3, color=labels, colorscale="Turbo"), text=[f"Depth {x:.1f}" for x in df.DEPTH]))
        fig.update_layout(height=620, title="3D PCA Electrofacies Space", scene=dict(xaxis_title="PC1", yaxis_title="PC2", zaxis_title="PC3"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df.GR, y=df.DEPTH, mode="markers", marker=dict(color=labels, colorscale="Turbo", size=5), name="Facies"))
        fig2.update_yaxes(autorange="reversed", title="Depth")
        fig2.update_xaxes(title="GR")
        fig2.update_layout(height=620, title="Cluster-to-Depth Mapping")
        st.plotly_chart(fig2, use_container_width=True)


def _render_day_04(uploaded: pd.DataFrame | None) -> None:
    t2 = np.logspace(-1, np.log10(3000), 128)
    spectrum = 0.36*np.exp(-((np.log10(t2)-0.25)/0.33)**2) + 0.64*np.exp(-((np.log10(t2)-1.8)/0.45)**2)
    spectrum /= np.trapz(spectrum, np.log(t2))
    with st.sidebar:
        cutoff = st.slider("T2 cutoff (ms)", 1.0, 250.0, 33.0, 1.0)
        phi = st.slider("NMR porosity", 0.05, 0.35, 0.22, 0.01)
        c = st.slider("Timur-Coates c", 1000.0, 15000.0, 6000.0, 500.0)
        a = st.slider("Porosity exponent a", 2.0, 6.0, 4.0, 0.1)
        b = st.slider("FFI/BVI exponent b", 1.0, 4.0, 2.0, 0.1)
    left = t2 <= cutoff
    bvi = np.trapz(spectrum[left], np.log(t2[left])) if left.sum()>1 else 0.0
    ffi = max(1-bvi, 0)
    k = c*(phi**a)*(ffi/max(bvi,0.01))**b
    _metric_row([("BVI", f"{bvi:.2f}", None), ("FFI", f"{ffi:.2f}", None), ("Coates permeability", f"{k:.1f} mD", None)])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t2, y=spectrum, mode="lines", name="T2 spectrum", fill="tozeroy"))
    fig.add_vline(x=cutoff, line_dash="dash", annotation_text="Cutoff")
    fig.update_xaxes(type="log", title="T2 (ms)")
    fig.update_yaxes(title="Normalized spectral amplitude")
    fig.update_layout(height=560, title="NMR T2 Fluid Partitioning")
    st.plotly_chart(fig, use_container_width=True)


def _render_day_05(uploaded: pd.DataFrame | None) -> None:
    vp = np.linspace(2.2, 5.8, 220)
    with st.sidebar:
        lith = st.selectbox("Lithology", ["Mudrock", "Sandstone", "Carbonate"])
        gas_sat = st.slider("Gas saturation", 0.0, 1.0, 0.2, 0.05)
        method = st.selectbox("Vs estimator", ["Castagna", "Random Forest surrogate"])
    if lith == "Mudrock": vs_base = (vp - 1.36)/1.16
    elif lith == "Sandstone": vs_base = 0.8042*vp - 0.8559
    else: vs_base = 0.5832*vp - 0.0778
    vs_base = np.clip(vs_base, 0.6, None)
    rho = 2.35 - 0.18*gas_sat + 0.12*(vp-vp.min())/(vp.max()-vp.min())
    vp_sub = vp*(1 - 0.08*gas_sat)
    if method.startswith("Random"):
        train_vp = RNG.uniform(2.0, 6.0, 500)
        train_rho = RNG.uniform(2.1, 2.75, 500)
        train_gas = RNG.uniform(0, 1, 500)
        train_vs = 0.78*train_vp - 0.55 + 0.12*(train_rho-2.4) - 0.04*train_gas + RNG.normal(0,.05,500)
        rf = RandomForestRegressor(n_estimators=120, random_state=42).fit(np.c_[train_vp,train_rho,train_gas], train_vs)
        vs = rf.predict(np.c_[vp_sub,rho,np.full_like(vp,gas_sat)])
    else: vs = vs_base
    nu = (vp_sub**2 - 2*vs**2) / np.maximum(2*(vp_sub**2 - vs**2), EPS)
    _metric_row([("Mean Vs", f"{vs.mean():.2f} km/s", None), ("Mean Poisson ratio", f"{nu.mean():.3f}", None), ("Vp fluid-substitution shift", f"{-8*gas_sat:.1f}%", None)])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vp, y=vs_base, mode="lines", name="Dry/base trend"))
    fig.add_trace(go.Scatter(x=vp_sub, y=vs, mode="lines", name="Current model"))
    fig.update_xaxes(title="Vp (km/s)")
    fig.update_yaxes(title="Vs (km/s)")
    fig.update_layout(height=560, title="Dynamic Vp–Vs Rock Physics Simulator")
    st.plotly_chart(fig, use_container_width=True)


def _render_day_06(uploaded: pd.DataFrame | None) -> None:
    d = _depth(350, 2400, 2700)
    phi = 0.14 + 0.08*(1+np.sin(d/30))/2
    k = 5 + 180*(phi-phi.min())/(phi.max()-phi.min())
    with st.sidebar:
        fwl = st.slider("Free Water Level (m)", 2500.0, 2780.0, 2670.0, 5.0)
        sigma = st.slider("Interfacial tension (mN/m)", 10.0, 60.0, 30.0, 1.0)
        theta = st.slider("Contact angle (deg)", 0.0, 60.0, 20.0, 1.0)
        lam = st.slider("Brooks-Corey λ", 0.5, 4.0, 1.8, 0.1)
        swi = st.slider("Irreducible Sw", 0.05, 0.45, 0.18, 0.01)
    h = np.maximum(fwl-d, 0)
    pc = 0.433*0.35*h
    pe = 1.2
    sw = np.where(pc>pe, swi+(1-swi)*(pe/np.maximum(pc,pe))**lam, 1.0)
    j = pc / np.maximum(sigma*np.cos(np.deg2rad(theta)), EPS) * np.sqrt(k/np.maximum(phi,EPS))
    transition = float(np.sum((sw>swi+0.05)&(sw<0.95))*(d[1]-d[0]))
    _metric_row([("Mean J", f"{np.nanmean(j):.2f}", None), ("Transition thickness", f"{transition:.1f} m", None), ("Mean Sw", f"{sw.mean():.2f}", None)])
    c1,c2=st.columns(2)
    with c1:
        fig=go.Figure(go.Scatter(x=sw,y=d,mode="lines",name="Sw"))
        fig.add_hline(y=fwl,line_dash="dash",annotation_text="FWL")
        fig.update_yaxes(autorange="reversed",title="Depth")
        fig.update_xaxes(range=[0,1],title="Sw")
        fig.update_layout(height=580,title="Saturation-Height Projection")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig2=go.Figure(go.Scatter(x=sw,y=j,mode="markers",marker=dict(color=k,colorscale="Viridis")))
        fig2.update_xaxes(title="Sw")
        fig2.update_yaxes(title="Leverett J")
        fig2.update_layout(height=580,title="Scaled Capillary Pressure")
        st.plotly_chart(fig2,use_container_width=True)


def _day7_benchmark() -> pd.DataFrame:
    d=_depth(500,1500,1850)
    bs=np.full(len(d),8.5)
    wash=((d>1600)&(d<1635))|((d>1740)&(d<1760))
    cali=bs+RNG.normal(0,.08,len(d))+wash*RNG.uniform(0.8,2.5,len(d))
    drho=RNG.normal(0,.015,len(d))+wash*RNG.normal(.12,.03,len(d))
    rhob=2.45+0.08*np.sin(d/25)+RNG.normal(0,.02,len(d))-wash*.12
    return pd.DataFrame({"DEPTH":d,"BS":bs,"CALI":cali,"DRHO":drho,"RHOB":rhob})


def _render_day_07(uploaded: pd.DataFrame | None) -> None:
    df=_use_data(uploaded,_day7_benchmark(),["DEPTH","BS","CALI","DRHO","RHOB"])
    with st.sidebar:
        contamination=st.slider("Anomaly sensitivity",0.01,0.25,0.08,0.01)
        neighbors=st.slider("k-NN neighbors",2,20,8)
    X=np.c_[df.CALI-df.BS,df.DRHO]
    model=IsolationForest(contamination=contamination,random_state=42).fit(X)
    flag=model.predict(X)<0
    good=~flag
    knn=KNeighborsRegressor(n_neighbors=min(neighbors,max(2,good.sum()-1))).fit(df.loc[good,["DEPTH"]],df.loc[good,"RHOB"])
    corrected=df.RHOB.copy()
    corrected.loc[flag]=knn.predict(df.loc[flag,["DEPTH"]])
    _metric_row([("Bad-hole samples",f"{flag.mean():.1%}",None),("Max washout",f"{(df.CALI-df.BS).max():.2f} in",None),("Mean density correction",f"{np.mean(np.abs(corrected-df.RHOB)):.3f} g/cc",None)])
    fig=make_subplots(rows=1,cols=3,shared_yaxes=True,subplot_titles=("Caliper","Density Correction","RHOB Repair"))
    fig.add_trace(go.Scatter(x=df.CALI,y=df.DEPTH,name="CALI"),1,1)
    fig.add_trace(go.Scatter(x=df.BS,y=df.DEPTH,name="BS"),1,1)
    fig.add_trace(go.Scatter(x=df.DRHO,y=df.DEPTH,name="DRHO"),1,2)
    fig.add_trace(go.Scatter(x=df.RHOB,y=df.DEPTH,name="Raw RHOB"),1,3)
    fig.add_trace(go.Scatter(x=corrected,y=df.DEPTH,name="Reconstructed"),1,3)
    fig.add_trace(go.Scatter(x=np.where(flag,df.RHOB,np.nan),y=df.DEPTH,mode="markers",marker=dict(symbol="x",size=7),name="Flag"),1,3)
    fig.update_yaxes(autorange="reversed",title="Depth")
    fig.update_layout(height=620,title="Bad-Hole Detection & Reconstruction")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_08(uploaded: pd.DataFrame | None) -> None:
    d=_depth(600,2100,2500)
    df=pd.DataFrame({"DEPTH":d,"VSH":np.clip(.35+.3*np.sin(d/33)+RNG.normal(0,.08,len(d)),0,1),"PHIE":np.clip(.18+.08*np.sin(d/21)+RNG.normal(0,.02,len(d)),.02,.35),"SW":np.clip(.55+.3*np.sin(d/18)+RNG.normal(0,.08,len(d)),.05,1)})
    df=_use_data(uploaded,df,["DEPTH","VSH","PHIE","SW"])
    with st.sidebar:
        vmax=st.slider("Vsh max",0.1,0.7,0.40,0.02)
        pmin=st.slider("Φe min",0.03,0.25,0.10,0.01)
        smax=st.slider("Sw max",0.2,0.9,0.60,0.02)
    dz=np.median(np.diff(df.DEPTH))
    sand=df.VSH<=vmax
    pay=sand&(df.PHIE>=pmin)&(df.SW<=smax)
    gross=(df.DEPTH.max()-df.DEPTH.min())
    net_sand=sand.sum()*dz
    net_pay=pay.sum()*dz
    _metric_row([("Gross interval",f"{gross:.1f} m",None),("Net sand",f"{net_sand:.1f} m",None),("Net pay",f"{net_pay:.1f} m",None),("NTG",f"{net_sand/gross:.2f}",None)])
    fig=make_subplots(rows=1,cols=4,shared_yaxes=True,subplot_titles=("Vsh","Φe","Sw","Pay Flag"))
    for x,col,i in [(df.VSH,"Vsh",1),(df.PHIE,"PHIE",2),(df.SW,"Sw",3)]: fig.add_trace(go.Scatter(x=x,y=df.DEPTH,name=col),1,i)
    fig.add_trace(go.Scatter(x=pay.astype(int),y=df.DEPTH,mode="lines",fill="tozerox",name="Net Pay"),1,4)
    fig.update_yaxes(autorange="reversed",title="Depth")
    fig.update_layout(height=620,title="Interactive Cutoff & Pay Summary")
    st.plotly_chart(fig,use_container_width=True)


def _arps_modified(t, qi, di, b, dterm):
    t=np.asarray(t,float)
    qh=qi/(1+b*di*t)**(1/max(b,1e-4))
    dnom=di/(1+b*di*t)
    idx=np.where(dnom<=dterm)[0]
    if len(idx):
        tl=t[idx[0]]; ql=qh[idx[0]]
        qh[idx[0]:]=ql*np.exp(-dterm*(t[idx[0]:]-tl))
    return qh


def _render_day_09(uploaded: pd.DataFrame | None) -> None:
    months=np.arange(0,84)
    qtrue=_arps_modified(months,1200,.055,1.05,.008)
    qhist=np.maximum(qtrue*(1+RNG.normal(0,.05,len(months))),1)
    df=pd.DataFrame({"MONTH":months,"RATE":qhist})
    df=_use_data(uploaded,df,["MONTH","RATE"])
    with st.sidebar:
        fit_end=st.slider("Historical fit end (month)",24,int(df.MONTH.max()),60)
        terminal=st.slider("Terminal decline / month",.002,.025,.008,.001)
        oil_price=st.slider("Oil price ($/bbl)",30,120,70)
    fit=df[df.MONTH<=fit_end]
    try:
        popt,_=curve_fit(lambda t,qi,di,b:_arps_modified(t,qi,di,b,terminal),fit.MONTH,fit.RATE,p0=[fit.RATE.iloc[0],.05,1.0],bounds=([1,.001,.1],[5000,.3,2.0]),maxfev=10000)
    except Exception:
        popt=[fit.RATE.iloc[0],.05,1.0]
    fc_t=np.arange(0,361)
    qf=_arps_modified(fc_t,*popt,terminal)
    eur=np.trapz(qf,fc_t*30.4375)/1000
    hist_cum=np.trapz(fit.RATE,fit.MONTH*30.4375)/1000
    revenue=eur*1000*oil_price/1e6
    _metric_row([("qi fit",f"{popt[0]:.0f} bopd",None),("b-factor",f"{popt[2]:.2f}",None),("30-y EUR",f"{eur:.1f} Mbbl",f"+{eur-hist_cum:.1f} vs hist"),("Gross revenue",f"${revenue:.1f} MM",None)])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df.MONTH,y=df.RATE,mode="markers",name="History"))
    fig.add_trace(go.Scatter(x=fc_t,y=qf,mode="lines",name="Modified Arps forecast"))
    fig.update_yaxes(type="log",title="Oil rate")
    fig.update_xaxes(title="Month")
    fig.update_layout(height=560,title="DCA History Match & 30-Year Forecast")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_10(uploaded: pd.DataFrame | None) -> None:
    t=np.arange(1,61)
    p=4200-35*t-0.22*t**2
    np_cum=0.25*t**1.35
    wp=0.08*t**1.2
    with st.sidebar:
        m=st.slider("Gas-cap ratio m",0.0,1.5,0.35,.05)
        we_coeff=st.slider("Water influx strength",0.0,2.0,0.75,.05)
    eo=(4200-p)/4200*0.18+0.005
    eg=(4200-p)/4200*0.30+0.005
    efw=(4200-p)/4200*0.02
    et=eo+m*eg+efw
    we=we_coeff*0.18*t
    F=np_cum*1.25 + wp*0.4 + we
    x=we/np.maximum(et,EPS)
    y=F/np.maximum(et,EPS)
    coef=np.polyfit(x,y,1)
    ooip=coef[1]
    pred=np.polyval(coef,x)
    r2=1-np.sum((y-pred)**2)/max(np.sum((y-y.mean())**2),EPS)
    drive=np.vstack([eo,m*eg,efw,np.gradient(we)]).clip(min=0)
    last=drive[:,-1]; last=last/max(last.sum(),EPS)
    _metric_row([("OOIP intercept",f"{ooip:.1f} MMstb",None),("Linear R²",f"{r2:.3f}",None),("Final pressure",f"{p[-1]:.0f} psi",None)])
    c1,c2=st.columns([1.3,1])
    with c1:
        fig=go.Figure(go.Scatter(x=x,y=y,mode="markers",name="HO points"))
        fig.add_trace(go.Scatter(x=x,y=pred,mode="lines",name="Fit"))
        fig.update_xaxes(title="We / Et"); fig.update_yaxes(title="F / Et")
        fig.update_layout(height=520,title="Havlena–Odeh Linearization")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig2=go.Figure(go.Pie(labels=["Oil expansion","Gas-cap","Rock/fluid","Water drive"],values=last,hole=.45))
        fig2.update_layout(height=520,title="Current Drive Index")
        st.plotly_chart(fig2,use_container_width=True)


def _render_day_11(uploaded: pd.DataFrame | None) -> None:
    dt=np.logspace(-2,3,240)
    dp=120*np.log1p(dt/0.03)+420*(1-np.exp(-dt/0.02))
    dp+=RNG.normal(0,5,len(dt))
    with st.sidebar:
        smooth=st.slider("Bourdet smoothing window",3,25,9,2)
        mu=st.slider("Viscosity (cP)",0.2,5.0,1.2,.1)
        bo=st.slider("Bo",1.0,1.8,1.25,.05)
        h=st.slider("Net thickness (ft)",10,200,60)
        q=st.slider("Test rate (stb/d)",100,5000,1200)
    ldt=np.log(dt)
    raw=np.gradient(dp,ldt)
    deriv=pd.Series(raw).rolling(smooth,center=True,min_periods=1).mean().to_numpy()
    plateau=np.nanmedian(deriv[(dt>3)&(dt<80)])
    k=70.6*q*mu*bo/max(h*plateau,EPS)
    skin=max((dp[(dt>1)&(dt<3)].mean()-plateau)/max(plateau,EPS),0)
    _metric_row([("Derivative plateau",f"{plateau:.1f} psi",None),("Estimated k",f"{k:.1f} mD",None),("Mechanical skin",f"{skin:.2f}",None)])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=dt,y=dp,mode="lines",name="Δp"))
    fig.add_trace(go.Scatter(x=dt,y=deriv,mode="lines",name="Bourdet derivative"))
    fig.add_hline(y=plateau,line_dash="dash",annotation_text="IARF plateau")
    fig.update_xaxes(type="log",title="Δt (hr)"); fig.update_yaxes(type="log",title="Pressure / derivative (psi)")
    fig.update_layout(height=560,title="PTA Bourdet Diagnostic")
    st.plotly_chart(fig,use_container_width=True)


def _rachford_rice(z: np.ndarray, K: np.ndarray) -> float:
    f0 = np.sum(z * (K - 1))
    f1 = np.sum(z * (K - 1) / np.maximum(K, EPS))
    if f0 <= 0:
        return 0.0
    if f1 >= 0:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        v = (lo + hi) / 2
        f = np.sum(z * (K - 1) / np.maximum(1 + v * (K - 1), EPS))
        if f > 0:
            lo = v
        else:
            hi = v
    return (lo + hi) / 2


def _pr_lnphi(comp: np.ndarray, T: float, P: float, Tc: np.ndarray, Pc: np.ndarray, omega: np.ndarray, phase: str) -> np.ndarray:
    """Peng-Robinson mixture fugacity coefficients. P in bar, R in L·bar/mol/K."""
    R = 0.08314462618
    kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
    alpha = (1 + kappa * (1 - np.sqrt(T / Tc)))**2
    ai = 0.45724 * (R**2) * (Tc**2) / Pc * alpha
    bi = 0.07780 * R * Tc / Pc
    aij = np.sqrt(np.outer(ai, ai))
    am = float(comp @ aij @ comp)
    bm = float(comp @ bi)
    A = am * P / max(R**2 * T**2, EPS)
    B = bm * P / max(R * T, EPS)
    coeff = [1.0, -(1 - B), A - 3 * B**2 - 2 * B, -(A * B - B**2 - B**3)]
    roots = np.roots(coeff)
    real = np.sort(roots.real[np.abs(roots.imag) < 1e-8])
    if len(real) == 0:
        raise ValueError("No real PR compressibility root")
    Z = float(real[0] if phase == "L" else real[-1])
    Z = max(Z, B + 1e-10)
    sum_aij = aij @ comp
    if B < 1e-12 or A < 1e-12 or am < EPS or bm < EPS:
        return bi / max(bm, EPS) * (Z - 1) - np.log(max(Z - B, EPS))
    log_term = np.log(
        max(Z + (1 + math.sqrt(2)) * B, EPS)
        / max(Z + (1 - math.sqrt(2)) * B, EPS)
    )
    lnphi = (
        bi / bm * (Z - 1)
        - np.log(max(Z - B, EPS))
        - A / (2 * math.sqrt(2) * B)
        * (2 * sum_aij / am - bi / bm)
        * log_term
    )
    return lnphi


def _pr_flash(z: np.ndarray, T: float, P: float, Tc: np.ndarray, Pc: np.ndarray, omega: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    K = (Pc / P) * np.exp(5.373 * (1 + omega) * (1 - Tc / T))
    K = np.clip(K, 1e-5, 1e5)
    V = _rachford_rice(z, K)
    if V <= 0:
        return 0.0, z.copy(), np.clip(K * z, EPS, None) / np.sum(np.clip(K * z, EPS, None))
    if V >= 1:
        x = np.clip(z / np.maximum(K, EPS), EPS, None); x /= x.sum()
        return 1.0, x, z.copy()
    x = z.copy(); y = z.copy()
    for _ in range(60):
        V = _rachford_rice(z, K)
        denom = np.maximum(1 + V * (K - 1), EPS)
        x = z / denom; x /= x.sum()
        y = K * x; y /= y.sum()
        try:
            lnphi_l = _pr_lnphi(x, T, P, Tc, Pc, omega, "L")
            lnphi_v = _pr_lnphi(y, T, P, Tc, Pc, omega, "V")
        except ValueError:
            break
        K_new = np.exp(np.clip(lnphi_l - lnphi_v, -20, 20))
        if np.max(np.abs(np.log(np.maximum(K_new, EPS) / np.maximum(K, EPS)))) < 1e-7:
            K = K_new
            break
        K = np.sqrt(K * K_new)
    V = _rachford_rice(z, K)
    denom = np.maximum(1 + V * (K - 1), EPS)
    x = z / denom; x /= x.sum()
    y = K * x; y /= y.sum()
    return float(V), x, y


def _render_day_12(uploaded: pd.DataFrame | None) -> None:
    names=np.array(["Methane","Ethane","n-Butane","n-Hexane"])
    z=np.array([.58,.18,.14,.10])
    Tc=np.array([190.6,305.3,425.1,507.6])
    Pc=np.array([45.99,48.72,37.96,30.25])
    omega=np.array([.011,.099,.200,.301])
    with st.sidebar:
        T=st.slider("Temperature (K)",250.0,500.0,355.0,2.5)
        P=st.slider("Pressure (bar)",10.0,350.0,120.0,5.0)
    V,x,y=_pr_flash(z,T,P,Tc,Pc,omega)
    _metric_row([("Vapor fraction",f"{V:.3f}",None),("Liquid fraction",f"{1-V:.3f}",None),("State", "Two-phase" if 1e-4<V<1-1e-4 else ("Vapor" if V>=1-1e-4 else "Liquid"), None)])
    pr=np.linspace(10,350,90)
    vf=np.array([_pr_flash(z,T,float(pp),Tc,Pc,omega)[0] for pp in pr])
    c1,c2=st.columns(2)
    with c1:
        fig=go.Figure(go.Scatter(x=pr,y=vf,mode="lines",name="PR vapor fraction"))
        fig.add_vline(x=P,line_dash="dash",annotation_text="Selected state")
        fig.update_xaxes(title="Pressure (bar)"); fig.update_yaxes(title="Vapor fraction",range=[0,1])
        fig.update_layout(height=500,title="Peng–Robinson Isothermal Flash Envelope")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig2=go.Figure()
        fig2.add_trace(go.Bar(x=names,y=x,name="Liquid x")); fig2.add_trace(go.Bar(x=names,y=y,name="Vapor y"))
        fig2.update_layout(barmode="group",height=500,title="PR Equilibrium Phase Compositions")
        st.plotly_chart(fig2,use_container_width=True)
    st.caption("Peng–Robinson EOS with classical mixing rules, Wilson K-value initialization, Rachford–Rice phase split, and iterative fugacity matching. Binary-interaction parameters are zero in this portfolio benchmark.")

def _render_day_13(uploaded: pd.DataFrame | None) -> None:
    sw=np.linspace(.15,.95,400)
    with st.sidebar:
        swi=st.slider("Swi",.05,.35,.18,.01)
        sor=st.slider("Sor",.05,.40,.22,.01)
        nw=st.slider("Corey nw",1.0,5.0,2.5,.1)
        no=st.slider("Corey no",1.0,5.0,2.0,.1)
        muw=st.slider("Water viscosity",.2,2.0,.5,.1)
        muo=st.slider("Oil viscosity",.5,10.0,2.0,.1)
        pvi=st.slider("Injected PV",0.05,1.5,.45,.05)
    se=np.clip((sw-swi)/max(1-swi-sor,EPS),0,1)
    krw=se**nw; kro=(1-se)**no
    fw=(krw/muw)/np.maximum(krw/muw+kro/muo,EPS)
    dfd=np.gradient(fw,sw)
    tangent=(fw)/(np.maximum(sw-swi,EPS))
    valid=sw>swi+.01
    idx=np.nanargmax(np.where(valid,tangent,-np.inf))
    swf=sw[idx]; slope=dfd[idx]
    x=np.linspace(0,1,400)
    front=min(pvi*max(slope,0.1),1.0)
    profile=np.where(x<front,swf+(1-sor-swf)*(1-x/max(front,EPS))*0.35,swi)
    _metric_row([("Shock Sw",f"{swf:.3f}",None),("dfw/dSw at shock",f"{slope:.2f}",None),("Front position",f"{front:.2f} L",None)])
    c1,c2=st.columns(2)
    with c1:
        fig=go.Figure(go.Scatter(x=sw,y=fw,mode="lines",name="fw"))
        line=fw[idx]/max(swf-swi,EPS)*(sw-swi)
        fig.add_trace(go.Scatter(x=sw,y=line,mode="lines",name="Welge tangent"))
        fig.update_xaxes(title="Sw"); fig.update_yaxes(title="fw",range=[0,1])
        fig.update_layout(height=500,title="Fractional Flow & Shock Construction")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig2=go.Figure(go.Scatter(x=x,y=profile,mode="lines",name="Sw(x)"))
        fig2.add_vline(x=front,line_dash="dash",annotation_text="Shock front")
        fig2.update_xaxes(title="Normalized reservoir length"); fig2.update_yaxes(title="Sw",range=[0,1])
        fig2.update_layout(height=500,title="1D Saturation Profile")
        st.plotly_chart(fig2,use_container_width=True)


def _render_day_14(uploaded: pd.DataFrame | None) -> None:
    t=np.arange(1,121)
    oil=1800*np.exp(-.009*t)+100
    water=150+8*t+np.where(t>65,18*(t-65),0)
    wor=water/oil
    dwor=np.gradient(wor,t)
    inj=1600+100*np.sin(t/9)
    pinj=2400+2.2*t+np.where(t>75,5*(t-75),0)
    wi=np.cumsum(inj*30)/1e6
    hall=np.cumsum(pinj*30)/1e6
    with st.sidebar:
        break_m=st.slider("Hall slope-break locator (month)",12,110,75)
    s1=np.polyfit(wi[:break_m],hall[:break_m],1)[0]
    s2=np.polyfit(wi[break_m:],hall[break_m:],1)[0]
    interpretation="Plugging / rising skin" if s2>s1*1.15 else ("Fracture extension / reduced resistance" if s2<s1*.85 else "Stable injectivity")
    _metric_row([("Current WOR",f"{wor[-1]:.2f}",None),("Hall slope pre",f"{s1:.2f}",None),("Hall slope post",f"{s2:.2f}",interpretation)])
    c1,c2=st.columns(2)
    with c1:
        fig=go.Figure(); fig.add_trace(go.Scatter(x=t,y=wor,name="WOR")); fig.add_trace(go.Scatter(x=t,y=dwor,name="dWOR/dt",yaxis="y2"))
        fig.update_layout(height=500,title="Chan Diagnostic",yaxis2=dict(overlaying="y",side="right",title="Derivative"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig2=go.Figure(go.Scatter(x=wi,y=hall,mode="lines+markers",name="Hall"))
        fig2.add_vline(x=wi[break_m],line_dash="dash",annotation_text="Selected break")
        fig2.update_xaxes(title="Cumulative water injected (MMbbl)"); fig2.update_yaxes(title="∫Pinj dt")
        fig2.update_layout(height=500,title="Interactive Hall Plot")
        st.plotly_chart(fig2,use_container_width=True)


def _render_day_15(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        time_h=st.slider("Elapsed time (hr)",1.0,500.0,72.0,1.0)
        q1=st.slider("Producer P1 rate",-5000,-200,-1800,100)
        q2=st.slider("Producer P2 rate",-5000,-200,-1400,100)
        qi=st.slider("Injector I1 rate",200,5000,1800,100)
        p2x=st.slider("P2 Easting",300.0,1800.0,1150.0,50.0)
        iy=st.slider("I1 Northing",200.0,1800.0,1300.0,50.0)
    xs=np.linspace(0,2000,100); ys=np.linspace(0,2000,100); X,Y=np.meshgrid(xs,ys)
    wells=[(600,700,q1,"P1"),(p2x,900,q2,"P2"),(900,iy,qi,"I1")]
    dp=np.zeros_like(X)
    alpha=0.08
    for wx,wy,q,_ in wells:
        r2=(X-wx)**2+(Y-wy)**2+25
        u=r2/(4*alpha*time_h*3600+EPS)
        dp += -q*0.012*exp1(np.maximum(u,1e-8))
    _metric_row([("Field ΔP range",f"{dp.min():.0f} to {dp.max():.0f} psi",None),("Elapsed time",f"{time_h:.0f} hr",None),("Net rate",f"{q1+q2+qi:.0f} stb/d",None)])
    fig=go.Figure(go.Heatmap(x=xs,y=ys,z=dp,colorscale="RdBu",zmid=0,colorbar_title="ΔP psi"))
    for wx,wy,q,name in wells:
        fig.add_trace(go.Scatter(x=[wx],y=[wy],mode="markers+text",text=[name],textposition="top center",marker=dict(size=13,symbol="triangle-up" if q>0 else "circle"),name=name))
    fig.update_layout(height=620,title="2D Interference Pressure Field",xaxis_title="Easting (m)",yaxis_title="Northing (m)")
    st.plotly_chart(fig,use_container_width=True)

def _render_day_16(uploaded: pd.DataFrame | None) -> None:
    d=_depth(320,0,3200)
    with st.sidebar:
        qg=st.slider("Gas rate (MMscf/d)",0.5,40.0,8.0,.5)
        tid=st.slider("Tubing ID (in)",1.5,5.5,2.875,.125)
        pwh=st.slider("Wellhead pressure (psi)",100,2500,700,50)
        sigma=st.slider("Surface tension (dyn/cm)",20.0,75.0,45.0,1.0)
        rho_l=st.slider("Liquid density (lb/ft³)",35.0,70.0,52.0,1.0)
    p=pwh+0.18*d
    rho_g=np.maximum(0.0032*p,0.2)
    area=math.pi*(tid/12)**2/4
    q_actual=qg*1e6/86400*14.7/np.maximum(p,1)
    v=q_actual/area
    vc=1.593*(sigma**0.25)*np.maximum(rho_l-rho_g,EPS)**0.25/np.sqrt(rho_g)
    risk=v<vc
    onset=d[np.argmax(risk)] if risk.any() else np.nan
    _metric_row([("Min velocity margin",f"{np.min(v-vc):.2f} ft/s",None),("Loading onset",f"{onset:.0f} ft" if np.isfinite(onset) else "None",None),("Bottomhole pressure",f"{p[-1]:.0f} psi",None)])
    fig=go.Figure(); fig.add_trace(go.Scatter(x=v,y=d,name="Actual gas velocity")); fig.add_trace(go.Scatter(x=vc,y=d,name="Turner critical"))
    fig.update_yaxes(autorange="reversed",title="Depth (ft)"); fig.update_xaxes(title="Velocity (ft/s)")
    fig.update_layout(height=580,title="Gas-Condensate Liquid Loading Envelope")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_17(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        wob=st.slider("WOB (klbf)",5.0,80.0,35.0,1.0)
        rpm=st.slider("RPM",40,220,120,5)
        torque=st.slider("Torque (klbf·ft)",2.0,30.0,12.0,.5)
        rop=st.slider("ROP (ft/hr)",5.0,250.0,85.0,5.0)
        bit=st.slider("Bit diameter (in)",6.0,17.5,8.5,.25)
        ucs=st.slider("Formation UCS (ksi)",2.0,35.0,12.0,.5)
    area=math.pi*bit**2/4
    mse=wob*1000/area + 120*math.pi*rpm*torque*1000/(area*max(rop,EPS))
    mse_ksi=mse/1000
    eff=ucs/max(mse_ksi,EPS)
    w=np.linspace(5,80,160)
    rop_curve=210*(1-np.exp(-w/28))*np.exp(-np.maximum(w-58,0)/45)
    _metric_row([("MSE",f"{mse_ksi:.1f} ksi",None),("UCS",f"{ucs:.1f} ksi",None),("Drilling efficiency",f"{eff:.2f}","UCS / MSE")])
    fig=go.Figure(go.Scatter(x=w,y=rop_curve,name="Founder curve"))
    fig.add_trace(go.Scatter(x=[wob],y=[rop],mode="markers",marker=dict(size=14),name="Operating point"))
    fig.update_xaxes(title="WOB (klbf)"); fig.update_yaxes(title="ROP (ft/hr)"); fig.update_layout(height=540,title="MSE / Bit Flounder Optimizer")
    st.plotly_chart(fig,use_container_width=True)


def _minimum_curvature(md,inc_deg,azi_deg):
    md=np.asarray(md,float); inc=np.deg2rad(inc_deg); azi=np.deg2rad(azi_deg)
    n=np.zeros(len(md)); e=np.zeros(len(md)); tvd=np.zeros(len(md))
    for i in range(1,len(md)):
        dmd=md[i]-md[i-1]
        dog=np.arccos(np.clip(np.cos(inc[i]-inc[i-1])-np.sin(inc[i-1])*np.sin(inc[i])*(1-np.cos(azi[i]-azi[i-1])),-1,1))
        rf=2/dog*np.tan(dog/2) if dog>1e-8 else 1.0
        n[i]=n[i-1]+dmd/2*(np.sin(inc[i-1])*np.cos(azi[i-1])+np.sin(inc[i])*np.cos(azi[i]))*rf
        e[i]=e[i-1]+dmd/2*(np.sin(inc[i-1])*np.sin(azi[i-1])+np.sin(inc[i])*np.sin(azi[i]))*rf
        tvd[i]=tvd[i-1]+dmd/2*(np.cos(inc[i-1])+np.cos(inc[i]))*rf
    return tvd,n,e


def _render_day_18(uploaded: pd.DataFrame | None) -> None:
    md=np.arange(0,4200,100)
    inc=np.clip((md-400)/2600*78,0,78)
    azi=35+8*np.sin(md/900)
    tvd,n,e=_minimum_curvature(md,inc,azi)
    with st.sidebar:
        offset=st.slider("Offset-well Easting shift (m)",100.0,900.0,420.0,20.0)
        azi_shift=st.slider("Offset azimuth shift (deg)",-30.0,30.0,8.0,1.0)
        uncertainty=st.slider("1σ positional uncertainty at TD (m)",5.0,100.0,35.0,5.0)
    tvd2,n2,e2=_minimum_curvature(md,np.clip(inc*0.95,0,80),azi+azi_shift); e2+=offset
    sep=np.sqrt((n-n2)**2+(e-e2)**2+(tvd-tvd2)**2)
    sigma=5+(uncertainty-5)*(md/md.max())
    sr=sep/np.maximum(2*sigma,EPS)
    _metric_row([("Minimum center distance",f"{sep.min():.1f} m",None),("Minimum separation ratio",f"{sr.min():.2f}",None),("TD TVD",f"{tvd[-1]:.0f} m",None)])
    fig=go.Figure()
    fig.add_trace(go.Scatter3d(x=e,y=n,z=-tvd,mode="lines",name="Well A")); fig.add_trace(go.Scatter3d(x=e2,y=n2,z=-tvd2,mode="lines",name="Offset Well"))
    fig.update_layout(height=650,title="3D Directional Trajectory & Anti-Collision Radar",scene=dict(xaxis_title="Easting",yaxis_title="Northing",zaxis_title="TVD"))
    st.plotly_chart(fig,use_container_width=True)


def _render_day_19(uploaded: pd.DataFrame | None) -> None:
    d=np.linspace(0,12000,400)
    pp=8.8+0.00018*d
    fg=12.7+0.00012*d
    with st.sidebar:
        mud=st.slider("Static mud weight (ppg)",8.5,16.0,11.2,.1)
        speed=st.slider("Tripping speed (ft/min)",0.0,180.0,70.0,5.0)
        model=st.selectbox("Rheology",["Herschel-Bulkley","Bingham Plastic"])
        pv=st.slider("Plastic viscosity (cP)",8.0,60.0,28.0,1.0)
        yp=st.slider("Yield point (lb/100ft²)",2.0,40.0,14.0,1.0)
    coeff=(0.0018*pv+0.004*yp)*(1.15 if model.startswith("Herschel") else 1.0)
    delta=coeff*speed*(d/d.max())
    surge=mud+delta; swab=mud-delta
    margin=np.minimum(fg-surge,swab-pp)
    _metric_row([("Minimum mud-window margin",f"{margin.min():.2f} ppg",None),("Bottom surge",f"{surge[-1]:.2f} ppg",None),("Bottom swab",f"{swab[-1]:.2f} ppg",None)])
    fig=go.Figure();
    for x,name in [(pp,"Pore pressure"),(fg,"Fracture gradient"),(surge,"Surge ECD"),(swab,"Swab ECD")]: fig.add_trace(go.Scatter(x=x,y=d,name=name))
    fig.update_yaxes(autorange="reversed",title="TVD (ft)"); fig.update_xaxes(title="Equivalent density (ppg)"); fig.update_layout(height=600,title="Dynamic Surge / Swab Mud Window")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_20(uploaded: pd.DataFrame | None) -> None:
    md=np.linspace(0,16000,400)
    inc=np.clip((md-2000)/8000*88,0,88)
    with st.sidebar:
        mu=st.slider("Friction factor μ",0.05,0.45,0.22,.01)
        pipe_wt=st.slider("Pipe buoyed weight (lb/ft)",8.0,35.0,18.0,1.0)
        mode=st.selectbox("Operation",["Tripping In","Tripping Out","Rotating On Bottom"])
    sign={"Tripping In":-1,"Tripping Out":1,"Rotating On Bottom":.35}[mode]
    vertical=pipe_wt*np.cos(np.deg2rad(inc)); normal=pipe_wt*np.sin(np.deg2rad(inc))
    incremental=(vertical+sign*mu*normal)*(md[1]-md[0])
    tension=np.cumsum(incremental[::-1])[::-1]/1000
    sinus=25+0.0018*md; helical=45+0.0030*md; yield_lim=np.full_like(md,320.0)
    _metric_row([("Surface tension",f"{tension[0]:.1f} klbf",None),("Peak tension",f"{tension.max():.1f} klbf",None),("Helical crossings",str(int(np.sum(tension>helical))),None)])
    fig=go.Figure();
    for x,name in [(tension,"Modeled tension"),(sinus,"Sinusoidal buckling"),(helical,"Helical buckling"),(yield_lim,"Pipe yield")]: fig.add_trace(go.Scatter(x=x,y=md,name=name))
    fig.update_yaxes(autorange="reversed",title="MD (ft)"); fig.update_xaxes(title="Axial force (klbf)"); fig.update_layout(height=600,title="Soft-String Torque & Drag / Buckling")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_21(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        sidpp=st.slider("SIDPP (psi)",50,1200,420,10)
        sicp=st.slider("SICP (psi)",100,1800,720,10)
        slow=st.slider("Slow pump pressure (psi)",200,1800,850,25)
        kick=st.slider("Kick volume (bbl)",5.0,80.0,25.0,1.0)
        choke=st.slider("Choke opening (%)",5,100,45,5)
        progress=st.slider("Circulation progress (%)",0,200,60,5)
    icp=sidpp+slow
    phase1=min(progress/100,1); phase2=max((progress-100)/100,0)
    dp_sched=icp-(sidpp*phase1)
    casing=sicp*(1-0.55*phase1)*(1-0.7*phase2)*(1+0.25*(50-choke)/50)
    remaining=kick*max(1-progress/125,0)
    _metric_row([("Target drillpipe pressure",f"{dp_sched:.0f} psi",None),("Modeled casing pressure",f"{casing:.0f} psi",None),("Kick remaining",f"{remaining:.1f} bbl",None)])
    x=np.linspace(0,200,201)
    sched=icp-sidpp*np.minimum(x/100,1)
    cas=sicp*(1-0.55*np.minimum(x/100,1))*(1-0.7*np.maximum((x-100)/100,0))
    fig=go.Figure(); fig.add_trace(go.Scatter(x=x,y=sched,name="Drillpipe target")); fig.add_trace(go.Scatter(x=x,y=cas,name="Casing pressure")); fig.add_vline(x=progress,line_dash="dash",annotation_text="Current")
    fig.update_xaxes(title="Circulation progress (%)"); fig.update_yaxes(title="Pressure (psi)"); fig.update_layout(height=560,title="Driller's Method Pressure Schedule")
    st.plotly_chart(fig,use_container_width=True)


def _day22_benchmark() -> pd.DataFrame:
    n=800; t=np.arange(n)
    torque=8+0.6*np.sin(t/25)+RNG.normal(0,.25,n)
    hook=180+3*np.sin(t/40)+RNG.normal(0,1.2,n)
    spp=2500+40*np.sin(t/30)+RNG.normal(0,18,n)
    rop=70+8*np.sin(t/19)+RNG.normal(0,3,n)
    flow=520+8*np.sin(t/35)+RNG.normal(0,3,n)
    mask=t>610
    torque[mask]+=np.linspace(0,6,mask.sum()); hook[mask]-=np.linspace(0,22,mask.sum()); spp[mask]+=np.linspace(0,280,mask.sum()); rop[mask]-=np.linspace(0,45,mask.sum())
    return pd.DataFrame({"TIME":t,"TORQUE":torque,"HOOKLOAD":hook,"SPP":spp,"ROP":rop,"FLOW":flow})


def _render_day_22(uploaded: pd.DataFrame | None) -> None:
    df=_use_data(uploaded,_day22_benchmark(),["TIME","TORQUE","HOOKLOAD","SPP","ROP","FLOW"])
    with st.sidebar:
        playback=st.slider("Playback position",50,len(df)-1,min(650,len(df)-1),10)
        contamination=st.slider("Anomaly contamination",.01,.20,.06,.01)
    feats=df[["TORQUE","HOOKLOAD","SPP","ROP","FLOW"]]
    z=StandardScaler().fit_transform(feats)
    iso=IsolationForest(contamination=contamination,random_state=42).fit(z)
    score=-iso.score_samples(z); score=(score-score.min())/max(score.max()-score.min(),EPS)*100
    prob=score[playback]
    _metric_row([("Stuck-pipe probability",f"{prob:.0f}%",None),("Current torque",f"{df.TORQUE.iloc[playback]:.1f} klbf-ft",None),("Current hookload",f"{df.HOOKLOAD.iloc[playback]:.0f} klbf",None)])
    gauge=go.Figure(go.Indicator(mode="gauge+number",value=prob,title={"text":"Stuck Pipe Probability"},gauge={"axis":{"range":[0,100]},"threshold":{"value":70}})); gauge.update_layout(height=300)
    st.plotly_chart(gauge,use_container_width=True)
    fig=go.Figure(); fig.add_trace(go.Scatter(x=df.TIME[:playback+1],y=df.TORQUE[:playback+1],name="Torque")); fig.add_trace(go.Scatter(x=df.TIME[:playback+1],y=df.HOOKLOAD[:playback+1]/20,name="Hookload/20")); fig.add_trace(go.Scatter(x=df.TIME[:playback+1],y=score[:playback+1]/10,name="Anomaly score/10")); fig.update_layout(height=420,title="Real-Time Sensor Playback")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_23(uploaded: pd.DataFrame | None) -> None:
    d=np.linspace(1000,14000,450)
    dt_n=65+0.0028*d
    dt_obs=dt_n.copy(); dt_obs[d>8500]+=0.012*(d[d>8500]-8500)
    rho=2.15+0.000035*d
    with st.sidebar:
        nctl_slope=st.slider("NCTL sonic slope",.0015,.0045,.0028,.0001)
        eaton_n=st.slider("Eaton exponent",1.0,5.0,3.0,.1)
        mud=st.slider("Planned mud weight (ppg)",8.5,18.0,12.0,.1)
    dt_n=65+nctl_slope*d
    sigma=np.cumsum(rho*0.433*np.gradient(d)/1000) # scaled psi proxy
    sigma=0.95*d # practical psi proxy for educational display
    ph=0.465*d
    pp=sigma-(sigma-ph)*np.clip(dt_n/np.maximum(dt_obs,EPS),0,1.3)**eaton_n
    pp_grad=pp/np.maximum(0.052*d,EPS)
    fg=np.minimum(pp_grad+2.0+0.0001*d,20)
    safe=(mud>pp_grad)&(mud<fg)
    _metric_row([("Max pore pressure",f"{pp_grad.max():.2f} ppg",None),("Min fracture gradient",f"{fg.min():.2f} ppg",None),("Planned MW safe coverage",f"{safe.mean():.1%}",None)])
    fig=go.Figure();
    for x,name in [(pp_grad,"Pore pressure"),(fg,"Fracture gradient"),(np.full_like(d,mud),"Planned MW")]: fig.add_trace(go.Scatter(x=x,y=d,name=name))
    fig.update_yaxes(autorange="reversed",title="TVD (ft)"); fig.update_xaxes(title="Equivalent gradient (ppg)"); fig.update_layout(height=600,title="Eaton Pore Pressure & Safe Mud Window")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_24(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        pr=st.slider("Reservoir pressure (psi)",1000,7000,3600,100)
        pwh=st.slider("Wellhead pressure (psi)",50,1800,450,25)
        tid=st.slider("Tubing ID (in)",1.5,5.5,2.875,.125)
        wc=st.slider("Water cut",0.0,.95,.35,.05)
        qmax=st.slider("Vogel qmax (stb/d)",500,12000,4500,100)
    q=np.linspace(0,qmax,350)
    # invert Vogel for Pwf/Pr: 0.8x^2+0.2x+(q/qmax-1)=0
    disc=.04-3.2*(q/qmax-1)
    x=(-.2+np.sqrt(np.maximum(disc,0)))/1.6
    ipr=pr*np.clip(x,0,1)
    hydro=450+850*wc
    friction=(q/1000)**1.8*380*(2.875/tid)**4.8
    vlp=pwh+hydro+friction
    idx=np.argmin(np.abs(ipr-vlp)); qop=q[idx]; pop=(ipr[idx]+vlp[idx])/2
    _metric_row([("Operating rate",f"{qop:.0f} stb/d",None),("Node pressure",f"{pop:.0f} psi",None),("Drawdown",f"{pr-pop:.0f} psi",None)])
    fig=go.Figure(); fig.add_trace(go.Scatter(x=q,y=ipr,name="IPR")); fig.add_trace(go.Scatter(x=q,y=vlp,name="VLP")); fig.add_trace(go.Scatter(x=[qop],y=[pop],mode="markers",marker=dict(size=13),name="Operating point")); fig.update_xaxes(title="Liquid rate (stb/d)"); fig.update_yaxes(title="Pwf (psi)"); fig.update_layout(height=560,title="Integrated Nodal Analysis")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_25(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        visc=st.slider("Fluid viscosity (cP)",1.0,1000.0,80.0,5.0)
        freq=st.slider("VFD frequency (Hz)",35.0,70.0,60.0,1.0)
        stages=st.slider("Pump stages",50,400,180,10)
    q=np.linspace(0,6000,300)
    scale=freq/60
    q60=q/scale
    head0=np.maximum(280-0.000007*(q60-2800)**2,30)
    eff0=np.maximum(.72-0.00000005*(q60-3000)**2,.15)
    ch=1/(1+.0009*(visc-1)**.72); cq=1/(1+.00045*(visc-1)**.68); ce=1/(1+.0014*(visc-1)**.70)
    head=head0*ch*scale**2*stages; eff=eff0*ce
    q_adj=q*cq
    bep=q_adj[np.argmax(eff)]
    _metric_row([("Head factor CH",f"{ch:.3f}",None),("Efficiency factor Cη",f"{ce:.3f}",None),("Derated BEP",f"{bep:.0f} bpd",None)])
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Scatter(x=q_adj,y=head,name="Head"),secondary_y=False); fig.add_trace(go.Scatter(x=q_adj,y=eff*100,name="Efficiency"),secondary_y=True)
    fig.update_xaxes(title="Flow rate (bpd)"); fig.update_yaxes(title="Head (ft)",secondary_y=False); fig.update_yaxes(title="Efficiency (%)",secondary_y=True); fig.update_layout(height=560,title="ESP Viscosity Derating Sandbox")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_26(uploaded: pd.DataFrame | None) -> None:
    wells=["A","B","C","D","E"]
    base=np.array([420,560,310,680,390.])
    a=np.array([0.22,0.16,0.28,0.12,0.24]); b=np.array([1.8e-5,1.4e-5,2.2e-5,1.0e-5,1.9e-5])
    with st.sidebar:
        cap=st.slider("Total compressor capacity (Mscf/d)",500,12000,5000,250)
        gas_price=st.slider("Gas opportunity cost ($/Mscf)",0.0,10.0,3.0,.5)
    def oil(q): return base+a*q-b*q*q
    def obj(q): return -np.sum(oil(q))
    cons={"type":"ineq","fun":lambda q:cap-np.sum(q)}
    res=minimize(obj,np.full(5,cap/5),method="SLSQP",bounds=[(0,4000)]*5,constraints=cons)
    q=np.clip(res.x,0,None); qo=oil(q); gain=qo-base
    _metric_row([("Allocated gas",f"{q.sum():.0f} Mscf/d",None),("Incremental oil",f"{gain.sum():.0f} bopd",None),("Oil / lift gas",f"{gain.sum()/max(q.sum(),1):.3f} bbl/Mscf",None)])
    fig=go.Figure(); fig.add_trace(go.Bar(x=wells,y=q,name="Optimal gas")); fig.add_trace(go.Bar(x=wells,y=gain*10,name="Incremental oil ×10")); fig.update_layout(barmode="group",height=540,title="Constrained Gas-Lift Allocation")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_27(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        pup=st.slider("Upstream pressure (psi)",500,8000,3200,100)
        pdown=st.slider("Downstream pressure (psi)",50,3000,600,50)
        q=st.slider("Mixture rate (bbl/d equiv.)",100,40000,9000,500)
        rho=st.slider("Mixture density (lb/ft³)",5.0,65.0,28.0,1.0)
        choke=st.slider("Choke ID (in)",.5,4.0,1.5,.125)
        c=st.slider("API RP 14E c-factor",75.0,150.0,100.0,5.0)
    area=math.pi*(choke/12)**2/4
    v=q*5.615/86400/max(area,EPS)
    ve=c/math.sqrt(rho)
    ratio=pdown/pup; critical=ratio<0.55
    risk=v>ve
    _metric_row([("Flow regime","Sonic/critical" if critical else "Sub-critical",None),("Actual velocity",f"{v:.1f} ft/s",None),("Erosional limit",f"{ve:.1f} ft/s","RISK" if risk else "SAFE")])
    fig=go.Figure(go.Indicator(mode="gauge+number+delta",value=v,delta={"reference":ve},title={"text":"Mixture velocity vs API RP 14E"},gauge={"axis":{"range":[0,max(ve*1.6,v*1.2)]},"threshold":{"value":ve}})); fig.update_layout(height=420)
    st.plotly_chart(fig,use_container_width=True)


def _render_day_28(uploaded: pd.DataFrame | None) -> None:
    x=np.linspace(0,2000,60)
    with st.sidebar:
        completion=st.selectbox("Completion",["Open-hole / slotted liner","AICD equalized"])
        friction=st.slider("Heel-to-toe friction strength",0.0,2.0,1.0,.1)
        water_risk=st.slider("Heel water breakthrough severity",0.0,1.0,.55,.05)
    heel=np.exp(-x/450)
    oil=120*(1+friction*heel)
    water=35*(1+3*water_risk*heel)
    if completion.startswith("AICD"):
        oil=0.75*oil+0.25*np.mean(oil); water=0.45*water+0.55*np.mean(water)
    cv=np.std(oil)/np.mean(oil)
    _metric_row([("Oil inflow CV",f"{cv:.3f}",None),("Heel water rate",f"{water[0]:.1f}",None),("Toe oil rate",f"{oil[-1]:.1f}",None)])
    fig=go.Figure(); fig.add_trace(go.Scatter(x=x,y=oil,name="Oil inflow")); fig.add_trace(go.Scatter(x=x,y=water,name="Water inflow")); fig.update_xaxes(title="Distance heel → toe (m)"); fig.update_yaxes(title="Segment inflow index"); fig.update_layout(height=540,title="Horizontal Completion Inflow Equalization")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_29(uploaded: pd.DataFrame | None) -> None:
    d=np.linspace(0,12000,350)
    with st.sidebar:
        qg=st.slider("Gas rate (MMscf/d)",0.2,30.0,5.0,.2)
        pwh=st.slider("Wellhead pressure (psi)",80,2500,520,20)
        tid=st.slider("Tubing ID (in)",1.5,5.5,2.875,.125)
    p=pwh+0.16*d; rho_g=np.maximum(.0032*p,.15); area=math.pi*(tid/12)**2/4
    actual=qg*1e6/86400*14.7/np.maximum(p,1)/area
    turner=1.593*(45**.25)*np.maximum(55-rho_g,EPS)**.25/np.sqrt(rho_g)
    coleman=.82*turner; li=.72*turner
    margin=actual-turner
    idx=np.where(margin<0)[0]; onset=d[idx[0]] if len(idx) else np.nan
    _metric_row([("Turner loading onset",f"{onset:.0f} ft" if np.isfinite(onset) else "None",None),("Bottom velocity margin",f"{margin[-1]:.2f} ft/s",None),("Tubing ID",f"{tid:.3f} in",None)])
    fig=go.Figure();
    for x,name in [(actual,"Actual"),(turner,"Turner"),(coleman,"Coleman"),(li,"Li")]: fig.add_trace(go.Scatter(x=x,y=d,name=name))
    fig.update_yaxes(autorange="reversed",title="Depth (ft)"); fig.update_xaxes(title="Superficial gas velocity (ft/s)"); fig.update_layout(height=590,title="Gas Well Critical Velocity Profiler")
    st.plotly_chart(fig,use_container_width=True)


def _render_day_30(uploaded: pd.DataFrame | None) -> None:
    with st.sidebar:
        pr=st.slider("Asset reservoir pressure (psi)",1200,6000,3400,100)
        rw=st.slider("Formation Rw (ohm·m)",.02,.30,.08,.01)
        pwh=st.slider("Wellhead pressure (psi)",50,1600,400,25)
        lift_cap=st.slider("Lift/compression capacity index",0.5,1.5,1.0,.05)
    # Petrophysical block
    df=_day1_benchmark(); igr=np.clip((df.GR-25)/95,0,1); vsh=np.clip(.083*(2**(3.7*igr)-1),0,1); phi=np.clip((2.65-df.RHOB)/1.65*(1-vsh),.01,.4); sw=np.clip((rw/(np.maximum(df.RT,EPS)*phi**2))**.5,0,1)
    pay=((vsh<.4)&(phi>.1)&(sw<.6)).mean()
    # Material-balance pressure KPI
    depletion=(4200-pr)/4200
    # Trajectory clearance proxy
    md=np.arange(0,4200,100); inc=np.clip((md-400)/2600*78,0,78); azi=35+8*np.sin(md/900); tvd,n,e=_minimum_curvature(md,inc,azi); _,n2,e2=_minimum_curvature(md,inc*.95,azi+8); e2+=420; clearance=np.sqrt((n-n2)**2+(e-e2)**2).min()
    # Nodal block
    qmax=4500*(pr/3600)*lift_cap; q=np.linspace(0,max(qmax,100),300); disc=.04-3.2*(q/max(qmax,1)-1); ipr=pr*np.clip((-.2+np.sqrt(np.maximum(disc,0)))/1.6,0,1); vlp=pwh+780+(q/1000)**1.8*380/lift_cap; idx=np.argmin(abs(ipr-vlp)); qop=q[idx]
    compressor_flag=qop<1800 and pr<2600
    _metric_row([("Reservoir net-pay fraction",f"{pay:.1%}",None),("Pressure depletion",f"{depletion:.1%}",None),("Min trajectory clearance",f"{clearance:.1f} m",None),("Operating rate",f"{qop:.0f} stb/d","Lift support required" if compressor_flag else "Within current lift envelope")])
    tab1,tab2,tab3,tab4=st.tabs(["Formation","Reservoir","Well Geometry","Production"])
    with tab1:
        fig=go.Figure(go.Scatter(x=sw,y=df.DEPTH,name="Sw")); fig.update_yaxes(autorange="reversed",title="Depth"); fig.update_layout(height=430,title="Formation Saturation State"); st.plotly_chart(fig,use_container_width=True)
    with tab2:
        fig=go.Figure(go.Indicator(mode="gauge+number",value=pr,title={"text":"Current Reservoir Pressure"},gauge={"axis":{"range":[0,6000]}})); fig.update_layout(height=380); st.plotly_chart(fig,use_container_width=True)
    with tab3:
        fig=go.Figure(); fig.add_trace(go.Scatter3d(x=e,y=n,z=-tvd,mode="lines",name="Producer")); fig.add_trace(go.Scatter3d(x=e2,y=n2,z=-tvd,mode="lines",name="Offset")); fig.update_layout(height=500,title="Trajectory Clearance"); st.plotly_chart(fig,use_container_width=True)
    with tab4:
        fig=go.Figure(); fig.add_trace(go.Scatter(x=q,y=ipr,name="IPR")); fig.add_trace(go.Scatter(x=q,y=vlp,name="VLP")); fig.add_trace(go.Scatter(x=[qop],y=[(ipr[idx]+vlp[idx])/2],mode="markers",marker=dict(size=13),name="Operating point")); fig.update_layout(height=500,title="Asset Nodal Response"); st.plotly_chart(fig,use_container_width=True)


_RENDERERS: dict[int, Callable[[pd.DataFrame | None], None]] = {
    1:_render_day_01,2:_render_day_02,3:_render_day_03,4:_render_day_04,5:_render_day_05,6:_render_day_06,7:_render_day_07,8:_render_day_08,
    9:_render_day_09,10:_render_day_10,11:_render_day_11,12:_render_day_12,13:_render_day_13,14:_render_day_14,15:_render_day_15,16:_render_day_16,
    17:_render_day_17,18:_render_day_18,19:_render_day_19,20:_render_day_20,21:_render_day_21,22:_render_day_22,23:_render_day_23,24:_render_day_24,
    25:_render_day_25,26:_render_day_26,27:_render_day_27,28:_render_day_28,29:_render_day_29,30:_render_day_30,
}


def render_lab(day: int, uploaded: pd.DataFrame | None = None) -> None:
    renderer=_RENDERERS.get(day)
    if renderer is None:
        st.error(f"No renderer registered for Day {day:02d}")
        return
    renderer(uploaded)