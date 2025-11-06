Project Structure
advanced_data_analysis/
│
├── analysis.py
├── data/
│   └── sample_data.csv
└── results/

Make sure to create a results/ folder where the cleaned data and visualizations will be saved.



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# Load data
data = pd.read_csv('data/sample_data.csv')

# 1. Basic overview
print("First 5 rows:")
print(data.head())

print("\nData Info:")
print(data.info())

print("\nDescriptive Statistics:")
print(data.describe())

# 2. Handle missing values
print("\nChecking for missing values:")
print(data.isnull().sum())

# Fill missing numeric values with mean, categorical with mode
for col in data.columns:
    if data[col].dtype in [np.float64, np.int64]:
        data[col].fillna(data[col].mean(), inplace=True)
    else:
        data[col].fillna(data[col].mode()[0], inplace=True)

print("\nData after filling missing values:")
print(data.isnull().sum())

# 3. Analysis
# Average salary
avg_salary = data['Salary'].mean()
print(f"\nAverage salary: {avg_salary:.2f}")

# Department-wise average salary
dept_salary = data.groupby('Department')['Salary'].mean()
print("\nAverage salary by department:")
print(dept_salary)

# Correlation analysis
corr_matrix = data.corr()
print("\nCorrelation matrix:")
print(corr_matrix)

# Save correlation matrix
corr_matrix.to_csv('results/correlation_matrix.csv')

# 4. Visualizations
# Average salary by department
plt.figure(figsize=(8,6))
sns.barplot(x=dept_salary.index, y=dept_salary.values)
plt.title("Average Salary by Department")
plt.ylabel("Salary")
plt.xlabel("Department")
plt.savefig('results/avg_salary_by_department.png')
plt.close()

# Age distribution
plt.figure(figsize=(8,6))
sns.histplot(data['Age'], bins=5, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.savefig('results/age_distribution.png')
plt.close()

# Correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.savefig('results/correlation_heatmap.png')
plt.close()

# 5. Save cleaned data
data.to_csv('results/cleaned_data.csv', index=False)

print("\nAnalysis complete. Cleaned data and visualizations saved in 'results/' folder.")
