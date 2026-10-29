from shiny import reactive
import plotly.graph_objects as go

from cpat_shiny.server_logic.visualization.figures import figure

graph_selection = reactive.value({
    "country_visualization": "",
    "scenario_visualization": "",
})

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
        results,
        graph_type: str
        ) -> go.Figure:
    """The graph of the selected country and scenario, from the run in `results` (a ModelRun, or None)."""
    run = results()
    scenario_name = inputs.scenario_visualization()
    country = inputs.country_visualization()
    if run is None or scenario_name not in run.policy_names() or country not in run.countries:
        return go.Figure()
    return figure(run, country, scenario_name, graph_type)
