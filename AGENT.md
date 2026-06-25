# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app (development)
shiny run app.py --port 8000

# Visit with Chinese language
# http://localhost:8000?lang=CN

# Run an individual plot module standalone (no server)
python -m "Visualisation_Energy Shares3"

# Test font rendering
python -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from i18n import get_font_family, set_language
set_language('CN')
plt.rcParams['font.family'] = get_font_family()
# ...create test plot...
"
```

## Architecture

Shiny for Python app with six matplotlib-rendered plots comparing China's climate/energy targets against realized data. English/Chinese bilingual via URL query param (`?lang=CN`) or `LANGUAGE` env var.

### Font rendering

- **UI text (CSS)**: `font-family` on `body` in `app.py`'s inline `<style>` — matches the embedding website's stack (`Microsoft YaHei` → `PingFang SC` → `STHeiti` → `SimHei` → `Noto Sans CJK SC` → system fallbacks)
- **Plot text (matplotlib)**: `get_font_family()` in `i18n.py` — same priority: CSS-stack system fonts → bundled font (`fonts/NotoSansCJKsc-Regular.ttf`) → other CJK → `sans-serif`
- Bundled font registered once via `fontManager.addfont()`; 16 MB, SIL OFL licensed

### Language flow

1. `app.py`'s `lang()` reactive reads `?lang=` query param, falls back to `LANGUAGE` env var (default `"EN"`)
2. `set_language(lang)` sets a `contextvars.ContextVar` (per-session isolation for Shiny concurrency)
3. Every `@render.plot` and `@render.ui` calls `set_language()` at top
4. All user-facing strings go through `i18n(key)` — looks up `translation.json` for CN, returns key verbatim for EN

### Plot loading

`app.py` dynamically imports five `Visualisation_*.py` modules via `importlib.util._load_plot_builder()`. Each exports a parameterless function returning `matplotlib.figure.Figure`. All data is hardcoded in the source files (no CSV/JSON data files).

Default selected tab: `i18n("Energy intensity")`.

### Key patterns across all plot modules

- Colors defined as module-level constants (`COLOR_TARGET = '#2F6B58'`, `COLOR_REALIZED = '#405A79'`)
- Grid: major (`--`) + minor (`:`) via `AutoMinorLocator(2)`, except Energy Shares (Y-only, dashed, alpha 0.35)
- Text annotations use `path_effects=[pe.withStroke(linewidth=2, foreground="white")]` for readability
- Figure sizes vary per plot (e.g., `(9.2, 5.2)` for intensity, `(14, 8)` for energy shares)
- Each file has `if __name__ == "__main__":` block for standalone testing with `plt.show()`

## Gotchas

- **`Visualisation_Forest coverage rate and stock volume.py` sets global `plt.rcParams` at module level** — this can affect plots rendered after it. It doesn't set `font.family` though, so that's inherited from `app.py`'s per-render setting.
- **Redundant module name**: `carbon_energy_viz` is used as the import name for both carbon intensity and energy intensity plots. Safe because `importlib` caches loaded modules.
- **Dead code**: `Visualisation_Forest coverage rate and stock volume.py` exports three functions but `app.py` only imports `make_forest_stock_plot`.
- **Installed capacity alignment**: targets split coal/gas separately; realized data combines them as "火电" (thermal).
- **Energy Shares** is the only plot using `fig.tight_layout()`; others use `constrained_layout=True` in `subplots()`. It's also the only plot using `FontProperties` directly for the legend.
- **Translation keys** may contain literal `\n` newlines and LaTeX math (`CO$_2$`). Keys with `{}` placeholders are resolved via `str.format()`.
