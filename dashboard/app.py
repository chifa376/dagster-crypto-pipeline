import streamlit as st
import duckdb

import pandas as pd
import plotly.express as px
COLOR_PALETTE = ["#2F80ED", "#6C2BD9", "#00B8D9", "#20C997", "#FFB020"]
# ================= CONFIG =================
st.set_page_config(
    page_title="Crypto BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= DATA =================
@st.cache_data
def load_data():
    conn = duckdb.connect("data/crypto.duckdb")
    df_raw = conn.execute("SELECT * FROM crypto_prices_raw").fetchdf()
    df_summary = conn.execute("SELECT * FROM daily_summary").fetchdf()
    df_ma = conn.execute("SELECT * FROM moving_averages").fetchdf()
    conn.close()

    df_raw["extracted_at"] = pd.to_datetime(df_raw["extracted_at"])
    return df_raw, df_summary, df_ma


try:
    df_raw, df_summary, df_ma = load_data()
except Exception:
    st.error("❌ Données introuvables. Lance d'abord l'extraction puis dbt run.")
    st.stop()

# ================= SIDEBAR =================
st.sidebar.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
    <div style="font-size:28px;">📊</div>
    <div style="font-size:22px;font-weight:800;">Crypto BI</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Accueil", "💰 Prix", "🏦 Market Cap", "📈 Tendances", "🧾 Données"]
)

crypto_list = df_raw["crypto"].unique().tolist()
selected_crypto = st.sidebar.selectbox("Choisir une crypto", crypto_list)

st.sidebar.markdown("### ⏱ Filtre temps")

df_raw["time_str"] = df_raw["extracted_at"].dt.strftime("%H:%M:%S")
time_options = df_raw["time_str"].sort_values().unique().tolist()

selected_times = st.sidebar.multiselect(
    "Choisir les heures d'extraction",
    options=time_options,
    default=time_options
)

df_raw = df_raw[df_raw["time_str"].isin(selected_times)]

if df_raw.empty:
    st.warning("Aucune donnée pour ce filtre.")
    st.stop()
# ================= STYLE =================

st.markdown("""
<style>

/* ===== GLOBAL RESET ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Supprimer TOUS les espaces du haut */
[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
}

section.main > div {
    padding-top: 0rem !important;
}

/* Container principal */
.block-container {
    padding-top: 0rem !important;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1450px;
}

/* ===== SIDEBAR FIX ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #16004f 0%, #25006f 100%);
    padding-top: 0rem !important;
}

/* ⚡ IMPORTANT : supprimer espace interne réel */
[data-testid="stSidebar"] > div {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* 🔥 ULTIMATE FIX (celui qui manquait) */
[data-testid="stSidebarNav"] {
    padding-top: 0rem !important;
}

/* Texte sidebar */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Selectbox */
[data-testid="stSelectbox"] div {
    color: #111827 !important;
    border-radius: 12px !important;
}

/* ===== DESIGN ===== */
.stApp {
    background: #f7f9fc;
}

/* Title */
.main-title {
    font-size: 38px;
    font-weight: 900;
    color: #25105f;
}

/* KPI */
[data-testid="stMetric"] {
    background: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(37, 16, 95, 0.08);
}

[data-testid="stMetricValue"] {
    color: #25105f !important;
    font-size: 30px;
    font-weight: 900;
}

/* Charts */
[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
}

/* Radio menu */
.stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    padding: 9px 12px;
    border-radius: 10px;
    margin-bottom: 7px;
}
            
/* Remonter tout le contenu de la sidebar */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    margin-top: -55px !important;
}

/* Optionnel : cacher le bouton << */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)


# ================= PREP DATA =================
df_crypto = df_raw[df_raw["crypto"] == selected_crypto].sort_values("extracted_at")
df_ma_crypto = df_ma[df_ma["crypto"] == selected_crypto]

latest = df_crypto.iloc[-1]
first = df_crypto.iloc[0]

price_growth = ((latest["price_usd"] - first["price_usd"]) / first["price_usd"]) * 100
volatility = df_crypto["price_usd"].max() - df_crypto["price_usd"].min()
trend = "Haussière 📈" if price_growth >= 0 else "Baissière 📉"

best_crypto = df_summary.loc[df_summary["avg_price_usd"].idxmax()]["crypto"]

# Comparaison BTC vs ETH
btc_avg = df_summary[df_summary["crypto"] == "bitcoin"]["avg_price_usd"].values[0]
eth_avg = df_summary[df_summary["crypto"] == "ethereum"]["avg_price_usd"].values[0]
ratio = btc_avg / eth_avg

# ================= HEADER =================
st.markdown('<div class="main-title">📊 Crypto Analytics Dashboard</div>', unsafe_allow_html=True)

# ================= ALERTES =================
if latest["change_24h_usd"] > 0:
    st.success(f"🚀 Alerte positive : {selected_crypto.upper()} est en hausse de {latest['change_24h_usd']:.2f}% sur 24h.")
else:
    st.error(f"⚠️ Alerte baisse : {selected_crypto.upper()} est en baisse de {latest['change_24h_usd']:.2f}% sur 24h.")

# ================= ACCUEIL =================
if page == "🏠 Accueil":
    st.subheader("Vue globale")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Prix actuel", f"{latest['price_usd']:,.2f} $", f"{latest['change_24h_usd']:.2f}%")
    c2.metric("🚀 Croissance période", f"{price_growth:.2f}%")
    c3.metric("⚡ Volatilité", f"{volatility:,.2f} $")
    c4.metric("🏆 Top crypto", best_crypto.upper())

    st.info(f"Tendance actuelle : {trend}")
    # 🔥 Recommandation BI
    if price_growth > 5:
        st.success("📈 Recommandation : tendance forte → opportunité d'achat")
        st.caption("👉 Le marché montre une dynamique positive significative.")
    elif price_growth < -5:
        st.error("📉 Recommandation : tendance négative → prudence")
        st.caption("👉 Risque de baisse prolongée, éviter les décisions impulsives.")
    else:
        st.info("⚖️ Marché stable → observation recommandée")
        st.caption("👉 Aucun signal fort détecté.")
    st.warning(f"Comparaison BTC vs ETH : BTC est environ {ratio:.1f}x plus cher que ETH.")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df_summary,
            x="crypto",
            y="avg_price_usd",
            color="crypto",
            text_auto=".2f",
            title="💰 Prix moyen par crypto",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(
            height=360,
            margin=dict(l=60, r=30, t=60, b=40),
            showlegend=False  
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            df_summary,
            names="crypto",
            values="avg_market_cap_usd",
            title="🏦 Répartition du Market Cap",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_traces(
            textinfo="percent",        # % seulement dans le cercle
            textposition="inside"      # texte bien centré
        )

        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True,
            legend=dict(
                orientation="v",
                y=0.5,
                yanchor="middle",
                x=1.05,
                xanchor="left"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= PRIX =================
elif page == "💰 Prix":
    st.subheader(f"Analyse des prix - {selected_crypto.capitalize()}")

    c1, c2, c3 = st.columns(3)

    c1.metric("Prix USD", f"{latest['price_usd']:,.2f} $", f"{latest['change_24h_usd']:.2f}%")
    c2.metric("Prix EUR", f"{latest['price_eur']:,.2f} €")
    c3.metric("Prix moyen USD", f"{df_crypto['price_usd'].mean():,.2f} $")

    fig = px.line(
        df_crypto,
        x="extracted_at",
        y="price_usd",
        markers=True,
        title=f"📈 Évolution du prix USD - {selected_crypto.capitalize()}",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(line=dict(width=4), marker=dict(size=8))
    fig.update_layout(height=420, transition_duration=700)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(
        df_raw,
        x="extracted_at",
        y="price_usd",
        color="crypto",
        markers=True,
        title="Comparaison des prix entre cryptos",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig2.update_layout(height=420, transition_duration=700)
    st.plotly_chart(fig2, use_container_width=True)

# ================= MARKET CAP =================
elif page == "🏦 Market Cap":
    st.subheader("Analyse Market Cap")

    c1, c2, c3 = st.columns(3)

    c1.metric("Market Cap actuel", f"{latest['market_cap_usd']:,.0f} $")
    c2.metric("Market Cap moyen", f"{df_crypto['market_cap_usd'].mean():,.0f} $")
    c3.metric("Max Market Cap", f"{df_crypto['market_cap_usd'].max():,.0f} $")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df_summary,
            x="crypto",
            y="avg_market_cap_usd",
            color="crypto",
            text_auto=".2s",
            title="Market Cap moyen par crypto",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(height=380, transition_duration=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            df_summary,
            names="crypto",
            values="avg_market_cap_usd",
            title="Dominance du marché",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(height=380, transition_duration=600)
        st.plotly_chart(fig, use_container_width=True)

# ================= TENDANCES =================
elif page == "📈 Tendances":
    st.subheader(f"Tendances - {selected_crypto.capitalize()}")

    c1, c2, c3 = st.columns(3)

    c1.metric("Croissance période", f"{price_growth:.2f}%")
    c2.metric("Volatilité", f"{volatility:,.2f} $")
    c3.metric("Nombre d'observations", len(df_crypto))

    fig = px.line(
        df_ma_crypto,
        x=df_ma_crypto.index,
        y="moving_avg_3",
        markers=True,
        title=f"Moyenne mobile 3 observations - {selected_crypto.capitalize()}",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(line=dict(width=4))
    fig.update_layout(height=420, transition_duration=700)
    st.plotly_chart(fig, use_container_width=True)

    df_signal = df_crypto.copy()
    avg_price = df_crypto["price_usd"].mean()
    df_signal["signal"] = df_signal["price_usd"].apply(
        lambda x: "Haussière" if x >= avg_price else "Baissière"
    )

    fig2 = px.scatter(
        df_signal,
        x="extracted_at",
        y="price_usd",
        color="signal",
        size="price_usd",
        title="Signal de tendance",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig2.update_layout(height=420, transition_duration=700)
    st.plotly_chart(fig2, use_container_width=True)

# ================= DONNÉES =================
elif page == "🧾 Données":
    st.subheader("Tables utilisées")

    tab1, tab2, tab3 = st.tabs(["Données brutes", "Résumé journalier", "Moving Average"])

    with tab1:
        st.dataframe(df_raw, use_container_width=True)

    with tab2:
        st.dataframe(df_summary, use_container_width=True)

    with tab3:
        st.dataframe(df_ma, use_container_width=True)

st.divider()
