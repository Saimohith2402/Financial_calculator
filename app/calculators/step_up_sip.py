import streamlit as st
import pandas as pd
from datetime import datetime
from utils.common import plot_investment_vs_return, format_inr
from utils.export import generate_csv_download, generate_pdf_report

def render():
    st.header("📈 Step-up SIP Calculator")

    # Inputs
    monthly_investment = st.number_input("Initial Monthly Investment (₹)", value=10000.0, min_value=500.0)
    step_up_percent = st.slider("Annual Step-up (%)", 0, 100, 10)
    years = st.slider("Investment Duration (Years)", 1, 40, 20)
    return_rate = st.slider("Expected Return Rate (p.a. %)", 5.0, 20.0, 12.0)

    months = years * 12
    monthly_rate = return_rate / 12 / 100
    current_sip = monthly_investment

    total_invested = 0
    future_value = 0
    investment = []
    returns = []
    dates = []

    for i in range(months):
        if i % 12 == 0 and i > 0:
            current_sip *= (1 + step_up_percent / 100)

        total_invested += current_sip
        future_value = future_value * (1 + monthly_rate) + current_sip

        dates.append(datetime.today().replace(day=1) + pd.DateOffset(months=i))
        investment.append(total_invested)
        returns.append(future_value)

    st.success(f"Future Value: {format_inr(future_value)}")
    st.info(f"Total Invested: {format_inr(total_invested)}")
    st.info(f"Total Returns: {format_inr(future_value - total_invested)}")

    df = pd.DataFrame({"Date": dates, "Investment": investment, "Returns": returns})
    plot_investment_vs_return(df)

    # 🧾 Export Options
    st.markdown("### 📤 Export Options")
    generate_csv_download(df, filename="stepup_sip_schedule.csv")

    summary = {
        "Initial SIP": format_inr(monthly_investment),
        "Step-up": f"{step_up_percent}% annually",
        "Duration": f"{years} years",
        "Expected Return": f"{return_rate}%",
        "Future Value": format_inr(future_value)
    }
    generate_pdf_report(summary, filename="stepup_sip_summary.pdf")
