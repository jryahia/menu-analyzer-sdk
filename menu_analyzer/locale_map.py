"""Mapping of all 64 supported locale codes to human-readable metadata."""

from typing import TypedDict


class LocaleInfo(TypedDict):
    name: str
    native_name: str
    flag_emoji: str


def _flag(country: str) -> str:
    """Flag for an ISO 3166-1 alpha-2 code, built from regional indicator letters."""
    return "".join(chr(0x1F1E6 + ord(letter) - ord("A")) for letter in country)


# No national flag: Kurdish uses the generic white flag.
_WHITE_FLAG = "\U0001F3F3\uFE0F"


LOCALE_MAP: dict[str, LocaleInfo] = {
    # ── European — Western ────────────────────────────────────────────────────
    "en":    {"name": "English",     "native_name": "English",          "flag_emoji": _flag("GB")},
    "it":    {"name": "Italian",     "native_name": "Italiano",         "flag_emoji": _flag("IT")},
    "fr":    {"name": "French",      "native_name": "Français",         "flag_emoji": _flag("FR")},
    "es":    {"name": "Spanish",     "native_name": "Español",          "flag_emoji": _flag("ES")},
    "de":    {"name": "German",      "native_name": "Deutsch",          "flag_emoji": _flag("DE")},
    "pt":    {"name": "Portuguese",  "native_name": "Português",        "flag_emoji": _flag("PT")},
    "nl":    {"name": "Dutch",       "native_name": "Nederlands",       "flag_emoji": _flag("NL")},
    "sv":    {"name": "Swedish",     "native_name": "Svenska",          "flag_emoji": _flag("SE")},
    "no":    {"name": "Norwegian",   "native_name": "Norsk",            "flag_emoji": _flag("NO")},
    "da":    {"name": "Danish",      "native_name": "Dansk",            "flag_emoji": _flag("DK")},
    "fi":    {"name": "Finnish",     "native_name": "Suomi",            "flag_emoji": _flag("FI")},
    "pl":    {"name": "Polish",      "native_name": "Polski",           "flag_emoji": _flag("PL")},
    "cs":    {"name": "Czech",       "native_name": "Čeština",          "flag_emoji": _flag("CZ")},
    "ro":    {"name": "Romanian",    "native_name": "Română",           "flag_emoji": _flag("RO")},
    "hu":    {"name": "Hungarian",   "native_name": "Magyar",           "flag_emoji": _flag("HU")},
    "el":    {"name": "Greek",       "native_name": "Ελληνικά",         "flag_emoji": _flag("GR")},

    # ── European — Eastern / Other scripts ───────────────────────────────────
    "ru":    {"name": "Russian",     "native_name": "Русский",          "flag_emoji": _flag("RU")},
    "he":    {"name": "Hebrew",      "native_name": "עברית",            "flag_emoji": _flag("IL")},

    # ── Middle East / Central Asia ────────────────────────────────────────────
    "ar":    {"name": "Arabic",      "native_name": "العربية",          "flag_emoji": _flag("SA")},
    "tr":    {"name": "Turkish",     "native_name": "Türkçe",           "flag_emoji": _flag("TR")},
    "fa":    {"name": "Persian",     "native_name": "فارسی",            "flag_emoji": _flag("IR")},
    "ku":    {"name": "Kurdish",     "native_name": "Kurdî",            "flag_emoji": _WHITE_FLAG},
    "ps":    {"name": "Pashto",      "native_name": "پښتو",             "flag_emoji": _flag("AF")},
    "tg":    {"name": "Tajik",       "native_name": "Тоҷикӣ",           "flag_emoji": _flag("TJ")},

    # ── East Asia ─────────────────────────────────────────────────────────────
    "zh-CN": {"name": "Chinese (Simplified)",  "native_name": "中文（简体）", "flag_emoji": _flag("CN")},
    "zh-TW": {"name": "Chinese (Traditional)", "native_name": "中文（繁體）", "flag_emoji": _flag("TW")},
    "ja":    {"name": "Japanese",    "native_name": "日本語",            "flag_emoji": _flag("JP")},
    "ko":    {"name": "Korean",      "native_name": "한국어",            "flag_emoji": _flag("KR")},

    # ── South Asia ────────────────────────────────────────────────────────────
    "hi":    {"name": "Hindi",       "native_name": "हिन्दी",           "flag_emoji": _flag("IN")},
    "ur":    {"name": "Urdu",        "native_name": "اردو",             "flag_emoji": _flag("PK")},
    "bn":    {"name": "Bengali",     "native_name": "বাংলা",            "flag_emoji": _flag("BD")},
    "ta":    {"name": "Tamil",       "native_name": "தமிழ்",            "flag_emoji": _flag("IN")},
    "te":    {"name": "Telugu",      "native_name": "తెలుగు",           "flag_emoji": _flag("IN")},
    "mr":    {"name": "Marathi",     "native_name": "मराठी",            "flag_emoji": _flag("IN")},
    "gu":    {"name": "Gujarati",    "native_name": "ગુજરાતી",          "flag_emoji": _flag("IN")},
    "kn":    {"name": "Kannada",     "native_name": "ಕನ್ನಡ",            "flag_emoji": _flag("IN")},
    "ml":    {"name": "Malayalam",   "native_name": "മലയാളം",           "flag_emoji": _flag("IN")},
    "pa":    {"name": "Punjabi",     "native_name": "ਪੰਜਾਬੀ",           "flag_emoji": _flag("IN")},
    "ne":    {"name": "Nepali",      "native_name": "नेपाली",           "flag_emoji": _flag("NP")},
    "si":    {"name": "Sinhala",     "native_name": "සිංහල",            "flag_emoji": _flag("LK")},

    # ── Southeast Asia ────────────────────────────────────────────────────────
    "th":    {"name": "Thai",        "native_name": "ภาษาไทย",          "flag_emoji": _flag("TH")},
    "vi":    {"name": "Vietnamese",  "native_name": "Tiếng Việt",       "flag_emoji": _flag("VN")},
    "id":    {"name": "Indonesian",  "native_name": "Bahasa Indonesia",  "flag_emoji": _flag("ID")},
    "ms":    {"name": "Malay",       "native_name": "Bahasa Melayu",    "flag_emoji": _flag("MY")},
    "tl":    {"name": "Filipino",    "native_name": "Filipino",         "flag_emoji": _flag("PH")},
    "my":    {"name": "Burmese",     "native_name": "မြန်မာဘာသာ",       "flag_emoji": _flag("MM")},
    "km":    {"name": "Khmer",       "native_name": "ភាសាខ្មែរ",         "flag_emoji": _flag("KH")},
    "lo":    {"name": "Lao",         "native_name": "ພາສາລາວ",          "flag_emoji": _flag("LA")},

    # ── Africa — East / Horn ─────────────────────────────────────────────────
    "sw":    {"name": "Swahili",     "native_name": "Kiswahili",        "flag_emoji": _flag("KE")},
    "am":    {"name": "Amharic",     "native_name": "አማርኛ",             "flag_emoji": _flag("ET")},
    "om":    {"name": "Oromo",       "native_name": "Afaan Oromoo",     "flag_emoji": _flag("ET")},

    # ── Africa — West ─────────────────────────────────────────────────────────
    "ha":    {"name": "Hausa",       "native_name": "Hausa",            "flag_emoji": _flag("NG")},
    "yo":    {"name": "Yoruba",      "native_name": "Yorùbá",           "flag_emoji": _flag("NG")},
    "ig":    {"name": "Igbo",        "native_name": "Igbo",             "flag_emoji": _flag("NG")},

    # ── Africa — South ────────────────────────────────────────────────────────
    "zu":    {"name": "Zulu",        "native_name": "isiZulu",          "flag_emoji": _flag("ZA")},
    "af":    {"name": "Afrikaans",   "native_name": "Afrikaans",        "flag_emoji": _flag("ZA")},
    "st":    {"name": "Sesotho",     "native_name": "Sesotho",          "flag_emoji": _flag("ZA")},
    "tn":    {"name": "Setswana",    "native_name": "Setswana",         "flag_emoji": _flag("ZA")},
    "ts":    {"name": "Tsonga",      "native_name": "Xitsonga",         "flag_emoji": _flag("ZA")},
    "ve":    {"name": "Venda",       "native_name": "Tshivenḓa",        "flag_emoji": _flag("ZA")},
    "xh":    {"name": "Xhosa",       "native_name": "isiXhosa",         "flag_emoji": _flag("ZA")},
    "nso":   {"name": "Northern Sotho", "native_name": "Sesotho sa Leboa", "flag_emoji": _flag("ZA")},
    "ss":    {"name": "Swati",       "native_name": "siSwati",          "flag_emoji": _flag("SZ")},

    # ── Afro-Asiatic / Other ──────────────────────────────────────────────────
    "ber":   {"name": "Berber (Tamazight)", "native_name": "ⵜⴰⵎⴰⵣⵉⵖⵜ", "flag_emoji": _flag("MA")},
}

# Ordered list for consistent iteration
LOCALE_CODES: list[str] = list(LOCALE_MAP.keys())

assert len(LOCALE_CODES) == 64, f"Expected 64 locales, got {len(LOCALE_CODES)}"


def get_locale_info(code: str) -> LocaleInfo:
    """Return metadata for a locale code, raising KeyError if unsupported."""
    return LOCALE_MAP[code]
