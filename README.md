# Klarone Laptop Price Prediction & Recommendation System

An end-to-end intelligent machine learning and rule-based recommendation backend. This system predicts the market price of a laptop based on its specifications and recommends how suitable it is for three distinct use cases: **Gaming**, **Student**, and **Business**.

The backend is built with **FastAPI** and is ready to be consumed by a React frontend.

---

## 🚀 Project Architecture & Pipeline

The project follows a modular machine learning pipeline from raw data to real-time endpoint serving:

```
Raw Dataset ➔ Data Cleaning ➔ Hardware Normalization ➔ Feature Engineering ➔ Preprocessing ➔ Model Training ➔ Real-time FastAPI Endpoint
```

### Key Components

1. **`data_cleaning.py`**: Performs basic cleaning, removes duplicates, handles missing values, and drops redundant columns (saves to `cleaned_laptops.csv`).
2. **`hardware_normalization.py`**: Standardizes hardware descriptions for CPU and GPU models (saves to `normalized_laptops.csv`).
3. **`feature_engineering.py`**: Splits resolutions into dimensions (`screen_width`, `screen_height`) and extracts structural hardware properties (saves to `feature_engineered_laptops.csv`).
4. **`preprocessing.py`**: Prepares the engineered dataset for machine learning by splitting features/targets and fitting a `OneHotEncoder` (saves to `preprocessed_laptops.csv` and serialized `encoder.pkl`).
5. **`train_model.py`**: Splits data into training/testing sets, trains a `RandomForestRegressor`, and logs metrics. The current model achieves an **$R^2$ accuracy score of ~87%** (saves serialized model to `laptop_price_model.pkl`).
6. **`utils.py`**: Houses the centralized parsing functions and the suitability scoring equations to prevent code duplication between offline data preparation and online API serving.
7. **`main.py` (FastAPI)**: Serves prediction requests, automatically runs feature engineering on raw specs, generates price predictions, computes use-case suitability scores, and returns the response.

---

## 📊 Recommendation Formulas

Suitability scores are calculated using a weighted expert system based on hardware performance tiers:

* **Gaming Score**: Focused heavily on GPU.
  $$\text{Gaming Score} = (\text{GPU} \times 55\%) + (\text{CPU} \times 20\%) + (\text{RAM} \times 15\%) + (\text{SSD} \times 5\%) + (\text{Spec Score} \times 5\%)$$
* **Student Score**: Balanced for lightweight study tasks.
  $$\text{Student Score} = (\text{GPU} \times 10\%) + (\text{CPU} \times 30\%) + (\text{RAM} \times 25\%) + (\text{SSD} \times 20\%) + (\text{Spec Score} \times 15\%)$$
  *(Penalties are applied for high-power gaming components like RTX GPUs or HX processors to optimize battery life suitability).*
* **Business Score**: Focused on office productivity.
  $$\text{Business Score} = (\text{GPU} \times 5\%) + (\text{CPU} \times 35\%) + (\text{RAM} \times 25\%) + (\text{SSD} \times 20\%) + (\text{Spec Score} \times 15\%)$$
  *(Penalties are applied for discrete/gaming GPUs and high-power processors).*

---

## 💻 Local Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Install Dependencies
Activate your virtual environment and install the required libraries:
```bash
# Windows
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the API Server
Start the FastAPI server using Uvicorn:
```bash
python -m uvicorn api.main:app --reload --port 8080
```

### 4. Open Interactive Documentation
Go to your browser and access the interactive Swagger UI to test endpoints:
* **Swagger UI**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
* **ReDoc**: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

---

## 📡 API Endpoint Details

### **POST** `/predict`

Accepts raw specifications of a laptop and performs feature extraction on-the-fly to return predictions.

#### **Request Body** (`application/json`):
```json
{
    "brand": "Lenovo",
    "processor_name": "Intel Core i3 11th Gen",
    "graphics": "Intel UHD Graphics",
    "ram(GB)": 8,
    "ssd(GB)": 256,
    "Hard Disk(GB)": 0,
    "Operating System": "Windows",
    "screen_size(inches)": 15.6,
    "no_of_cores": 4,
    "no_of_threads": 8,
    "spec_score": 55,
    "resolution (pixels)": "1920x1080"
}
```

#### **Response Body** (`application/json`):
```json
{
    "predicted_price": 53770,
    "gaming_score": 36,
    "student_score": 57,
    "business_score": 59
}
```

---

## ☁️ Deployment

To deploy this backend API 24/7 on a cloud platform like **Render**:
1. Connect your GitHub repository to Render.
2. Select **Web Service**.
3. Set the build and start configurations:
   * **Language**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT`
