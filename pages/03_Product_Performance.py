import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Product Performance",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Performance Dashboard")

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
# PRECOMPUTED PRODUCT METRICS (IMPORTANT FIX)
# --------------------------------------------------
@st.cache_data
def product_metrics(data):
    return (
        data.groupby("Description")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Price=("Price", "mean"),
            Products=("StockCode", "nunique")
        )
        .reset_index()
    )

prod_df = product_metrics(df)

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_products = df["StockCode"].nunique()
total_revenue = prod_df["Revenue"].sum()
total_quantity = prod_df["Quantity"].sum()

best_product_revenue = prod_df.loc[prod_df["Revenue"].idxmax(), "Description"]
best_product_quantity = prod_df.loc[prod_df["Quantity"].idxmax(), "Description"]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Products", f"{total_products:,}")
c2.metric("💰 Revenue", f"£{total_revenue:,.0f}")
c3.metric("🛒 Quantity Sold", f"{int(total_quantity):,}")
c4.metric("🏆 Top Product", best_product_revenue[:30])

st.divider()

# --------------------------------------------------
# TOP PRODUCTS BY REVENUE
# --------------------------------------------------
top_rev = prod_df.sort_values("Revenue", ascending=False).head(10)

fig1 = px.bar(
    top_rev,
    x="Revenue",
    y="Description",
    orientation="h",
    color="Revenue",
    title="Top 10 Products by Revenue",
    hover_data=["Quantity", "Price"]
)

fig1.update_layout(
    template="plotly_dark",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# TOP PRODUCTS BY QUANTITY
# --------------------------------------------------
top_qty = prod_df.sort_values("Quantity", ascending=False).head(10)

fig2 = px.bar(
    top_qty,
    x="Quantity",
    y="Description",
    orientation="h",
    color="Quantity",
    title="Top 10 Products by Quantity Sold",
    hover_data=["Revenue", "Price"]
)

fig2.update_layout(
    template="plotly_dark",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# REVENUE SHARE (DONUT)
# --------------------------------------------------
fig3 = px.pie(
    top_rev,
    names="Description",
    values="Revenue",
    hole=0.55,
    title="Revenue Share of Top 10 Products"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# PRICE DISTRIBUTION
# --------------------------------------------------
fig4 = px.histogram(
    df,
    x="Price",
    nbins=40,
    title="Product Price Distribution"
)

fig4.update_layout(template="plotly_dark")

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# PRODUCT TABLE
# --------------------------------------------------
st.subheader("📋 Top Products Table")

st.dataframe(
    prod_df.sort_values("Revenue", ascending=False).head(15),
    use_container_width=True
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------
st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Revenue Product: **{best_product_revenue}**

🛒 Highest Quantity Product: **{best_product_quantity}**

💰 Total Revenue: **£{total_revenue:,.0f}**

📦 Total Products: **{total_products:,}**
""")