from typing import Dict, List

from shiny import ui
from htmltools import Tag
from shinywidgets import output_widget

from cpat_shiny.mapping import ALL_COUNTRIES

from cpat_shiny.ui.components.common.section_empty import section_empty
from cpat_shiny.ui.labels import VISUALIZATIONS



def visualizations_section(
        graph_selection: Dict[str, str],
        selected_countries: List[str],
        scenarios_names: List[str]
        ) -> Tag:
    countries = {k: v for k, v in ALL_COUNTRIES.items() if k in selected_countries}
    scenarios = {s:s for s in scenarios_names}
    return ui.div(
        ui.layout_columns(
            ui.input_selectize(
                id="country_visualization",
                label=VISUALIZATIONS["selectedCountry"],
                choices=countries,
                selected=graph_selection['country_visualization']
            ),
            ui.input_selectize(
                id="scenario_visualization",
                label=VISUALIZATIONS["selectedScenario"],
                choices=scenarios,
                selected=graph_selection['scenario_visualization']
            ),
            col_widths=(6, 6),
            fill=False
        ),
        ui.hr(),
        output_widget("plot_ec_by_sector"),
        ui.hr(),
        output_widget("plot_ec_by_fuel"),
        ui.hr(),
        output_widget("plot_ec_change_by_fuel"),
        ui.hr(),
        output_widget("plot_domestic_p"),
        ui.hr(),
        output_widget("plot_em_by_sector"),
        ui.hr(),
        output_widget("plot_distribution")
    )

visualizations_section_empty = section_empty(VISUALIZATIONS["visualizationsEmpty"])
