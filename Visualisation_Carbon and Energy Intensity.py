import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import AutoMinorLocator
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import math, re

# ----------------------------
# Shared aesthetics
# ----------------------------
rcParams["font.family"] = "Times New Roman"
COLOR_REALIZED    = "#405A79"   # realized line
COLOR_TARGET      = "#2F6B58"   # dotted targets
COLOR_RANGE_FILL  = "#2F6B58"   # band fill for ranges (carbon)
COLOR_ABS_DIAMOND = "#6F6860"   # subtle diamond color (energy abs targets)
GRID_GRAY         = "#9AA0A6"

def dotted_line_with_endpoint(ax, x0, y0, x1, y1,
                              color=COLOR_TARGET, lw=1.4,
                              pattern=(0.5, 1.4),
                              ms_end=3.0):
    seg, = ax.plot([x0, x1], [y0, y1],
                   linestyle=(0, pattern), linewidth=lw,
                   color=color, zorder=3)
    seg.set_dash_capstyle('round')
    ax.plot([x1], [y1], marker="o", markersize=ms_end,
            markerfacecolor=color, markeredgecolor="white",
            markeredgewidth=0.7, zorder=4)
    return seg

def fmt_pct(val: float) -> str:
    if math.isclose(val, round(val), abs_tol=1e-9):
        return f"{int(round(val))}"
    return f"{val:.1f}".rstrip("0").rstrip(".")

def apply_grid(ax):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(which="major", axis="both", linestyle="--", linewidth=0.6, color=GRID_GRAY, alpha=0.45)
    ax.grid(which="minor", axis="both", linestyle=":",  linewidth=0.5, color=GRID_GRAY, alpha=0.25)

# ========== Panel A: Carbon intensity ==========
# Realized (kg CO2 / 10k yuan, 2005 prices)
realized_kg = {
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
years_carbon = range(2005, 2031)
s_real_c = pd.Series(realized_kg, dtype="float64").reindex(years_carbon)
s_real_c_interp = s_real_c.interpolate("linear")
s_plot_c = s_real_c.dropna()

# Targets (≥5-year spans only)
targets_c = [
    dict(baseline=2010, target_year=2015, pct=17),               # 5YP
    dict(baseline=2005, target_year=2020, pct_range=(40, 45)),   # long-term range
    dict(baseline=2015, target_year=2020, pct=18),               # 5YP
    dict(baseline=2020, target_year=2025, pct=18),               # 5YP
    dict(baseline=2005, target_year=2030, pct_range=(60, 65)),   # long-term range
]

# ========== Panel B: Energy intensity ==========
# Absolute targets (rebase 1990¥ -> 2005¥)
P1990, P2005 = 26, 61
r = P1990 / P2005
abs_targets_1990 = {2010: 2.25, 2020: 1.54}    # in 1990¥
abs_targets_2005 = {2015: 0.869}               # already 2005¥
abs_targets_2005.update({y: v * r for y, v in abs_targets_1990.items()})

# Realized energy intensity (2005¥)
realized_e = [
    (1990,2.259788354),(1991,2.173371973),(1992,2.000539212),(1993,1.866593822),
    (1994,1.749931708),(1995,1.685119423),(1996,1.581419766),(1997,1.451795195),
    (1998,1.352416357),(1999,1.296245710),(2000,1.248716700),(2001,1.220104398),
    (2002,1.220104398),(2003,1.288361987),(2004,1.365151774),(2005,1.390748370),
    (2006,1.36),(2007,1.29),(2008,1.24),(2009,1.16),(2010,1.13),
    (2011,1.112431568),(2012,1.073625816),(2013,1.021884813),(2014,0.983079060),
    (2015,0.931338057),(2016,0.889021167),(2017,0.859387129),(2018,0.829753090),
    (2019,0.814936070),(2020,0.814936070),(2021,0.792120979),(2022,0.792120979),
]
df_real_e_all = pd.DataFrame(realized_e, columns=["Year","Realized_2005"])
s_real_e = df_real_e_all.set_index("Year")["Realized_2005"].reindex(range(2005, 2031))  # start at 2005
s_real_e_interp = s_real_e.interpolate("linear")
s_plot_e = s_real_e.dropna()

# Percentage-reduction targets (energy) — pre-2015 18% (2003→2010) REMOVED
pct_rows_e = [
    dict(Announcement_Year=2007, Targeted_Change="20 percent",            Baseline_Year=2005, Target_Year=2010),
    dict(Announcement_Year=2011, Targeted_Change="16 percent",            Baseline_Year=2010, Target_Year=2015),
    dict(Announcement_Year=2016, Targeted_Change="15 percent",            Baseline_Year=2015, Target_Year=2020),
    dict(Announcement_Year=2021, Targeted_Change="13.5 percent",          Baseline_Year=2020, Target_Year=2025),
]
df_pct_e = pd.DataFrame(pct_rows_e)

def parse_pct(s: str):
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    pct = float(m.group(1)) if m else None
    lower_bound = ("more than" in s.lower()) or ("at least" in s.lower())
    return pct, lower_bound

df_pct_e[["pct","lower_bound"]] = df_pct_e["Targeted_Change"].apply(lambda s: pd.Series(parse_pct(s)))
real_map_e = dict(realized_e)
df_pct_e["Baseline_Value_2005"]       = df_pct_e["Baseline_Year"].map(real_map_e)
df_pct_e["Implied_Target_Value_2005"] = df_pct_e["Baseline_Value_2005"] * (1 - df_pct_e["pct"]/100.0)
df_pct_e = df_pct_e.drop_duplicates(subset=["Baseline_Year","Target_Year","pct"]).reset_index(drop=True)

# ----------------------------
# One figure, two panels STACKED (shared timeline)
# ----------------------------
fig, (axA, axB) = plt.subplots(2, 1, figsize=(9.2, 10.4), sharex=True, constrained_layout=True)
fig.suptitle("Carbon and Energy Intensity in China: Realized vs. Targets", fontweight="bold")

# ----- Panel a: Carbon intensity -----
ax = axA
ax.plot(s_plot_c.index, s_plot_c.values,
        color=COLOR_REALIZED, marker="o", markersize=3.6,
        linewidth=1.9, alpha=0.9, label="Realized carbon intensity")

for t in targets_c:
    b, ty = t["baseline"], t["target_year"]
    base_val = s_real_c_interp.loc[b]
    if pd.isna(base_val): continue
    if "pct" in t:
        y1 = base_val * (1 - t["pct"]/100.0)
        dotted_line_with_endpoint(ax, b, base_val, ty, y1, ms_end=3.0)
        midx, midy = (b + ty)/2, (base_val + y1)/2
        txt = f"-{fmt_pct(t['pct'])}%"
        ax.annotate(txt, (midx, midy), xytext=(0, 12),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=COLOR_TARGET,
                    path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)])
    else:
        low, high = t["pct_range"]
        y1_lo = base_val * (1 - high/100.0)   # more ambitious
        y1_hi = base_val * (1 - low/100.0)    # less ambitious
        dotted_line_with_endpoint(ax, b, base_val, ty, y1_lo, ms_end=2.8)
        dotted_line_with_endpoint(ax, b, base_val, ty, y1_hi, ms_end=2.8)
        x = np.array([b, ty])
        lower = np.array([base_val, min(y1_lo, y1_hi)])
        upper = np.array([base_val, max(y1_lo, y1_hi)])
        ax.fill_between(x, lower, upper, color=COLOR_RANGE_FILL, alpha=0.3, zorder=2)
        midx = (b + ty) / 2
        midy = ((base_val + min(y1_lo, y1_hi))/2 + (base_val + max(y1_lo, y1_hi))/2) / 2
        txt = f"-{fmt_pct(low)}–{fmt_pct(high)}%"
        ax.annotate(txt, (midx, midy), xytext=(0, 0),
                    textcoords="offset points", ha="center", va="center",
                    fontsize=10, fontweight="bold", color=COLOR_TARGET,
                    path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)])

# Y-limits for panel A
vals_c = list(s_plot_c.values)
for t in targets_c:
    b = t["baseline"]; base_val = s_real_c_interp.loc[b]
    if "pct" in t:
        vals_c.append(base_val * (1 - t["pct"]/100.0))
    else:
        low, high = t["pct_range"]
        vals_c += [base_val * (1 - low/100.0), base_val * (1 - high/100.0)]
ax.set_ylim(min(vals_c)*0.9, max(vals_c)*1.03)

ax.set_ylabel("Carbon intensity (kg CO₂ per 10,000 yuan, 2005 prices)")
ax.set_title("a. Carbon intensity", loc="left", fontweight="bold")
apply_grid(ax)

legend_items_a = [
    Line2D([0],[0], color=COLOR_REALIZED, lw=1.9, marker="o", markersize=3.8, label="Realized"),
    Line2D([0],[0], color=COLOR_TARGET, lw=1.4, linestyle=(0,(0.5,1.4)), label="5YP target"),
    Patch(facecolor=COLOR_RANGE_FILL, edgecolor='none', alpha=0.3, label="Long-term range target"),
]
ax.legend(handles=legend_items_a, frameon=False, loc="upper right")

# ----- Panel b: Energy intensity -----
ax = axB
ax.plot(s_plot_e.index, s_plot_e.values,
        color=COLOR_REALIZED, marker="o", markersize=3.6,
        linewidth=1.9, alpha=0.9, label="Realized energy intensity")

for _, r in df_pct_e.iterrows():
    x0, y0 = int(r["Baseline_Year"]), float(r["Baseline_Value_2005"])
    x1, y1 = int(r["Target_Year"]),   float(r["Implied_Target_Value_2005"])
    dotted_line_with_endpoint(ax, x0, y0, x1, y1, ms_end=2.8)
    midx, midy = (x0 + x1)/2, (y0 + y1)/2
    txt = f"-{fmt_pct(r['pct'])}%"
    if r["lower_bound"]:
        txt = "≥" + txt
    ax.annotate(txt, (midx, midy), xytext=(0, 12),
                textcoords="offset points", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=COLOR_TARGET,
                path_effects=[pe.withStroke(linewidth=2.0, foreground="white", alpha=0.9)])

# Absolute targets as small, subtle diamonds
abs_years = sorted(abs_targets_2005.keys())
abs_vals  = [abs_targets_2005[y] for y in abs_years]
ax.plot(abs_years, abs_vals,
        linestyle="None", marker="D", markersize=5.0,
        markeredgewidth=0.8, markeredgecolor="white",
        color=COLOR_ABS_DIAMOND, label="Absolute targets", zorder=5)
for yr, val in zip(abs_years, abs_vals):
    ax.annotate(f"{val:.2f}", xy=(yr, val), xytext=(0, -8),
                textcoords="offset points", ha="center", va="top",
                fontsize=9, fontweight="bold", color=COLOR_ABS_DIAMOND)

# Shared X timeline for BOTH panels (2005–2031) with 5-year major ticks
for ax_ in (axA, axB):
    ax_.set_xlim(2005, 2031)
axB.set_xticks([2005, 2010, 2015, 2020, 2025, 2030])

# Y-limits for panel B
vals_e = list(s_plot_e.values) + abs_vals + df_pct_e["Implied_Target_Value_2005"].tolist()
ax.set_ylim(min(vals_e)*0.9, max(vals_e)*1.03)

ax.set_xlabel("Year")
ax.set_ylabel("Energy intensity (tce per 10,000 yuan, 2005 prices)")
ax.set_title("b. Energy intensity", loc="left", fontweight="bold")
apply_grid(ax)

legend_items_b = [
    Line2D([0],[0], color=COLOR_REALIZED, lw=1.9, marker="o", markersize=3.8, label="Realized"),
    Line2D([0],[0], color=COLOR_ABS_DIAMOND, marker="D", linestyle="None", markersize=5.0, label="Absolute targets"),
    Line2D([0],[0], color=COLOR_TARGET, lw=1.4, linestyle=(0,(0.5,1.4)), label="Percentage targets"),
]
ax.legend(handles=legend_items_b, frameon=False, loc="upper right")

plt.show()
