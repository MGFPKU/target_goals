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
make_forest_coverage_stock_plot = _load_plot_builder(
    "forest_viz",
    "Visualisation_Forest coverage rate and stock volume.py",
    "make_forest_coverage_stock_plot",
)

app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Carbon intensity", ui.output_plot("carbon_intensity_plot")),
        ui.nav_panel("Energy intensity", ui.output_plot("energy_intensity_plot")),
        ui.nav_panel("Energy mix shares", ui.output_plot("energy_mix_shares_plot")),
        ui.nav_panel("Installed power generation capacity", ui.output_plot("installed_capacity_plot")),
        ui.nav_panel("Forest stock volume", ui.output_plot("forest_stock_plot")),
        id="tab",
    )
)


def server(input, output, session):
    @render.plot(alt="Carbon intensity targets (for the whole economy)")
    def carbon_intensity_plot():
        return make_carbon_intensity_plot()

    @render.plot(alt="Energy intensity targets (for the whole economy)")
    def energy_intensity_plot():
        return make_energy_intensity_plot()

    @render.plot(alt="Energy mix shares targets and realized values")
    def energy_mix_shares_plot():
        return make_energy_mix_shares_plot()

    @render.plot(alt="Installed capacity targets, realized values, and achievement gaps")
    def installed_capacity_plot():
        return make_installed_capacity_plot()

    @render.plot(alt="Forest coverage and stock volume targets versus achieved values")
    def forest_stock_plot():
        return make_forest_coverage_stock_plot()


app = App(app_ui, server)