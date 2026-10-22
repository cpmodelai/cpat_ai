from typing import Union, List, Dict, Tuple

import pandas as pd
from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.validation.manual_inputs import ManualInputsValidation

from cpat_shiny.ui.components.common.notifications import success_notification
from cpat_shiny.ui.labels import SERVER

def load_scenario_name(
        inputs: Inputs,
        validation_message: Value,
        df_scenarios: pd.DataFrame
        ) -> Dict[str, str]:
    ManualInputsValidation.validate_scenario_name(inputs, validation_message, df_scenarios)
    scenario_name = {'ScenarioName': [inputs.scenario_name_input()]}
    return scenario_name

def load_countries(
        inputs: Inputs,
        validation_message: Value,
        df_scenarios: pd.DataFrame
        ) -> Dict[str, Tuple[str]]:
    ManualInputsValidation.validate_countries(inputs, validation_message, df_scenarios)
    countries = {'SelectedCountries': [inputs.countries_input()]}
    return countries

def load_ct_inputs(
        inputs: Inputs,
        validation_message: Value
        ) -> Dict[str, Union[int, str]]:
    ManualInputsValidation.validate_ct_inputs(inputs, validation_message)
    ct_inputs = {
        'CTintroYear': [inputs.start_year()],
        'CTtargetYear': [inputs.target_year()],
        'CTintroValue': [inputs.start_level()],
        'CTtargetValue': [inputs.target_level()],
        'CTLinearProjection': [inputs.ct_projection()]
    }
    return ct_inputs

def load_prices_source(
        inputs: Inputs,
        validation_message: Value
        ) -> Dict[str, str]:
    ManualInputsValidation.validate_prices_selection(inputs, validation_message)
    prices_source = {'IntPricesSource': [inputs.prices_source_selection()]}
    return prices_source

def load_fuels_and_sectors(
        inputs: Inputs
        ) -> Dict[str, Tuple[str]]:
    fuels_and_sectors = {
        'SelectedFuels': [inputs.fuels_input()],
        'SelectedSectors': [inputs.sectors_input()],
    }
    return fuels_and_sectors


def load_scenario_data(
        inputs: Inputs,
        validation_message: Value,
        df_scenarios: pd.DataFrame
        ) -> Dict[str, Union[List[str], str, int]]:
    scenario_inputs = {
        **load_scenario_name(inputs, validation_message, df_scenarios),
        **load_countries(inputs, validation_message, df_scenarios),
        **load_ct_inputs(inputs, validation_message),
        **load_prices_source(inputs, validation_message),
        **load_fuels_and_sectors(inputs)
    }

    return scenario_inputs

def add_scenario(
        inputs: Inputs,
        validation_text: Value,
        df_scenarios: Value
        ) -> None:
    validation_text.set("")
    data = load_scenario_data(inputs, validation_text, df_scenarios())
    if validation_text() == "":
        new_scenario = pd.DataFrame(data)
        if not df_scenarios().empty:
            new_scenario = pd.concat([df_scenarios(), new_scenario], ignore_index=True)
            new_scenario.reset_index()
        df_scenarios.set(new_scenario)

        success_notification(SERVER["scenarioCreated"])
