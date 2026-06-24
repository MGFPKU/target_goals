import contextvars
import os
import json
from pathlib import Path
from typing import Dict

_lang_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "lang", default=os.getenv("LANGUAGE", "EN").upper()
)

# Validate the default value
_default = _lang_ctx.get()
if _default not in ("CN", "EN"):
    _default = "EN"
    _lang_ctx.set(_default)

_translation: Dict[str, str] = {}

# Always load the translation dictionary at import time — the file is small
# and we need it available for sessions that request CN even when the
# process-level default is EN.
_path = Path(__file__).parent / "translation.json"
if _path.exists():
    try:
        with open(_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            if isinstance(raw, dict):
                _translation = {str(k): str(v) for k, v in raw.items()}
    except Exception:
        _translation = {}


def set_language(lang: str) -> None:
    """Set the current language for this session / context.

    Only ``"CN"`` and ``"EN"`` are recognised; anything else falls back to
    ``"EN"``.  Call this once at the start of every Shiny render.
    """
    lang = lang.upper()
    if lang not in ("CN", "EN"):
        lang = "EN"
    _lang_ctx.set(lang)


def i18n(key: str, *args, **kwargs) -> str:
    """Return localized string.  Supports str.format() placeholders.

    When the current language is EN the key is returned as-is (English is the
    default / source language).  When it is CN the Chinese translation is
    looked up from translation.json; falls back to the English key if not
    found.
    """
    if _lang_ctx.get() == "CN":
        result = _translation.get(key, key)
    else:
        result = key

    if not args and not kwargs:
        return result

    try:
        return result.format(*args, **kwargs)
    except Exception:
        return result


def get_font_family() -> str:
    """Return a matplotlib font family suitable for the current language."""
    if _lang_ctx.get() == "CN":
        try:
            import matplotlib.font_manager as fm

            candidates = [
                "HarmonyOS Sans SC",
                "Noto Sans CJK SC",
                "Noto Sans CJK JP",
                "Microsoft YaHei",
                "AR PL UMing CN",
                "SimHei",
            ]
            available = {f.name for f in fm.fontManager.ttflist}
            for candidate in candidates:
                if candidate in available:
                    return candidate
        except Exception:
            pass
        return "sans-serif"
    return "Arial"
