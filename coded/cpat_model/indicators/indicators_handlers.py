from typing import List

from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.ui.components.common.notifications import success_notification

from cpat_shiny.ui.labels import SERVER
from cpat_shiny.server_logic.paths import EMPTY_FILE_PATH

from cpat_shiny.server_logic.reactive.reactive_graphs import global_graphs, global_graphs_xl
from cpat_shiny.server_logic.visualization.graph_generator import GraphGenerator
from cpat_model.indicators.indicators import MitIndicators
from cpat_model.indicators.indicators_excel_saver import IndicatorsExcelSaver

def create_indicators_handler(
        inputs: Inputs,
        validation_text_indicators_selection: str,
        results: Value,
        indicators: Value,
        selected_countries: Value
        ) -> None:
    if validation_text_indicators_selection == '':
        selected_indicators = list(inputs.indicators_input())
        indicators.set(
            MitIndicators(results(), selected_indicators, selected_countries())
        )
        gg = GraphGenerator(indicators(), (2022, 2035))
        global_graphs_xl.set(gg.graphs_xl)
        global_graphs.set(gg.graphs)

        success_notification(SERVER["indicatorsCreated"])

def download_indicators_handler(
        inputs: Inputs,
        validation_text_indicators_file: str,
        indicators: Value,
        module_name: str = 'Mitigation'
        ) -> str:
    if validation_text_indicators_file == '':
        indicators_file_name = inputs.indicators_file_name_input()
        indicators_path = f'{indicators_file_name}.xlsx'
        IndicatorsExcelSaver(indicators(), global_graphs_xl(), indicators_path, module_name)
        success_notification(SERVER["indicatorsDownloaded"])
        return indicators_path
    return EMPTY_FILE_PATH
