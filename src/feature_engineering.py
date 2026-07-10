import re
import sys
from pathlib import Path
import pandas as pd

# Add src folder to path if running directly
sys.path.append(str(Path(__file__).resolve().parent))
from utils import (
    extract_gpu_brand,
    extract_gpu_type,
    extract_gpu_vram,
    extract_gpu_series,
    extract_cpu_brand,
    extract_cpu_family,
    extract_cpu_generation,
    extract_cpu_series
)

df = pd.read_csv("data/normalized_laptops.csv")


df["gpu_brand"] = df["graphics"].apply(extract_gpu_brand)

df["gpu_type"] = df["graphics"].apply(extract_gpu_type)

df["gpu_vram"] = df["graphics"].apply(extract_gpu_vram)

df["gpu_series"] = df["graphics"].apply(extract_gpu_series)


df["cpu_brand"] = df["processor_name"].apply(extract_cpu_brand)

df["cpu_family"] = df["processor_name"].apply(extract_cpu_family)

df["cpu_generation"] = df["processor_name"].apply(extract_cpu_generation)

df["cpu_series"] = df["processor_name"].apply(extract_cpu_series)

# ==========================================================
# Remove Original Columns
# ==========================================================

# df.drop(
    # columns=[
        # "graphics",
        # "processor_name"
    # ],
    # inplace=True
# )

# ==========================================================
# Save Feature Engineered Dataset
# ==========================================================

df.to_csv(
    "data/feature_engineered_laptops.csv",
    index=False
)

print("\nFeature engineered dataset saved successfully!")