from typing import Dict, Optional

import pandas as pd
from shiny import ui
from shiny.reactive._reactives import Value
from htmltools import Tag

from cpat_shiny.ui.components.common.multiple_selectize import multiple_selectize
from cpat_shiny.ui.components.common.section_empty import section_empty
from cpat_shiny.ui.components.common.validation_output import validation_output
from cpat_shiny.ui.components.common.results_section_card import results_section_card
from cpat_shiny.ui.components.common.height_wrapper import height_wrapper

from cpat_shiny.mapping import ALL_INDICATORS

from cpat_shiny.ui.labels import RESULTS

def download_indicators_btn(
        indicators: Optional[pd.DataFrame]
        ) -> Tag:
    if indicators is not None:
        return (
            ui.download_button("download_indicators", RESULTS["downloadIndicators"])
        )
    return (
        ui.download_button("download_indicators_blocked", RESULTS["downloadIndicators"])
    )

def get_filter_choices(
        indicators: Optional[pd.DataFrame]
        ) -> Dict[str, Dict[str, str]]:
    col_names = ['Unit', 'Indicator header']
    if indicators is not None:
        choices = {
            code: {
                unique_code: unique_code
                for unique_code in
                indicators[code].unique()
            }
            for code in col_names
        }
        return choices
    choices = {code: {'a': ' '} for code in col_names} #TODO change a
    return choices

def indicators_section(
        results_inputs_selection: Value,
        indicators: Value
        ) -> Tag:
    filter_choices = get_filter_choices(indicators())
    return ui.div(
        ui.layout_columns(
            results_section_card(
                multiple_selectize({
                    'id': "indicators_input",
                    'label': RESULTS["selectIndicators"],
                    'choices': {"All": {"all": "All indicators"}, "Indicators": ALL_INDICATORS},
                    'selected': list(results_inputs_selection()['indicators_input'])
                }),
                ui.input_action_button("create_indicators", RESULTS["createIndicators"]),
                validation_output("validation_indicators_selection_message_output"),
            ),
            results_section_card(
                height_wrapper(
                    ui.input_text(
                        id="indicators_file_name_input",
                        label=RESULTS["indicatorsFileName"],
                        value=results_inputs_selection()['indicators_file_name_input'],
                        width='100%'
                    ),
                    height=121.7
                ),
                download_indicators_btn(indicators()),
                validation_output("validation_indicators_file_message_output"),
            ),
            ui.input_text(
                id="indicators_cpat_code",
                label=RESULTS["indicatorsCpatCode"],
                value=results_inputs_selection()['indicators_cpat_code'],
                width='100%'
            ),
            multiple_selectize({
                'id': "indicators_unit",
                'label': RESULTS["indicatorsUnit"],
                'choices': filter_choices['Unit'],
                'selected': list(results_inputs_selection()['indicators_unit'])
            }),
            multiple_selectize({
                'id': "indicators_header",
                'label': RESULTS["indicatorsHeader"],
                'choices': filter_choices['Indicator header'],
                'selected': list(results_inputs_selection()['indicators_header'])
            }),
            ui.input_action_button(
                "rerender_indicators_df",
                RESULTS["applyFilters"],
                style="""
                    margin-top: 32px;
                """
            ),
            ui.output_data_frame("indicators_df"),
            col_widths=(
                6, 6,
                3, 3, 3, 3,
                12
            ),
        ),
    )

indicators_section_empty = section_empty(RESULTS["resultsEmpty"])
