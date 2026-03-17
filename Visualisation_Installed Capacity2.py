import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

mpl.rcParams["font.family"] = "Times New Roman"

TARGET_DATA = {
    2015: {
        "coal": 960,
        "gas": 56,
        "hydro": 290,
        "wind": 100,
        "solar": 35,
        "nuclear": 40,
        "pumped storage": 30,
    },
    2020: {
        "coal": 1100,
        "gas": 110,
        "hydro": 350,
        "wind": 210,
        "solar": 110,
        "nuclear": 58,
        "pumped storage": 40,
    },
    2030: {
        "wind+solar": 1200,
        "new energy storage": 120,
    },
    2035: {
        "wind+solar": 3600,
    },
}

ACHIEVED_DATA = {
    2015: {
        "thermal": 990,
        "hydro": 319,
        "wind": 129,
        "solar": 43,
        "nuclear": 26,
        "pumped storage": 23,
    },
    2020: {
        "thermal": 1245,
        "hydro": 370,
        "wind": 281,
        "solar": 253,
        "nuclear": 50,
        "pumped storage": 31,
    },
}

TARGET_ORDER = [
    "coal",
    "gas",
    "nuclear",
    "hydro",
    "wind",
    "solar",
    "wind+solar",
    "pumped storage",
    "new energy storage",
]

ACHIEVED_ORDER = ["thermal", "nuclear", "hydro", "wind", "solar", "pumped storage"]

COLOR_MAP = {
    "coal": "#2F2F2F",
    "gas": "#D9D9D9",
    "thermal": "#7A7A7A",
    "nuclear": "#6A3D9A",
    "hydro": "#1F78B4",
    "wind": "#33A02C",
    "solar": "#FFD92F",
    "wind+solar": "#9EE979",
    "pumped storage": "#A6CEE3",
    "new energy storage": "#66C2A5",
}

TARGET_POS = {2015: 0, 2020: 2, 2030: 4.2, 2035: 5.8}
ACHIEVED_POS = {2015: 0.7, 2020: 2.7}


OVERLAP_TECH = ["nuclear", "hydro", "wind", "solar", "pumped storage"]


def _draw_diff_panel(axis, year):
    differences = [ACHIEVED_DATA[year][tech] - TARGET_DATA[year][tech] for tech in OVERLAP_TECH]
    bar_colors = [COLOR_MAP[tech] for tech in OVERLAP_TECH]

    axis.bar(OVERLAP_TECH, differences, color=bar_colors, edgecolor="black", linewidth=0.8)
    axis.axhline(0, color="black", linewidth=0.8)
    axis.set_title(f"Target achievement gap ({year})", fontsize=11)
    axis.set_ylabel("GW")
    axis.grid(axis="y", linestyle="--", alpha=0.3)
    axis.set_xticks(range(len(OVERLAP_TECH)))
    axis.set_xticklabels(["Nuclear", "Hydro", "Wind", "Solar", "Pumped\nstorage"], fontsize=9)


def make_installed_capacity_plot():
    fig = plt.figure(figsize=(12, 10))
    grid = GridSpec(2, 2, width_ratios=[2.6, 1.2], height_ratios=[1, 1], wspace=0.30, hspace=0.32)

    ax_main = fig.add_subplot(grid[:, 0])
    ax_diff_2015 = fig.add_subplot(grid[0, 1])
    ax_diff_2020 = fig.add_subplot(grid[1, 1])

    width = 0.58
    target_edge = "#666666"
    achieved_edge = "#000000"
    line_width = 0.9

    for year, values in TARGET_DATA.items():
        bottom = 0
        for technology in TARGET_ORDER:
            value = values.get(technology, 0)
            if value <= 0:
                continue
            ax_main.bar(
                TARGET_POS[year],
                value,
                width,
                bottom=bottom,
                color=COLOR_MAP[technology],
                edgecolor=target_edge,
                linewidth=line_width,
            )
            bottom += value
        ax_main.text(TARGET_POS[year], bottom + 25, "Target", ha="center", va="bottom", rotation=90)

    for year, values in ACHIEVED_DATA.items():
        bottom = 0
        for technology in ACHIEVED_ORDER:
            value = values.get(technology, 0)
            if value <= 0:
                continue
            ax_main.bar(
                ACHIEVED_POS[year],
                value,
                width,
                bottom=bottom,
                color=COLOR_MAP[technology],
                edgecolor=achieved_edge,
                linewidth=line_width,
            )
            bottom += value
        ax_main.text(ACHIEVED_POS[year], bottom + 25, "Realized", ha="center", va="bottom", rotation=90)

    ax_main.set_ylabel("Installed capacity (GW)")
    ax_main.grid(axis="y", linestyle="--", alpha=0.35)
    ax_main.set_axisbelow(True)

    x_ticks = [
        (TARGET_POS[2015] + ACHIEVED_POS[2015]) / 2,
        (TARGET_POS[2020] + ACHIEVED_POS[2020]) / 2,
        TARGET_POS[2030],
        TARGET_POS[2035],
    ]
    ax_main.set_xticks(x_ticks)
    ax_main.set_xticklabels(["2015", "2020", "2030", "2035"])

    max_target = max(sum(values.values()) for values in TARGET_DATA.values())
    max_achieved = max(sum(values.values()) for values in ACHIEVED_DATA.values())
    ax_main.set_ylim(0, max(max_target, max_achieved) + 400)

    legend_order = [
        "coal",
        "gas",
        "thermal",
        "nuclear",
        "hydro",
        "wind",
        "solar",
        "wind+solar",
        "pumped storage",
        "new energy storage",
    ]
    legend_items = [
        Patch(facecolor=COLOR_MAP[technology], edgecolor="black", linewidth=line_width, label=technology.capitalize())
        for technology in legend_order
    ]
    ax_main.legend(handles=legend_items, frameon=False, ncol=2, title="Technology", loc="upper left")

    _draw_diff_panel(ax_diff_2015, 2015)
    _draw_diff_panel(ax_diff_2020, 2020)

    fig.suptitle(
        "Installed capacity targets, realized values, and achievement gaps for major power technologies",
        fontsize=15,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    return fig


if __name__ == "__main__":
    make_installed_capacity_plot()
    plt.show()
