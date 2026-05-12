"""GPT-4 Vision integration — OCR + structured multi-language dish analysis."""

import json
import os
import time

from openai import OpenAI

from .exceptions import AnalysisError
from .locale_map import LOCALE_CODES
from .models import MenuAnalysisResult

_LOCALE_LIST = ", ".join(LOCALE_CODES)

_SYSTEM_PROMPT = f"""\
You are a professional menu analyst and food expert with deep knowledge of global cuisines.
You will receive a restaurant menu image. Your job is to perform OCR and dish analysis.

TASKS:
1. Extract ALL text from the menu image via OCR.
2. Identify every dish on the menu (name, description, price).
3. For each dish, produce a complete analysis using your domain knowledge.
4. Return the full structured JSON described below.

FOR EACH DISH, populate a "MultiLangOutput" object with exactly 64 locale keys:
  {_LOCALE_LIST}

For EACH locale key, provide a "DishAnalysis" object with ALL of these fields:

  dish_name            : str  — translated dish name in that language
  ingredients          : list[str]  — inferred ingredients, each translated
  dietary_flags        : list[str]  — applicable from: vegan, vegetarian, gluten_free, keto, halal, kosher
  allergen_warnings    : list[str]  — applicable from: lactose, nuts, shellfish, eggs, soy, gluten
  nutrition            : object or null — estimated per-serving values:
      calories         : int or null
      protein_g        : float or null
      carbs_g          : float or null
      fat_g            : float or null
  spice_level          : int 0-5 (0 = not spicy, 5 = extremely spicy)
  estimated_prep_minutes : int or null
  wine_pairing         : list[str]  — 0-3 wine suggestions, translated to that language

TOP-LEVEL RESPONSE SCHEMA:
{{
  "raw_text": "<full OCR text from menu>",
  "total_dishes_detected": <int>,
  "dishes": [
    {{
      "en":   {{ ...DishAnalysis... }},
      "it":   {{ ...DishAnalysis... }},
      "fr":   {{ ...DishAnalysis... }},
      "es":   {{ ...DishAnalysis... }},
      "de":   {{ ...DishAnalysis... }},
      "pt":   {{ ...DishAnalysis... }},
      "nl":   {{ ...DishAnalysis... }},
      "sv":   {{ ...DishAnalysis... }},
      "no":   {{ ...DishAnalysis... }},
      "da":   {{ ...DishAnalysis... }},
      "fi":   {{ ...DishAnalysis... }},
      "pl":   {{ ...DishAnalysis... }},
      "cs":   {{ ...DishAnalysis... }},
      "ro":   {{ ...DishAnalysis... }},
      "hu":   {{ ...DishAnalysis... }},
      "el":   {{ ...DishAnalysis... }},
      "ru":   {{ ...DishAnalysis... }},
      "he":   {{ ...DishAnalysis... }},
      "ar":   {{ ...DishAnalysis... }},
      "tr":   {{ ...DishAnalysis... }},
      "fa":   {{ ...DishAnalysis... }},
      "ku":   {{ ...DishAnalysis... }},
      "ps":   {{ ...DishAnalysis... }},
      "tg":   {{ ...DishAnalysis... }},
      "zh-CN": {{ ...DishAnalysis... }},
      "zh-TW": {{ ...DishAnalysis... }},
      "ja":   {{ ...DishAnalysis... }},
      "ko":   {{ ...DishAnalysis... }},
      "hi":   {{ ...DishAnalysis... }},
      "ur":   {{ ...DishAnalysis... }},
      "bn":   {{ ...DishAnalysis... }},
      "ta":   {{ ...DishAnalysis... }},
      "te":   {{ ...DishAnalysis... }},
      "mr":   {{ ...DishAnalysis... }},
      "gu":   {{ ...DishAnalysis... }},
      "kn":   {{ ...DishAnalysis... }},
      "ml":   {{ ...DishAnalysis... }},
      "pa":   {{ ...DishAnalysis... }},
      "ne":   {{ ...DishAnalysis... }},
      "si":   {{ ...DishAnalysis... }},
      "th":   {{ ...DishAnalysis... }},
      "vi":   {{ ...DishAnalysis... }},
      "id":   {{ ...DishAnalysis... }},
      "ms":   {{ ...DishAnalysis... }},
      "tl":   {{ ...DishAnalysis... }},
      "my":   {{ ...DishAnalysis... }},
      "km":   {{ ...DishAnalysis... }},
      "lo":   {{ ...DishAnalysis... }},
      "sw":   {{ ...DishAnalysis... }},
      "am":   {{ ...DishAnalysis... }},
      "om":   {{ ...DishAnalysis... }},
      "ha":   {{ ...DishAnalysis... }},
      "yo":   {{ ...DishAnalysis... }},
      "ig":   {{ ...DishAnalysis... }},
      "zu":   {{ ...DishAnalysis... }},
      "af":   {{ ...DishAnalysis... }},
      "st":   {{ ...DishAnalysis... }},
      "tn":   {{ ...DishAnalysis... }},
      "ts":   {{ ...DishAnalysis... }},
      "ve":   {{ ...DishAnalysis... }},
      "xh":   {{ ...DishAnalysis... }},
      "nso":  {{ ...DishAnalysis... }},
      "ss":   {{ ...DishAnalysis... }},
      "ber":  {{ ...DishAnalysis... }}
    }},
    ... (one object per dish)
  ]
}}

RULES:
- You MUST include ALL 64 locale keys for EVERY dish, no exceptions.
- Use domain knowledge to infer ingredients and allergens not visible in the image.
- Keep translations natural and idiomatic, not literal.
- Output ONLY the JSON object — no markdown fences, no explanations.
"""

_RETRY_SYSTEM_PROMPT = """\
You are a JSON generator. Return ONLY a valid JSON object — no markdown, no text.
The JSON must have keys: raw_text (string), total_dishes_detected (integer), dishes (array).
Each dish must have exactly 64 locale keys each containing: dish_name, ingredients, dietary_flags,
allergen_warnings, nutrition (calories/protein_g/carbs_g/fat_g), spice_level, estimated_prep_minutes, wine_pairing.
"""


def process_menu(
    base64_image: str,
    mime_type: str,
    model: str = "gpt-4o",
    api_key: str | None = None,
) -> MenuAnalysisResult:
    """Send a base64-encoded menu image to GPT-4 Vision and return structured analysis.

    Args:
        base64_image: Base64-encoded image data (without data-URI prefix).
        mime_type: MIME type of the image, e.g. "image/jpeg".
        model: OpenAI model to use (must support vision).
        api_key: OpenAI API key; falls back to OPENAI_API_KEY env var.

    Returns:
        Validated MenuAnalysisResult.

    Raises:
        AnalysisError: if GPT-4 Vision fails or returns unparseable JSON.
    """
    resolved_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_key:
        raise AnalysisError(
            "No OpenAI API key provided. "
            "Pass api_key= or set the OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=resolved_key)
    start_ms = int(time.time() * 1000)

    raw_json = _call_vision(client, base64_image, mime_type, model, _SYSTEM_PROMPT)

    try:
        result = _parse_result(raw_json, start_ms)
    except Exception as exc:
        # One retry with a simplified prompt
        raw_json = _call_vision(client, base64_image, mime_type, model, _RETRY_SYSTEM_PROMPT)
        try:
            result = _parse_result(raw_json, start_ms)
        except Exception as retry_exc:
            raise AnalysisError(
                "Failed to parse GPT-4 Vision response after retry",
                {"original_error": str(exc), "retry_error": str(retry_exc), "raw": raw_json[:500]},
            ) from retry_exc

    return result


def _call_vision(
    client: OpenAI,
    base64_image: str,
    mime_type: str,
    model: str,
    system_prompt: str,
) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=16384,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": "high",
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Please analyze this menu image. "
                                "Return the full JSON with ALL 64 locale translations for every dish."
                            ),
                        },
                    ],
                },
            ],
        )
    except Exception as exc:
        raise AnalysisError(f"OpenAI API call failed: {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise AnalysisError("GPT-4 Vision returned an empty response")
    return content


def _parse_result(raw_json: str, start_ms: int) -> MenuAnalysisResult:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise AnalysisError(f"Response is not valid JSON: {exc}") from exc

    elapsed = int(time.time() * 1000) - start_ms
    data["processing_time_ms"] = elapsed

    return MenuAnalysisResult.model_validate(data)
