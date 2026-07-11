import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Order Analysis",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Order Analysis Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/processed/dashboard_dataset.csv"
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

df["Order_Size"] = (
    df["Order_Size"]
    .fillna("Unknown")
    .astype(str)
)

order_order = ["Small", "Medium", "Large", "Unknown"]

available = [x for x in order_order if x in df["Order_Size"].unique()]

order = st.sidebar.multiselect(
    "Order Size",
    options=available,
    default=available
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["Order_Size"].isin(order)) &
    (df["Country"].isin(country))
]

if filtered_df.empty:
    st.warning("No records found.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total_orders = filtered_df["Invoice"].nunique()
total_revenue = filtered_df["Revenue"].sum()
avg_order = total_revenue / total_orders
customers = filtered_df["Customer ID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🧾 Orders", f"{total_orders:,}")
c2.metric("💰 Revenue", f"£{total_revenue:,.0f}")
c3.metric("📦 Avg Order Value", f"£{avg_order:,.0f}")
c4.metric("👥 Customers", f"{customers:,}")

st.divider()

# --------------------------------------------------
# HISTOGRAM
# --------------------------------------------------

st.subheader("📊 Order Value Distribution")

invoice_value = (
    filtered_df.groupby("Invoice")["Revenue"]
    .sum()
    .reset_index()
)

fig1 = px.histogram(
    invoice_value,
    x="Revenue",
    nbins=40,
    color_discrete_sequence=["royalblue"],
    title="Distribution of Order Values"
)

fig1.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig1, width="stretch")

# --------------------------------------------------
# BOX PLOT + WEEKDAY TREND
# --------------------------------------------------

left, right = st.columns(2)

with left:

    fig2 = px.box(
        filtered_df,
        x="Order_Size",
        y="Revenue",
        color="Order_Size",
        title="Revenue by Order Size"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig2, width="stretch")

with right:

    weekday = (
        filtered_df.groupby("Weekday")["Invoice"]
        .nunique()
        .reset_index(name="Orders")
    )

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday["Weekday"] = pd.Categorical(
        weekday["Weekday"],
        categories=weekday_order,
        ordered=True
    )

    weekday = weekday.sort_values("Weekday")

    fig3 = px.line(
        weekday,
        x="Weekday",
        y="Orders",
        markers=True,
        title="Weekly Order Trend"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig3, width="stretch")

st.divider()

# --------------------------------------------------
# TOP ORDERS
# --------------------------------------------------

st.subheader("🏆 Top 10 Highest Value Orders")

top_orders = (
    filtered_df.groupby("Invoice")
    .agg(
        Revenue=("Revenue","sum"),
        Customer=("Customer ID","first"),
        Country=("Country","first")
    )
    .sort_values("Revenue",ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(
    top_orders,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# ORDER SIZE ANALYSIS
# --------------------------------------------------

st.subheader("📦 Order Size Contribution")

size = (
    filtered_df.groupby("Order_Size")
    .agg(
        Orders=("Invoice","nunique"),
        Revenue=("Revenue","sum")
    )
    .reset_index()
)

fig4 = px.funnel(
    size,
    x="Revenue",
    y="Order_Size",
    color="Order_Size",
    title="Revenue Contribution by Order Size"
)

fig4.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig4, width="stretch")

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

highest_size = (
    size.sort_values("Revenue",ascending=False)
    .iloc[0]["Order_Size"]
)

highest_day = (
    weekday.sort_values("Orders",ascending=False)
    .iloc[0]["Weekday"]
)

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Revenue Order Size: **{highest_size}**

📅 Busiest Weekday: **{highest_day}**

🧾 Total Orders: **{total_orders:,}**

💰 Total Revenue: **£{total_revenue:,.0f}**

### Recommendations

• Focus promotions on the highest-performing order size.

• Optimize staffing during peak weekdays.

• Encourage customers with smaller baskets to increase average order value.

• Monitor high-value orders for customer retention opportunities.
""")