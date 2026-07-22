import streamlit as st
import pandas as pd

from ai.sql_generator import generate_sql
from ai.business_insights import generate_business_insight
from ai.chart_selector import recommend_chart

from utils.database import execute_sql
from utils.ai_chart import create_ai_chart

from utils.export import dataframe_to_excel
from utils.export import dataframe_to_csv


def show_chat(df: pd.DataFrame):

    st.header("🤖 AI Business Assistant")

    question = st.chat_input(

        "Ask anything about your business..."

    )

    if question is None:

        st.info("""

Examples

• Highest Revenue Product

• Lowest Sales

• Monthly Sales Trend

• Customer Count

• Region Wise Revenue

""")

        return

    with st.chat_message("user"):

        st.write(question)

    with st.spinner("Thinking..."):

        sql = generate_sql(

            question,

            df.columns.tolist()

        )

        st.subheader("Generated SQL")

        st.code(sql, language="sql")

        result = execute_sql(sql)

        st.subheader("Result")

        st.dataframe(result, use_container_width=True)

        chart = recommend_chart(

            question,

            result.columns.tolist()

        )

        st.subheader("Recommended Chart")

        st.info(chart)

        fig = create_ai_chart(

            result,

            chart

        )

        if fig is not None:

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        insight = generate_business_insight(

            question,

            result

        )

        st.subheader("Business Insight")

        st.markdown(insight)

        c1, c2 = st.columns(2)

        with c1:

            st.download_button(

                "📄 Excel",

                dataframe_to_excel(result),

                "result.xlsx"

            )

        with c2:

            st.download_button(

                "📄 CSV",

                dataframe_to_csv(result),

                "result.csv"

            )

        st.session_state.chat_history.append({

            "question": question,

            "sql": sql,

            "insight": insight

        })