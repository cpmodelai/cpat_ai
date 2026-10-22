import pandas as pd
from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.ui.labels import VALIDATION
from cpat_shiny.mapping import ALL_COUNTRIES, CT_AFTER_TARGET_YEAR, PRICES_SELECTION

from cpat_model.constants import BASELINE_SCENARIO


class ManualInputsValidation:
    @staticmethod
    def validate_scenario_name(
            inputs: Inputs,
            validation_message: Value,
            df_scenarios: pd.DataFrame
            ) -> None:
        if validation_message() == "":
            scenario_name = inputs.scenario_name_input()

            if not scenario_name or not scenario_name.strip():
                validation_message.set(VALIDATION['nameEmpty'])
                return
            if len(scenario_name) > 30:
                validation_message.set(VALIDATION['nameTooLong'])
                return
            # TODO: assertion for allowed characters
            if scenario_name == BASELINE_SCENARIO:
                validation_message.set(VALIDATION['baselineName'])
                return
            if 'ScenarioName' in df_scenarios.columns:
                if scenario_name in df_scenarios['ScenarioName'].unique():
                    validation_message.set(VALIDATION['nameNotUnique'].format(scenario_name=scenario_name))
                    return

    @staticmethod
    def validate_countries(
            inputs: Inputs,
            validation_message: Value,
            df_scenarios: pd.DataFrame
            ) -> None:
        if validation_message() == "":
            countries = inputs.countries_input()

            if not countries:
                validation_message.set(VALIDATION['countriesEmpty'])
                return
            if 'SelectedCountries' in df_scenarios.columns:
                c = sorted(countries)
                e_c = sorted(df_scenarios['SelectedCountries'].unique()[0])
                if c != e_c:
                    c = ', '.join([ALL_COUNTRIES[country] for country in c])
                    e_c = ', '.join([ALL_COUNTRIES[country] for country in e_c])
                    validation_message.set(VALIDATION['countriesNotConsistent'].format(c=c, e_c=e_c))
                    return

    @staticmethod
    def validate_ct_inputs(
            inputs: Inputs,
            validation_message: Value
            ) -> None:
        if validation_message() == "":
            start_year = inputs.start_year()

            if isinstance(start_year, (int, float)):
                if start_year % 1 != 0:
                    validation_message.set(VALIDATION["startYearIsFraction"])
                    return
                if start_year < 2024:
                    validation_message.set(VALIDATION["startYearTooLow"])
                    return
                if start_year > 2050:
                    validation_message.set(VALIDATION["startYearTooHigh"])
                    return
            else:
                validation_message.set(VALIDATION["startYearType"])
                return

            target_year = inputs.target_year()
            if isinstance(target_year, (int, float)):
                if target_year % 1 != 0:
                    validation_message.set(VALIDATION["targetYearIsFraction"])
                    return
                if target_year > 2050:
                    validation_message.set(VALIDATION["targetYearTooHigh"])
                    return
                if target_year < start_year:
                    validation_message.set(VALIDATION["targetYearTooLow"])
                    return
            else:
                validation_message.set(VALIDATION["targetYearType"])
                return

            start_level = inputs.start_level()
            if isinstance(start_level, (int, float)):
                if start_level < 0:
                    validation_message.set(VALIDATION["startLevelTooLow"])
                    return
            else:
                validation_message.set(VALIDATION["startLevelType"])
                return

            target_level = inputs.target_level()
            if isinstance(target_level, (int, float)):
                if target_level < start_level:
                    validation_message.set(VALIDATION["targetLevelTooLow"])
                    return
            else:
                validation_message.set(VALIDATION["targetLevelType"])
                return

            ct_projection = inputs.ct_projection()
            if ct_projection not in CT_AFTER_TARGET_YEAR:
                validation_message.set(VALIDATION["CTProjectionIncorrect"])
                return

    @staticmethod
    def validate_prices_selection(
            inputs: Inputs,
            validation_message: Value
            ) -> None:
        if validation_message() == "":
            countrisource_selectiones = inputs.prices_source_selection()

            if countrisource_selectiones not in PRICES_SELECTION:
                validation_message.set(VALIDATION["PricesSelectionIncorrect"])
                return
