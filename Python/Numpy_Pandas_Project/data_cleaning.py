import numpy as np
import pandas as pd

data = pd.read_csv('employee_dirty_data.csv')

'''
print(data.head())
print(data.tail())
print(data.shape)
print(data.columns)
print(data.info())
print(data.describe())

print(data.isnull())
print(data.isnull().sum())

print(data.duplicated())
print(data.duplicated().sum())
'''

data.drop_duplicates(inplace=True)
data["Name"] = data["Name"].str.strip()
data.dropna(subset=["Name"], inplace=True)

data["Department"] = data["Department"].replace({
    "it":"IT",
    "finance":"Finance"
})

data.fillna( {"City":"Unknown","Department": "Unknown"}, inplace=True)

columns = ["Age", "Salary", "Experience"]
for col in columns:
    data[col] = data[col].fillna(0)
    data.loc[data[col]<0 , col] = 0

data["Bonus"] = data["Salary"] * 10 / 100

conditions = [
    data["Salary"] < 45000,
    (data["Salary"] >= 45000) & (data["Salary"] <= 60000),
    data["Salary"] >= 60000,
]

category = [
    "Low",
    "Medium",
    "High"
]

data.insert(5, "Salary_Category", np.select(conditions, category, default="Unknown"))

data.to_csv("employee_cleaned_data.csv", index=False)
print("✅ Cleaned data saved successfully!")
