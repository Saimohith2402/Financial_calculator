# app/main.py
import streamlit as st
from calculators import home_loan_emi, sip, step_up_sip, lumpsum_investment, loan_comparision
from ml_tools import inflation_forecast, retirement_planner, inflation_adjusted_sip
from utils.common import set_page_config
from utils import export  

# Configure page
set_page_config()

# Custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f1f5f9;
    }
    .banner {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.07);
        padding: 1.2rem;
        border-radius: 18px;
        box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.15);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        transition: transform 0.25s ease, border 0.25s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
    }
    .card-emoji {
        font-size: 1.9rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        transition: text-shadow 0.3s ease-in-out;
    }
    .glow {
        text-shadow: 0 0 12px #38bdf8, 0 0 20px #4ade80;
        animation: pulse 0.8s ease-out;
    }
    @keyframes pulse {
        0% { text-shadow: 0 0 0px #38bdf8; }
        50% { text-shadow: 0 0 20px #38bdf8, 0 0 30px #4ade80; }
        100% { text-shadow: 0 0 0px #38bdf8; }
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #f8fafc;
    }
    .launch-btn button, .back-btn button {
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        color: black !important;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='banner'>💼 All-in-One Finance Calculator</div>", unsafe_allow_html=True)

if "active_tool" not in st.session_state:
    st.session_state.active_tool = None
if "clicked_icon" not in st.session_state:
    st.session_state.clicked_icon = None

# Show dashboard
if not st.session_state.active_tool:
    st.subheader("🔍 Choose a Calculator or Tool")

    def render_card(icon, title, key, col):
        with col:
            # If this icon was clicked → glow
            glow_class = "glow" if st.session_state.clicked_icon == key else ""
            st.markdown(f"""
                <div class='card'>
                    <div class='card-emoji {glow_class}'>{icon}</div>
                    <div class='card-title'>{title}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Launch", key=key):
                st.session_state.active_tool = title
                st.session_state.clicked_icon = key

    row1 = st.columns(3)
    render_card("🏠", "Home Loan EMI", "home", row1[0])
    render_card("💰", "SIP Calculator", "sip", row1[1])
    render_card("📈", "Step-up SIP", "step", row1[2])

    row2 = st.columns(3)
    render_card("💸", "Lumpsum Investment", "lump", row2[0])
    render_card("📊", "Inflation Forecast", "inf", row2[1])
    render_card("🧓", "Retirement Planner", "retire", row2[2])

    row3 = st.columns(3)
    render_card("📉", "Inflation-Adjusted SIP", "sipinf", row3[0])
    render_card("⚖️", "Loan Comparison", "loancomp", row3[1])

else:
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.active_tool = None
        st.session_state.clicked_icon = None
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.active_tool == "Home Loan EMI":
        home_loan_emi.render()
    elif st.session_state.active_tool == "SIP Calculator":
        sip.render()
    elif st.session_state.active_tool == "Step-up SIP":
        step_up_sip.render()
    elif st.session_state.active_tool == "Lumpsum Investment":
        lumpsum_investment.render()
    elif st.session_state.active_tool == "Inflation Forecast":
        inflation_forecast.render()
    elif st.session_state.active_tool == "Retirement Planner":
        retirement_planner.render()
    elif st.session_state.active_tool == "Inflation-Adjusted SIP":
        inflation_adjusted_sip.render()
    elif st.session_state.active_tool == "Loan Comparison":
        loan_comparision.render()

