import plotly.express as px


def create_chart(df, chart_type, x, y):

    if chart_type == "Bar Chart":
        return px.bar(df, x=x, y=y, color=x)

    elif chart_type == "Line Chart":
        return px.line(df, x=x, y=y)

    elif chart_type == "Pie Chart":
        return px.pie(df, names=x, values=y)

    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y)

    elif chart_type == "Histogram":
        return px.histogram(df, x=x)

    elif chart_type == "Box Plot":
        return px.box(df, x=x, y=y)

    elif chart_type == "Area Chart":
        return px.area(df, x=x, y=y)

    else:
        return px.bar(df, x=x, y=y)