import pandas as pd

data = {
    "Name": ["Priya", None, "Kriti"],
    "Age": [45, None, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)

# fill default value
df.fillna({
    "Name": "Unknown",
    "Age": 0
}, inplace=True)
print(df)

# print(df.isnull().sum())
'''
.isnull().sum()
it will return count with column name like in which column how many values are None.
'''

# df.dropna(axis=0, inplace=True)
'''
0 = row
1 = column

What is inplace?
The inplace parameter tells Pandas:
"Should I modify the original DataFrame directly, or should I create a new DataFrame with the changes?"
'''


