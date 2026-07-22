import pandas as pd


def clean_dataset(df: pd.DataFrame):

    cleaned_df = df.copy()

    report = []

    # ==========================================
    # Remove Duplicate Rows
    # ==========================================

    duplicate_count = cleaned_df.duplicated().sum()

    if duplicate_count > 0:

        cleaned_df.drop_duplicates(inplace=True)

        report.append(
            f"Removed {duplicate_count} duplicate rows."
        )

    else:

        report.append("No duplicate rows found.")

    # ==========================================
    # Remove Empty Rows
    # ==========================================

    empty_rows = cleaned_df.isnull().all(axis=1).sum()

    if empty_rows > 0:

        cleaned_df.dropna(
            how="all",
            inplace=True
        )

        report.append(
            f"Removed {empty_rows} completely empty rows."
        )

    else:

        report.append("No empty rows found.")

    # ==========================================
    # Handle Missing Values
    # ==========================================

    for column in cleaned_df.columns:

        missing = cleaned_df[column].isnull().sum()

        if missing == 0:
            continue

        if pd.api.types.is_numeric_dtype(cleaned_df[column]):

            value = cleaned_df[column].median()

            cleaned_df[column].fillna(
                value,
                inplace=True
            )

            report.append(
                f"{column}: Filled {missing} missing values using median."
            )

        else:

            mode = cleaned_df[column].mode()

            if len(mode) > 0:

                cleaned_df[column].fillna(
                    mode[0],
                    inplace=True
                )

                report.append(
                    f"{column}: Filled {missing} missing values using mode."
                )

            else:

                cleaned_df[column].fillna(
                    "Unknown",
                    inplace=True
                )

                report.append(
                    f"{column}: Filled {missing} missing values with 'Unknown'."
                )

    # ==========================================
    # Remove Extra Spaces
    # ==========================================

    object_columns = cleaned_df.select_dtypes(
        include="object"
    ).columns

    for col in object_columns:

        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

    report.append("Removed unnecessary spaces from text columns.")

    # ==========================================
    # Try Date Conversion
    # ==========================================

    for col in object_columns:

        try:

            converted = pd.to_datetime(
                cleaned_df[col],
                errors="raise"
            )

            cleaned_df[col] = converted

            report.append(
                f"{col}: Converted to Date format."
            )

        except Exception:

            pass

    # ==========================================
    # Reset Index
    # ==========================================

    cleaned_df.reset_index(
        drop=True,
        inplace=True
    )

    report.append("Reset dataframe index.")

    return cleaned_df, report