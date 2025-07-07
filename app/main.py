import streamlit as st
from calculators import home_loan_emi, sip, step_up_sip, lumpsum_investment
from ml_tools import inflation_forecast, retirement_planner, inflation_adjusted_sip
from utils.common import set_page_config
from utils import export

# Configure page
set_page_config()

st.markdown("""
    <style>
    .card {
        background-color: #1e1e1e;
        padding: 1.2rem;
        border-radius: 15px;
        box-shadow: 0px 2px 10px rgba(255, 255, 255, 0.05);
        text-align: center;
        border: 1px solid #333;
        transition: 0.3s ease;
    }
    .card:hover {
        background-color: #2a2a2a;
        transform: scale(1.03);
        border-color: #666;
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #ffffff;
    }
    .card-emoji {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 All-in-One Finance Calculator")

if "active_tool" not in st.session_state:
    st.session_state.active_tool = None

# Show dashboard
if not st.session_state.active_tool:
    st.subheader("🔍 Choose a Calculator or Tool")

    def render_card(icon, title, key, col):
        with col:
            st.markdown(f"""
                <div class='card'>
                    <div class='card-emoji'>{icon}</div>
                    <div class='card-title'>{title}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select", key=key):
                st.session_state.active_tool = title

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

else:
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.active_tool = None

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
