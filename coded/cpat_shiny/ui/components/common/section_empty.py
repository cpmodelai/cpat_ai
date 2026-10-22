from shiny import ui
from htmltools import Tag

def section_empty(
        text: str
        ) -> Tag:
    return ui.div(
        ui.h3(text),
        style="""
            text-align: center;
        """
    )
