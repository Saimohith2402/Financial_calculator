import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.common import plot_investment_vs_return, format_inr
from utils.export import generate_csv_download, generate_pdf_report

def calculate_emi(P, r, n):
    monthly_rate = r / 12 / 100
    return P * monthly_rate * ((1 + monthly_rate) ** n) / (((1 + monthly_rate) ** n) - 1)

def calculate_principal(EMI, r, n):
    monthly_rate = r / 12 / 100
    return EMI * (((1 + monthly_rate) ** n) - 1) / (monthly_rate * ((1 + monthly_rate) ** n))

def calculate_tenure(P, EMI, r):
    monthly_rate = r / 12 / 100
    return np.log(EMI / (EMI - P * monthly_rate)) / np.log(1 + monthly_rate)

def calculate_interest_rate(P, EMI, n, tol=1e-6, max_iter=1000):
    low, high = 0.01, 100.0
    for _ in range(max_iter):
        mid = (low + high) / 2
        guess_emi = calculate_emi(P, mid, n)
        if abs(guess_emi - EMI) < tol:
            return mid
        elif guess_emi > EMI:
            high = mid
        else:
            low = mid
    return mid

def render():
    st.header("🏠 Home Loan EMI Calculator (4-Way Solver with Prepayment)")

    mode = st.selectbox("🧮 What do you want to calculate?", ["EMI", "Principal", "Interest Rate", "Tenure"])

    if mode == "EMI":
        loan_amt = st.number_input("Loan Amount (₹)", value=2500000.0, min_value=10000.0)
        interest_rate = st.slider("Interest Rate (p.a. %)", 5.0, 15.0, 8.5)
        tenure_years = st.slider("Tenure (Years)", 1, 30, 20)
        months = tenure_years * 12
        emi = calculate_emi(loan_amt, interest_rate, months)
        st.success(f"Monthly EMI: {format_inr(emi)}")

        # 🏦 Prepayment Options
        st.markdown("### 🏦 Prepayment Options")
        prepay_type = st.selectbox("Prepayment Frequency", ["None", "One-time", "Yearly", "Monthly"])

        prepay_amount = 0
        prepay_start_month = 0
        reduce_type = "Reduce Tenure"

        if prepay_type != "None":
            prepay_amount = st.number_input("Prepayment Amount (₹)", value=100000.0, min_value=1000.0)
            prepay_start_month = st.number_input("Start Prepayment After (in months)", value=12, min_value=1)
            reduce_type = st.radio("When you prepay, what should reduce?", ["Reduce Tenure", "Reduce EMI"])

        # Without prepayment total interest for comparison
        original_total_payment = emi * months

        # Amortization with Prepayment
        principal_remaining = loan_amt
        data = []
        month = 0
        total_interest_paid = 0

        while principal_remaining > 0 and month < 1000:
            month += 1
            interest = principal_remaining * (interest_rate / 1200)
            principal = emi - interest
            principal_remaining -= principal
            total_interest_paid += interest

            if prepay_type != "None" and month >= prepay_start_month:
                if prepay_type == "One-time" and month == prepay_start_month:
                    principal_remaining -= prepay_amount
                elif prepay_type == "Yearly" and (month - prepay_start_month) % 12 == 0:
                    principal_remaining -= prepay_amount
                elif prepay_type == "Monthly":
                    principal_remaining -= prepay_amount

                if reduce_type == "Reduce EMI":
                    remaining_months = max(1, months - month)
                    emi = calculate_emi(principal_remaining, interest_rate, remaining_months)

            if principal_remaining < 0:
                principal += principal_remaining
                principal_remaining = 0

            date = datetime.today().replace(day=1) + pd.DateOffset(months=month)
            data.append([date, emi * month, principal])

        df = pd.DataFrame(data, columns=["Date", "Total Paid", "Principal Paid"])
        df["Investment"] = df["Total Paid"] - df["Principal Paid"]
        df.rename(columns={"Principal Paid": "Returns"}, inplace=True)

        total_paid = df["Total Paid"].iloc[-1]
        total_months = len(df)

        # 📊 Chart
        plot_investment_vs_return(df)

        # 📌 Detailed Summary
        st.markdown("### 📌 Loan Summary")
        st.info(f"Actual Tenure: {total_months // 12} years {total_months % 12} months")
        st.info(f"Total Payment: {format_inr(total_paid)}")
        st.info(f"Total Interest Paid: {format_inr(total_interest_paid)}")
        st.info(f"Interest Saved vs No Prepayment: {format_inr(original_total_payment - total_paid)}")

        # 🧾 Export
        st.markdown("### 📤 Export Options")
        generate_csv_download(df, filename="home_loan_schedule.csv")

        summary = {
            "Loan Amount": format_inr(loan_amt),
            "Interest Rate": f"{interest_rate:.2f}%",
            "Original Tenure": f"{tenure_years} years",
            "Final Tenure": f"{total_months} months",
            "Monthly EMI": format_inr(emi),
            "Prepayment Type": prepay_type,
            "Prepayment Impact": reduce_type,
            "Interest Saved": format_inr(original_total_payment - total_paid)
        }
        generate_pdf_report(summary, filename="home_loan_summary.pdf")

    elif mode == "Principal":
        emi = st.number_input("Monthly EMI (₹)", value=25000.0, min_value=500.0)
        interest_rate = st.slider("Interest Rate (p.a. %)", 5.0, 15.0, 8.5)
        tenure_years = st.slider("Tenure (Years)", 1, 30, 20)
        months = tenure_years * 12
        principal = calculate_principal(emi, interest_rate, months)
        st.success(f"Loan Amount: {format_inr(principal)}")

    elif mode == "Interest Rate":
        emi = st.number_input("Monthly EMI (₹)", value=25000.0, min_value=500.0)
        principal = st.number_input("Loan Amount (₹)", value=2500000.0, min_value=10000.0)
        tenure_years = st.slider("Tenure (Years)", 1, 30, 20)
        months = tenure_years * 12
        rate = calculate_interest_rate(principal, emi, months)
        st.success(f"Estimated Interest Rate: {rate:.2f}%")

    elif mode == "Tenure":
        emi = st.number_input("Monthly EMI (₹)", value=25000.0, min_value=500.0)
        principal = st.number_input("Loan Amount (₹)", value=2500000.0, min_value=10000.0)
        interest_rate = st.slider("Interest Rate (p.a. %)", 5.0, 15.0, 8.5)
        months = int(np.ceil(calculate_tenure(principal, emi, interest_rate)))
        years = months // 12
        rem_months = months % 12
        st.success(f"Tenure: {years} years {rem_months} months")