import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.export import generate_csv_download, generate_pdf_report
from utils.common import format_inr

def render():
    st.header("🤖 ML: Inflation Forecast (Linear Regression)")

    # Sample inflation data (can replace with real data later)
    years = np.arange(2010, 2024)
    inflation = np.array([11.99, 8.86, 9.3, 10.9, 6.37, 4.9, 5.02, 3.3, 4.86, 6.62, 6.16, 6.7, 5.1])

    df = pd.DataFrame({"Year": years, "Inflation": inflation})
    st.line_chart(df.set_index("Year"))

    future_years = st.slider("Forecast up to year", 2025, 2035, 2030)

    # Train linear model
    model = LinearRegression()
    model.fit(years.reshape(-1, 1), inflation)
    pred_years = np.arange(2024, future_years + 1).reshape(-1, 1)
    predictions = model.predict(pred_years)

    result_df = pd.DataFrame({
        "Year": pred_years.flatten(),
        "Predicted Inflation (%)": np.round(predictions, 2)
    })

    st.line_chart(result_df.set_index("Year"))
    st.dataframe(result_df)

    # 🧾 Export options
    st.markdown("### 📤 Export Options")
    generate_csv_download(result_df, filename="inflation_forecast.csv")

    summary = {
        "Forecast Range": f"2024 to {future_years}",
        "Final Year Prediction": f"{predictions[-1]:.2f}%"
    }
    generate_pdf_report(summary, filename="inflation_forecast_summary.pdf")
