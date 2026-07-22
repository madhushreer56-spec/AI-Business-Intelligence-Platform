from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_dashboard(df):

    summary = f"""
Dataset Summary

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column Names:
{list(df.columns)}

Statistics:
{df.describe(include='all').to_string()}
"""

    prompt = f"""
You are a Senior Business Analyst.

Analyze the following dashboard information and generate:

1. Executive Summary
2. Important KPIs
3. Business Trends
4. Risks
5. Recommendations

Dashboard Information:

{summary}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text