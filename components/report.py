import streamlit as st

from utils.report_generator import generate_report


def show_report(df):

    st.title("📄 Executive Report")

    st.write("Generate a professional business report.")

    if st.button("Generate Report"):

        with st.spinner("Generating PDF..."):

            report = generate_report(df)

        with open(report, "rb") as file:

            st.download_button(

                "⬇ Download Report",

                file,

                file_name="Business_Report.pdf",

                mime="application/pdf"

            )

        st.success("Report Generated Successfully.")