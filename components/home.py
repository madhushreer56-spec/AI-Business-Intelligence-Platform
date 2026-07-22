import streamlit as st

from components.upload import upload_dataset
from components.ai_assistant import show_ai_assistant
from utils.database import save_to_database


def show_home():

    user = st.session_state.get("user", "User")

    st.markdown(
        f"""
        <h1 style="text-align:center;">
        👋 Welcome, {user}
        </h1>

        <h3 style="text-align:center;color:#9CA3AF;">
        AI Powered Business Intelligence Platform
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if "dataset" not in st.session_state:
        st.session_state.dataset = None

    if st.session_state.dataset is None:

        uploaded_df = upload_dataset()

        if uploaded_df is not None:

            st.session_state.dataset = uploaded_df

            save_to_database(uploaded_df)

            st.success("✅ Dataset uploaded successfully!")

            st.rerun()

        st.info("📂 Upload a CSV or Excel file to begin.")

        return

    df = st.session_state.dataset

    st.success("✅ Dataset Loaded Successfully")

    st.write("")

    show_ai_assistant(df)