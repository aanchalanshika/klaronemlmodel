# Frontend Integration Guide (React / Full-stack Developer)

This document provides instructions on how to integrate the **Klarone AI Platform** backend into your React application.

---

## 📡 Base API URL

The backend runs locally at:
- **Base URL**: `http://127.0.0.1:8000`

---

## 🛠️ API Integration Details

The API exposes two primary endpoints to support the two main features of the platform:

---

### 1. AI Laptop Advisor (Main Feature)
Use this endpoint to submit a natural language query and get the top 5 recommended laptops.

- **Endpoint**: `POST /recommend`
- **Headers**: `Content-Type: application/json`

#### **Request Body (JSON)**
```json
{
  "query": "I am a business student who uses microsoft office services alot like powerpoint and zoom meetings. Budget 60000"
}
```

#### **Response Body (JSON)**
```json
{
  "recommendations": [
    {
      "model_name": "Asus VivoBook 15 X1500EA-EJ701W Laptop",
      "actual_price": 56799,
      "recommendation_score": 85,
      "gaming_score": 59,
      "student_score": 80,
      "business_score": 83,
      "reason": [
        "Fits within your budget of ₹60,000.",
        "16GB RAM is excellent for multitasking and coding.",
        "512GB SSD offers fast boot times and adequate storage.",
        "Powered by 11th Gen Core i7 processor.",
        "Intel Iris Xe graphics are ideal for office work and programming."
      ]
    }
  ]
}
```

---

### 2. AI Laptop Value Estimator
Use this endpoint to estimate the market value of custom laptop configurations.

- **Endpoint**: `POST /estimate-value`
- **Headers**: `Content-Type: application/json`

#### **Request Body (JSON)**
```json
{
  "brand": "Lenovo",
  "processor_name": "Ryzen 7 8845HS",
  "graphics": "RTX 4060",
  "ram(GB)": 32,
  "ssd(GB)": 1024,
  "Hard Disk(GB)": 0,
  "Operating System": "Windows",
  "screen_size(inches)": 15.6,
  "no_of_cores": 8,
  "no_of_threads": 16,
  "spec_score": 85,
  "resolution (pixels)": "1920x1080"
}
```

#### **Response Body (JSON)**
```json
{
  "predicted_price": 108000,
  "gaming_score": 88,
  "student_score": 82,
  "business_score": 61
}
```

---

## 💻 Integration Code Examples (Axios)

### 1. Get Recommendations (Advisor)
```javascript
import axios from "axios";

const getRecommendations = async (userQuery) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/recommend",
      { query: userQuery },
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data.recommendations; // Array of 5 laptop recommendation objects
  } catch (error) {
    console.error("Error fetching recommendations:", error);
  }
};
```

### 2. Get Custom Value Estimation (Estimator)
```javascript
import axios from "axios";

const estimateValue = async (customSpecs) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/estimate-value",
      customSpecs,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data; // { predicted_price, gaming_score, student_score, business_score }
  } catch (error) {
    console.error("Error estimating custom price value:", error);
  }
};
```
