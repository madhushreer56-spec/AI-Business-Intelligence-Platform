from sklearn.ensemble import IsolationForest
import pandas as pd


def detect_anomalies(df):

    if "Sales" not in df.columns:
        return None

    temp = df.copy()

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    temp["Anomaly"] = model.fit_predict(
        temp[["Sales"]]
    )

    anomalies = temp[temp["Anomaly"] == -1]

    return anomalies