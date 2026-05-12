"""Main public interface for the Menu Analyzer SDK."""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv

from .exceptions import AnalysisError
from .image_loader import load_image
from .locale_map import LOCALE_MAP, LOCALE_CODES
from .models import MenuAnalysisResult
from .ocr_processor import process_menu

load_dotenv()


class MenuAnalyzer:
    """AI-powered menu analyzer that performs OCR and dish analysis in 64 languages.

    A single API call to GPT-4 Vision returns structured data for every dish on the
    menu, translated simultaneously into all 64 supported locales.

    Args:
        api_key: OpenAI API key. If omitted, reads from the OPENAI_API_KEY env var.
        model: OpenAI model to use. Defaults to "gpt-4o" (supports vision + JSON mode).

    Example::

        analyzer = MenuAnalyzer(api_key="sk-...")
        result = analyzer.analyze_sync("https://example.com/menu.jpg")
        print(result.dishes[0].en.dish_name)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o",
    ) -> None:
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise AnalysisError(
                "OpenAI API key is required. "
                "Pass api_key= or set the OPENAI_API_KEY environment variable."
            )
        self._model = model

    async def analyze(self, image: str | bytes) -> MenuAnalysisResult:
        """Analyze a menu image and return structured dish data in 64 languages.

        Args:
            image: A menu image as one of:
                - HTTPS/HTTP URL string
                - ``data:image/...;base64,...`` URI string
                - Local file path string
                - Raw base64 string
                - Raw bytes

        Returns:
            MenuAnalysisResult with all dishes translated into all 64 locales.

        Raises:
            ImageLoadError: if the image cannot be loaded or exceeds 20 MB.
            AnalysisError: if GPT-4 Vision analysis fails.
        """
        mime_type, b64_data = load_image(image)
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: process_menu(b64_data, mime_type, self._model, self._api_key),
        )

    def analyze_sync(self, image: str | bytes) -> MenuAnalysisResult:
        """Synchronous wrapper around :meth:`analyze`.

        Prefer this method in scripts and notebooks. Use :meth:`analyze` directly
        when you are already inside an async event loop.

        Args:
            image: Same as :meth:`analyze`.

        Returns:
            MenuAnalysisResult with all dishes translated into all 64 locales.
        """
        mime_type, b64_data = load_image(image)
        return process_menu(b64_data, mime_type, self._model, self._api_key)

    def supported_locales(self) -> list[dict[str, Any]]:
        """Return metadata for all 64 supported locale codes.

        Returns:
            List of dicts, each with keys: ``code``, ``name``, ``native_name``,
            ``flag_emoji``.

        Example::

            for locale in analyzer.supported_locales():
                print(locale["flag_emoji"], locale["code"], locale["name"])
        """
        return [
            {"code": code, **LOCALE_MAP[code]}
            for code in LOCALE_CODES
        ]
