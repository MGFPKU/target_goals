import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "axes.titlepad": 10,
        "axes.linewidth": 0.9,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "legend.fontsize": 10,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

COVERAGE_TARGET_POINTS = [
    {"year": 2010, "value": 20.00, "label": "20.00"},
    {"year": 2015, "value": 21.66, "label": "21.66"},
    {"year": 2020, "value": 23.04, "label": "23.04"},
    {"year": 2025, "value": 24.10, "label": "24.10"},
    {"year": 2030, "value": 25.00, "label": "25.00"},
    {"year": 2035, "value": 26.00, "label": "26.00"},
]

COVERAGE_ACHIEVED_POINTS = [
    {"year": 2010, "value": 20.36, "label": "20.36"},
    {"year": 2015, "value": 21.66, "label": "21.66"},
    {"year": 2020, "value": 23.04, "label": "23.04"},
    {"year": 2025, "value": 25.09, "label": "25.09"},
]

STOCK_TARGET_POINTS = [
    {"year": 2015, "value": 14.3, "label": "14.3"},
    {"year": 2020, "value": 16.5, "label": "16.5"},
    {"year": 2025, "value": 18.0, "label": "18.0"},
    {"year": 2030, "value": 19.0, "label": "19.0"},
    {"year": 2035, "value": 24.0, "label": "24.0"},
]

STOCK_ACHIEVED_POINTS = [
    {"year": 2015, "value": 15.10, "label": "15.10"},
    {"year": 2020, "value": 17.56, "label": "17.56"},
    {"year": 2025, "value": 20.99, "label": "20.99"},
]

TARGET_COLOR = "#1f78b4"
ACHIEVED_COLOR = "#ff7f00"


def _style_axis(axis):
    axis.grid(axis="y", linestyle=":", linewidth=0.7, color="0.60", alpha=0.35)
    axis.grid(axis="x", linestyle=":", linewidth=0.5, color="0.80", alpha=0.20)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color("0.25")
    axis.spines["bottom"].set_color("0.25")
    axis.tick_params(axis="both", which="major", pad=3)


def _to_arrays(points):
    sorted_points = sorted(points, key=lambda point: point["year"])
    years = np.array([point["year"] for point in sorted_points], dtype=float)
    values = np.array([point["value"] for point in sorted_points], dtype=float)
    labels = [point["label"] for point in sorted_points]
    return years, values, labels


def make_forest_coverage_stock_plot():
    coverage_years, coverage_vals, coverage_labels = _to_arrays(COVERAGE_TARGET_POINTS)
    coverage_ach_years, coverage_ach_vals, coverage_ach_labels = _to_arrays(COVERAGE_ACHIEVED_POINTS)
    stock_years, stock_vals, stock_labels = _to_arrays(STOCK_TARGET_POINTS)
    stock_ach_years, stock_ach_vals, stock_ach_labels = _to_arrays(STOCK_ACHIEVED_POINTS)

    fig, (ax_coverage, ax_stock) = plt.subplots(
        1,
        2,
        figsize=(13.4, 6.8),
        gridspec_kw={"wspace": 0.24},
    )

    ax_coverage.plot(coverage_years, coverage_vals, linewidth=2.1, color=TARGET_COLOR, zorder=2, label="Target")
    ax_coverage.scatter(coverage_years, coverage_vals, s=60, facecolor="white", edgecolor=TARGET_COLOR, linewidth=1.4, zorder=3)
    ax_coverage.plot(
        coverage_ach_years,
        coverage_ach_vals,
        linewidth=2.0,
        linestyle="--",
        color=ACHIEVED_COLOR,
        zorder=2,
        label="Achieved",
    )
    ax_coverage.scatter(
        coverage_ach_years,
        coverage_ach_vals,
        s=54,
        facecolor=ACHIEVED_COLOR,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )

    ax_coverage.set_xticks(coverage_years.astype(int))
    ax_coverage.set_xlabel("Year")
    ax_coverage.set_ylabel("Forest coverage rate (%)")
    ax_coverage.set_ylim(19.3, 26.7)
    ax_coverage.set_yticks([20, 21, 22, 23, 24, 25, 26])

    for x_value, y_value, label in zip(coverage_ach_years, coverage_ach_vals, coverage_ach_labels):
        ax_coverage.annotate(
            label,
            (x_value, y_value),
            textcoords="offset points",
            xytext=(-10, 0),
            ha="right",
            va="center",
            fontsize=9.2,
            color=ACHIEVED_COLOR,
        )

    for x_value, y_value, label in zip(coverage_years, coverage_vals, coverage_labels):
        ax_coverage.annotate(
            label,
            (x_value, y_value),
            textcoords="offset points",
            xytext=(10, 0),
            ha="left",
            va="center",
            fontsize=9.2,
            color=TARGET_COLOR,
        )

    ax_coverage.set_title("Forest coverage rate")
    ax_coverage.legend(frameon=False, loc="upper left")
    _style_axis(ax_coverage)

    ax_stock.plot(stock_years, stock_vals, linewidth=2.1, color=TARGET_COLOR, zorder=2, label="Target")
    ax_stock.scatter(stock_years, stock_vals, s=60, facecolor="white", edgecolor=TARGET_COLOR, linewidth=1.4, zorder=3)
    ax_stock.plot(
        stock_ach_years,
        stock_ach_vals,
        linewidth=2.0,
        linestyle="--",
        color=ACHIEVED_COLOR,
        zorder=2,
        label="Achieved",
    )
    ax_stock.scatter(
        stock_ach_years,
        stock_ach_vals,
        s=54,
        facecolor=ACHIEVED_COLOR,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )

    ax_stock.set_xticks(np.array([2015, 2020, 2025, 2030, 2035]))
    ax_stock.set_xlabel("Year")
    ax_stock.set_ylabel("Forest stock volume (billion m³)")
    ax_stock.set_ylim(13.5, 24.8)
    ax_stock.set_yticks([14, 16, 18, 20, 22, 24])

    for x_value, y_value, label in zip(stock_ach_years, stock_ach_vals, stock_ach_labels):
        ax_stock.annotate(
            label,
            (x_value, y_value),
            textcoords="offset points",
            xytext=(-10, 0),
            ha="right",
            va="center",
            fontsize=9.2,
            color=ACHIEVED_COLOR,
        )

    for x_value, y_value, label in zip(stock_years, stock_vals, stock_labels):
        ax_stock.annotate(
            label,
            (x_value, y_value),
            textcoords="offset points",
            xytext=(10, 0),
            ha="left",
            va="center",
            fontsize=9.2,
            color=TARGET_COLOR,
        )

    ax_stock.set_title("Forest stock volume")
    ax_stock.legend(frameon=False, loc="upper left")
    _style_axis(ax_stock)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    make_forest_coverage_stock_plot()
    plt.show()
