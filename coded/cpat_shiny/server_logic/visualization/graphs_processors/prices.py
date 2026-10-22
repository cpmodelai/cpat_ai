from typing import List, Dict, Tuple, Union, Optional
import pandas as pd

from cpat_shiny.server_logic.visualization.graph_processor import GraphProcessor
from cpat_shiny.server_logic.visualization.graphs import Line
from cpat_shiny.server_logic.visualization.graphs_xl import LineXL

from cpat_shiny.mapping import ALL_COUNTRIES

from cpat_shiny.server_logic.visualization.graphs_titles import GRAPHS_TITLES


MAPPING = {
    'mit.rp.all.coa.a': 'Coal',
    'mit.rp.all.nga.a': 'Natural gas',
    'mit.rp.all.ele.a': 'Electricity',
    'mit.rp.all.oop.a': 'Oil',
    'mit.rp.all.die.a': 'Diesel',
    'mit.rp.all.gso.a': 'Gasoline'
}

class PGraphs(GraphProcessor):
    def __init__(
            self,
            data: Dict[str, Union[List[str], Tuple[int]]],
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ):
        super().__init__(data)
        self.__domestic_energy_price_changes_in_policy_scenario(indicators_ref)

    def __domestic_energy_price_changes_in_policy_scenario(
            self,
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]],
            reference_year = 2022
            ) -> None:
        #TODO: or Helpers? if yes also update in indicators/../p.py
        helpers = indicators_ref['Indicators']

        for country in self.countries:
            for scenario_no, scenario_name in enumerate(self.scenarios):
                if scenario_no != 0:
                    suffix = f'2_U{scenario_no}'
                    cpat_codes = [
                        f'{country}.{code}.{suffix}'
                        for code in list(MAPPING.keys())
                    ]
                    df = helpers[scenario_name]

                    df = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                            ]
                        .rename(index=self.adjusted_mapping(
                            MAPPING, country, suffix))
                        .pipe(self.select_years)
                    )
                    df = (
                        df.div(df[f'{reference_year}'], axis=0)
                        * 100
                    )

                    title = GRAPHS_TITLES['domestic_p'].format(
                        reference_year=reference_year,
                        scenario_name=scenario_name,
                        country=ALL_COUNTRIES[country.upper()]
                    )
                    self.graphs[title] = (
                        Line(
                            self.get_graph_config(
                                title=title,
                                y_label='Baseline = 100'
                            ), df
                        ).fig
                    )
                    self.graphs_xl[title] = (
                        LineXL(
                            self.get_graph_config(
                                title=title,
                                y_label='Baseline = 100'
                            ), df
                        ).fig
                    )
