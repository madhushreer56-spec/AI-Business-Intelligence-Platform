import streamlit as st

from utils.report_generator import generate_report


def show_reports(df):

    st.title("📄 Reports Center")

    tab1, tab2 = st.tabs(

        [

            "📰 Data Narrator",

            "📑 Executive Report"

        ]

    )

    # ==========================================
    # DATA NARRATOR
    # ==========================================

    with tab1:

        st.subheader("Dataset Summary")

        rows, cols = df.shape

        st.write(f"Rows : {rows}")

        st.write(f"Columns : {cols}")

        st.write("")

        st.markdown("### Column Information")

        st.dataframe(

            df.dtypes.astype(str),

            use_container_width=True

        )

        st.markdown("### Missing Values")

        st.dataframe(

            df.isnull().sum(),

            use_container_width=True

        )

        st.markdown("### Basic Statistics")

        st.dataframe(

            df.describe(),

            use_container_width=True

        )

    # ==========================================
    # EXECUTIVE REPORT
    # ==========================================

    with tab2:

        st.subheader("Executive Business Report")

        if st.button(

            "Generate PDF Report",

            use_container_width=True

        ):

            filename = generate_report(df)

            with open(filename, "rb") as file:

                st.download_button(

                    "⬇ Download Executive Report",

                    file,

                    file_name="Business_Report.pdf",

                    mime="application/pdf",

                    use_container_width=True

                )