import pandas as pd

data = {
    "Name": ["Priya", "Kajal", "Kriti"],
    "Age": [45, 15, 20],
    "City": ["Ahmedabad", "Vadodara", "Surat"]
}

df = pd.DataFrame(data)
avg = df["Age"].mean()
print(avg)