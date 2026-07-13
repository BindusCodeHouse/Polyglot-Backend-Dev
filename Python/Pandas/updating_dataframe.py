import pandas as pd

data = {
    "Name": ["Priya", "kajal", "Kriti"],
    "Age": [45, 30, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
print("Before")
print(df)

# .loc[]
# df.loc[row_index, columnName]

df.loc[0, "Name"] = "Swara"
print("After")
print(df)