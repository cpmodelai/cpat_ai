from typing import Dict, Union, Tuple

from shiny import ui
from htmltools import Tag

from cpat_shiny.ui.components.common.multiple_selectize import multiple_selectize

from cpat_shiny.mapping import ALL_COUNTRIES, ALL_FUELS, ALL_SECTORS, CT_AFTER_TARGET_YEAR, PRICES_SELECTION
from cpat_shiny.ui.labels import COMMON


def input_section(
        input_selection: Dict[str, Union[str, int, float, Tuple[str]]]
        ) -> Tag:
    return ui.div(
        ui.layout_columns(
            ui.input_text(
                id="scenario_name_input",
                label=COMMON["scenarioName"],
                value=input_selection['scenario_name_input'],
                width='100%'
            ),
            ui.div(), # space placeholder
            multiple_selectize({
                'id': "countries_input",
                'label': COMMON["selectCountries"],
                'choices': ALL_COUNTRIES,
                'selected': list(input_selection['countries_input'])
            }),
            ui.div(), # space placeholder
            ui.layout_columns(
                ui.input_numeric(
                    id="start_year",
                    label=COMMON["startCTYear"],
                    value=input_selection['start_year'],
                    min=2024,
                    max=2050,
                    step=1,
                    width='100%'
                ),
                ui.input_numeric(
                    id="target_year",
                    label=COMMON["targetCTYear"],
                    value=input_selection['target_year'],
                    min=2024,
                    max=2050,
                    step=1,
                    width='100%'
                ),
                ui.input_numeric(
                    id="start_level",
                    label=COMMON["startCTLevel"],
                    value=input_selection['start_level'],
                    min=0,
                    max=100,
                    step=0.5,
                    width='100%'
                ),
                ui.input_numeric(
                    id="target_level",
                    label=COMMON["targetCTLevel"],
                    value=input_selection['target_level'],
                    min=0,
                    max=100,
                    step=0.5,
                    width='100%'
                ),
                col_widths=(3, 3, 3, 3),
                fill=False
            ),
            ui.layout_columns(
                ui.div(
                    ui.input_selectize(
                        id="ct_projection",
                        label=COMMON["afterTargetCT"],
                        choices=CT_AFTER_TARGET_YEAR,
                        selected=input_selection['ct_projection'],
                        width='100%'
                    ),
                ),
                ui.div(
                    ui.input_selectize(
                        id="prices_source_selection",
                        label=COMMON["pricesSourceSelection"],
                        choices=PRICES_SELECTION,
                        selected=input_selection['prices_source_selection'],
                        width='100%'
                    ),
                ),
                col_widths=(6, 6),
                fill=False
            ),
            multiple_selectize({
                'id': "fuels_input",
                'label': COMMON["selectFuels"],
                'choices': {"All": {"all": "All fuels"}, "Fuels": ALL_FUELS},
                'selected': list(input_selection['fuels_input'])
                }),
            multiple_selectize({
                'id': "sectors_input",
                'label': COMMON["selectSectors"],
                'choices': {"All": {"all": "All sectors"}, "Sectors": ALL_SECTORS},
                'selected': list(input_selection['sectors_input'])
            }),
            ui.input_action_button("add_scenario_btn", COMMON["addScenario"]),
            ui.output_ui("validation_message_output"),
            # making the page scrollable at render for multi.selectize-dropdown
            ui.div({"style": "height: 60px;"}),
            col_widths=(
                6, 6,
                6, 6,
                12,
                12,
                6, 6,
                12,
                12,
                12
            ),
            fill=False
        ),
    )
