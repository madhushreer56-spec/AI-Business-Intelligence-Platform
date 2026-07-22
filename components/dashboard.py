import streamlit as st
import pandas as pd
import plotly.express as px


def interactive_dashboard(df: pd.DataFrame):

    st.title("📊 Interactive Dashboard")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object","category"]
    ).columns.tolist()

    if len(numeric_cols) == 0:

        st.warning("No numeric columns found.")

        return

    col1,col2 = st.columns(2)

    with col1:

        x = st.selectbox(
            "Select Category",
            categorical_cols if categorical_cols else df.columns.tolist()
        )

    with col2:

        y = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

    chart = st.selectbox(

        "Chart Type",

        [
            "Bar",
            "Line",
            "Pie",
            "Scatter",
            "Histogram",
            "Box Plot"
        ]

    )

    if chart=="Bar":

        fig=px.bar(df,x=x,y=y)

    elif chart=="Line":

        fig=px.line(df,x=x,y=y)

    elif chart=="Pie":

        fig=px.pie(df,names=x,values=y)

    elif chart=="Scatter":

        fig=px.scatter(df,x=x,y=y,color=x)

    elif chart=="Histogram":

        fig=px.histogram(df,x=y)

    else:

        fig=px.box(df,y=y)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )