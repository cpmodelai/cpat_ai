from shiny import reactive
import plotly.graph_objects as go

from cpat_shiny.mapping import ALL_COUNTRIES

from cpat_shiny.server_logic.visualization.graphs_titles import GRAPHS_TITLES

global_graphs = reactive.value({})
graph_selection = reactive.value({
    "country_visualization": "",
    "scenario_visualization": "",
})

global_graphs_xl = reactive.value({})

def create_update_country_visualization(inputs):
    @reactive.effect
    @reactive.event(inputs.country_visualization)
    def _():
        current_selection = graph_selection.get()
        current_selection['country_visualization'] = inputs.country_visualization()
        graph_selection.set(current_selection)

def create_update_scenario_visualization(inputs):
    @reactive.effect
    @reactive.event(inputs.scenario_visualization)
    def _():
        current_selection = graph_selection.get()
        current_selection['scenario_visualization'] = inputs.scenario_visualization()
        graph_selection.set(current_selection)

def get_graph(
        inputs,
        graph_type: str
        ) -> go.Figure:
    if global_graphs():
        scenario_name = inputs.scenario_visualization()
        country = inputs.country_visualization().upper()
        if graph_type in GRAPHS_TITLES:
            if graph_type == 'domestic_p':
                title = GRAPHS_TITLES[graph_type].format(
                    reference_year=2022, # TODO: softcode this
                    scenario_name=scenario_name,
                    country=ALL_COUNTRIES[country]
                )
            else:
                title = GRAPHS_TITLES[graph_type].format(
                    scenario_name=scenario_name, country=ALL_COUNTRIES[country]
                )
        else:
            title = ''
        if title in global_graphs():
            return global_graphs()[title]
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig
    return go.Figure()
