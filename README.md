# Target Goals — China's Climate & Energy Policy Targets

A [Shiny for Python](https://shiny.posit.co/py/) web app that visualises China's climate and energy policy targets against realised values. Six interactive matplotlib plots track carbon intensity, energy intensity, absolute emissions, energy mix, installed capacity, and forest stock volume.

## Dependencies

Python ≥ 3.12, plus:

```bash
pip install -r requirements.txt
# matplotlib>=3.10.8, pandas>=3.0.1, shiny>=1.5.1
```

## Running

```bash
shiny run app.py --port 8000
```

Open http://localhost:8000?lang=CN for the Chinese version (default is English).

The `LANGUAGE` env var sets the default locale:

```bash
LANGUAGE=CN shiny run app.py
```

## Language support

English / 中文 bilingual. The URL query parameter `?lang=CN` switches to Chinese; `?lang=EN` switches back. All user-facing text is stored in `translation.json` (65 key-value pairs). Strings carrying `{}` placeholders are resolved at runtime via `str.format()`.

## Plot modules

Each tab corresponds to a self-contained `Visualisation_*.py` script. All data is hardcoded in the source files — there are no external CSV or JSON data files. Every script exports a parameterless `make_*_plot()` function that returns a `matplotlib.figure.Figure`:

| Tab                      | Script                                                  |
| ------------------------ | ------------------------------------------------------- |
| Carbon intensity         | `Visualisation_Carbon and Energy Intensity.py`          |
| Energy intensity         | `Visualisation_Carbon and Energy Intensity.py`          |
| Absolute emissions       | `Visualisation_Absolute Target.py`                      |
| Energy mix shares        | `Visualisation_Energy Shares3.py`                       |
| Installed capacity       | `Visualisation_Installed Capacity2.py`                  |
| Forest stock volume      | `Visualisation_Forest coverage rate and stock volume.py`|

## CJK font handling

Chinese text inside plots requires a CJK font. A bundled Noto Sans CJK SC font (`fonts/NotoSansCJKsc-Regular.ttf`, SIL OFL 1.1) is registered with matplotlib at first use. The app prefers system fonts that match the embedding website's CSS stack (`Microsoft YaHei` → `PingFang SC` → `STHeiti` → `SimHei`) before falling back to the bundled font.

## Project structure

```
target_goals/
├── app.py                  # Shiny UI + server, dynamic plot loading
├── i18n.py                 # Language context, translation lookup, font selection
├── translation.json        # EN → CN translations
├── fonts/
│   ├── NotoSansCJKsc-Regular.ttf   # Bundled CJK font (16 MB)
│   └── OFL.txt                     # Font licence
├── Visualisation_*.py      # Five plot modules (see table above)
├── requirements.txt
├── pyproject.toml
└── .env                    # LANGUAGE setting (gitignored)
```
