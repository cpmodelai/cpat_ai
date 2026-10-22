import pandas as pd

from cpat_model.indicators.utils.code_column_adder import CodeColumnAdder
from cpat_model.indicators.mitigation.mit_indicators_common import MitIndicatorsCommon

from cpat_model.indicators.utils.constants import (
    TRA_BLD_IND_SECTORS, FOSSIL_FUELS_AND_BIO,
    REVERSE_SECTORS_AGG,
    REN_AGG, POW_ELEC_FUELS
    )

from cpat_model.constants import BASELINE_SCENARIO


class IndicatorsDEC(MitIndicatorsCommon):
    def __init__(self, main_instance):
        self.main_instance = main_instance

    def calculate(
            self,
            ec: pd.DataFrame,
            scenario_name: str,
            scenario_no: int
            ) -> None:
        ### Energy consumption, {sector}, {fuel}, policy
        ### mit.ener.{s}.{f}.e
        ### Energy consumption, {s}, sector-generated renewables, policy
        ### mit.ener.{s}.ren.e
        ### Fossil fuel consumption by sector, {sector_aggregation}, policy (ktoe)
        ### mit_ener.{s_aggr}.tot.e
        ec_avi_jfu = (
            ec[
                ec.index.get_level_values('SectorCode').isin(['avi']) &
                ec.index.get_level_values('FuelCode').isin(['jfu'])
            ]
        )
        ec_sector_fuel = (
            ec[
                ec.index.get_level_values('SectorCode').isin(TRA_BLD_IND_SECTORS) &
                ec.index.get_level_values('FuelCode').isin(FOSSIL_FUELS_AND_BIO)
            ]
        )
        ec_sector_ren = (
            ec[
                ec.index.get_level_values('SectorCode').isin(TRA_BLD_IND_SECTORS) &
                ec.index.get_level_values('FuelCode').isin(REN_AGG['ren'])
            ]
            .groupby(level=['CountryCode', 'SectorCode'])
            .sum(numeric_only=True)
            .pipe(
                self._extend_indexrs, ###
                column_name='FuelCode',
                aggr='ren'
            )
        )
        ec_sector_fuel = (
            pd.concat([ec_sector_fuel, ec_avi_jfu, ec_sector_ren], axis=0)
        )
        ec_sector_aggr_tot = ec_sector_fuel.reset_index()
        ec_sector_aggr_tot['SectorCode'] = (
            ec_sector_aggr_tot['SectorCode']
            .map(lambda x: self._map_to_group(x, REVERSE_SECTORS_AGG)) ###
        )
        ec_sector_aggr_tot = (
            ec_sector_aggr_tot
            .groupby(['CountryCode', 'SectorCode'])
            .sum(numeric_only=True)
            .rename(index={'res': 'bld'}, level='SectorCode')
            .pipe(
                CodeColumnAdder.mit_ener_s_tot_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_sector_fuel = (
            ec_sector_fuel
            .pipe(
                CodeColumnAdder.mit_ener_s_f_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_oen_tot = (
            ec[
                ec.index.get_level_values('SectorCode').isin(['oen']) &
                ec.index.get_level_values('FuelCode').isin((FOSSIL_FUELS_AND_BIO + REN_AGG['ren']))
            ]
            .groupby(['CountryCode', 'SectorCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_ener_s_tot_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        is_helper = scenario_name == BASELINE_SCENARIO
        self.main_instance.update_indicators(scenario_name, ec_sector_aggr_tot, is_helper)
        self.main_instance.update_indicators(scenario_name, ec_oen_tot, is_helper)
        self.main_instance.update_indicators(scenario_name, ec_sector_fuel, is_helper)

        ### Energy consumption, power, {f}, policy
        ### mit.ener.pow.{f}.e
        ### Fossil fuel consumption by sector, Power, elasticity, policy (ktoe)
        ### mit.ener.pow.tot.e
        ec_pow = (
            ec[
                ec.index.get_level_values('SectorCode').isin(['pow']) &
                ec.index.get_level_values('FuelCode').isin(POW_ELEC_FUELS)
            ]
        )
        ec_pow_tot = (
            ec_pow
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                self._extend_indexrs, ###
                column_name='FuelCode',
                aggr='tot'
            )
            .pipe(
                CodeColumnAdder.mit_ener_pow_f_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_pow = (
            ec_pow
            .pipe(
                CodeColumnAdder.mit_ener_pow_f_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_pow_tot, is_helper)
        self.main_instance.update_indicators(scenario_name, ec_pow, is_helper)
