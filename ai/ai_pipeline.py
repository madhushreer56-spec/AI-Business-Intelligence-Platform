from ai.gemini_client import generate_content
from ai.fallback import local_sql


def ask_ai(question, columns):

    prompt = f"""
You are an Expert Business Intelligence Assistant.

Database Table:
sales

Available Columns:
{", ".join(columns)}

User Question:
{question}

Return EXACTLY in this format.

SQL:
<SQLite Query>

CHART:
Choose ONLY ONE from:

Bar Chart
Line Chart
Pie Chart
Scatter Plot
Histogram
Table

INSIGHT:
Professional business insight under 120 words.

Rules:

1. SQLite only.
2. Do not explain SQL.
3. No markdown.
4. No ```sql.
5. Return exactly SQL, CHART and INSIGHT.
"""

    try:

        text = generate_content(prompt)

    except Exception:

        # ---------------------------------
        # Offline Business Intelligence Mode
        # ---------------------------------

        return local_sql(question)

    sql = ""
    chart = "Table"
    insight = ""

    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper = line.upper()

        # -----------------------------
        # SQL
        # -----------------------------

        if upper.startswith("SQL:"):

            current_section = "sql"

            sql = line[4:].strip()

            continue

        # -----------------------------
        # CHART
        # -----------------------------

        elif upper.startswith("CHART:"):

            current_section = "chart"

            chart = line[6:].strip()

            continue

        # -----------------------------
        # INSIGHT
        # -----------------------------

        elif upper.startswith("INSIGHT:"):

            current_section = "insight"

            insight = line[8:].strip()

            continue

        # -----------------------------
        # Continue current section
        # -----------------------------

        if current_section == "sql":

            sql += " " + line

        elif current_section == "chart":

            chart += " " + line

        elif current_section == "insight":

            insight += "\n" + line

    sql = sql.strip()

    chart = chart.strip()

    insight = insight.strip()

    if chart == "":

        chart = "Table"

    return (

        sql,

        chart,

        insight

    )