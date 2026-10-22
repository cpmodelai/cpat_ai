from typing import List, Dict, Tuple, Union, Optional
import pandas as pd

from cpat_shiny.server_logic.visualization.graph_processor import GraphProcessor
from cpat_shiny.server_logic.visualization.graphs import StackedArea
from cpat_shiny.server_logic.visualization.graphs_xl import StackedAreaXL
from cpat_shiny.mapping import ALL_COUNTRIES

from cpat_shiny.server_logic.visualization.graphs_titles import GRAPHS_TITLES


BY_SECTOR_EM_MAPPING = {
    'mit.co2.pow': 'Power',
    'mit.co2.tra': 'Transport',
    'mit.co2.res': 'Buildings',
    'mit.co2.ind': 'Industry',
    'mit.co2.oen': 'Other',
    'mit.co2.enr.tot': 'Baseline'
}
SECTORS_FOR_EM = ['pow', 'tra', 'res', 'ind', 'oen']

class EMGraphs(GraphProcessor):
    def __init__(
            self,
            data: Dict[str, Union[List[str], Tuple[int]]],
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ):
        super().__init__(data)
        self.__co2_emissions_by_sector(indicators_ref)

    def __co2_emissions_by_sector(
            self,
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ) -> None:
        indicators = indicators_ref['Indicators']

        for country in self.countries:
            for scenario_no, scenario_name in enumerate(self.scenarios):
                if scenario_no == 0:
                    suffix = '1'
                    total_code = [f'{country}.mit.co2.enr.tot.{suffix}']
                    df = indicators[scenario_name]
                    df_baseline = (
                        df[
                            df.index.get_level_values('CPATCode').isin(total_code)
                        ]
                        .rename(
                            index=self.adjusted_mapping(BY_SECTOR_EM_MAPPING, country, suffix)
                        )
                        .pipe(self.select_years)
                    )
                else:
                    suffix = f'2_U{scenario_no}'
                    cpat_codes = [
                        f'{country}.mit.co2.{s}.{suffix}'
                        for s in SECTORS_FOR_EM
                    ]
                    df = indicators[scenario_name]
                    df_scenario = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                        ]
                        .rename(
                            index=self.adjusted_mapping(BY_SECTOR_EM_MAPPING, country, suffix)
                        )
                        .pipe(self.select_years)
                    )

                    title = GRAPHS_TITLES['em_by_sector'].format(
                        scenario_name=scenario_name,
                        country=ALL_COUNTRIES[country.upper()]
                    )
                    self.graphs[title] = (
                        StackedArea(
                            self.get_graph_config(
                                title=title,
                                y_label='mtCO2'
                            ), df_baseline, df_scenario
                        ).fig
                    )
                    self.graphs_xl[title] = (
                        StackedAreaXL(
                            self.get_graph_config(
                                title=title,
                                y_label='mtCO2'
                            ), df_baseline, df_scenario
                        ).fig
                    )
