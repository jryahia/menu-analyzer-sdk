"""Custom exceptions for the Menu Analyzer SDK."""


class MenuAnalyzerError(Exception):
    """Base exception for all Menu Analyzer errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | details={self.details}"
        return self.message


class ImageLoadError(MenuAnalyzerError):
    """Raised when an image cannot be loaded, decoded, or validated."""


class AnalysisError(MenuAnalyzerError):
    """Raised when GPT-4 Vision analysis fails or produces unparseable output."""
