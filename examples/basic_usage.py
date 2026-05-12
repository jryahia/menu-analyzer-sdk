"""Basic usage example for the Menu Analyzer SDK.

Run this script after installing the package:

    pip install -e ..
    OPENAI_API_KEY=sk-... python basic_usage.py

Sample menu image URL (Italian restaurant, public domain):
    https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Biologia_marina_chavez.jpg/320px-Biologia_marina_chavez.jpg
"""

import json
import os

from menu_analyzer import MenuAnalyzer

# ── Configuration ─────────────────────────────────────────────────────────────

# Real menu image URL you can test with — a publicly accessible sample menu
SAMPLE_MENU_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/"
    "Gastronom%C3%ADa_de_Espa%C3%B1a.jpg/640px-Gastronom%C3%ADa_de_Espa%C3%B1a.jpg"
)

# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Set the OPENAI_API_KEY environment variable before running.")
        return

    print("Initializing Menu Analyzer...")
    analyzer = MenuAnalyzer(api_key=api_key)

    print(f"\nSupported locales: {len(analyzer.supported_locales())}")
    for locale in analyzer.supported_locales()[:5]:
        print(f"  {locale['flag_emoji']}  {locale['code']:6s}  {locale['name']}")
    print("  ... (64 total)\n")

    print(f"Analyzing menu image: {SAMPLE_MENU_URL}\n")
    print("This may take 10-30 seconds for a full 64-language response...\n")

    result = analyzer.analyze_sync(SAMPLE_MENU_URL)

    print(f"OCR raw text preview:\n{(result.raw_text or '')[:300]}\n")
    print(f"Dishes detected: {result.total_dishes_detected}")
    print(f"Processing time: {result.processing_time_ms} ms\n")

    for i, dish in enumerate(result.dishes, start=1):
        print(f"─── Dish {i} ─────────────────────────────────")
        print(f"  EN: {dish.en.dish_name}")
        print(f"  IT: {dish.it.dish_name}")
        print(f"  FR: {dish.fr.dish_name}")
        print(f"  AR: {dish.ar.dish_name}")
        print(f"  ZH: {dish.zh_CN.dish_name}")
        print(f"  JA: {dish.ja.dish_name}")
        print(f"  HI: {dish.hi.dish_name}")
        print(f"  SW: {dish.sw.dish_name}")
        print()
        print(f"  Ingredients (EN):       {', '.join(dish.en.ingredients[:4])}")
        print(f"  Dietary flags (EN):     {', '.join(dish.en.dietary_flags) or 'none'}")
        print(f"  Allergen warnings (EN): {', '.join(dish.en.allergen_warnings) or 'none'}")
        print(f"  Spice level:            {dish.en.spice_level}/5")
        if dish.en.nutrition:
            n = dish.en.nutrition
            print(f"  Nutrition (est.):       {n.calories} kcal | {n.protein_g}g protein")
        if dish.en.wine_pairing:
            print(f"  Wine pairing (EN):      {', '.join(dish.en.wine_pairing)}")
        print()

    # Full JSON output
    result_dict = result.model_dump(by_alias=True)
    print("Full JSON result (first dish, English only):")
    first_dish_en = result_dict["dishes"][0].get("en") if result_dict["dishes"] else {}
    print(json.dumps(first_dish_en, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
