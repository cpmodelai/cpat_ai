from shiny import ui

from cpat_shiny.ui.css.head import GLOBAL_CSS
from cpat_shiny.ui.labels import PAGE

mitigation_page = ui.page_sidebar(
    ui.sidebar(
        ui.h2(PAGE["CPATPython"]),
        ui.input_radio_buttons(
            id="section_selector",
            label=PAGE["selectSection"],
            choices={
                "input-section": PAGE["manualInputs"],
                "scenarios-section": PAGE["scenarios"],
                "raw-results-section": PAGE["rawResults"],
                "indicators-section": PAGE['indicators'],
                "visualizations-section": PAGE["visualizations"],
                "documentation-section": PAGE['documentation']
            }
        )
    ),
    # render page content
    ui.output_ui("page_content"),
)

app_ui = ui.page_navbar(
    ui.head_content(
        ui.tags.style(GLOBAL_CSS),
    ),
    ui.nav_panel(PAGE["CPATPython"], mitigation_page),
    ui.nav_panel("Other tool", "Other tool content"),
    title=PAGE["tools"],
    id="main_page",
)
