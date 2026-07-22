import streamlit as st
import pandas as pd

from ai.ai_pipeline import ask_ai

from utils.database import execute_sql
from utils.ai_chart import create_ai_chart
from utils.export import dataframe_to_csv, dataframe_to_excel


def show_ai_assistant(df: pd.DataFrame):

    st.markdown("## 🤖 Ask AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # -----------------------------
    # Display Previous Chats
    # -----------------------------

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):

            st.subheader("📝 SQL Query")
            st.code(chat["sql"], language="sql")

            st.subheader("📊 Result")
            st.dataframe(
                chat["result"],
                use_container_width=True
            )

            if chat["figure"] is not None:

                st.subheader("📈 Visualization")

                st.plotly_chart(
                    chat["figure"],
                    use_container_width=True
                )

            st.subheader("💡 Business Insight")

            st.markdown(chat["insight"])

    # -----------------------------
    # Chat Input
    # -----------------------------

    question = st.chat_input(
        "Ask anything about your business data..."
    )

    if not question:
        return

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        status = st.empty()

        status.info("🤖 AI is analyzing your business data...")

        try:

            sql, chart_type, insight = ask_ai(
                question,
                df.columns.tolist()
            )

            # Detect Offline BI Mode
            if "Offline Business Intelligence" in insight:

                status.warning(
                    "☁ Gemini AI is currently unavailable.\n\n"
                    "Automatically switched to Offline BI Mode."
                )

            else:

                status.success(
                    "✅ Analysis Completed"
                )

            result = execute_sql(sql)

            figure = create_ai_chart(
                result,
                chart_type
            )

        except Exception as e:

            status.empty()

            st.error(str(e))

            return

        status.empty()

        st.subheader("📝 SQL Query")

        st.code(
            sql,
            language="sql"
        )

        st.subheader("📊 Result")

        st.dataframe(
            result,
            use_container_width=True
        )

        if figure is not None:

            st.subheader("📈 Visualization")

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        st.subheader("💡 Business Insight")

        st.markdown(insight)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            csv = dataframe_to_csv(result)

            st.download_button(

                "⬇ Download CSV",

                csv,

                "query_result.csv",

                use_container_width=True

            )

        with col2:

            excel = dataframe_to_excel(result)

            st.download_button(

                "⬇ Download Excel",

                excel,

                "query_result.xlsx",

                use_container_width=True

            )

    st.session_state.chat_history.append({

        "question": question,

        "sql": sql,

        "result": result,

        "figure": figure,

        "insight": insight

    })