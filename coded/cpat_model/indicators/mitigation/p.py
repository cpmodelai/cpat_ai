import pandas as pd

from cpat_model.indicators.utils.code_column_adder import CodeColumnAdder
from cpat_model.indicators.mitigation.mit_indicators_common import MitIndicatorsCommon


class IndicatorsP(MitIndicatorsCommon):
    def __init__(self, main_instance):
        self.main_instance = main_instance

    def calculate(
            self,
            p: pd.DataFrame,
            scenario_name: str,
            scenario_no: int
            ) -> None:
        # for Domestic energy price changes in policy scenario
        p_changes = (
            p[
                p.index.get_level_values('FuelCode').isin(['die', 'oop', 'gso', 'coa', 'nga', 'ele']) &
                ~p.index.get_level_values('SectorCode').isin((['elec', 'wav', 'neu']))
            ]
            .groupby(['CountryCode', 'FuelCode'])
            .mean(numeric_only=True)
            .pipe(
                CodeColumnAdder.mit_rp_s_f_a,
                scenario_name=scenario_name,
                scenario_no=scenario_no
                )
        )
        #TODO: is_helper = True? if yes, also update in visualization/../prices.py
        self.main_instance.update_indicators(scenario_name, p_changes)
