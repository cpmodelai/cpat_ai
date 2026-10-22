import pandas as pd

from cpat_model.indicators.utils.code_column_adder import CodeColumnAdder
from cpat_model.indicators.mitigation.mit_indicators_common import MitIndicatorsCommon

from cpat_model.indicators.utils.constants import (
    SECTORS_AGG, FOSSIL_FUELS, REVERSE_SECTORS_AGG
    )


class IndicatorsEM(MitIndicatorsCommon):
    def __init__(self, main_instance):
        self.main_instance = main_instance

    def calculate(
            self,
            em: pd.DataFrame,
            scenario_name: str,
            scenario_no: int
            ) -> None:

        em_fossil = (
            em[
                em.index.get_level_values('FuelCode').isin(FOSSIL_FUELS) &
                em.index.get_level_values('SectorCode').isin(
                    [v for l in SECTORS_AGG.values() for v in l]
                )
            ]
        )

        em_fuel_agg = (
            em_fossil
            .groupby(['CountryCode', 'FuelCode'])
            .sum(numeric_only=True)
        )
        em_enr_tot = (
            em_fuel_agg
            .groupby(['CountryCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_co2_enr_tot,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )

        em_fuel_agg = (
            em_fuel_agg
            .pipe(
                CodeColumnAdder.mit_co2_f,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )

        em_fossil_reset = em_fossil.reset_index()
        em_fossil_reset['SectorCode'] = (
            em_fossil_reset['SectorCode']
            .map(lambda x: self._map_to_group(x, REVERSE_SECTORS_AGG))
        )
        em_fossil_reset = em_fossil_reset.dropna(subset=['SectorCode'])
        em_sector_agg = (
            em_fossil_reset
            .groupby(['CountryCode', 'SectorCode'])
            .sum(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_co2_s,
                scenario_name=scenario_name,
                scenario_no=scenario_no
            )
        )
        self.main_instance.update_indicators(scenario_name, em_enr_tot)
        self.main_instance.update_indicators(scenario_name, em_fuel_agg)
        self.main_instance.update_indicators(scenario_name, em_sector_agg)
