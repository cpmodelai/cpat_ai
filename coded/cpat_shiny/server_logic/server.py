import asyncio

from shiny import Inputs, Outputs, Session, render, reactive, ui
from shinywidgets import render_widget
from shiny.types import FileInfo

import pandas as pd

from cpat_shiny.ui.labels import SERVER

from cpat_shiny.ui.sections.section_selection import section_selection
from cpat_shiny.ui.sections.documentation_section import html_content

from cpat_shiny.ui.components.common.notifications import (
    success_notification, error_notification, progress_bar
)
from cpat_shiny.ui.components.common.scenario import scenarios_container
from cpat_shiny.ui.components.common.validation_message import validation_message

from cpat_shiny.server_logic.load_scenario import add_scenario
from cpat_shiny.server_logic.load_scenarios import process_csv_scenarios
from cpat_shiny.server_logic.get_scenarios import get_scenarios
from cpat_shiny.server_logic.apply_results_filters import (
    apply_results_filters, apply_results_filters_indicators
)
from cpat_shiny.server_logic.reactive.reactive_input import (
    input_selection, create_update_scenario_name, create_update_countries, create_update_start_year,
    create_update_target_year, create_update_start_level, create_update_target_level,
    create_update_ct_projection, create_update_prices_source_selection,
    create_update_fuels, create_update_sectors
)

from cpat_shiny.server_logic.save_results_handlers import (
    save_raw_results_handler, extract_raw_results
)
from cpat_shiny.server_logic.reactive.reactive_results_inputs import (
    validation_text_raw_results_file, validation_text_raw_results_vars,
    create_update_validation_text_raw_results_vars, create_update_validation_text_raw_results_file,
    validation_text_indicators_selection, validation_text_indicators_file,
    create_update_validation_text_indicators_selection,
    create_update_validation_text_indicators_file,
    results_inputs_selection, create_update_vars_to_save, create_update_indicators_to_calc,
    create_update_raw_results_file_name, create_update_indicators_file_name,
    global_raw_results,
    create_update_raw_results_country_code, create_update_raw_results_sector_code,
    create_update_raw_results_fuel_code, create_update_raw_results_scenario_name,
    df_raw_results_to_render, df_indicators_to_render,
    create_update_raw_results_df_selection,
    create_update_indicators_cpat_code, create_update_indicators_unit,
    create_update_indicators_header
)

from cpat_shiny.server_logic.reactive.reactive_graphs import (
    graph_selection, get_graph,
    create_update_country_visualization, create_update_scenario_visualization
)

from cpat_shiny.server_logic.reactive.reactive_documentation import (
    documentation_selection, create_update_documentation_selection
)

from cpat_model.indicators.indicators_handlers import (
    create_indicators_handler, download_indicators_handler
)

from cpat_model.constants import BASELINE_SCENARIO


def server(inputs: Inputs, output: Outputs, session: Session) -> None:

    df_scenarios = reactive.value(pd.DataFrame())
    validation_text = reactive.value("")

    results = reactive.value({})

    selected_countries = reactive.value([])
    scenarios_names = reactive.value([])

    indicators = reactive.value({})

    create_update_scenario_name(inputs)
    create_update_countries(inputs)
    create_update_start_year(inputs)
    create_update_target_year(inputs)
    create_update_start_level(inputs)
    create_update_target_level(inputs)
    create_update_ct_projection(inputs)
    create_update_prices_source_selection(inputs)
    create_update_fuels(inputs, session)
    create_update_sectors(inputs, session)

    create_update_vars_to_save(inputs, session)
    create_update_indicators_to_calc(inputs, session)
    create_update_raw_results_file_name(inputs)
    create_update_indicators_file_name(inputs)
    create_update_raw_results_country_code(inputs)
    create_update_raw_results_sector_code(inputs)
    create_update_raw_results_fuel_code(inputs)
    create_update_raw_results_scenario_name(inputs)
    create_update_indicators_cpat_code(inputs)
    create_update_indicators_unit(inputs)
    create_update_indicators_header(inputs)

    create_update_raw_results_df_selection(inputs)

    create_update_validation_text_indicators_selection(inputs)
    create_update_validation_text_indicators_file(inputs)
    create_update_validation_text_raw_results_vars(inputs)
    create_update_validation_text_raw_results_file(inputs)

    create_update_country_visualization(inputs)
    create_update_scenario_visualization(inputs)

    create_update_documentation_selection(inputs)

    @reactive.effect
    @reactive.event(inputs.add_scenario_btn)
    def _():
        add_scenario(inputs, validation_text, df_scenarios)

    @render.ui
    @reactive.event(inputs.add_scenario_btn)
    def validation_message_output():
        return validation_message(validation_text())

    # only for dev:
    @output
    @render.text
    def df_scenarios_out():
        return df_scenarios().to_string(index=False)

    @reactive.effect
    @reactive.event(inputs.load_scenarios)
    def _():
        process_csv_scenarios(inputs.load_scenarios(), df_scenarios)

    @render.download(filename='scenarios.csv')
    def download_scenarios():
        yield df_scenarios().to_csv(index=False)

    async def run_scenarios_task() -> None:
        scenarios_input, selected_country_list = get_scenarios(df_scenarios())
        # This is old run_scenarios, new run_scenarion would look like the logic from run_model.py
        # results.set(run_scenarios(scenarios_input, selected_country_list))
        indicators.set({})

        all_scenarios = list(results().keys())
        all_scenarios.remove(BASELINE_SCENARIO)
        scenarios_names.set(all_scenarios)
        selected_countries.set(selected_country_list)

        graph_selection.set({
            "country_visualization": selected_countries()[0],
            "scenario_visualization": scenarios_names()[0]
        })


    @output
    @render.ui
    @reactive.event(inputs.run_scenarios_btn)
    async def run_scenarios_progress():
        if len(df_scenarios()):
            await progress_bar(
                SERVER["scenariosInProgress"],
                run_scenarios_task,
                lambda: success_notification(SERVER["runSuccessful"])
            )

    @output
    @render.ui
    def scenarios_cards():
        return scenarios_container(df_scenarios())

    @reactive.effect
    @reactive.event(inputs.delete_all_scenarios)
    def _():
        df_scenarios.set(pd.DataFrame())
        error_notification(SERVER["scenariosDeleted"])

    ### MITIGATION TAB ###
    @output
    @render.ui
    def page_content():
        return section_selection(
            inputs, results, global_raw_results, indicators,
            input_selection, results_inputs_selection, graph_selection,
            selected_countries, scenarios_names, documentation_selection
        )
    
    @reactive.effect
    @reactive.event(inputs.extract_vars_raw_results)
    def _():
        if validation_text_raw_results_vars() == '':
            global_raw_results.set(extract_raw_results(list(inputs.vars_to_save_input()), results()))

            current_selection = results_inputs_selection.get()
            current_selection['raw_results_df_selection'] = list(global_raw_results().keys())[0]
            results_inputs_selection.set(current_selection)

            apply_results_filters(global_raw_results, inputs, df_raw_results_to_render)

    @render.download()
    def save_raw_results():
        path_name = save_raw_results_handler(
            inputs.raw_results_file_name_input(), validation_text_raw_results_file, global_raw_results()
        )
        return path_name

    @reactive.effect
    @reactive.event(inputs.rerender_raw_results_df)
    def _():
        apply_results_filters(global_raw_results, inputs, df_raw_results_to_render)

    @render.data_frame
    async def raw_results_df():
        if global_raw_results(): # TODO extract
            await asyncio.sleep(1)
            return render.DataGrid(df_raw_results_to_render())
        return pd.DataFrame()

    @render.ui
    def validation_raw_results_vars_message_output():
        return validation_message(validation_text_raw_results_vars(), negative_margin=False)

    @render.ui
    def validation_raw_results_file_message_output():
        return validation_message(validation_text_raw_results_file(), negative_margin=False)

    @render.ui
    def validation_indicators_selection_message_output():
        return validation_message(validation_text_indicators_selection(), negative_margin=False)

    @render.ui
    def validation_indicators_file_message_output():
        return validation_message(validation_text_indicators_file(), negative_margin=False)

    @reactive.effect
    @reactive.event(inputs.create_indicators)
    def _():
        create_indicators_handler(
            inputs,
            validation_text_indicators_selection(),
            results, indicators, selected_countries
        )
        apply_results_filters_indicators(indicators, inputs, df_indicators_to_render)

    @reactive.effect
    @reactive.event(inputs.rerender_indicators_df)
    def _():
        apply_results_filters_indicators(indicators, inputs, df_indicators_to_render)

    @render.data_frame
    def indicators_df():
        if indicators():
            return render.DataGrid(df_indicators_to_render())
        return pd.DataFrame()

    @render.download()
    def download_indicators():
        return download_indicators_handler(
            inputs, validation_text_indicators_file(),
            indicators
        )

    @render_widget
    def plot_ec_by_sector():
        return get_graph(inputs, graph_type='ec_by_sector')

    @render_widget
    def plot_ec_by_fuel():
        return get_graph(inputs, graph_type='ec_by_fuel')

    @render_widget
    def plot_ec_change_by_fuel():
        return get_graph(inputs, graph_type='ec_change_by_fuel')

    @render_widget
    def plot_domestic_p():
        return get_graph(inputs, graph_type='domestic_p')

    @render_widget
    def plot_em_by_sector():
        return get_graph(inputs, graph_type='em_by_sector')

    # TODO fix remove scenario
    # def create_remove_handler(index):
    #     @reactive.effect
    #     @reactive.event(getattr(inputs, f"remove_scenario_{index}"))
    #     def handle_remove_scenario():
    #         if index in df_scenarios().index:
    #             df_scenarios.set(
    #                 df_scenarios().drop(index=index)
    #             )
    #             if df_scenarios().empty:
    #                 df_scenarios.set(pd.DataFrame())

    # # Create handlers for each index in the DataFrame
    # @reactive.effect
    # def create_handlers():
    #     for index, _ in df_scenarios().iterrows():
    #         create_remove_handler(index)

    @output
    @render.ui
    def render_documentation_section():
        html = html_content(documentation_selection())
        return ui.HTML(f"""
            {html}
            <script>
                MathJax.typeset();
            </script>
        """)
