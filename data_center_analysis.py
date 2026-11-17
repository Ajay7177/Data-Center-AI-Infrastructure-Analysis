import pandas as pd

df = pd.read_csv("data/data_center_projects_synthetic.csv")

print(df.head())   #to check the data loaded properly we see the top 5 rows
print(df.shape)
print(df.columns)
df.info()

print(df.isnull().sum()) #find missing value and count of them

print(df.duplicated().sum())   # find duplicate and count them

df = df.drop_duplicates()  #removing duplicates

print(df.shape)


df["City"] = df["City"].fillna("Unknown") #handling missing values


print(df["Investment_USD"].isnull().sum())

print(df["Project_ID"].duplicated().sum())

df["Country"] =df["Country"].replace("USA","United States")   #replacing values

df["AI_Focused"] =df["AI_Focused"].replace("yes","Yes")   #replacing values




#--------------------EDA---------------------------

project_count_each_year = df.groupby("Year")["Project_ID"].count()

print("\nproject_count_each_year")
print(project_count_each_year)


#Visualize Project Count by Year

import matplotlib.pyplot as plt

project_count_each_year.plot(kind="bar", figsize=(10, 5))

plt.title("Number of Data Center Projects by Year")
plt.xlabel("Year")
plt.ylabel("Number of Projects")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


#Total Investment by Year

investment_by_year = df.groupby("Year")["Investment_USD"].sum()

print("\n--- Total Investment by Year ---")
print(investment_by_year)

# Visualize Investment by Year

investment_by_year_billion = investment_by_year / 1_000_000_000

investment_by_year_billion.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Total Data Center Investment by Year")
plt.xlabel("Year")
plt.ylabel("Investment (USD Billions)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


# AI-Focused vs Traditional Projects

ai_project_counts = df["AI_Focused"].value_counts()

print("\n--- AI-Focused vs Traditional Projects ---")
print(ai_project_counts)


#Visualize AI-Focused vs Traditional Projects

ai_project_counts.plot(
    kind="bar",
    figsize=(7, 5)
)

plt.title("AI-Focused vs Traditional Data Center Projects")
plt.xlabel("AI-Focused")
plt.ylabel("Number of Projects")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()



# Calculate AI-focused project percentage
total_projects = len(df)
ai_projects = (df["AI_Focused"] == "Yes").sum()

ai_percentage = (ai_projects / total_projects) * 100

print(f"\nAI-focused projects: {ai_projects}")
print(f"Total projects: {total_projects}")
print(f"AI-focused percentage: {ai_percentage:.2f}%")


# AI-Focused Project Percentage by Year

# Count AI-focused projects for each year
ai_projects_by_year = df[df["AI_Focused"] == "Yes"].groupby("Year")["Project_ID"].count()

# Count all projects for each year
total_projects_by_year = df.groupby("Year")["Project_ID"].count()

# Calculate the percentage
ai_share_by_year = (ai_projects_by_year / total_projects_by_year) * 100

print("\n--- AI-Focused Project Percentage by Year ---")
print(ai_share_by_year.round(2))


# Visualize AI-Focused Project Trend

ai_share_by_year.plot(
    kind="line",
    marker="o",
    figsize=(10, 5)
)

plt.title("Growth of AI-Focused Data Center Projects")
plt.xlabel("Year")
plt.ylabel("AI-Focused Projects (%)")
plt.xticks(ai_share_by_year.index)
plt.grid(True)
plt.tight_layout()
plt.show()


# Data Center Projects by Country

projects_by_country = df["Country"].value_counts()

print("\n--- Data Center Projects by Country ---")
print(projects_by_country)


# Visualize Projects by Country

projects_by_country.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Number of Data Center Projects by Country")
plt.xlabel("Country")
plt.ylabel("Number of Projects")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# Top 5 countries by project count

top_5_countries = projects_by_country.head(5)

print("\n--- Top 5 Countries by Project Count ---")
print(top_5_countries)


# Total Investment by Country

investment_by_country = (
    df.groupby("Country")["Investment_USD"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Total Investment by Country ---")
print((investment_by_country / 1_000_000_000).round(2))

# Top 10 Countries by Investment

top_10_investment = investment_by_country.head(10) / 1_000_000_000

top_10_investment.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Top 10 Countries by Data Center Investment")
plt.xlabel("Country")
plt.ylabel("Investment (USD Billions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Investment by Infrastructure Type

investment_by_type = (
    df.groupby("Infrastructure_Type")["Investment_USD"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Investment by Infrastructure Type ---")
print((investment_by_type / 1_000_000_000).round(2))

# Visualize Investment by Infrastructure Type

investment_by_type_billion = investment_by_type / 1_000_000_000

investment_by_type_billion.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Investment by Infrastructure Type")
plt.xlabel("Infrastructure Type")
plt.ylabel("Investment (USD Billions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Average Investment per Project by Infrastructure Type

average_investment_by_type = (
    df.groupby("Infrastructure_Type")["Investment_USD"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- Average Investment per Project by Infrastructure Type ---")
print((average_investment_by_type / 1_000_000).round(2))

# Visualize Average Investment per Project

average_investment_million = average_investment_by_type / 1_000_000

average_investment_million.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Average Investment per Project by Infrastructure Type")
plt.xlabel("Infrastructure Type")
plt.ylabel("Average Investment (USD Millions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Project Status Analysis

project_status_counts = df["Project_Status"].value_counts()

print("\n--- Project Count by Status ---")
print(project_status_counts)


# Visualize Project Status

project_status_counts.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Data Center Projects by Status")
plt.xlabel("Project Status")
plt.ylabel("Number of Projects")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Investment by AI Focus

investment_by_ai_focus = (
    df.groupby("AI_Focused")["Investment_USD"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Investment by AI Focus ---")
print((investment_by_ai_focus / 1_000_000_000).round(2))

# Visualize Investment by AI Focus

investment_by_ai_focus_billion = investment_by_ai_focus / 1_000_000_000

investment_by_ai_focus_billion.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Investment: AI-Focused vs Non-AI-Focused Projects")
plt.xlabel("AI-Focused Project")
plt.ylabel("Investment (USD Billions)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Average Investment by AI Focus

average_investment_by_ai = (
    df.groupby("AI_Focused")["Investment_USD"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- Average Investment per Project by AI Focus ---")
print((average_investment_by_ai / 1_000_000).round(2))

# Visualize Average Investment by AI Focus

average_investment_ai_million = average_investment_by_ai / 1_000_000

average_investment_ai_million.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Average Investment per Project: AI vs Non-AI")
plt.xlabel("AI-Focused Project")
plt.ylabel("Average Investment (USD Millions)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# Average Capacity by AI Focus

average_capacity_by_ai = (
    df.groupby("AI_Focused")["Capacity_MW"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- Average Project Capacity by AI Focus ---")
print(average_capacity_by_ai.round(2))


# Visualize Average Capacity by AI Focus

average_capacity_by_ai.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Average Data Center Capacity: AI vs Non-AI")
plt.xlabel("AI-Focused Project")
plt.ylabel("Average Capacity (MW)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Average Project Capacity by Year

average_capacity_by_year = (
    df.groupby("Year")["Capacity_MW"]
    .mean()
)

print("\n--- Average Project Capacity by Year ---")
print(average_capacity_by_year.round(2))

# Visualize Average Project Capacity by Year

average_capacity_by_year.plot(
    kind="line",
    marker="o",
    figsize=(10, 5)
)

plt.title("Average Data Center Project Capacity by Year")
plt.xlabel("Year")
plt.ylabel("Average Capacity (MW)")
plt.xticks(average_capacity_by_year.index)
plt.grid(True)
plt.tight_layout()
plt.show()

# Project Count by Infrastructure Type

projects_by_type = df["Infrastructure_Type"].value_counts()

print("\n--- Project Count by Infrastructure Type ---")
print(projects_by_type)

# Visualize Project Count by Infrastructure Type

projects_by_type.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Number of Projects by Infrastructure Type")
plt.xlabel("Infrastructure Type")
plt.ylabel("Number of Projects")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# AI-Focused Projects by Country

ai_projects_by_country = (
    df[df["AI_Focused"] == "Yes"]
    .groupby("Country")["Project_ID"]
    .count()
    .sort_values(ascending=False)
)

print("\n--- AI-Focused Projects by Country ---")
print(ai_projects_by_country)

# Visualize Top 10 Countries by AI-Focused Projects

top_10_ai_countries = ai_projects_by_country.head(10)

top_10_ai_countries.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Top 10 Countries by AI-Focused Project Count")
plt.xlabel("Country")
plt.ylabel("Number of AI-Focused Projects")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# AI-Focused Investment by Country

ai_investment_by_country = (
    df[df["AI_Focused"] == "Yes"]
    .groupby("Country")["Investment_USD"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- AI-Focused Investment by Country (USD Billions) ---")
print((ai_investment_by_country / 1_000_000_000).round(2))

# Visualize Top 10 Countries by AI-Focused Investment

top_10_ai_investment = (
    ai_investment_by_country.head(10) / 1_000_000_000
)

top_10_ai_investment.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Top 10 Countries by AI-Focused Investment")
plt.xlabel("Country")
plt.ylabel("Investment (USD Billions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# Investment per MW by AI Focus

df["Investment_Per_MW"] = (
    df["Investment_USD"] / df["Capacity_MW"]
)

average_investment_per_mw = (
    df.groupby("AI_Focused")["Investment_Per_MW"]
    .mean()
)

print("\n--- Average Investment per MW by AI Focus ---")
print((average_investment_per_mw / 1_000_000).round(2))

# Visualize Average Investment per MW by AI Focus

average_investment_per_mw_million = (
    average_investment_per_mw / 1_000_000
)

average_investment_per_mw_million.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Average Investment per MW: AI vs Non-AI")
plt.xlabel("AI-Focused Project")
plt.ylabel("Average Investment (USD Millions per MW)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()




# Generate automated PDF report

from report import create_report

create_report(df)