import streamlit as st
import pandas as pd
from datetime import datetime
from utils.common import plot_investment_vs_return, format_inr
from utils.export import generate_csv_download, generate_pdf_report

def render():
    st.header("💰 Lumpsum Investment Calculator")

    # Inputs
    amount = st.number_input("Initial Investment (₹)", value=100000.0, min_value=1000.0)
    rate = st.slider("Annual Return Rate (%)", 5.0, 20.0, 10.0)
    years = st.slider("Investment Duration (Years)", 1, 50, 10)

    future_value = amount * ((1 + rate / 100) ** years)
    total_gain = future_value - amount

    st.success(f"Future Value: {format_inr(future_value)}")
    st.info(f"Total Gain: {format_inr(total_gain)}")

    # Data for graph
    dates = [datetime.today().replace(day=1) + pd.DateOffset(years=i) for i in range(years + 1)]
    investment = [amount] * (years + 1)
    returns = [amount * ((1 + rate / 100) ** i) for i in range(years + 1)]

    df = pd.DataFrame({"Date": dates, "Investment": investment, "Returns": returns})
    plot_investment_vs_return(df)

    # 🧾 Export Options
    st.markdown("### 📤 Export Options")
    generate_csv_download(df, filename="lumpsum_growth_schedule.csv")

    summary = {
        "Investment Amount": format_inr(amount),
        "Return Rate": f"{rate}%",
        "Duration": f"{years} years",
        "Future Value": format_inr(future_value)
    }
    generate_pdf_report(summary, filename="lumpsum_summary.pdf")
