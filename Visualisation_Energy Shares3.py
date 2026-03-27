import re

import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.artist import Artist
from matplotlib.font_manager import FontProperties
from matplotlib.legend_handler import HandlerTuple
from matplotlib.ticker import MultipleLocator

plt.rcParams["font.family"] = "Arial"
mpl.rcParams["font.serif"] = ["Arial"]


TARGET_DATA = [
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
    (2020, "terminal-electricity", "27 percent", 2020),
    (2025, "terminal-electricity", "30 percent", 2025),
    (2010, "non-fossil-generation", "10 percent", 2010),
    (2015, "non-fossil-generation", "30 percent", 2015),
    (2025, "non-fossil-generation", "39 percent", 2025),
]

FUEL_MAP = {
    "coal": "Coal (primary energy consumption)",
    "gas": "Gas (primary energy consumption)",
    "non-fossil": "Non-fossil (primary energy consumption)",
    "terminal-electricity": "Electricity share (terminal energy)",
    "non-fossil-generation": "Non-fossil (power generation, primary energy)",
}

ACTUAL_DATA = {
    "Year": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2010],
    "Coal (primary energy consumption)": [53.2, 54.8, 56.0, 55.9, 56.9, 57.7, 59.0, 60.6, 62.2, 63.8, 69.2],
    "Gas (primary energy consumption)": [8.8, 8.5, 8.4, 8.8, 8.4, 8.0, 7.6, 6.9, 6.1, 5.8, 4.0],
    "Non-fossil (primary energy consumption)": [19.8, 17.9, 17.6, 16.7, 15.9, 15.3, 14.5, 13.6, 13.0, 12.0, 9.4],
}

COLORS = {
    "Coal (primary energy consumption)": "#1a659b",
    "Gas (primary energy consumption)": "#8E1B11",
    "Non-fossil (primary energy consumption)": "#2A5F4A",
    "Electricity share (terminal energy)": "#7B1FA2",
    "Non-fossil (power generation, primary energy)": "#6D6D6D",
}


def parse_percent(text):
    match = re.search(r"([0-9]+\.?[0-9]*)", text)
    return float(match.group(1)) if match else None


def _header(text):
    handle = mlines.Line2D([], [], linestyle="None")
    return handle, text


def make_energy_mix_shares_plot():
    df = pd.DataFrame(TARGET_DATA, columns=["Announcement_Year", "Fuel", "Targeted_Change", "Target_Year"])
    df["Value"] = df["Targeted_Change"].apply(parse_percent)

    df = df[df["Fuel"].isin(FUEL_MAP.keys())].copy()
    df["Fuel"] = df["Fuel"].map(FUEL_MAP)

    df_sorted = df.sort_values(["Fuel", "Target_Year", "Announcement_Year"])
    df_grouped = df_sorted.groupby(["Fuel", "Target_Year"]).last().reset_index()[["Fuel", "Target_Year", "Value"]]
    df_pivot = df_grouped.pivot(index="Target_Year", columns="Fuel", values="Value").sort_index()

    revision_map = {}
    for fuel in df["Fuel"].unique():
        revision_map[fuel] = df[df["Fuel"] == fuel].groupby("Target_Year")["Value"].apply(list).to_dict()

    df_actual = pd.DataFrame(ACTUAL_DATA)

    target_years = df_pivot.index.tolist()
    x = np.arange(len(target_years))

    fig, ax = plt.subplots(figsize=(14, 8))

    for fuel in df_pivot.columns:
        y_vals = df_pivot[fuel].reindex(target_years)

        for index, value in enumerate(y_vals):
            if pd.isna(value):
                continue
            ax.plot(
                index,
                value,
                marker="o",
                color=COLORS[fuel],
                markersize=15,
                markeredgecolor="white",
                markeredgewidth=1.5,
            )
            ax.plot(
                index,
                value,
                marker="o",
                color=COLORS[fuel],
                markersize=7,
                markeredgecolor="white",
                markeredgewidth=1.2,
            )

        for index, year in enumerate(target_years):
            values = revision_map[fuel].get(year, [])
            if len(values) <= 1:
                continue

            df_revision = df[(df["Fuel"] == fuel) & (df["Target_Year"] == year)].sort_values("Announcement_Year")
            ordered_values = df_revision["Value"].tolist()
            if len(ordered_values) < 2:
                continue

            start_value, end_value = ordered_values[0], ordered_values[-1]
            ax.bar(
                x[index],
                end_value - start_value,
                bottom=start_value,
                width=0.12,
                color="gray",
                alpha=0.6,
                edgecolor="black",
                linewidth=0.8,
            )
            ax.annotate(
                "",
                xy=(x[index], end_value),
                xytext=(x[index], start_value),
                arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2),
            )

    year_to_x = {year: index for index, year in enumerate(target_years)}
    tracked_fuels = [
        "Coal (primary energy consumption)",
        "Gas (primary energy consumption)",
        "Non-fossil (primary energy consumption)",
    ]

    for _, row in df_actual.iterrows():
        year = row["Year"]
        if year not in year_to_x:
            continue
        x_index = year_to_x[year]
        for fuel in tracked_fuels:
            ax.plot(
                x_index,
                row[fuel],
                marker="D",
                color=COLORS[fuel],
                markersize=7,
                markeredgecolor="black",
                markeredgewidth=0.8,
            )

    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Target Year")
    ax.set_ylabel("Share by Source (%)", fontsize=14)
    ax.set_title("Energy Mix Targets and Realized Shares in China", loc="left", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(target_years)

    handles: list[Artist | tuple[Artist, ...]] = []
    labels: list[str] = []

    handle, label = _header("Primary energy consumption")
    handles.append(handle)
    labels.append(label)

    for fuel in tracked_fuels:
        target = mlines.Line2D(
            [],
            [],
            color=COLORS[fuel],
            marker="o",
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=1.2,
            linestyle="None",
        )
        actual = mlines.Line2D(
            [],
            [],
            color=COLORS[fuel],
            marker="D",
            markersize=6,
            markeredgecolor="black",
            markeredgewidth=0.8,
            linestyle="None",
        )
        handles.append((target, actual))
        labels.append(fuel.replace(" (primary energy consumption)", ""))

    handle, label = _header("Terminal energy consumption")
    handles.append(handle)
    labels.append(label)
    handles.append(
        mlines.Line2D(
            [],
            [],
            color=COLORS["Electricity share (terminal energy)"],
            marker="o",
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=1.2,
            linestyle="None",
        )
    )
    labels.append("Electricity")

    handle, label = _header("Primary energy generation")
    handles.append(handle)
    labels.append(label)
    handles.append(
        mlines.Line2D(
            [],
            [],
            color=COLORS["Non-fossil (power generation, primary energy)"],
            marker="o",
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=1.2,
            linestyle="None",
        )
    )
    labels.append("Non-fossil")

    handle, label = _header("Symbols")
    handles.append(handle)
    labels.append(label)

    target_symbol = mlines.Line2D([], [], color="black", marker="o", markersize=8, linestyle="None")
    actual_symbol = mlines.Line2D([], [], color="black", marker="D", markersize=6, linestyle="None")
    revision_symbol = mlines.Line2D([], [], color="black", marker=r"$\rightarrow$", markersize=10, linestyle="None")

    handles.extend([target_symbol, actual_symbol, revision_symbol])
    labels.extend(["Target", "Realized", "Revised target"])

    legend = ax.legend(
        handles,
        labels,
        handler_map={tuple: HandlerTuple(ndivide=None)},
        frameon=False,
        fontsize=9,
        ncol=3,
        columnspacing=1.6,
        handletextpad=0.8,
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        prop=FontProperties(family="Arial", size=9),
    )

    for text in legend.get_texts():
        if text.get_text() in [
            "Primary energy consumption",
            "Terminal energy consumption",
            "Primary energy generation",
            "Symbols",
        ]:
            text.set_fontweight("bold")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    make_energy_mix_shares_plot()
    plt.show()
