from typing import Dict

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes


class GraphXL:
    def __init__(
            self,
            graph_config: Dict[str, str]
            ) -> None:
        self.title: str = graph_config['Title']
        self.y_label: str = graph_config['YLabel']
        self.fig: Figure
        self.ax: Axes
        self.fig, self.ax = plt.subplots(figsize=(6.4, 4.8))

    def hide_legend_title(
            self
            ) -> None:
        legend = self.ax.get_legend()
        legend.set_title('')

class StackedAreaXL(GraphXL):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df_baseline: pd.DataFrame,
            df_scenario: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)

        baseline_max = df_baseline.max().max()
        # TODO: tmp solution to change negative values to 0 (they are close to 0 for 'Others')
        df_scenario = df_scenario.map(lambda x: max(x, 0))
        df_scenario.T.plot.area(ax=self.ax)
        df_baseline.T.plot(ax=self.ax, color='red', linewidth=2, marker='o')
        plt.xlabel('Year')
        plt.ylabel( self.y_label)
        plt.title(self.title)
        plt.ylim(top=baseline_max * 10 / 8)
        self.hide_legend_title()

class StackedColumnXL(GraphXL):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df_change: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)

        df_change.T.plot(kind='bar', stacked=True, ax=self.ax)
        plt.xlabel('Year')
        plt.ylabel('Mtoe')
        plt.title(self.title)
        self.hide_legend_title()

class LineXL(GraphXL):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)
        df.T.plot(kind='line', ax=self.ax)
        plt.xlabel('Year')
        plt.ylabel(self.y_label)
        plt.grid()
        plt.title(self.title)
        self.hide_legend_title()
