import streamlit as st
import pandas as pd
import numpy as np
from utils.export import generate_csv_download, generate_pdf_report
from utils.common import format_inr

def future_value(pmt, rate, n):
    r = rate / 100
    return pmt * (((1 + r) ** n - 1) / r)

def corpus_needed(expense, inflation, years):
    adjusted_expense = expense * ((1 + inflation / 100) ** years)
    return adjusted_expense * 12 * 30  # 30x rule

def render():
    st.header("🧓 Retirement Planner & FIRE Estimator")

    current_age = st.slider("🎂 Current Age", 18, 60, 25)
    retirement_age = st.slider("🏁 Retirement Age", current_age + 1, 75, 60)
    expense = st.number_input("💸 Current Monthly Expenses (₹)", value=30000.0, min_value=1000.0)
    inflation = st.slider("📈 Expected Inflation Rate (%)", 4.0, 12.0, 6.0)
    returns = st.slider("📉 Expected Returns on Investment (%)", 5.0, 15.0, 10.0)
    post_retire_age = st.slider("🧓 Income Required Until Age", retirement_age + 1, 100, 85)

    years_to_retire = retirement_age - current_age
    years_post_retire = post_retire_age - retirement_age

    # 🔥 FIRE Corpus (Retire Today)
    fire_corpus = expense * 12 * 30

    # 🧮 Corpus at Retirement
    adjusted_expense = expense * ((1 + inflation / 100) ** years_to_retire)
    annual_exp = adjusted_expense * 12
    corpus_required = future_value(annual_exp, returns, years_post_retire)

    st.success(f"🔥 FIRE Corpus (If retiring today): {format_inr(fire_corpus)}")
    st.success(f"🎯 Corpus Needed at Retirement (Age {retirement_age}): {format_inr(corpus_required)}")

    # 📈 Plot Corpus Growth Over Years
    yearly_data = []
    for i in range(1, years_to_retire + 1):
        inflated_exp = expense * ((1 + inflation / 100) ** i)
        annual_exp = inflated_exp * 12
        corpus = future_value(annual_exp, returns, years_post_retire)
        yearly_data.append([current_age + i, corpus])

    df = pd.DataFrame(yearly_data, columns=["Age", "Corpus Required"])
    st.line_chart(df.set_index("Age"))

    # 📤 Export
    st.markdown("### 📤 Export Options")
    generate_csv_download(df, filename="retirement_projection.csv")

    summary = {
        "Current Age": current_age,
        "Retirement Age": retirement_age,
        "Monthly Expense Today": format_inr(expense),
        "Inflation Rate": f"{inflation:.2f}%",
        "Expected Returns": f"{returns:.2f}%",
        "Years to Retire": years_to_retire,
        "Corpus at Retirement": format_inr(corpus_required),
        "FIRE Corpus Today": format_inr(fire_corpus)
    }
    generate_pdf_report(summary, filename="retirement_summary.pdf")
