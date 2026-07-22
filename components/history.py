import streamlit as st


def show_history():

    st.title("🕒 Chat History")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    history = st.session_state.chat_history

    if len(history) == 0:

        st.info("No chat history available.")

        return

    if st.button(
        "🗑 Clear Chat History",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.success("Chat history cleared.")

        st.rerun()

    st.divider()

    for i, chat in enumerate(reversed(history), start=1):

        with st.expander(f"Conversation {i}"):

            st.markdown("### 👤 Question")
            st.write(chat["question"])

            st.markdown("### 📝 SQL")
            st.code(chat["sql"], language="sql")

            st.markdown("### 💡 Business Insight")
            st.write(chat["insight"])

            if "result" in chat:

                st.markdown("### 📊 Result")

                st.dataframe(
                    chat["result"],
                    use_container_width=True
                )

            if "figure" in chat:

                if chat["figure"] is not None:

                    st.plotly_chart(
                        chat["figure"],
                        use_container_width=True
                    )