import math
import re

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import AutoMinorLocator

rcParams["font.family"] = "Arial"

COLOR_REALIZED = "#405A79"
COLOR_TARGET = "#2F6B58"
COLOR_RANGE_FILL = "#2F6B58"
COLOR_ABS_DIAMOND = "#6F6860"
GRID_GRAY = "#9AA0A6"


def dotted_line_with_endpoint(
    ax,
    x0,
    y0,
    x1,
    y1,
    color=COLOR_TARGET,
    lw=1.4,
    pattern=(0.5, 1.4),
    ms_end=3.0,
):
    segment, = ax.plot(
        [x0, x1],
        [y0, y1],
        linestyle=(0, pattern),
        linewidth=lw,
        color=color,
        zorder=3,
    )
    segment.set_dash_capstyle("round")
    ax.plot(
        [x1],
        [y1],
        marker="o",
        markersize=ms_end,
        markerfacecolor=color,
        markeredgecolor="white",
        markeredgewidth=0.7,
        zorder=4,
    )
    return segment


def fmt_pct(val: float) -> str:
    if math.isclose(val, round(val), abs_tol=1e-9):
        return f"{int(round(val))}"
    return f"{val:.1f}".rstrip("0").rstrip(".")


def apply_grid(ax):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(
        which="major",
        axis="both",
        linestyle="--",
        linewidth=0.6,
        color=GRID_GRAY,
        alpha=0.45,
    )
    ax.grid(
        which="minor",
        axis="both",
        linestyle=":",
        linewidth=0.5,
        color=GRID_GRAY,
        alpha=0.25,
    )


def parse_pct(text: str):
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    pct = float(match.group(1)) if match else None
    lower_bound = ("more than" in text.lower()) or ("at least" in text.lower())
    return pct, lower_bound


def _carbon_inputs():
    realized = {
        2005: 0.30456933,
        2010: 0.210125739,
        2012: 0.198284199,
        2014: 0.177973973,
        2017: 0.150344339,
        2018: 0.141290459,
        2019: 0.139877555,
        2020: 0.138147321,
        2021: 0.128410356,
        2022: 0.128410356,
        2023: 0.124044404,
    }
    pct_targets = [
        (2010, 2015, 17.0),
        (2015, 2020, 18.0),
        (2020, 2025, 18.0),
    ]
    range_targets = [
        (2005, 2020, 40.0, 45.0),
        (2005, 2030, 60.0, 65.0),
    ]
    return realized, pct_targets, range_targets


def _energy_inputs():
    p_1990, p_2005 = 26, 61
    rebasing_factor = p_1990 / p_2005

    abs_targets_1990 = {2010: 2.25, 2020: 1.54}
    abs_targets_2005 = {2015: 0.869}
    abs_targets_2005.update({year: value * rebasing_factor for year, value in abs_targets_1990.items()})

    realized = [
        (1990, 2.259788354),
        (1991, 2.173371973),
        (1992, 2.000539212),
        (1993, 1.866593822),
        (1994, 1.749931708),
        (1995, 1.685119423),
        (1996, 1.581419766),
        (1997, 1.451795195),
        (1998, 1.352416357),
        (1999, 1.296245710),
        (2000, 1.248716700),
        (2001, 1.220104398),
        (2002, 1.220104398),
        (2003, 1.288361987),
        (2004, 1.365151774),
        (2005, 1.390748370),
        (2006, 1.36),
        (2007, 1.29),
        (2008, 1.24),
        (2009, 1.16),
        (2010, 1.13),
        (2011, 1.112431568),
        (2012, 1.073625816),
        (2013, 1.021884813),
        (2014, 0.983079060),
        (2015, 0.931338057),
        (2016, 0.889021167),
        (2017, 0.859387129),
        (2018, 0.829753090),
        (2019, 0.814936070),
        (2020, 0.814936070),
        (2021, 0.792120979),
        (2022, 0.792120979),
    ]

    pct_targets = [
        {
            "Announcement_Year": 2007,
            "Targeted_Change": "20 percent",
            "Baseline_Year": 2005,
            "Target_Year": 2010,
        },
        {
            "Announcement_Year": 2011,
            "Targeted_Change": "16 percent",
            "Baseline_Year": 2010,
            "Target_Year": 2015,
        },
        {
            "Announcement_Year": 2016,
            "Targeted_Change": "15 percent",
            "Baseline_Year": 2015,
            "Target_Year": 2020,
        },
        {
            "Announcement_Year": 2021,
            "Targeted_Change": "13.5 percent",
            "Baseline_Year": 2020,
            "Target_Year": 2025,
        },
    ]

    return abs_targets_2005, realized, pct_targets


def make_carbon_intensity_plot():
    realized_kg, pct_targets, range_targets = _carbon_inputs()

    years = range(2005, 2031)
    series_real = pd.Series(realized_kg, dtype="float64").reindex(years)
    series_interp = series_real.interpolate("linear")
    series_plot = series_real.dropna()

    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    ax.plot(
        series_plot.index.to_numpy(dtype=float),
        series_plot.to_numpy(dtype=float),
        color=COLOR_REALIZED,
        marker="o",
        markersize=3.6,
        linewidth=1.9,
        alpha=0.9,
    )

    for baseline, target_year, pct in pct_targets:
        baseline_value = series_interp.loc[baseline]
        if pd.isna(baseline_value):
            continue
        endpoint = baseline_value * (1 - pct / 100.0)
        dotted_line_with_endpoint(ax, baseline, baseline_value, target_year, endpoint, ms_end=3.0)
        mid_x = (baseline + target_year) / 2
        mid_y = (baseline_value + endpoint) / 2
        label = f"-{fmt_pct(pct)}%"
        ax.annotate(
            label,
            (mid_x, mid_y),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color=COLOR_TARGET,
            path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
        )

    for baseline, target_year, low, high in range_targets:
        baseline_value = series_interp.loc[baseline]
        if pd.isna(baseline_value):
            continue
        endpoint_low = baseline_value * (1 - high / 100.0)
        endpoint_high = baseline_value * (1 - low / 100.0)
        dotted_line_with_endpoint(ax, baseline, baseline_value, target_year, endpoint_low, ms_end=2.8)
        dotted_line_with_endpoint(ax, baseline, baseline_value, target_year, endpoint_high, ms_end=2.8)
        x_vals = np.array([baseline, target_year])
        lower = np.array([baseline_value, min(endpoint_low, endpoint_high)])
        upper = np.array([baseline_value, max(endpoint_low, endpoint_high)])
        ax.fill_between(x_vals, lower, upper, color=COLOR_RANGE_FILL, alpha=0.3, zorder=2)
        mid_x = (baseline + target_year) / 2
        mid_y = ((baseline_value + min(endpoint_low, endpoint_high)) / 2 + (baseline_value + max(endpoint_low, endpoint_high)) / 2) / 2
        label = f"-{fmt_pct(low)}–{fmt_pct(high)}%"
        ax.annotate(
            label,
            (mid_x, mid_y),
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=COLOR_TARGET,
            path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
        )

    y_values = list(series_plot.values)
    for baseline, _, pct in pct_targets:
        baseline_value = series_interp.loc[baseline]
        y_values.append(baseline_value * (1 - pct / 100.0))
    for baseline, _, low, high in range_targets:
        baseline_value = series_interp.loc[baseline]
        y_values += [baseline_value * (1 - low / 100.0), baseline_value * (1 - high / 100.0)]

    ax.set_xlim(2005, 2031)
    ax.set_xticks([2005, 2010, 2015, 2020, 2025, 2030])
    ax.set_ylim(min(y_values) * 0.9, max(y_values) * 1.03)
    ax.set_ylabel("Carbon intensity (kg CO$_2$ per 10,000 yuan, 2005 prices)")
    ax.set_title("Target and realized carbon intensity", loc="left", fontweight="bold")
    apply_grid(ax)

    legend_items = [
        Line2D([0], [0], color=COLOR_REALIZED, lw=1.9, marker="o", markersize=3.8, label="Realized"),
        Line2D([0], [0], color=COLOR_TARGET, lw=1.4, linestyle=(0, (0.5, 1.4)), label="5YP target"),
        Patch(facecolor=COLOR_RANGE_FILL, edgecolor="none", alpha=0.3, label="Long-term range target"),
    ]
    ax.legend(handles=legend_items, frameon=False, loc="upper right")

    return fig


def make_energy_intensity_plot():
    abs_targets_2005, realized_e, pct_rows_e = _energy_inputs()

    series_real = (
        pd.DataFrame(realized_e, columns=["Year", "Realized_2005"])
        .set_index("Year")["Realized_2005"]
        .reindex(range(2005, 2031))
    )
    series_plot = series_real.dropna()

    df_pct = pd.DataFrame(pct_rows_e)
    df_pct[["pct", "lower_bound"]] = df_pct["Targeted_Change"].apply(lambda value: pd.Series(parse_pct(value)))
    real_map = dict(realized_e)
    df_pct["Baseline_Value_2005"] = df_pct["Baseline_Year"].map(real_map)
    df_pct["Implied_Target_Value_2005"] = df_pct["Baseline_Value_2005"] * (1 - df_pct["pct"] / 100.0)
    df_pct = df_pct.drop_duplicates(subset=["Baseline_Year", "Target_Year", "pct"]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    ax.plot(
        series_plot.index.to_numpy(dtype=float),
        series_plot.to_numpy(dtype=float),
        color=COLOR_REALIZED,
        marker="o",
        markersize=3.6,
        linewidth=1.9,
        alpha=0.9,
    )

    for _, row in df_pct.iterrows():
        x0 = int(row["Baseline_Year"])
        y0 = float(row["Baseline_Value_2005"])
        x1 = int(row["Target_Year"])
        y1 = float(row["Implied_Target_Value_2005"])
        dotted_line_with_endpoint(ax, x0, y0, x1, y1, ms_end=2.8)
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        label = f"-{fmt_pct(float(row['pct']))}%"
        if row["lower_bound"]:
            label = "≥" + label
        ax.annotate(
            label,
            (mid_x, mid_y),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color=COLOR_TARGET,
            path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
        )

    abs_years = sorted(abs_targets_2005)
    abs_values = [abs_targets_2005[year] for year in abs_years]
    ax.plot(
        abs_years,
        abs_values,
        linestyle="None",
        marker="D",
        markersize=5.0,
        markeredgewidth=0.8,
        markeredgecolor="white",
        color=COLOR_ABS_DIAMOND,
        zorder=5,
    )
    for year, value in zip(abs_years, abs_values):
        ax.annotate(
            f"{value:.2f}",
            xy=(year, value),
            xytext=(0, -8),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=9,
            fontweight="bold",
            color=COLOR_ABS_DIAMOND,
        )

    y_values = list(series_plot.values) + abs_values + df_pct["Implied_Target_Value_2005"].tolist()

    ax.set_xlim(2005, 2031)
    ax.set_xticks([2005, 2010, 2015, 2020, 2025, 2030])
    ax.set_ylim(min(y_values) * 0.9, max(y_values) * 1.03)
    ax.set_ylabel("Energy intensity (tce per 10,000 yuan, 2005 prices)")
    ax.set_title("Target and realized energy intensity", loc="left", fontweight="bold")
    apply_grid(ax)

    legend_items = [
        Line2D([0], [0], color=COLOR_REALIZED, lw=1.9, marker="o", markersize=3.8, label="Realized"),
        Line2D([0], [0], color=COLOR_ABS_DIAMOND, marker="D", linestyle="None", markersize=5.0, label="Absolute targets"),
        Line2D([0], [0], color=COLOR_TARGET, lw=1.4, linestyle=(0, (0.5, 1.4)), label="Percentage targets"),
    ]
    ax.legend(handles=legend_items, frameon=False, loc="upper right")

    return fig


if __name__ == "__main__":
    make_carbon_intensity_plot()
    make_energy_intensity_plot()
    plt.show()
