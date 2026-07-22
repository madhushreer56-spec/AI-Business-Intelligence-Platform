import pandas as pd
from io import BytesIO


def dataframe_to_excel(df: pd.DataFrame):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")

    output.seek(0)

    return output


def dataframe_to_csv(df: pd.DataFrame):

    return df.to_csv(index=False).encode("utf-8")