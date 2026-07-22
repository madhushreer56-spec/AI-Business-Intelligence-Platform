import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest


def show_prediction(df: pd.DataFrame):

    st.title("📈 Prediction Center")

    tab1, tab2 = st.tabs(
        [
            "🔮 Forecast",
            "🚨 Anomaly Detection"
        ]
    )

    # =====================================================
    # FORECAST
    # =====================================================

    with tab1:

        st.subheader("Sales Forecast")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) == 0:

            st.warning("No numeric columns available.")

        else:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_cols,
                key="forecast_column"
            )

            future_days = st.slider(
                "Forecast Period",
                5,
                50,
                10
            )

            y = df[column].fillna(0).values

            X = np.arange(len(y)).reshape(-1, 1)

            model = LinearRegression()

            model.fit(X, y)

            future_x = np.arange(
                len(y),
                len(y) + future_days
            ).reshape(-1, 1)

            prediction = model.predict(future_x)

            history = pd.DataFrame({

                "Index": np.arange(len(y)),

                "Value": y,

                "Type": "Historical"

            })

            future = pd.DataFrame({

                "Index": np.arange(
                    len(y),
                    len(y) + future_days
                ),

                "Value": prediction,

                "Type": "Forecast"

            })

            final_df = pd.concat(
                [history, future],
                ignore_index=True
            )

            fig = px.line(

                final_df,

                x="Index",

                y="Value",

                color="Type",

                markers=True,

                title=f"{column} Forecast"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Forecast Values")

            st.dataframe(
                future,
                use_container_width=True
            )

    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    with tab2:

        st.subheader("AI Anomaly Detection")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) == 0:

            st.warning("No numeric columns available.")

        else:

            column = st.selectbox(
                "Select Column",
                numeric_cols,
                key="anomaly_column"
            )

            contamination = st.slider(
                "Anomaly Percentage",
                1,
                20,
                5
            ) / 100

            data = df[[column]].copy()

            data.fillna(0, inplace=True)

            model = IsolationForest(

                contamination=contamination,

                random_state=42

            )

            data["Prediction"] = model.fit_predict(data)

            data["Status"] = data["Prediction"].map({

                1: "Normal",

                -1: "Anomaly"

            })

            anomaly_count = (data["Status"] == "Anomaly").sum()

            normal_count = (data["Status"] == "Normal").sum()

            c1, c2 = st.columns(2)

            c1.metric(
                "Normal Records",
                normal_count
            )

            c2.metric(
                "Detected Anomalies",
                anomaly_count
            )

            fig = px.scatter(

                data,

                x=data.index,

                y=column,

                color="Status",

                hover_data=[column],

                title="Detected Anomalies"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Detection Results")

            st.dataframe(
                data,
                use_container_width=True
            )

            anomalies = data[data["Status"] == "Anomaly"]

            if not anomalies.empty:

                st.download_button(

                    "⬇ Download Anomalies",

                    anomalies.to_csv(index=False).encode(),

                    "anomalies.csv",

                    "text/csv",

                    use_container_width=True

                )