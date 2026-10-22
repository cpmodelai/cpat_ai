from typing import Tuple

from cpat_model.indicators.indicators import MitIndicators
from cpat_shiny.server_logic.visualization.graphs_processors.energy_consumption import ECGraphs
from cpat_shiny.server_logic.visualization.graphs_processors.prices import PGraphs
from cpat_shiny.server_logic.visualization.graphs_processors.emissions import EMGraphs


class GraphGenerator:
    def __init__(
            self,
            indicators: MitIndicators,
            years: Tuple[int, int]
            ) -> None:
        self.graphs = {}
        self.graphs_xl = {}
        indicators_ref = {
            'Indicators': indicators.indicators,
            'Helpers': indicators.helper_indicators
        }

        self.selected_countries = indicators.selected_countries.copy()
        self.__countries = [c.lower() for c in indicators.selected_countries]
        self.scenarios = indicators.scenarios.copy()
        self.years = years

        data = {
            'Countries': self.__countries,
            'Scenarios': self.scenarios,
            'Years': self.years
        }

        if 'ec' in indicators.selected_indicators and 'dec' in indicators.selected_indicators:
            ecg = ECGraphs(data, indicators_ref)
            self.graphs.update(ecg.graphs)
            self.graphs_xl.update(ecg.graphs_xl)
        if 'p' in indicators.selected_indicators:
            pg = PGraphs(data, indicators_ref)
            self.graphs.update(pg.graphs)
            self.graphs_xl.update(pg.graphs_xl)
        if 'em' in indicators.selected_indicators:
            emg = EMGraphs(data, indicators_ref)
            self.graphs.update(emg.graphs)
            self.graphs_xl.update(emg.graphs_xl)
