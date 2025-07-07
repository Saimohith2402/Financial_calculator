import streamlit as st
import plotly.graph_objects as go

def set_page_config():
    st.set_page_config(page_title="Finance Calculator", layout="wide")

def calculate_emi(P, R, N):
    """
    Calculate EMI using:
    EMI = [P * r * (1 + r)^N] / [(1 + r)^N – 1]
    where r = annual interest / 12 / 100
    """
    r = R / (12 * 100)
    emi = P * r * ((1 + r) ** N) / (((1 + r) ** N) - 1)
    return emi

def plot_investment_vs_return(df, investment_label="Investment", return_label="Returns"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df[investment_label], name=investment_label, line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df[return_label], name=return_label, line=dict(color='green')))
    fig.update_layout(title="Time vs Money", xaxis_title="Date", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)
import locale

def format_inr(amount):
    """Format a number in Indian comma style with ₹ sign"""
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
    except:
        # fallback for Windows
        locale.setlocale(locale.LC_ALL, '')
    return f"₹{locale.format_string('%d', amount, grouping=True)}"
