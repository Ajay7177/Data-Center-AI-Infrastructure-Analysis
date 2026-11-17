-- 1. Create Database
CREATE DATABASE data_center_analysis;

USE data_center_analysis;

-- 2. Create Projects Table

CREATE TABLE data_center_projects (
    Project_ID VARCHAR(20) PRIMARY KEY,
    Company VARCHAR(100),
    Announcement_Date DATE,
    Year INT,
    Country VARCHAR(100),
    Region VARCHAR(100),
    City VARCHAR(100),
    Infrastructure_Type VARCHAR(100),
    AI_Focused VARCHAR(10),
    Capacity_MW DECIMAL(12,2),
    Investment_USD DECIMAL(18,2),
    Project_Status VARCHAR(50)
);

-- Import the CSV into this table using MySQL Workbench:
-- Right-click the table > Table Data Import Wizard.

-- 3. Total Projects by Year
SELECT
    Year,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Year
ORDER BY Year;

-- 4. Total Investment by Year
SELECT
    Year,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Year
ORDER BY Year;

-- 5. AI vs Traditional Projects
SELECT
    AI_Focused,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY AI_Focused;

-- 6. Country-wise Project Count
SELECT
    Country,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Country
ORDER BY Total_Projects DESC;

-- 7. Country-wise Investment
SELECT
    Country,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Country
ORDER BY Investment_Billion_USD DESC;

-- 8. Investment by Infrastructure Type
SELECT
    Infrastructure_Type,
    ROUND(SUM(Investment_USD) / 1000000000, 2) AS Investment_Billion_USD
FROM data_center_projects
GROUP BY Infrastructure_Type
ORDER BY Investment_Billion_USD DESC;

-- 9. Average Investment by AI Focus
SELECT
    AI_Focused,
    ROUND(AVG(Investment_USD), 2) AS Average_Investment_USD
FROM data_center_projects
GROUP BY AI_Focused;

-- 10. Average Capacity by AI Focus
SELECT
    AI_Focused,
    ROUND(AVG(Capacity_MW), 2) AS Average_Capacity_MW
FROM data_center_projects
GROUP BY AI_Focused;

-- 11. Project Status Summary
SELECT
    Project_Status,
    COUNT(*) AS Total_Projects
FROM data_center_projects
GROUP BY Project_Status
ORDER BY Total_Projects DESC;

-- 12. AI Project Share by Year
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