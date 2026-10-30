from shiny import reactive

from cpat_shiny.mapping import ALL_FUELS, ALL_SECTORS

input_selection = reactive.value({
        "scenario_name_input": "",
        "countries_input": (),
        "start_year": 2024,
        "target_year": 2030,
        "start_level": 0,
        "target_level": 10,
        "ct_projection": 'lin',
        "prices_source_selection": "IMF-WB",
        "fuels_input": (),
        "sectors_input": ()
    })

def create_update_scenario_name(inputs):
    @reactive.effect
    @reactive.event(inputs.scenario_name_input)
    def _():
        current_selection = input_selection.get()
        current_selection['scenario_name_input'] = inputs.scenario_name_input()
        input_selection.set(current_selection)

def create_update_countries(inputs):
    @reactive.effect
    @reactive.event(inputs.countries_input)
    def _():
        current_selection = input_selection.get()
        current_selection['countries_input'] = inputs.countries_input()
        input_selection.set(current_selection)

def create_update_start_year(inputs):
    @reactive.effect
    @reactive.event(inputs.start_year)
    def _():
        current_selection = input_selection.get()
        current_selection['start_year'] = inputs.start_year()
        input_selection.set(current_selection)

def create_update_target_year(inputs):
    @reactive.effect
    @reactive.event(inputs.target_year)
    def _():
        current_selection = input_selection.get()
        current_selection['target_year'] = inputs.target_year()
        input_selection.set(current_selection)

def create_update_start_level(inputs):
    @reactive.effect
    @reactive.event(inputs.start_level)
    def _():
        current_selection = input_selection.get()
        current_selection['start_level'] = inputs.start_level()
        input_selection.set(current_selection)

def create_update_target_level(inputs):
    @reactive.effect
    @reactive.event(inputs.target_level)
    def _():
        current_selection = input_selection.get()
        current_selection['target_level'] = inputs.target_level()
        input_selection.set(current_selection)

def create_update_ct_projection(inputs):
    @reactive.effect
    @reactive.event(inputs.ct_projection)
    def _():
        current_selection = input_selection.get()
        current_selection['ct_projection'] = inputs.ct_projection()
        input_selection.set(current_selection)

def create_update_prices_source_selection(inputs):
    @reactive.effect
    @reactive.event(inputs.prices_source_selection)
    def _():
        current_selection = input_selection.get()
        current_selection['prices_source_selection'] = inputs.prices_source_selection()
        input_selection.set(current_selection)

def create_update_fuels(inputs, session):
    @reactive.effect
    @reactive.event(inputs.fuels_input)
    def _():
        selected = inputs.fuels_input()
        if "all" in selected:
            session.send_input_message("fuels_input", {"value": list(ALL_FUELS.keys())})
        current_selection = input_selection.get()
        current_selection['fuels_input'] = inputs.fuels_input()
        input_selection.set(current_selection)

def create_update_sectors(inputs, session):
    @reactive.effect
    @reactive.event(inputs.sectors_input)
    def _():
        selected = inputs.sectors_input()
        if "all" in selected:
            session.send_input_message("sectors_input", {"value": list(ALL_SECTORS.keys())})
        current_selection = input_selection.get()
        current_selection['sectors_input'] = inputs.sectors_input()
        input_selection.set(current_selection)
