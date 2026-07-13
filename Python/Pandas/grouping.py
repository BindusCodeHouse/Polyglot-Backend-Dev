import pandas as pd

data = {
    "Name":["Varun","Karan","Marun","Tarun","Karan"],
    "Age":[33,22,11,33,11],
    "Salary":[100000,200000,150000,80000,100000]
}

df = pd.DataFrame(data)

# Group In Single Column
# grouped = df.groupby("Age")["Salary"].sum()

# Group In Multiple Column
grouped = df.groupby(["Age","Name"])["Salary"].sum()
print(grouped)
