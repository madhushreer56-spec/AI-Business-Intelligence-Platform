from reportlab.platypus import *

from reportlab.lib.styles import getSampleStyleSheet

import pandas as pd


def generate_report(df: pd.DataFrame):

    filename = "Business_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(

        Paragraph(

            "AI Business Intelligence Report",

            styles["Title"]

        )

    )

    story.append(Spacer(1,20))

    story.append(

        Paragraph(

            f"Rows : {df.shape[0]}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"Columns : {df.shape[1]}",

            styles["Normal"]

        )

    )

    story.append(Spacer(1,20))

    story.append(

        Paragraph(

            "Columns",

            styles["Heading2"]

        )

    )

    for col in df.columns:

        story.append(

            Paragraph(

                col,

                styles["Normal"]

            )

        )

    story.append(Spacer(1,20))

    story.append(

        Paragraph(

            "Missing Values",

            styles["Heading2"]

        )

    )

    missing = df.isnull().sum()

    for col, value in missing.items():

        story.append(

            Paragraph(

                f"{col} : {value}",

                styles["Normal"]

            )

        )

    story.append(Spacer(1,20))

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:

        story.append(

            Paragraph(

                "Statistics",

                styles["Heading2"]

            )

        )

        stats = numeric.describe().transpose()

        for column in stats.index:

            story.append(

                Paragraph(

                    f"<b>{column}</b>",

                    styles["Normal"]

                )

            )

            story.append(

                Paragraph(

                    f"Mean : {stats.loc[column,'mean']:.2f}",

                    styles["Normal"]

                )

            )

            story.append(

                Paragraph(

                    f"Minimum : {stats.loc[column,'min']:.2f}",

                    styles["Normal"]

                )

            )

            story.append(

                Paragraph(

                    f"Maximum : {stats.loc[column,'max']:.2f}",

                    styles["Normal"]

                )

            )

            story.append(Spacer(1,10))

    doc.build(story)

    return filename