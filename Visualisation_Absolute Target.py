import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch
from matplotlib.ticker import AutoMinorLocator

rcParams["font.family"] = "Arial"

COLOR_TARGET = "#2F6B58"
COLOR_RANGE_FILL = "#2F6B58"
GRID_GRAY = "#9AA0A6"


def _apply_grid(ax):
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


def make_absolute_target_plot():
    peak_year = 2030
    target_year = 2035

    peak_level = 100
    target_upper = 93  # −7%
    target_lower = 90  # −10%

    x = np.array([peak_year, target_year])
    y_upper = np.array([peak_level, target_upper])
    y_lower = np.array([peak_level, target_lower])

    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)

    # Target corridor (shaded band)
    ax.fill_between(
        x,
        y_lower,
        y_upper,
        color=COLOR_RANGE_FILL,
        alpha=0.3,
        label="2035 target range",
        zorder=2,
    )

    # Boundary lines (dotted, with round endpoint dots)
    for y_vals in [y_upper, y_lower]:
        (line,) = ax.plot(
            x,
            y_vals,
            linestyle=(0, (0.5, 1.4)),
            linewidth=1.4,
            color=COLOR_TARGET,
            zorder=3,
        )
        line.set_dash_capstyle("round")
        ax.plot(
            [target_year],
            [y_vals[-1]],
            marker="o",
            markersize=3.6,
            markerfacecolor=COLOR_TARGET,
            markeredgecolor="white",
            markeredgewidth=0.7,
            zorder=4,
        )

    # Peak point
    ax.scatter([peak_year], [peak_level], color=COLOR_TARGET, s=40, zorder=5)
    ax.annotate(
        "Peak level",
        (peak_year, peak_level),
        xytext=(0, 9),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color=COLOR_TARGET,
        path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
    )

    # Vertical reference line at 2035
    (vline,) = ax.plot(
        [target_year, target_year],
        [target_lower, target_upper],
        linestyle=(0, (0.5, 1.4)),
        linewidth=1.3,
        color=COLOR_TARGET,
        zorder=3,
    )
    vline.set_dash_capstyle("round")

    # Percentage labels (right side, bold)
    ax.annotate(
        "−7%",
        (target_year, target_upper),
        xytext=(8, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=COLOR_TARGET,
        path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
    )
    ax.annotate(
        "−10%",
        (target_year, target_lower),
        xytext=(8, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=COLOR_TARGET,
        path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)],
    )

    # Axes formatting
    ax.set_xlim(2028.5, 2037.0)
    ax.set_ylim(88, 103)

    ax.set_xticks([peak_year, target_year])
    ax.set_xticklabels(["Peak year", "2035"])

    ax.set_yticks([])
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions level (economy-wide all-GHGs net emissions)")

    ax.set_title(
        "China's first absolute carbon emissions reduction target",
        loc="left",
        fontweight="bold",
    )

    _apply_grid(ax)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    legend_items = [
        Patch(
            facecolor=COLOR_RANGE_FILL,
            edgecolor="none",
            alpha=0.3,
            label="2035 target range",
        ),
    ]
    ax.legend(handles=legend_items, frameon=False, loc="upper right")

    return fig


if __name__ == "__main__":
    make_absolute_target_plot()
    plt.show()
