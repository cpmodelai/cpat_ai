from shiny import ui
from htmltools import Tag

from cpat_shiny.ui.components.common.height_wrapper import height_wrapper

def validation_output(
        render_id: str
        ) -> Tag:
    return height_wrapper(
        ui.output_ui(render_id),
        height=48
    )
