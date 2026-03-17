from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Carbon intensity", "Panel A content"),
        ui.nav_panel("Energy intensity", "Panel B content"),
        ui.nav_panel("Energy mix shares", "Panel C content"),
        ui.nav_panel("Installed power generation capacity", "Panel D content"),
        ui.nav_panel("Forest stock volume", "Panel E content"),
        id="tab",
    )
)

def server(input, output, session):
    pass

app = App(app_ui, server)