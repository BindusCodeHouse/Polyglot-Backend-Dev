import pandas as pd

data = {
    "Name": ["Priya", "kajal", "Kriti"],
    "Age": [45, 30, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
print("Before")
print(df)

# when you don't want to add column for particular index then you use
df["Future"] =df["Age"] + 10
print("After")
print(df)


# using insert() when you want to add column for particular position
# insert(index, column_nm, value)
print("After")
df.insert(0, "Future", [55,40,30])
print(df)