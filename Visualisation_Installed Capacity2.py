import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

# ------------------------------------------------------------
# GLOBAL FONT
# ------------------------------------------------------------
mpl.rcParams['font.family'] = 'Times New Roman'

# ============================================================
# DATA SOURCES
# ------------------------------------------------------------
# Realized capacity data:
# National Energy Administration (NEA)
# 2015 electricity statistics
# https://www.nea.gov.cn/2016-01/15/c_135013789.htm
#
# 2020 electricity statistics
# https://www.nea.gov.cn/2021-01/20/c_139683739.htm
#
# Pumped storage capacity:
# China Electricity Council (CEC) electricity statistics
# http://www.cec.org.cn/
#
# Target data:
# China National Climate Target Database
# ============================================================

# TARGET DATA
target_data = {
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

# REALIZED DATA
achieved_data = {
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

target_order = [
    "coal","gas","nuclear","hydro","wind","solar",
    "wind+solar","pumped storage","new energy storage"
]

achieved_order = [
    "thermal","nuclear","hydro","wind","solar","pumped storage"
]

# COLORS
color_map = {
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

# FIGURE LAYOUT
fig = plt.figure(figsize=(12,10))
gs = GridSpec(
    2,2,
    width_ratios=[2.6,1.2],
    height_ratios=[1,1],
    wspace=0.30,
    hspace=0.32
)

ax = fig.add_subplot(gs[:,0])
ax_diff_2015 = fig.add_subplot(gs[0,1])
ax_diff_2020 = fig.add_subplot(gs[1,1])

# BAR POSITIONS
target_pos = {2015:0,2020:2,2030:4.2,2035:5.8}
achieved_pos = {2015:0.7,2020:2.7}
width=0.58

target_edge="#666666"
achieved_edge="#000000"
lw=0.9

# TARGET BARS
for year,data in target_data.items():
    bottom=0
    for tech in target_order:
        val=data.get(tech,0)
        if val>0:
            ax.bar(
                target_pos[year],val,width,
                bottom=bottom,
                color=color_map[tech],
                edgecolor=target_edge,
                linewidth=lw
            )
            bottom+=val

    ax.text(target_pos[year],bottom+25,"Target",
            ha="center",va="bottom",rotation=90)

# ACHIEVED BARS
for year,data in achieved_data.items():
    bottom=0
    for tech in achieved_order:
        val=data.get(tech,0)
        if val>0:
            ax.bar(
                achieved_pos[year],val,width,
                bottom=bottom,
                color=color_map[tech],
                edgecolor=achieved_edge,
                linewidth=lw
            )
            bottom+=val

    ax.text(achieved_pos[year],bottom+25,"Realized",
            ha="center",va="bottom",rotation=90)

# AXES
ax.set_ylabel("Installed capacity (GW)")
ax.grid(axis="y",linestyle="--",alpha=0.35)
ax.set_axisbelow(True)

xticks=[
(target_pos[2015]+achieved_pos[2015])/2,
(target_pos[2020]+achieved_pos[2020])/2,
target_pos[2030],
target_pos[2035]
]

ax.set_xticks(xticks)
ax.set_xticklabels(["2015","2020","2030","2035"])

max_target=max(sum(v.values()) for v in target_data.values())
max_achieved=max(sum(v.values()) for v in achieved_data.values())

# extra headroom to avoid overlap
ax.set_ylim(0,max(max_target,max_achieved)+400)

# LEGEND
legend_order=[
"coal","gas","thermal","nuclear","hydro",
"wind","solar","wind+solar",
"pumped storage","new energy storage"
]

legend_items=[
Patch(facecolor=color_map[t],edgecolor="black",linewidth=lw,label=t.capitalize())
for t in legend_order
]

leg=ax.legend(
handles=legend_items,
frameon=False,
ncol=2,
title="Technology",
loc="upper left"
)
leg._legend_box.align="left"

# DIFFERENCE PANELS
overlap=["nuclear","hydro","wind","solar","pumped storage"]

def diff_panel(axis,year):

    diffs=[]
    cols=[]

    for tech in overlap:
        diff=achieved_data[year][tech]-target_data[year][tech]
        diffs.append(diff)
        cols.append(color_map[tech])

    bars=axis.bar(overlap,diffs,color=cols,edgecolor="black",linewidth=0.8)

    axis.axhline(0,color="black",linewidth=0.8)

    axis.set_title(f"Target achievement gap ({year})",fontsize=11)

    axis.set_ylabel("GW")

    axis.grid(axis="y",linestyle="--",alpha=0.3)

    axis.set_xticklabels(
        ["Nuclear","Hydro","Wind","Solar","Pumped\nstorage"],
        fontsize=9
    )

diff_panel(ax_diff_2015,2015)
diff_panel(ax_diff_2020,2020)

# GLOBAL TITLE
fig.suptitle(
"Installed capacity targets, realized values, and achievement gaps for major power technologies",
fontsize=15,
y=0.98
)

plt.tight_layout(rect=[0,0,1,0.96])
plt.show()