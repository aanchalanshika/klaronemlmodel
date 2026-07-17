"""
==========================================================
Klarone AI Platform
Recommendation Engine

Complete recommendation pipeline.

Author : Aanchal Anshika
==========================================================
"""

from intent_parser import IntentParser
from requirement_generator import RequirementGenerator
from filter_engine import FilterEngine
from ranking_engine import RankingEngine
from explanation_engine import ExplanationEngine


from utils import format_indian_currency


class RecommendationEngine:

    def __init__(self):

        self.intent_parser = IntentParser()

        self.requirement_generator = RequirementGenerator()

        self.filter_engine = FilterEngine()

        self.ranking_engine = RankingEngine()

        self.explanation_engine = ExplanationEngine()
        # ======================================================
    # Complete Recommendation Pipeline
    # ======================================================

    def recommend(self, query, top_k=5):

        # ---------------------------------------
        # Parse User Intent
        # ---------------------------------------

        intent = self.intent_parser.parse(query)

        # ---------------------------------------
        # Generate Laptop Requirements
        # ---------------------------------------

        requirements = self.requirement_generator.generate(
            intent
        )

        # ---------------------------------------
        # Filter Candidate Laptops
        # ---------------------------------------

        filtered = self.filter_engine.filter(
            requirements,
            intent
        )

        if len(filtered) == 0:

            return {

                "intent": intent,

                "requirements": requirements,

                "recommendations": []

            }

        # ---------------------------------------
        # Rank Laptops
        # ---------------------------------------

        ranked = self.ranking_engine.rank(
            filtered,
            intent
        )

        # ---------------------------------------
        # Remove Duplicate Laptop Models
        # ---------------------------------------

        ranked = ranked.drop_duplicates(
            subset=["model_name"]
        )

        recommendations = []
        
                # ---------------------------------------
        # Create Top Recommendations
        # ---------------------------------------

        for _, laptop in ranked.head(top_k).iterrows():

            explanation = self.explanation_engine.explain(
                laptop,
                intent
            )

            recommendation = {

                "model_name": laptop["model_name"],

                "brand": laptop["brand"],

                "price": int(laptop["price"]),

                "overall_match": float(
                    laptop["overall_match"]
                ),

                "gaming_score": int(
                    laptop["gaming_score"]
                ),

                "student_score": int(
                    laptop["student_score"]
                ),

                "business_score": int(
                    laptop["business_score"]
                ),

                "processor": laptop["processor_name"],

                "ram": int(
                    laptop["ram(GB)"]
                ),

                "ssd": int(
                    laptop["ssd(GB)"]
                ),

                "graphics": laptop["graphics"],

                "explanation": explanation

            }

            recommendations.append(
                recommendation
            )
                # ---------------------------------------
        # Return Final Result
        # ---------------------------------------

        return {

            "intent": intent,

            "requirements": requirements,

            "recommendations": recommendations

        }
# ======================================================
# Testing
# ======================================================

if __name__ == "__main__":

    engine = RecommendationEngine()

    while True:

        query = input("\nEnter Query (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        result = engine.recommend(query)

        print("\n")
        print("=" * 100)
        print("USER INTENT")
        print("=" * 100)
        print(result["intent"])

        print("\n")
        print("=" * 100)
        print("TOP RECOMMENDATIONS")
        print("=" * 100)

        if len(result["recommendations"]) == 0:

            print("No laptops matched the given requirements.")
            continue

        for i, laptop in enumerate(result["recommendations"], start=1):

            print(f"\n{i}. {laptop['model_name']}")

            print(f"Brand          : {laptop['brand']}")
            print(f"Price          : ₹{format_indian_currency(laptop['price'])}")

            print(f"Overall Match  : {laptop['overall_match']}%")

            print(f"🎮 Gaming      : {laptop['gaming_score']}/100")
            print(f"🎓 Student     : {laptop['student_score']}/100")
            print(f"💼 Business    : {laptop['business_score']}/100")

            print("\nWhy this laptop?")

            for reason in laptop["explanation"]:
                print(f"  ✔ {reason}")

            print("-" * 80)