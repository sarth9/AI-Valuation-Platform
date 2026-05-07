import pandas as pd

df = pd.read_csv("data/processed_company_data.csv")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nPreview:")
print(df.head())

print("\nSummary stats:")
print(df.describe().T)