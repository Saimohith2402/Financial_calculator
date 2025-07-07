import streamlit as st
import pandas as pd
import numpy as np
from utils.export import generate_csv_download, generate_pdf_report
from utils.common import format_inr

def future_value_sip(pmt, rate, n):
    r = rate / 100 / 12
    return pmt * (((1 + r) ** n - 1) / r) * (1 + r)

def render():
    st.header("📉 Inflation-Adjusted SIP Returns")

    monthly_investment = st.number_input("💸 Monthly SIP Investment (₹)", value=5000.0, min_value=100.0)
    annual_return = st.slider("📈 Expected Return (% p.a.)", 5.0, 20.0, 12.0)
    inflation_rate = st.slider("🔥 Expected Inflation (% p.a.)", 2.0, 10.0, 6.0)
    years = st.slider("📅 Investment Duration (Years)", 1, 40, 20)

    months = years * 12

    # Nominal future value
    nominal_fv = future_value_sip(monthly_investment, annual_return, months)

    # Inflation-adjusted FV
    real_rate = ((1 + annual_return / 100) / (1 + inflation_rate / 100)) - 1
    real_rate_percent = real_rate * 100
    real_fv = future_value_sip(monthly_investment, real_rate_percent, months)

    st.success(f"📈 Nominal Future Value: {format_inr(nominal_fv)}")
    st.success(f"🔥 Inflation-adjusted (Real) Future Value: {format_inr(real_fv)}")

    # Yearly data for plotting
    df = pd.DataFrame({
        "Year": list(range(1, years + 1)),
        "Nominal Value": [future_value_sip(monthly_investment, annual_return, y * 12) for y in range(1, years + 1)],
        "Real Value": [future_value_sip(monthly_investment, real_rate_percent, y * 12) for y in range(1, years + 1)]
    })
    st.line_chart(df.set_index("Year"))

    # Export
    st.markdown("### 📤 Export Options")
    generate_csv_download(df, filename="sip_inflation_adjusted.csv")

    summary = {
        "Monthly Investment": format_inr(monthly_investment),
        "Expected Return": f"{annual_return:.2f}%",
        "Inflation Rate": f"{inflation_rate:.2f}%",
        "Duration": f"{years} years",
        "Nominal Future Value": format_inr(nominal_fv),
        "Real Future Value": format_inr(real_fv)
    }
    generate_pdf_report(summary, filename="sip_inflation_summary.pdf")
