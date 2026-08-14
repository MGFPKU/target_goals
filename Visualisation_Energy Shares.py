import re

import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.legend_handler import HandlerPatch
from matplotlib.ticker import MultipleLocator

from i18n import i18n, get_font_family


# ------------------------------------------------------------
# 1. Policy target data
# ------------------------------------------------------------

data = [
    (2013, "coal", "around 65 percent", 2015),
    (2013, "coal", "below 65 percent", 2017),
    (2014, "coal", "62 percent", 2020),
    (2016, "coal", "below 58 percent", 2020),
    (2013, "gas", "7.5 percent", 2015),
    (2012, "gas", "5.3 percent", 2010),
    (2014, "gas", "10 percent", 2020),
    (2007, "non-fossil", "10 percent", 2010),
    (2011, "non-fossil", "11.4 percent", 2015),
    (2013, "non-fossil", "13 percent", 2017),
    (2014, "non-fossil", "15 percent", 2020),
    (2016, "non-fossil", "20 percent", 2030),
    (2021, "non-fossil", "25 percent", 2030),
    (2024, "non-fossil", "18.9 percent", 2024),
    (2021, "non-fossil", "20 percent", 2025),
    (2021, "non-fossil", "80 percent", 2060),
    (2023, "non-fossil", "18.3 percent", 2023),
    (2024, "non-fossil", "more than 30 percent", 2035),
]


def parse_percent(value):
    match = re.search(r"([0-9]+\.?[0-9]*)", value)
    return float(match.group(1)) if match else np.nan


df = pd.DataFrame(
    data,
    columns=[
        "Announcement_Year",
        "Fuel",
        "Targeted_Change",
        "Target_Year",
    ],
)

df["Value"] = df["Targeted_Change"].apply(parse_percent)


fuel_map = {
    "coal": "Coal",
    "gas": "Gas",
    "non-fossil": "Non-fossil",
}

df = df[df["Fuel"].isin(fuel_map)].copy()
df["Fuel"] = df["Fuel"].map(fuel_map)


df_sorted = df.sort_values(["Fuel", "Target_Year", "Announcement_Year"])

df_grouped = (
    df_sorted.groupby(["Fuel", "Target_Year"])
    .last()
    .reset_index()[["Fuel", "Target_Year", "Value"]]
)

df_pivot = df_grouped.pivot(
    index="Target_Year",
    columns="Fuel",
    values="Value",
).sort_index()


revision_map = {}

for fuel in df["Fuel"].unique():
    revision_map[fuel] = (
        df[df["Fuel"] == fuel].groupby("Target_Year")["Value"].apply(list).to_dict()
    )


# ------------------------------------------------------------
# 2. Realised data
# ------------------------------------------------------------

actual_data = {
    "Year": [
        2025,
        2024,
        2023,
        2022,
        2021,
        2020,
        2019,
        2018,
        2017,
        2016,
        2015,
        2010,
    ],
    "Coal": [
        np.nan,
        53.2,
        54.8,
        56.0,
        55.9,
        56.9,
        57.7,
        59.0,
        60.6,
        62.2,
        63.8,
        69.2,
    ],
    "Gas": [
        np.nan,
        8.8,
        8.5,
        8.4,
        8.8,
        8.4,
        8.0,
        7.6,
        6.9,
        6.1,
        5.8,
        4.0,
    ],
    "Non-fossil": [
        21.7,
        19.8,
        17.9,
        17.6,
        16.7,
        15.9,
        15.3,
        14.5,
        13.6,
        13.0,
        12.0,
        9.4,
    ],
}


df_actual = pd.DataFrame(actual_data).sort_values("Year").reset_index(drop=True)


# ------------------------------------------------------------
# 3. Plot setup
# ------------------------------------------------------------

target_years = df_pivot.index.tolist()
x = np.arange(len(target_years))

year_to_x = {year: position for position, year in enumerate(target_years)}


colors = {
    "Coal": "#1a659b",
    "Gas": "#8E1B11",
    "Non-fossil": "#2A5F4A",
}

fuel_order = ["Coal", "Gas", "Non-fossil"]


def make_energy_mix_shares_plot():

    fig, ax = plt.subplots(figsize=(10, 5.6), constrained_layout=True)

    # Align font with the existing project styling
    plt.rcParams.update(
        {
            "font.family": get_font_family(),
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )

    # --------------------------------------------------------
    # 4. Realised values
    # --------------------------------------------------------

    for fuel in fuel_order:
        realised_subset = df_actual[df_actual["Year"].isin(target_years)].copy()

        realised_subset["x"] = realised_subset["Year"].map(year_to_x)
        realised_subset = realised_subset.sort_values("x")

        ax.plot(
            realised_subset["x"],
            realised_subset[fuel],
            color=colors[fuel],
            linewidth=2.1,
            linestyle="-",
            marker=None,
            solid_capstyle="round",
            zorder=2,
        )

    # --------------------------------------------------------
    # 5. Target values
    # --------------------------------------------------------

    for fuel in fuel_order:
        y_values = df_pivot[fuel].reindex(target_years)

        ax.scatter(
            x,
            y_values,
            s=84,
            color=colors[fuel],
            edgecolor="white",
            linewidth=1.1,
            zorder=4,
        )

    # --------------------------------------------------------
    # 6. Revised targets as arrows
    # --------------------------------------------------------

    for fuel in fuel_order:
        for i, year in enumerate(target_years):
            values = revision_map.get(fuel, {}).get(year, [])

            if len(values) > 1:
                df_revision = df[
                    (df["Fuel"] == fuel) & (df["Target_Year"] == year)
                ].sort_values("Announcement_Year")

                ordered_values = df_revision["Value"].tolist()

                if len(ordered_values) >= 2:
                    start_value = ordered_values[0]
                    end_value = ordered_values[-1]

                    ax.annotate(
                        "",
                        xy=(x[i], end_value),
                        xytext=(x[i], start_value),
                        arrowprops={
                            "arrowstyle": "-|>",
                            "color": "#202020",
                            "linewidth": 1.7,
                            "mutation_scale": 14,
                            "shrinkA": 7,
                            "shrinkB": 7,
                        },
                        zorder=6,
                    )

    # --------------------------------------------------------
    # 7. Axis styling
    # --------------------------------------------------------

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_linewidth(1.1)
    ax.spines["bottom"].set_linewidth(1.1)

    ax.yaxis.set_major_locator(MultipleLocator(10))

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.65,
        color="#BEBEBE",
        alpha=0.65,
        zorder=0,
    )

    ax.set_ylim(
        0,
        90,
    )

    ax.set_xlabel(
        i18n("Target year"),
        fontsize=11,
        labelpad=8,
    )

    ax.set_ylabel(
        i18n("Share of primary energy consumption (%)"),
        fontsize=11,
        labelpad=8,
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        target_years,
        fontsize=10,
    )

    ax.tick_params(
        axis="x",
        length=4,
        width=0.9,
        pad=5,
        color="#4D4D4D",
    )

    ax.tick_params(
        axis="y",
        length=4,
        width=0.9,
        pad=5,
        color="#4D4D4D",
    )

    ax.set_xlim(
        -0.55,
        len(target_years) - 0.45,
    )

    # --------------------------------------------------------
    # 8. Legend symbols
    # --------------------------------------------------------

    target_symbol = mlines.Line2D(
        [],
        [],
        marker="o",
        linestyle="None",
        markersize=8,
        markerfacecolor="#404040",
        markeredgecolor="white",
        markeredgewidth=1.0,
        color="#404040",
        label=i18n("Target"),
    )

    revision_symbol = mpatches.FancyArrowPatch(
        (0, 0),
        (1, 0),
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.7,
        color="#202020",
    )

    realised_symbol = mlines.Line2D(
        [],
        [],
        color="#404040",
        linewidth=2.1,
        linestyle="-",
        label=i18n("Realised"),
    )

    def make_legend_arrow(
        legend,
        orig_handle,
        xdescent,
        ydescent,
        width,
        height,
        fontsize,
    ):
        return mpatches.FancyArrowPatch(
            (
                xdescent,
                ydescent + height / 2,
            ),
            (
                xdescent + width,
                ydescent + height / 2,
            ),
            arrowstyle="-|>",
            mutation_scale=fontsize,
            linewidth=1.7,
            color="#202020",
        )

    # Left legend: symbol meaning
    symbol_legend = ax.legend(
        handles=[
            target_symbol,
            revision_symbol,
            realised_symbol,
        ],
        labels=[
            i18n("Target"),
            i18n("Revised target"),
            i18n("Realised"),
        ],
        handler_map={
            mpatches.FancyArrowPatch: HandlerPatch(patch_func=make_legend_arrow)
        },
        ncol=1,
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(0.03, 1.005),
        borderaxespad=0,
        handlelength=2.3,
        handletextpad=0.6,
        labelspacing=0.45,
        fontsize=10,
    )

    ax.add_artist(symbol_legend)

    # Right legend: energy source colours
    coal_square = mlines.Line2D(
        [],
        [],
        marker="s",
        linestyle="None",
        markersize=9,
        markerfacecolor=colors["Coal"],
        markeredgecolor=colors["Coal"],
        label=i18n("Coal"),
    )

    gas_square = mlines.Line2D(
        [],
        [],
        marker="s",
        linestyle="None",
        markersize=9,
        markerfacecolor=colors["Gas"],
        markeredgecolor=colors["Gas"],
        label=i18n("Gas"),
    )

    non_fossil_square = mlines.Line2D(
        [],
        [],
        marker="s",
        linestyle="None",
        markersize=9,
        markerfacecolor=colors["Non-fossil"],
        markeredgecolor=colors["Non-fossil"],
        label=i18n("Non-fossil"),
    )

    ax.legend(
        handles=[
            coal_square,
            gas_square,
            non_fossil_square,
        ],
        ncol=3,
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(0.42, 1.005),
        borderaxespad=0,
        handlelength=0.9,
        handletextpad=0.5,
        columnspacing=1.2,
        fontsize=10,
    )

    return fig


if __name__ == "__main__":
    make_energy_mix_shares_plot()
    plt.show()
