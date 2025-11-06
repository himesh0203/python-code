Install Required Libraries
pip install pandas numpy matplotlib seaborn


Project Structure
data_analysis_project/
│
├── analysis.py
└── data/
    └── sample_data.csv


Sample CSV (data/sample_data.csv)
Name,Age,Department,Salary
Alice,30,HR,50000
Bob,35,IT,70000
Charlie,28,Finance,55000
Diana,40,IT,80000
Eve,25,HR,48000


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('data/sample_data.csv')

# Basic overview
print("First 5 rows of data:")
print(data.head())

print("\nData info:")
print(data.info())

print("\nDescriptive statistics:")
print(data.describe())

# Analysis examples
# Average salary
avg_salary = data['Salary'].mean()
print(f"\nAverage salary: {avg_salary}")

# Department-wise average salary
dept_salary = data.groupby('Department')['Salary'].mean()
print("\nAverage salary by department:")
print(dept_salary)

# Visualization
plt.figure(figsize=(8,6))
sns.barplot(x=dept_salary.index, y=dept_salary.values)
plt.title("Average Salary by Department")
plt.ylabel("Salary")
plt.xlabel("Department")
plt.show()

# Age distribution
plt.figure(figsize=(8,6))
sns.histplot(data['Age'], bins=5, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()
