import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# Publishable defaults
# -------------------------
plt.rcParams.update({
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
})

# ============================================================
# OFFICIAL ACHIEVED DATA SOURCES (China)
# ------------------------------------------------------------
# 2010:
# 第七次全国森林资源清查主要结果（2004-2008年）
# https://www.forestry.gov.cn/main/65/20100128/326341.html
#
# 2015:
# 国家林业局发展规划与资金管理司解读《林业发展“十三五”规划》
# https://www.forestry.gov.cn/c/www/gkzcjd/56826.jhtml
#
# 2020:
# 关于林草碳汇与应对气候变化
# https://www.forestry.gov.cn/c/www/lczdgz/150626.jhtml
#
# 2025:
# 2025年中国国土绿化状况公报
# https://www.forestry.gov.cn/lyj/1/lcdt/20260312/662822.html
# ============================================================

# -------------------------
# Target data: forest coverage rate (%)
# -------------------------
cov_points = [
    {"year": 2010, "value": 20.00, "label": "20.00"},
    {"year": 2015, "value": 21.66, "label": "21.66"},
    {"year": 2020, "value": 23.04, "label": "23.04"},
    {"year": 2025, "value": 24.10, "label": "24.10"},
    {"year": 2030, "value": 25.00, "label": "25.00"},
    {"year": 2035, "value": 26.00, "label": "26.00"},
]
cov_points = sorted(cov_points, key=lambda d: d["year"])
cov_years = np.array([p["year"] for p in cov_points], dtype=float)
cov_vals  = np.array([p["value"] for p in cov_points], dtype=float)
cov_labs  = [p["label"] for p in cov_points]

# -------------------------
# Achieved data: forest coverage rate (%)
# -------------------------
cov_ach_points = [
    {"year": 2010, "value": 20.36, "label": "20.36"},
    {"year": 2015, "value": 21.66, "label": "21.66"},
    {"year": 2020, "value": 23.04, "label": "23.04"},
    {"year": 2025, "value": 25.09, "label": "25.09"},
]
cov_ach_years = np.array([p["year"] for p in cov_ach_points], dtype=float)
cov_ach_vals  = np.array([p["value"] for p in cov_ach_points], dtype=float)
cov_ach_labs  = [p["label"] for p in cov_ach_points]

# -------------------------
# Target data: forest stock volume (billion m³)
# -------------------------
stock_points = [
    {"year": 2015, "value": 14.3, "label": "14.3"},
    {"year": 2020, "value": 16.5, "label": "16.5"},
    {"year": 2025, "value": 18.0, "label": "18.0"},
    {"year": 2030, "value": 19.0, "label": "19.0"},
    {"year": 2035, "value": 24.0, "label": "24.0"},
]
stock_points = sorted(stock_points, key=lambda d: d["year"])
stock_years = np.array([p["year"] for p in stock_points], dtype=float)
stock_vals  = np.array([p["value"] for p in stock_points], dtype=float)
stock_labs  = [p["label"] for p in stock_points]

# -------------------------
# Achieved data: forest stock volume (billion m³)
# -------------------------
stock_ach_points = [
    {"year": 2015, "value": 15.10,  "label": "15.10"},
    {"year": 2020, "value": 17.56,  "label": "17.56"},
    {"year": 2025, "value": 20.99,  "label": "20.99"},
]
stock_ach_years = np.array([p["year"] for p in stock_ach_points], dtype=float)
stock_ach_vals  = np.array([p["value"] for p in stock_ach_points], dtype=float)
stock_ach_labs  = [p["label"] for p in stock_ach_points]

# -------------------------
# Colors
# -------------------------
target_color = "#1f78b4"    # blue
achieved_color = "#ff7f00"  # orange

# -------------------------
# Helper to style axes
# -------------------------
def style_axis(ax):
    ax.grid(axis="y", linestyle=":", linewidth=0.7, color="0.60", alpha=0.35)
    ax.grid(axis="x", linestyle=":", linewidth=0.5, color="0.80", alpha=0.20)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("0.25")
    ax.spines["bottom"].set_color("0.25")

    ax.tick_params(axis="both", which="major", pad=3)

# -------------------------
# Figure
# -------------------------
fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(13.4, 6.8),
    gridspec_kw={"wspace": 0.24}
)

# ---- Left panel: forest coverage rate ----
ax1.plot(
    cov_years, cov_vals,
    linewidth=2.1, color=target_color, zorder=2, label="Target"
)
ax1.scatter(
    cov_years, cov_vals,
    s=60, facecolor="white", edgecolor=target_color,
    linewidth=1.4, zorder=3
)

ax1.plot(
    cov_ach_years, cov_ach_vals,
    linewidth=2.0, linestyle="--", color=achieved_color, zorder=2, label="Achieved"
)
ax1.scatter(
    cov_ach_years, cov_ach_vals,
    s=54, facecolor=achieved_color, edgecolor="white",
    linewidth=0.8, zorder=3
)

ax1.set_xticks(cov_years.astype(int))
ax1.set_xlabel("Year")
ax1.set_ylabel("Forest coverage rate (%)")
ax1.set_ylim(19.3, 26.7)
ax1.set_yticks([20, 21, 22, 23, 24, 25, 26])

# labels: achieved left, target right
for x, y, lab in zip(cov_ach_years, cov_ach_vals, cov_ach_labs):
    ax1.annotate(
        lab, (x, y), textcoords="offset points", xytext=(-10, 0),
        ha="right", va="center", fontsize=9.2, color=achieved_color
    )

for x, y, lab in zip(cov_years, cov_vals, cov_labs):
    ax1.annotate(
        lab, (x, y), textcoords="offset points", xytext=(10, 0),
        ha="left", va="center", fontsize=9.2, color=target_color
    )

ax1.set_title("Forest coverage rate")
ax1.legend(frameon=False, loc="upper left")
style_axis(ax1)

# ---- Right panel: forest stock volume ----
ax2.plot(
    stock_years, stock_vals,
    linewidth=2.1, color=target_color, zorder=2, label="Target"
)
ax2.scatter(
    stock_years, stock_vals,
    s=60, facecolor="white", edgecolor=target_color,
    linewidth=1.4, zorder=3
)

ax2.plot(
    stock_ach_years, stock_ach_vals,
    linewidth=2.0, linestyle="--", color=achieved_color, zorder=2, label="Achieved"
)
ax2.scatter(
    stock_ach_years, stock_ach_vals,
    s=54, facecolor=achieved_color, edgecolor="white",
    linewidth=0.8, zorder=3
)

ax2.set_xticks(np.array([2015, 2020, 2025, 2030, 2035]))
ax2.set_xlabel("Year")
ax2.set_ylabel("Forest stock volume (billion m³)")
ax2.set_ylim(13.5, 24.8)
ax2.set_yticks([14, 16, 18, 20, 22, 24])

# labels: achieved left, target right
for x, y, lab in zip(stock_ach_years, stock_ach_vals, stock_ach_labs):
    ax2.annotate(
        lab, (x, y), textcoords="offset points", xytext=(-10, 0),
        ha="right", va="center", fontsize=9.2, color=achieved_color
    )

for x, y, lab in zip(stock_years, stock_vals, stock_labs):
    ax2.annotate(
        lab, (x, y), textcoords="offset points", xytext=(10, 0),
        ha="left", va="center", fontsize=9.2, color=target_color
    )

ax2.set_title("Forest stock volume")
ax2.legend(frameon=False, loc="upper left")
style_axis(ax2)

plt.tight_layout()
plt.show()

# Optional saving:
# fig.savefig("forest_targets_vs_achieved_two_panels_publishable.pdf", bbox_inches="tight")
# fig.savefig("forest_targets_vs_achieved_two_panels_publishable.png", dpi=450, bbox_inches="tight")