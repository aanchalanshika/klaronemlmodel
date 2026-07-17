"""
==========================================================
Klarone AI Platform
Requirement Generator

Converts user intent into laptop requirements.

Author : Aanchal Anshika
==========================================================
"""


class RequirementGenerator:

    def __init__(self):

        self.role_profiles = {

            "student": {

                "minimum": {
                    "cpu": "Core i3",
                    "ram": 8,
                    "ssd": 256,
                    "gpu": "Integrated"
                },

                "recommended": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "ideal": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "RTX3050"
                }

            },

            "software_engineer": {

                "minimum": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "recommended": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "RTX3050"
                },

                "ideal": {
                    "cpu": "Core i7",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4060"
                }

            },

            "data_scientist": {

                "minimum": {
                    "cpu": "Ryzen 7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "RTX3050"
                },

                "recommended": {
                    "cpu": "Ryzen 7",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4060"
                },

                "ideal": {
                    "cpu": "Ryzen 9",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4070"
                }

            },

            "hr": {

                "minimum": {
                    "cpu": "Core i3",
                    "ram": 8,
                    "ssd": 256,
                    "gpu": "Integrated"
                },

                "recommended": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "ideal": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                }

            },

            "teacher": {

                "minimum": {
                    "cpu": "Core i3",
                    "ram": 8,
                    "ssd": 256,
                    "gpu": "Integrated"
                },

                "recommended": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "ideal": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                }

            },

            "business": {

                "minimum": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "recommended": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "Integrated"
                },

                "ideal": {
                    "cpu": "Core i7",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "Integrated"
                }

            },

            "video_editor": {

                "minimum": {
                    "cpu": "Core i7",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "RTX3050"
                },

                "recommended": {
                    "cpu": "Core i7",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4060"
                },

                "ideal": {
                    "cpu": "Core i9",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4070"
                }

            },

            "graphic_designer": {

                "minimum": {
                    "cpu": "Core i5",
                    "ram": 16,
                    "ssd": 512,
                    "gpu": "RTX3050"
                },

                "recommended": {
                    "cpu": "Core i7",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4060"
                },

                "ideal": {
                    "cpu": "Core i9",
                    "ram": 32,
                    "ssd": 1024,
                    "gpu": "RTX4070"
                }

            }

        }

    # =====================================================

    def generate(self, intent):

        role = intent["role"]

        if role not in self.role_profiles:

            role = "student"

        requirements = self.role_profiles[role].copy()

        # -----------------------------------------
        # Gaming Upgrade
        # -----------------------------------------

        if intent["gaming"] == "casual":

            requirements["recommended"]["gpu"] = "RTX3050"

        elif intent["gaming"] == "heavy":

            requirements["recommended"]["gpu"] = "RTX4060"

            requirements["recommended"]["ram"] = max(
                16,
                requirements["recommended"]["ram"]
            )

        # -----------------------------------------
        # Coding Upgrade
        # -----------------------------------------

        if intent["coding"]:

            requirements["recommended"]["ram"] = max(
                16,
                requirements["recommended"]["ram"]
            )

            requirements["recommended"]["ssd"] = max(
                512,
                requirements["recommended"]["ssd"]
            )

        # -----------------------------------------
        # Editing Upgrade
        # -----------------------------------------

        if intent["editing"]:

            requirements["recommended"]["gpu"] = "RTX4060"

            requirements["recommended"]["ram"] = 32

            requirements["recommended"]["ssd"] = 1024

        return requirements


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample = {

        "role": "student",

        "budget": 80000,

        "gaming": "casual",

        "coding": True,

        "editing": False

    }

    generator = RequirementGenerator()

    result = generator.generate(sample)

    from pprint import pprint

    pprint(result)