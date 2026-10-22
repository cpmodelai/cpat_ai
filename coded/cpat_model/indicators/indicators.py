from typing import Dict, List, Optional
import pandas as pd

from cpat_model.constants import BASELINE_SCENARIO

from cpat_model.indicators.mitigation.dec import IndicatorsDEC
from cpat_model.indicators.mitigation.ec import IndicatorsEC
from cpat_model.indicators.mitigation.p import IndicatorsP
from cpat_model.indicators.mitigation.em import IndicatorsEM


class Indicators:
    """
    TODO
    Attributes:
    Methods:
    """
    def __init__(
            self,
            results,
            selected_indicators: List[str],
            selected_countries: List[str]
            ) -> None:

        self.indicators = {}
        self.helper_indicators = {}

        # creating structure for the calculated indicators
        self.selected_indicators = selected_indicators
        self.selected_countries = selected_countries

    def get_grouped_indicators(
            self
            ) -> None:
        self.grouped_indicators = pd.DataFrame()
        for _, df in self.indicators.items():
            if df is not None:
                self.grouped_indicators = pd.concat([self.grouped_indicators, df], axis=0)

        self.grouped_indicators = self.grouped_indicators.reset_index().set_index('CPATCode')
        self.grouped_indicators = self.grouped_indicators.rename(columns={'CPATIndicator': 'Indicator header'})

    def update_indicators(
            self,
            scenario_name: str,
            df: pd.DataFrame,
            is_helper = False
            ) -> None:
        target_dict = self.helper_indicators if is_helper else self.indicators

        if target_dict[scenario_name] is None:
            target_dict[scenario_name] = df.copy()
        else:
            target_dict[scenario_name] = (
                pd.concat([target_dict[scenario_name], df], axis=0)
            )


class MitIndicators(Indicators):
    """
    TODO
    Attributes:
    Methods:
    """
    def __init__(
            self,
            results,
            selected_indicators: List[str],
            selected_countries: List[str]
            ) -> None:

        Indicators.__init__(self, results, selected_indicators, selected_countries)
        self.scenarios = []
        for scenario_name in results.keys():
            self.scenarios.append(scenario_name)
            self.indicators[scenario_name] = None
            self.helper_indicators[scenario_name] = None

        indicators_sections = {
            'dec': self.__create_idicators_dec,
            'ec': self.__create_idicators_ec,
            'p': self.__create_idicators_p,
            'em': self.__create_idicators_em,
        }
        for scenario_no, (scenario_name, res) in enumerate(results.items()):
            for selected_indicator in self.selected_indicators:
                indicators_sections[selected_indicator](scenario_name, scenario_no, res)

        self.get_grouped_indicators()

    def __create_idicators_ec(
            self,
            scenario_name: str,
            scenario_no: int,
            scenario_results
            ) -> None:
        ec = scenario_results.ec #ref is enough
        IndicatorsEC(self).calculate(ec, scenario_name, scenario_no)

    def __create_idicators_dec(
            self,
            scenario_name: str,
            scenario_no: int,
            scenario_results
            ) -> None:
        ec = scenario_results.ec #ref is enough
        IndicatorsDEC(self).calculate(ec, scenario_name, scenario_no)

    def __create_idicators_p(
            self,
            scenario_name: str,
            scenario_no: int,
            scenario_results
            ) -> None:
        if scenario_no != 0:
            p = scenario_results.p #ref is enough
            IndicatorsP(self).calculate(p, scenario_name, scenario_no)

    def __create_idicators_em(
            self,
            scenario_name: str,
            scenario_no: int,
            scenario_results
            ) -> None:
        em = scenario_results.em
        IndicatorsEM(self).calculate(em, scenario_name, scenario_no)