import pandas as pd

customer1 = pd.DataFrame({
    "Name":["John","BOB"],
    "Age": [20, 30]
})

customer2 = pd.DataFrame({
    "Name":["Joy","Peter"],
    "Age": [25, 35]
})

df1 = pd.concat([customer1,customer2], axis=0)
print(df1)