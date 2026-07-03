import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Executive Business Summary")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        r"C:\Users\91895\OneDrive\Desktop\NeuralRetail\data\processed\dashboard_dataset.csv"
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

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

st.sidebar.header("Dashboard Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].dropna().unique()),
    default=sorted(df["Country"].dropna().unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].dropna().unique()),
    default=sorted(df["Year"].dropna().unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Year"].isin(year)) &
    (df["Segment"].isin(segment))
]

if filtered_df.empty:
    st.warning("No data available.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

revenue = filtered_df["Revenue"].sum()
orders = filtered_df["Invoice"].nunique()
customers = filtered_df["Customer ID"].nunique()
products = filtered_df["StockCode"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Revenue",
    f"£{revenue:,.0f}"
)

c2.metric(
    "🛒 Orders",
    f"{orders:,}"
)

c3.metric(
    "👥 Customers",
    f"{customers:,}"
)

c4.metric(
    "📦 Products",
    f"{products:,}"
)

st.divider()

# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------

left, right = st.columns([2,1])

with left:

    trend = (
        filtered_df
        .groupby("InvoiceDate")["Revenue"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        trend,
        x="InvoiceDate",
        y="Revenue",
        markers=True,
        title="Revenue Trend"
    )

    fig1.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig1,
        width="stretch",
        key="summary_trend"
    )

with right:

    country_rev = (
        filtered_df
        .groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        country_rev,
        x="Revenue",
        y="Country",
        orientation="h",
        color="Revenue",
        title="Top Revenue Countries"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig2,
        width="stretch",
        key="country_summary"
    )

st.divider()

# --------------------------------------------------
# SEGMENT CONTRIBUTION
# --------------------------------------------------

segment_rev = (
    filtered_df
    .groupby("Segment")["Revenue"]
    .sum()
    .reset_index()
)

fig3 = px.treemap(
    segment_rev,
    path=["Segment"],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Blues",
    title="Revenue Contribution by Customer Segment"
)

fig3.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig3,
    width="stretch",
    key="segment_treemap"
)

st.divider()

# --------------------------------------------------
# TOP PRODUCTS & TOP CUSTOMERS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Description")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_products,
        width="stretch",
        hide_index=True
    )

with right:

    st.subheader("👑 Top 10 Customers")

    top_customers = (
        filtered_df.groupby("Customer ID")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            Country=("Country", "first")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_customers,
        width="stretch",
        hide_index=True
    )

st.divider()

# --------------------------------------------------
# BUSINESS PERFORMANCE SCORECARD
# --------------------------------------------------

st.subheader("📊 Business Performance Scorecard")

score = pd.DataFrame({
    "Business Area": [
        "Revenue Growth",
        "Customer Base",
        "Order Volume",
        "Product Diversity",
        "Customer Segmentation",
        "Inventory Health"
    ],
    "Status": [
        "Excellent",
        "Excellent",
        "Good",
        "Good",
        "Excellent",
        "Moderate"
    ]
})

st.dataframe(
    score,
    width="stretch",
    hide_index=True
)

st.divider()

# --------------------------------------------------
# EXECUTIVE RECOMMENDATIONS
# --------------------------------------------------

top_country = (
    filtered_df.groupby("Country")["Revenue"]
    .sum()
    .idxmax()
)

top_segment = (
    filtered_df.groupby("Segment")["Revenue"]
    .sum()
    .idxmax()
)

top_product = (
    filtered_df.groupby("Description")["Revenue"]
    .sum()
    .idxmax()
)

avg_order = revenue / orders if orders > 0 else 0

st.subheader("🤖 Executive Recommendations")

st.success(f"""
### Key Findings

✅ Total Revenue Generated: **£{revenue:,.0f}**

✅ Total Customers: **{customers:,}**

✅ Total Orders: **{orders:,}**

✅ Average Order Value: **£{avg_order:,.2f}**

---

### Business Highlights

🏆 Highest Revenue Country: **{top_country}**

👥 Best Customer Segment: **{top_segment}**

📦 Best Selling Product: **{top_product}**

---

### Strategic Recommendations

• Increase marketing investment in **{top_country}**.

• Retain **{top_segment}** customers using loyalty programs.

• Bundle high-performing products with medium-selling products.

• Re-engage inactive customers through personalized campaigns.

• Improve inventory planning using the forecasting dashboard.

• Continue monitoring churn prediction to improve customer retention.
""")

st.divider()

# --------------------------------------------------
# PROJECT SUMMARY
# --------------------------------------------------

st.subheader("📌 Project Summary")

st.info("""
### NeuralRetail Business Intelligence System

This dashboard summarizes insights generated across the analytics platform.

The project includes:

• Executive Dashboard

• Sales Performance Analysis

• Product Performance Analysis

• Customer Analytics

• Geographic Sales Analysis

• Monthly & Seasonal Trends

• Customer Segmentation

• Churn Prediction

• Inventory Analysis

• Order Analysis

• Customer Lifetime Value Analysis

• Executive Business Summary

The dashboards provide actionable insights for strategic decision-making using interactive visualizations, customer segmentation, revenue forecasting, and business intelligence techniques.
""")