from shiny import ui
from htmltools import Tag

def results_section_card(
        *elements
        ) -> Tag:
    return ui.card(
        ui.layout_columns(
            *elements,
            col_widths=(
                12,
                12,
                12
            ),
        ),
        height='320px'
    ),
