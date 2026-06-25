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


_BUNDLED_FONT_REGISTERED = False


def get_font_family() -> str:
    """Return a matplotlib font family suitable for the current language."""
    if _lang_ctx.get() == "CN":
        try:
            import matplotlib.font_manager as fm

            # Ensure the bundled CJK font is registered with matplotlib.
            # This guarantees Chinese text renders on all platforms even when
            # system CJK fonts are not installed or not detected (e.g. stale
            # font cache on Windows).
            global _BUNDLED_FONT_REGISTERED
            if not _BUNDLED_FONT_REGISTERED:
                bundled = (
                    Path(__file__).parent
                    / "fonts"
                    / "NotoSansCJKsc-Regular.ttf"
                )
                if bundled.exists():
                    fm.fontManager.addfont(str(bundled))
                _BUNDLED_FONT_REGISTERED = True

            # Priority 1: system fonts that match the CSS/website font stack.
            # These keep the app visually consistent with the embedding website
            # (https://mgflab.nsd.pku.edu.cn/MGFsjk/zczz/index.htm).
            css_stack_candidates = [
                "Microsoft YaHei",
                "PingFang SC",
                "STHeiti",
                "SimHei",
            ]
            available = {f.name for f in fm.fontManager.ttflist}
            for candidate in css_stack_candidates:
                if candidate in available:
                    return candidate

            # Priority 2: bundled font (always available after registration).
            if "Noto Sans CJK SC" in available:
                return "Noto Sans CJK SC"

            # Priority 3: other system CJK fonts.
            other_candidates = [
                "HarmonyOS Sans SC",
                "Noto Sans CJK JP",
                "AR PL UMing CN",
            ]
            for candidate in other_candidates:
                if candidate in available:
                    return candidate
        except Exception:
            pass
        return "sans-serif"
    return "Arial"
