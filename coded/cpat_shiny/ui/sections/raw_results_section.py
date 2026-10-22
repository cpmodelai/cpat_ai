from typing import Dict

import pandas as pd

from shiny import ui
from shiny.reactive._reactives import Value
from htmltools import Tag

from cpat_shiny.ui.components.common.multiple_selectize import multiple_selectize
from cpat_shiny.ui.components.common.section_empty import section_empty
from cpat_shiny.ui.components.common.validation_output import validation_output
from cpat_shiny.ui.components.common.results_section_card import results_section_card
from cpat_shiny.ui.components.common.height_wrapper import height_wrapper

from cpat_shiny.mapping import CPAT_VARIABLES

from cpat_shiny.ui.labels import RESULTS

from cpat_model.constants import ID_COL_NAMES

FIRST_VAR = list(CPAT_VARIABLES.keys())[0]
EMPTY_RESULTS_CHOICES = {FIRST_VAR: ' '}

def download_btn(
        raw_results: Dict[str, pd.DataFrame]
        ) -> Tag:
    if raw_results:
        return (
            ui.download_button("save_raw_results", RESULTS["downloadResults"])
        )
    return (
        ui.download_button("save_raw_results_blocked", RESULTS["downloadResults"])
    )


def get_var_selection_choices(
        raw_results: Dict[str, pd.DataFrame]
        ) -> Dict[str, str]:
    if raw_results:
        return {k: v for k, v in CPAT_VARIABLES.items() if k in raw_results}
    return EMPTY_RESULTS_CHOICES

def get_filter_choices(
        raw_results: Dict[str, pd.DataFrame] 
        ) -> Dict[str, Dict[str, str]]:
    if raw_results:
        choices = {
            code: {
                unique_code: unique_code
                for unique_code in
                raw_results[FIRST_VAR].index.get_level_values(code).unique()
            }
            for code in [*ID_COL_NAMES, 'ScenarioName']
        }
        return choices
    choices = {code: EMPTY_RESULTS_CHOICES for code in [*ID_COL_NAMES, 'ScenarioName']}
    return choices

def raw_results_section(
        results_inputs_selection: Value,
        global_raw_results: Value
        ) -> Tag:
    filter_choices = get_filter_choices(global_raw_results())
    return ui.div(
        ui.layout_columns(
            results_section_card(
                multiple_selectize({
                    'id': "vars_to_save_input",
                    'label': RESULTS["selectVariables"],
                    'choices': {"All": {"all": "All variables"}, "Sectors": CPAT_VARIABLES},
                    'selected': list(results_inputs_selection()['vars_to_save_input'])
                }),
                ui.input_action_button("extract_vars_raw_results", RESULTS["extractVariables"]),
                validation_output("validation_raw_results_vars_message_output"),
            ),
            results_section_card(
                height_wrapper(
                    ui.input_text(
                        id="raw_results_file_name_input",
                        label=RESULTS["resultsFileName"],
                        value=results_inputs_selection()['raw_results_file_name_input'],
                        width='100%'
                    ),
                    height=121.7
                ),
                download_btn(global_raw_results()),
                validation_output("validation_raw_results_file_message_output"),
            ),
            ui.input_selectize(
                id="raw_results_df_selection",
                label=RESULTS["rawResultsDfSelection"],
                choices=get_var_selection_choices(global_raw_results()),
                selected=results_inputs_selection()['raw_results_df_selection'],
                width='100%'
            ),
            ui.div(),
            multiple_selectize({
                'id': "raw_results_country_code",
                'label': RESULTS["rawResultsCountryCode"],
                'choices': filter_choices['CountryCode'],
                'selected': list(results_inputs_selection()['raw_results_country_code'])
            }),
            multiple_selectize({
                'id': "raw_results_sector_code",
                'label': RESULTS["rawResultsSectorCode"],
                'choices': filter_choices['SectorCode'],
                'selected': list(results_inputs_selection()['raw_results_sector_code'])
            }),
            multiple_selectize({
                'id': "raw_results_fuel_code",
                'label': RESULTS["rawResultsFuelCode"],
                'choices': filter_choices['FuelCode'],
                'selected': list(results_inputs_selection()['raw_results_fuel_code'])
            }),
            multiple_selectize({
                'id': "raw_results_scenario_name",
                'label': RESULTS["rawResultsScenarioName"],
                'choices': filter_choices['ScenarioName'],
                'selected': list(results_inputs_selection()['raw_results_scenario_name'])
            }),
            ui.input_action_button(
                "rerender_raw_results_df",
                RESULTS["applyFilters"],
                style="""
                    margin-top: 32px;
                """
            ),
            ui.output_data_frame("raw_results_df"),
            col_widths=(
                6, 6,
                6, 6,
                2, 2, 2, 2, 4,
                12
            ),
        ),
    )
raw_results_section_empty = section_empty(RESULTS["resultsEmpty"])
