# calculators/loan_comparison.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

def render():
    st.header("📊 Loan Comparison Tool")

    st.write("Compare multiple loans side by side (EMI, total interest, total payment).")

    num_loans = st.number_input("Number of Loans to Compare", min_value=2, max_value=5, value=2)

    loans = []
    for i in range(num_loans):
        st.subheader(f"Loan {i+1}")
        principal = st.number_input(f"Principal (Loan {i+1})", min_value=1000, value=500000, step=1000, key=f"p{i}")
        annual_rate = st.number_input(f"Interest Rate % (Loan {i+1})", min_value=1.0, max_value=50.0, value=8.0, step=0.1, key=f"r{i}")
        years = st.number_input(f"Tenure (Years, Loan {i+1})", min_value=1, max_value=40, value=20, key=f"t{i}")

        monthly_rate = annual_rate / 12 / 100
        months = years * 12
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total_payment = emi * months
        total_interest = total_payment - principal

        loans.append({
            "Loan": f"Loan {i+1}",
            "Principal": principal,
            "Rate (%)": annual_rate,
            "Tenure (Years)": years,
            "EMI": round(emi, 2),
            "Total Payment": round(total_payment, 2),
            "Total Interest": round(total_interest, 2),
        })

    df = pd.DataFrame(loans)
    st.subheader("📑 Comparison Table")
    st.dataframe(df)

    # ------------------ CSV Export ------------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="loan_comparison.csv",
        mime="text/csv",
    )

    # ------------------ PDF Export ------------------
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    style = getSampleStyleSheet()["Normal"]

    # Convert DataFrame to table for PDF
    data_for_pdf = [df.columns.tolist()] + df.values.tolist()
    table = Table(data_for_pdf)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(Paragraph("Loan Comparison Report", getSampleStyleSheet()["Title"]))
    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    st.download_button(
        label="📄 Download as PDF",
        data=pdf,
        file_name="loan_comparison.pdf",
        mime="application/pdf",
    )

    # ------------------ Chart ------------------
    st.subheader("📉 Total Payment vs Interest")
    fig, ax = plt.subplots()
    df.set_index("Loan")[["Principal", "Total Interest"]].plot(kind="bar", stacked=True, ax=ax)
    plt.ylabel("Amount (₹)")
    plt.title("Principal vs Interest")
    st.pyplot(fig)
