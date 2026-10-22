from typing import Dict

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


class Graph:
    def __init__(
            self,
            graph_config: Dict[str, str]
            ) -> None:
        self.title: str = graph_config['Title']
        self.y_label: str = graph_config['YLabel']
        self.fig: go.Figure = go.Figure()

    def hide_legend_title(
            self
            ) -> None:
        self.fig.update_layout(legend_title_text='')

    def round_hover_data(
            self
            ) -> None:
        self.fig.update_traces(hovertemplate="(%{x:.0f}, %{y:.2f})")

class StackedArea(Graph):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df_baseline: pd.DataFrame,
            df_scenario: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)

        self.fig = px.area(
            df_scenario.T,
            labels={'index': 'Year', 'value': self.y_label},
            title=self.title
        )

        self.fig.add_trace(
            go.Scatter(
                x=df_baseline.T.index,
                y=df_baseline.T.values.flatten(),
                mode='lines+markers',
                name='Baseline',
                line=dict(color='red', width=2)
            )
        )
        self.hide_legend_title()
        self.round_hover_data()


class StackedColumn(Graph):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df_change: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)

        self.fig = px.bar(
            df_change.T,
            barmode='stack',
            title=self.title,
            labels={'value': 'Mtoe', 'index': 'Year'}
        )
        self.hide_legend_title()
        self.round_hover_data()


class Line(Graph):
    def __init__(
            self,
            graph_config: Dict[str, str],
            df: pd.DataFrame
            ) -> None:
        super().__init__(graph_config)

        self.fig = px.line(
            df.T,
            labels={'index': 'Year', 'value': self.y_label},
            title=self.title
        )
        self.hide_legend_title()
        self.round_hover_data()
