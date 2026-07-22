import pandas as pd


def generate_local_insight(question, result_df: pd.DataFrame):

    if result_df.empty:
        return """
### Summary
No records were returned.

### Business Insight
The query did not match any available data.

### Recommendation
Try asking a different question or verify the dataset.
"""

    summary = f"The query returned {len(result_df)} record(s)."

    recommendation = "Use this information to support business decision making."

    # Numeric Summary
    numeric_cols = result_df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        col = numeric_cols[0]

        total = result_df[col].sum()

        avg = result_df[col].mean()

        maximum = result_df[col].max()

        summary += (
            f"\n\nTotal {col}: {total:,.2f}"
            f"\nAverage {col}: {avg:,.2f}"
            f"\nMaximum {col}: {maximum:,.2f}"
        )

        recommendation = (
            f"Monitor '{col}' regularly to improve business performance."
        )

    return f"""
### Summary

{summary}

### Business Insight

The data has been analyzed successfully using local analytics.

### Recommendation

{recommendation}
"""