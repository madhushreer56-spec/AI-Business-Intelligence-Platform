import streamlit as st
import pandas as pd

from ai.ai_pipeline import ask_ai, generate_result_insight

from utils.database import execute_sql
from utils.ai_chart import create_ai_chart
from utils.export import dataframe_to_csv, dataframe_to_excel


# ==========================================================
# AI ASSISTANT
# ==========================================================

def show_ai_assistant(df: pd.DataFrame):

    st.markdown("## 🤖 Ask AI")

    # ------------------------------------------------------
    # Initialize chat history
    # ------------------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ------------------------------------------------------
    # Display Previous Conversations
    # ------------------------------------------------------

    for chat in st.session_state.chat_history:

        # User message
        with st.chat_message("user"):

            st.write(
                chat["question"]
            )

        # AI response
        with st.chat_message("assistant"):

            # SQL
            st.subheader("📝 SQL Query")

            st.code(
                chat["sql"],
                language="sql"
            )

            # Result
            st.subheader("📊 Result")

            st.dataframe(
                chat["result"],
                use_container_width=True
            )

            # Visualization
            if chat.get("figure") is not None:

                st.subheader("📈 Visualization")

                st.plotly_chart(
                    chat["figure"],
                    use_container_width=True
                )

            # Business Insight
            st.subheader("💡 Business Insight")

            st.markdown(
                chat["insight"]
            )

    # ------------------------------------------------------
    # Chat Input
    # ------------------------------------------------------

    question = st.chat_input(
        "Ask anything about your business data..."
    )

    if not question:
        return

    # ------------------------------------------------------
    # Display User Question
    # ------------------------------------------------------

    with st.chat_message("user"):

        st.write(question)

    # ------------------------------------------------------
    # AI Response
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        status = st.empty()

        status.info(
            "🤖 AI is analyzing your business data..."
        )

        try:

            # ------------------------------------------------
            # Step 1: Gemini generates SQL + chart type
            # ------------------------------------------------

            sql, chart_type = ask_ai(
                question,
                df
            )

            # ------------------------------------------------
            # Step 2: Execute SQL
            # ------------------------------------------------

            result = execute_sql(
                sql
            )

            # ------------------------------------------------
            # Step 3: Generate insight from ACTUAL result
            # ------------------------------------------------

            insight = generate_result_insight(
                question,
                result
            )

            # ------------------------------------------------
            # Step 4: Create visualization
            # ------------------------------------------------

            figure = create_ai_chart(
                result,
                chart_type
            )

            status.success(
                "✅ Analysis Completed"
            )

        except Exception as e:

            status.empty()

            st.error(
                f"❌ AI Analysis Error:\n\n{e}"
            )

            return

        # ------------------------------------------------------
        # Remove loading message
        # ------------------------------------------------------

        status.empty()

        # ------------------------------------------------------
        # Display SQL
        # ------------------------------------------------------

        st.subheader(
            "📝 SQL Query"
        )

        st.code(
            sql,
            language="sql"
        )

        # ------------------------------------------------------
        # Display Result
        # ------------------------------------------------------

        st.subheader(
            "📊 Result"
        )

        if result.empty:

            st.warning(
                "No matching records were found."
            )

        else:

            st.dataframe(
                result,
                use_container_width=True
            )

        # ------------------------------------------------------
        # Display Visualization
        # ------------------------------------------------------

        if figure is not None:

            st.subheader(
                "📈 Visualization"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        # ------------------------------------------------------
        # Display Business Insight
        # ------------------------------------------------------

        st.subheader(
            "💡 Business Insight"
        )

        st.markdown(
            insight
        )

        # ------------------------------------------------------
        # Download Buttons
        # ------------------------------------------------------

        st.divider()

        col1, col2 = st.columns(2)

        # CSV
        with col1:

            csv = dataframe_to_csv(
                result
            )

            st.download_button(
                label="⬇ Download CSV",
                data=csv,
                file_name="query_result.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Excel
        with col2:

            excel = dataframe_to_excel(
                result
            )

            st.download_button(
                label="⬇ Download Excel",
                data=excel,
                file_name="query_result.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )

    # ------------------------------------------------------
    # Save Conversation
    # ------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "question": question,
            "sql": sql,
            "result": result,
            "figure": figure,
            "insight": insight
        }
    )