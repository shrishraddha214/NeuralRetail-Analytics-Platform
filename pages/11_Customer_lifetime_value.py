import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Lifetime Value",
    page_icon="💎",
    layout="wide"
)

st.title("💎 Customer Lifetime Value Dashboard")

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
# CLEAN DUPLICATE COLUMNS
# --------------------------------------------------

if "Segment_y" in df.columns:
    df["Segment"] = df["Segment_y"]
elif "Segment_x" in df.columns:
    df["Segment"] = df["Segment_x"]

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

segments = sorted(df["Segment"].dropna().unique())

selected_segment = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)

countries = sorted(df["Country"].dropna().unique())

selected_country = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries
)

df = df[
    (df["Segment"].isin(selected_segment)) &
    (df["Country"].isin(selected_country))
]

if df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# --------------------------------------------------
# CUSTOMER LEVEL DATA
# --------------------------------------------------

customer = (
    df.groupby("Customer ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Monetary=("Monetary", "first"),
        Frequency=("Frequency", "first"),
        Segment=("Segment", "first"),
        Country=("Country", "first")
    )
    .reset_index()
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_customers = customer["Customer ID"].nunique()
total_revenue = customer["Revenue"].sum()
avg_clv = customer["Monetary"].mean()
best_segment = (
    customer.groupby("Segment")["Revenue"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

c2.metric(
    "💰 Revenue",
    f"£{total_revenue:,.0f}"
)

c3.metric(
    "💎 Avg CLV",
    f"£{avg_clv:,.0f}"
)

c4.metric(
    "🏆 Best Segment",
    best_segment
)

st.divider()

# --------------------------------------------------
# CUSTOMER VALUE BUBBLE CHART
# --------------------------------------------------

st.subheader("💎 Customer Value Matrix")

fig1 = px.scatter(
    customer,
    x="Frequency",
    y="Monetary",
    size="Revenue",
    color="Segment",
    hover_name="Customer ID",
    size_max=45,
    title="Customer Lifetime Value vs Purchase Frequency"
)

fig1.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Purchase Frequency",
    yaxis_title="Customer Lifetime Value (£)"
)

st.plotly_chart(
    fig1,
    width="stretch",
    key="bubble_clv"
)

st.divider()

# --------------------------------------------------
# PARETO ANALYSIS (80/20 RULE)
# --------------------------------------------------

st.subheader("📈 Pareto Analysis (Top Customers Contribution)")

pareto = (
    customer.sort_values("Revenue", ascending=False)
    .reset_index(drop=True)
)

pareto["Cumulative Revenue"] = pareto["Revenue"].cumsum()
pareto["Cumulative %"] = (
    pareto["Cumulative Revenue"]
    / pareto["Revenue"].sum()
) * 100

fig2 = px.bar(
    pareto.head(20),
    x="Customer ID",
    y="Revenue",
    title="Top 20 Customers by Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig2.add_scatter(
    x=pareto.head(20)["Customer ID"],
    y=pareto.head(20)["Cumulative %"],
    mode="lines+markers",
    name="Cumulative %",
    yaxis="y2"
)

fig2.update_layout(
    template="plotly_dark",
    height=550,
    yaxis=dict(title="Revenue (£)"),
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        range=[0, 100]
    )
)

st.plotly_chart(
    fig2,
    width="stretch",
    key="pareto_chart"
)

st.divider()

# --------------------------------------------------
# TOP 15 CUSTOMERS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    top15 = (
        customer.sort_values("Revenue", ascending=False)
        .head(15)
    )

    fig3 = px.bar(
        top15,
        x="Revenue",
        y=top15["Customer ID"].astype(str),
        orientation="h",
        color="Revenue",
        title="Top 15 Customers by Revenue"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=550,
        yaxis_title="Customer ID"
    )

    st.plotly_chart(
        fig3,
        width="stretch",
        key="top15_customer"
    )

with right:

    seg = (
        customer.groupby("Segment")
        .agg(
            Customers=("Customer ID", "count"),
            Revenue=("Revenue", "sum")
        )
        .reset_index()
    )

    fig4 = px.bar(
        seg,
        x="Segment",
        y="Customers",
        color="Revenue",
        title="Customers by Segment"
    )

    fig4.update_layout(
        template="plotly_dark",
        height=550
    )

    st.plotly_chart(
        fig4,
        width="stretch",
        key="segment_customer"
    )

st.divider()

# --------------------------------------------------
# CUSTOMER VALUE TABLE
# --------------------------------------------------

st.subheader("📋 Top Customer Summary")

table = (
    customer.sort_values("Revenue", ascending=False)
    .head(20)[
        [
            "Customer ID",
            "Revenue",
            "Monetary",
            "Frequency",
            "Segment",
            "Country"
        ]
    ]
)

table = table.rename(
    columns={
        "Customer ID": "Customer",
        "Revenue": "Revenue (£)",
        "Monetary": "CLV (£)",
        "Frequency": "Frequency"
    }
)

st.dataframe(
    table,
    width="stretch",
    hide_index=True
)

st.divider()

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

highest_customer = (
    customer.sort_values("Revenue", ascending=False)
    .iloc[0]["Customer ID"]
)

highest_country = (
    customer.groupby("Country")["Revenue"]
    .sum()
    .idxmax()
)

highest_segment = (
    customer.groupby("Segment")["Revenue"]
    .sum()
    .idxmax()
)

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Value Customer: **{int(highest_customer)}**

💰 Highest Revenue Segment: **{highest_segment}**

🌍 Highest Revenue Country: **{highest_country}**

👥 Total Customers: **{total_customers:,}**

💎 Average Customer Lifetime Value: **£{avg_clv:,.0f}**

### Recommendations

• Prioritize retention of high-value customers.

• Create exclusive loyalty programs for premium customers.

• Cross-sell products to customers with high purchase frequency.

• Focus marketing efforts on high-performing customer segments.
""")