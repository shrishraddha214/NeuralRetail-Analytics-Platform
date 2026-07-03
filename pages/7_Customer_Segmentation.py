import streamlit as st
import pandas as pd
import plotly.express as px
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)
st.title("👥 Customer Segmentation Dashboard")
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        r"C:\Users\91895\OneDrive\Desktop\NeuralRetail\data\processed\dashboard_dataset.csv"
    )
    return df

df = load_data()
# --------------------------------------------------
# CLEAN DUPLICATE COLUMNS
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
# SIDEBAR
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
customers = df["Customer ID"].nunique()
revenue = df["Revenue"].sum()
avg_customer = revenue / customers if customers > 0 else 0
largest_segment = df["Segment"].value_counts().idxmax()
c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Customers", f"{customers:,}")
c2.metric("💰 Revenue", f"£{revenue:,.0f}")
c3.metric("💳 Avg Revenue / Customer", f"£{avg_customer:,.0f}")
c4.metric("🏆 Largest Segment", largest_segment)
st.divider()
# --------------------------------------------------
# SEGMENT ANALYSIS
# --------------------------------------------------

st.subheader("📊 Customer Segment Analysis")

bubble = (
    df.groupby("Segment")
    .agg(
        Customers=("Customer ID", "nunique"),
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique")
    )
    .reset_index()
)

fig_bubble = px.scatter(
    bubble,
    x="Orders",
    y="Revenue",
    size="Customers",
    color="Segment",
    hover_name="Segment",
    size_max=70,
    title="Customer Segments by Revenue & Orders"
)

fig_bubble.update_layout(
    template="plotly_dark",
    height=500
)

segment_rev = (
    df.groupby("Segment")["Revenue"]
    .sum()
    .reset_index()
)

fig2 = px.sunburst(
    segment_rev,
    path=["Segment"],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Viridis",
    title="Revenue Contribution by Segment"
)

fig2.update_layout(
    template="plotly_dark",
    height=500
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_bubble,
        width="stretch",
        key="segment_bubble"
    )

with right:
    st.plotly_chart(
        fig2,
        width="stretch",
        key="segment_sunburst"
    )
# --------------------------------------------------
# RECENCY vs MONETARY
# --------------------------------------------------
scatter = (
    df.groupby("Customer ID")
    .agg(
        Recency=("Recency", "first"),
        Monetary=("Monetary", "first"),
        Segment=("Segment", "first")
    )
    .reset_index()
)

fig3 = px.scatter(
    scatter,
    x="Recency",
    y="Monetary",
    color="Segment",
    size="Monetary",
    hover_data=["Customer ID"],
    title="Recency vs Monetary"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, width="stretch")

# --------------------------------------------------
# FREQUENCY vs MONETARY
# --------------------------------------------------

scatter2 = (
    df.groupby("Customer ID")
    .agg(
        Frequency=("Frequency", "first"),
        Monetary=("Monetary", "first"),
        Segment=("Segment", "first")
    )
    .reset_index()
)

fig4 = px.scatter(
    scatter2,
    x="Frequency",
    y="Monetary",
    color="Segment",
    size="Frequency",
    hover_data=["Customer ID"],
    title="Frequency vs Monetary"
)

fig4.update_layout(template="plotly_dark")

st.plotly_chart(fig4, width="stretch")

# --------------------------------------------------
# SUMMARY TABLE
# --------------------------------------------------

st.subheader("📋 Segment Summary")

table = (
    df.groupby("Segment")
    .agg(
        Customers=("Customer ID", "nunique"),
        Revenue=("Revenue", "sum"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary=("Monetary", "mean")
    )
    .reset_index()
)

st.dataframe(
    table,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

best_segment = segment_rev.sort_values(
    "Revenue",
    ascending=False
).iloc[0]["Segment"]

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Revenue Segment: **{best_segment}**

👥 Total Customers: **{customers:,}**

💰 Total Revenue: **£{revenue:,.0f}**

📈 Customers are grouped using RFM Analysis and K-Means Clustering.

### Recommendations
- Reward Loyal/VIP customers with exclusive offers.
- Re-engage At-Risk customers through targeted campaigns.
- Upsell Regular customers to increase lifetime value.
""")