from htmltools import Tag

from shiny import Inputs
from shiny.reactive._reactives import Value

from cpat_shiny.ui.sections.input_section import input_section
from cpat_shiny.ui.sections.scenarios_section import scenarios_section
from cpat_shiny.ui.sections.raw_results_section import raw_results_section, raw_results_section_empty
from cpat_shiny.ui.sections.indicators_section import indicators_section, indicators_section_empty
from cpat_shiny.ui.sections.visualizations_section import (
    visualizations_section, visualizations_section_empty
)
from cpat_shiny.ui.sections.documentation_section import documentation_section

def section_selection(
        inputs: Inputs,
        results: Value,
        global_raw_results: Value,
        indicators: Value,
        input_selection: Value,
        results_inputs_selection: Value,
        graph_selection: Value,
        selected_countries: Value,
        scenarios_names: Value,
        documentation_selection: Value
        ) -> Tag:
    selected_page = inputs.section_selector()
    if selected_page == "input-section":
        return input_section(input_selection())
    elif selected_page == "scenarios-section":
        return scenarios_section
    elif selected_page == 'raw-results-section':
        if results():
            return raw_results_section(results_inputs_selection, global_raw_results)
        return raw_results_section_empty
    elif selected_page == 'indicators-section':
        if results():
            return indicators_section(results_inputs_selection, indicators)
        return indicators_section_empty
    elif selected_page == "visualizations-section":
        if indicators():
            return visualizations_section(
                graph_selection(), selected_countries(), scenarios_names()
            )
        return visualizations_section_empty
    elif selected_page == "documentation-section":
        return documentation_section(documentation_selection())
