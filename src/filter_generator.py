"""
==========================================================
Klarone AI Platform
Filter Generator

Filters laptops based on user requirements.

Author : Aanchal Anshika
==========================================================
"""

import pandas as pd


class FilterGenerator:

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
    # Main Filter
    # ======================================================

    def filter(self, requirements, intent):

        df = self.df.copy()

        minimum = requirements["minimum"]

        print("Initial Laptops :", len(df))

        # -----------------------------
        # Budget
        # -----------------------------

        if intent["budget"] is not None:

            df = df[
                df["price"] <= intent["budget"]
            ]

            print("After Budget :", len(df))

        # -----------------------------
        # RAM
        # -----------------------------

        df = df[
            df["ram(GB)"] >= minimum["ram"]
        ]

        print("After RAM :", len(df))

        # -----------------------------
        # SSD
        # -----------------------------

        df = df[
            df["ssd(GB)"] >= minimum["ssd"]
        ]

        print("After SSD :", len(df))

        # -----------------------------
        # CPU
        # -----------------------------

        df = df[
            df["processor_name"].apply(
                lambda x:
                self.cpu_matches(
                    x,
                    minimum["cpu"]
                )
            )
        ]

        print("After CPU :", len(df))

        # -----------------------------
        # Brand
        # -----------------------------

        if intent["preferred_brand"] is not None:

            df = df[
                df["brand"].str.upper()
                ==
                intent["preferred_brand"].upper()
            ]

            print("After Brand :", len(df))

        return df.reset_index(drop=True)
        # --------------------------------------------------
        # Brand Filter
        # --------------------------------------------------

        if intent["preferred_brand"] is not None:

            df = df[
                df["brand"].str.upper()
                ==
                intent["preferred_brand"].upper()
            ]

            print("After Brand :", len(df))

        return df.reset_index(drop=True)
# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    sample_intent = {

        "role": "student",

        "budget": 80000,

        "gaming": "casual",

        "preferred_brand": "Lenovo",

        "coding": True,

        "editing": False,

        "design": False,

        "office_work": False,

        "battery": False,

        "lightweight": False,

        "ai_ml": False

    }

    sample_requirements = {

        "minimum": {

            "cpu": "Core i3",

            "ram": 8,

            "ssd": 256,

            "gpu": "Integrated"

        }

    }

    engine = FilterGenerator()

    laptops = engine.filter(

        sample_requirements,

        sample_intent

    )

    print()

    print("=" * 100)

    print("FILTERED LAPTOPS")

    print("=" * 100)

    print(

        laptops[

            [

                "model_name",

                "price",

                "processor_name",

                "ram(GB)",

                "ssd(GB)",

                "graphics"

            ]

        ].head(20)

    )

    print()

    print("Total Matching Laptops :", len(laptops))