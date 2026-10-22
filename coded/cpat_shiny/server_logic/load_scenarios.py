import ast

import pandas as pd
from shiny.reactive._reactives import Value

from cpat_shiny.mapping import SCENARIOS_COL_TYPES


def process_csv_scenarios(
        file_info: list,
        df_scenarios: Value
        ) -> None:
    if file_info is not None:
        file_path = file_info[0]["datapath"]
        df = pd.read_csv(file_path)
        # TODO add schema/input verification
        # transforming tuple columns
        df = (
            df
            .assign(
                **{
                    col: df[col].apply(ast.literal_eval)
                    for col in SCENARIOS_COL_TYPES['Tuple']
                    }
                )
        )
        df_scenarios.set(df)
