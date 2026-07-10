import re
import pandas as pd
df = pd.read_csv("data/cleaned_laptops.csv")

def clean_gpu_name(gpu):
    """ standardizing the gpu names """
    if pd.isna(gpu):
        return gpu
    gpu = gpu.upper().strip()
    gpu = re.sub(r"\s+", " ", gpu)
    gpu = gpu.replace("GEFORCE", "")
    gpu = gpu.replace("GRAPHICS", "")
    gpu = gpu.replace("GRAPHIC", "")
    # ==========================================================
    # Normalize RTX naming
    # ==========================================================

    gpu = re.sub(r"RTX\s*RTX", "RTX", gpu)

    gpu = re.sub(r"RTX(\d{4})", r"RTX \1", gpu)
    gpu = re.sub(r"\s+", " ", gpu).strip()
        # ==========================================================
    # Normalize GTX naming
    # ==========================================================
    
    gpu = re.sub(r"GTX\s*GTX", "GTX", gpu)
    
    gpu = re.sub(r"GTX[- ]?(\d{4})", r"GTX \1", gpu)
    return gpu
df["graphics"] = df["graphics"].apply(clean_gpu_name)
# ==========================================================
# Preview Cleaned Graphics Column
# ==========================================================

print("=" * 60)
print("CLEANED GPU VALUES")
print("=" * 60)

print(df["graphics"].unique()[:30])
# ==========================================================
# Save Normalized Dataset
# ==========================================================

df.to_csv("data/normalized_laptops.csv", index=False)

print("\nNormalized dataset saved successfully.")
    

   
    