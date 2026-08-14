import importlib.util
import os
from pathlib import Path

import matplotlib as mpl
from shiny import App, reactive, render, ui

from i18n import i18n, get_font_family, set_language


def _load_plot_builder(module_name, script_name, function_name):
    script_path = Path(__file__).with_name(script_name)
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


make_carbon_intensity_plot = _load_plot_builder(
    "annual_carbon_intensity_viz",
    "Visualisation_Annual Carbon Intensity Reductions.py",
    "make_carbon_intensity_plot",
)
make_energy_intensity_plot = _load_plot_builder(
    "annual_energy_intensity_viz",
    "Visualisation_Annual Energy Intensity Reductions.py",
    "make_energy_intensity_plot",
)
make_energy_mix_shares_plot = _load_plot_builder(
    "energy_shares_viz",
    "Visualisation_Energy Shares.py",
    "make_energy_mix_shares_plot",
)
make_installed_capacity_plot = _load_plot_builder(
    "installed_capacity_viz",
    "Visualisation_Installed Capacity.py",
    "make_installed_capacity_plot",
)
make_forest_stock_plot = _load_plot_builder(
    "forest_viz",
    "Visualisation_Forest coverage rate and stock volume.py",
    "make_forest_stock_plot",
)

app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .plot-shell {
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }
        .nav-tabs .nav-link {
            color: #4B7C6A !important;
        }

        .nav-tabs .nav-link.active {
            color: #000000 !important;
        }

        /* Center the entire app content */
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Microsoft YaHei',
                '微软雅黑', 'PingFang SC', 'STHeiti', SimHei,
                'Noto Sans SC', 'Noto Sans CJK SC',
                Arial, Helvetica, sans-serif;
        }

        .container-fluid {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        """
    ),
    ui.output_ui("tabset"),
)


def server(input, output, session):

    @reactive.calc
    def lang():
        query = session.clientdata.url_search()
        params = {}
        if query.startswith("?"):
            query = query[1:]
        for pair in query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
        # Query param takes precedence; fall back to env var; ultimate default EN
        return params.get("lang") or os.getenv("LANGUAGE", "EN")

    @render.ui
    def tabset():
        set_language(lang())
        return ui.navset_tab(
            ui.nav_panel(
                i18n("Carbon intensity"),
                ui.div(
                    ui.output_plot("carbon_intensity_plot", width="100%", height="460px"),
                    class_="plot-shell",
                ),
                ui.div(
                    ui.p(
                        i18n("Note: Data are shown only for years in which they were reported in official sources.")
                    ),
                    ui.p(
                        i18n("Sources: Target data is from the Target Tracker; realised data from Statistical Communiques of the PRC, State Council Reports on the Work of the Government, Reports on the Implementation of the Plans for Economic and Social Development, and China's Policies and Actions on Climate Change Annual Reports.")
                    ),
                    class_="plot-shell",
                ),
            ),
            ui.nav_panel(
                i18n("Energy intensity"),
                ui.div(
                    ui.output_plot("energy_intensity_plot", width="100%", height="460px"),
                    class_="plot-shell",
                ),
                ui.div(
                    ui.p(
                        i18n("Note: Data are shown only for years in which they were reported in official sources.")
                    ),
                    ui.p(
                        i18n("Sources: Target data is from the Target Tracker; realised data from Statistical Communiques of the PRC, State Council Reports on the Work of the Government, Reports on the Implementation of the Plans for Economic and Social Development, and China's Policies and Actions on Climate Change Annual Reports.")
                    ),
                    class_="plot-shell",
                ),
            ),
            ui.nav_panel(
                i18n("Energy mix shares"),
                ui.div(
                    ui.output_plot("energy_mix_shares_plot", width="100%", height="500px"),
                    class_="plot-shell",
                ),
                ui.div(
                    ui.p(
                        i18n("Note: Data are shown only for years in which they were reported in official sources. Non-fossil refers to the energy consumption from hydropower, nuclear power, wind power, solar power, biomass energy, and geothermal energy.")
                    ),
                    ui.p(
                        i18n("Source: Target data is from the Target Tracker; the realized data is from official Chinese policy documents and national statistics.")
                    ),
                    class_="plot-shell",
                ),
            ),
            ui.nav_panel(
                i18n("Installed power generation capacity"),
                ui.div(
                    ui.output_plot("installed_capacity_plot", width="1000px", height="620px"),
                    class_="plot-shell",
                ),
                ui.div(
                    ui.p(
                        i18n("Note: Installed capacity refers to the total power output of all power generation units at rated conditions. Coal- and gas-fired capacity targets are combined as a thermal power target for comparison with realised data.")
                    ),
                    ui.p(
                        i18n("Source: Target data is from the Target Tracker; the realized data is from the National Energy Administration and China Electricity Council.")
                    ),
                    class_="plot-shell",
                ),
            ),
            ui.nav_panel(
                i18n("Forest stock volume"),
                ui.div(
                    ui.output_plot("forest_stock_plot", width="100%", height="430px"),
                    class_="plot-shell",
                ),
                ui.div(
                    ui.p(
                        i18n("Note: Forest stock volume refers to the total trunk volume of all trees in the forest.")
                    ),
                    ui.p(
                        i18n("Source: Target data is from the Target Tracker; the realized data is from official Chinese forestry statistics and sector reports.")
                    ),
                    class_="plot-shell",
                ),
            ),
            id="tab",
            selected=i18n("Energy intensity"),
        )

    @render.plot(alt=i18n("Annual carbon intensity reductions"))
    def carbon_intensity_plot():
        set_language(lang())
        mpl.rcParams["font.family"] = get_font_family()
        return make_carbon_intensity_plot()

    @render.plot(alt=i18n("Annual energy intensity reductions"))
    def energy_intensity_plot():
        set_language(lang())
        mpl.rcParams["font.family"] = get_font_family()
        return make_energy_intensity_plot()

    @render.plot(alt=i18n("Energy mix shares targets and realized values"))
    def energy_mix_shares_plot():
        set_language(lang())
        mpl.rcParams["font.family"] = get_font_family()
        return make_energy_mix_shares_plot()

    @render.plot(
        alt=i18n("Installed capacity targets, realized values, and achievement gaps")
    )
    def installed_capacity_plot():
        set_language(lang())
        mpl.rcParams["font.family"] = get_font_family()
        return make_installed_capacity_plot()

    @render.plot(alt=i18n("Forest stock volume targets versus achieved values"))
    def forest_stock_plot():
        set_language(lang())
        mpl.rcParams["font.family"] = get_font_family()
        return make_forest_stock_plot()


app = App(app_ui, server)
