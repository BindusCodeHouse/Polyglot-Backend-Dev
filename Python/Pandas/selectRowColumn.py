'''
1. select specific Row
2. select specific Column
3. filter Rows
4. combine multiple condition
'''

import pandas as pd

data = {
    "Name": ["Priya", "kajal", "Kriti"],
    "Age": [45, 30, 20],
    "City": ["Ahmedavad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
print(df["Name"])    # select single column
print(df[["Name","Age"]])  # select multiple column
print(df[df["Age"] > 30])  # filter record

filtered_df = df[(df["Age"] > 30) & (df["City"] == "Ahmedavad")]
print(filtered_df)
