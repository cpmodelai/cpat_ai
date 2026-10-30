from shiny import ui
from htmltools import Tag

def height_wrapper(
        *elements,
        height: int
        ) -> Tag:
    return ui.div(
        *elements,
        style=f"""
            height: {height}px;
        """
    )
