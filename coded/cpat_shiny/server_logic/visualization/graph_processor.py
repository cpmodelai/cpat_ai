from typing import List, Dict, Tuple, Union

import pandas as pd

class GraphProcessor:
    def __init__(
            self,
            data: Dict[str, Union[List[str], Tuple[int]]]
            ) -> None:

        self.countries = data['Countries']
        self.scenarios = data['Scenarios']
        self.start_year = data['Years'][0]
        self.end_year = data['Years'][1]

        self.graphs = {}
        self.graphs_xl = {}

    def select_years(
            self,
            df: pd.DataFrame
            ) -> pd.DataFrame:
        # also drops ['Unit', 'Indicator header'] columns
        return df.loc[
            :,
            (df.columns >= str(self.start_year)) & (df.columns <= str(self.end_year))
        ]

    def adjusted_mapping(
            self,
            mapping: Dict[str, str],
            country: str,
            suffix: str
            ) -> Dict[str, str]:
        return {f'{country}.{k}.{suffix}': v for k, v in mapping.items()}

    def add_columns(
            self,
            df: pd.DataFrame,
            target_row: str,
            source_row: str
            ) -> pd.DataFrame:
        df.loc[target_row] += df.loc[source_row]
        df = df.drop(source_row)
        return df

    def get_graph_config(
            self,
            title: str,
            y_label: str = ''
            ) -> Dict[str, str]:
        return {
            'Title': title,
            'YLabel': y_label
        }
