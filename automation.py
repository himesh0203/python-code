Install Required Libraries
pip install pandas numpy matplotlib seaborn pdfkit jinja2


You also need wkhtmltopdf installed on your system for pdfkit to work.

On Windows: https://wkhtmltopdf.org/downloads.html

On macOS (Homebrew): brew install wkhtmltopdf

On Linux: sudo apt install wkhtmltopdf




Project Structure
automated_data_analysis/
│
├── analysis.py
├── templates/
│   └── report_template.html
├── data/
│   └── sample_data.csv
└── results/



HTML Template (templates/report_template.html)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automated Data Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #333; }
        img { max-width: 600px; display: block; margin-bottom: 20px; }
        table { border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 5px 10px; }
    </style>
</head>
<body>
    <h1>Automated Data Analysis Report</h1>
    
    <h2>Descriptive Statistics</h2>
    {{ descriptive_table|safe }}
    
    <h2>Department-wise Average Salary</h2>
    {{ dept_salary_table|safe }}
    <img src="{{ avg_salary_plot }}" alt="Average Salary by Department">
    
    <h2>Age Distribution</h2>
    <img src="{{ age_distribution_plot }}" alt="Age Distribution">
    
    <h2>Correlation Heatmap</h2>
    <img src="{{ correlation_plot }}" alt="Correlation Heatmap">
</body>
</html>




analysis.py – Automated Script
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pdfkit
from jinja2 import Environment, FileSystemLoader

# Ensure results folder exists
os.makedirs("results", exist_ok=True)

# Load data
data = pd.read_csv('data/sample_data.csv')

# -------------------------------
# Data Cleaning
# -------------------------------
for col in data.columns:
    if data[col].dtype in [np.float64, np.int64]:
        data[col].fillna(data[col].mean(), inplace=True)
    else:
        data[col].fillna(data[col].mode()[0], inplace=True)

# -------------------------------
# Analysis
# -------------------------------
descriptive_stats = data.describe().round(2).to_html()
dept_salary = data.groupby('Department')['Salary'].mean().round(2)
dept_salary_table = dept_salary.to_frame().to_html()

# -------------------------------
# Visualizations
# -------------------------------
# Average salary by department
avg_salary_plot = 'results/avg_salary_by_department.png'
plt.figure(figsize=(8,6))
sns.barplot(x=dept_salary.index, y=dept_salary.values)
plt.title("Average Salary by Department")
plt.ylabel("Salary")
plt.xlabel("Department")
plt.tight_layout()
plt.savefig(avg_salary_plot)
plt.close()

# Age distribution
age_distribution_plot = 'results/age_distribution.png'
plt.figure(figsize=(8,6))
sns.histplot(data['Age'], bins=5, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(age_distribution_plot)
plt.close()

# Correlation heatmap
corr_matrix = data.corr()
correlation_plot = 'results/correlation_heatmap.png'
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(correlation_plot)
plt.close()

# -------------------------------
# Generate HTML report
# -------------------------------
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')

html_out = template.render(
    descriptive_table=descriptive_stats,
    dept_salary_table=dept_salary_table,
    avg_salary_plot=avg_salary_plot,
    age_distribution_plot=age_distribution_plot,
    correlation_plot=correlation_plot
)

html_file = 'results/report.html'
with open(html_file, 'w') as f:
    f.write(html_out)

# -------------------------------
# Convert HTML to PDF
# -------------------------------
pdf_file = 'results/report.pdf'
pdfkit.from_file(html_file, pdf_file)

# -------------------------------
# Save cleaned data
# -------------------------------
data.to_csv('results/cleaned_data.csv', index=False)

print("Automation complete! Check the 'results/' folder for outputs.")
