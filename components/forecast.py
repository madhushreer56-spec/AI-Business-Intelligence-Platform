import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from sklearn.linear_model import LinearRegression


def show_forecast(df: pd.DataFrame):

    st.title("📈 Sales Forecast")

    numeric = df.select_dtypes(include="number").columns.tolist()

    if len(numeric) == 0:

        st.warning("No numeric columns found.")

        return

    column = st.selectbox(

        "Forecast Column",

        numeric

    )

    future = st.slider(

        "Forecast Points",

        5,

        50,

        10

    )

    values = df[column].dropna().reset_index(drop=True)

    if len(values) < 5:

        st.warning("Not enough data.")

        return

    X = np.arange(len(values)).reshape(-1, 1)

    y = values.values

    model = LinearRegression()

    model.fit(X, y)

    future_x = np.arange(

        len(values) + future

    ).reshape(-1, 1)

    prediction = model.predict(future_x)

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=list(range(len(values))),

            y=values,

            mode="lines+markers",

            name="Actual"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=list(range(len(prediction))),

            y=prediction,

            mode="lines",

            name="Forecast"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    forecast_df = pd.DataFrame({

        "Future Index": range(

            len(values),

            len(values) + future

        ),

        "Forecast": prediction[-future:]

    })

    st.subheader("Forecast Values")

    st.dataframe(

        forecast_df,

        use_container_width=True

    )

    st.success("Forecast completed.")