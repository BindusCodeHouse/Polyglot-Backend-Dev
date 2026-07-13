import pandas as pd

data = {
    "Name": ["Priya", "kajal", "Kriti"],
    "Age": [45, 30, 20],
    "City": ["Ahmedavad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
print(df.info())   # it return all information about data like row, column or null count
print(df.shape)
print(df.columns)

# df.to_csv("output.csv", index=False)  # index false remove index column from table.
# df.to_json("output.json")

