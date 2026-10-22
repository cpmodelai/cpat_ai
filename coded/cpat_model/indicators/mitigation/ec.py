import pandas as pd

from cpat_model.indicators.utils.code_column_adder import CodeColumnAdder
from cpat_model.indicators.mitigation.mit_indicators_common import MitIndicatorsCommon

from cpat_model.indicators.utils.constants import (
    FOSSIL_FUELS_AND_BIO, RNW_AGG,
    KTOE_TO_GWH, GWH_TO_TWH,
    SECTORS_AGG, REVERSE_SECTORS_AGG,
    REN_AGG, REVERSE_REN_AGG, SECTORS_FOR_REN_AGG, POW_ELEC_FUELS
    )

class IndicatorsEC(MitIndicatorsCommon):
    def __init__(self, main_instance):
        self.main_instance = main_instance

    def calculate(
            self,
            ec: pd.DataFrame,
            scenario_name: str,
            scenario_no: int
            ) -> None:
        ### All scenarios (baseline and policy) below:

        ### Energy consumption - {f} (baseline) | (policy)
        ### mit.ener.con.{f}
        ### Total Energy consumption, ktoe (baseline) | (policy)
        ### mit.ener.con.tot
        ### Total fossil fuel energy consumption (baseline) | (policy)
        ### mit.ener.tot.tot
        ec_fuel_agg = (
            ec[
                ec.index.get_level_values('FuelCode').isin((FOSSIL_FUELS_AND_BIO + ['nuc'])) &
                ec.index.get_level_values('SectorCode').isin(
                    [v for l in SECTORS_AGG.values() for v in l]
                )
            ]
            .groupby(level=['CountryCode', 'FuelCode'])
            .sum(numeric_only=True)
        )
        ec_tot_tot = (
            ec_fuel_agg[ # only fossil fuels
                ~ec_fuel_agg.index.get_level_values('FuelCode').isin((['bio', 'nuc']))
            ]
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_ener_tot_tot,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_tot = (
            ec_fuel_agg
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
        )
        ec_fuel_agg = (
            ec_fuel_agg
            .pipe(
                CodeColumnAdder.mit_ener_con_f,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_fuel_agg)
        self.main_instance.update_indicators(scenario_name, ec_tot_tot)

        ### Energy consumption - Non-biomass renewable final electricity (baseline) | (policy)
        ### mit.ener.con.nrw
        ### Total consumption by fuel type: Nuclear & renewables (baseline) | (policy)
        ### mit.ener.con.ren
        ec_rnw_elec = (
            ec[
                ec.index.get_level_values('SectorCode').isin(['elec']) &
                ec.index.get_level_values('FuelCode').isin(RNW_AGG['rnw'])
            ] / KTOE_TO_GWH
        )

        ec_rnw_bld_ind = (
            ec[
                ec.index.get_level_values('SectorCode').isin(
                    (SECTORS_AGG['res'] + SECTORS_AGG['ind'])) &
                ec.index.get_level_values('FuelCode').isin(RNW_AGG['rnw'])
            ]
        )

        ec_rnw = (
            pd.concat([ec_rnw_elec, ec_rnw_bld_ind], axis=0)
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
        )
        ec_tot = (
            pd.concat([ec_tot, ec_rnw], axis=0)
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_ener_con_tot,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_nuc = (
            ec[
                ec.index.get_level_values('SectorCode').isin(['pow']) &
                ec.index.get_level_values('FuelCode').isin(['nuc'])
            ]
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
        )
        ec_ren = (
            pd.concat([ec_rnw, ec_nuc], axis=0)
            .groupby(level=['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                self._extend_indexrs, ###
                column_name='FuelCode',
                aggr='ren'
            )
            .pipe(
                CodeColumnAdder.mit_ener_con_f,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_rnw = (
            ec_rnw
            .pipe(
                self._extend_indexrs, ###
                column_name='FuelCode',
                aggr='rnw'
            )
            .pipe(
                CodeColumnAdder.mit_ener_con_f,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_rnw)
        self.main_instance.update_indicators(scenario_name, ec_ren)
        self.main_instance.update_indicators(scenario_name, ec_tot)

        ### {f} consumption: {s} (baseline) | (policy)
        ### mit.ener.{f}.{s} // sector aggregated
        ec_reset_by_sector = (
            ec[
                ec.index.get_level_values('FuelCode').isin(FOSSIL_FUELS_AND_BIO)
            ]
            .reset_index()
        )
        ec_reset_by_sector['SectorCode'] = (
            ec_reset_by_sector['SectorCode']
            .map(lambda x: self._map_to_group(x, REVERSE_SECTORS_AGG)) ###
        )
        ec_reset_by_sector = ec_reset_by_sector.dropna(subset=['SectorCode'])

        ec_by_sector = (
            ec_reset_by_sector
            .groupby(['CountryCode', 'SectorCode', 'FuelCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_ener_f_s_aggr,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_by_sector)

        ### Electricity generation from {f}, baseline | policy (TWh)
        ### mit.elec.twh.{f}
        ### Total electricity supplied, baseline | policy (TWh)
        ### mit.ener.twh.tot
        ec_reset_ren = ec.reset_index()
        ec_reset_ren['FuelCode'] = (
            ec_reset_ren['FuelCode']
            .map(lambda x: self._map_to_group(x, REVERSE_REN_AGG)) ###
        )
        ec_reset_ren = ec_reset_ren.dropna(subset=['FuelCode'])
        ec_ren = (
            ec_reset_ren[
                ec_reset_ren['SectorCode']
                .isin(SECTORS_FOR_REN_AGG)
                ]
            .groupby(['CountryCode', 'FuelCode'])
            .sum(numeric_only=True)
        )

        ec_twh_no_ren = (
            ec[
                ec.index.get_level_values('FuelCode').isin(POW_ELEC_FUELS) &
                ec.index.get_level_values('SectorCode').isin(['elec'])
                ]
            .reset_index(level='SectorCode', drop=True)
        )
        ec_thw = (
            pd.concat([ec_ren, ec_twh_no_ren], axis=0) *
            KTOE_TO_GWH *
            GWH_TO_TWH
            )
        ec_thw_tot = (
            ec_thw
            .groupby(['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_elec_twh_tot,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_thw = (
            ec_thw
            .pipe(
                CodeColumnAdder.mit_elec_twh_f,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_thw)
        self.main_instance.update_indicators(scenario_name, ec_thw_tot)

        ### codes for total ec by fuel graphs
        ### TODO add nuc separately?
        ec_tot_sec = (
            ec[
                ec.index.get_level_values('FuelCode').isin(FOSSIL_FUELS_AND_BIO) &
                ec.index.get_level_values('SectorCode').isin(
                    [v for l in SECTORS_AGG.values() for v in l]
                )
            ]
            .groupby(['CountryCode', 'FuelCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_ener_tot_f_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        ec_tot_sec_ren = (
            ec[
                # why nuc included; if no nuc RNW_AGG['rnw']
                ec.index.get_level_values('FuelCode').isin(REN_AGG['ren']) &
                ec.index.get_level_values('SectorCode').isin(['elec']) # can be ?pow? and no conv
            ]
        ) / KTOE_TO_GWH
        ec_tot_sec_ren = (
            pd.concat([
                ec_tot_sec_ren,
                ec[
                # again: why nuc, if we should plot it as a separate category?
                    ec.index.get_level_values('FuelCode').isin(REN_AGG['ren']) &
                    ec.index.get_level_values('SectorCode').isin(SECTORS_FOR_REN_AGG)
                ]
            ], axis=0)
            .groupby(['CountryCode'])
            .sum(numeric_only=True)
            .pipe(self._extend_indexrs, 'FuelCode', 'ren') ###
            .pipe(
                CodeColumnAdder.mit_ener_tot_f_e,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, ec_tot_sec, True)
        self.main_instance.update_indicators(scenario_name, ec_tot_sec_ren, True)
