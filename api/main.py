import os
import sys
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add src folder to python path so we can import utils
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "src"))

from src.utils import (
    extract_gpu_brand,
    extract_gpu_type,
    extract_gpu_vram,
    extract_gpu_series,
    extract_cpu_brand,
    extract_cpu_family,
    extract_cpu_generation,
    extract_cpu_series,
    calculate_score
)

MODEL_PATH = BASE_DIR / "models" / "laptop_price_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "encoder.pkl"

if not MODEL_PATH.exists() or not ENCODER_PATH.exists():
    raise FileNotFoundError("Model or Encoder file not found. Ensure training has run successfully.")

# Load models
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

app = FastAPI(
    title="Klarone Laptop Price Prediction & Recommendation API",
    version="2.0.0",
    description="Upgraded API with auto-feature extraction from raw specifications."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LaptopRawSpecs(BaseModel):
    brand: str
    processor_name: str
    graphics: str
    ram_gb: int = Field(alias="ram(GB)")
    ssd_gb: int = Field(alias="ssd(GB)")
    hard_disk_gb: int = Field(0, alias="Hard Disk(GB)")
    operating_system: str = Field(alias="Operating System")
    screen_size_inches: float = Field(alias="screen_size(inches)")
    no_of_cores: int
    no_of_threads: int
    spec_score: int
    resolution: str = Field(alias="resolution (pixels)")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


@app.get("/")
def read_root():
    return {"message": "Welcome to the Klarone Laptop Price Prediction & Recommendation API!"}


@app.post("/predict")
def predict_and_recommend(specs: LaptopRawSpecs):
    try:
        # Convert Pydantic model to dictionary representation using aliases
        specs_dict = specs.model_dump(by_alias=True)

        # --------------------------------------------------
        # 1. Dynamic Feature Extraction (Feature Engineering)
        # --------------------------------------------------
        # Parse screen resolution (e.g. "1920x1080" -> 1920, 1080)
        try:
            res_split = specs_dict["resolution (pixels)"].lower().split("x")
            screen_width = int(res_split[0].strip())
            screen_height = int(res_split[1].strip())
        except Exception:
            raise ValueError("Invalid format for 'resolution (pixels)'. Expected format 'WidthxHeight' (e.g., '1920x1080').")

        # Extract GPU features
        gpu_brand = extract_gpu_brand(specs_dict["graphics"])
        gpu_type = extract_gpu_type(specs_dict["graphics"])
        gpu_vram = extract_gpu_vram(specs_dict["graphics"])
        gpu_series = extract_gpu_series(specs_dict["graphics"])

        # Extract CPU features
        cpu_brand = extract_cpu_brand(specs_dict["processor_name"])
        cpu_family = extract_cpu_family(specs_dict["processor_name"])
        cpu_generation = extract_cpu_generation(specs_dict["processor_name"])
        cpu_series = extract_cpu_series(specs_dict["processor_name"])

        # --------------------------------------------------
        # 2. Prepare Payload for Machine Learning Model
        # --------------------------------------------------
        ml_input = {
            "brand": specs_dict["brand"],
            "ram(GB)": specs_dict["ram(GB)"],
            "ssd(GB)": specs_dict["ssd(GB)"],
            "Hard Disk(GB)": specs_dict["Hard Disk(GB)"],
            "Operating System": specs_dict["Operating System"],
            "screen_size(inches)": specs_dict["screen_size(inches)"],
            "no_of_cores": specs_dict["no_of_cores"],
            "no_of_threads": specs_dict["no_of_threads"],
            "spec_score": specs_dict["spec_score"],
            "gpu_brand": gpu_brand,
            "gpu_type": gpu_type,
            "gpu_vram": gpu_vram,
            "gpu_series": gpu_series,
            "cpu_brand": cpu_brand,
            "cpu_family": cpu_family,
            "cpu_generation": cpu_generation,
            "cpu_series": cpu_series,
            "screen_width": screen_width,
            "screen_height": screen_height
        }

        # Create DataFrame matching preprocessing.py flow
        new_df = pd.DataFrame([ml_input])

        # Categorical columns to encode
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

        # One Hot Encode categorical features
        encoded_features = encoder.transform(new_df[categorical_columns])
        encoded_df = pd.DataFrame(
            encoded_features,
            columns=encoder.get_feature_names_out(categorical_columns),
            index=new_df.index
        )

        # Drop original and merge encoded features
        new_df.drop(columns=categorical_columns, inplace=True)
        new_df = pd.concat([new_df, encoded_df], axis=1)

        # Match columns with training feature columns
        new_df = new_df.reindex(
            columns=model.feature_names_in_,
            fill_value=0
        )

        # Run Prediction
        predicted_price = float(model.predict(new_df)[0])

        # --------------------------------------------------
        # 3. Calculate Suitability Scores
        # --------------------------------------------------
        scoring_input = {
            "graphics": specs_dict["graphics"],
            "processor_name": specs_dict["processor_name"],
            "cpu_generation": cpu_generation,
            "ram(GB)": specs_dict["ram(GB)"],
            "ssd(GB)": specs_dict["ssd(GB)"],
            "spec_score": specs_dict["spec_score"]
        }

        gaming_score = calculate_score(scoring_input, "gaming")
        student_score = calculate_score(scoring_input, "student")
        business_score = calculate_score(scoring_input, "business")

        return {
            "predicted_price": round(predicted_price),
            "gaming_score": gaming_score,
            "student_score": student_score,
            "business_score": business_score
        }

    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
