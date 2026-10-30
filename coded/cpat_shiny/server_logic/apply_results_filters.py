def apply_results_filters(
        global_raw_results,
        inputs,
        df_raw_results_to_render
        ) -> None:
    if global_raw_results():
        choice = inputs.raw_results_df_selection()
        if choice not in global_raw_results():
            choice = next(iter(global_raw_results()))

        ### filter inputs
        countries = list(inputs.raw_results_country_code())
        sectors = list(inputs.raw_results_sector_code())
        fuels = list(inputs.raw_results_fuel_code())
        scenarios = list(inputs.raw_results_scenario_name())
        df = global_raw_results()[choice]
        if countries:
            df = df[df.index.get_level_values('CountryCode').isin(countries)]
        if sectors:
            df = df[df.index.get_level_values('SectorCode').isin(sectors)]
        if fuels:
            df = df[df.index.get_level_values('FuelCode').isin(fuels)]
        if scenarios:
            df = df[df.index.get_level_values('ScenarioName').isin(scenarios)]

        df_raw_results_to_render.set(df.round(2).reset_index())

def apply_results_filters_indicators(
        indicators,
        inputs,
        df_indicators_to_render
        ) -> None:
    if indicators() is not None:
        ### filter inputs
        cpat_code = inputs.indicators_cpat_code()
        unit = list(inputs.indicators_unit())
        header = list(inputs.indicators_header())
        df = indicators()
        if cpat_code:
            df = df[df.index.get_level_values('CPATCode').str.contains(cpat_code, regex=False)]
        if unit:
            df = df[df['Unit'].isin(unit)]
        if header:
            df = df[df['Indicator header'].isin(header)]

        df_indicators_to_render.set(df.round(2).reset_index())
