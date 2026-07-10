import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/preprocessed_laptops.csv")

# ==========================================================
# Separate Features and Target
# ==========================================================

X = df.drop(columns=["price"])
y = df["price"]

# ==========================================================
# Train-Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================================
# Train Random Forest Model
# ==========================================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# Make Predictions
# ==========================================================

y_pred = model.predict(X_test)

print("\n")
print("=" * 60)
print("PREDICTED PRICES")
print("=" * 60)

print(y_pred[:10])

# ==========================================================
# Model Evaluation
# ==========================================================

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5

r2 = r2_score(y_test, y_pred)

print("\n")
print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")
accuracy = r2 * 100

print(f"Accuracy : {accuracy:.2f}%")
# ==========================================================
# Save Model
# ==========================================================

joblib.dump(
    model,
    "models/laptop_price_model.pkl"
)

print("\n")
print("=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)