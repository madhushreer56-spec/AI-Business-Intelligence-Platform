import re
import pandas as pd

from ai.gemini_client import generate_content
from ai.prompts import AI_PROMPT


# ==========================================================
# DATASET INFORMATION
# ==========================================================

def build_dataset_info(df):

    info = []

    for column in df.columns:

        dtype = str(df[column].dtype)

        unique_values = df[column].dropna().unique()

        if len(unique_values) <= 15:

            values = ", ".join(
                str(v) for v in unique_values[:15]
            )

        else:

            values = f"{len(unique_values)} unique values"

        info.append(
            f"- {column} | type: {dtype} | values: {values}"
        )

    return "\n".join(info)


# ==========================================================
# CLEAN SQL
# ==========================================================

def clean_sql(sql):

    sql = sql.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```SQL", "")
    sql = sql.replace("```", "")

    sql = sql.strip()

    match = re.search(
        r"(SELECT\s.+)",
        sql,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        sql = match.group(1).strip()

    # Remove anything after a closing semicolon
    if ";" in sql:

        sql = sql.split(";")[0] + ";"

    return sql


# ==========================================================
# VALIDATE SQL
# ==========================================================

def validate_sql(sql):

    sql_upper = sql.strip().upper()

    if not sql_upper.startswith("SELECT"):

        raise ValueError(
            "AI generated a non-SELECT query. "
            "Only SELECT queries are allowed."
        )

    forbidden = [
        "DROP ",
        "DELETE ",
        "UPDATE ",
        "INSERT ",
        "ALTER ",
        "CREATE ",
        "ATTACH ",
        "DETACH ",
        "PRAGMA ",
        "REPLACE ",
        "VACUUM "
    ]

    for keyword in forbidden:

        if keyword in sql_upper:

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True


# ==========================================================
# PARSE GEMINI RESPONSE
# ==========================================================

def parse_ai_response(response):

    sql_match = re.search(
        r"SQL:\s*(.*?)(?=\n\s*Chart:)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    chart_match = re.search(
        r"Chart:\s*(.*?)(?=\n\s*Insight:)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    insight_match = re.search(
        r"Insight:\s*(.*)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    if not sql_match:

        raise ValueError(
            "Gemini did not return a valid SQL query."
        )

    sql = clean_sql(
        sql_match.group(1)
    )

    chart = (
        chart_match.group(1).strip()
        if chart_match
        else "Table"
    )

    insight = (
        insight_match.group(1).strip()
        if insight_match
        else ""
    )

    allowed_charts = [
        "Bar Chart",
        "Line Chart",
        "Pie Chart",
        "Scatter Plot",
        "Histogram",
        "Table"
    ]

    # Gemini sometimes adds extra text
    for allowed in allowed_charts:

        if allowed.lower() in chart.lower():

            chart = allowed
            break

    else:

        chart = "Table"

    validate_sql(sql)

    return sql, chart, insight


# ==========================================================
# GENERATE RESULT-SPECIFIC BUSINESS INSIGHT
# ==========================================================

def generate_result_insight(question, result_df):

    if result_df is None or result_df.empty:

        return (
            "No matching records were found for this question."
        )

    result_text = result_df.to_string(
        index=False
    )

    prompt = f"""
You are an expert Business Intelligence analyst.

The user asked:

{question}

The SQL query has already been executed successfully.

Here is the ACTUAL SQL RESULT:

{result_text}

Analyze ONLY the actual result shown above.

Your answer MUST:

1. Directly answer the user's question.
2. Mention the important actual values from the result.
3. Compare categories when appropriate.
4. Do not invent numbers.
5. Do not make assumptions that are not supported by the result.
6. If percentages are present, explain them clearly.
7. Keep the answer under 120 words.
8. Mention that the result represents this dataset when appropriate.

Return the answer in this format:

Summary:
<direct answer>

Business Insight:
<important finding from the actual result>

Recommendation:
<short useful recommendation, if appropriate>
"""

    try:

        return generate_content(prompt)

    except Exception:

        return (
            "The analysis was completed successfully, "
            "but Gemini could not generate the detailed "
            "business insight."
        )


# ==========================================================
# MAIN AI FUNCTION
# ==========================================================

def ask_ai(question, df):

    dataset_info = build_dataset_info(df)

    sample_data = df.head(10).to_string(
        index=False
    )

    prompt = AI_PROMPT.format(
        columns=dataset_info,
        dataset_info=dataset_info,
        sample_data=sample_data,
        question=question
    )

    # ----------------------------------------------
    # Ask Gemini for SQL + chart
    # ----------------------------------------------

    response = generate_content(prompt)

    sql, chart_type, _ = parse_ai_response(
        response
    )

    return sql, chart_type