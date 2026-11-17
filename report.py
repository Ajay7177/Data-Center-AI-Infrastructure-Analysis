import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)


# --------------------------------------------------
# OUTPUT FOLDERS
# --------------------------------------------------

OUTPUT_DIR = "outputs"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")
CLEANED_DIR = os.path.join(OUTPUT_DIR, "cleaned_data")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)


# --------------------------------------------------
# CHART GENERATION
# --------------------------------------------------

def save_chart(series, title, xlabel, ylabel, filename,
               chart_type="bar", convert_to_billions=False):

    plot_data = series.copy()

    if convert_to_billions:
        plot_data = plot_data / 1_000_000_000

    fig, ax = plt.subplots(figsize=(8, 4.5))

    if chart_type == "line":
        plot_data.plot(kind="line", marker="o", ax=ax)
    else:
        plot_data.plot(kind="bar", ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    chart_path = os.path.join(CHART_DIR, filename)
    fig.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return chart_path


# --------------------------------------------------
# PDF REPORT GENERATION
# --------------------------------------------------

def create_report(df):

    print("\nGenerating Data Center Investment PDF Report...")

    # Save cleaned dataset
    cleaned_path = os.path.join(
        CLEANED_DIR,
        "cleaned_data_center_projects.csv"
    )

    df.to_csv(cleaned_path, index=False)

    # Save statistical summary
    summary_path = os.path.join(
        OUTPUT_DIR,
        "statistical_summary.csv"
    )

    df.describe(include="all").transpose().to_csv(summary_path)

    # --------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------

    total_projects = len(df)

    ai_projects = (df["AI_Focused"] == "Yes").sum()

    ai_share = (
        ai_projects / total_projects * 100
        if total_projects else 0
    )

    total_investment = df["Investment_USD"].sum()

    average_investment = df["Investment_USD"].mean()

    average_capacity = df["Capacity_MW"].mean()

    missing_values = int(df.isnull().sum().sum())

    # Yearly project counts
    projects_by_year = (
        df.groupby("Year")["Project_ID"]
        .count()
        .sort_index()
    )

    # Yearly investment
    investment_by_year = (
        df.groupby("Year")["Investment_USD"]
        .sum()
        .sort_index()
    )

    # AI share by year
    ai_by_year = (
        df[df["AI_Focused"] == "Yes"]
        .groupby("Year")["Project_ID"]
        .count()
    )

    total_by_year = (
        df.groupby("Year")["Project_ID"]
        .count()
    )

    ai_share_by_year = (
        ai_by_year.reindex(total_by_year.index, fill_value=0)
        / total_by_year
        * 100
    )

    # Project status
    status_counts = df["Project_Status"].value_counts()

    # Investment by infrastructure type
    investment_by_type = (
        df.groupby("Infrastructure_Type")["Investment_USD"]
        .sum()
        .sort_values(ascending=False)
    )

    # Country analysis
    projects_by_country = df["Country"].value_counts()

    investment_by_country = (
        df.groupby("Country")["Investment_USD"]
        .sum()
        .sort_values(ascending=False)
    )

    # --------------------------------------------------
    # SAVE CHARTS
    # --------------------------------------------------

    chart_paths = []

    chart_paths.append(save_chart(
        projects_by_year,
        "Data Center Projects by Year",
        "Year",
        "Number of Projects",
        "projects_by_year.png"
    ))

    chart_paths.append(save_chart(
        investment_by_year,
        "Total Investment by Year",
        "Year",
        "Investment (USD Billions)",
        "investment_by_year.png",
        convert_to_billions=True
    ))

    chart_paths.append(save_chart(
        ai_share_by_year,
        "AI-Focused Project Share by Year",
        "Year",
        "AI-Focused Projects (%)",
        "ai_share_by_year.png",
        chart_type="line"
    ))

    chart_paths.append(save_chart(
        status_counts,
        "Projects by Status",
        "Project Status",
        "Number of Projects",
        "projects_by_status.png"
    ))

    chart_paths.append(save_chart(
        investment_by_type,
        "Investment by Infrastructure Type",
        "Infrastructure Type",
        "Investment (USD Billions)",
        "investment_by_type.png",
        convert_to_billions=True
    ))

    chart_paths.append(save_chart(
        projects_by_country.head(10),
        "Top 10 Countries by Project Count",
        "Country",
        "Number of Projects",
        "top_countries.png"
    ))

    # --------------------------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------------------------

    peak_project_year = projects_by_year.idxmax()

    highest_investment_year = investment_by_year.idxmax()

    top_country = (
        projects_by_country.index[0]
        if not projects_by_country.empty
        else "Not available"
    )

    top_infrastructure = (
        investment_by_type.index[0]
        if not investment_by_type.empty
        else "Not available"
    )

    insights = [
        f"Total projects in the cleaned dataset: {total_projects}.",

        f"AI-focused projects: {ai_projects}, representing "
        f"{ai_share:.2f}% of all projects.",

        f"Year with the highest project count: "
        f"{peak_project_year}.",

        f"Year with the highest total recorded investment: "
        f"{highest_investment_year}.",

        f"Country with the most projects: {top_country}.",

        f"Infrastructure type with the highest total investment: "
        f"{top_infrastructure}.",

        f"Average recorded project investment: "
        f"${average_investment:,.2f}.",

        f"Average project capacity: {average_capacity:,.2f} MW.",

        f"Missing values remaining in the dataset: {missing_values}."
    ]

    insights_path = os.path.join(
        OUTPUT_DIR,
        "business_insights.txt"
    )

    with open(insights_path, "w", encoding="utf-8") as file:
        file.write(
            "DATA CENTER & AI INFRASTRUCTURE INVESTMENT ANALYSIS\n\n"
        )

        for insight in insights:
            file.write("- " + insight + "\n")

        file.write(
            "\nNote: This project uses synthetic data. "
            "Findings are illustrative and are not verified "
            "real-world investment figures.\n"
        )

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    pdf_path = os.path.join(
        REPORT_DIR,
        "Data_Center_AI_Investment_Report.pdf"
    )

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=23,
        spaceAfter=15
    ))

    story = []

    # Title
    story.append(Paragraph(
        "Data Center & AI Infrastructure Investment Trend Analysis",
        styles["ReportTitle"]
    ))

    story.append(Paragraph(
        "Automated Exploratory Data Analysis Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Project Objective",
        styles["Heading1"]
    ))

    story.append(Paragraph(
        "This project analyzes data center projects, investment, "
        "infrastructure types, project status, country distribution, "
        "and AI-focused development using Python and Pandas.",
        styles["BodyText"]
    ))

    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Dataset Summary",
        styles["Heading1"]
    ))

    summary_data = [
        ["Metric", "Value"],
        ["Total Projects", f"{total_projects:,}"],
        ["AI-Focused Projects", f"{ai_projects:,}"],
        ["AI-Focused Project Share", f"{ai_share:.2f}%"],
        [
            "Total Recorded Investment",
            f"${total_investment / 1_000_000_000:,.2f} billion"
        ],
        [
            "Average Project Investment",
            f"${average_investment:,.2f}"
        ],
        ["Average Project Capacity", f"{average_capacity:,.2f} MW"],
        ["Missing Values Remaining", str(missing_values)]
    ]

    table = Table(summary_data, colWidths=[250, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(table)
    story.append(Spacer(1, 18))

    # Business insights
    story.append(Paragraph(
        "Key Business Insights",
        styles["Heading1"]
    ))

    for insight in insights:
        story.append(Paragraph(
            "- " + insight,
            styles["BodyText"]
        ))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Visual Analysis",
        styles["Heading1"]
    ))

    for chart_path in chart_paths:
        story.append(Spacer(1, 10))

        story.append(Image(
            chart_path,
            width=6.5 * inch,
            height=3.5 * inch,
            kind="proportional"
        ))

    story.append(PageBreak())

    # Recommendations
    story.append(Paragraph(
        "Recommendations",
        styles["Heading1"]
    ))

    recommendations = [
        "Monitor yearly project counts and investment trends "
        "to understand changes in project activity.",

        "Compare AI-focused and traditional projects to understand "
        "how project characteristics differ.",

        "Review country and infrastructure-type distributions "
        "to identify areas with the highest recorded activity.",

        "Validate missing values, duplicate records, and inconsistent "
        "categories before interpreting analytical results.",

        "Use the Power BI dashboard for interactive exploration "
        "of project and investment trends."
    ]

    for recommendation in recommendations:
        story.append(Paragraph(
            "- " + recommendation,
            styles["BodyText"]
        ))
        story.append(Spacer(1, 8))

    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "<b>Data Disclaimer:</b> The project dataset is synthetic. "
        "The reported values and trends are illustrative and must "
        "not be interpreted as verified real-world investment data.",
        styles["BodyText"]
    ))

    # Create PDF
    document.build(story)

    print("\nPDF report generated successfully!")
    print("PDF:", pdf_path)
    print("Cleaned dataset:", cleaned_path)
    print("Statistical summary:", summary_path)
    print("Business insights:", insights_path)
    print("Charts saved in:", CHART_DIR)

    return pdf_path