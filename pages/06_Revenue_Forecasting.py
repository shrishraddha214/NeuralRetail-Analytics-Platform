import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Revenue Forecast",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Revenue Forecast Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    forecast = pd.read_csv("data/processed/dashboard_dataset.csv")
    actual = pd.read_csv( "data/processed/daily_sales.csv")

    forecast["ds"] = pd.to_datetime(forecast["ds"])
    actual["ds"] = pd.to_datetime(actual["ds"])

    return forecast, actual

forecast, actual = load_data()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

current_revenue = actual["y"].sum()
future_revenue = forecast.tail(30)["yhat"].sum()
growth = ((future_revenue-current_revenue)/current_revenue)*100

best_day = forecast.loc[forecast["yhat"].idxmax()]
best_prediction = best_day["yhat"]

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "💰 Current Revenue",
    f"£{current_revenue:,.0f}"
)

c2.metric(
    "📈 Forecast (30 Days)",
    f"£{future_revenue:,.0f}"
)

c3.metric(
    "🚀 Growth",
    f"{growth:.2f}%"
)

c4.metric(
    "⭐ Highest Forecast",
    f"£{best_prediction:,.0f}"
)

st.divider()

# --------------------------------------------------
# ACTUAL VS FORECAST
# --------------------------------------------------

left,right = st.columns(2)

with left:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=actual["ds"],
        y=actual["y"],
        mode="lines",
        name="Actual"
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode="lines",
        name="Forecast"
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Actual vs Forecast Revenue",
        height=500
    )

    st.plotly_chart(fig,width="stretch")

with right:

    fig2 = px.line(
        forecast,
        x="ds",
        y=["yhat","yhat_lower","yhat_upper"],
        title="Forecast Confidence Interval"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig2,width="stretch")
# --------------------------------------------------
# FORECAST CONFIDENCE
# --------------------------------------------------

fig2 = px.line(
    forecast,
    x="ds",
    y=["yhat", "yhat_lower", "yhat_upper"],
    title="Forecast Confidence Interval"
)

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, width="stretch")

# --------------------------------------------------
# NEXT 30 DAYS FORECAST
# --------------------------------------------------

next30 = forecast.tail(30)

fig3 = px.bar(
    next30,
    x="ds",
    y="yhat",
    color="yhat",
    title="Next 30 Days Predicted Revenue"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, width="stretch")

# --------------------------------------------------
# FORECAST TABLE
# --------------------------------------------------

st.divider()

st.subheader("📋 Next 30 Days Forecast")

table = next30[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()

table.columns = [
    "Date",
    "Forecast Revenue",
    "Lower Limit",
    "Upper Limit"
]

st.dataframe(
    table,
    width="stretch",
    hide_index=True
)
# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader("📌 Business Insights")

col1,col2 = st.columns(2)

with col1:

    st.info(f"""
### Revenue Forecast

- Forecast generated using **Facebook Prophet**
- Total forecast revenue: **£{future_revenue:,.0f}**
- Highest expected revenue: **£{best_prediction:,.0f}**
- Expected growth: **{growth:.2f}%**
""")

with col2:

    st.success(f"""
### Recommendation

✔ Increase inventory before **{best_day['ds'].strftime('%d %B %Y')}**

✔ Plan marketing campaigns around forecast peaks

✔ Monitor actual sales against predictions

✔ Update the forecasting model monthly
""")