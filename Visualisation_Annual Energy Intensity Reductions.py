import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from i18n import get_font_family, i18n


data = pd.DataFrame(
    {
        "year": list(range(2010, 2027)),
        "target": [
            -5.2, -3.5, -3.5, np.nan, -3.9, -3.1, -3.4, -3.4, -3.0,
            -3.0, np.nan, -3.0, np.nan, np.nan, -2.5, -3.0, np.nan,
        ],
        "realised": [
            np.nan, np.nan, np.nan, -3.7, -4.8, -5.6, -5.0, -3.7, -3.1,
            -2.6, -0.1, np.nan, np.nan, np.nan, -3.0, -5.1, np.nan,
        ],
    }
)

PLOT_DATA = data.assign(target=data["target"].abs(), realised=data["realised"].abs())
PLOT_DATA = PLOT_DATA[PLOT_DATA["year"].between(2010, 2025)].copy()

REALISED_COLOR = "#4C6F6A"
BAR_EDGE_COLOR = "#3E5A56"
TARGET_EDGE_COLOR = "#2F2F2F"
GRID_COLOR = "#C7C7C7"


def make_energy_intensity_plot():
    # Configure fonts before axes are created so ticks use the same family.
    plt.rcParams.update(
        {
            "font.family": get_font_family(),
            "font.size": 10,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "axes.edgecolor": "#555555",
            "axes.linewidth": 0.8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

    ax.bar(
        PLOT_DATA["year"], PLOT_DATA["realised"], width=0.52,
        color=REALISED_COLOR, edgecolor=BAR_EDGE_COLOR, linewidth=0.8, zorder=2,
    )
    ax.scatter(
        PLOT_DATA["year"], PLOT_DATA["target"], marker="o", s=64,
        facecolors="white", edgecolors=TARGET_EDGE_COLOR, linewidths=1.4, zorder=4,
    )

    ax.set_title(i18n("Energy intensity reduction"), loc="left", fontweight="bold", fontsize=12)
    ax.set_ylabel(i18n("Annual reduction (%)"), labelpad=8)
    ax.set_xlabel(i18n("Year"), labelpad=6)
    ax.set_ylim(0, 7.2)
    ax.set_yticks(np.arange(0, 7.1, 1))
    ax.set_xticks(PLOT_DATA["year"])
    ax.set_xticklabels(PLOT_DATA["year"], rotation=45, ha="right")
    ax.set_xlim(PLOT_DATA["year"].min() - 0.6, PLOT_DATA["year"].max() + 0.6)
    ax.grid(axis="y", linestyle="--", linewidth=0.65, color=GRID_COLOR, alpha=0.65, zorder=0)
    ax.axhline(0, color="#555555", linewidth=0.8, zorder=3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", length=4, width=0.8, color="#555555")

    ax.legend(
        handles=[
            Line2D([], [], marker="s", linestyle="none", label=i18n("Realised reduction"), markerfacecolor=REALISED_COLOR, markeredgecolor=BAR_EDGE_COLOR, markeredgewidth=0.8, markersize=8),
            Line2D([], [], marker="o", linestyle="none", label=i18n("Target reduction"), markerfacecolor="white", markeredgecolor=TARGET_EDGE_COLOR, markeredgewidth=1.4, markersize=7),
        ],
        frameon=False,
        ncol=2,
        loc="upper left",
        handletextpad=0.5,
        columnspacing=1.3,
    )
    return fig


if __name__ == "__main__":
    make_energy_intensity_plot()
    plt.show()
