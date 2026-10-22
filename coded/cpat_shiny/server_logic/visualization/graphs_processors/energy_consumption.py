from typing import List, Dict, Tuple, Union, Optional
import pandas as pd

from cpat_shiny.server_logic.visualization.graph_processor import GraphProcessor
from cpat_shiny.server_logic.visualization.graphs import StackedArea, StackedColumn
from cpat_shiny.server_logic.visualization.graphs_xl import StackedAreaXL, StackedColumnXL
from cpat_shiny.mapping import ALL_COUNTRIES

from cpat_shiny.server_logic.visualization.graphs_titles import GRAPHS_TITLES

from cpat_model.indicators.utils.constants import FOSSIL_FUELS_AND_BIO


BY_SECTOR_NAMES_MAPPING = {
    'mit.ener.pow.tot.e': 'Power',
    'mit.ener.tra.tot.e': 'Transport',
    'mit.ener.bld.tot.e': 'Buildings',
    'mit.ener.ind.tot.e': 'Industry',
    'mit.ener.oen.tot.e': 'Other',
    'mit.ener.tot.tot.e': 'Baseline'
}

BY_FUEL_NAMES_MAPPING = {
    'mit.ener.tot.coa.e': 'Coal',
    'mit.ener.tot.nga.e': 'Gas',
    'mit.ener.tot.gso.e': 'Gasoline',
    'mit.ener.tot.lpg.e': 'LPG/kerosine',
    'mit.ener.tot.ker.e': 'Kerosine',
    'mit.ener.tot.ren.e': 'Renewables',
    'mit.ener.tot.oop.e': 'Oil',
    'mit.ener.tot.nuc.e': 'Nuclear',
    'mit.ener.tot.die.e': 'Diesel',
    'mit.ener.tot.bio.e': 'Biomass',
    'mit.ener.tot.tot.e': 'Baseline'
}

TOTAL_EC_SECTORS = ['pow', 'tra', 'bld', 'ind', 'oen']


class ECGraphs(GraphProcessor):
    def __init__(
            self,
            data: Dict[str, Union[List[str], Tuple[int]]],
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ) -> None:
        super().__init__(data)
        self.__total_ec_by_sector(indicators_ref)
        self.__total_ec_and_change_in_ec_by_fuel(indicators_ref)

    def __total_ec_by_sector(
            self,
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ) -> None:

        indicators = indicators_ref['Indicators']
        helpers = indicators_ref['Helpers']

        for country in self.countries:
            for scenario_no, scenario_name in enumerate(self.scenarios):
                if scenario_no == 0:
                    suffix = '1'
                    cpat_codes = [
                        f'{country}.mit.ener.{s}.tot.e.{suffix}'
                        for s in TOTAL_EC_SECTORS
                    ]
                    total_code = f'{country}.mit.ener.tot.tot.e.{suffix}'
                    df = helpers[scenario_name]

                    df_baseline = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                            ]
                        .groupby('Unit')
                        .sum(numeric_only=True)
                        .reset_index()
                        .assign(**{'CPATCode': total_code})
                        .set_index(['CPATCode'])
                        .rename(index=self.adjusted_mapping(
                            BY_SECTOR_NAMES_MAPPING, country, suffix))
                        .pipe(self.select_years)
                    ) / 1000 # convert ktoe to mtoe
                else:
                    suffix = f'2_U{scenario_no}'
                    cpat_codes = [
                        f'{country}.mit.ener.{s}.tot.e.{suffix}'
                        for s in TOTAL_EC_SECTORS
                    ]
                    df = indicators[scenario_name]

                    df_scenario = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                            ]
                        .rename(index=self.adjusted_mapping(
                            BY_SECTOR_NAMES_MAPPING, country, suffix))
                        .pipe(self.select_years)
                    ) / 1000 # convert ktoe to mtoe

                    title = GRAPHS_TITLES['ec_by_sector'].format(
                        scenario_name=scenario_name, country=ALL_COUNTRIES[country.upper()]
                    )
                    self.graphs[title] = (
                        StackedArea(
                            self.get_graph_config(
                                title=title,
                                y_label='Mtoe'
                            ), df_baseline, df_scenario
                        ).fig
                    )
                    self.graphs_xl[title] = (
                        StackedAreaXL(
                            self.get_graph_config(
                                title=title,
                                y_label='Mtoe'
                            ), df_baseline, df_scenario
                        ).fig
                    )


    def __total_ec_and_change_in_ec_by_fuel(
            self,
            indicators_ref: Dict[str, Dict[str, Optional[pd.DataFrame]]]
            ) -> None:
        helpers = indicators_ref['Helpers']

        for country in self.countries:
            for scenario_no, scenario_name in enumerate(self.scenarios):
                if scenario_no == 0:
                    suffix = '1'
                    cpat_codes = [
                        f'{country}.mit.ener.tot.{f}.e.{suffix}'
                        for f in (FOSSIL_FUELS_AND_BIO + ['ren'])
                    ]
                    total_code = f'{country}.mit.ener.tot.tot.e.{suffix}'
                    df = helpers[scenario_name]

                    df_baseline = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                            ]
                    )
                    df_baseline_change = (
                        df_baseline
                        .rename(index=self.adjusted_mapping(BY_FUEL_NAMES_MAPPING, country, suffix))
                        .pipe(self.add_columns, 'LPG/kerosine', 'Kerosine') # connect lpg and ker
                        .pipe(self.select_years)
                    ) / 1000
                    df_baseline = (
                        df_baseline
                        .groupby('Unit')
                        .sum(numeric_only=True)
                        .reset_index()
                        .assign(**{'CPATCode': total_code})
                        .set_index(['CPATCode'])
                        .rename(index=self.adjusted_mapping(BY_FUEL_NAMES_MAPPING, country, suffix))
                        .pipe(self.select_years)
                    ) / 1000 # convert ktoe to mtoe
                else:
                    suffix = f'2_U{scenario_no}'
                    cpat_codes = [
                        f'{country}.mit.ener.tot.{s}.e.{suffix}'
                        for s in (FOSSIL_FUELS_AND_BIO + ['ren'])
                    ]
                    df = helpers[scenario_name]

                    df_scenario = (
                        df[
                            df.index.get_level_values('CPATCode').isin(cpat_codes)
                            ]
                        .rename(index=self.adjusted_mapping(BY_FUEL_NAMES_MAPPING, country, suffix))
                        .pipe(self.add_columns, 'LPG/kerosine', 'Kerosine') # connect lpg and ker
                        .pipe(self.select_years)
                    ) / 1000 # convert ktoe to mtoe

                    title = GRAPHS_TITLES['ec_by_fuel'].format(
                        scenario_name=scenario_name, country=ALL_COUNTRIES[country.upper()]
                    )
                    self.graphs[title] = (
                        StackedArea(
                            self.get_graph_config(
                                title=title,
                                y_label='Mtoe'
                            ), df_baseline, df_scenario
                        ).fig
                    )
                    self.graphs_xl[title] = (
                        StackedAreaXL(
                            self.get_graph_config(
                                title=title,
                                y_label='Mtoe'
                            ), df_baseline, df_scenario
                        ).fig
                    )

                    df_change = df_scenario - df_baseline_change
                    title = GRAPHS_TITLES['ec_change_by_fuel'].format(
                        scenario_name=scenario_name, country=ALL_COUNTRIES[country.upper()]
                    )
                    self.graphs[title] = (
                        StackedColumn(
                            self.get_graph_config(
                                title=title,
                            ), df_change
                        ).fig
                    )
                    self.graphs_xl[title] = (
                        StackedColumnXL(
                            self.get_graph_config(
                                title=title,
                            ), df_change
                        ).fig
                    )
