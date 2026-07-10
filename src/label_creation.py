

import pandas as pd

df = pd.read_csv("data/feature_engineered_laptops.csv")

print(df.columns.tolist())
print(df["graphics"].drop_duplicates().head(10).tolist())

print()

print(df["processor_name"].drop_duplicates().head(10).tolist())

import sys
from pathlib import Path

# Add src folder to path if running directly
sys.path.append(str(Path(__file__).resolve().parent))
from utils import calculate_score

# Create Recommendation Scores
# ==========================================================

df["gaming_score"] = df.apply(
    lambda row: calculate_score(row, "gaming"),
    axis=1
)

df["student_score"] = df.apply(
    lambda row: calculate_score(row, "student"),
    axis=1
)

df["business_score"] = df.apply(
    lambda row: calculate_score(row, "business"),
    axis=1
)
print("\n")
print("=" * 100)
print("LAPTOP SUITABILITY SCORES")
print("=" * 100)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(
    df[
        [
            "model_name",
            "gaming_score",
            "student_score",
            "business_score"
        ]
    ].head(20)
)

# ==========================================================
# Save Dataset
# ==========================================================

df.to_csv(
    "data/labeled_laptops.csv",
    index=False
)

print("\nLabeled dataset saved successfully!")
print(df["cpu_generation"].drop_duplicates().tolist())