import re
from typing import Literal

from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.ui.labels import VALIDATION, RESULTS


INVALID_CHARS = r'<>:"/\\|?*#%&}{$!\'`@+='

def validate_folder_name(
        inputs: Inputs,
        validation_text_results: Value,
        input_name: Literal["resultsFileName", "indicatorsFileName"]
        ) -> None:
    input_mapping = {
        "resultsFileName": 'raw_results_file_name_input',
        "indicatorsFileName": 'indicators_file_name_input'
    }
    assert (
        input_name in input_mapping
    ), f"Invalid input name to validate: {input_name}"

    if validation_text_results() == "":
        file_name = getattr(inputs, input_mapping[input_name])()

        if not file_name or not file_name.strip():
            validation_text_results.set(
                VALIDATION['fileNameEmpty'].format(input_name=RESULTS[input_name])
            )
            return
        if file_name == 'empty':
            validation_text_results.set(
                VALIDATION['fileNameIsEmpty'].format(input_name=RESULTS[input_name])
            )
            return
        if re.search(f"[{re.escape(INVALID_CHARS)}]", file_name):
            validation_text_results.set(
                VALIDATION['fileNameInvalidChars'].format(input_name=RESULTS[input_name])
            )
            return
        if file_name != file_name.strip():
            validation_text_results.set(
                VALIDATION['fileNameTrailingWhitespace'].format(input_name=RESULTS[input_name])
            )
            return
        if len(file_name) > 30:
            validation_text_results.set(
                VALIDATION['fileNameTooLong'].format(input_name=RESULTS[input_name])
            )
            return

def validate_selection(
        inputs: Inputs,
        validation_text_results: Value,
        input_name: Literal["selectVariables", "selectIndicators"]
        ) -> None:
    input_mapping = {
        "selectVariables": 'vars_to_save_input',
        "selectIndicators": 'indicators_input'
    }
    assert (
        input_name in input_mapping
    ), f"Invalid input name to validate: {input_name}"

    if validation_text_results() == "":
        selected = getattr(inputs, input_mapping[input_name])()

        if not selected:
            validation_text_results.set(
                VALIDATION['fileNameEmpty'].format(input_name=RESULTS[input_name])
            )
            return


class ResultsInputsValidation:
    @staticmethod
    def validate_raw_results_vars_to_save(
            inputs: Inputs,
            validation_text_results: Value
            ) -> None:
        validate_selection(inputs, validation_text_results, 'selectVariables')

    @staticmethod
    def validate_indicators_to_save(
            inputs: Inputs,
            validation_text_results: Value
            ) -> None:
        validate_selection(inputs, validation_text_results, 'selectIndicators')

    @staticmethod
    def validate_raw_results_file_name(
            inputs: Inputs,
            validation_text_results: Value
            ) -> None:
        validate_folder_name(inputs, validation_text_results, 'resultsFileName')

    @staticmethod
    def validate_indicators_file_name(
            inputs: Inputs,
            validation_text_results: Value
            ) -> None:
        validate_folder_name(inputs, validation_text_results, 'indicatorsFileName')
