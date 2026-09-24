# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import os
# from datetime import datetime
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots


# # ====================================================
# # PAGE CONFIGURATION
# # ====================================================

# st.set_page_config(
#     page_title="TCS | Stock Terminal",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# # ====================================================
# # SESSION STATE DEFAULTS
# # ====================================================

# if "theme" not in st.session_state:
#     st.session_state.theme = "dark"


# # ====================================================
# # THEME DEFINITIONS
# # ====================================================

# THEMES = {
#     "dark": dict(
#         BG="#080a12", TEXT="#e9ecf6", TEXT_MUTED="#8892b0", TEXT_MUTED2="#7d87a3",
#         BORDER="#1c2338", BORDER2="#232c48", CARD1="#131a2c", CARD2="#0d1120",
#         HERO1="#0d1120", HERO2="#090b14", PREDICT1="#171f38", PREDICT2="#10142280",
#         INPUT_BG="#131a2c", SIDEBAR1="#0b0e18", SIDEBAR2="#070911",
#         SHINE="rgba(255,255,255,0.06)", GRID_OP="0.55", CHART_GRID="#1c2338",
#         CHART_FONT="#c9cfe3", NAV_BG="#0d1120", NAV_ACTIVE="#171f38",
#     ),
#     "light": dict(
#         BG="#f3f5fb", TEXT="#161a2c", TEXT_MUTED="#525a72", TEXT_MUTED2="#697088",
#         BORDER="#dde1f0", BORDER2="#ccd2e8", CARD1="#ffffff", CARD2="#f4f6fc",
#         HERO1="#ffffff", HERO2="#eef0fb", PREDICT1="#ffffff", PREDICT2="#f4f6fbdd",
#         INPUT_BG="#ffffff", SIDEBAR1="#ffffff", SIDEBAR2="#eef0fb",
#         SHINE="rgba(124,92,255,0.10)", GRID_OP="0.22", CHART_GRID="#dde1f0",
#         CHART_FONT="#3a4160", NAV_BG="#ffffff", NAV_ACTIVE="#eef0fb",
#     ),
# }


# def build_css(theme_name: str) -> str:
#     v = THEMES[theme_name]

#     css = """
#     @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#     .stApp { background: __BG__; color: __TEXT__; }

#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}

#     /* ================= HERO / PERSPECTIVE GRID ================= */

#     .hero-wrap {
#         position: relative;
#         border-radius: 20px;
#         padding: 34px 34px 26px 34px;
#         margin-bottom: 20px;
#         overflow: hidden;
#         background:
#             radial-gradient(circle at 15% 0%, rgba(124,92,255,0.22), transparent 55%),
#             radial-gradient(circle at 90% 10%, rgba(240,180,41,0.10), transparent 45%),
#             linear-gradient(180deg, __HERO1__ 0%, __HERO2__ 100%);
#         border: 1px solid __BORDER__;
#     }

#     .grid-floor {
#         position: absolute;
#         left: 0; right: 0; bottom: -40px;
#         height: 160px;
#         background-image:
#             linear-gradient(rgba(124,92,255,0.35) 1px, transparent 1px),
#             linear-gradient(90deg, rgba(124,92,255,0.35) 1px, transparent 1px);
#         background-size: 42px 28px;
#         transform: perspective(280px) rotateX(62deg);
#         transform-origin: bottom;
#         mask-image: linear-gradient(to top, black 20%, transparent 90%);
#         -webkit-mask-image: linear-gradient(to top, black 20%, transparent 90%);
#         opacity: __GRID_OP__;
#         pointer-events: none;
#     }

#     .ticker-badge {
#         background: linear-gradient(135deg, #7c5cff, #4c2fd4);
#         color: white;
#         font-weight: 700;
#         font-size: 12.5px;
#         padding: 5px 12px;
#         border-radius: 6px;
#         letter-spacing: 0.6px;
#         box-shadow: 0 4px 14px rgba(124,92,255,0.4);
#     }

#     .ticker-row {
#         position: relative; z-index: 2;
#         display: flex; align-items: center; justify-content: space-between;
#         margin-bottom: 16px; flex-wrap: wrap; gap: 10px;
#     }

#     .ticker-live {
#         display: flex; align-items: center; gap: 6px;
#         font-size: 12px; color: #2dd4bf; font-weight: 600;
#         letter-spacing: 0.5px; font-family: 'JetBrains Mono', monospace;
#     }

#     .dot {
#         height: 7px; width: 7px; background-color: #2dd4bf; border-radius: 50%;
#         display: inline-block; box-shadow: 0 0 8px #2dd4bf; animation: pulse 1.6s infinite;
#     }

#     @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

#     .hero-title {
#         position: relative; z-index: 2;
#         font-family: 'Space Grotesk', sans-serif;
#         font-size: 36px; font-weight: 700; color: __TEXT__;
#         letter-spacing: -0.5px; margin-bottom: 4px;
#     }

#     .hero-title span {
#         background: linear-gradient(90deg, #7c5cff, #f0b429);
#         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     }

#     .hero-sub { position: relative; z-index: 2; color: __TEXT_MUTED__; font-size: 14px; max-width: 600px; }

#     /* ================= TOP NAV STRIP ================= */

#     div[data-testid="stTabs"] button[data-baseweb="tab"] {
#         font-family: 'Space Grotesk', sans-serif;
#         font-weight: 600;
#         font-size: 14px;
#         color: __TEXT_MUTED__;
#         padding: 10px 16px;
#     }

#     div[data-testid="stTabs"] button[aria-selected="true"] {
#         color: #7c5cff !important;
#         border-bottom: 2px solid #7c5cff !important;
#     }

#     div[data-testid="stTabs"] {
#         border-bottom: 1px solid __BORDER__;
#         margin-bottom: 18px;
#     }

#     /* ================= SECTION HEADERS ================= */

#     .section-header {
#         font-family: 'Space Grotesk', sans-serif;
#         font-size: 17px; font-weight: 600; color: __TEXT__;
#         margin-top: 6px; margin-bottom: 14px;
#         display: flex; align-items: center; gap: 8px;
#     }

#     .section-header .eyebrow {
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 11px; color: #7c5cff;
#         background: rgba(124,92,255,0.12);
#         border: 1px solid rgba(124,92,255,0.3);
#         padding: 2px 8px; border-radius: 5px; letter-spacing: 0.5px;
#     }

#     .subtext { color: __TEXT_MUTED__; font-size: 13px; margin-top: -8px; margin-bottom: 14px; }

#     /* ================= 3D TILT METRIC CARDS ================= */

#     .tilt-card {
#         background: linear-gradient(160deg, __CARD1__, __CARD2__);
#         border: 1px solid __BORDER2__;
#         border-radius: 14px; padding: 16px 18px; height: 100%;
#         transform-style: preserve-3d; perspective: 800px;
#         transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
#     }

#     .tilt-card:hover {
#         transform: perspective(800px) rotateX(4deg) rotateY(-4deg) translateY(-3px) scale(1.015);
#         border-color: #7c5cff;
#         box-shadow: 0 14px 34px rgba(124,92,255,0.22);
#     }

#     .metric-label {
#         font-size: 12px; color: __TEXT_MUTED2__; text-transform: uppercase;
#         letter-spacing: 0.8px; font-weight: 600; margin-bottom: 6px;
#     }

#     .metric-value {
#         font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 700; color: __TEXT__;
#     }

#     .metric-sub { font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

#     /* ================= PREDICTION HOLO CARD ================= */

#     .predict-card {
#         position: relative;
#         background: linear-gradient(150deg, __PREDICT1__ 0%, __PREDICT2__ 100%);
#         border: 1px solid #33406a;
#         border-radius: 20px; padding: 32px 34px; margin-top: 8px;
#         transform-style: preserve-3d; perspective: 1000px;
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#         box-shadow: 0 10px 40px rgba(124,92,255,0.16);
#         overflow: hidden;
#     }

#     .predict-card:hover {
#         transform: perspective(1000px) rotateX(3deg) rotateY(-2deg) translateY(-4px);
#         box-shadow: 0 20px 60px rgba(124,92,255,0.28);
#     }

#     .predict-card::before {
#         content: ""; position: absolute; top: -60%; left: -20%;
#         width: 60%; height: 220%;
#         background: linear-gradient(120deg, transparent, __SHINE__, transparent);
#         transform: rotate(20deg); pointer-events: none;
#     }

#     .predict-label {
#         font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: __TEXT_MUTED2__;
#         text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
#     }

#     .predict-price {
#         font-family: 'JetBrains Mono', monospace; font-size: 46px; font-weight: 700; color: __TEXT__;
#         margin: 8px 0 12px 0; text-shadow: 0 0 30px rgba(124,92,255,0.30);
#     }

#     .badge-up {
#         background: rgba(45, 212, 191, 0.12); color: #2dd4bf;
#         border: 1px solid rgba(45, 212, 191, 0.4);
#         padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
#         font-family: 'JetBrains Mono', monospace; display: inline-block;
#     }

#     .badge-down {
#         background: rgba(255, 92, 92, 0.12); color: #ff5c5c;
#         border: 1px solid rgba(255, 92, 92, 0.4);
#         padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
#         font-family: 'JetBrains Mono', monospace; display: inline-block;
#     }

#     .badge-flat {
#         background: rgba(148, 163, 184, 0.12); color: #94a3b8;
#         border: 1px solid rgba(148, 163, 184, 0.35);
#         padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
#         font-family: 'JetBrains Mono', monospace; display: inline-block;
#     }

#     /* ================= SIGNAL BADGES (BUY/HOLD/SELL) ================= */

#     .signal-chip {
#         display: inline-flex; align-items: center; gap: 8px;
#         padding: 10px 20px; border-radius: 12px;
#         font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px;
#         letter-spacing: 0.5px;
#     }

#     .signal-buy { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
#     .signal-sell { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
#     .signal-hold { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }

#     .signal-note { font-size: 12px; color: __TEXT_MUTED2__; margin-top: 8px; font-style: italic; }

#     /* ================= BUTTONS ================= */

#     div.stButton > button {
#         background: linear-gradient(135deg, #7c5cff, #4c2fd4);
#         color: white; font-weight: 700; font-size: 15px;
#         font-family: 'Space Grotesk', sans-serif; border: none; border-radius: 10px;
#         padding: 12px 0; box-shadow: 0 4px 18px rgba(124,92,255,0.35);
#         transition: transform 0.15s ease, box-shadow 0.15s ease;
#     }

#     div.stButton > button:hover {
#         transform: translateY(-2px); box-shadow: 0 10px 28px rgba(124,92,255,0.5); color: white;
#     }

#     div.stDownloadButton > button {
#         background: __CARD1__; color: __TEXT__; font-weight: 600;
#         border: 1px solid __BORDER2__; border-radius: 10px;
#     }

#     /* ================= INPUTS ================= */

#     div[data-baseweb="input"] { background-color: __INPUT_BG__ !important; border-radius: 8px !important; }

#     /* ================= SIDEBAR ================= */

#     section[data-testid="stSidebar"] {
#         background: linear-gradient(180deg, __SIDEBAR1__, __SIDEBAR2__);
#         border-right: 1px solid __BORDER__;
#     }

#     /* ================= MISC ================= */

#     hr { border-color: __BORDER__ !important; }

#     .stDataFrame { border: 1px solid __BORDER2__; border-radius: 10px; overflow: hidden; }

#     .footer-note {
#         text-align: center; color: __TEXT_MUTED2__; font-size: 12px;
#         font-family: 'JetBrains Mono', monospace; padding: 10px 0 4px 0;
#     }
#     """

#     for key, val in v.items():
#         css = css.replace(f"__{key}__", val)

#     return f"<style>{css}</style>"


# st.markdown(build_css(st.session_state.theme), unsafe_allow_html=True)
# THEME = THEMES[st.session_state.theme]


# # ====================================================
# # LOAD MODEL AND DATA  (unchanged pipeline / artifacts)
# # ====================================================

# MODEL_PATH = "TCS_stock_model.pkl"
# SCALER_PATH = "TCS_scaler.pkl"
# DATA_PATH = "TCS_stock_cleaned.csv"


# @st.cache_resource(show_spinner=False)
# def load_model():
#     return joblib.load(MODEL_PATH)


# @st.cache_resource(show_spinner=False)
# def load_scaler():
#     return joblib.load(SCALER_PATH)


# @st.cache_data(show_spinner=False)
# def load_data():
#     return pd.read_csv(DATA_PATH)


# with st.spinner("Booting stock terminal · loading model and market data..."):
#     try:
#         if not os.path.exists(MODEL_PATH):
#             raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
#         if not os.path.exists(SCALER_PATH):
#             raise FileNotFoundError(
#                 f"Scaler file not found: {SCALER_PATH}. This model was trained on "
#                 f"StandardScaler-scaled features, so the scaler is required to make "
#                 f"correct predictions — re-run the training notebook to generate it."
#             )
#         if not os.path.exists(DATA_PATH):
#             raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

#         model = load_model()
#         scaler = load_scaler()
#         df = load_data()

#         if df.empty:
#             raise ValueError("Loaded dataset is empty.")

#         required_cols = {"Open", "High", "Low", "Close"}
#         missing_cols = required_cols - set(df.columns)
#         if missing_cols:
#             raise ValueError(f"Dataset is missing required column(s): {', '.join(sorted(missing_cols))}")

#     except Exception as e:
#         st.error(f"⚠️ Failed to initialize the terminal: {e}")
#         st.stop()

# has_predicted_col = "Predicted_Close" in df.columns
# has_date_col = "Date" in df.columns
# has_volume = "Volume" in df.columns


# # ====================================================
# # BACKTEST: MODEL PREDICTIONS vs ACTUAL (real data only)
# # Computed early so both the sidebar and the Model Performance tab can use it.
# # ====================================================

# @st.cache_data(show_spinner=False)
# def compute_backtest(_model, _scaler, data: pd.DataFrame):
#     """
#     Runs the SAME prediction call used for live forecasting (scaled inputs,
#     matching how the model was trained) across the historical dataset, and
#     compares it against the real 'Predicted_Close' ground-truth column
#     already present in the cleaned dataset. No values are invented — this
#     is the model's actual output on real past rows.
#     """
#     if "Predicted_Close" not in data.columns:
#         return None

#     working = data.copy()
#     if "Date" in working.columns:
#         working["Date"] = pd.to_datetime(working["Date"])
#         working = working.sort_values("Date").reset_index(drop=True)

#     working = working.dropna(subset=["Open", "High", "Low", "Close", "Predicted_Close"])
#     if working.empty:
#         return None

#     X_hist = working[["Open", "High", "Low", "Close"]].values
#     X_hist_scaled = _scaler.transform(X_hist)
#     y_model = _model.predict(X_hist_scaled)

#     result = working.copy()
#     result["Model_Predicted"] = y_model
#     result["Error"] = result["Model_Predicted"] - result["Predicted_Close"]
#     return result


# with st.spinner("Running historical backtest..."):
#     backtest_df = compute_backtest(model, scaler, df)

# if backtest_df is not None and len(backtest_df) > 0:
#     err = backtest_df["Error"].values
#     actual = backtest_df["Predicted_Close"].values
#     mae = float(np.mean(np.abs(err)))
#     rmse = float(np.sqrt(np.mean(err ** 2)))
#     ss_res = float(np.sum(err ** 2))
#     ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
#     r2 = 1 - ss_res / ss_tot if ss_tot != 0 else float("nan")
#     nonzero = actual != 0
#     mape = float(np.mean(np.abs(err[nonzero] / actual[nonzero]))) * 100 if nonzero.any() else float("nan")
# else:
#     mae = rmse = r2 = mape = None


# # ====================================================
# # HERO / TICKER HEADER
# # ====================================================

# st.markdown(f"""
# <div class="hero-wrap">
#     <div class="grid-floor"></div>
#     <div class="ticker-row">
#         <div style="display:flex; align-items:center; gap:10px;">
#             <span class="ticker-badge">TCS · NSE</span>
#         </div>
#         <div class="ticker-live">
#             <span class="dot"></span> LIVE MODEL &nbsp;·&nbsp; {datetime.now().strftime("%d %b %Y, %I:%M %p")}
#         </div>
#     </div>
#     <div class="hero-title">Tata Consultancy Services <span>Price Forecast</span></div>
#     <div class="hero-sub">
#         A machine-learning terminal that reads today's Open, High, Low and Close
#         to project TCS's next closing price — with a live candlestick view of the
#         trend behind it and a transparent look at how the model has performed historically.
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ====================================================
# # SIDEBAR
# # ====================================================

# with st.sidebar:
#     st.markdown("### 📊 Stock Terminal")
#     st.caption("AI-powered TCS price forecasting")
#     st.divider()

#     st.markdown("**Appearance**")
#     theme_choice = st.radio(
#         "Theme", options=["Dark", "Light"],
#         index=0 if st.session_state.theme == "dark" else 1,
#         horizontal=True, label_visibility="collapsed",
#     )
#     new_theme = "dark" if theme_choice == "Dark" else "light"
#     if new_theme != st.session_state.theme:
#         st.session_state.theme = new_theme
#         st.rerun()

#     st.divider()
#     st.markdown("**About this tool**")
#     st.write(
#         "This terminal uses a trained machine learning model to forecast "
#         "TCS's next closing price based on Open, High, Low and Close values."
#     )
#     st.divider()
#     st.markdown("**Dataset**")
#     st.write(f"📅 {len(df):,} trading days loaded")
#     if has_date_col:
#         try:
#             d_min = pd.to_datetime(df["Date"]).min().strftime("%d %b %Y")
#             d_max = pd.to_datetime(df["Date"]).max().strftime("%d %b %Y")
#             st.write(f"🗓️ {d_min} → {d_max}")
#         except Exception:
#             pass
#     st.write(f"🧠 Model: `{type(model).__name__}`")
#     st.write(f"⚙️ Preprocessing: `{type(scaler).__name__}` (fit during training)")
#     if mae is not None:
#         st.write(f"🎯 Backtest R²: `{r2:.4f}`  ·  MAE: `₹{mae:.2f}`")
#     st.divider()
#     st.caption("⚠️ For educational purposes only. Not financial advice.")


# # ====================================================
# # LATEST DATA
# # ====================================================

# latest_row = df.iloc[-1]
# latest_open = float(latest_row["Open"])
# latest_high = float(latest_row["High"])
# latest_low = float(latest_row["Low"])
# latest_close = float(latest_row["Close"])


# # ====================================================
# # CHART DATA PREP (cached — computed once, reused across tabs)
# # ====================================================

# @st.cache_data(show_spinner=False)
# def prepare_chart_data(raw_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     One-time computation of everything the charts need: sorted dates,
#     moving averages, and daily change direction for volume colouring.
#     """
#     data = raw_df.copy()
#     if "Date" in data.columns:
#         data["Date"] = pd.to_datetime(data["Date"])
#         data = data.sort_values("Date").reset_index(drop=True)
#     else:
#         data = data.reset_index(drop=True)

#     data["SMA20"] = data["Close"].rolling(window=20, min_periods=1).mean()
#     data["SMA50"] = data["Close"].rolling(window=50, min_periods=1).mean()
#     data["EMA9"] = data["Close"].ewm(span=9, adjust=False).mean()

#     data["Change"] = data["Close"].diff()
#     data["Direction"] = np.where(data["Change"] >= 0, "up", "down")

#     return data


# full_chart_data = prepare_chart_data(df)


# # ====================================================
# # TOP NAVIGATION (TABS)
# # ====================================================

# tab_overview, tab_predict, tab_charts, tab_history, tab_model = st.tabs(
#     ["📊  Overview", "🔮  Predict", "📈  Charts", "🕒  History", "🎯  Model Performance"]
# )


# # ----------------------------------------------------
# # TAB 1 — OVERVIEW
# # ----------------------------------------------------

# with tab_overview:

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">SNAPSHOT</span> Latest Market Data</div>',
#         unsafe_allow_html=True
#     )

#     col1, col2, col3, col4 = st.columns(4)
#     metric_cols = [
#         (col1, "Open", latest_open),
#         (col2, "High", latest_high),
#         (col3, "Low", latest_low),
#         (col4, "Close", latest_close),
#     ]
#     for col, label, value in metric_cols:
#         with col:
#             st.markdown(f"""
#             <div class="tilt-card">
#                 <div class="metric-label">{label}</div>
#                 <div class="metric-value">₹{value:.2f}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.write("")

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">STATS</span> Dataset-Wide Highlights</div>',
#         unsafe_allow_html=True
#     )

#     all_time_high = float(df["Close"].max())
#     all_time_low = float(df["Close"].min())

#     window_30 = full_chart_data.tail(30)
#     trend_30 = float(window_30["Close"].iloc[-1] - window_30["Close"].iloc[0]) if len(window_30) > 1 else 0.0
#     trend_30_pct = (trend_30 / window_30["Close"].iloc[0]) * 100 if len(window_30) > 1 and window_30["Close"].iloc[0] != 0 else 0.0

#     scol1, scol2, scol3, scol4 = st.columns(4)
#     with scol1:
#         st.markdown(f"""
#         <div class="tilt-card">
#             <div class="metric-label">All-Time High</div>
#             <div class="metric-value">₹{all_time_high:.2f}</div>
#         </div>""", unsafe_allow_html=True)
#     with scol2:
#         st.markdown(f"""
#         <div class="tilt-card">
#             <div class="metric-label">All-Time Low</div>
#             <div class="metric-value">₹{all_time_low:.2f}</div>
#         </div>""", unsafe_allow_html=True)
#     with scol3:
#         trend_color = "#2dd4bf" if trend_30 >= 0 else "#ff5c5c"
#         arrow = "▲" if trend_30 >= 0 else "▼"
#         st.markdown(f"""
#         <div class="tilt-card">
#             <div class="metric-label">30-Day Trend</div>
#             <div class="metric-value" style="color:{trend_color};">{arrow} {trend_30_pct:+.2f}%</div>
#         </div>""", unsafe_allow_html=True)
#     with scol4:
#         if has_volume:
#             avg_vol = float(df["Volume"].tail(30).mean())
#             vol_display = f"{avg_vol:,.0f}"
#         else:
#             vol_display = "N/A"
#         st.markdown(f"""
#         <div class="tilt-card">
#             <div class="metric-label">Avg Volume (30d)</div>
#             <div class="metric-value">{vol_display}</div>
#         </div>""", unsafe_allow_html=True)

#     st.write("")

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">GLANCE</span> Recent Price Action (90 Days)</div>',
#         unsafe_allow_html=True
#     )

#     glance_data = full_chart_data.tail(90)
#     x_axis = glance_data["Date"] if has_date_col else glance_data.index

#     fig_glance = go.Figure()
#     fig_glance.add_trace(go.Scatter(
#         x=x_axis, y=glance_data["Close"], mode="lines",
#         line=dict(color="#7c5cff", width=2),
#         fill="tozeroy", fillcolor="rgba(124,92,255,0.12)",
#         name="Close", showlegend=False,
#     ))
#     fig_glance.update_layout(
#         height=220, margin=dict(l=10, r=10, t=10, b=10),
#         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=10),
#         hovermode="x unified",
#     )
#     fig_glance.update_xaxes(gridcolor=THEME["CHART_GRID"], showticklabels=True)
#     fig_glance.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="₹")
#     st.plotly_chart(fig_glance, use_container_width=True, config={"displayModeBar": False})


# # ----------------------------------------------------
# # TAB 2 — PREDICT
# # ----------------------------------------------------

# with tab_predict:

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">INPUT</span> Enter Stock Values</div>',
#         unsafe_allow_html=True
#     )
#     st.markdown(
#         '<div class="subtext">Defaults are pre-filled with the most recent trading day. Adjust any value to test a different scenario.</div>',
#         unsafe_allow_html=True
#     )

#     col1, col2 = st.columns(2)

#     with col1:
#         open_price = st.number_input("Open Price (₹)", min_value=0.0, value=latest_open, step=0.10)
#         high_price = st.number_input("High Price (₹)", min_value=0.0, value=latest_high, step=0.10)

#     with col2:
#         low_price = st.number_input("Low Price (₹)", min_value=0.0, value=latest_low, step=0.10)
#         close_price = st.number_input("Close Price (₹)", min_value=0.0, value=latest_close, step=0.10)

#     st.write("")

#     predict_button = st.button(
#         "🔮  Predict Tomorrow's Closing Price", type="primary", use_container_width=True
#     )

#     if predict_button:
#         try:
#             with st.spinner("Running model inference..."):

#                 # ---- PREDICTION LOGIC (matches training pipeline) ----
#                 # Model expects: Open, High, Low, Close — scaled with the
#                 # SAME StandardScaler fitted during training (TCS_scaler.pkl).
#                 # Feeding raw ₹-scale values directly into the model (as the
#                 # very first version of this app did) produces wildly wrong
#                 # predictions, since the model's coefficients were learned
#                 # on standardized (mean 0, std 1) inputs, not raw prices.
#                 input_data = np.array([[open_price, high_price, low_price, close_price]])
#                 input_scaled = scaler.transform(input_data)
#                 prediction = model.predict(input_scaled)
#                 predicted_price = float(prediction[0])
#                 # -------------------------------------------------------

#                 difference = predicted_price - close_price
#                 percentage = (difference / close_price) * 100 if close_price != 0 else 0.0

#             if predicted_price > close_price:
#                 badge_html = f'<span class="badge-up">▲ +₹{difference:.2f} ({percentage:.2f}%)</span>'
#                 trend_msg = "📈 The model predicts tomorrow's closing price may be **higher** than today's close."
#             elif predicted_price < close_price:
#                 badge_html = f'<span class="badge-down">▼ ₹{difference:.2f} ({percentage:.2f}%)</span>'
#                 trend_msg = "📉 The model predicts tomorrow's closing price may be **lower** than today's close."
#             else:
#                 badge_html = '<span class="badge-flat">● No change</span>'
#                 trend_msg = "➡️ The model predicts approximately the **same** closing price."

#             st.write("")
#             st.markdown(f"""
#             <div class="predict-card">
#                 <div class="predict-label">Predicted Closing Price · Tomorrow</div>
#                 <div class="predict-price">₹{predicted_price:.2f}</div>
#                 {badge_html}
#             </div>
#             """, unsafe_allow_html=True)

#             st.write("")

#             colA, colB = st.columns(2)
#             with colA:
#                 st.markdown(f"""
#                 <div class="tilt-card">
#                     <div class="metric-label">Current Closing Price</div>
#                     <div class="metric-value">₹{close_price:.2f}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             with colB:
#                 color = "#2dd4bf" if difference > 0 else ("#ff5c5c" if difference < 0 else "#94a3b8")
#                 st.markdown(f"""
#                 <div class="tilt-card">
#                     <div class="metric-label">Expected Change</div>
#                     <div class="metric-value" style="color:{color};">₹{difference:.2f} ({percentage:.2f}%)</div>
#                 </div>
#                 """, unsafe_allow_html=True)

#             st.write("")

#             # ---- Signal derived directly from the model's own % change ----
#             buy_th, sell_th = 0.5, -0.5
#             if percentage > buy_th:
#                 signal_html = '<div class="signal-chip signal-buy">🟢 BUY SIGNAL</div>'
#             elif percentage < sell_th:
#                 signal_html = '<div class="signal-chip signal-sell">🔴 SELL SIGNAL</div>'
#             else:
#                 signal_html = '<div class="signal-chip signal-hold">🟡 HOLD SIGNAL</div>'

#             st.markdown(
#                 f"""{signal_html}
#                 <div class="signal-note">
#                     Heuristic signal derived from the model's predicted % change
#                     (Buy if &gt; {buy_th}%, Sell if &lt; {sell_th}%, otherwise Hold).
#                     This is not financial advice.
#                 </div>""",
#                 unsafe_allow_html=True
#             )

#             st.write("")

#             if predicted_price > close_price:
#                 st.info(trend_msg)
#             elif predicted_price < close_price:
#                 st.warning(trend_msg)
#             else:
#                 st.info(trend_msg)

#             if mae is not None:
#                 st.caption(
#                     f"ℹ️ On historical backtesting, this model's next-day predictions have an average "
#                     f"error of ± ₹{mae:.2f} (MAE). See the **Model Performance** tab for full accuracy details."
#                 )

#         except Exception as e:
#             st.error(f"Prediction error: {e}")


# # ----------------------------------------------------
# # TAB 3 — CHARTS
# # ----------------------------------------------------

# with tab_charts:

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">CHART</span> TCS Price Action</div>',
#         unsafe_allow_html=True
#     )

#     range_options = {
#         "1M": 21, "3M": 63, "6M": 126, "1Y": 252, "3Y": 756, "All": len(full_chart_data),
#     }

#     ctrl_col1, ctrl_col2 = st.columns([3, 1])
#     with ctrl_col1:
#         selected_range = st.radio(
#             "Range", options=list(range_options.keys()), index=2,
#             horizontal=True, label_visibility="collapsed",
#         )
#     with ctrl_col2:
#         chart_type = st.selectbox("Chart type", options=["Candlestick", "Line"], label_visibility="collapsed")

#     lookback = range_options[selected_range]
#     plot_data = full_chart_data.tail(lookback).copy()
#     x_axis = plot_data["Date"] if has_date_col else plot_data.index

#     row_heights = [0.72, 0.28] if has_volume else [1.0]
#     rows = 2 if has_volume else 1

#     fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=row_heights)

#     if chart_type == "Candlestick":
#         fig.add_trace(go.Candlestick(
#             x=x_axis, open=plot_data["Open"], high=plot_data["High"],
#             low=plot_data["Low"], close=plot_data["Close"],
#             increasing_line_color="#2dd4bf", decreasing_line_color="#ff5c5c",
#             increasing_fillcolor="rgba(45,212,191,0.7)", decreasing_fillcolor="rgba(255,92,92,0.7)",
#             name="TCS", showlegend=False,
#         ), row=1, col=1)
#     else:
#         fig.add_trace(go.Scatter(
#             x=x_axis, y=plot_data["Close"], mode="lines",
#             line=dict(color=THEME["CHART_FONT"], width=1.8),
#             fill="tozeroy", fillcolor="rgba(124,92,255,0.08)",
#             name="Close", showlegend=False,
#         ), row=1, col=1)

#     fig.add_trace(go.Scatter(
#         x=x_axis, y=plot_data["EMA9"], mode="lines",
#         line=dict(color="#f0b429", width=1.3), name="EMA 9",
#     ), row=1, col=1)

#     fig.add_trace(go.Scatter(
#         x=x_axis, y=plot_data["SMA20"], mode="lines",
#         line=dict(color="#7c5cff", width=1.3), name="SMA 20",
#     ), row=1, col=1)

#     if lookback > 60:
#         fig.add_trace(go.Scatter(
#             x=x_axis, y=plot_data["SMA50"], mode="lines",
#             line=dict(color="#4c9aff", width=1.1, dash="dot"), name="SMA 50",
#         ), row=1, col=1)

#     if has_volume:
#         vol_colors = np.where(plot_data["Direction"] == "up", "rgba(45,212,191,0.55)", "rgba(255,92,92,0.55)")
#         fig.add_trace(go.Bar(
#             x=x_axis, y=plot_data["Volume"], marker_color=vol_colors, name="Volume", showlegend=False,
#         ), row=2, col=1)

#     fig.update_layout(
#         height=560 if has_volume else 460,
#         margin=dict(l=10, r=10, t=36, b=10),
#         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
#         hovermode="x unified", dragmode="pan",
#         legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
#     )

#     fig.update_xaxes(
#         gridcolor=THEME["CHART_GRID"], showspikes=True, spikemode="across",
#         spikecolor="#7c5cff", spikethickness=1, rangeslider_visible=False, row=rows, col=1,
#     )
#     if has_volume:
#         fig.update_xaxes(showticklabels=False, row=1, col=1)

#     fig.update_yaxes(
#         gridcolor=THEME["CHART_GRID"], side="right", title="Price (₹)",
#         showspikes=True, spikecolor="#7c5cff", spikethickness=1, row=1, col=1,
#     )
#     if has_volume:
#         fig.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="Vol", row=2, col=1)

#     st.plotly_chart(
#         fig, use_container_width=True,
#         config={
#             "displayModeBar": True, "displaylogo": False, "scrollZoom": True,
#             "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
#         },
#     )

#     last_point = plot_data.iloc[-1]
#     period_change = last_point["Close"] - plot_data.iloc[0]["Close"]
#     period_pct = (period_change / plot_data.iloc[0]["Close"]) * 100 if plot_data.iloc[0]["Close"] != 0 else 0.0
#     trend_color = "#2dd4bf" if period_change >= 0 else "#ff5c5c"
#     trend_arrow = "▲" if period_change >= 0 else "▼"

#     st.markdown(
#         f"""<span style="font-family:'JetBrains Mono',monospace; font-size:12.5px; color:{trend_color};">
#         {trend_arrow} {period_change:+.2f} ({period_pct:+.2f}%) over {selected_range}
#         </span> &nbsp;·&nbsp;
#         <span style="font-family:'JetBrains Mono',monospace; font-size:12.5px; color:{THEME['TEXT_MUTED2']};">
#         scroll to zoom · drag to pan · double-click to reset
#         </span>""",
#         unsafe_allow_html=True,
#     )


# # ----------------------------------------------------
# # TAB 4 — HISTORY
# # ----------------------------------------------------

# with tab_history:

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">TABLE</span> Historical TCS Data</div>',
#         unsafe_allow_html=True
#     )

#     max_rows = len(df)
#     default_rows = min(20, max_rows)
#     num_rows = st.slider(
#         "Rows to display (most recent first)",
#         min_value=min(5, max_rows), max_value=max_rows, value=default_rows,
#         step=1 if max_rows < 50 else 10,
#     )

#     display_df = df.tail(num_rows).sort_index(ascending=False)
#     st.dataframe(display_df, use_container_width=True)

#     csv_bytes = df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         "⬇️  Download Full Dataset (CSV)",
#         data=csv_bytes,
#         file_name="TCS_stock_cleaned.csv",
#         mime="text/csv",
#         use_container_width=True,
#     )


# # ----------------------------------------------------
# # TAB 5 — MODEL PERFORMANCE
# # ----------------------------------------------------

# with tab_model:

#     st.markdown(
#         '<div class="section-header"><span class="eyebrow">BACKTEST</span> Prediction vs Actual</div>',
#         unsafe_allow_html=True
#     )

#     if backtest_df is None:
#         st.warning(
#             "Historical actual-vs-predicted comparison isn't available — the dataset doesn't "
#             "include a `Predicted_Close` ground-truth column to compare against."
#         )
#     else:
#         st.markdown(
#             f"""<div class="subtext">
#             The model was run on every historical row's Open/High/Low/Close and compared against the
#             real next-day closing price already recorded in the dataset ({len(backtest_df):,} data points).
#             No values below are simulated.
#             </div>""",
#             unsafe_allow_html=True
#         )

#         mcol1, mcol2, mcol3, mcol4 = st.columns(4)
#         with mcol1:
#             st.markdown(f"""
#             <div class="tilt-card">
#                 <div class="metric-label">Mean Abs. Error</div>
#                 <div class="metric-value">₹{mae:.2f}</div>
#                 <div class="metric-sub">avg. rupee deviation</div>
#             </div>""", unsafe_allow_html=True)
#         with mcol2:
#             st.markdown(f"""
#             <div class="tilt-card">
#                 <div class="metric-label">RMSE</div>
#                 <div class="metric-value">₹{rmse:.2f}</div>
#                 <div class="metric-sub">penalizes large misses</div>
#             </div>""", unsafe_allow_html=True)
#         with mcol3:
#             r2_display = f"{r2:.4f}" if not np.isnan(r2) else "N/A"
#             st.markdown(f"""
#             <div class="tilt-card">
#                 <div class="metric-label">R² Score</div>
#                 <div class="metric-value">{r2_display}</div>
#                 <div class="metric-sub">variance explained</div>
#             </div>""", unsafe_allow_html=True)
#         with mcol4:
#             mape_display = f"{mape:.2f}%" if not np.isnan(mape) else "N/A"
#             st.markdown(f"""
#             <div class="tilt-card">
#                 <div class="metric-label">MAPE</div>
#                 <div class="metric-value">{mape_display}</div>
#                 <div class="metric-sub">avg. % error</div>
#             </div>""", unsafe_allow_html=True)

#         st.write("")

#         st.markdown(
#             '<div class="section-header"><span class="eyebrow">OVERLAY</span> Actual vs Model-Predicted Close</div>',
#             unsafe_allow_html=True
#         )

#         bt_range_options = {"90D": 90, "1Y": 252, "3Y": 756, "All": len(backtest_df)}
#         bt_range = st.radio(
#             "Backtest range", options=list(bt_range_options.keys()), index=1,
#             horizontal=True, label_visibility="collapsed", key="bt_range",
#         )
#         bt_lookback = bt_range_options[bt_range]
#         bt_plot = backtest_df.tail(bt_lookback)
#         bt_x = bt_plot["Date"] if "Date" in bt_plot.columns else bt_plot.index

#         fig_bt = go.Figure()
#         fig_bt.add_trace(go.Scatter(
#             x=bt_x, y=bt_plot["Predicted_Close"], mode="lines",
#             line=dict(color="#2dd4bf", width=1.8), name="Actual Next-Day Close",
#         ))
#         fig_bt.add_trace(go.Scatter(
#             x=bt_x, y=bt_plot["Model_Predicted"], mode="lines",
#             line=dict(color="#7c5cff", width=1.6, dash="dot"), name="Model Predicted",
#         ))
#         fig_bt.update_layout(
#             height=420, margin=dict(l=10, r=10, t=30, b=10),
#             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#             font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
#             hovermode="x unified",
#             legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
#         )
#         fig_bt.update_xaxes(gridcolor=THEME["CHART_GRID"])
#         fig_bt.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="₹")
#         st.plotly_chart(fig_bt, use_container_width=True, config={"displayModeBar": False})

#         st.write("")

#         st.markdown(
#             '<div class="section-header"><span class="eyebrow">SCATTER</span> Predicted vs Actual Correlation</div>',
#             unsafe_allow_html=True
#         )

#         sample = backtest_df.sample(min(2000, len(backtest_df)), random_state=42)
#         fig_scatter = go.Figure()
#         fig_scatter.add_trace(go.Scatter(
#             x=sample["Predicted_Close"], y=sample["Model_Predicted"],
#             mode="markers", marker=dict(color="#7c5cff", size=5, opacity=0.45),
#             name="Predictions",
#         ))
#         axis_min = float(min(sample["Predicted_Close"].min(), sample["Model_Predicted"].min()))
#         axis_max = float(max(sample["Predicted_Close"].max(), sample["Model_Predicted"].max()))
#         fig_scatter.add_trace(go.Scatter(
#             x=[axis_min, axis_max], y=[axis_min, axis_max],
#             mode="lines", line=dict(color="#f0b429", width=1.5, dash="dash"),
#             name="Perfect Prediction",
#         ))
#         fig_scatter.update_layout(
#             height=420, margin=dict(l=10, r=10, t=30, b=10),
#             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#             font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
#             xaxis_title="Actual Next-Day Close (₹)", yaxis_title="Model Predicted (₹)",
#             legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
#         )
#         fig_scatter.update_xaxes(gridcolor=THEME["CHART_GRID"])
#         fig_scatter.update_yaxes(gridcolor=THEME["CHART_GRID"])
#         st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

#         st.caption(
#             "Points closer to the dashed diagonal indicate predictions closer to the actual "
#             "next-day closing price. Metrics above are computed on the full historical dataset."
#         )


# # ====================================================
# # FOOTER
# # ====================================================

# st.divider()
# st.markdown(
#     '<div class="footer-note">TCS Stock Price Prediction using Machine Learning · Terminal UI · '
#     'Educational project — not financial advice</div>',
#     unsafe_allow_html=True
# )

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ====================================================
# PAGE CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="TCS | Stock Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================================
# SESSION STATE DEFAULTS
# ====================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ====================================================
# THEME DEFINITIONS
# ====================================================

THEMES = {
    "dark": dict(
        BG="#080a12", TEXT="#e9ecf6", TEXT_MUTED="#8892b0", TEXT_MUTED2="#7d87a3",
        BORDER="#1c2338", BORDER2="#232c48", CARD1="#131a2c", CARD2="#0d1120",
        HERO1="#0d1120", HERO2="#090b14", PREDICT1="#171f38", PREDICT2="#10142280",
        INPUT_BG="#131a2c", SIDEBAR1="#0b0e18", SIDEBAR2="#070911",
        SHINE="rgba(255,255,255,0.06)", GRID_OP="0.55", CHART_GRID="#1c2338",
        CHART_FONT="#c9cfe3", NAV_BG="#0d1120", NAV_ACTIVE="#171f38",
    ),
    "light": dict(
        BG="#f3f5fb", TEXT="#161a2c", TEXT_MUTED="#525a72", TEXT_MUTED2="#697088",
        BORDER="#dde1f0", BORDER2="#ccd2e8", CARD1="#ffffff", CARD2="#f4f6fc",
        HERO1="#ffffff", HERO2="#eef0fb", PREDICT1="#ffffff", PREDICT2="#f4f6fbdd",
        INPUT_BG="#ffffff", SIDEBAR1="#ffffff", SIDEBAR2="#eef0fb",
        SHINE="rgba(124,92,255,0.10)", GRID_OP="0.22", CHART_GRID="#dde1f0",
        CHART_FONT="#3a4160", NAV_BG="#ffffff", NAV_ACTIVE="#eef0fb",
    ),
}


def build_css(theme_name: str) -> str:
    v = THEMES[theme_name]

    css = """
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: __BG__; color: __TEXT__; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ================= HERO / PERSPECTIVE GRID ================= */

    .hero-wrap {
        position: relative;
        border-radius: 20px;
        padding: 34px 34px 26px 34px;
        margin-bottom: 20px;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 0%, rgba(124,92,255,0.22), transparent 55%),
            radial-gradient(circle at 90% 10%, rgba(240,180,41,0.10), transparent 45%),
            linear-gradient(180deg, __HERO1__ 0%, __HERO2__ 100%);
        border: 1px solid __BORDER__;
    }

    .grid-floor {
        position: absolute;
        left: 0; right: 0; bottom: -40px;
        height: 160px;
        background-image:
            linear-gradient(rgba(124,92,255,0.35) 1px, transparent 1px),
            linear-gradient(90deg, rgba(124,92,255,0.35) 1px, transparent 1px);
        background-size: 42px 28px;
        transform: perspective(280px) rotateX(62deg);
        transform-origin: bottom;
        mask-image: linear-gradient(to top, black 20%, transparent 90%);
        -webkit-mask-image: linear-gradient(to top, black 20%, transparent 90%);
        opacity: __GRID_OP__;
        pointer-events: none;
    }

    .ticker-badge {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white;
        font-weight: 700;
        font-size: 12.5px;
        padding: 5px 12px;
        border-radius: 6px;
        letter-spacing: 0.6px;
        box-shadow: 0 4px 14px rgba(124,92,255,0.4);
    }

    .ticker-row {
        position: relative; z-index: 2;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 16px; flex-wrap: wrap; gap: 10px;
    }

    .ticker-live {
        display: flex; align-items: center; gap: 6px;
        font-size: 12px; color: #2dd4bf; font-weight: 600;
        letter-spacing: 0.5px; font-family: 'JetBrains Mono', monospace;
    }

    .dot {
        height: 7px; width: 7px; background-color: #2dd4bf; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 8px #2dd4bf; animation: pulse 1.6s infinite;
    }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    .hero-title {
        position: relative; z-index: 2;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px; font-weight: 700; color: __TEXT__;
        letter-spacing: -0.5px; margin-bottom: 4px;
    }

    .hero-title span {
        background: linear-gradient(90deg, #7c5cff, #f0b429);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .hero-sub { position: relative; z-index: 2; color: __TEXT_MUTED__; font-size: 14px; max-width: 600px; }

    /* ================= TOP NAV STRIP ================= */

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: __TEXT_MUTED__;
        padding: 10px 16px;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #7c5cff !important;
        border-bottom: 2px solid #7c5cff !important;
    }

    div[data-testid="stTabs"] {
        border-bottom: 1px solid __BORDER__;
        margin-bottom: 18px;
    }

    /* ================= SECTION HEADERS ================= */

    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px; font-weight: 600; color: __TEXT__;
        margin-top: 6px; margin-bottom: 14px;
        display: flex; align-items: center; gap: 8px;
    }

    .section-header .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #7c5cff;
        background: rgba(124,92,255,0.12);
        border: 1px solid rgba(124,92,255,0.3);
        padding: 2px 8px; border-radius: 5px; letter-spacing: 0.5px;
    }

    .subtext { color: __TEXT_MUTED__; font-size: 13px; margin-top: -8px; margin-bottom: 14px; }

    /* ================= 3D TILT METRIC CARDS ================= */

    .tilt-card {
        background: linear-gradient(160deg, __CARD1__, __CARD2__);
        border: 1px solid __BORDER2__;
        border-radius: 14px; padding: 16px 18px; height: 100%;
        transform-style: preserve-3d; perspective: 800px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .tilt-card:hover {
        transform: perspective(800px) rotateX(4deg) rotateY(-4deg) translateY(-3px) scale(1.015);
        border-color: #7c5cff;
        box-shadow: 0 14px 34px rgba(124,92,255,0.22);
    }

    .metric-label {
        font-size: 12px; color: __TEXT_MUTED2__; text-transform: uppercase;
        letter-spacing: 0.8px; font-weight: 600; margin-bottom: 6px;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 700; color: __TEXT__;
    }

    .metric-sub { font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* ================= PREDICTION HOLO CARD ================= */

    .predict-card {
        position: relative;
        background: linear-gradient(150deg, __PREDICT1__ 0%, __PREDICT2__ 100%);
        border: 1px solid #33406a;
        border-radius: 20px; padding: 32px 34px; margin-top: 8px;
        transform-style: preserve-3d; perspective: 1000px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 10px 40px rgba(124,92,255,0.16);
        overflow: hidden;
    }

    .predict-card:hover {
        transform: perspective(1000px) rotateX(3deg) rotateY(-2deg) translateY(-4px);
        box-shadow: 0 20px 60px rgba(124,92,255,0.28);
    }

    .predict-card::before {
        content: ""; position: absolute; top: -60%; left: -20%;
        width: 60%; height: 220%;
        background: linear-gradient(120deg, transparent, __SHINE__, transparent);
        transform: rotate(20deg); pointer-events: none;
    }

    .predict-label {
        font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: __TEXT_MUTED2__;
        text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
    }

    .predict-price {
        font-family: 'JetBrains Mono', monospace; font-size: 46px; font-weight: 700; color: __TEXT__;
        margin: 8px 0 12px 0; text-shadow: 0 0 30px rgba(124,92,255,0.30);
    }

    .badge-up {
        background: rgba(45, 212, 191, 0.12); color: #2dd4bf;
        border: 1px solid rgba(45, 212, 191, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-down {
        background: rgba(255, 92, 92, 0.12); color: #ff5c5c;
        border: 1px solid rgba(255, 92, 92, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-flat {
        background: rgba(148, 163, 184, 0.12); color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.35);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    /* ================= SIGNAL BADGES (BUY/HOLD/SELL) ================= */

    .signal-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 20px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px;
        letter-spacing: 0.5px;
    }

    .signal-buy { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .signal-sell { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .signal-hold { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }

    .signal-note { font-size: 12px; color: __TEXT_MUTED2__; margin-top: 8px; font-style: italic; }

    /* ================= FIT DIAGNOSIS BADGES ================= */

    .fit-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 12px 22px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 17px;
        letter-spacing: 0.4px;
    }

    .fit-good { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .fit-overfit { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .fit-underfit { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }
    .fit-moderate { background: rgba(124,92,255,0.14); color: #9c8bff; border: 1px solid rgba(124,92,255,0.45); }

    .fit-note { font-size: 13px; color: __TEXT_MUTED__; margin-top: 10px; line-height: 1.6; max-width: 640px; }

    .fit-caveat {
        font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 14px;
        border-left: 2px solid __BORDER2__; padding-left: 10px; font-style: italic;
        max-width: 640px;
    }

    /* ================= BUTTONS ================= */

    div.stButton > button {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white; font-weight: 700; font-size: 15px;
        font-family: 'Space Grotesk', sans-serif; border: none; border-radius: 10px;
        padding: 12px 0; box-shadow: 0 4px 18px rgba(124,92,255,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 10px 28px rgba(124,92,255,0.5); color: white;
    }

    div.stDownloadButton > button {
        background: __CARD1__; color: __TEXT__; font-weight: 600;
        border: 1px solid __BORDER2__; border-radius: 10px;
    }

    /* ================= INPUTS ================= */

    div[data-baseweb="input"] { background-color: __INPUT_BG__ !important; border-radius: 8px !important; }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, __SIDEBAR1__, __SIDEBAR2__);
        border-right: 1px solid __BORDER__;
    }

    /* ================= MISC ================= */

    hr { border-color: __BORDER__ !important; }

    .stDataFrame { border: 1px solid __BORDER2__; border-radius: 10px; overflow: hidden; }

    .footer-note {
        text-align: center; color: __TEXT_MUTED2__; font-size: 12px;
        font-family: 'JetBrains Mono', monospace; padding: 10px 0 4px 0;
    }
    """

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ====================================================
# PAGE CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="TCS | Stock Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================================
# SESSION STATE DEFAULTS
# ====================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ====================================================
# THEME DEFINITIONS
# ====================================================

THEMES = {
    "dark": dict(
        BG="#080a12", TEXT="#e9ecf6", TEXT_MUTED="#8892b0", TEXT_MUTED2="#7d87a3",
        BORDER="#1c2338", BORDER2="#232c48", CARD1="#131a2c", CARD2="#0d1120",
        HERO1="#0d1120", HERO2="#090b14", PREDICT1="#171f38", PREDICT2="#10142280",
        INPUT_BG="#131a2c", SIDEBAR1="#0b0e18", SIDEBAR2="#070911",
        SHINE="rgba(255,255,255,0.06)", GRID_OP="0.55", CHART_GRID="#1c2338",
        CHART_FONT="#c9cfe3", NAV_BG="#0d1120", NAV_ACTIVE="#171f38",
    ),
    "light": dict(
        BG="#f3f5fb", TEXT="#161a2c", TEXT_MUTED="#525a72", TEXT_MUTED2="#697088",
        BORDER="#dde1f0", BORDER2="#ccd2e8", CARD1="#ffffff", CARD2="#f4f6fc",
        HERO1="#ffffff", HERO2="#eef0fb", PREDICT1="#ffffff", PREDICT2="#f4f6fbdd",
        INPUT_BG="#ffffff", SIDEBAR1="#ffffff", SIDEBAR2="#eef0fb",
        SHINE="rgba(124,92,255,0.10)", GRID_OP="0.22", CHART_GRID="#dde1f0",
        CHART_FONT="#3a4160", NAV_BG="#ffffff", NAV_ACTIVE="#eef0fb",
    ),
}


def build_css(theme_name: str) -> str:
    v = THEMES[theme_name]

    css = """
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: __BG__; color: __TEXT__; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ================= HERO / PERSPECTIVE GRID ================= */

    .hero-wrap {
        position: relative;
        border-radius: 20px;
        padding: 34px 34px 26px 34px;
        margin-bottom: 20px;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 0%, rgba(124,92,255,0.22), transparent 55%),
            radial-gradient(circle at 90% 10%, rgba(240,180,41,0.10), transparent 45%),
            linear-gradient(180deg, __HERO1__ 0%, __HERO2__ 100%);
        border: 1px solid __BORDER__;
    }

    .grid-floor {
        position: absolute;
        left: 0; right: 0; bottom: -40px;
        height: 160px;
        background-image:
            linear-gradient(rgba(124,92,255,0.35) 1px, transparent 1px),
            linear-gradient(90deg, rgba(124,92,255,0.35) 1px, transparent 1px);
        background-size: 42px 28px;
        transform: perspective(280px) rotateX(62deg);
        transform-origin: bottom;
        mask-image: linear-gradient(to top, black 20%, transparent 90%);
        -webkit-mask-image: linear-gradient(to top, black 20%, transparent 90%);
        opacity: __GRID_OP__;
        pointer-events: none;
    }

    .ticker-badge {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white;
        font-weight: 700;
        font-size: 12.5px;
        padding: 5px 12px;
        border-radius: 6px;
        letter-spacing: 0.6px;
        box-shadow: 0 4px 14px rgba(124,92,255,0.4);
    }

    .ticker-row {
        position: relative; z-index: 2;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 16px; flex-wrap: wrap; gap: 10px;
    }

    .ticker-live {
        display: flex; align-items: center; gap: 6px;
        font-size: 12px; color: #2dd4bf; font-weight: 600;
        letter-spacing: 0.5px; font-family: 'JetBrains Mono', monospace;
    }

    .dot {
        height: 7px; width: 7px; background-color: #2dd4bf; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 8px #2dd4bf; animation: pulse 1.6s infinite;
    }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    .hero-title {
        position: relative; z-index: 2;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px; font-weight: 700; color: __TEXT__;
        letter-spacing: -0.5px; margin-bottom: 4px;
    }

    .hero-title span {
        background: linear-gradient(90deg, #7c5cff, #f0b429);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .hero-sub { position: relative; z-index: 2; color: __TEXT_MUTED__; font-size: 14px; max-width: 600px; }

    /* ================= TOP NAV STRIP ================= */

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: __TEXT_MUTED__;
        padding: 10px 16px;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #7c5cff !important;
        border-bottom: 2px solid #7c5cff !important;
    }

    div[data-testid="stTabs"] {
        border-bottom: 1px solid __BORDER__;
        margin-bottom: 18px;
    }

    /* ================= SECTION HEADERS ================= */

    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px; font-weight: 600; color: __TEXT__;
        margin-top: 6px; margin-bottom: 14px;
        display: flex; align-items: center; gap: 8px;
    }

    .section-header .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #7c5cff;
        background: rgba(124,92,255,0.12);
        border: 1px solid rgba(124,92,255,0.3);
        padding: 2px 8px; border-radius: 5px; letter-spacing: 0.5px;
    }

    .subtext { color: __TEXT_MUTED__; font-size: 13px; margin-top: -8px; margin-bottom: 14px; }

    /* ================= 3D TILT METRIC CARDS ================= */

    .tilt-card {
        background: linear-gradient(160deg, __CARD1__, __CARD2__);
        border: 1px solid __BORDER2__;
        border-radius: 14px; padding: 16px 18px; height: 100%;
        transform-style: preserve-3d; perspective: 800px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .tilt-card:hover {
        transform: perspective(800px) rotateX(4deg) rotateY(-4deg) translateY(-3px) scale(1.015);
        border-color: #7c5cff;
        box-shadow: 0 14px 34px rgba(124,92,255,0.22);
    }

    .metric-label {
        font-size: 12px; color: __TEXT_MUTED2__; text-transform: uppercase;
        letter-spacing: 0.8px; font-weight: 600; margin-bottom: 6px;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 700; color: __TEXT__;
    }

    .metric-sub { font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* ================= PREDICTION HOLO CARD ================= */

    .predict-card {
        position: relative;
        background: linear-gradient(150deg, __PREDICT1__ 0%, __PREDICT2__ 100%);
        border: 1px solid #33406a;
        border-radius: 20px; padding: 32px 34px; margin-top: 8px;
        transform-style: preserve-3d; perspective: 1000px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 10px 40px rgba(124,92,255,0.16);
        overflow: hidden;
    }

    .predict-card:hover {
        transform: perspective(1000px) rotateX(3deg) rotateY(-2deg) translateY(-4px);
        box-shadow: 0 20px 60px rgba(124,92,255,0.28);
    }

    .predict-card::before {
        content: ""; position: absolute; top: -60%; left: -20%;
        width: 60%; height: 220%;
        background: linear-gradient(120deg, transparent, __SHINE__, transparent);
        transform: rotate(20deg); pointer-events: none;
    }

    .predict-label {
        font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: __TEXT_MUTED2__;
        text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
    }

    .predict-price {
        font-family: 'JetBrains Mono', monospace; font-size: 46px; font-weight: 700; color: __TEXT__;
        margin: 8px 0 12px 0; text-shadow: 0 0 30px rgba(124,92,255,0.30);
    }

    .badge-up {
        background: rgba(45, 212, 191, 0.12); color: #2dd4bf;
        border: 1px solid rgba(45, 212, 191, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-down {
        background: rgba(255, 92, 92, 0.12); color: #ff5c5c;
        border: 1px solid rgba(255, 92, 92, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-flat {
        background: rgba(148, 163, 184, 0.12); color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.35);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    /* ================= SIGNAL BADGES (BUY/HOLD/SELL) ================= */

    .signal-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 20px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px;
        letter-spacing: 0.5px;
    }

    .signal-buy { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .signal-sell { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .signal-hold { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }

    .signal-note { font-size: 12px; color: __TEXT_MUTED2__; margin-top: 8px; font-style: italic; }

    /* ================= FIT DIAGNOSIS BADGES ================= */

    .fit-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 12px 22px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 17px;
        letter-spacing: 0.4px;
    }

    .fit-good { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .fit-overfit { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .fit-underfit { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }
    .fit-moderate { background: rgba(124,92,255,0.14); color: #9c8bff; border: 1px solid rgba(124,92,255,0.45); }

    .fit-note { font-size: 13px; color: __TEXT_MUTED__; margin-top: 10px; line-height: 1.6; max-width: 640px; }

    .fit-caveat {
        font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 14px;
        border-left: 2px solid __BORDER2__; padding-left: 10px; font-style: italic;
        max-width: 640px;
    }

    /* ================= BUTTONS ================= */

    div.stButton > button {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white; font-weight: 700; font-size: 15px;
        font-family: 'Space Grotesk', sans-serif; border: none; border-radius: 10px;
        padding: 12px 0; box-shadow: 0 4px 18px rgba(124,92,255,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 10px 28px rgba(124,92,255,0.5); color: white;
    }

    div.stDownloadButton > button {
        background: __CARD1__; color: __TEXT__; font-weight: 600;
        border: 1px solid __BORDER2__; border-radius: 10px;
    }

    /* ================= INPUTS ================= */

    div[data-baseweb="input"] { background-color: __INPUT_BG__ !important; border-radius: 8px !important; }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, __SIDEBAR1__, __SIDEBAR2__);
        border-right: 1px solid __BORDER__;
    }

    /* ================= MISC ================= */

    hr { border-color: __BORDER__ !important; }

    .stDataFrame { border: 1px solid __BORDER2__; border-radius: 10px; overflow: hidden; }

    .footer-note {
        text-align: center; color: __TEXT_MUTED2__; font-size: 12px;
        font-family: 'JetBrains Mono', monospace; padding: 10px 0 4px 0;
    }
    """

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ====================================================
# PAGE CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="TCS | Stock Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================================
# SESSION STATE DEFAULTS
# ====================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ====================================================
# THEME DEFINITIONS
# ====================================================

THEMES = {
    "dark": dict(
        BG="#080a12", TEXT="#e9ecf6", TEXT_MUTED="#8892b0", TEXT_MUTED2="#7d87a3",
        BORDER="#1c2338", BORDER2="#232c48", CARD1="#131a2c", CARD2="#0d1120",
        HERO1="#0d1120", HERO2="#090b14", PREDICT1="#171f38", PREDICT2="#10142280",
        INPUT_BG="#131a2c", SIDEBAR1="#0b0e18", SIDEBAR2="#070911",
        SHINE="rgba(255,255,255,0.06)", GRID_OP="0.55", CHART_GRID="#1c2338",
        CHART_FONT="#c9cfe3", NAV_BG="#0d1120", NAV_ACTIVE="#171f38",
    ),
    "light": dict(
        BG="#f3f5fb", TEXT="#161a2c", TEXT_MUTED="#525a72", TEXT_MUTED2="#697088",
        BORDER="#dde1f0", BORDER2="#ccd2e8", CARD1="#ffffff", CARD2="#f4f6fc",
        HERO1="#ffffff", HERO2="#eef0fb", PREDICT1="#ffffff", PREDICT2="#f4f6fbdd",
        INPUT_BG="#ffffff", SIDEBAR1="#ffffff", SIDEBAR2="#eef0fb",
        SHINE="rgba(124,92,255,0.10)", GRID_OP="0.22", CHART_GRID="#dde1f0",
        CHART_FONT="#3a4160", NAV_BG="#ffffff", NAV_ACTIVE="#eef0fb",
    ),
}


def build_css(theme_name: str) -> str:
    v = THEMES[theme_name]

    css = """
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: __BG__; color: __TEXT__; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ================= HERO / PERSPECTIVE GRID ================= */

    .hero-wrap {
        position: relative;
        border-radius: 20px;
        padding: 34px 34px 26px 34px;
        margin-bottom: 20px;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 0%, rgba(124,92,255,0.22), transparent 55%),
            radial-gradient(circle at 90% 10%, rgba(240,180,41,0.10), transparent 45%),
            linear-gradient(180deg, __HERO1__ 0%, __HERO2__ 100%);
        border: 1px solid __BORDER__;
    }

    .grid-floor {
        position: absolute;
        left: 0; right: 0; bottom: -40px;
        height: 160px;
        background-image:
            linear-gradient(rgba(124,92,255,0.35) 1px, transparent 1px),
            linear-gradient(90deg, rgba(124,92,255,0.35) 1px, transparent 1px);
        background-size: 42px 28px;
        transform: perspective(280px) rotateX(62deg);
        transform-origin: bottom;
        mask-image: linear-gradient(to top, black 20%, transparent 90%);
        -webkit-mask-image: linear-gradient(to top, black 20%, transparent 90%);
        opacity: __GRID_OP__;
        pointer-events: none;
    }

    .ticker-badge {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white;
        font-weight: 700;
        font-size: 12.5px;
        padding: 5px 12px;
        border-radius: 6px;
        letter-spacing: 0.6px;
        box-shadow: 0 4px 14px rgba(124,92,255,0.4);
    }

    .ticker-row {
        position: relative; z-index: 2;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 16px; flex-wrap: wrap; gap: 10px;
    }

    .ticker-live {
        display: flex; align-items: center; gap: 6px;
        font-size: 12px; color: #2dd4bf; font-weight: 600;
        letter-spacing: 0.5px; font-family: 'JetBrains Mono', monospace;
    }

    .dot {
        height: 7px; width: 7px; background-color: #2dd4bf; border-radius: 50%;
        display: inline-block; box-shadow: 0 0 8px #2dd4bf; animation: pulse 1.6s infinite;
    }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    .hero-title {
        position: relative; z-index: 2;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 36px; font-weight: 700; color: __TEXT__;
        letter-spacing: -0.5px; margin-bottom: 4px;
    }

    .hero-title span {
        background: linear-gradient(90deg, #7c5cff, #f0b429);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .hero-sub { position: relative; z-index: 2; color: __TEXT_MUTED__; font-size: 14px; max-width: 600px; }

    /* ================= TOP NAV STRIP ================= */

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: __TEXT_MUTED__;
        padding: 10px 16px;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #7c5cff !important;
        border-bottom: 2px solid #7c5cff !important;
    }

    div[data-testid="stTabs"] {
        border-bottom: 1px solid __BORDER__;
        margin-bottom: 18px;
    }

    /* ================= SECTION HEADERS ================= */

    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px; font-weight: 600; color: __TEXT__;
        margin-top: 6px; margin-bottom: 14px;
        display: flex; align-items: center; gap: 8px;
    }

    .section-header .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #7c5cff;
        background: rgba(124,92,255,0.12);
        border: 1px solid rgba(124,92,255,0.3);
        padding: 2px 8px; border-radius: 5px; letter-spacing: 0.5px;
    }

    .subtext { color: __TEXT_MUTED__; font-size: 13px; margin-top: -8px; margin-bottom: 14px; }

    /* ================= 3D TILT METRIC CARDS ================= */

    .tilt-card {
        background: linear-gradient(160deg, __CARD1__, __CARD2__);
        border: 1px solid __BORDER2__;
        border-radius: 14px; padding: 16px 18px; height: 100%;
        transform-style: preserve-3d; perspective: 800px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .tilt-card:hover {
        transform: perspective(800px) rotateX(4deg) rotateY(-4deg) translateY(-3px) scale(1.015);
        border-color: #7c5cff;
        box-shadow: 0 14px 34px rgba(124,92,255,0.22);
    }

    .metric-label {
        font-size: 12px; color: __TEXT_MUTED2__; text-transform: uppercase;
        letter-spacing: 0.8px; font-weight: 600; margin-bottom: 6px;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace; font-size: 21px; font-weight: 700; color: __TEXT__;
    }

    .metric-sub { font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* ================= PREDICTION HOLO CARD ================= */

    .predict-card {
        position: relative;
        background: linear-gradient(150deg, __PREDICT1__ 0%, __PREDICT2__ 100%);
        border: 1px solid #33406a;
        border-radius: 20px; padding: 32px 34px; margin-top: 8px;
        transform-style: preserve-3d; perspective: 1000px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 10px 40px rgba(124,92,255,0.16);
        overflow: hidden;
    }

    .predict-card:hover {
        transform: perspective(1000px) rotateX(3deg) rotateY(-2deg) translateY(-4px);
        box-shadow: 0 20px 60px rgba(124,92,255,0.28);
    }

    .predict-card::before {
        content: ""; position: absolute; top: -60%; left: -20%;
        width: 60%; height: 220%;
        background: linear-gradient(120deg, transparent, __SHINE__, transparent);
        transform: rotate(20deg); pointer-events: none;
    }

    .predict-label {
        font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: __TEXT_MUTED2__;
        text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
    }

    .predict-price {
        font-family: 'JetBrains Mono', monospace; font-size: 46px; font-weight: 700; color: __TEXT__;
        margin: 8px 0 12px 0; text-shadow: 0 0 30px rgba(124,92,255,0.30);
    }

    .badge-up {
        background: rgba(45, 212, 191, 0.12); color: #2dd4bf;
        border: 1px solid rgba(45, 212, 191, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-down {
        background: rgba(255, 92, 92, 0.12); color: #ff5c5c;
        border: 1px solid rgba(255, 92, 92, 0.4);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    .badge-flat {
        background: rgba(148, 163, 184, 0.12); color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.35);
        padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 14px;
        font-family: 'JetBrains Mono', monospace; display: inline-block;
    }

    /* ================= SIGNAL BADGES (BUY/HOLD/SELL) ================= */

    .signal-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 20px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px;
        letter-spacing: 0.5px;
    }

    .signal-buy { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .signal-sell { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .signal-hold { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }

    .signal-note { font-size: 12px; color: __TEXT_MUTED2__; margin-top: 8px; font-style: italic; }

    /* ================= FIT DIAGNOSIS BADGES ================= */

    .fit-chip {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 12px 22px; border-radius: 12px;
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 17px;
        letter-spacing: 0.4px;
    }

    .fit-good { background: rgba(45,212,191,0.14); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.45); }
    .fit-overfit { background: rgba(255,92,92,0.14); color: #ff5c5c; border: 1px solid rgba(255,92,92,0.45); }
    .fit-underfit { background: rgba(240,180,41,0.14); color: #f0b429; border: 1px solid rgba(240,180,41,0.45); }
    .fit-moderate { background: rgba(124,92,255,0.14); color: #9c8bff; border: 1px solid rgba(124,92,255,0.45); }

    .fit-note { font-size: 13px; color: __TEXT_MUTED__; margin-top: 10px; line-height: 1.6; max-width: 640px; }

    .fit-caveat {
        font-size: 11.5px; color: __TEXT_MUTED2__; margin-top: 14px;
        border-left: 2px solid __BORDER2__; padding-left: 10px; font-style: italic;
        max-width: 640px;
    }

    /* ================= BUTTONS ================= */

    div.stButton > button {
        background: linear-gradient(135deg, #7c5cff, #4c2fd4);
        color: white; font-weight: 700; font-size: 15px;
        font-family: 'Space Grotesk', sans-serif; border: none; border-radius: 10px;
        padding: 12px 0; box-shadow: 0 4px 18px rgba(124,92,255,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 10px 28px rgba(124,92,255,0.5); color: white;
    }

    div.stDownloadButton > button {
        background: __CARD1__; color: __TEXT__; font-weight: 600;
        border: 1px solid __BORDER2__; border-radius: 10px;
    }

    /* ================= INPUTS ================= */

    div[data-baseweb="input"] { background-color: __INPUT_BG__ !important; border-radius: 8px !important; }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, __SIDEBAR1__, __SIDEBAR2__);
        border-right: 1px solid __BORDER__;
    }

    /* ================= MISC ================= */

    hr { border-color: __BORDER__ !important; }

    .stDataFrame { border: 1px solid __BORDER2__; border-radius: 10px; overflow: hidden; }

    .footer-note {
        text-align: center; color: __TEXT_MUTED2__; font-size: 12px;
        font-family: 'JetBrains Mono', monospace; padding: 10px 0 4px 0;
    }
    """

    for key, val in v.items():
        css = css.replace(f"__{key}__", val)

    return f"<style>{css}</style>"


st.markdown(build_css(st.session_state.theme), unsafe_allow_html=True)
THEME = THEMES[st.session_state.theme]


# ====================================================
# LOAD MODEL AND DATA  (unchanged pipeline / artifacts)
# ====================================================

MODEL_PATH = "TCS_stock_model.pkl"
SCALER_PATH = "TCS_scaler.pkl"
DATA_PATH = "TCS_stock_cleaned.csv"


@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_scaler():
    return joblib.load(SCALER_PATH)


@st.cache_data(show_spinner=False)
def load_data():
    return pd.read_csv(DATA_PATH)


with st.spinner("Booting stock terminal · loading model and market data..."):
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(
                f"Scaler file not found: {SCALER_PATH}. This model was trained on "
                f"StandardScaler-scaled features, so the scaler is required to make "
                f"correct predictions — re-run the training notebook to generate it."
            )
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

        model = load_model()
        scaler = load_scaler()
        df = load_data()

        if df.empty:
            raise ValueError("Loaded dataset is empty.")

        required_cols = {"Open", "High", "Low", "Close"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise ValueError(f"Dataset is missing required column(s): {', '.join(sorted(missing_cols))}")

    except Exception as e:
        st.error(f"⚠️ Failed to initialize the terminal: {e}")
        st.stop()

has_predicted_col = "Predicted_Close" in df.columns
has_date_col = "Date" in df.columns
has_volume = "Volume" in df.columns


# ====================================================
# BACKTEST: MODEL PREDICTIONS vs ACTUAL (real data only)
# Computed early so both the sidebar and the Model Performance tab can use it.
# ====================================================

@st.cache_data(show_spinner=False)
def compute_backtest(_model, _scaler, data: pd.DataFrame):
    """
    Runs the SAME prediction call used for live forecasting (scaled inputs,
    matching how the model was trained) across the historical dataset, and
    compares it against the real 'Predicted_Close' ground-truth column
    already present in the cleaned dataset. No values are invented — this
    is the model's actual output on real past rows.
    """
    if "Predicted_Close" not in data.columns:
        return None

    working = data.copy()
    if "Date" in working.columns:
        working["Date"] = pd.to_datetime(working["Date"])
        working = working.sort_values("Date").reset_index(drop=True)

    working = working.dropna(subset=["Open", "High", "Low", "Close", "Predicted_Close"])
    if working.empty:
        return None

    X_hist = working[["Open", "High", "Low", "Close"]].values
    X_hist_scaled = _scaler.transform(X_hist)
    y_model = _model.predict(X_hist_scaled)

    result = working.copy()
    result["Model_Predicted"] = y_model
    result["Error"] = result["Model_Predicted"] - result["Predicted_Close"]
    return result


with st.spinner("Running historical backtest..."):
    backtest_df = compute_backtest(model, scaler, df)

if backtest_df is not None and len(backtest_df) > 0:
    err = backtest_df["Error"].values
    actual = backtest_df["Predicted_Close"].values
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err ** 2)))
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((actual - np.mean(actual)) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else float("nan")
    nonzero = actual != 0
    mape = float(np.mean(np.abs(err[nonzero] / actual[nonzero]))) * 100 if nonzero.any() else float("nan")
else:
    mae = rmse = r2 = mape = None


# ====================================================
# FIT DIAGNOSIS: chronological split-based overfit/underfit check
# ====================================================

@st.cache_data(show_spinner=False)
def compute_fit_diagnosis(_bt_df: pd.DataFrame, split_ratio: float = 0.8):
    """
    Since the model is loaded pre-trained (no access to the original
    train/test split), this approximates a fit diagnosis by chronologically
    splitting the historical backtest into an earlier segment ("reference")
    and a later, more recent segment ("holdout") — then comparing how well
    the model's predictions track actual prices in each.

    Logic:
      - Both segments weak (low R²)              -> underfit
      - Reference much stronger than holdout      -> overfit
      - Both segments strong and close together   -> good fit
      - Anything else                             -> moderate / inconclusive
    """
    if _bt_df is None or len(_bt_df) < 30:
        return None

    n = len(_bt_df)
    split_idx = int(n * split_ratio)
    ref_seg = _bt_df.iloc[:split_idx]
    holdout_seg = _bt_df.iloc[split_idx:]

    def seg_metrics(seg: pd.DataFrame) -> dict:
        e = seg["Error"].values
        a = seg["Predicted_Close"].values
        mae_ = float(np.mean(np.abs(e)))
        rmse_ = float(np.sqrt(np.mean(e ** 2)))
        ss_res_ = float(np.sum(e ** 2))
        ss_tot_ = float(np.sum((a - np.mean(a)) ** 2))
        r2_ = 1 - ss_res_ / ss_tot_ if ss_tot_ != 0 else float("nan")
        nz = a != 0
        mape_ = float(np.mean(np.abs(e[nz] / a[nz]))) * 100 if nz.any() else float("nan")
        return dict(mae=mae_, rmse=rmse_, r2=r2_, mape=mape_, n=len(seg))

    ref_m = seg_metrics(ref_seg)
    hold_m = seg_metrics(holdout_seg)

    r2_gap = ref_m["r2"] - hold_m["r2"]
    rmse_ratio = hold_m["rmse"] / ref_m["rmse"] if ref_m["rmse"] > 0 else float("nan")

    # MAPE ratio is scale-invariant (%), unlike RMSE ratio which is in raw ₹
    # and gets inflated purely because TCS's price level rose over time —
    # a ₹40 miss on a ₹4000 stock is a smaller relative error than a ₹20
    # miss on a ₹500 stock, even though the raw rupee RMSE looks "worse".
    # MAPE is the fairer signal for comparing fit quality across segments
    # that sit at different price levels.
    mape_ratio = hold_m["mape"] / ref_m["mape"] if ref_m["mape"] > 0 else float("nan")

    if ref_m["r2"] < 0.5 and hold_m["r2"] < 0.5:
        verdict = "underfit"
    elif r2_gap > 0.15 or (not np.isnan(mape_ratio) and mape_ratio > 1.5):
        verdict = "overfit"
    elif ref_m["r2"] >= 0.7 and hold_m["r2"] >= 0.6 and r2_gap <= 0.15 and (np.isnan(mape_ratio) or mape_ratio <= 1.5):
        verdict = "good_fit"
    else:
        verdict = "moderate"

    return dict(
        reference=ref_m, holdout=hold_m, verdict=verdict,
        r2_gap=r2_gap, rmse_ratio=rmse_ratio, mape_ratio=mape_ratio,
        reference_seg=ref_seg, holdout_seg=holdout_seg, split_idx=split_idx,
    )


fit_diag = compute_fit_diagnosis(backtest_df) if backtest_df is not None else None


# ====================================================
# HERO / TICKER HEADER
# ====================================================

st.markdown(f"""
<div class="hero-wrap">
    <div class="grid-floor"></div>
    <div class="ticker-row">
        <div style="display:flex; align-items:center; gap:10px;">
            <span class="ticker-badge">TCS · NSE</span>
        </div>
        <div class="ticker-live">
            <span class="dot"></span> LIVE MODEL &nbsp;·&nbsp; {datetime.now().strftime("%d %b %Y, %I:%M %p")}
        </div>
    </div>
    <div class="hero-title">Tata Consultancy Services <span>Price Forecast</span></div>
    <div class="hero-sub">
        A machine-learning terminal that reads today's Open, High, Low and Close
        to project TCS's next closing price — with a live candlestick view of the
        trend behind it and a transparent look at how the model has performed historically.
    </div>
</div>
""", unsafe_allow_html=True)


# ====================================================
# SIDEBAR
# ====================================================

with st.sidebar:
    st.markdown("### 📊 Stock Terminal")
    st.caption("AI-powered TCS price forecasting")
    st.divider()

    st.markdown("**Appearance**")
    theme_choice = st.radio(
        "Theme", options=["Dark", "Light"],
        index=0 if st.session_state.theme == "dark" else 1,
        horizontal=True, label_visibility="collapsed",
    )
    new_theme = "dark" if theme_choice == "Dark" else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.divider()
    st.markdown("**About this tool**")
    st.write(
        "This terminal uses a trained machine learning model to forecast "
        "TCS's next closing price based on Open, High, Low and Close values."
    )
    st.divider()
    st.markdown("**Dataset**")
    st.write(f"📅 {len(df):,} trading days loaded")
    if has_date_col:
        try:
            d_min = pd.to_datetime(df["Date"]).min().strftime("%d %b %Y")
            d_max = pd.to_datetime(df["Date"]).max().strftime("%d %b %Y")
            st.write(f"🗓️ {d_min} → {d_max}")
        except Exception:
            pass
    st.write(f"🧠 Model: `{type(model).__name__}`")
    st.write(f"⚙️ Preprocessing: `{type(scaler).__name__}` (fit during training)")
    if mae is not None:
        st.write(f"🎯 Backtest R²: `{r2:.4f}`  ·  MAE: `₹{mae:.2f}`")
    if fit_diag is not None:
        verdict_labels = {
            "good_fit": "🟢 Good Fit", "overfit": "🔴 Overfitting Risk",
            "underfit": "🟡 Underfitting", "moderate": "🟣 Moderate Fit",
        }
        st.write(f"🩺 Fit check: `{verdict_labels.get(fit_diag['verdict'], 'N/A')}`")
    st.divider()
    st.caption("⚠️ For educational purposes only. Not financial advice.")


# ====================================================
# LATEST DATA
# ====================================================

latest_row = df.iloc[-1]
latest_open = float(latest_row["Open"])
latest_high = float(latest_row["High"])
latest_low = float(latest_row["Low"])
latest_close = float(latest_row["Close"])


# ====================================================
# CHART DATA PREP (cached — computed once, reused across tabs)
# ====================================================

@st.cache_data(show_spinner=False)
def prepare_chart_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    One-time computation of everything the charts need: sorted dates,
    moving averages, and daily change direction for volume colouring.
    """
    data = raw_df.copy()
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.sort_values("Date").reset_index(drop=True)
    else:
        data = data.reset_index(drop=True)

    data["SMA20"] = data["Close"].rolling(window=20, min_periods=1).mean()
    data["SMA50"] = data["Close"].rolling(window=50, min_periods=1).mean()
    data["EMA9"] = data["Close"].ewm(span=9, adjust=False).mean()

    data["Change"] = data["Close"].diff()
    data["Direction"] = np.where(data["Change"] >= 0, "up", "down")

    return data


full_chart_data = prepare_chart_data(df)


# ====================================================
# TOP NAVIGATION (TABS)
# ====================================================

tab_overview, tab_predict, tab_charts, tab_history, tab_model, tab_fit = st.tabs(
    ["📊  Overview", "🔮  Predict", "📈  Charts", "🕒  History", "🎯  Model Performance", "🩺  Fit Check"]
)


# ----------------------------------------------------
# TAB 1 — OVERVIEW
# ----------------------------------------------------

with tab_overview:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">SNAPSHOT</span> Latest Market Data</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)
    metric_cols = [
        (col1, "Open", latest_open),
        (col2, "High", latest_high),
        (col3, "Low", latest_low),
        (col4, "Close", latest_close),
    ]
    for col, label, value in metric_cols:
        with col:
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">₹{value:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-header"><span class="eyebrow">STATS</span> Dataset-Wide Highlights</div>',
        unsafe_allow_html=True
    )

    all_time_high = float(df["Close"].max())
    all_time_low = float(df["Close"].min())

    window_30 = full_chart_data.tail(30)
    trend_30 = float(window_30["Close"].iloc[-1] - window_30["Close"].iloc[0]) if len(window_30) > 1 else 0.0
    trend_30_pct = (trend_30 / window_30["Close"].iloc[0]) * 100 if len(window_30) > 1 and window_30["Close"].iloc[0] != 0 else 0.0

    scol1, scol2, scol3, scol4 = st.columns(4)
    with scol1:
        st.markdown(f"""
        <div class="tilt-card">
            <div class="metric-label">All-Time High</div>
            <div class="metric-value">₹{all_time_high:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with scol2:
        st.markdown(f"""
        <div class="tilt-card">
            <div class="metric-label">All-Time Low</div>
            <div class="metric-value">₹{all_time_low:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with scol3:
        trend_color = "#2dd4bf" if trend_30 >= 0 else "#ff5c5c"
        arrow = "▲" if trend_30 >= 0 else "▼"
        st.markdown(f"""
        <div class="tilt-card">
            <div class="metric-label">30-Day Trend</div>
            <div class="metric-value" style="color:{trend_color};">{arrow} {trend_30_pct:+.2f}%</div>
        </div>""", unsafe_allow_html=True)
    with scol4:
        if has_volume:
            avg_vol = float(df["Volume"].tail(30).mean())
            vol_display = f"{avg_vol:,.0f}"
        else:
            vol_display = "N/A"
        st.markdown(f"""
        <div class="tilt-card">
            <div class="metric-label">Avg Volume (30d)</div>
            <div class="metric-value">{vol_display}</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-header"><span class="eyebrow">GLANCE</span> Recent Price Action (90 Days)</div>',
        unsafe_allow_html=True
    )

    glance_data = full_chart_data.tail(90)
    x_axis = glance_data["Date"] if has_date_col else glance_data.index

    fig_glance = go.Figure()
    fig_glance.add_trace(go.Scatter(
        x=x_axis, y=glance_data["Close"], mode="lines",
        line=dict(color="#7c5cff", width=2),
        fill="tozeroy", fillcolor="rgba(124,92,255,0.12)",
        name="Close", showlegend=False,
    ))
    fig_glance.update_layout(
        height=220, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=10),
        hovermode="x unified",
    )
    fig_glance.update_xaxes(gridcolor=THEME["CHART_GRID"], showticklabels=True)
    fig_glance.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="₹")
    st.plotly_chart(fig_glance, use_container_width=True, config={"displayModeBar": False})


# ----------------------------------------------------
# TAB 2 — PREDICT
# ----------------------------------------------------

with tab_predict:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">INPUT</span> Enter Stock Values</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtext">Defaults are pre-filled with the most recent trading day. Adjust any value to test a different scenario.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        open_price = st.number_input("Open Price (₹)", min_value=0.0, value=latest_open, step=0.10)
        high_price = st.number_input("High Price (₹)", min_value=0.0, value=latest_high, step=0.10)

    with col2:
        low_price = st.number_input("Low Price (₹)", min_value=0.0, value=latest_low, step=0.10)
        close_price = st.number_input("Close Price (₹)", min_value=0.0, value=latest_close, step=0.10)

    st.write("")

    predict_button = st.button(
        "🔮  Predict Tomorrow's Closing Price", type="primary", use_container_width=True
    )

    if predict_button:
        try:
            with st.spinner("Running model inference..."):

                # ---- PREDICTION LOGIC (matches training pipeline) ----
                # Model expects: Open, High, Low, Close — scaled with the
                # SAME StandardScaler fitted during training (TCS_scaler.pkl).
                # Feeding raw ₹-scale values directly into the model (as the
                # very first version of this app did) produces wildly wrong
                # predictions, since the model's coefficients were learned
                # on standardized (mean 0, std 1) inputs, not raw prices.
                input_data = np.array([[open_price, high_price, low_price, close_price]])
                input_scaled = scaler.transform(input_data)
                prediction = model.predict(input_scaled)
                predicted_price = float(prediction[0])
                # -------------------------------------------------------

                difference = predicted_price - close_price
                percentage = (difference / close_price) * 100 if close_price != 0 else 0.0

            if predicted_price > close_price:
                badge_html = f'<span class="badge-up">▲ +₹{difference:.2f} ({percentage:.2f}%)</span>'
                trend_msg = "📈 The model predicts tomorrow's closing price may be **higher** than today's close."
            elif predicted_price < close_price:
                badge_html = f'<span class="badge-down">▼ ₹{difference:.2f} ({percentage:.2f}%)</span>'
                trend_msg = "📉 The model predicts tomorrow's closing price may be **lower** than today's close."
            else:
                badge_html = '<span class="badge-flat">● No change</span>'
                trend_msg = "➡️ The model predicts approximately the **same** closing price."

            st.write("")
            st.markdown(f"""
            <div class="predict-card">
                <div class="predict-label">Predicted Closing Price · Tomorrow</div>
                <div class="predict-price">₹{predicted_price:.2f}</div>
                {badge_html}
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            colA, colB = st.columns(2)
            with colA:
                st.markdown(f"""
                <div class="tilt-card">
                    <div class="metric-label">Current Closing Price</div>
                    <div class="metric-value">₹{close_price:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            with colB:
                color = "#2dd4bf" if difference > 0 else ("#ff5c5c" if difference < 0 else "#94a3b8")
                st.markdown(f"""
                <div class="tilt-card">
                    <div class="metric-label">Expected Change</div>
                    <div class="metric-value" style="color:{color};">₹{difference:.2f} ({percentage:.2f}%)</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # ---- Signal derived directly from the model's own % change ----
            buy_th, sell_th = 0.5, -0.5
            if percentage > buy_th:
                signal_html = '<div class="signal-chip signal-buy">🟢 BUY SIGNAL</div>'
            elif percentage < sell_th:
                signal_html = '<div class="signal-chip signal-sell">🔴 SELL SIGNAL</div>'
            else:
                signal_html = '<div class="signal-chip signal-hold">🟡 HOLD SIGNAL</div>'

            st.markdown(
                f"""{signal_html}
                <div class="signal-note">
                    Heuristic signal derived from the model's predicted % change
                    (Buy if &gt; {buy_th}%, Sell if &lt; {sell_th}%, otherwise Hold).
                    This is not financial advice.
                </div>""",
                unsafe_allow_html=True
            )

            st.write("")

            if predicted_price > close_price:
                st.info(trend_msg)
            elif predicted_price < close_price:
                st.warning(trend_msg)
            else:
                st.info(trend_msg)

            if mae is not None:
                st.caption(
                    f"ℹ️ On historical backtesting, this model's next-day predictions have an average "
                    f"error of ± ₹{mae:.2f} (MAE). See the **Model Performance** tab for full accuracy details."
                )

        except Exception as e:
            st.error(f"Prediction error: {e}")


# ----------------------------------------------------
# TAB 3 — CHARTS
# ----------------------------------------------------

with tab_charts:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">CHART</span> TCS Price Action</div>',
        unsafe_allow_html=True
    )

    range_options = {
        "1M": 21, "3M": 63, "6M": 126, "1Y": 252, "3Y": 756, "All": len(full_chart_data),
    }

    ctrl_col1, ctrl_col2 = st.columns([3, 1])
    with ctrl_col1:
        selected_range = st.radio(
            "Range", options=list(range_options.keys()), index=2,
            horizontal=True, label_visibility="collapsed",
        )
    with ctrl_col2:
        chart_type = st.selectbox("Chart type", options=["Candlestick", "Line"], label_visibility="collapsed")

    lookback = range_options[selected_range]
    plot_data = full_chart_data.tail(lookback).copy()
    x_axis = plot_data["Date"] if has_date_col else plot_data.index

    row_heights = [0.72, 0.28] if has_volume else [1.0]
    rows = 2 if has_volume else 1

    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=row_heights)

    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=x_axis, open=plot_data["Open"], high=plot_data["High"],
            low=plot_data["Low"], close=plot_data["Close"],
            increasing_line_color="#2dd4bf", decreasing_line_color="#ff5c5c",
            increasing_fillcolor="rgba(45,212,191,0.7)", decreasing_fillcolor="rgba(255,92,92,0.7)",
            name="TCS", showlegend=False,
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=x_axis, y=plot_data["Close"], mode="lines",
            line=dict(color=THEME["CHART_FONT"], width=1.8),
            fill="tozeroy", fillcolor="rgba(124,92,255,0.08)",
            name="Close", showlegend=False,
        ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=x_axis, y=plot_data["EMA9"], mode="lines",
        line=dict(color="#f0b429", width=1.3), name="EMA 9",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=x_axis, y=plot_data["SMA20"], mode="lines",
        line=dict(color="#7c5cff", width=1.3), name="SMA 20",
    ), row=1, col=1)

    if lookback > 60:
        fig.add_trace(go.Scatter(
            x=x_axis, y=plot_data["SMA50"], mode="lines",
            line=dict(color="#4c9aff", width=1.1, dash="dot"), name="SMA 50",
        ), row=1, col=1)

    if has_volume:
        vol_colors = np.where(plot_data["Direction"] == "up", "rgba(45,212,191,0.55)", "rgba(255,92,92,0.55)")
        fig.add_trace(go.Bar(
            x=x_axis, y=plot_data["Volume"], marker_color=vol_colors, name="Volume", showlegend=False,
        ), row=2, col=1)

    fig.update_layout(
        height=560 if has_volume else 460,
        margin=dict(l=10, r=10, t=36, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
        hovermode="x unified", dragmode="pan",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
    )

    fig.update_xaxes(
        gridcolor=THEME["CHART_GRID"], showspikes=True, spikemode="across",
        spikecolor="#7c5cff", spikethickness=1, rangeslider_visible=False, row=rows, col=1,
    )
    if has_volume:
        fig.update_xaxes(showticklabels=False, row=1, col=1)

    fig.update_yaxes(
        gridcolor=THEME["CHART_GRID"], side="right", title="Price (₹)",
        showspikes=True, spikecolor="#7c5cff", spikethickness=1, row=1, col=1,
    )
    if has_volume:
        fig.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="Vol", row=2, col=1)

    st.plotly_chart(
        fig, use_container_width=True,
        config={
            "displayModeBar": True, "displaylogo": False, "scrollZoom": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
        },
    )

    last_point = plot_data.iloc[-1]
    period_change = last_point["Close"] - plot_data.iloc[0]["Close"]
    period_pct = (period_change / plot_data.iloc[0]["Close"]) * 100 if plot_data.iloc[0]["Close"] != 0 else 0.0
    trend_color = "#2dd4bf" if period_change >= 0 else "#ff5c5c"
    trend_arrow = "▲" if period_change >= 0 else "▼"

    st.markdown(
        f"""<span style="font-family:'JetBrains Mono',monospace; font-size:12.5px; color:{trend_color};">
        {trend_arrow} {period_change:+.2f} ({period_pct:+.2f}%) over {selected_range}
        </span> &nbsp;·&nbsp;
        <span style="font-family:'JetBrains Mono',monospace; font-size:12.5px; color:{THEME['TEXT_MUTED2']};">
        scroll to zoom · drag to pan · double-click to reset
        </span>""",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------
# TAB 4 — HISTORY
# ----------------------------------------------------

with tab_history:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">TABLE</span> Historical TCS Data</div>',
        unsafe_allow_html=True
    )

    max_rows = len(df)
    default_rows = min(20, max_rows)
    num_rows = st.slider(
        "Rows to display (most recent first)",
        min_value=min(5, max_rows), max_value=max_rows, value=default_rows,
        step=1 if max_rows < 50 else 10,
    )

    display_df = df.tail(num_rows).sort_index(ascending=False)
    st.dataframe(display_df, use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️  Download Full Dataset (CSV)",
        data=csv_bytes,
        file_name="TCS_stock_cleaned.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ----------------------------------------------------
# TAB 5 — MODEL PERFORMANCE
# ----------------------------------------------------

with tab_model:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">BACKTEST</span> Prediction vs Actual</div>',
        unsafe_allow_html=True
    )

    if backtest_df is None:
        st.warning(
            "Historical actual-vs-predicted comparison isn't available — the dataset doesn't "
            "include a `Predicted_Close` ground-truth column to compare against."
        )
    else:
        st.markdown(
            f"""<div class="subtext">
            The model was run on every historical row's Open/High/Low/Close and compared against the
            real next-day closing price already recorded in the dataset ({len(backtest_df):,} data points).
            No values below are simulated.
            </div>""",
            unsafe_allow_html=True
        )

        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">Mean Abs. Error</div>
                <div class="metric-value">₹{mae:.2f}</div>
                <div class="metric-sub">avg. rupee deviation</div>
            </div>""", unsafe_allow_html=True)
        with mcol2:
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">RMSE</div>
                <div class="metric-value">₹{rmse:.2f}</div>
                <div class="metric-sub">penalizes large misses</div>
            </div>""", unsafe_allow_html=True)
        with mcol3:
            r2_display = f"{r2:.4f}" if not np.isnan(r2) else "N/A"
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">R² Score</div>
                <div class="metric-value">{r2_display}</div>
                <div class="metric-sub">variance explained</div>
            </div>""", unsafe_allow_html=True)
        with mcol4:
            mape_display = f"{mape:.2f}%" if not np.isnan(mape) else "N/A"
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">MAPE</div>
                <div class="metric-value">{mape_display}</div>
                <div class="metric-sub">avg. % error</div>
            </div>""", unsafe_allow_html=True)

        st.write("")

        st.markdown(
            '<div class="section-header"><span class="eyebrow">OVERLAY</span> Actual vs Model-Predicted Close</div>',
            unsafe_allow_html=True
        )

        bt_range_options = {"90D": 90, "1Y": 252, "3Y": 756, "All": len(backtest_df)}
        bt_range = st.radio(
            "Backtest range", options=list(bt_range_options.keys()), index=1,
            horizontal=True, label_visibility="collapsed", key="bt_range",
        )
        bt_lookback = bt_range_options[bt_range]
        bt_plot = backtest_df.tail(bt_lookback)
        bt_x = bt_plot["Date"] if "Date" in bt_plot.columns else bt_plot.index

        fig_bt = go.Figure()
        fig_bt.add_trace(go.Scatter(
            x=bt_x, y=bt_plot["Predicted_Close"], mode="lines",
            line=dict(color="#2dd4bf", width=1.8), name="Actual Next-Day Close",
        ))
        fig_bt.add_trace(go.Scatter(
            x=bt_x, y=bt_plot["Model_Predicted"], mode="lines",
            line=dict(color="#7c5cff", width=1.6, dash="dot"), name="Model Predicted",
        ))
        fig_bt.update_layout(
            height=420, margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        )
        fig_bt.update_xaxes(gridcolor=THEME["CHART_GRID"])
        fig_bt.update_yaxes(gridcolor=THEME["CHART_GRID"], side="right", title="₹")
        st.plotly_chart(fig_bt, use_container_width=True, config={"displayModeBar": False})

        st.write("")

        st.markdown(
            '<div class="section-header"><span class="eyebrow">SCATTER</span> Predicted vs Actual Correlation</div>',
            unsafe_allow_html=True
        )

        sample = backtest_df.sample(min(2000, len(backtest_df)), random_state=42)
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=sample["Predicted_Close"], y=sample["Model_Predicted"],
            mode="markers", marker=dict(color="#7c5cff", size=5, opacity=0.45),
            name="Predictions",
        ))
        axis_min = float(min(sample["Predicted_Close"].min(), sample["Model_Predicted"].min()))
        axis_max = float(max(sample["Predicted_Close"].max(), sample["Model_Predicted"].max()))
        fig_scatter.add_trace(go.Scatter(
            x=[axis_min, axis_max], y=[axis_min, axis_max],
            mode="lines", line=dict(color="#f0b429", width=1.5, dash="dash"),
            name="Perfect Prediction",
        ))
        fig_scatter.update_layout(
            height=420, margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
            xaxis_title="Actual Next-Day Close (₹)", yaxis_title="Model Predicted (₹)",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        )
        fig_scatter.update_xaxes(gridcolor=THEME["CHART_GRID"])
        fig_scatter.update_yaxes(gridcolor=THEME["CHART_GRID"])
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

        st.caption(
            "Points closer to the dashed diagonal indicate predictions closer to the actual "
            "next-day closing price. Metrics above are computed on the full historical dataset."
        )


# ----------------------------------------------------
# TAB 6 — FIT CHECK (overfitting / underfitting diagnosis)
# ----------------------------------------------------

with tab_fit:

    st.markdown(
        '<div class="section-header"><span class="eyebrow">DIAGNOSIS</span> Overfitting / Underfitting Check</div>',
        unsafe_allow_html=True
    )

    if backtest_df is None or fit_diag is None:
        st.warning(
            "A fit diagnosis needs the `Predicted_Close` ground-truth column and at least "
            "~30 historical rows to compare against — this dataset doesn't have enough of either."
        )
    else:
        ref_m = fit_diag["reference"]
        hold_m = fit_diag["holdout"]
        verdict = fit_diag["verdict"]

        verdict_meta = {
            "good_fit": dict(
                cls="fit-good", icon="🟢", label="GOOD FIT",
                explanation=(
                    "The model performs consistently well on both the earlier reference "
                    "period and the more recent holdout period. R² stays reasonably high "
                    "in both, and error doesn't blow up on newer data — a sign the model "
                    "has learned a generalizable relationship rather than memorizing noise."
                ),
            ),
            "overfit": dict(
                cls="fit-overfit", icon="🔴", label="OVERFITTING RISK",
                explanation=(
                    "The model tracks the earlier reference period noticeably better than "
                    "the more recent holdout period — R² drops and/or error grows on newer "
                    "data. This pattern typically means the model latched onto patterns "
                    "specific to the earlier data (or the market regime shifted) rather "
                    "than learning something that holds up going forward."
                ),
            ),
            "underfit": dict(
                cls="fit-underfit", icon="🟡", label="UNDERFITTING",
                explanation=(
                    "The model explains relatively little variance in either the reference "
                    "or the holdout period (low R² in both). This usually means the model "
                    "is too simple for the relationship between Open/High/Low/Close and the "
                    "next-day close, or the features alone don't carry enough signal."
                ),
            ),
            "moderate": dict(
                cls="fit-moderate", icon="🟣", label="MODERATE FIT",
                explanation=(
                    "Performance is mixed — not a clean case of overfitting or underfitting. "
                    "The reference and holdout segments show some difference, but not enough "
                    "to point clearly in one direction. Worth monitoring as more data comes in."
                ),
            ),
        }[verdict]

        st.markdown(f"""
        <div class="fit-chip {verdict_meta['cls']}">{verdict_meta['icon']} {verdict_meta['label']}</div>
        <div class="fit-note">{verdict_meta['explanation']}</div>
        """, unsafe_allow_html=True)

        st.markdown(
            """<div class="fit-caveat">
            Note: this model was loaded pre-trained, so the original train/test split isn't known.
            This diagnosis approximates it by chronologically splitting the historical backtest into
            an earlier "reference" segment and a later "holdout" segment, then comparing how well the
            model's predictions hold up in each. It's a reasonable proxy for generalization drift, but
            not a substitute for re-evaluating the model with its actual training-time train/test split.
            </div>""",
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f'<div class="section-header"><span class="eyebrow">SPLIT</span> Reference (first {int(fit_diag["split_idx"])} rows) vs Holdout (last {len(fit_diag["holdout_seg"])} rows)</div>',
            unsafe_allow_html=True
        )

        colR, colH = st.columns(2)

        with colR:
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">Reference Segment — R²</div>
                <div class="metric-value">{ref_m['r2']:.4f}</div>
                <div class="metric-sub">MAE ₹{ref_m['mae']:.2f} · RMSE ₹{ref_m['rmse']:.2f} · MAPE {ref_m['mape']:.2f}% · n={ref_m['n']}</div>
            </div>""", unsafe_allow_html=True)

        with colH:
            gap_color = "#ff5c5c" if verdict == "overfit" else ("#2dd4bf" if verdict == "good_fit" else "#f0b429")
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">Holdout Segment — R²</div>
                <div class="metric-value" style="color:{gap_color};">{hold_m['r2']:.4f}</div>
                <div class="metric-sub">MAE ₹{hold_m['mae']:.2f} · RMSE ₹{hold_m['rmse']:.2f} · MAPE {hold_m['mape']:.2f}% · n={hold_m['n']}</div>
            </div>""", unsafe_allow_html=True)

        st.write("")

        gapcol1, gapcol2, gapcol3 = st.columns(3)
        with gapcol1:
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">R² Gap (Reference − Holdout)</div>
                <div class="metric-value" style="color:{gap_color};">{fit_diag['r2_gap']:+.4f}</div>
                <div class="metric-sub">larger gap → stronger overfit signal</div>
            </div>""", unsafe_allow_html=True)
        with gapcol2:
            mape_ratio_display = f"{fit_diag['mape_ratio']:.2f}×" if not np.isnan(fit_diag["mape_ratio"]) else "N/A"
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">MAPE Ratio (Holdout / Reference)</div>
                <div class="metric-value" style="color:{gap_color};">{mape_ratio_display}</div>
                <div class="metric-sub">&gt;1.5× flags real degradation (scale-fair)</div>
            </div>""", unsafe_allow_html=True)
        with gapcol3:
            rmse_ratio_display = f"{fit_diag['rmse_ratio']:.2f}×" if not np.isnan(fit_diag["rmse_ratio"]) else "N/A"
            st.markdown(f"""
            <div class="tilt-card">
                <div class="metric-label">RMSE Ratio (Holdout / Reference)</div>
                <div class="metric-value">{rmse_ratio_display}</div>
                <div class="metric-sub">raw ₹ — inflated by price-level drift</div>
            </div>""", unsafe_allow_html=True)

        st.caption(
            "💡 Trust the MAPE ratio over the RMSE ratio here — RMSE is in raw ₹, so it naturally "
            "grows if TCS's price level rose between the reference and holdout periods, even with no "
            "real change in model quality. MAPE (% error) is scale-invariant and the fairer signal."
        )

        st.write("")

        st.markdown(
            '<div class="section-header"><span class="eyebrow">RESIDUALS</span> Prediction Error Over Time</div>',
            unsafe_allow_html=True
        )

        ref_seg = fit_diag["reference_seg"]
        hold_seg = fit_diag["holdout_seg"]
        ref_x = ref_seg["Date"] if "Date" in ref_seg.columns else ref_seg.index
        hold_x = hold_seg["Date"] if "Date" in hold_seg.columns else hold_seg.index

        fig_res = go.Figure()
        fig_res.add_trace(go.Scatter(
            x=ref_x, y=ref_seg["Error"], mode="markers",
            marker=dict(color="#7c5cff", size=4, opacity=0.45),
            name="Reference Segment",
        ))
        fig_res.add_trace(go.Scatter(
            x=hold_x, y=hold_seg["Error"], mode="markers",
            marker=dict(color="#f0b429", size=4, opacity=0.55),
            name="Holdout Segment",
        ))
        fig_res.add_hline(y=0, line=dict(color=THEME["CHART_GRID"], width=1.5, dash="dot"))
        fig_res.update_layout(
            height=380, margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
            hovermode="x unified",
            xaxis_title="Date" if has_date_col else "Row Index",
            yaxis_title="Error (Predicted − Actual, ₹)",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        )
        fig_res.update_xaxes(gridcolor=THEME["CHART_GRID"])
        fig_res.update_yaxes(gridcolor=THEME["CHART_GRID"])
        st.plotly_chart(fig_res, use_container_width=True, config={"displayModeBar": False})

        st.caption(
            "If the holdout (amber) points sit visibly further from zero or spread out more than the "
            "reference (violet) points, that's the visual signature of overfitting — the model fits older "
            "data well but its errors grow on data it effectively hasn't 'seen' the pattern for."
        )

        st.write("")

        st.markdown(
            '<div class="section-header"><span class="eyebrow">DISTRIBUTION</span> Error Spread: Reference vs Holdout</div>',
            unsafe_allow_html=True
        )

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=ref_seg["Error"], name="Reference Segment",
            marker_color="rgba(124,92,255,0.55)", nbinsx=40,
        ))
        fig_hist.add_trace(go.Histogram(
            x=hold_seg["Error"], name="Holdout Segment",
            marker_color="rgba(240,180,41,0.55)", nbinsx=40,
        ))
        fig_hist.update_layout(
            barmode="overlay", height=340, margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["CHART_FONT"], family="JetBrains Mono", size=11),
            xaxis_title="Error (₹)", yaxis_title="Frequency",
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, bgcolor="rgba(0,0,0,0)"),
        )
        fig_hist.update_xaxes(gridcolor=THEME["CHART_GRID"])
        fig_hist.update_yaxes(gridcolor=THEME["CHART_GRID"])
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

        st.caption(
            "A wider or off-center amber (holdout) distribution compared to the violet (reference) "
            "distribution reinforces the same signal shown in the metrics above."
        )


# ====================================================
# FOOTER
# ====================================================

st.divider()
st.markdown(
    '<div class="footer-note">TCS Stock Price Prediction using Machine Learning · Terminal UI · '
    'Educational project — not financial advice</div>',
    unsafe_allow_html=True
)