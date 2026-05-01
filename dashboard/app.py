import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("Crypto Pipeline Dashboard")

conn = duckdb.connect("data/crypto.duckdb")

daily_summary = conn.execute("""
    SELECT * FROM daily_summary
""").fetchdf()

moving_averages = conn.execute("""
    SELECT * FROM moving_averages
""").fetchdf()

st.subheader("Daily Summary")
st.dataframe(daily_summary)

fig1 = px.bar(
    daily_summary,
    x="crypto",
    y="avg_price_usd",
    title="Average crypto price in USD"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Moving Averages")
st.dataframe(moving_averages)

fig2 = px.line(
    moving_averages,
    x="crypto",
    y="moving_avg_3",
    title="Moving average by crypto"
)
st.plotly_chart(fig2, use_container_width=True)