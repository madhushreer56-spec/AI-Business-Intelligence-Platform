import streamlit as st
import pandas as pd


def upload_dataset():

    st.subheader("📂 Upload Business Dataset")

    uploaded = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded is None:
        return None

    try:

        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)

        else:
            df = pd.read_excel(uploaded)

        st.success("✅ Dataset uploaded successfully!")

        with st.expander("Preview Dataset"):

            st.dataframe(
                df.head(10),
                use_container_width=True
            )

        return df

    except Exception as e:

        st.error(f"Error loading dataset\n{e}")

        return None