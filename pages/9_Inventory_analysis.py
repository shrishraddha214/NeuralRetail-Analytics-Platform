import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Inventory Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Analysis Dashboard")

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
# KPIs
# --------------------------------------------------

total_products = df["StockCode"].nunique()
total_quantity = df["Quantity"].sum()
total_revenue = df["Revenue"].sum()

high_risk = len(df[df["Inventory_Risk"] == "High"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Products", f"{total_products:,}")
c2.metric("🛒 Quantity Sold", f"{total_quantity:,}")
c3.metric("💰 Revenue", f"£{total_revenue:,.0f}")
c4.metric("⚠️ High Risk Products", high_risk)

st.divider()

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

left, right = st.columns(2)

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig1 = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h",
    color="Revenue",
    title="Top 10 Products by Revenue"
)

fig1.update_layout(template="plotly_dark")

with left:
    st.plotly_chart(fig1, width="stretch")

# --------------------------------------------------
# INVENTORY RISK
# --------------------------------------------------

risk = (
    df.groupby("Inventory_Risk")["StockCode"]
    .nunique()
    .reset_index(name="Products")
)

fig2 = px.pie(
    risk,
    names="Inventory_Risk",
    values="Products",
    hole=0.45,
    title="Inventory Risk Distribution"
)

fig2.update_layout(template="plotly_dark")

with right:
    st.plotly_chart(fig2, width="stretch")

# --------------------------------------------------
# QUANTITY SOLD
# --------------------------------------------------

qty = (
    df.groupby("Description")["Quantity"]
    .sum()
    .reset_index()
    .sort_values("Quantity", ascending=False)
    .head(15)
)

fig3 = px.bar(
    qty,
    x="Description",
    y="Quantity",
    color="Quantity",
    title="Top Products by Quantity Sold"
)

fig3.update_layout(
    template="plotly_dark",
    xaxis_tickangle=-45
)

st.plotly_chart(fig3, width="stretch")

# --------------------------------------------------
# ORDER SIZE
# --------------------------------------------------

pareto = (
    df.groupby("StockCode")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

pareto["Cumulative %"] = (
    pareto["Revenue"].cumsum()
    / pareto["Revenue"].sum()
) * 100

fig = go.Figure() 

fig.add_bar(
    x=pareto["StockCode"],
    y=pareto["Revenue"],
    name="Revenue"
)

fig.add_scatter(
    x=pareto["StockCode"],
    y=pareto["Cumulative %"],
    mode="lines+markers",
    yaxis="y2",
    name="Cumulative %"
)

fig.update_layout(
    title="Pareto Analysis of Top Products",
    template="plotly_dark",
    yaxis2=dict(
        overlaying="y",
        side="right",
        range=[0, 100]
    ),
    height=500
)

st.plotly_chart(fig, width="stretch")
# --------------------------------------------------
# INVENTORY TABLE
# --------------------------------------------------

st.subheader("📋 Product Performance")

table = (
    df.groupby(["StockCode", "Description"])
    .agg(
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Risk=("Inventory_Risk", "first")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

st.dataframe(
    table,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

best_product = top_products.iloc[0]["Description"]

st.subheader("💡 Business Insights")

st.success(f"""
🏆 Highest Revenue Product: **{best_product}**

📦 Total Products: **{total_products:,}**

💰 Total Revenue: **£{total_revenue:,.0f}**

⚠️ High Inventory Risk Products: **{high_risk}**

### Recommendations

✔ Monitor products marked as High Risk.

✔ Increase stock for best-selling products.

✔ Review slow-moving inventory regularly.

✔ Optimize inventory based on sales trends.
""")