import pandas as pd
from fpdf import FPDF
import base64
import streamlit as st
import os

def generate_csv_download(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f"📥 [Download CSV](data:file/csv;base64,{b64})", unsafe_allow_html=True)

def generate_pdf_report(data_dict, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in data_dict.items():
        # Replace ₹ with Rs. to avoid Unicode errors
        if isinstance(value, str):
            value = value.replace("₹", "Rs.")
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output(filename)

    with open(filename, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)

    # Clean up file after use
    try:
        os.remove(filename)
    except:
        pass
