from typing import Union, Dict, List, Tuple
from shiny import ui
import pandas as pd
from htmltools import Tag

from cpat_shiny.ui.components.common.section_empty import section_empty
from cpat_shiny.mapping import (
    ALL_COUNTRIES, ALL_SECTORS, ALL_FUELS, CT_AFTER_TARGET_YEAR, SCENARIOS_COLUMNS
)
from cpat_shiny.ui.labels import COMMON, SCENARIO_CARDS

def get_scenario_rows(
        df_scenarios: pd.DataFrame
        ) -> List[Dict[str, Union[str, int, Tuple[str]]]]:

    rows = []
    for index, row in df_scenarios.iterrows():
        rows.append(
            {
                'index': index,
                **{col: row[col] for col in SCENARIOS_COLUMNS}
            }
        )
    return rows

def map_props(
        props
        ) -> Dict[str, str]:
    countries = ', '.join([ALL_COUNTRIES[code] for code in props['SelectedCountries']])
    sectors = ', '.join([ALL_SECTORS[code] for code in props['SelectedSectors']])
    fuels = ', '.join([ALL_FUELS[code] for code in props['SelectedFuels']])
    ct_after_target_year = CT_AFTER_TARGET_YEAR[props['CTLinearProjection']]
    return {
        "Countries": countries,
        "Sectors": sectors,
        "Fuels": fuels,
        "CTProjection": ct_after_target_year
    }

def prop_column(
        width: int,
        prop_name: str,
        prop_value: Union[int, str],
        with_margin: bool = True
        ) -> Tag:
    return ui.column(
        width,
        ui.div(
            ui.row(ui.h5(prop_name)),
            ui.row(
                ui.p(
                    prop_value,
                    {"style": "margin-bottom: 16px;"} if with_margin else {},
                ),
            ),
        ),
    )

def scenario_card(
        props
        ) -> Tag:
    mapped_props = map_props(props)
    card =  ui.card(
        ui.card_header(
            ui.h3(props['ScenarioName'])
            ),
        ui.div(
            ui.h5(SCENARIO_CARDS["countries"]),
            ui.p(mapped_props['Countries']),
            ui.hr(),
            ui.row(
                prop_column(3, COMMON["startCTYear"], props['CTintroYear']),
                prop_column(3, COMMON["targetCTYear"], props['CTtargetYear']),
                prop_column(3, COMMON["startCTLevel"], props['CTintroValue']),
                prop_column(3, COMMON["targetCTLevel"], props['CTtargetValue']),
            ),
            ui.row(
                prop_column(3, COMMON["afterTargetCT"], mapped_props['CTProjection'], False),
                prop_column(3, COMMON["pricesSourceSelection"], props['IntPricesSource'], False),
            ),
            ui.hr(),
            ui.h5(SCENARIO_CARDS["selectedFuels"]),
            ui.p(mapped_props['Fuels']),
            ui.hr(),
            ui.h5(SCENARIO_CARDS["selectedSectors"]),
            ui.p(mapped_props['Sectors']),
        ),
        ui.card_footer( # TODO fix remove scenario (and remove fixed height)
            # ui.input_action_button(
            #     id=f"remove_scenario_{props['index']}",
            #     label=SCENARIO_CARDS["removeScenario"]
            # )
            style="""
                height: 50px;
            """
        ),
        height='200px',
        full_screen=True,
    )
    return card

def scenarios_container(
        df_scenarios: pd.DataFrame
        ) -> Tag:
    rows = get_scenario_rows(df_scenarios)
    if rows:
        return ui.div(
                *[
                    scenario_card(row) for row in rows
                ]
        )
    return section_empty(SCENARIO_CARDS["scenariosEmpty"])
