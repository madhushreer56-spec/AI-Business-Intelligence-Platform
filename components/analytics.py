import streamlit as st
import pandas as pd
import plotly.express as px


def show_analytics(df: pd.DataFrame):

    st.title("📊 Analytics Center")

    tabs = st.tabs(
        [
            "📈 KPI Dashboard",
            "📊 Interactive Dashboard",
            "🎨 Visualization Studio"
        ]
    )

    # ==========================================================
    # KPI DASHBOARD
    # ==========================================================

    with tabs[0]:

        st.subheader("Business KPIs")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) == 0:

            st.warning("No numeric columns found.")

        else:

            selected = st.selectbox(

                "Select KPI Column",

                numeric_cols,

                key="kpi"

            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Total",
                f"{df[selected].sum():,.2f}"
            )

            c2.metric(
                "Average",
                f"{df[selected].mean():,.2f}"
            )

            c3.metric(
                "Maximum",
                f"{df[selected].max():,.2f}"
            )

            c4.metric(
                "Minimum",
                f"{df[selected].min():,.2f}"
            )

            st.divider()

            fig = px.histogram(

                df,

                x=selected,

                nbins=30,

                title=f"Distribution of {selected}"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    with tabs[1]:

        st.subheader("Interactive Dashboard")

        categorical = df.select_dtypes(

            include=["object", "category"]

        ).columns.tolist()

        numeric = df.select_dtypes(

            include="number"

        ).columns.tolist()

        if len(categorical) == 0:

            st.warning("No categorical columns found.")

        elif len(numeric) == 0:

            st.warning("No numeric columns found.")

        else:

            c1, c2 = st.columns(2)

            with c1:

                x = st.selectbox(

                    "Category",

                    categorical,

                    key="dashx"

                )

            with c2:

                y = st.selectbox(

                    "Value",

                    numeric,

                    key="dashy"

                )

            fig = px.bar(

                df,

                x=x,

                y=y,

                color=x,

                title=f"{y} by {x}"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

            st.dataframe(

                df[[x, y]],

                use_container_width=True

            )

    # ==========================================================
    # VISUALIZATION STUDIO
    # ==========================================================

    with tabs[2]:

        st.subheader("Visualization Studio")

        chart = st.selectbox(

            "Chart Type",

            [

                "Bar Chart",

                "Line Chart",

                "Pie Chart",

                "Scatter Plot",

                "Histogram"

            ]

        )

        categorical = df.select_dtypes(

            include=["object", "category"]

        ).columns.tolist()

        numeric = df.select_dtypes(

            include="number"

        ).columns.tolist()

        if len(categorical) == 0 or len(numeric) == 0:

            st.warning("Dataset doesn't contain suitable columns.")

            return

        c1, c2 = st.columns(2)

        with c1:

            x = st.selectbox(

                "Category",

                categorical,

                key="vizx"

            )

        with c2:

            y = st.selectbox(

                "Value",

                numeric,

                key="vizy"

            )

        if chart == "Bar Chart":

            fig = px.bar(df, x=x, y=y, color=x)

        elif chart == "Line Chart":

            fig = px.line(df, x=x, y=y)

        elif chart == "Pie Chart":

            fig = px.pie(df, names=x, values=y)

        elif chart == "Scatter Plot":

            fig = px.scatter(df, x=x, y=y)

        else:

            fig = px.histogram(df, x=y)

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        st.download_button(

            "⬇ Download Current Dataset (CSV)",

            df.to_csv(index=False).encode(),

            "dataset.csv",

            "text/csv",

            use_container_width=True

        )