import streamlit as st


def nav_button(label, icon):

    page_name = f"{icon} {label}"

    active = st.session_state.page == page_name

    if st.button(

        page_name,

        use_container_width=True,

        type="primary" if active else "secondary",

        key=page_name

    ):

        st.session_state.page = page_name

        st.rerun()


def show_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding-top:10px;padding-bottom:15px;">
                <h2 style="color:white;margin-bottom:0;">
                    🤖 AI Powered
                </h2>
                <h3 style="color:white;margin-top:5px;">
                    Business Intelligence Platform
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        if "page" not in st.session_state:
            st.session_state.page = "🏠 Home"

        nav_button("Home", "🏠")
        nav_button("AI Data Cleaner", "🧹")
        nav_button("Analytics", "📊")
        nav_button("Prediction", "📈")
        nav_button("Reports", "📄")
        nav_button("Chat History", "🕒")

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="logout_btn"
        ):

            st.session_state.logged_in = False
            st.session_state.user = ""
            st.session_state.dataset = None
            st.session_state.chat_history = []
            st.session_state.page = "🏠 Home"

            st.rerun()

    return st.session_state.page