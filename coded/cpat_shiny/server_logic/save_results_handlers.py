from typing import Dict, List

import pandas as pd

from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.ui.components.common.notifications import success_notification
from cpat_shiny.ui.labels import SERVER
from cpat_shiny.server_logic.paths import EMPTY_FILE_PATH


def extract_raw_results(
        results_to_be_saved : List[str],
        results: Dict[str, object],
        sorting_order = ['CountryCode', 'FuelCode', 'SectorCode']
        ) -> Dict[str, pd.DataFrame]:

    raw_results_dict = {}
    for attr in results_to_be_saved:
        df_attr = pd.DataFrame()
        for scen in results.keys():
            df = getattr(results[scen], attr)
            if isinstance(df, pd.DataFrame):
                if sorting_order:
                    df = (
                        df
                        .assign(**{'ScenarioName': scen})
                        .set_index('ScenarioName', append=True)
                        .sort_values(by=sorting_order)
                    )
                else:
                    df = (
                        df
                        .assign(**{'ScenarioName': scen})
                        .set_index('ScenarioName', append=True)
                    )
                df_attr = pd.concat([df_attr, df], axis=0)
            else:
                print(f"{attr} is not in DataFrame format.")
        raw_results_dict[attr] = df_attr.copy()
    return raw_results_dict

def save_results_shiny(
        raw_results_dict: Dict[str, pd.DataFrame],
        path_name: str
        ) -> None:
    """
    """
    # pylint: disable=abstract-class-instantiated
    with pd.ExcelWriter(
        path_name,
        engine="xlsxwriter"
    ) as results_writer:
        for attr, df_attr in raw_results_dict.items():
            df_attr.to_excel(results_writer, sheet_name=attr)

def save_raw_results_handler(
        file_name: str,
        validation_text_results: Value,
        raw_results_list: Dict[str, pd.DataFrame]
        ) -> str:
    if validation_text_results() == '':
        path_name = f'{file_name}.xlsx'
        save_results_shiny(raw_results_list, path_name)
        success_notification(SERVER["resultsSaved"])

        return path_name
    return EMPTY_FILE_PATH
