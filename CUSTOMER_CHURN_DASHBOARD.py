
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

session = get_active_session()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220 0%, #101b30 50%, #101827 100%);
    color: #f1f5f9;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background-color: #0b1324;
    border-right: 1px solid #26354d;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label {
    color: #cbd5e1;
}

.metric-card {
    background: linear-gradient(145deg, #182740, #111d32);
    border: 1px solid #2b4262;
    border-radius: 18px;
    padding: 22px 24px;
    min-height: 145px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
}

.metric-label {
    color: #a9bad2;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 12px;
}

.metric-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: 750;
    letter-spacing: -1px;
}

.metric-note {
    color: #7dd3fc;
    font-size: 12px;
    margin-top: 8px;
}

.section-card {
    background: #111e32;
    border: 1px solid #263954;
    border-radius: 18px;
    padding: 22px;
    margin-top: 14px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #263954;
    border-radius: 12px;
    overflow: hidden;
}

.stButton button {
    background: #2563eb;
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 600;
}

.stButton button:hover {
    background: #3b82f6;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 10px 0 20px 0;">
    <div style="color:#7dd3fc; font-size:13px; font-weight:700;
                letter-spacing:2px;">
        CUSTOMER INTELLIGENCE • SNOWFLAKE ML
    </div>
    <h1 style="font-size:38px; margin:8px 0;">
        Customer Churn Analytics
    </h1>
    <p style="font-size:16px; color:#a9bad2;">
        Predict customer churn, understand risk patterns, and identify
        customers who may need attention.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 📊 Dashboard")
st.sidebar.caption("Customer Churn Prediction")
st.sidebar.divider()
st.sidebar.markdown("### Risk Threshold")
risk_threshold = st.sidebar.slider(
    "High-risk probability (%)",
    min_value=50,
    max_value=95,
    value=70,
    step=5
) / 100

st.sidebar.info(
    "Customers at or above this probability are displayed as high risk."
)

summary = session.sql("""
    SELECT
        COUNT(*) AS TOTAL_CUSTOMERS,
        SUM(PREDICTED_CHURN) AS PREDICTED_CHURN,
        SUM(
            CASE WHEN CHURN_PROBABILITY >= 0.70 THEN 1 ELSE 0 END
        ) AS HIGH_RISK_CUSTOMERS,
        ROUND(AVG(CHURN_PROBABILITY) * 100, 2) AS AVG_CHURN_RISK
    FROM CHURN_DB.CUSTOMER_DATA.ALL_CUSTOMER_PREDICTIONS
""").to_pandas()

total_customers = int(summary.iloc[0]["TOTAL_CUSTOMERS"] or 0)
predicted_churn = int(summary.iloc[0]["PREDICTED_CHURN"] or 0)
high_risk = int(summary.iloc[0]["HIGH_RISK_CUSTOMERS"] or 0)
avg_risk = float(summary.iloc[0]["AVG_CHURN_RISK"] or 0)

st.markdown("### Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👥 TOTAL CUSTOMERS</div>
        <div class="metric-value">{total_customers:,}</div>
        <div class="metric-note">Customers analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📉 PREDICTED CHURN</div>
        <div class="metric-value">{predicted_churn:,}</div>
        <div class="metric-note">Model-predicted churn</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚠️ HIGH-RISK CUSTOMERS</div>
        <div class="metric-value">{high_risk:,}</div>
        <div class="metric-note">Risk probability ≥ 70%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 AVERAGE CHURN RISK</div>
        <div class="metric-value">{avg_risk:.2f}%</div>
        <div class="metric-note">Average predicted probability</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("## Customer Risk Insights")

contract_data = session.sql("""
    SELECT
        D.CONTRACT,
        COUNT(*) AS TOTAL_CUSTOMERS,
        SUM(P.PREDICTED_CHURN) AS PREDICTED_CHURN,
        SUM(
            CASE WHEN P.CHURN_PROBABILITY >= 0.70 THEN 1 ELSE 0 END
        ) AS HIGH_RISK_CUSTOMERS,
        ROUND(AVG(P.CHURN_PROBABILITY) * 100, 2) AS AVG_CHURN_RISK
    FROM CHURN_DB.CUSTOMER_DATA.ALL_CUSTOMER_PREDICTIONS P
    JOIN CHURN_DB.CUSTOMER_DATA.CHURN_CLEAN D
        ON P.CUSTOMERID = D.CUSTOMERID
    GROUP BY D.CONTRACT
    ORDER BY HIGH_RISK_CUSTOMERS DESC
""").to_pandas()

payment_data = session.sql("""
    SELECT
        D.PAYMENTMETHOD,
        COUNT(*) AS TOTAL_CUSTOMERS,
        SUM(P.PREDICTED_CHURN) AS PREDICTED_CHURN,
        SUM(
            CASE WHEN P.CHURN_PROBABILITY >= 0.70 THEN 1 ELSE 0 END
        ) AS HIGH_RISK_CUSTOMERS,
        ROUND(AVG(P.CHURN_PROBABILITY) * 100, 2) AS AVG_CHURN_RISK
    FROM CHURN_DB.CUSTOMER_DATA.ALL_CUSTOMER_PREDICTIONS P
    JOIN CHURN_DB.CUSTOMER_DATA.CHURN_CLEAN D
        ON P.CUSTOMERID = D.CUSTOMERID
    GROUP BY D.PAYMENTMETHOD
    ORDER BY HIGH_RISK_CUSTOMERS DESC
""").to_pandas()

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Churn Risk by Contract")
    st.caption("Compare high-risk customers across contract types.")
    st.bar_chart(
        contract_data.set_index("CONTRACT")["HIGH_RISK_CUSTOMERS"],
        color="#38bdf8"
    )
    st.dataframe(
        contract_data,
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with chart2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 💳 Churn Risk by Payment Method")
    st.caption("Compare predicted high-risk customers by payment method.")
    st.bar_chart(
        payment_data.set_index("PAYMENTMETHOD")["HIGH_RISK_CUSTOMERS"],
        color="#818cf8"
    )
    st.dataframe(
        payment_data,
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown("## 🚨 High-Risk Customer Explorer")
st.caption(
    "Search and review customers whose predicted churn probability "
    "meets the selected risk threshold."
)

high_risk_data = session.sql(f"""
    SELECT
        CUSTOMERID,
        ACTUAL_CHURN,
        PREDICTED_CHURN,
        ROUND(CHURN_PROBABILITY * 100, 2) AS CHURN_RISK_PERCENT
    FROM CHURN_DB.CUSTOMER_DATA.ALL_CUSTOMER_PREDICTIONS
    WHERE CHURN_PROBABILITY >= {risk_threshold}
    ORDER BY CHURN_PROBABILITY DESC
""").to_pandas()

search_customer = st.text_input(
    "🔍 Search by Customer ID",
    placeholder="Enter a customer ID..."
)

if search_customer:
    high_risk_data = high_risk_data[
        high_risk_data["CUSTOMERID"].astype(str).str.contains(
            search_customer, case=False, na=False
        )
    ]

st.markdown(
    f"**{len(high_risk_data):,} customers** match the selected risk threshold."
)

st.dataframe(
    high_risk_data,
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div style="text-align:center; color:#718096; font-size:12px;
            padding-top:25px;">
    CUSTOMER CHURN PREDICTION • POWERED BY SNOWFLAKE
    <br>
    Predictions are estimates and do not guarantee future customer churn.
</div>
""", unsafe_allow_html=True)
