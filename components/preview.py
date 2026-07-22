import streamlit as st
import pandas as pd


def show_preview(df: pd.DataFrame):

    st.header("📄 Dataset Preview")

    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Dataset Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

    st.subheader("📋 Column Names")
    st.write(list(df.columns))

    st.subheader("🧾 Data Types")
    st.dataframe(
        df.dtypes.astype(str),
        use_container_width=True
    )

    st.subheader("❌ Missing Values by Column")
    st.dataframe(
        df.isnull().sum().reset_index().rename(
            columns={
                "index": "Column",
                0: "Missing Values"
            }
        ),
        use_container_width=True
    )

    st.subheader("📈 Basic Statistics")

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        st.dataframe(
            numeric_df.describe(),
            use_container_width=True
        )
    else:
        st.info("No numeric columns available.")