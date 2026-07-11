import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Country Analysis Dashboard")

# --------------------------------------------------
# LOAD DATA

# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/dashboard_dataset.csv")

df = load_data()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

segment = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

df = df[
    (df["Segment"].isin(segment)) &
    (df["Year"].isin(year))
]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

countries = df["Country"].nunique()
customers = df["Customer ID"].nunique()
revenue = df["Revenue"].sum()

top_country = (
    df.groupby("Country")["Revenue"]
      .sum()
      .idxmax()
)

top_revenue = (
    df.groupby("Country")["Revenue"]
      .sum()
      .max()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🌍 Countries", countries)
c2.metric("👥 Customers", f"{customers:,}")
c3.metric("🏆 Top Country", top_country)
c4.metric("💰 Revenue", f"£{revenue:,.0f}")

st.divider()

# ==================================================
# GRAPH 1 : TOP COUNTRIES BY REVENUE
# ==================================================

country_rev = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(15)
      .reset_index()
)

fig1 = px.bar(
    country_rev,
    x="Country",
    y="Revenue",
    color="Revenue",
    title="Top 15 Countries by Revenue"
)

fig1.update_layout(template="plotly_dark")

st.plotly_chart(fig1, width="stretch")

# ==================================================
# GRAPH 2 : AVERAGE ORDER VALUE
# ==================================================

country_aov = (
    df.groupby("Country")
      .agg(
          Revenue=("Revenue", "sum"),
          Orders=("Invoice", "nunique")
      )
)

country_aov["Average Order Value"] = (
    country_aov["Revenue"] /
    country_aov["Orders"]
)

country_aov = (
    country_aov
    .sort_values("Average Order Value", ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    country_aov,
    x="Country",
    y="Average Order Value",
    color="Average Order Value",
    title="Average Order Value by Country"
)

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, width="stretch")

# ==================================================
# GRAPH 3 : REVENUE PER CUSTOMER
# ==================================================

customer_value = (
    df.groupby("Country")
      .agg(
          Revenue=("Revenue", "sum"),
          Customers=("Customer ID", "nunique")
      )
)

customer_value["Revenue per Customer"] = (
    customer_value["Revenue"] /
    customer_value["Customers"]
)

customer_value = (
    customer_value
    .sort_values("Revenue per Customer", ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    customer_value,
    x="Country",
    y="Revenue per Customer",
    color="Revenue per Customer",
    title="Revenue per Customer by Country"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, width="stretch")

# ==================================================
# GRAPH 4 : WORLD MAP
# ==================================================

fig4 = px.choropleth(
    country_rev,
    locations="Country",
    locationmode="country names",
    color="Revenue",
    hover_name="Country",
    color_continuous_scale="Blues",
    title="Global Revenue Distribution"
)

fig4.update_layout(template="plotly_dark")

st.plotly_chart(fig4, width="stretch")

# ==================================================
# COUNTRY SUMMARY TABLE
# ==================================================

st.subheader("📋 Country Performance Summary")

table = (
    df.groupby("Country")
      .agg(
          Revenue=("Revenue", "sum"),
          Customers=("Customer ID", "nunique"),
          Orders=("Invoice", "nunique"),
          Quantity=("Quantity", "sum")
      )
      .sort_values("Revenue", ascending=False)
)

st.dataframe(table, width="stretch")

# ==================================================
# BUSINESS INSIGHTS
# ==================================================

highest_customer_value = customer_value.iloc[0]["Country"]
highest_aov = country_aov.iloc[0]["Country"]

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Revenue Country: **{top_country}**

💰 Revenue Generated: **£{top_revenue:,.0f}**

🛒 Highest Average Order Value: **{highest_aov}**

👥 Highest Revenue per Customer: **{highest_customer_value}**

🌍 Countries Served: **{countries}**
""")