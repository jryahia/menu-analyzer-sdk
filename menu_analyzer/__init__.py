"""Menu Analyzer SDK — restaurant menu OCR + multi-language analysis via GPT-4 Vision."""

from .client import MenuAnalyzer
from .exceptions import AnalysisError, ImageLoadError, MenuAnalyzerError
from .models import DishAnalysis, DishNutrition, MenuAnalysisResult, MultiLangOutput

__version__ = "0.1.0"
__all__ = [
    "MenuAnalyzer",
    "MenuAnalysisResult",
    "MultiLangOutput",
    "DishAnalysis",
    "DishNutrition",
    "MenuAnalyzerError",
    "ImageLoadError",
    "AnalysisError",
]
