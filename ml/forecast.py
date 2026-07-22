import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_sales(df):

    if "Sales" not in df.columns:
        return None

    temp = df.copy()

    temp = temp.reset_index()

    temp["Day"] = range(1, len(temp) + 1)

    X = temp[["Day"]]
    y = temp["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    future_days = pd.DataFrame({
        "Day": range(len(temp) + 1, len(temp) + 8)
    })

    predictions = model.predict(future_days)

    forecast = future_days.copy()

    forecast["Predicted Sales"] = predictions

    return forecast