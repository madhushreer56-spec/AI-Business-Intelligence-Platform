import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.ensemble import IsolationForest


def show_anomalies(df: pd.DataFrame):

    st.title("🚨 AI Anomaly Detection")

    numeric = df.select_dtypes(include="number").columns.tolist()

    if len(numeric) == 0:

        st.warning("No numeric columns.")

        return

    feature = st.selectbox(

        "Select Column",

        numeric

    )

    contamination = st.slider(

        "Outlier Percentage",

        1,

        20,

        5

    )

    data = df[[feature]].dropna().copy()

    model = IsolationForest(

        contamination=contamination / 100,

        random_state=42

    )

    data["Prediction"] = model.fit_predict(data)

    data["Status"] = data["Prediction"].map({

        1: "Normal",

        -1: "Anomaly"

    })

    # Safe positive score
    score = model.decision_function(data[[feature]])

    score = abs(score - score.min()) + 1

    data["Risk Score"] = score

    st.metric(

        "Anomalies",

        len(data[data["Status"] == "Anomaly"])

    )

    fig = px.scatter(

        data,

        x=data.index,

        y=feature,

        color="Status",

        size="Risk Score",

        hover_data=["Risk Score"]

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.subheader("Detected Records")

    st.dataframe(

        data[data["Status"] == "Anomaly"],

        use_container_width=True

    )