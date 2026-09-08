import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Powered Business Intelligence Platform",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)

# =====================================================
# LOAD CSS
# =====================================================

def load_css():

    try:

        with open("assets/style.css") as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )

    except:
        pass


load_css()

# =====================================================
# COMPONENTS
# =====================================================

from components.auth import show_login
from components.sidebar import show_sidebar
from components.home import show_home
from components.cleaner import show_cleaner
from components.analytics import show_analytics
from components.prediction import show_prediction
from components.reports import show_reports
from components.history import show_history

# =====================================================
# SESSION STATE
# =====================================================

defaults = {

    "logged_in": False,

    "user": "",

    "user_email": "",

    "user_id": None,

    "dataset": None,

    "chat_history": []

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# =====================================================
# LOGIN
# =====================================================

if not st.session_state.logged_in:

    show_login()

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

page = show_sidebar()

df = st.session_state.dataset

# =====================================================
# HOME
# =====================================================

if page == "🏠 Home":

    show_home()

# =====================================================
# OTHER PAGES
# =====================================================

else:

    if df is None:

        st.warning(

            "⚠ Please upload a dataset from the Home page first."

        )

        st.stop()

    if page == "🧹 AI Data Cleaner":

        show_cleaner(df)

    elif page == "📊 Analytics":

        show_analytics(df)

    elif page == "📈 Prediction":

        show_prediction(df)

    elif page == "📄 Reports":

        show_reports(df)

    elif page == "🕒 Chat History":

        show_history()