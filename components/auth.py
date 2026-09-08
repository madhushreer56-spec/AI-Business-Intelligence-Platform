import streamlit as st
import sqlite3
import os
import re
import hashlib
import hmac


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_FOLDER = "database"
DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    "business.db"
)


def get_auth_connection():

    os.makedirs(
        DATABASE_FOLDER,
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_PATH
    )


# ==========================================================
# CREATE USERS TABLE
# ==========================================================

def create_users_table():

    conn = get_auth_connection()

    try:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()

    finally:

        conn.close()


# ==========================================================
# PASSWORD HASHING
# ==========================================================

def hash_password(password):

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


# ==========================================================
# VERIFY PASSWORD
# ==========================================================

def verify_password(password, stored_hash):

    try:

        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(
            salt_hex
        )

        stored_password_hash = bytes.fromhex(
            hash_hex
        )

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return hmac.compare_digest(
            password_hash,
            stored_password_hash
        )

    except Exception:

        return False


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    ) is not None


# ==========================================================
# SIGN UP
# ==========================================================

def signup_user(
    name,
    email,
    password
):

    conn = get_auth_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return False, "An account with this email already exists."

        password_hash = hash_password(
            password
        )

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )

            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    except Exception as e:

        return False, f"Registration error: {e}"

    finally:

        conn.close()


# ==========================================================
# LOGIN
# ==========================================================

def login_user(
    email,
    password
):

    conn = get_auth_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash

            FROM users

            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:

            return False, None

        user_id = user[0]
        name = user[1]
        user_email = user[2]
        stored_hash = user[3]

        if not verify_password(
            password,
            stored_hash
        ):

            return False, None

        return True, {
            "id": user_id,
            "name": name,
            "email": user_email
        }

    finally:

        conn.close()


# ==========================================================
# LOGIN PAGE
# ==========================================================

def show_login():

    # Make sure users table exists
    create_users_table()

    st.markdown(
        """
        <div style="
            text-align:center;
            padding-top:40px;
            padding-bottom:20px;
        ">

        <h1>🤖 AI Business Intelligence Platform</h1>

        <p style="
            color:#9CA3AF;
            font-size:18px;
        ">
        AI-powered business data analysis
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # Login / Sign Up tabs
    # ------------------------------------------------------

    login_tab, signup_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )

    # ======================================================
    # LOGIN
    # ======================================================

    with login_tab:

        st.subheader(
            "Welcome Back"
        )

        st.write(
            "Login to access your business intelligence dashboard."
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            key="login_button"
        ):

            email = email.strip().lower()

            if not email or not password:

                st.error(
                    "Please enter your email and password."
                )

            elif not valid_email(email):

                st.error(
                    "Please enter a valid email address."
                )

            else:

                success, user = login_user(
                    email,
                    password
                )

                if success:

                    st.session_state.logged_in = True

                    st.session_state.user = user["name"]

                    st.session_state.user_email = user["email"]

                    st.session_state.user_id = user["id"]

                    st.success(
                        f"Welcome back, {user['name']}! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )

    # ======================================================
    # SIGN UP
    # ======================================================

    with signup_tab:

        st.subheader(
            "Create Your Account"
        )

        st.write(
            "Create your own account to use the platform."
        )

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="signup_name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="example@gmail.com",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm_password"
        )

        st.caption(
            "Password should contain at least 6 characters."
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="signup_button"
        ):

            name = name.strip()

            email = email.strip().lower()

            # ----------------------------------------------
            # Validation
            # ----------------------------------------------

            if not name:

                st.error(
                    "Please enter your name."
                )

            elif not valid_email(email):

                st.error(
                    "Please enter a valid email address."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = signup_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "You can now open the Login tab and sign in."
                    )

                else:

                    st.error(
                        message
                    )