import math
import re

import pandas as pd
import plotly.graph_objects as go

COLOR_REALIZED = "#405A79"
COLOR_TARGET = "#2F6B58"
COLOR_RANGE_FILL = "#2F6B58"
COLOR_ABS_DIAMOND = "#6F6860"
GRID_GRAY = "#9AA0A6"


def fmt_pct(val: float) -> str:
    if math.isclose(val, round(val), abs_tol=1e-9):
        return f"{int(round(val))}"
    return f"{val:.1f}".rstrip("0").rstrip(".")


def parse_pct(text: str):
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    pct = float(match.group(1)) if match else None
    lower_bound = ("more than" in text.lower()) or ("at least" in text.lower())
    return pct, lower_bound


def _carbon_inputs():
    realized = {
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
    pct_targets = [
        (2010, 2015, 17.0),
        (2015, 2020, 18.0),
        (2020, 2025, 18.0),
    ]
    range_targets = [
        (2005, 2020, 40.0, 45.0),
        (2005, 2030, 60.0, 65.0),
    ]
    return realized, pct_targets, range_targets


def _energy_inputs():
    p_1990, p_2005 = 26, 61
    rebasing_factor = p_1990 / p_2005

    abs_targets_1990 = {2010: 2.25, 2020: 1.54}
    abs_targets_2005 = {2015: 0.869}
    abs_targets_2005.update({year: value * rebasing_factor for year, value in abs_targets_1990.items()})

    realized = [
        (1990, 2.259788354),
        (1991, 2.173371973),
        (1992, 2.000539212),
        (1993, 1.866593822),
        (1994, 1.749931708),
        (1995, 1.685119423),
        (1996, 1.581419766),
        (1997, 1.451795195),
        (1998, 1.352416357),
        (1999, 1.296245710),
        (2000, 1.248716700),
        (2001, 1.220104398),
        (2002, 1.220104398),
        (2003, 1.288361987),
        (2004, 1.365151774),
        (2005, 1.390748370),
        (2006, 1.36),
        (2007, 1.29),
        (2008, 1.24),
        (2009, 1.16),
        (2010, 1.13),
        (2011, 1.112431568),
        (2012, 1.073625816),
        (2013, 1.021884813),
        (2014, 0.983079060),
        (2015, 0.931338057),
        (2016, 0.889021167),
        (2017, 0.859387129),
        (2018, 0.829753090),
        (2019, 0.814936070),
        (2020, 0.814936070),
        (2021, 0.792120979),
        (2022, 0.792120979),
    ]

    pct_targets = [
        {
            "Announcement_Year": 2007,
            "Targeted_Change": "20 percent",
            "Baseline_Year": 2005,
            "Target_Year": 2010,
        },
        {
            "Announcement_Year": 2011,
            "Targeted_Change": "16 percent",
            "Baseline_Year": 2010,
            "Target_Year": 2015,
        },
        {
            "Announcement_Year": 2016,
            "Targeted_Change": "15 percent",
            "Baseline_Year": 2015,
            "Target_Year": 2020,
        },
        {
            "Announcement_Year": 2021,
            "Targeted_Change": "13.5 percent",
            "Baseline_Year": 2020,
            "Target_Year": 2025,
        },
    ]

    return abs_targets_2005, realized, pct_targets


def _apply_layout(fig, title, xlabel, ylabel, y_values):
    fig.update_layout(
        font=dict(family="Times New Roman"),
        title=dict(text=f"<b>{title}</b>", x=0, xanchor="left", font=dict(size=14)),
        xaxis=dict(
            range=[2005, 2031],
            tickvals=[2005, 2010, 2015, 2020, 2025, 2030],
            title=dict(text=xlabel),
            showgrid=True,
            gridcolor=GRID_GRAY,
            gridwidth=0.6,
            griddash="dash",
            zeroline=False,
        ),
        yaxis=dict(
            range=[min(y_values) * 0.9, max(y_values) * 1.03],
            title=dict(text=ylabel),
            showgrid=True,
            gridcolor=GRID_GRAY,
            gridwidth=0.6,
            griddash="dash",
            zeroline=False,
        ),
        legend=dict(borderwidth=0, bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=520,
    )


def make_carbon_intensity_plot():
    realized_kg, pct_targets, range_targets = _carbon_inputs()

    years = range(2005, 2031)
    series_real = pd.Series(realized_kg, dtype="float64").reindex(years)
    series_interp = series_real.interpolate("linear")
    series_plot = series_real.dropna()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=series_plot.index.tolist(),
        y=series_plot.tolist(),
        mode="lines+markers",
        name="Realized",
        line=dict(color=COLOR_REALIZED, width=1.9),
        marker=dict(size=3.6, color=COLOR_REALIZED, line=dict(color="white", width=0.7)),
        opacity=0.9,
    ))

    first_pct = True
    for baseline, target_year, pct in pct_targets:
        baseline_value = series_interp.loc[baseline]
        if pd.isna(baseline_value):
            continue
        endpoint = baseline_value * (1 - pct / 100.0)

        fig.add_trace(go.Scatter(
            x=[baseline, target_year],
            y=[baseline_value, endpoint],
            mode="lines",
            name="5YP target" if first_pct else None,
            showlegend=first_pct,
            line=dict(color=COLOR_TARGET, width=1.4, dash="dot"),
            hoverinfo="skip",
        ))
        first_pct = False

        fig.add_trace(go.Scatter(
            x=[target_year],
            y=[endpoint],
            mode="markers",
            showlegend=False,
            marker=dict(size=6, color=COLOR_TARGET, line=dict(color="white", width=0.7)),
            hoverinfo="skip",
        ))

        mid_x = (baseline + target_year) / 2
        mid_y = (baseline_value + endpoint) / 2
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            text=f"<b>-{fmt_pct(pct)}%</b>",
            showarrow=False,
            yshift=12,
            font=dict(size=10, color=COLOR_TARGET, family="Times New Roman"),
            bgcolor="rgba(255,255,255,0.8)",
            borderpad=1,
        )

    first_range = True
    for baseline, target_year, low, high in range_targets:
        baseline_value = series_interp.loc[baseline]
        if pd.isna(baseline_value):
            continue
        endpoint_low = baseline_value * (1 - high / 100.0)
        endpoint_high = baseline_value * (1 - low / 100.0)

        fig.add_trace(go.Scatter(
            x=[baseline, target_year, target_year, baseline],
            y=[baseline_value, endpoint_high, endpoint_low, baseline_value],
            fill="toself",
            fillcolor="rgba(47, 107, 88, 0.3)",
            mode="none",
            name="Long-term range target" if first_range else None,
            showlegend=first_range,
            hoverinfo="skip",
        ))
        first_range = False

        for ep in [endpoint_low, endpoint_high]:
            fig.add_trace(go.Scatter(
                x=[baseline, target_year],
                y=[baseline_value, ep],
                mode="lines",
                showlegend=False,
                line=dict(color=COLOR_TARGET, width=1.4, dash="dot"),
                hoverinfo="skip",
            ))
            fig.add_trace(go.Scatter(
                x=[target_year],
                y=[ep],
                mode="markers",
                showlegend=False,
                marker=dict(size=5.6, color=COLOR_TARGET, line=dict(color="white", width=0.7)),
                hoverinfo="skip",
            ))

        mid_x = (baseline + target_year) / 2
        mid_y = ((baseline_value + endpoint_low) / 2 + (baseline_value + endpoint_high) / 2) / 2
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            text=f"<b>-{fmt_pct(low)}–{fmt_pct(high)}%</b>",
            showarrow=False,
            font=dict(size=10, color=COLOR_TARGET, family="Times New Roman"),
            bgcolor="rgba(255,255,255,0.8)",
            borderpad=1,
        )

    y_values = list(series_plot.values)
    for baseline, _, pct in pct_targets:
        baseline_value = series_interp.loc[baseline]
        y_values.append(baseline_value * (1 - pct / 100.0))
    for baseline, _, low, high in range_targets:
        baseline_value = series_interp.loc[baseline]
        y_values += [baseline_value * (1 - low / 100.0), baseline_value * (1 - high / 100.0)]

    _apply_layout(
        fig,
        title="Carbon intensity",
        xlabel="Year",
        ylabel="Carbon intensity (kg CO₂ per 10,000 yuan, 2005 prices)",
        y_values=y_values,
    )
    return fig


def make_energy_intensity_plot():
    abs_targets_2005, realized_e, pct_rows_e = _energy_inputs()

    series_real = (
        pd.DataFrame(realized_e, columns=["Year", "Realized_2005"])
        .set_index("Year")["Realized_2005"]
        .reindex(range(2005, 2031))
    )
    series_plot = series_real.dropna()

    df_pct = pd.DataFrame(pct_rows_e)
    df_pct[["pct", "lower_bound"]] = df_pct["Targeted_Change"].apply(lambda value: pd.Series(parse_pct(value)))
    real_map = dict(realized_e)
    df_pct["Baseline_Value_2005"] = df_pct["Baseline_Year"].map(real_map)
    df_pct["Implied_Target_Value_2005"] = df_pct["Baseline_Value_2005"] * (1 - df_pct["pct"] / 100.0)
    df_pct = df_pct.drop_duplicates(subset=["Baseline_Year", "Target_Year", "pct"]).reset_index(drop=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=series_plot.index.tolist(),
        y=series_plot.tolist(),
        mode="lines+markers",
        name="Realized",
        line=dict(color=COLOR_REALIZED, width=1.9),
        marker=dict(size=3.6, color=COLOR_REALIZED, line=dict(color="white", width=0.7)),
        opacity=0.9,
    ))

    first_pct = True
    for _, row in df_pct.iterrows():
        x0 = int(row["Baseline_Year"])
        y0 = float(row["Baseline_Value_2005"])
        x1 = int(row["Target_Year"])
        y1 = float(row["Implied_Target_Value_2005"])

        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="lines",
            name="Percentage targets" if first_pct else None,
            showlegend=first_pct,
            line=dict(color=COLOR_TARGET, width=1.4, dash="dot"),
            hoverinfo="skip",
        ))
        first_pct = False

        fig.add_trace(go.Scatter(
            x=[x1],
            y=[y1],
            mode="markers",
            showlegend=False,
            marker=dict(size=5.6, color=COLOR_TARGET, line=dict(color="white", width=0.7)),
            hoverinfo="skip",
        ))

        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        label = f"-{fmt_pct(float(row['pct']))}%"
        if row["lower_bound"]:
            label = "≥" + label
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            text=f"<b>{label}</b>",
            showarrow=False,
            yshift=12,
            font=dict(size=10, color=COLOR_TARGET, family="Times New Roman"),
            bgcolor="rgba(255,255,255,0.8)",
            borderpad=1,
        )

    abs_years = sorted(abs_targets_2005)
    abs_values = [abs_targets_2005[year] for year in abs_years]
    fig.add_trace(go.Scatter(
        x=abs_years,
        y=abs_values,
        mode="markers",
        name="Absolute targets",
        marker=dict(
            symbol="diamond",
            size=8,
            color=COLOR_ABS_DIAMOND,
            line=dict(color="white", width=0.8),
        ),
    ))
    for year, value in zip(abs_years, abs_values):
        fig.add_annotation(
            x=year,
            y=value,
            text=f"<b>{value:.2f}</b>",
            showarrow=False,
            yshift=-14,
            font=dict(size=9, color=COLOR_ABS_DIAMOND, family="Times New Roman"),
        )

    y_values = list(series_plot.values) + abs_values + df_pct["Implied_Target_Value_2005"].tolist()

    _apply_layout(
        fig,
        title="Energy intensity",
        xlabel="Year",
        ylabel="Energy intensity (tce per 10,000 yuan, 2005 prices)",
        y_values=y_values,
    )
    return fig


if __name__ == "__main__":
    make_carbon_intensity_plot().show()
    make_energy_intensity_plot().show()
