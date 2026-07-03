import streamlit as st
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NeuralRetail",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main{
    background:#0B1220;
}

.block-container{
    padding-top:3rem;
    padding-left:3rem;
    padding-right:3rem;
    padding-bottom:3rem;
}

.big-font{
    font-size:56px;
    font-weight:800;
    color:#F8FAFC;
    letter-spacing:0.5px;
}

.subtitle{
    font-size:21px;
    color:#94A3B8;
    margin-top:-15px;
    margin-bottom:30px;
}

.info-box{
    background:linear-gradient(135deg,#172554,#1E3A8A);
    padding:30px;
    border-radius:18px;
    border-left:6px solid #60A5FA;
    color:white;
    box-shadow:0 12px 35px rgba(0,0,0,.35);
    margin-bottom:30px;
}

.feature-box{
    background:#111C2F;
    border:1px solid #23395B;
    border-radius:18px;
    padding:28px;
    height:270px;
    transition:.35s;
    box-shadow:0px 8px 20px rgba(0,0,0,.25);
}

.feature-box:hover{
    transform:translateY(-8px);
    border:1px solid #3B82F6;
    box-shadow:0px 15px 35px rgba(59,130,246,.35);
}

.metric-card{
    background:#132238;
    border-radius:18px;
    padding:22px;
    text-align:center;
    border:1px solid #1D4ED8;
}

.section-title{
    color:#60A5FA;
    font-size:28px;
    font-weight:bold;
    margin-bottom:15px;
}

.footer{
    text-align:center;
    color:#94A3B8;
    margin-top:70px;
    padding:20px;
}

hr{
    border:1px solid #1E293B;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🛒NeuralRetail ")
st.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.caption("NeuralRetail v1.0")
# --------------------------------------------------
# Home Page
# --------------------------------------------------

st.markdown("""
<div style="margin-top:20px">

<p class="big-font">
🛒 NeuralRetail Analytics Platform
</p>

<p class="subtitle">
Business Intelligence • Machine Learning • Forecasting
</p>

</div>
""",unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div class="info-box">

<h2>📌 Executive Overview</h2>

<p style="font-size:18px">

NeuralRetail is an end-to-end Retail Business Intelligence platform designed
to transform transactional retail data into strategic business insights
through interactive dashboards, machine learning, customer analytics and
predictive forecasting.

</p>

</div>
""",unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# Features
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Analytics</h3>
        <p>✔ Executive Dashboard</p>
        <p>✔ Sales Performance</p>
        <p>✔ Product Performance</p>
        <p>✔ Customer Analytics</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 Machine Learning</h3>
        <p>✔ Customer Segmentation</p>
        <p>✔ Churn Prediction</p>
        <p>✔ Revenue Forecasting</p>
        <p>✔ Customer Lifetime Value</p>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📈 Business Intelligence</h3>
        <p>✔ Interactive Filters</p>
        <p>✔ Dynamic Visualizations</p>
        <p>✔ Executive Insights</p>
        <p>✔ Decision Support</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Technology Stack
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🛠 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

tech1.metric("Language", "Python 3.12")
tech2.metric("Framework", "Streamlit")
tech3.metric("ML", "Random Forest")
tech4.metric("Forecasting", "Prophet")

st.markdown("---")

# --------------------------------------------------
# Dashboards
# --------------------------------------------------

st.subheader("📑 Available Dashboards")

dashboards = [
    "📊 Executive Dashboard",
    "📈 Sales Performance Dashboard",
    "📦 Product Performance Dashboard",
    "👥 Customer Analytics Dashboard",
    "🌍 Country Analysis Dashboard",
    "📅 Revenue Forecast Dashboard",
    "🎯 Customer Segmentation Dashboard",
    "🔄 Customer Churn Dashboard",
    "📦 Inventory Analysis Dashboard",
    "🛒 Order Analysis Dashboard",
    "💎 Customer Lifetime Value Dashboard",
    "📋 Executive Business Summary"
]

for dashboard in dashboards:
    st.write("•", dashboard)

st.sidebar.markdown("---")

st.subheader("🚀 Platform Highlights")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Dashboards", "12")
c2.metric("ML Models", "3")
c3.metric("KPIs", "50+")
c4.metric("Visualizations", "80+") 

st.markdown("""
<div class="footer">

<b>NeuralRetail Analytics Platform</b><br>

Business Intelligence • Machine Learning • Forecasting

<br><br>

Developed using Python | Streamlit | Plotly | Scikit-learn | Prophet

</div>
""", unsafe_allow_html=True)