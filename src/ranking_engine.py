"""
==========================================================
Klarone AI Platform
Ranking Engine

Ranks laptops according to the user's needs.

Author : Aanchal Anshika
==========================================================
"""

import pandas as pd


class RankingEngine:

    def __init__(self):
        pass
            # ======================================================
    # Overall Match Calculator
    # ======================================================

    def calculate_overall_match(self, row, intent):

        role = intent["role"]

        gaming = row["gaming_score"]
        student = row["student_score"]
        business = row["business_score"]

        # Check for dedicated graphics or gaming branding
        is_gaming_laptop = False
        gpu_type = str(row.get("gpu_type", "")).upper()
        if "DEDICATED" in gpu_type:
            is_gaming_laptop = True
        
        graphics = str(row.get("graphics", "")).upper()
        if any(kw in graphics for kw in ["RTX", "GTX", "RX"]):
            is_gaming_laptop = True
            
        model_name = str(row.get("model_name", "")).upper()
        gaming_brands = ["GAMING", "VICTUS", "OMEN", "TUF", "ROG", "LEGION", "NITRO", "PREDATOR", "ALIENWARE"]
        if any(brand in model_name for brand in gaming_brands):
            is_gaming_laptop = True

        # -----------------------------------------
        # Student
        # -----------------------------------------

        if role == "student":

            if intent.get("gaming") == "none":
                overall = (
                    student * 0.85 +
                    business * 0.15
                )
                if is_gaming_laptop:
                    overall -= 20
            else:
                overall = (
                    student * 0.60 +
                    gaming * 0.30 +
                    business * 0.10
                )

        # -----------------------------------------
        # HR / Business / Teacher
        # -----------------------------------------

        elif role in ["business", "hr", "teacher"]:

            if intent.get("gaming") == "none":
                overall = (
                    business * 0.80 +
                    student * 0.20
                )
                if is_gaming_laptop:
                    overall -= 30
            else:
                overall = (
                    business * 0.70 +
                    student * 0.20 +
                    gaming * 0.10
                )

        # -----------------------------------------
        # Software Engineer / Developer
        # -----------------------------------------

        elif role == "software_engineer":

            if intent.get("gaming") == "none":
                overall = (
                    student * 0.60 +
                    business * 0.40
                )
                if is_gaming_laptop:
                    overall -= 20
            else:
                overall = (
                    student * 0.40 +
                    business * 0.30 +
                    gaming * 0.30
                )

        # -----------------------------------------
        # Data Scientist
        # -----------------------------------------

        elif role == "data_scientist":

            if intent.get("gaming") == "none":
                overall = (
                    student * 0.60 +
                    business * 0.40
                )
                if is_gaming_laptop:
                    overall -= 20
            else:
                overall = (
                    student * 0.40 +
                    business * 0.30 +
                    gaming * 0.30
                )

        # -----------------------------------------
        # Video Editor
        # -----------------------------------------

        elif role == "video_editor":

            overall = (

                gaming * 0.65 +

                student * 0.20 +

                business * 0.05

            )

        # -----------------------------------------
        # Graphic Designer
        # -----------------------------------------

        elif role == "graphic_designer":

            overall = (

                gaming * 0.50 +

                student * 0.30 +

                business * 0.10

            )

        else:

            overall = (

                student * 0.50 +

                gaming * 0.30 +

                business * 0.10

            )
            # =====================================================
        # =====================================================
        # Price Bonus / Penalty
        # =====================================================

        if intent["budget"] is not None:

            ratio = row["price"] / intent["budget"]

            if ratio <= 0.60:

                overall += 10

            elif ratio <= 0.80:

                overall += 7

            elif ratio <= 1.00:

                overall += 5
        else:
            # Default pricing heuristics when budget is not specified
            price = row["price"]
            if price > 100000:
                overall -= 30
            elif price > 75000:
                overall -= 15
            elif price < 55000:
                overall += 10

        # =====================================================
        # Preferred Brand Bonus
        # =====================================================

        if intent["preferred_brand"] is not None:

            if str(row["brand"]).upper() == intent["preferred_brand"].upper():

                overall += 5

        # =====================================================
        # Coding Bonus
        # =====================================================

        if intent["coding"]:

            if row["ram(GB)"] >= 16:

                overall += 3

            if row["ssd(GB)"] >= 512:

                overall += 2

        # =====================================================
        # Editing Bonus
        # =====================================================

        if intent["editing"]:

            graphics = str(row["graphics"]).upper()

            if "RTX" in graphics:

                overall += 5

        # =====================================================
        # AI / ML Bonus
        # =====================================================

        if intent["ai_ml"]:

            if row["ram(GB)"] >= 16:

                overall += 2

            graphics = str(row["graphics"]).upper()

            if "RTX" in graphics:

                overall += 3

        # =====================================================
        # Keep Overall Match Between 0 and 100
        # =====================================================

        overall = max(0, min(100, overall))

        return round(overall, 2)
        # ======================================================
    # Rank Laptops
    # ======================================================

    def rank(self, laptops, intent):

        laptops = laptops.copy()

        laptops["overall_match"] = laptops.apply(

            lambda row:

            self.calculate_overall_match(

                row,

                intent

            ),

            axis=1

        )

        laptops["recommendation_score"] = laptops["overall_match"]

        laptops = laptops.sort_values(

            by="recommendation_score",

            ascending=False

        )

        return laptops.reset_index(drop=True)
# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    from filter_generator import FilterGenerator
    from requirement_generator import RequirementGenerator

    intent = {

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

    generator = RequirementGenerator()

    requirements = generator.generate(intent)

    filter_engine = FilterGenerator()

    filtered = filter_engine.filter(

        requirements,

        intent

    )

    ranking = RankingEngine()

    ranked = ranking.rank(

        filtered,

        intent

    )

    print()

    print("=" * 120)

    print("TOP RECOMMENDATIONS")

    print("=" * 120)

    print(

        ranked[

            [

                "model_name",

                "overall_match",

                "gaming_score",

                "student_score",

                "business_score",

                "price"

            ]

        ].head(10)

    )