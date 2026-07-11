import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\91895\OneDrive\Desktop\NeuralRetail\data\processed\dashboard_dataset.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("📊 Dashboard Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

month = st.sidebar.multiselect(
    "Month",
    sorted(df["Month_Name"].unique()),
    default=sorted(df["Month_Name"].unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df[
    (df["Country"].isin(country)) &
    (df["Year"].isin(year)) &
    (df["Month_Name"].isin(month)) &
    (df["Segment"].isin(segment))
]

# =====================================================
# TITLE
# =====================================================

st.title("📊 Executive Dashboard")

st.markdown("Business Performance Overview")

st.divider()

# =====================================================
# KPI SECTION
# =====================================================

total_revenue = filtered_df["Revenue"].sum()
customers = filtered_df["Customer ID"].nunique()
orders = filtered_df["Invoice"].nunique()
products = filtered_df["StockCode"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Revenue",
    f"£{total_revenue:,.0f}"
)

c2.metric(
    "👥 Customers",
    f"{customers:,}"
)

c3.metric(
    "📦 Orders",
    f"{orders:,}"
)

c4.metric(
    "🛍 Products",
    f"{products:,}"
)

st.divider()

# =====================================================
# REVENUE TREND
# =====================================================

st.subheader("📈 Revenue Trend")

daily = (
    filtered_df
    .groupby("InvoiceDate")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily,
    x="InvoiceDate",
    y="Revenue",
    markers=True
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_title="Date",
    yaxis_title="Revenue (£)"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# COUNTRY + SEGMENT
# =====================================================

left, right = st.columns(2)

with left:

    country_df = (
        filtered_df
        .groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_country = px.bar(
        country_df,
        x="Country",
        y="Revenue",
        color="Revenue",
        title="Top 10 Countries by Revenue"
    )

    fig_country.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig_country, use_container_width=True)

with right:

    segment_df = (
        filtered_df
        .groupby("Segment")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_segment = px.pie(
        segment_df,
        names="Segment",
        values="Revenue",
        hole=0.55,
        title="Revenue by Customer Segment"
    )

    fig_segment.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig_segment, use_container_width=True)

st.divider()

# =====================================================
# MONTHLY REVENUE
# =====================================================

monthly = (
    filtered_df
    .groupby("Month_Name")["Revenue"]
    .sum()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly["Month_Name"] = pd.Categorical(
    monthly["Month_Name"],
    categories=month_order,
    ordered=True
)

monthly = monthly.sort_values("Month_Name")

fig_month = px.area(
    monthly,
    x="Month_Name",
    y="Revenue",
    title="Monthly Revenue"
)

fig_month.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig_month, use_container_width=True)

st.divider()

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("💡 Business Insights")

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

top_month = (
    monthly.sort_values("Revenue", ascending=False)
    .iloc[0]["Month_Name"]
)

st.success(f"""
• **Top Revenue Country:** {top_country}

• **Highest Revenue Segment:** {top_segment}

• **Highest Revenue Month:** {top_month}

• **Total Revenue:** £{total_revenue:,.0f}

• Use the filters on the left to interactively explore business performance.
""")