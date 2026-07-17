"""
==========================================================
Klarone AI Platform
Explanation Engine

Generates human-readable explanations for recommendations.

Author : Aanchal Anshika
==========================================================
"""


from utils import format_indian_currency


class ExplanationEngine:

    def __init__(self):
        pass
            # ======================================================
    # Generate Explanation
    # ======================================================

    def explain(self, laptop, intent):

        reasons = []

        # ----------------------------------------
        # Budget
        # ----------------------------------------

        if intent["budget"] is not None:

            if laptop["price"] <= intent["budget"]:

                reasons.append(
                    f"Fits within your budget of ₹{format_indian_currency(intent['budget'])}."
                )

        # ----------------------------------------
        # RAM
        # ----------------------------------------

        if laptop["ram(GB)"] >= 16:

            reasons.append(
                "16GB RAM is excellent for multitasking and coding."
            )

        elif laptop["ram(GB)"] >= 8:

            reasons.append(
                "8GB RAM is sufficient for daily tasks."
            )

        # ----------------------------------------
        # SSD
        # ----------------------------------------

        if laptop["ssd(GB)"] >= 1024:

            reasons.append(
                "1TB SSD provides fast performance and plenty of storage."
            )

        elif laptop["ssd(GB)"] >= 512:

            reasons.append(
                "512GB SSD offers fast boot times and adequate storage."
            )

        # ----------------------------------------
        # CPU
        # ----------------------------------------

        cpu = str(laptop["processor_name"])

        reasons.append(
            f"Powered by {cpu} processor."
        )
            # ----------------------------------------
        # GPU
        # ----------------------------------------

        graphics = str(laptop["graphics"]).upper()

        if "RTX" in graphics:

            reasons.append(
                "Dedicated RTX graphics support gaming and creative workloads."
            )

        elif "GTX" in graphics:

            reasons.append(
                "Dedicated GTX graphics are suitable for casual gaming."
            )

        elif "IRIS" in graphics:

            reasons.append(
                "Intel Iris Xe graphics are ideal for office work and programming."
            )

        elif "RADEON" in graphics:

            reasons.append(
                "AMD Radeon graphics provide balanced everyday performance."
            )

        elif "UHD" in graphics:

            reasons.append(
                "Integrated Intel UHD graphics are suitable for daily use."
            )
            # ----------------------------------------
        # Brand
        # ----------------------------------------

        if intent["preferred_brand"] is not None:

            if laptop["brand"].upper() == intent["preferred_brand"].upper():

                reasons.append(
                    "Matches your preferred brand."
                )

        # ----------------------------------------
        # Gaming
        # ----------------------------------------

        if intent["gaming"] != "none":

            if laptop["gaming_score"] >= 80:

                reasons.append(
                    "Excellent choice for gaming."
                )

            elif laptop["gaming_score"] >= 65:

                reasons.append(
                    "Suitable for casual gaming."
                )

        # ----------------------------------------
        # Coding
        # ----------------------------------------

        if intent["coding"]:

            if laptop["student_score"] >= 70:

                reasons.append(
                    "Well suited for software development."
                )

        return reasons
if __name__ == "__main__":

    import pandas as pd

    df = pd.read_csv("data/labeled_laptops.csv")

    laptop = df.iloc[0]

    intent = {

        "budget": 80000,

        "preferred_brand": "Lenovo",

        "gaming": "casual",

        "coding": True

    }

    engine = ExplanationEngine()

    explanation = engine.explain(

        laptop,

        intent

    )

    print()

    print("=" * 80)

    print("WHY THIS LAPTOP?")

    print("=" * 80)

    for reason in explanation:

        print("✔", reason)