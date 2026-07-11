import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Churn Prediction Dashboard",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Customer Churn Prediction Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/processed/dashboard_dataset.csv"
    )
    return df

df = load_data()

# --------------------------------------------------
# HANDLE DUPLICATE COLUMNS
# --------------------------------------------------

if "Segment_y" in df.columns:
    df["Segment"] = df["Segment_y"]
elif "Segment_x" in df.columns:
    df["Segment"] = df["Segment_x"]

if "Churn_y" in df.columns:
    df["Churn"] = df["Churn_y"]
elif "Churn_x" in df.columns:
    df["Churn"] = df["Churn_x"]

# --------------------------------------------------
# SIDEBAR FILTER
# --------------------------------------------------

st.sidebar.header("Filters")

segments = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

df = df[df["Segment"].isin(segments)]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_customers = df["Customer ID"].nunique()

churn_customers = (
    df[df["Churn"] == 1]["Customer ID"]
    .nunique()
)

active_customers = total_customers - churn_customers

churn_rate = (
    churn_customers / total_customers * 100
    if total_customers > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Total Customers", f"{total_customers:,}")
c2.metric("⚠️ Churn Customers", churn_customers)
c3.metric("✅ Active Customers", active_customers)
c4.metric("📉 Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# --------------------------------------------------
# CHURN DISTRIBUTION
# --------------------------------------------------

left, right = st.columns(2)

pie = (
    df.groupby("Churn")["Customer ID"]
    .nunique()
    .reset_index(name="Customers")
)

pie["Status"] = pie["Churn"].map({
    0: "Active",
    1: "Churned"
})

import plotly.graph_objects as go

churn_rate = (
    df["Churn"].sum()
    / len(df)
) * 100

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=churn_rate,
    number={"suffix": "%"},
    title={"text": "Overall Churn Rate"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#EF4444"},
        "steps": [
            {"range": [0, 30], "color": "#16A34A"},
            {"range": [30, 60], "color": "#F59E0B"},
            {"range": [60, 100], "color": "#DC2626"}
        ]
    }
))

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig, width="stretch")
# --------------------------------------------------
# CHURN BY SEGMENT
# --------------------------------------------------

segment = (
    df.groupby("Segment")["Churn"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    segment,
    x="Segment",
    y="Churn",
    color="Churn",
    title="Churn by Customer Segment"
)

fig2.update_layout(template="plotly_dark")

with right:
    st.plotly_chart(fig2, width="stretch")

# --------------------------------------------------
# FREQUENCY VS MONETARY
# --------------------------------------------------

scatter = (
    df.groupby("Customer ID")
    .agg(
        Frequency=("Frequency", "first"),
        Monetary=("Monetary", "first"),
        Churn=("Churn", "first")
    )
    .reset_index()
)

scatter["Status"] = scatter["Churn"].map({
    0: "Active",
    1: "Churned"
})

fig3 = px.scatter(
    scatter,
    x="Frequency",
    y="Monetary",
    color="Status",
    size="Monetary",
    hover_data=["Customer ID"],
    title="Frequency vs Monetary"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, width="stretch")

# --------------------------------------------------
# RECENCY DISTRIBUTION
# --------------------------------------------------

fig4 = px.histogram(
    df,
    x="Recency",
    color="Segment",
    nbins=25,
    title="Customer Recency Distribution"
)

fig4.update_layout(template="plotly_dark")

st.plotly_chart(fig4, width="stretch")

# --------------------------------------------------
# HIGH RISK CUSTOMERS
# --------------------------------------------------

st.subheader("🚨 High Risk Customers")

risk = (
    df[df["Churn_Prediction"] == 1][[
        "Customer ID",
        "Segment",
        "Recency",
        "Frequency",
        "Monetary"
    ]]
    .drop_duplicates()
    .sort_values("Monetary", ascending=False)
)

st.dataframe(
    risk,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

highest = (
    segment.sort_values("Churn", ascending=False)
    .iloc[0]["Segment"]
)

st.subheader("💡 Business Insights")

st.success(f"""
📉 Overall Churn Rate: **{churn_rate:.2f}%**

⚠️ Highest Churn Segment: **{highest}**

👥 Total Customers: **{total_customers:,}**

### Recommendations

✔ Offer loyalty rewards to high-value customers.

✔ Contact customers with high Recency immediately.

✔ Personalize offers for customers predicted to churn.

✔ Monitor churn trends monthly to reduce customer loss.
""")