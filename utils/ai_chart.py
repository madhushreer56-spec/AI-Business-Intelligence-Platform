import plotly.express as px


def create_ai_chart(df, chart_type):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    if len(df) == 0:
        return None

    if chart_type == "Table":
        return None

    if len(numeric_cols) == 0:
        return None

    y = numeric_cols[0]

    if len(categorical_cols) > 0:
        x = categorical_cols[0]
    else:
        x = df.columns[0]

    if chart_type == "Bar Chart":
        return px.bar(df, x=x, y=y)

    elif chart_type == "Line Chart":
        return px.line(df, x=x, y=y)

    elif chart_type == "Pie Chart":
        return px.pie(df, names=x, values=y)

    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y)

    elif chart_type == "Histogram":
        return px.histogram(df, x=y)

    return None