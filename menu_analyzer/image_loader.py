"""Image loading utilities — handles URLs, base64 strings, file paths, and raw bytes."""

import base64
import re
from pathlib import Path

import httpx

from .exceptions import ImageLoadError

_MAX_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB

_MIME_BY_EXTENSION: dict[str, str] = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

_MIME_BY_MAGIC: dict[bytes, str] = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG":       "image/png",
    b"GIF8":          "image/gif",
    b"RIFF":          "image/webp",  # RIFF....WEBP
}


def _detect_mime(data: bytes) -> str:
    for magic, mime in _MIME_BY_MAGIC.items():
        if data.startswith(magic):
            return mime
    return "image/jpeg"


def load_image(image_source: str | bytes) -> tuple[str, str]:
    """Load an image from a URL, data-URI, base64 string, file path, or raw bytes.

    Returns:
        (mime_type, base64_encoded_data) — ready to embed in an OpenAI vision message.

    Raises:
        ImageLoadError: if the source cannot be resolved or exceeds 20 MB.
    """
    if isinstance(image_source, bytes):
        return _from_bytes(image_source)

    source = image_source.strip()

    # data:image/... URI
    if source.startswith("data:"):
        return _from_data_uri(source)

    # HTTP/HTTPS URL
    if source.startswith("http://") or source.startswith("https://"):
        return _from_url(source)

    # Local file path
    path = Path(source)
    if path.exists() and path.is_file():
        return _from_file(path)

    # Fallback: treat as raw base64
    return _from_raw_base64(source)


def _from_bytes(data: bytes) -> tuple[str, str]:
    _validate_size(len(data))
    mime = _detect_mime(data)
    return mime, base64.b64encode(data).decode()


def _from_data_uri(uri: str) -> tuple[str, str]:
    match = re.match(r"data:([^;]+);base64,(.+)", uri, re.DOTALL)
    if not match:
        raise ImageLoadError("Malformed data URI — expected data:<mime>;base64,<data>")
    mime, b64 = match.group(1), match.group(2)
    raw = _safe_b64decode(b64)
    _validate_size(len(raw))
    return mime, b64.strip()


def _from_url(url: str) -> tuple[str, str]:
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ImageLoadError(f"HTTP {exc.response.status_code} fetching image: {url}") from exc
    except httpx.RequestError as exc:
        raise ImageLoadError(f"Network error fetching image: {exc}") from exc

    data = response.content
    _validate_size(len(data))

    content_type = response.headers.get("content-type", "")
    mime = content_type.split(";")[0].strip() or _detect_mime(data)
    return mime, base64.b64encode(data).decode()


def _from_file(path: Path) -> tuple[str, str]:
    size = path.stat().st_size
    _validate_size(size)
    mime = _MIME_BY_EXTENSION.get(path.suffix.lower(), "image/jpeg")
    data = path.read_bytes()
    return mime, base64.b64encode(data).decode()


def _from_raw_base64(source: str) -> tuple[str, str]:
    raw = _safe_b64decode(source)
    _validate_size(len(raw))
    mime = _detect_mime(raw)
    return mime, source.strip()


def _safe_b64decode(data: str) -> bytes:
    try:
        return base64.b64decode(data, validate=False)
    except Exception as exc:
        raise ImageLoadError("Failed to decode base64 image data") from exc


def _validate_size(size_bytes: int) -> None:
    if size_bytes > _MAX_SIZE_BYTES:
        mb = size_bytes / (1024 * 1024)
        raise ImageLoadError(f"Image too large: {mb:.1f} MB (max 20 MB)")
