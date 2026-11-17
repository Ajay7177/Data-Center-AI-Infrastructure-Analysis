CREATE DATABASE IF NOT EXISTS data_center_analysis;
USE data_center_analysis;

USE data_center_analysis;

SELECT COUNT(*) AS total_rows
FROM data_center_projects;

SELECT *
FROM data_center_projects
LIMIT 10;

-- number of data center projects for each year from 2019 to 2026
 
SELECT
    Year,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Year
ORDER BY Year;

-- total investment by year:
SELECT
    Year,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Year
ORDER BY Year;

-- AI-focused vs. traditional data center projects
SELECT
    AI_Focused,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY AI_Focused;

-- top 10 countries by project count:
SELECT
    Country,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Country
ORDER BY Total_Projects DESC
LIMIT 10;

-- top 10 countries by total investment
SELECT
    Country,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Country
ORDER BY Investment_Billion_USD DESC
LIMIT 10;

-- nvestment by infrastructure type
SELECT
    Infrastructure_Type,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Infrastructure_Type
ORDER BY Investment_Billion_USD DESC;

-- average investment for AI-focused vs. traditional projects
SELECT
    AI_Focused,
    ROUND(AVG(Investment_USD), 2) AS Average_Investment_USD
FROM data_center_projects
GROUP BY AI_Focused;

-- average project capacity by AI focus
SELECT
    AI_Focused,
    ROUND(AVG(Capacity_MW), 2) AS Average_Capacity_MW
FROM data_center_projects
GROUP BY AI_Focused;

-- project status distribution (how many projects are planned, under construction, or operational.)
SELECT
    Project_Status,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Project_Status
ORDER BY Total_Projects DESC;

-- calculate the percentage of AI-focused projects by year
SELECT
    Year,
    COUNT(*) AS Total_Projects,
    SUM(CASE WHEN AI_Focused = 'Yes' THEN 1 ELSE 0 END) AS AI_Projects,
    ROUND(
        100.0 * SUM(CASE WHEN AI_Focused = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS AI_Project_Percentage
FROM data_center_projects
GROUP BY Year
ORDER BY Year;



SELECT
    p.Company,
    c.Company_Type,
    c.HQ_Country,
    COUNT(*) AS Total_Projects,
    ROUND(SUM(p.Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects p
INNER JOIN companies c
    ON p.Company = c.Company
GROUP BY
    p.Company,
    c.Company_Type,
    c.HQ_Country
ORDER BY Total_Projects DESC;