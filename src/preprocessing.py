import pandas as pd
from sklearn.preprocessing import OneHotEncoder
# ==========================================================
# Load Feature Engineered Dataset
# ==========================================================

df = pd.read_csv("data/feature_engineered_laptops.csv")

# ==========================================================
# Dataset Information
# ==========================================================

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print(df.shape)

print()

print("=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())

# ==========================================================
# Store Model Names
# ==========================================================

model_names = df["model_name"]

# ==========================================================
# Separate Features and Target
# ==========================================================

X = df.drop(columns=["model_name", "price"])
# ==========================================================
# Split Screen Resolution
# ==========================================================

resolution = X["resolution (pixels)"].str.split("x", expand=True)

X["screen_width"] = resolution[0].astype(int)
X["screen_height"] = resolution[1].astype(int)

X.drop(columns=["resolution (pixels)"], inplace=True)
# ==========================================================
# Find Categorical Columns
# ==========================================================

categorical_columns = X.select_dtypes(include=["object"]).columns

print("\n")
print("=" * 60)
print("CATEGORICAL COLUMNS")
print("=" * 60)

print(categorical_columns.tolist())

y = df["price"]
# ==========================================================
# One Hot Encoding
# ==========================================================

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

encoded_features = encoder.fit_transform(
    X[categorical_columns]
)

encoded_df = pd.DataFrame(
    encoded_features,
    columns=encoder.get_feature_names_out(categorical_columns)
)

encoded_df.index = X.index
# ==========================================================
# Replace Categorical Columns
# ==========================================================

X = X.drop(columns=categorical_columns)

X = pd.concat(
    [X, encoded_df],
    axis=1
)
# ==========================================================
# Display Information
# ==========================================================

print()

print("=" * 60)
print("FEATURES (X)")
print("=" * 60)

print(X.head())

print()

print("=" * 60)
print("TARGET (y)")
print("=" * 60)

print(y.head())

print()

print("=" * 60)
print("MODEL NAMES")
print("=" * 60)

print(model_names.head())
print("\n")
print("=" * 60)
print("NUMERICAL COLUMNS")
print("=" * 60)

print(
    X.select_dtypes(exclude=["object"]).columns.tolist()
)
print("\n")
print("=" * 60)
print("ENCODED DATASET")
print("=" * 60)

print(X.head())

print()

print("Shape :", X.shape)
# ==========================================================
# Save Preprocessed Dataset
# ==========================================================

preprocessed_data = X.copy()

preprocessed_data["price"] = y

preprocessed_data.to_csv(
    "data/preprocessed_laptops.csv",
    index=False
)

print("\n")
print("Preprocessed dataset saved successfully!")
import joblib

# ==========================================================
# Save Encoder
# ==========================================================

joblib.dump(
    encoder,
    "models/encoder.pkl"
)

print("Encoder saved successfully!")