import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Sales Trend",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Trend Analysis")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\91895\OneDrive\Desktop\NeuralRetail\data\processed\dashboard_dataset.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filters")

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

df = df[
    (df["Country"].isin(country)) &
    (df["Year"].isin(year))
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("💰 Revenue", f"£{df['Revenue'].sum():,.0f}")
c2.metric("📦 Orders", f"{df['Invoice'].nunique():,}")
c3.metric("🛒 Quantity Sold", f"{int(df['Quantity'].sum()):,}")

st.divider()

# --------------------------------------------------
# Daily Revenue Trend
# --------------------------------------------------
daily = (
    df.groupby("InvoiceDate")["Revenue"]
    .sum()
    .reset_index()
)

fig_daily = px.line(
    daily,
    x="InvoiceDate",
    y="Revenue",
    title="Daily Revenue Trend",
    markers=True
)

fig_daily.update_layout(template="plotly_dark")

st.plotly_chart(fig_daily, width="stretch")

# --------------------------------------------------
# Monthly Revenue
# --------------------------------------------------
monthly = (
    df.groupby("Month_Name")["Revenue"]
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

fig_month = px.bar(
    monthly,
    x="Month_Name",
    y="Revenue",
    color="Revenue",
    title="Monthly Revenue"
)

fig_month.update_layout(template="plotly_dark")

st.plotly_chart(fig_month, width="stretch")

# --------------------------------------------------
# Revenue by Weekday
# --------------------------------------------------
weekday = (
    df.groupby("Weekday")["Revenue"]
    .sum()
    .reset_index()
)

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday["Day_Name"] = pd.Categorical(
    weekday["Weekday"],
    categories=day_order,
    ordered=True
)

weekday = weekday.sort_values("Day_Name")

fig_day = px.bar(
    weekday,
    x="Day_Name",
    y="Revenue",
    color="Revenue",
    title="Revenue by Weekday"
)

fig_day.update_layout(template="plotly_dark")

st.plotly_chart(fig_day, width="stretch")

# --------------------------------------------------
# Business Insights
# --------------------------------------------------
best_month = monthly.loc[monthly["Revenue"].idxmax(), "Month_Name"]
best_day = weekday.loc[weekday["Revenue"].idxmax(), "Day_Name"]

st.subheader("💡 Insights")

st.success(f"""
- Highest Revenue Month: **{best_month}**
- Highest Revenue Day: **{best_day}**
- Total Revenue: **£{df['Revenue'].sum():,.0f}**
- Total Orders: **{df['Invoice'].nunique():,}**
""")