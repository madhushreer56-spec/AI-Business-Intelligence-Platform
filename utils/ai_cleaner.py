import pandas as pd
import numpy as np
from pandas.api.types import (
    is_numeric_dtype,
    is_string_dtype,
    is_datetime64_any_dtype
)


def clean_dataset(df):

    cleaned_df = df.copy()

    report = []

    # ==========================================
    # Remove Duplicate Rows
    # ==========================================

    duplicate_rows = cleaned_df.duplicated().sum()

    if duplicate_rows > 0:

        cleaned_df.drop_duplicates(inplace=True)

        report.append(
            f"✅ Removed {duplicate_rows} duplicate rows."
        )

    else:

        report.append(
            "✅ No duplicate rows found."
        )

    # ==========================================
    # Remove Completely Empty Rows
    # ==========================================

    empty_rows = cleaned_df.isnull().all(axis=1).sum()

    if empty_rows > 0:

        cleaned_df.dropna(
            how="all",
            inplace=True
        )

        report.append(
            f"✅ Removed {empty_rows} empty rows."
        )

    # ==========================================
    # Clean Every Column
    # ==========================================

    for column in cleaned_df.columns:

        missing = cleaned_df[column].isnull().sum()

        # -------------------------
        # Numeric Columns
        # -------------------------

        if is_numeric_dtype(cleaned_df[column]):

            if missing > 0:

                median = cleaned_df[column].median()

                cleaned_df[column].fillna(
                    median,
                    inplace=True
                )

                report.append(
                    f"✅ Filled {missing} missing values in '{column}' using median."
                )

            # ---------------------
            # Outlier Detection
            # ---------------------

            q1 = cleaned_df[column].quantile(0.25)

            q3 = cleaned_df[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            outliers = (
                (cleaned_df[column] < lower) |
                (cleaned_df[column] > upper)
            ).sum()

            if outliers > 0:

                report.append(
                    f"⚠ Detected {outliers} outliers in '{column}'."
                )

        # -------------------------
        # Text Columns
        # -------------------------

        elif is_string_dtype(cleaned_df[column]) or cleaned_df[column].dtype == "object":

            cleaned_df[column] = (
                cleaned_df[column]
                .astype(str)
                .str.strip()
            )

            cleaned_df[column].replace(
                "nan",
                np.nan,
                inplace=True
            )

            if missing > 0:

                mode = cleaned_df[column].mode()

                if len(mode) > 0:

                    cleaned_df[column].fillna(
                        mode.iloc[0],
                        inplace=True
                    )

                    report.append(
                        f"✅ Filled {missing} missing values in '{column}' using mode."
                    )

                else:

                    cleaned_df[column].fillna(
                        "Unknown",
                        inplace=True
                    )

                    report.append(
                        f"✅ Filled {missing} missing values in '{column}' using 'Unknown'."
                    )

            # ---------------------
            # Date Detection
            # ---------------------

            try:

                converted = pd.to_datetime(
                    cleaned_df[column],
                    errors="raise"
                )

                cleaned_df[column] = converted

                report.append(
                    f"📅 Converted '{column}' to Date format."
                )

            except Exception:

                pass

        # -------------------------
        # Datetime Columns
        # -------------------------

        elif is_datetime64_any_dtype(cleaned_df[column]):

            report.append(
                f"📅 '{column}' already contains Date values."
            )

    # ==========================================
    # Reset Index
    # ==========================================

    cleaned_df.reset_index(
        drop=True,
        inplace=True
    )

    report.append(
        "✅ Reset dataframe index."
    )

    # ==========================================
    # Dataset Summary
    # ==========================================

    report.append(
        f"📊 Final Dataset Shape : {cleaned_df.shape[0]} Rows × {cleaned_df.shape[1]} Columns"
    )

    return cleaned_df, report