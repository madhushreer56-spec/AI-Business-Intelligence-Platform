import streamlit as st
import pandas as pd


def show_narrator(df: pd.DataFrame):

    st.title("🧠 AI Data Narrator")

    st.write("Automatically generates a business summary of your dataset.")

    st.subheader("Dataset Overview")

    st.write(f"Rows : {df.shape[0]}")
    st.write(f"Columns : {df.shape[1]}")

    st.write(f"Missing Values : {df.isnull().sum().sum()}")

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:

        st.subheader("Key Statistics")

        st.dataframe(
            numeric.describe(),
            use_container_width=True
        )

    st.subheader("AI Summary")

    summary = f"""
This dataset contains **{df.shape[0]} records** and **{df.shape[1]} columns**.

There are **{df.isnull().sum().sum()} missing values**.

The dataset appears suitable for:

- KPI Analysis
- Forecasting
- Business Intelligence
- AI Question Answering
- Visualization
"""

    st.success(summary)