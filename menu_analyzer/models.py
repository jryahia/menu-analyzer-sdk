"""Pydantic v2 models for Menu Analyzer structured output."""

from pydantic import BaseModel, Field, ConfigDict


class DishNutrition(BaseModel):
    """Estimated nutritional values per serving."""

    calories: int | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None


class DishAnalysis(BaseModel):
    """Complete analysis of a single dish in one language/locale."""

    dish_name: str
    ingredients: list[str]
    dietary_flags: list[str]
    """Subset of: vegan, vegetarian, gluten_free, keto, halal, kosher"""
    allergen_warnings: list[str]
    """Subset of: lactose, nuts, shellfish, eggs, soy, gluten"""
    nutrition: DishNutrition | None = None
    spice_level: int = Field(default=0, ge=0, le=5)
    """0 = not spicy, 5 = extremely spicy"""
    estimated_prep_minutes: int | None = None
    wine_pairing: list[str] = Field(default_factory=list)


class MultiLangOutput(BaseModel):
    """Full dish analysis keyed by all 64 supported locale codes."""

    model_config = ConfigDict(populate_by_name=True)

    # European — Western
    en: DishAnalysis
    it: DishAnalysis
    fr: DishAnalysis
    es: DishAnalysis
    de: DishAnalysis
    pt: DishAnalysis
    nl: DishAnalysis
    sv: DishAnalysis
    no: DishAnalysis
    da: DishAnalysis
    fi: DishAnalysis
    pl: DishAnalysis
    cs: DishAnalysis
    ro: DishAnalysis
    hu: DishAnalysis
    el: DishAnalysis

    # European — Eastern / Other scripts
    ru: DishAnalysis
    he: DishAnalysis

    # Middle East / Central Asia
    ar: DishAnalysis
    tr: DishAnalysis
    fa: DishAnalysis
    ku: DishAnalysis
    ps: DishAnalysis
    tg: DishAnalysis

    # East Asia
    zh_CN: DishAnalysis = Field(alias="zh-CN")
    zh_TW: DishAnalysis = Field(alias="zh-TW")
    ja: DishAnalysis
    ko: DishAnalysis

    # South Asia
    hi: DishAnalysis
    ur: DishAnalysis
    bn: DishAnalysis
    ta: DishAnalysis
    te: DishAnalysis
    mr: DishAnalysis
    gu: DishAnalysis
    kn: DishAnalysis
    ml: DishAnalysis
    pa: DishAnalysis
    ne: DishAnalysis
    si: DishAnalysis

    # Southeast Asia
    th: DishAnalysis
    vi: DishAnalysis
    id: DishAnalysis
    ms: DishAnalysis
    tl: DishAnalysis
    my: DishAnalysis
    km: DishAnalysis
    lo: DishAnalysis

    # Africa — East / Horn
    sw: DishAnalysis
    am: DishAnalysis
    om: DishAnalysis

    # Africa — West
    ha: DishAnalysis
    yo: DishAnalysis
    ig: DishAnalysis

    # Africa — South
    zu: DishAnalysis
    af: DishAnalysis
    st: DishAnalysis
    tn: DishAnalysis
    ts: DishAnalysis
    ve: DishAnalysis
    xh: DishAnalysis
    nso: DishAnalysis
    ss: DishAnalysis

    # Afro-Asiatic / Other
    ber: DishAnalysis


class MenuAnalysisResult(BaseModel):
    """Top-level result returned by MenuAnalyzer.analyze()."""

    dishes: list[MultiLangOutput]
    raw_text: str | None = None
    """Raw OCR text extracted from the menu image."""
    total_dishes_detected: int
    processing_time_ms: int
