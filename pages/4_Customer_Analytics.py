import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analytics Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\91895\OneDrive\Desktop\NeuralRetail\data\processed\dashboard_dataset.csv")

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

df = df[
    (df["Country"].isin(country)) &
    (df["Segment"].isin(segment))
]

# --------------------------------------------------
# PRECOMPUTED CUSTOMER METRICS (OPTIMIZED)
# --------------------------------------------------
@st.cache_data
def customer_metrics(data):
    return (
        data.groupby("Customer ID")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

cust_df = customer_metrics(df)

# KPIs
customers = cust_df["Customer ID"].nunique()
orders = df["Invoice"].nunique()

avg_order = cust_df["Revenue"].sum() / orders
avg_customer = cust_df["Revenue"].mean()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Customers", f"{customers:,}")
c2.metric("📦 Orders", f"{orders:,}")
c3.metric("💰 Avg Order Value", f"£{avg_order:,.2f}")
c4.metric("🛒 Avg Customer Spend", f"£{avg_customer:,.2f}")

st.divider()

# --------------------------------------------------
# TOP CUSTOMERS
# --------------------------------------------------
top_customers = cust_df.sort_values("Revenue", ascending=False).head(10)

fig1 = px.bar(
    top_customers,
    x="Revenue",
    y="Customer ID",
    orientation="h",
    color="Revenue",
    title="Top 10 Customers by Revenue",
    hover_data=["Orders", "Quantity"]
)

fig1.update_layout(
    template="plotly_dark",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# SEGMENT DISTRIBUTION
# --------------------------------------------------
segment_df = (
    df.groupby("Segment")["Customer ID"]
    .nunique()
    .reset_index(name="Customers")
)

fig2 = px.pie(
    segment_df,
    names="Segment",
    values="Customers",
    hole=0.55,
    title="Customer Segment Distribution"
)

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# CUSTOMER SPENDING DISTRIBUTION
# --------------------------------------------------
fig3 = px.histogram(
    cust_df,
    x="Revenue",
    nbins=40,
    title="Customer Spending Distribution"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# TOP CUSTOMERS TABLE
# --------------------------------------------------
st.subheader("📋 Top Customers Table")

st.dataframe(
    top_customers,
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------
best_customer = top_customers.iloc[0]["Customer ID"]

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Spending Customer: **{best_customer}**

👥 Total Customers: **{customers:,}**

📦 Total Orders: **{orders:,}**

💰 Avg Order Value: **£{avg_order:,.2f}**

🛒 Avg Customer Spend: **£{avg_customer:,.2f}**
""")