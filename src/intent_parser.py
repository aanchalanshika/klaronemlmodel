"""
==========================================================
Klarone AI Platform
Intent Parser (V2)

Converts natural language into structured user intent.

Author: Antigravity
==========================================================
"""

import re


class IntentParser:

    def __init__(self):

        self.roles = {
            "student": [
                "student",
                "college",
                "university",
                "school",
                "btech",
                "engineering",
                "mba",
                "mca"
            ],
            "software_engineer": [
                "software engineer",
                "developer",
                "programmer",
                "backend",
                "frontend",
                "full stack",
                "fullstack",
                "web developer",
                "software development"
            ],
            "data_scientist": [
                "data scientist",
                "machine learning",
                "ml engineer",
                "ai engineer",
                "artificial intelligence",
                "deep learning",
                "data analyst"
            ],
            "hr": [
                "hr",
                "human resource",
                "recruiter"
            ],
            "teacher": [
                "teacher",
                "professor",
                "faculty",
                "lecturer"
            ],
            "business": [
                "business",
                "entrepreneur",
                "startup",
                "business owner",
                "office"
            ],
            "video_editor": [
                "video editor",
                "premiere",
                "davinci",
                "after effects",
                "video editing"
            ],
            "graphic_designer": [
                "graphic designer",
                "photoshop",
                "illustrator",
                "figma",
                "ui ux",
                "ui/ux"
            ]
        }

    # --------------------------------------------------
    # Detect User Roles (Multiple Support)
    # --------------------------------------------------
    def detect_roles(self, text):
        text = text.lower()
        matched_roles = []
        for role, keywords in self.roles.items():
            for keyword in keywords:
                if keyword in text:
                    matched_roles.append(role)
                    break
        return matched_roles

    def detect_role(self, text):
        roles = self.detect_roles(text)
        return roles[0] if roles else "general"

    # --------------------------------------------------
    # Detect Budget
    # --------------------------------------------------
    def detect_budget(self, text):
        text = text.lower().replace(",", "")

        # Try to find numeric budget values first
        patterns = [
            r'under\s*₹?\s*(\d+)',
            r'below\s*₹?\s*(\d+)',
            r'less than\s*₹?\s*(\d+)',
            r'budget\s*(?:is\s*)?₹?\s*(\d+)',
            r'budget\s*(?:of\s*)?₹?\s*(\d+)',
            r'₹\s*(\d+)',
            r'(\d+)\s*k',
            r'(\d{5,6})'
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = int(match.group(1))
                if value < 1000:
                    value *= 1000
                return value

        # Try to find vague budget descriptions if no numeric value is found
        if any(w in text for w in ["budget laptop", "cheap", "affordable"]):
            return 60000
        elif any(w in text for w in ["mid range", "midrange", "mid-range"]):
            return 80000
        elif any(w in text for w in ["premium", "flagship"]):
            return 150000

        return None

    # --------------------------------------------------
    # Detect Gaming Requirement
    # --------------------------------------------------
    def detect_gaming(self, text):
        text = text.lower()
        heavy_games = [
            "cyberpunk",
            "elden ring",
            "warzone",
            "red dead redemption",
            "rdr2",
            "hogwarts legacy",
            "black myth wukong",
            "aaa",
            "high end gaming",
            "heavy gaming"
        ]

        casual_games = [
            "valorant",
            "csgo",
            "counter strike",
            "pubg",
            "bgmi",
            "gta",
            "gta v",
            "minecraft",
            "fifa",
            "ea fc",
            "fortnite",
            "apex",
            "rocket league",
            "league of legends",
            "dota",
            "gaming",
            "play games",
            "games"
        ]

        for game in heavy_games:
            if game in text:
                return "heavy"

        for game in casual_games:
            if game in text:
                return "casual"

        return "none"

    # --------------------------------------------------
    # Detect Gaming Intensity Level
    # --------------------------------------------------
    def detect_gaming_level(self, text, detected_gaming):
        text = text.lower()
        
        heavy_kw = ["every day", "daily", "professionally", "hardcore gamer", "hardcore"]
        casual_kw = ["sometimes", "occasionally", "weekends", "casually"]
        light_kw = ["rarely", "once in a while"]

        if any(kw in text for kw in heavy_kw):
            return "heavy"
        if any(kw in text for kw in casual_kw):
            return "casual"
        if any(kw in text for kw in light_kw):
            return "light"

        # Fallback to the game titles level if gaming keyword is matched but no frequency keyword
        if detected_gaming != "none":
            return detected_gaming

        return "none"

    # --------------------------------------------------
    # Detect User Preferences
    # --------------------------------------------------
    def detect_preferences(self, text):
        text = text.lower()

        preferences = {
            # Coding / Programming
            "coding": any(
                word in text
                for word in [
                    "code",
                    "coding",
                    "programming",
                    "developer",
                    "software",
                    "python",
                    "java",
                    "c++",
                    "javascript",
                    "react",
                    "machine learning",
                    "data science",
                    "software development",
                    "programmer",
                    "backend",
                    "frontend",
                    "full stack",
                    "web developer"
                ]
            ),

            # Video Editing / Designing
            "editing": any(
                word in text
                for word in [
                    "editing",
                    "video",
                    "premiere",
                    "after effects",
                    "davinci",
                    "resolve",
                    "capcut",
                    "photoshop",
                    "video editor",
                    "video editing"
                ]
            ),

            # Graphic Design
            "design": any(
                word in text
                for word in [
                    "photoshop",
                    "illustrator",
                    "figma",
                    "graphic design",
                    "ui",
                    "ux",
                    "ui ux"
                ]
            ),

            # Office Work
            "office_work": any(
                word in text
                for word in [
                    "office",
                    "excel",
                    "word",
                    "powerpoint",
                    "outlook",
                    "hr",
                    "recruitment",
                    "office work"
                ]
            ),

            # Battery Preference
            "battery": any(
                word in text
                for word in [
                    "battery",
                    "battery life",
                    "long battery",
                    "all day battery"
                ]
            ),

            # Lightweight Laptop
            "lightweight": any(
                word in text
                for word in [
                    "lightweight",
                    "portable",
                    "travel",
                    "thin",
                    "light"
                ]
            ),

            # AI / Machine Learning
            "ai_ml": any(
                word in text
                for word in [
                    "ai",
                    "machine learning",
                    "deep learning",
                    "tensorflow",
                    "pytorch",
                    "llm",
                    "ml engineer",
                    "ai engineer",
                    "artificial intelligence"
                ]
            )
        }

        return preferences

    # --------------------------------------------------
    # Detect Preferred Brand
    # --------------------------------------------------
    def detect_brand(self, text):
        text = text.lower()

        brand_alias = {
            "Lenovo": [
                "lenovo",
                "lenevo",
                "lenova",
                "lenvo"
            ],
            "HP": [
                "hp",
                "hewlett packard"
            ],
            "Dell": [
                "dell",
                "delll",
                "del"
            ],
            "Asus": [
                "asus",
                "asuz"
            ],
            "Acer": [
                "acer"
            ],
            "MSI": [
                "msi"
            ],
            "Apple": [
                "apple",
                "macbook",
                "mac"
            ],
            "Samsung": [
                "samsung"
            ],
            "LG": [
                "lg"
            ],
            "Infinix": [
                "infinix"
            ],
            "Realme": [
                "realme"
            ]
        }

        for brand, aliases in brand_alias.items():
            for alias in aliases:
                if alias in text:
                    return brand

        return None

    # --------------------------------------------------
    # Parse Complete User Query
    # --------------------------------------------------
    def parse(self, query):
        query = query.lower()

        roles = self.detect_roles(query)
        role = self.detect_role(query)
        budget = self.detect_budget(query)
        gaming = self.detect_gaming(query)
        gaming_level = self.detect_gaming_level(query, gaming)
        preferences = self.detect_preferences(query)
        brand = self.detect_brand(query)

        result = {
            "role": role,
            "roles": roles,
            "budget": budget,
            "preferred_brand": brand,
            "gaming": gaming,
            "gaming_level": gaming_level,
            "coding": preferences["coding"],
            "editing": preferences["editing"],
            "design": preferences["design"],
            "office_work": preferences["office_work"],
            "battery": preferences["battery"],
            "lightweight": preferences["lightweight"],
            "ai_ml": preferences["ai_ml"]
        }

        return result


# ==========================================================
# Testing
# ==========================================================
if __name__ == "__main__":
    parser = IntentParser()

    print("=" * 60)
    print("KLARONE AI INTENT PARSER")
    print("=" * 60)

    while True:
        query = input("\nEnter Query (type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        result = parser.parse(query)
        print("\nDetected Intent\n")
        for key, value in result.items():
            print(f"{key:20}: {value}")