"""Mapping of all 64 supported locale codes to human-readable metadata."""

from typing import TypedDict


class LocaleInfo(TypedDict):
    name: str
    native_name: str
    flag_emoji: str


LOCALE_MAP: dict[str, LocaleInfo] = {
    # ── European — Western ────────────────────────────────────────────────────
    "en":    {"name": "English",     "native_name": "English",          "flag_emoji": "🇬🇧"},
    "it":    {"name": "Italian",     "native_name": "Italiano",         "flag_emoji": "🇮🇹"},
    "fr":    {"name": "French",      "native_name": "Français",         "flag_emoji": "🇫🇷"},
    "es":    {"name": "Spanish",     "native_name": "Español",          "flag_emoji": "🇪🇸"},
    "de":    {"name": "German",      "native_name": "Deutsch",          "flag_emoji": "🇩🇪"},
    "pt":    {"name": "Portuguese",  "native_name": "Português",        "flag_emoji": "🇵🇹"},
    "nl":    {"name": "Dutch",       "native_name": "Nederlands",       "flag_emoji": "🇳🇱"},
    "sv":    {"name": "Swedish",     "native_name": "Svenska",          "flag_emoji": "🇸🇪"},
    "no":    {"name": "Norwegian",   "native_name": "Norsk",            "flag_emoji": "🇳🇴"},
    "da":    {"name": "Danish",      "native_name": "Dansk",            "flag_emoji": "🇩🇰"},
    "fi":    {"name": "Finnish",     "native_name": "Suomi",            "flag_emoji": "🇫🇮"},
    "pl":    {"name": "Polish",      "native_name": "Polski",           "flag_emoji": "🇵🇱"},
    "cs":    {"name": "Czech",       "native_name": "Čeština",          "flag_emoji": "🇨🇿"},
    "ro":    {"name": "Romanian",    "native_name": "Română",           "flag_emoji": "🇷🇴"},
    "hu":    {"name": "Hungarian",   "native_name": "Magyar",           "flag_emoji": "🇭🇺"},
    "el":    {"name": "Greek",       "native_name": "Ελληνικά",         "flag_emoji": "🇬🇷"},

    # ── European — Eastern / Other scripts ───────────────────────────────────
    "ru":    {"name": "Russian",     "native_name": "Русский",          "flag_emoji": "🇷🇺"},
    "he":    {"name": "Hebrew",      "native_name": "עברית",            "flag_emoji": "🇮🇱"},

    # ── Middle East / Central Asia ────────────────────────────────────────────
    "ar":    {"name": "Arabic",      "native_name": "العربية",          "flag_emoji": "🇸🇦"},
    "tr":    {"name": "Turkish",     "native_name": "Türkçe",           "flag_emoji": "🇹🇷"},
    "fa":    {"name": "Persian",     "native_name": "فارسی",            "flag_emoji": "🇮🇷"},
    "ku":    {"name": "Kurdish",     "native_name": "Kurdî",            "flag_emoji": "🏳️"},
    "ps":    {"name": "Pashto",      "native_name": "پښتو",             "flag_emoji": "🇦🇫"},
    "tg":    {"name": "Tajik",       "native_name": "Тоҷикӣ",           "flag_emoji": "🇹🇯"},

    # ── East Asia ─────────────────────────────────────────────────────────────
    "zh-CN": {"name": "Chinese (Simplified)",  "native_name": "中文（简体）", "flag_emoji": "🇨🇳"},
    "zh-TW": {"name": "Chinese (Traditional)", "native_name": "中文（繁體）", "flag_emoji": "🇹🇼"},
    "ja":    {"name": "Japanese",    "native_name": "日本語",            "flag_emoji": "🇯🇵"},
    "ko":    {"name": "Korean",      "native_name": "한국어",            "flag_emoji": "🇰🇷"},

    # ── South Asia ────────────────────────────────────────────────────────────
    "hi":    {"name": "Hindi",       "native_name": "हिन्दी",           "flag_emoji": "🇮🇳"},
    "ur":    {"name": "Urdu",        "native_name": "اردو",             "flag_emoji": "🇵🇰"},
    "bn":    {"name": "Bengali",     "native_name": "বাংলা",            "flag_emoji": "🇧🇩"},
    "ta":    {"name": "Tamil",       "native_name": "தமிழ்",            "flag_emoji": "🇮🇳"},
    "te":    {"name": "Telugu",      "native_name": "తెలుగు",           "flag_emoji": "🇮🇳"},
    "mr":    {"name": "Marathi",     "native_name": "मराठी",            "flag_emoji": "🇮🇳"},
    "gu":    {"name": "Gujarati",    "native_name": "ગુજરાતી",          "flag_emoji": "🇮🇳"},
    "kn":    {"name": "Kannada",     "native_name": "ಕನ್ನಡ",            "flag_emoji": "🇮🇳"},
    "ml":    {"name": "Malayalam",   "native_name": "മലയാളം",           "flag_emoji": "🇮🇳"},
    "pa":    {"name": "Punjabi",     "native_name": "ਪੰਜਾਬੀ",           "flag_emoji": "🇮🇳"},
    "ne":    {"name": "Nepali",      "native_name": "नेपाली",           "flag_emoji": "🇳🇵"},
    "si":    {"name": "Sinhala",     "native_name": "සිංහල",            "flag_emoji": "🇱🇰"},

    # ── Southeast Asia ────────────────────────────────────────────────────────
    "th":    {"name": "Thai",        "native_name": "ภาษาไทย",          "flag_emoji": "🇹🇭"},
    "vi":    {"name": "Vietnamese",  "native_name": "Tiếng Việt",       "flag_emoji": "🇻🇳"},
    "id":    {"name": "Indonesian",  "native_name": "Bahasa Indonesia",  "flag_emoji": "🇮🇩"},
    "ms":    {"name": "Malay",       "native_name": "Bahasa Melayu",    "flag_emoji": "🇲🇾"},
    "tl":    {"name": "Filipino",    "native_name": "Filipino",         "flag_emoji": "🇵🇭"},
    "my":    {"name": "Burmese",     "native_name": "မြန်မာဘာသာ",       "flag_emoji": "🇲🇲"},
    "km":    {"name": "Khmer",       "native_name": "ភាសាខ្មែរ",         "flag_emoji": "🇰🇭"},
    "lo":    {"name": "Lao",         "native_name": "ພາສາລາວ",          "flag_emoji": "🇱🇦"},

    # ── Africa — East / Horn ─────────────────────────────────────────────────
    "sw":    {"name": "Swahili",     "native_name": "Kiswahili",        "flag_emoji": "🇰🇪"},
    "am":    {"name": "Amharic",     "native_name": "አማርኛ",             "flag_emoji": "🇪🇹"},
    "om":    {"name": "Oromo",       "native_name": "Afaan Oromoo",     "flag_emoji": "🇪🇹"},

    # ── Africa — West ─────────────────────────────────────────────────────────
    "ha":    {"name": "Hausa",       "native_name": "Hausa",            "flag_emoji": "🇳🇬"},
    "yo":    {"name": "Yoruba",      "native_name": "Yorùbá",           "flag_emoji": "🇳🇬"},
    "ig":    {"name": "Igbo",        "native_name": "Igbo",             "flag_emoji": "🇳🇬"},

    # ── Africa — South ────────────────────────────────────────────────────────
    "zu":    {"name": "Zulu",        "native_name": "isiZulu",          "flag_emoji": "🇿🇦"},
    "af":    {"name": "Afrikaans",   "native_name": "Afrikaans",        "flag_emoji": "🇿🇦"},
    "st":    {"name": "Sesotho",     "native_name": "Sesotho",          "flag_emoji": "🇿🇦"},
    "tn":    {"name": "Setswana",    "native_name": "Setswana",         "flag_emoji": "🇿🇦"},
    "ts":    {"name": "Tsonga",      "native_name": "Xitsonga",         "flag_emoji": "🇿🇦"},
    "ve":    {"name": "Venda",       "native_name": "Tshivenḓa",        "flag_emoji": "🇿🇦"},
    "xh":    {"name": "Xhosa",       "native_name": "isiXhosa",         "flag_emoji": "🇿🇦"},
    "nso":   {"name": "Northern Sotho", "native_name": "Sesotho sa Leboa", "flag_emoji": "🇿🇦"},
    "ss":    {"name": "Swati",       "native_name": "siSwati",          "flag_emoji": "🇸🇿"},

    # ── Afro-Asiatic / Other ──────────────────────────────────────────────────
    "ber":   {"name": "Berber (Tamazight)", "native_name": "ⵜⴰⵎⴰⵣⵉⵖⵜ", "flag_emoji": "🇲🇦"},
}

# Ordered list for consistent iteration
LOCALE_CODES: list[str] = list(LOCALE_MAP.keys())

assert len(LOCALE_CODES) == 64, f"Expected 64 locales, got {len(LOCALE_CODES)}"


def get_locale_info(code: str) -> LocaleInfo:
    """Return metadata for a locale code, raising KeyError if unsupported."""
    return LOCALE_MAP[code]
