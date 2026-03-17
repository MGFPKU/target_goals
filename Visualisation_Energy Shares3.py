import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.lines as mlines
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from matplotlib.legend_handler import HandlerTuple
from matplotlib.font_manager import FontProperties

# --------------------------
# Global font settings
# --------------------------
plt.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.serif'] = ['Times New Roman']

# --------------------------
# 1) Policy target data
# --------------------------
data = [
    (2013,'coal','around 65 percent',2015),
    (2013,'coal','below 65 percent',2017),
    (2014,'coal','62 percent',2020),
    (2016,'coal','below 58 percent',2020),

    (2013,'gas','7.5 percent',2015),
    (2012,'gas','5.3 percent',2010),
    (2014,'gas','10 percent',2020),

    (2007,'non-fossil','10 percent',2010),
    (2011,'non-fossil','11.4 percent',2015),
    (2013,'non-fossil','13 percent',2017),
    (2014,'non-fossil','15 percent',2020),
    (2016,'non-fossil','20 percent',2030),
    (2021,'non-fossil','25 percent',2030),
    (2024,'non-fossil','18.9 percent',2024),
    (2021,'non-fossil','20 percent',2025),
    (2021,'non-fossil','80 percent',2060),
    (2023,'non-fossil','18.3 percent',2023),
    (2024,'non-fossil','more than 30 percent',2035),

    (2020,'terminal-electricity','27 percent',2020),
    (2025,'terminal-electricity','30 percent',2025),

    (2010,'non-fossil-generation','10 percent',2010),
    (2015,'non-fossil-generation','30 percent',2015),
    (2025,'non-fossil-generation','39 percent',2025)
]

def parse_percent(s):
    match = re.search(r"([0-9]+\.?[0-9]*)", s)
    return float(match.group(1)) if match else None

df = pd.DataFrame(data,columns=["Announcement_Year","Fuel","Targeted_Change","Target_Year"])
df["Value"] = df["Targeted_Change"].apply(parse_percent)

fuel_map = {
'coal':'Coal (primary energy consumption)',
'gas':'Gas (primary energy consumption)',
'non-fossil':'Non-fossil (primary energy consumption)',
'terminal-electricity':'Electricity share (terminal energy)',
'non-fossil-generation':'Non-fossil (power generation, primary energy)'
}

df = df[df["Fuel"].isin(fuel_map.keys())].copy()
df["Fuel"] = df["Fuel"].map(fuel_map)

df_sorted = df.sort_values(["Fuel","Target_Year","Announcement_Year"])
df_grouped = df_sorted.groupby(["Fuel","Target_Year"]).last().reset_index()[["Fuel","Target_Year","Value"]]
df_pivot = df_grouped.pivot(index="Target_Year",columns="Fuel",values="Value").sort_index()

revision_map={}
for fuel in df["Fuel"].unique():
    revision_map[fuel]=df[df["Fuel"]==fuel].groupby("Target_Year")["Value"].apply(list).to_dict()

# --------------------------
# 2) Actual data
# --------------------------
actual_data={
"Year":[2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2010],
"Coal (primary energy consumption)":[53.2,54.8,56.0,55.9,56.9,57.7,59.0,60.6,62.2,63.8,69.2],
"Gas (primary energy consumption)":[8.8,8.5,8.4,8.8,8.4,8.0,7.6,6.9,6.1,5.8,4.0],
"Non-fossil (primary energy consumption)":[19.8,17.9,17.6,16.7,15.9,15.3,14.5,13.6,13.0,12.0,9.4]
}

df_actual=pd.DataFrame(actual_data)

# --------------------------
# 3) Plot
# --------------------------
target_years=df_pivot.index.tolist()
x=np.arange(len(target_years))

fig,ax=plt.subplots(figsize=(14,8))

colors={
"Coal (primary energy consumption)":"#1f77b4",
"Gas (primary energy consumption)":"#ff7f0e",
"Non-fossil (primary energy consumption)":"#2ca02c",
"Electricity share (terminal energy)":"#7b1fa2",
"Non-fossil (power generation, primary energy)":"#6d6d6d"
}

# Targets
for fuel in df_pivot.columns:

    y_vals=df_pivot[fuel].reindex(target_years)

    for i,y in enumerate(y_vals):
        if not pd.isna(y):

            ax.plot(i,y,marker='o',
                    color=colors[fuel],markersize=15,
                    markeredgecolor='white',markeredgewidth=1.5)

            ax.plot(i,y,marker='o',
                    color=colors[fuel],markersize=7,
                    markeredgecolor='white',markeredgewidth=1.2)

    for i,year in enumerate(target_years):

        vals=revision_map[fuel].get(year,[])

        if len(vals)>1:

            df_rev=df[(df["Fuel"]==fuel)&(df["Target_Year"]==year)].sort_values("Announcement_Year")
            vals_ordered=df_rev["Value"].tolist()

            if len(vals_ordered)>=2:

                start_val,end_val=vals_ordered[0],vals_ordered[-1]

                ax.bar(x[i],end_val-start_val,bottom=start_val,
                       width=0.12,color='gray',alpha=0.6,
                       edgecolor='black',linewidth=0.8)

                ax.annotate("",xy=(x[i],end_val),xytext=(x[i],start_val),
                            arrowprops=dict(arrowstyle="->",color="black",linewidth=1.2))

# Actual diamonds
year_to_x={year:i for i,year in enumerate(target_years)}

for _,row in df_actual.iterrows():

    if row["Year"] in year_to_x:

        xi=year_to_x[row["Year"]]

        for fuel in [
        "Coal (primary energy consumption)",
        "Gas (primary energy consumption)",
        "Non-fossil (primary energy consumption)"
        ]:

            ax.plot(xi,row[fuel],marker='D',
                    color=colors[fuel],markersize=7,
                    markeredgecolor='black',markeredgewidth=0.8)

# --------------------------
# 4) Styling
# --------------------------
ax.set_facecolor("white")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.yaxis.set_major_locator(MultipleLocator(10))
ax.grid(axis='y',linestyle='--',alpha=0.35)

ax.set_ylim(0,100)

ax.set_xlabel("Target Year",fontsize=14)
ax.set_ylabel("Share by Source (%)",fontsize=14)
ax.set_title("Energy Mix Targets and Realized Shares in China",fontsize=16,weight='bold')

ax.set_xticks(x)
ax.set_xticklabels(target_years)

# --------------------------
# 5) Legend with clean grouping
# --------------------------

def header(text):
    handle=mlines.Line2D([],[],linestyle="None")
    return handle,text

handles=[]
labels=[]

# Primary energy consumption
h,l=header("Primary energy consumption")
handles.append(h);labels.append(l)

for fuel in [
"Coal (primary energy consumption)",
"Gas (primary energy consumption)",
"Non-fossil (primary energy consumption)"
]:

    target=mlines.Line2D([],[],color=colors[fuel],
                         marker='o',markersize=8,
                         markeredgecolor='white',markeredgewidth=1.2,
                         linestyle='None')

    actual=mlines.Line2D([],[],color=colors[fuel],
                         marker='D',markersize=6,
                         markeredgecolor='black',markeredgewidth=0.8,
                         linestyle='None')

    handles.append((target,actual))
    labels.append(fuel.replace(" (primary energy consumption)",""))

# Terminal
h,l=header("Terminal energy consumption")
handles.append(h);labels.append(l)

handles.append(
mlines.Line2D([],[],color=colors["Electricity share (terminal energy)"],
marker='o',markersize=8,markeredgecolor='white',markeredgewidth=1.2,linestyle='None')
)
labels.append("Electricity")

# Generation
h,l=header("Primary energy generation")
handles.append(h);labels.append(l)

handles.append(
mlines.Line2D([],[],color=colors["Non-fossil (power generation, primary energy)"],
marker='o',markersize=8,markeredgecolor='white',markeredgewidth=1.2,linestyle='None')
)
labels.append("Non-fossil")

# Symbols
h,l=header("Symbols")
handles.append(h);labels.append(l)

target_symbol=mlines.Line2D([],[],color='black',marker='o',markersize=8,linestyle='None')
actual_symbol=mlines.Line2D([],[],color='black',marker='D',markersize=6,linestyle='None')
revision_symbol=mlines.Line2D([],[],color='black',marker=r'$\rightarrow$',markersize=10,linestyle='None')

handles.extend([target_symbol,actual_symbol,revision_symbol])
labels.extend(["Target","Realized","Revised target"])

legend=ax.legend(
handles,labels,
handler_map={tuple:HandlerTuple(ndivide=None)},
frameon=False,
fontsize=9,
ncol=3,
columnspacing=1.6,
handletextpad=0.8,
loc="upper left",
bbox_to_anchor=(0.01,0.99),
prop=FontProperties(family="Times New Roman",size=9)
)

# Make section headers bold
for text in legend.get_texts():
    if text.get_text() in [
    "Primary energy consumption",
    "Terminal energy consumption",
    "Primary energy generation",
    "Symbols"
    ]:
        text.set_fontweight("bold")

plt.tight_layout()
plt.show()