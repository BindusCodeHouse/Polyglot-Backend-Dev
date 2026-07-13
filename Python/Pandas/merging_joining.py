import pandas as pd

customer = pd.DataFrame({
    "cstId":[1,2,3],
    "Name":["Varun","Karan","Marun"]
})

order = pd.DataFrame({
    "cstId":[1,2,5],
    "Amount":[1000,500,200]
})

# Merging Data
df_merged = pd.merge(customer, order, on="cstId", how="right")
print(df_merged)

