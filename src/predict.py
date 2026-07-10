import joblib
import pandas as pd

# ==========================================================
# Load Trained Model and Encoder
# ==========================================================

model = joblib.load("models/laptop_price_model.pkl")
encoder = joblib.load("models/encoder.pkl")

# ==========================================================
# Format Indian Currency
# ==========================================================

def format_indian_currency(amount):

    amount = round(amount)

    s = str(amount)

    if len(s) <= 3:
        return f"₹{s}"

    last_three = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return "₹" + ",".join(parts) + "," + last_three


# ==========================================================
# New Laptop Details
# ==========================================================

new_laptop = {
    
    "brand": "Lenovo",
    "ram(GB)": 8,
    "ssd(GB)": 256,
    "Hard Disk(GB)": 0,
    "Operating System": "Windows",
    "screen_size(inches)": 15.6,
    "no_of_cores": 4,
    "no_of_threads": 8,
    "spec_score": 55,
    "gpu_brand": "INTEL",
    "gpu_type": "Integrated",
    "gpu_vram": 0,
    "gpu_series": "UHD",
    "cpu_brand": "INTEL",
    "cpu_family": "CORE I3",
    "cpu_generation": 11,
    "cpu_series": "OTHER",
    "screen_width": 1920,
    "screen_height": 1080
    }


# ==========================================================
# Convert to DataFrame
# ==========================================================

new_df = pd.DataFrame([new_laptop])

# ==========================================================
# Categorical Columns
# ==========================================================

categorical_columns = [
    "brand",
    "Operating System",
    "gpu_brand",
    "gpu_type",
    "gpu_series",
    "cpu_brand",
    "cpu_family",
    "cpu_series"
]

# ==========================================================
# Encode Categorical Features
# ==========================================================

encoded_features = encoder.transform(new_df[categorical_columns])

encoded_df = pd.DataFrame(
    encoded_features,
    columns=encoder.get_feature_names_out(categorical_columns),
    index=new_df.index
)

# ==========================================================
# Remove Original Categorical Columns
# ==========================================================

new_df.drop(columns=categorical_columns, inplace=True)

# ==========================================================
# Merge Encoded Features
# ==========================================================

new_df = pd.concat(
    [new_df, encoded_df],
    axis=1
)

# ==========================================================
# Match Training Columns
# ==========================================================

new_df = new_df.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)

# ==========================================================
# Predict Price
# ==========================================================

predicted_price = float(model.predict(new_df)[0])

# ==========================================================
# Display Result
# ==========================================================

print("=" * 60)
print("PREDICTED LAPTOP PRICE")
print("=" * 60)

print("Predicted Price :", format_indian_currency(predicted_price))