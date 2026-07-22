import streamlit as st


def show_login():

    # Center the login content
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            <div style='text-align:center; margin-top:60px;'>
                <div style='font-size:70px;'>🤖</div>
                <h1 style='color:white; margin-bottom:0;'>
                    AI Business Intelligence
                </h1>
                <p style='color:#94A3B8; font-size:18px;'>
                    Login to continue
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        remember = st.checkbox("Remember Me")

        if st.button("Login", use_container_width=True):

            if email == "admin@gmail.com" and password == "admin123":

                st.session_state.logged_in = True
                st.session_state.user = "Madhu"

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Email or Password")