import streamlit as st
import pandas as pd
import plotly.express as px


def show_visualization(df: pd.DataFrame):

    st.title("📊 Visualization Studio")

    numeric=df.select_dtypes(include="number").columns.tolist()

    all_cols=df.columns.tolist()

    chart=st.selectbox(

        "Choose Visualization",

        [

            "Bar Chart",

            "Line Chart",

            "Pie Chart",

            "Scatter Plot",

            "Histogram",

            "Box Plot",

            "Heatmap"

        ]

    )

    if chart!="Heatmap":

        x=st.selectbox("X Axis",all_cols)

        y=st.selectbox("Y Axis",numeric)

    if chart=="Bar Chart":

        fig=px.bar(df,x=x,y=y)

    elif chart=="Line Chart":

        fig=px.line(df,x=x,y=y)

    elif chart=="Pie Chart":

        fig=px.pie(df,names=x,values=y)

    elif chart=="Scatter Plot":

        fig=px.scatter(df,x=x,y=y,color=x)

    elif chart=="Histogram":

        fig=px.histogram(df,x=y)

    elif chart=="Box Plot":

        fig=px.box(df,y=y)

    elif chart=="Heatmap":

        corr=df[numeric].corr()

        fig=px.imshow(

            corr,

            text_auto=True,

            aspect="auto"

        )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    st.subheader("Visualization Data")

    st.dataframe(

        df,

        use_container_width=True

    )