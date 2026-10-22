from shiny import ui
from htmltools import Tag

DEFAULT_MARGIN_CSS = """
            color: red;
            font-weight: bold;
            width: 100%;
            text-align: center;
        """

NEGATIVE_MARGIN_CSS = DEFAULT_MARGIN_CSS + """
            margin-top: -20px;
        """


def validation_message(
        validation_text: str,
        negative_margin: bool = True
        ) -> Tag:
    return ui.div(
        validation_text,
        style = NEGATIVE_MARGIN_CSS if negative_margin else DEFAULT_MARGIN_CSS
    )
