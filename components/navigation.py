import streamlit as st


def navigation():

    return st.sidebar.radio(

        "Navigation",

        [

            "Dashboard",

            "Forecast",

            "Anomaly Detection",

            "AI Assistant",

            "AI Narrator",

            "Executive Report"

        ]

    )