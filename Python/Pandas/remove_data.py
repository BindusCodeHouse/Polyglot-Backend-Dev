import pandas as pd

data = {
    "Name": ["Priya", "kajal", "Kriti"],
    "Age": [45, 30, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
print("Before")
print(df)

# .drop(columns = ["ColumnName"], inplace=True)
df.drop(columns=["City"], inplace=True)
print("After")
print(df)