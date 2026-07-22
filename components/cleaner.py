import streamlit as st

from utils.ai_cleaner import clean_dataset


def show_cleaner(df):

    st.title("🧹 AI Data Cleaner")

    st.write(
        "Automatically clean your dataset using AI-powered preprocessing."
    )

    st.write("")

    # Only this button
    if st.button(

        "✨ Clean Dataset",

        use_container_width=True

    ):

        cleaned_df, report = clean_dataset(df)

        st.success("✅ Dataset cleaned successfully!")

        st.write("")

        st.subheader("Cleaning Report")

        for item in report:

            st.success(item)

        st.write("")

        st.subheader("Cleaned Dataset")

        st.dataframe(

            cleaned_df,

            use_container_width=True

        )

        csv = cleaned_df.to_csv(index=False).encode()

        st.download_button(

            "⬇ Download Cleaned Dataset",

            csv,

            "cleaned_dataset.csv",

            "text/csv",

            use_container_width=True

        )