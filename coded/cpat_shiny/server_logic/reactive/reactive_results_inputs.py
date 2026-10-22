from shiny import reactive
import pandas as pd

from cpat_shiny.server_logic.apply_results_filters import apply_results_filters
from cpat_shiny.validation.results_inputs import ResultsInputsValidation

from cpat_shiny.mapping import CPAT_VARIABLES, ALL_INDICATORS, AIR_POLLUTION_VARIABLES, AP_INDICATORS

results_inputs_selection = reactive.value({
    "vars_to_save_input": (),
    "indicators_input": (),
    "raw_results_file_name_input": 'raw_result',
    "indicators_file_name_input": 'indicators',

    "raw_results_df_selection": list(CPAT_VARIABLES.keys())[0],

    "raw_results_country_code": (),
    "raw_results_sector_code": (),
    "raw_results_fuel_code": (),
    "raw_results_scenario_name": (),

    "indicators_cpat_code": '',
    "indicators_unit": (),
    "indicators_header": (),
})


validation_text_raw_results_vars = reactive.value("")
validation_text_raw_results_file = reactive.value("")

validation_text_indicators_selection = reactive.value("")
validation_text_indicators_file = reactive.value("")

global_raw_results = reactive.value({})

df_raw_results_to_render = reactive.value(pd.DataFrame())
df_indicators_to_render = reactive.value(pd.DataFrame())

def create_update_vars_to_save(inputs, session):
    @reactive.effect
    @reactive.event(inputs.vars_to_save_input)
    def _():
        selected = inputs.vars_to_save_input()
        if "all" in selected:
            session.send_input_message("vars_to_save_input", {"value": list(CPAT_VARIABLES.keys())})
        current_selection = results_inputs_selection.get()
        current_selection['vars_to_save_input'] = inputs.vars_to_save_input()
        results_inputs_selection.set(current_selection)

def create_update_indicators_to_calc(inputs, session):
    @reactive.effect
    @reactive.event(inputs.indicators_input)
    def _():
        selected = inputs.indicators_input()
        if "all" in selected:
            session.send_input_message("indicators_input", {"value": list(ALL_INDICATORS.keys())})
        current_selection = results_inputs_selection.get()
        current_selection['indicators_input'] = inputs.indicators_input()
        results_inputs_selection.set(current_selection)

def create_update_raw_results_file_name(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_file_name_input)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_file_name_input'] = inputs.raw_results_file_name_input()
        results_inputs_selection.set(current_selection)


def create_update_indicators_file_name(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_file_name_input)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['indicators_file_name_input'] = inputs.indicators_file_name_input()
        results_inputs_selection.set(current_selection)

def create_update_validation_text_raw_results_vars(inputs):
    @reactive.effect
    @reactive.event(inputs.vars_to_save_input)
    def _():
        validation_text_raw_results_vars.set('')
        ResultsInputsValidation.validate_raw_results_vars_to_save(
            inputs, validation_text_raw_results_vars
        )

def create_update_validation_text_raw_results_file(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_file_name_input)
    def _():
        validation_text_raw_results_file.set('')
        ResultsInputsValidation.validate_raw_results_file_name(
            inputs, validation_text_raw_results_file
        )

def create_update_validation_text_indicators_selection(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_input)
    def _():
        validation_text_indicators_selection.set('')
        ResultsInputsValidation.validate_indicators_to_save(
            inputs, validation_text_indicators_selection
        )

def create_update_validation_text_indicators_file(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_file_name_input)
    def _():
        validation_text_indicators_file.set('')
        ResultsInputsValidation.validate_indicators_file_name(
            inputs, validation_text_indicators_file
        )

def create_update_raw_results_df_selection(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_df_selection)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_df_selection'] = inputs.raw_results_df_selection()
        results_inputs_selection.set(current_selection)
        apply_results_filters(global_raw_results, inputs, df_raw_results_to_render)

def create_update_raw_results_country_code(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_country_code)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_country_code'] = inputs.raw_results_country_code()
        results_inputs_selection.set(current_selection)

def create_update_raw_results_sector_code(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_sector_code)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_sector_code'] = inputs.raw_results_sector_code()
        results_inputs_selection.set(current_selection)

def create_update_raw_results_fuel_code(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_fuel_code)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_fuel_code'] = inputs.raw_results_fuel_code()
        results_inputs_selection.set(current_selection)

def create_update_raw_results_scenario_name(inputs):
    @reactive.effect
    @reactive.event(inputs.raw_results_scenario_name)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['raw_results_scenario_name'] = inputs.raw_results_scenario_name()
        results_inputs_selection.set(current_selection)

def create_update_indicators_cpat_code(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_cpat_code)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['indicators_cpat_code'] = inputs.indicators_cpat_code()
        results_inputs_selection.set(current_selection)

def create_update_indicators_unit(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_unit)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['indicators_unit'] = inputs.indicators_unit()
        results_inputs_selection.set(current_selection)

def create_update_indicators_header(inputs):
    @reactive.effect
    @reactive.event(inputs.indicators_header)
    def _():
        current_selection = results_inputs_selection.get()
        current_selection['indicators_header'] = inputs.indicators_header()
        results_inputs_selection.set(current_selection)
