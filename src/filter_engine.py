"""
==========================================================
Klarone AI Platform
Filter Engine

Filters laptops based on user specifications and budget.

Author : Antigravity
==========================================================
"""

import pandas as pd


class FilterEngine:

    def __init__(self, dataset_path="data/labeled_laptops.csv"):
        self.df = pd.read_csv(dataset_path)

    # ======================================================
    # CPU Matching
    # ======================================================
    def cpu_matches(self, laptop_cpu, required_cpu):
        laptop_cpu = str(laptop_cpu).upper()
        required_cpu = required_cpu.upper()

        cpu_levels = {
            "CORE I3": 1,
            "RYZEN 3": 1,
            "CORE I5": 2,
            "RYZEN 5": 2,
            "CORE I7": 3,
            "RYZEN 7": 3,
            "CORE I9": 4,
            "RYZEN 9": 4
        }

        laptop_level = 0
        required_level = 0

        for cpu, level in cpu_levels.items():
            if cpu in laptop_cpu:
                laptop_level = level
                break

        for cpu, level in cpu_levels.items():
            if cpu in required_cpu:
                required_level = level
                break

        return laptop_level >= required_level

    # ======================================================
    # GPU Matching
    # ======================================================
    def gpu_matches(self, laptop_graphics, required_gpu):
        laptop_graphics = str(laptop_graphics).upper()
        required_gpu = required_gpu.upper()

        if "INTEGRATED" in required_gpu or required_gpu == "NONE":
            return True

        # Determine laptop's GPU level
        laptop_level = 1
        if "RTX 4090" in laptop_graphics or "RTX 4080" in laptop_graphics or "RTX 4070" in laptop_graphics:
            laptop_level = 5
        elif "RTX 4060" in laptop_graphics or "RTX 4050" in laptop_graphics or "RTX 3060" in laptop_graphics:
            laptop_level = 4
        elif "RTX 3050" in laptop_graphics or "RTX 2050" in laptop_graphics:
            laptop_level = 3
        elif any(kw in laptop_graphics for kw in ["RTX", "GTX", "RX", "ARC", "MX"]):
            laptop_level = 2
            
        # Determine required level
        required_level = 1
        if "RTX4070" in required_gpu or "RTX 4070" in required_gpu:
            required_level = 5
        elif "RTX4060" in required_gpu or "RTX 4060" in required_gpu:
            required_level = 4
        elif "RTX3050" in required_gpu or "RTX 3050" in required_gpu:
            required_level = 3
        elif any(kw in required_gpu for kw in ["RTX", "GTX", "RX", "ARC", "MX"]):
            required_level = 2

        return laptop_level >= required_level

    # ======================================================
    # Main Filter
    # ======================================================
    def filter(self, requirements, intent):
        df = self.df.copy()
        minimum = requirements.get("minimum", {})

        # -----------------------------
        # Budget
        # -----------------------------
        if intent.get("budget") is not None:
            df = df[df["price"] <= intent["budget"]]

        # -----------------------------
        # RAM
        # -----------------------------
        if "ram" in minimum:
            df = df[df["ram(GB)"] >= minimum["ram"]]

        # -----------------------------
        # SSD
        # -----------------------------
        if "ssd" in minimum:
            df = df[df["ssd(GB)"] >= minimum["ssd"]]

        # -----------------------------
        # CPU
        # -----------------------------
        if "cpu" in minimum:
            df = df[df["processor_name"].apply(lambda x: self.cpu_matches(x, minimum["cpu"]))]

        # -----------------------------
        # GPU
        # -----------------------------
        if "gpu" in minimum:
            df = df[df["graphics"].apply(lambda x: self.gpu_matches(x, minimum["gpu"]))]

        # -----------------------------
        # Brand
        # -----------------------------
        if intent.get("preferred_brand") is not None:
            df = df[df["brand"].str.upper() == intent["preferred_brand"].upper()]

        return df.reset_index(drop=True)
