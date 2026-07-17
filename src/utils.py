import re
import pandas as pd

# ==========================================================
# Extract GPU Brand
# ==========================================================
def extract_gpu_brand(gpu):
    if pd.isna(gpu):
        return "Unknown"

    gpu = gpu.upper()

    if "NVIDIA" in gpu:
        return "NVIDIA"
    elif "INTEL" in gpu:
        return "INTEL"
    elif "AMD" in gpu:
        return "AMD"
    elif "APPLE" in gpu:
        return "APPLE"
    elif "QUALCOMM" in gpu:
        return "QUALCOMM"

    return "OTHER"


# ==========================================================
# Extract GPU Type
# ==========================================================
def extract_gpu_type(gpu):
    if pd.isna(gpu):
        return "Unknown"

    gpu = gpu.upper()

    dedicated_keywords = [
        "RTX",
        "GTX",
        "MX",
        "ARC",
        "QUADRO",
        "RX"
    ]

    for keyword in dedicated_keywords:
        if keyword in gpu:
            return "Dedicated"

    return "Integrated"


# ==========================================================
# Extract GPU VRAM
# ==========================================================
def extract_gpu_vram(gpu):
    if pd.isna(gpu):
        return 0

    gpu = gpu.upper()

    # Find numbers before GB
    match = re.search(r"(\d+)\s*GB", gpu)
    if match:
        return int(match.group(1))

    return 0


# ==========================================================
# Extract GPU Series
# ==========================================================
def extract_gpu_series(gpu):
    if pd.isna(gpu):
        return "Unknown"

    gpu = gpu.upper()

    if "RTX" in gpu:
        return "RTX"
    elif "GTX" in gpu:
        return "GTX"
    elif "MX" in gpu:
        return "MX"
    elif "IRIS XE" in gpu:
        return "IRIS XE"
    elif "UHD" in gpu:
        return "UHD"
    elif "VEGA" in gpu:
        return "VEGA"
    elif "RX" in gpu:
        return "RX"
    elif "ARC" in gpu:
        return "ARC"
    elif "ADRENO" in gpu:
        return "ADRENO"
    elif "APPLE" in gpu:
        return "APPLE"

    return "OTHER"


# ==========================================================
# Extract CPU Brand
# ==========================================================
def extract_cpu_brand(cpu):
    if pd.isna(cpu):
        return "Unknown"

    cpu = cpu.upper()
    # Apple must be checked first
    if "APPLE" in cpu or cpu.startswith("M1") or cpu.startswith("M2"):
        return "APPLE"
    elif "INTEL" in cpu or "CORE I3" in cpu or "CORE I5" in cpu or "CORE I7" in cpu or "CORE I9" in cpu or "CELERON" in cpu or "PENTIUM" in cpu:
        return "INTEL"
    elif "AMD" in cpu or "RYZEN" in cpu or "ATHLON" in cpu:
        return "AMD"
    elif "SNAPDRAGON" in cpu:
        return "QUALCOMM"

    return "OTHER"


# ==========================================================
# Extract CPU Family
# ==========================================================
def extract_cpu_family(cpu):
    if pd.isna(cpu):
        return "Unknown"

    cpu = cpu.upper()

    if "CORE I3" in cpu:
        return "CORE I3"
    elif "CORE I5" in cpu:
        return "CORE I5"
    elif "CORE I7" in cpu:
        return "CORE I7"
    elif "CORE I9" in cpu:
        return "CORE I9"
    elif "RYZEN 3" in cpu:
        return "RYZEN 3"
    elif "RYZEN 5" in cpu:
        return "RYZEN 5"
    elif "RYZEN 7" in cpu:
        return "RYZEN 7"
    elif "RYZEN 9" in cpu:
        return "RYZEN 9"
    elif "ATHLON" in cpu:
        return "ATHLON"
    elif "PENTIUM" in cpu:
        return "PENTIUM"
    elif "CELERON" in cpu:
        return "CELERON"
    elif "M1" in cpu:
        return "M1"
    elif "M2" in cpu:
        return "M2"

    return "OTHER"


# ==========================================================
# Extract CPU Generation
# ==========================================================
def extract_cpu_generation(cpu):
    if pd.isna(cpu):
        return 0

    cpu = cpu.upper()

    # Intel generations
    intel_match = re.search(r"(\d+)(ST|ND|RD|TH)\s+GEN", cpu)
    if intel_match:
        return int(intel_match.group(1))

    # AMD Ryzen generations (5600H -> 5000 series)
    amd_match = re.search(r"RYZEN\s+\d[\s-]*(\d{4})", cpu)
    if amd_match:
        return int(amd_match.group(1)[0]) * 1000

    # Apple
    if "M1" in cpu:
        return 1
    elif "M2" in cpu:
        return 2

    return 0


# ==========================================================
# Extract CPU Series
# ==========================================================
def extract_cpu_series(cpu):
    if pd.isna(cpu):
        return "Unknown"

    cpu = cpu.upper()

    if "HX" in cpu:
        return "HX"
    elif "HS" in cpu:
        return "HS"
    elif re.search(r"\dU\b", cpu):
        return "U"
    elif re.search(r"\dH\b", cpu):
        return "H"
    elif re.search(r"\dP\b", cpu):
        return "P"
    elif "M1" in cpu or "M2" in cpu:
        return "APPLE"

    return "OTHER"


# ==========================================================
# Extract CPU Performance Tier
# ==========================================================
def extract_cpu_tier(cpu):
    if pd.isna(cpu):
        return "Unknown"

    cpu = cpu.upper()

    if "CORE I3" in cpu or "RYZEN 3" in cpu or "CELERON" in cpu or "PENTIUM" in cpu:
        return "ENTRY"
    elif "CORE I5" in cpu or "RYZEN 5" in cpu:
        return "MID"
    elif "CORE I7" in cpu or "RYZEN 7" in cpu:
        return "HIGH"
    elif "CORE I9" in cpu or "RYZEN 9" in cpu:
        return "ENTHUSIAST"
    elif "M1" in cpu or "M2" in cpu:
        return "APPLE"

    return "OTHER"


# ==========================================================
# Score Calculator
# ==========================================================
def calculate_score(row, category):
    graphics = str(row["graphics"]).upper()
    processor = str(row["processor_name"]).upper()
    generation = row["cpu_generation"]
    ram = row["ram(GB)"]
    ssd = row["ssd(GB)"]
    spec = row["spec_score"]

    # ======================================================
    # GPU Performance Score
    # ======================================================
    gpu_score = 15

    # RTX Series
    if "RTX 4090" in graphics:
        gpu_score = 100
    elif "RTX 4080" in graphics:
        gpu_score = 99
    elif "RTX 4070" in graphics:
        gpu_score = 98
    elif "RTX 4060" in graphics:
        gpu_score = 96
    elif "RTX 4050" in graphics:
        gpu_score = 92
    elif "RTX 3060" in graphics:
        gpu_score = 90
    elif "RTX 3050 TI" in graphics:
        gpu_score = 87
    elif "RTX 3050" in graphics:
        gpu_score = 84
    elif "RTX 2050" in graphics:
        gpu_score = 78
    # GTX Series
    elif "GTX 1660 TI" in graphics:
        gpu_score = 82
    elif "GTX 1660" in graphics:
        gpu_score = 78
    elif "GTX 1650" in graphics:
        gpu_score = 72
    elif "GTX 1050 TI" in graphics:
        gpu_score = 60
    elif "GTX 1050" in graphics:
        gpu_score = 55
    # Intel Arc
    elif "ARC" in graphics:
        gpu_score = 75
    # AMD Radeon
    elif "RX 6800" in graphics:
        gpu_score = 96
    elif "RX 6700" in graphics:
        gpu_score = 92
    elif "RX 6650" in graphics:
        gpu_score = 88
    elif "RX 6600" in graphics:
        gpu_score = 84
    elif "RX 6500" in graphics:
        gpu_score = 78
    # Integrated
    elif "IRIS XE" in graphics:
        gpu_score = 35
    elif "UHD" in graphics:
        gpu_score = 15
    elif "VEGA 8" in graphics:
        gpu_score = 40
    elif "VEGA 7" in graphics:
        gpu_score = 35
    elif "VEGA 5" in graphics:
        gpu_score = 28
    elif "VEGA 3" in graphics:
        gpu_score = 22
    # Apple
    elif "M2" in graphics:
        gpu_score = 70
    elif "M1" in graphics:
        gpu_score = 60

    # ======================================================
    # CPU Performance Score
    # ======================================================
    cpu_score = 30

    # Base CPU Score
    if "CORE I9" in processor:
        cpu_score = 100
    elif "CORE I7" in processor:
        cpu_score = 92
    elif "CORE I5" in processor:
        cpu_score = 80
    elif "CORE I3" in processor:
        cpu_score = 60
    elif "RYZEN 9" in processor:
        cpu_score = 100
    elif "RYZEN 7" in processor:
         cpu_score = 92
    elif "RYZEN 5" in processor:
        cpu_score = 80
    elif "RYZEN 3" in processor:
        cpu_score = 60
    elif "APPLE M2" in processor:
         cpu_score = 94
    elif "APPLE M1" in processor:
        cpu_score = 88
    elif "CELERON" in processor:
        cpu_score = 18
    elif "PENTIUM" in processor:
      cpu_score = 22
    elif "ATHLON" in processor:
        cpu_score = 30

    # CPU Generation Bonus
    if generation == 11:
        cpu_score += 2
    elif generation == 12:
        cpu_score += 4
    elif generation == 13:
        cpu_score += 6
    elif generation >= 14:
        cpu_score += 8
    elif generation == 3000:
        cpu_score += 1
    elif generation == 4000:
        cpu_score += 2
    elif generation == 5000:
        cpu_score += 4
    elif generation == 6000:
        cpu_score += 6
    elif generation >= 7000:
        cpu_score += 8

    # CPU Series Bonus
    if "HX" in processor:
        cpu_score += 8
    elif "HS" in processor:
        cpu_score += 6
    elif "H" in processor:
        cpu_score += 5
    elif "P" in processor:
        cpu_score += 2
    elif "U" in processor:
        cpu_score -= 5

    # Keep CPU score within range
    cpu_score = max(0, min(100, cpu_score))

    # ======================================================
    # RAM Performance Score
    # ======================================================
    if ram >= 64:
        ram_score = 100
    elif ram >= 32:
        ram_score = 95
    elif ram >= 16:
        ram_score = 85
    elif ram >= 12:
        ram_score = 75
    elif ram >= 8:
        ram_score = 60
    elif ram >= 4:
        ram_score = 40
    else:
        ram_score = 20

    # ======================================================
    # SSD Performance Score
    # ======================================================
    if ssd >= 2048:
        ssd_score = 100
    elif ssd >= 1024:
        ssd_score = 95
    elif ssd >= 512:
        ssd_score = 80
    elif ssd >= 256:
        ssd_score = 60
    elif ssd >= 128:
        ssd_score = 40
    else:
        ssd_score = 20

    # ======================================================
    # Gaming Suitability Score
    # ======================================================
    gaming_score = (
        gpu_score * 0.55 +
        cpu_score * 0.20 +
        ram_score * 0.15 +
        ssd_score * 0.05 +
        spec * 0.05
    )

    # ======================================================
    # Student Suitability Score
    # ======================================================
    student_score = (
        gpu_score * 0.10 +
        cpu_score * 0.30 +
        ram_score * 0.25 +
        ssd_score * 0.20 +
        spec * 0.15
    )

    # Student Adjustments
    if "RTX" in graphics:
        student_score -= 5
    if ram > 32:
        student_score -= 5
    if "HX" in processor:
        student_score -= 5

    # ======================================================
    # Business Suitability Score
    # ======================================================
    business_score = (
        gpu_score * 0.05 +
        cpu_score * 0.35 +
        ram_score * 0.25 +
        ssd_score * 0.20 +
        spec * 0.15
    )

    # Business Adjustments
    if "RTX" in graphics:
        business_score -= 10
    elif "GTX" in graphics:
        business_score -= 5
    elif "RX" in graphics:
        business_score -= 8
    if ram > 16:
        business_score -= 5
    if "HX" in processor:
        business_score -= 8

    # Keep Scores Between 0 and 100
    gaming_score = max(0, min(100, gaming_score))
    student_score = max(0, min(100, student_score))
    business_score = max(0, min(100, business_score))

    if category == "gaming":
        return round(gaming_score)
    elif category == "student":
        return round(student_score)
    elif category == "business":
        return round(business_score)
    else:
        return 0


# ==========================================================
# Format Indian Currency
# ==========================================================
def format_indian_currency(number):
    if number is None:
        return ""
    try:
        s = str(int(round(float(number))))
    except Exception:
        return str(number)
        
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    remaining = s[:-3]
    groups = []
    while len(remaining) > 0:
        groups.append(remaining[-2:])
        remaining = remaining[:-2]
    groups.reverse()
    return ",".join(groups) + "," + last_three

