from data_loader import load_data
""" we have already loaded the data in the data loader file so instead of loading it again we are just importing the already loaded data
"""


import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()
""" this calls the function why we are doing this? because lets suppose we have changed the path so instead of oing to every file to change it 
we can just change it in one place and every other place it will be automatically loaded"""

# ==========================================================
# First Look at the Dataset
# ==========================================================

print("=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())


print("\n" + "=" * 60)
print("LAST 5 ROWS")
print("=" * 60)
print(df.tail())


# ==========================================================
# Dataset Shape
# ==========================================================

print("\n" + "=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ==========================================================
# Column Names
# ==========================================================

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())


# ==========================================================
# Dataset Information
# ==========================================================

print("\n" + "=" * 60)
print("DATASET INFO")
print("=" * 60)

df.info()


# ==========================================================
# Missing Values
# ==========================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = pd.DataFrame({
    "Missing Values": df.isnull().sum(),
    "Percentage": round((df.isnull().sum() / len(df)) * 100, 2)
})

print(missing)


# ==========================================================
# Duplicate Rows
# ==========================================================

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

print(df.duplicated().sum())


# ==========================================================
# Numerical Summary
# ==========================================================

print("\n" + "=" * 60)
print("NUMERICAL SUMMARY")
print("=" * 60)

print(df.describe())


# ==========================================================
# Categorical Summary
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORICAL SUMMARY")
print("=" * 60)

print(df.describe(include="object"))


# ==========================================================
# Unique Values
# ==========================================================

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

for column in df.columns:
    print(f"{column} : {df[column].nunique()}")


# ==========================================================
# Value Counts
# ==========================================================

print("\n" + "=" * 60)
print("BRAND DISTRIBUTION")
print("=" * 60)

print(df["brand"].value_counts())


print("\n" + "=" * 60)
print("PROCESSOR DISTRIBUTION")
print("=" * 60)

print(df["processor_name"].value_counts())


print("\n" + "=" * 60)
print("GRAPHICS DISTRIBUTION")
print("=" * 60)

print(df["graphics"].value_counts())


print("\n" + "=" * 60)
print("RAM DISTRIBUTION")
print("=" * 60)

print(df["ram(GB)"].value_counts())


print("\n" + "=" * 60)
print("SSD DISTRIBUTION")
print("=" * 60)

print(df["ssd(GB)"].value_counts())


# ==========================================================
# Price Distribution
# ==========================================================

plt.figure(figsize=(10,5))

plt.hist(df["price"], bins=30)

plt.title("Price Distribution")

plt.xlabel("Price")

plt.ylabel("Count")

plt.show()


# ==========================================================
# Specification Score Distribution
# ==========================================================

plt.figure(figsize=(10,5))

plt.hist(df["spec_score"], bins=20)

plt.title("Specification Score Distribution")

plt.xlabel("Specification Score")

plt.ylabel("Count")

plt.show()


# ==========================================================
# Correlation Heatmap
# ==========================================================

plt.figure(figsize=(10,8))

sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="Blues"
)

plt.title("Correlation Matrix")

plt.show()
# ==========================================================
#processor name 
# ========================================================
print(df["processor_name"].unique())
# ==========================================================
# graphics 
# ========================================================
print(df["graphics"].unique())
print("=" * 60)
print("LAPTOPS WITH SPEC SCORE = 0")
print("=" * 60)

print(df[df["spec_score"] == 0])