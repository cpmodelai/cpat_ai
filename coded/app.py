from shiny import App

from cpat_shiny.ui.ui import app_ui
from cpat_shiny.server_logic.server import server

app = App(app_ui, server)
