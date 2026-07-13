import pandas as pd

data = {
    "Name": ["Priya", "Kajal", "Kriti"],
    "Age": [45, 15, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)

# sorting single column data
# df.sort_values(by="Age", ascending=True, inplace=True)

# sorting multiple column data
df.sort_values(by=["Age","City"], ascending=[True,True], inplace=True)
print(df)