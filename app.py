import importlib.util
from pathlib import Path

from shiny import App, render, ui


def _load_plot_builders():
    script_path = Path(__file__).with_name("Visualisation_Carbon and Energy Intensity.py")
    spec = importlib.util.spec_from_file_location("carbon_energy_viz", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_carbon_intensity_plot, module.make_energy_intensity_plot


make_carbon_intensity_plot, make_energy_intensity_plot = _load_plot_builders()

app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Carbon intensity", ui.output_plot("carbon_intensity_plot")),
        ui.nav_panel("Energy intensity", ui.output_plot("energy_intensity_plot")),
        ui.nav_panel("Energy mix shares", "Panel C content"),
        ui.nav_panel("Installed power generation capacity", "Panel D content"),
        ui.nav_panel("Forest stock volume", "Panel E content"),
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


app = App(app_ui, server)