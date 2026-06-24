import os
import json
from pathlib import Path
from typing import Dict

LANG: str = os.getenv("LANGUAGE", "EN").upper()
if LANG not in ("CN", "EN"):
    LANG = "EN"

_translation: Dict[str, str] = {}

if LANG == "CN":
    _path = Path(__file__).parent / "translation.json"
    if _path.exists():
        try:
            with open(_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict):
                    _translation = {str(k): str(v) for k, v in raw.items()}
        except Exception:
            _translation = {}


def i18n(key: str, *args, **kwargs) -> str:
    """Return localized string.  Supports str.format() placeholders.

    When LANG=EN the key is returned as-is (English is the default / source
    language).  When LANG=CN the Chinese translation is looked up from
    translation.json; falls back to the English key if not found.
    """
    if LANG == "CN":
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
    if LANG == "CN":
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
