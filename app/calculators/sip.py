import streamlit as st
import pandas as pd
from datetime import datetime
from utils.common import plot_investment_vs_return, format_inr
from utils.export import generate_csv_download, generate_pdf_report

def render():
    st.header("📈 SIP Calculator")

    # Inputs
    monthly_investment = st.number_input("Monthly Investment (₹)", value=10000.0, min_value=500.0)
    years = st.slider("Investment Duration (Years)", 1, 40, 20)
    return_rate = st.slider("Expected Return Rate (p.a. %)", 5.0, 20.0, 12.0)

    months = years * 12
    monthly_rate = return_rate / 12 / 100

    # Future value calculation
    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate)) / monthly_rate
    total_invested = monthly_investment * months
    total_returns = future_value - total_invested

    # Outputs
    st.success(f"Future Value: {format_inr(future_value)}")
    st.info(f"Total Invested: {format_inr(total_invested)}") 
    st.info(f"Total Returns: {format_inr(total_returns)}")

    # Chart Data
    dates = [datetime.today().replace(day=1) + pd.DateOffset(months=i) for i in range(months + 1)]
    investment = [monthly_investment * i for i in range(months + 1)]
    returns = [
        monthly_investment * (((1 + monthly_rate) ** i - 1) * (1 + monthly_rate)) / monthly_rate
        for i in range(months + 1)
    ]

    df = pd.DataFrame({
        "Date": dates,
        "Investment": investment,
        "Returns": returns
    })

    plot_investment_vs_return(df)

    # 🧾 Export Options
    st.markdown("### 📤 Export Options")
    generate_csv_download(df, filename="sip_schedule.csv")

    summary = {
        "Monthly SIP": format_inr(monthly_investment),
        "Return Rate": f"{return_rate}%",
        "Duration": f"{years} years",
        "Future Value": format_inr(future_value)
    }
    generate_pdf_report(summary, filename="sip_summary.pdf")
