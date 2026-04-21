import importlib.util
from pathlib import Path

from shiny import App, render, ui


def _load_plot_builder(module_name, script_name, function_name):
    script_path = Path(__file__).with_name(script_name)
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


make_absolute_target_plot = _load_plot_builder(
    "absolute_target_viz",
    "Visualisation_Absolute Target.py",
    "make_absolute_target_plot",
)
make_carbon_intensity_plot = _load_plot_builder(
    "carbon_energy_viz",
    "Visualisation_Carbon and Energy Intensity.py",
    "make_carbon_intensity_plot",
)
make_energy_intensity_plot = _load_plot_builder(
    "carbon_energy_viz",
    "Visualisation_Carbon and Energy Intensity.py",
    "make_energy_intensity_plot",
)
make_energy_mix_shares_plot = _load_plot_builder(
    "energy_shares_viz",
    "Visualisation_Energy Shares3.py",
    "make_energy_mix_shares_plot",
)
make_installed_capacity_plot = _load_plot_builder(
    "installed_capacity_viz",
    "Visualisation_Installed Capacity2.py",
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
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        .nav-tabs .nav-link {
            color: #4B7C6A !important;
        }

        .nav-tabs .nav-link.active {
            color: #000000 !important;
        }
        """
    ),
    ui.navset_tab(
        ui.nav_panel(
            "Carbon intensity",
            ui.div(
                ui.output_plot("carbon_intensity_plot", width="100%", height="460px"),
                class_="plot-shell",
            ),
            ui.p(
                "Note: Realised carbon intensity is defined as CO₂ emissions from fuel combustion—sourced from China’s Biennial Update Reports and Biennial Transparency Reports on Climate Change—divided by real GDP at 2020 prices, as reported in China’s Statistical Yearbook. Where necessary, values are extended using officially reported carbon intensity reduction rates from China’s Annual Statistical Communiqués. China’s official carbon intensity targets cover CO₂ emissions from fuel combustion and selected industrial processes. Due to data constraints, the series presented here includes only CO₂ emissions from fuel combustion which, in 2021, accounted for approximately 96% of the total CO₂ emissions included in China’s carbon intensity indicator. Including CO₂ emissions from selected industrial processes would elevate the carbon intensity reduction levels slightly, for example by around 0.4% in 2021."
            ),
            ui.p(
                "Source: Target data is from the Target Tracker; the realized data is from official Chinese policy documents and national statistics."
            ),
        ),
        ui.nav_panel(
            "Energy intensity",
            ui.div(
                ui.output_plot("energy_intensity_plot", width="100%", height="460px"),
                class_="plot-shell",
            ),
            ui.p(
                "Source: Target data is from the Target Tracker; the realized data is from official Chinese policy documents and national statistics."
            ),
        ),
        ui.nav_panel(
            "Absolute target",
            ui.div(
                ui.output_plot("absolute_target_plot", width="100%", height="460px"),
                class_="plot-shell",
            ),
            ui.p("Source: China's 2035 National Determined Contributions."),
        ),
        ui.nav_panel(
            "Energy mix shares",
            ui.div(
                ui.output_plot("energy_mix_shares_plot", width="100%", height="560px"),
                class_="plot-shell",
            ),
            ui.p(
                "Note: Non-fossil refers to the energy consumption from hydropower, nuclear power, wind power, solar power, biomass energy, and geothermal energy."
            ),
            ui.p(
                "Source: Target data is from the Target Tracker; the realized data is from official Chinese policy documents and national statistics."
            ),
        ),
        ui.nav_panel(
            "Installed power generation capacity",
            ui.div(
                ui.output_plot("installed_capacity_plot", width="100%", height="620px"),
                class_="plot-shell",
            ),
            ui.p(
                "Source: Target data is from the Target Tracker; the realized data is from the National Energy Administration and China Electricity Council."
            ),
        ),
        ui.nav_panel(
            "Forest stock volume",
            ui.div(
                ui.output_plot("forest_stock_plot", width="100%", height="430px"),
                class_="plot-shell",
            ),
            ui.p(
                "Source: Target data is from the Target Tracker; the realized data is from official Chinese forestry statistics and sector reports."
            ),
        ),
        id="tab",
        selected="Energy intensity",
    ),
)


def server(input, output, session):
    @render.plot(alt="China's first absolute carbon emissions reduction target")
    def absolute_target_plot():
        return make_absolute_target_plot()

    @render.plot(alt="Carbon intensity targets (for the whole economy)")
    def carbon_intensity_plot():
        return make_carbon_intensity_plot()

    @render.plot(alt="Energy intensity targets (for the whole economy)")
    def energy_intensity_plot():
        return make_energy_intensity_plot()

    @render.plot(alt="Energy mix shares targets and realized values")
    def energy_mix_shares_plot():
        return make_energy_mix_shares_plot()

    @render.plot(
        alt="Installed capacity targets, realized values, and achievement gaps"
    )
    def installed_capacity_plot():
        return make_installed_capacity_plot()

    @render.plot(alt="Forest stock volume targets versus achieved values")
    def forest_stock_plot():
        return make_forest_stock_plot()


app = App(app_ui, server)
