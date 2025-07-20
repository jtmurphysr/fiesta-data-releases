#!/usr/bin/env python3
import json
import re
from collections import defaultdict

# Serveware shape overrides
SERVEWARE_OVERRIDES = {
    "Bistro Coupe 7 5/8 Inch Medium Bowl 38 OZ",
    "Fiesta 9 5/8 Inch Small Oval Serving Platter",
    "Fiesta 13 5/8 Inch Large Oval Serving Platter",
    "Bistro Coupe 9 5/8 Inch Large Bowl 68 OZ",
    "Classic Rim 8 1/4 Inch Large Serving Bowl 40 OZ",
    "2-Piece Chip and Dip Set 12 7/8 Inch",
    "Fiesta 11 7/8 Inch Oblong Serving Platter",
    "Fiesta 11 5/8 Inch Medium Oval Serving Platter",
    "Bistro Coupe 10 1/2 Inch Extra Large Bowl 96 OZ",
    "Fiesta 12 Inch Large Rectangular Platter",
    "Fiesta 18 1/2 OZ Gravy Sauceboat",
    "Classic Rim 10 1/2 Inch Extra Large Serving Bowl",
}

HLC_CATEGORIES = {
    "Bakeware", "Bowls", "Countertop Accessories",
    "Mugs, Cups & Saucers", "Pitchers, Teapots & Vases",
    "Plates", "Serveware", "Shapes", "Other"
}

CATEGORY_RULES = [
    ("Bakeware", [r"baker", r"casserole", r"loaf pan", r"pie.*plate"]),
    ("Bowls", [r"bowl"]),
    ("Countertop Accessories", [r"canister", r"cookie jar", r"salt.*pepper", r"shaker", r"utensil crock"]),
    ("Mugs, Cups & Saucers", [r"mug", r"cup", r"saucer"]),
    ("Pitchers, Teapots & Vases", [r"pitcher", r"teapot", r"vase", r"carafe"]),
    ("Plates", [r"plate"]),
    ("Serveware", [r"platter", r"chip.*dip", r"serving", r"sauceboat"]),
    ("Shapes", [r"heart", r"star", r"shell", r"tree", r"pumpkin", r"christmas", r"halloween", r"egg", r"snowflake"]),
]

def normalize_category(shape_name):
    lname = shape_name.lower()
    if shape_name in SERVEWARE_OVERRIDES:
        return "Serveware"
    for category, patterns in CATEGORY_RULES:
        if any(re.search(pat, lname) for pat in patterns):
            return category
    return "Other"

def normalize_shape_name(shape):
    match = re.match(r'([\d\s/]+) Inch (.*?) Bowl (\d+)\s*OZ', shape, re.IGNORECASE)
    if match:
        size, detail, volume = match.groups()
        return f'Bowl, {detail.strip()} ({size.strip()}", {volume.strip()} oz.)'
    return shape

def normalize_dataset(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen = set()
    result = []
    metrics = {
        "total_records": len(data),
        "normalized_shapes": 0,
        "category_changes": 0,
        "deduplicated": 0
    }
    shape_log = []
    category_log = []

    for item in data:
        original_shape = item["shape"]
        normalized_shape = normalize_shape_name(original_shape)

        if normalized_shape != original_shape:
            metrics["normalized_shapes"] += 1
            shape_log.append((original_shape, normalized_shape))

        item["shape"] = normalized_shape

        original_category = item["category"]
        new_category = normalize_category(normalized_shape)
        if new_category != original_category:
            metrics["category_changes"] += 1
            category_log.append((original_category, new_category, normalized_shape))

        item["category"] = new_category

        key = f"{normalized_shape}|{item['color']}"
        if key in seen:
            metrics["deduplicated"] += 1
            continue
        seen.add(key)
        result.append(item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # Log summary
    print("\nNormalization Complete:")
    print(json.dumps(metrics, indent=2))
    if shape_log:
        print("\nShape Normalizations:")
        for orig, norm in shape_log:
            print(f"- {orig} → {norm}")
    if category_log:
        print("\nCategory Changes:")
        for orig, new, shape in category_log:
            print(f"- {shape}: {orig} → {new}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python normalize_fiesta_dataset.py input.json output.json")
    else:
        normalize_dataset(sys.argv[1], sys.argv[2])
