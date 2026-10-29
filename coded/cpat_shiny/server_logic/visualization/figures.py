"""The graphs of the Visualizations section, from the result rows of a run (one country, one policy scenario).

    ec_by_sector       fuel use by sector (ener.<sector>.all), baseline total as a line
    ec_by_fuel         fuel use by fuel (ener.all.<fuel>), baseline total as a line
    ec_change_by_fuel  change in fuel use against the baseline by fuel (echg.all.<fuel>)
    domestic_p         average price by fuel (pav.uv.all.<fuel>), base year = 100
    em_by_sector       CO2 emissions from fuel combustion by sector (co2.<sector>.all), baseline total as a line
    distribution       household effect by decile in the analysis year (distribution rows tef, rec, net)
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from cpat_shiny.mapping import ALL_COUNTRIES
from cpat_shiny.server_logic.results_tables import result_row, result_rows
from cpat_shiny.server_logic.run_model import ModelRun
from cpat_shiny.server_logic.visualization.graphs import Line, StackedArea, StackedColumn
from cpat_shiny.server_logic.visualization.graphs_titles import GRAPHS_TITLES

KTOE_PER_MTOE = 1000

# the sector groups of Excel-AI's summary rows
SECTORS = {'Power': ('pow', 'all'), 'Transport': ('tra', 'all'), 'Buildings': ('bld', 'all'),
           'Industry': ('ind', 'all'), 'Other': ('oen', 'all')}
FUELS = {'Coal': ('all', 'coa'), 'Natural gas': ('all', 'nga'), 'Gasoline': ('all', 'gso'),
         'Diesel': ('all', 'die'), 'LPG': ('all', 'lpg'), 'Kerosene': ('all', 'ker'), 'Jet fuel': ('all', 'jfu'),
         'Other oil products': ('all', 'oop'), 'Biomass': ('all', 'bio')}
PRICE_FUELS = {'Coal': ('all', 'coa'), 'Natural gas': ('all', 'nga'), 'Electricity': ('all', 'ecy'),
               'Other oil products': ('all', 'oop'), 'Diesel': ('all', 'die'), 'Gasoline': ('all', 'gso')}
# distribution rows (% of household consumption, the whole sample): price effect, revenue recycling, net effect
DISTRIBUTION_ROWS = {'Price effect': 'tef', 'Revenue recycling': 'rec', 'Net effect': 'net'}


def config(title: str, y_label: str = '') -> dict:
    return {'Title': title, 'YLabel': y_label}


def baseline_total(run: ModelRun, country: str, variable: str, scale: float = 1) -> pd.DataFrame:
    return result_row(run, country, 1, variable, 'all', 'all').to_frame('Baseline').T / scale


def ec_by_sector(run, country, number, title):
    scenario = result_rows(run, country, number, 'ener', SECTORS) / KTOE_PER_MTOE
    return StackedArea(config(title, 'Mtoe'), baseline_total(run, country, 'ener', KTOE_PER_MTOE), scenario).fig


def ec_by_fuel(run, country, number, title):
    scenario = result_rows(run, country, number, 'ener', FUELS) / KTOE_PER_MTOE
    return StackedArea(config(title, 'Mtoe'), baseline_total(run, country, 'ener', KTOE_PER_MTOE), scenario).fig


def ec_change_by_fuel(run, country, number, title):
    return StackedColumn(config(title), result_rows(run, country, number, 'echg', FUELS) / KTOE_PER_MTOE).fig


def domestic_p(run, country, number, title):
    prices = result_rows(run, country, number, 'pav.uv', PRICE_FUELS)
    base_year = run.results.settings.base_year
    return Line(config(title, f'{base_year} = 100'), prices.div(prices[base_year], axis=0) * 100).fig


def em_by_sector(run, country, number, title):
    scenario = result_rows(run, country, number, 'co2', SECTORS)
    return StackedArea(config(title, 'MtCO2'), baseline_total(run, country, 'co2'), scenario).fig


def distribution(run, country, number, title):
    rows = run.results.distribution_by_code(country)
    deciles = list(range(1, 11))
    codes = {label: f'{country.lower()}.distn.{v}.tot.dec.ove.{number}' for label, v in DISTRIBUTION_ROWS.items()}
    if not all(code in rows.index for code in codes.values()):
        return go.Figure().update_layout(title=title)
    df = pd.DataFrame({label: rows.loc[code, deciles].astype(float) for label, code in codes.items()})
    fig = px.bar(df, barmode='group', title=title,
                 labels={'index': 'Decile (1 = poorest)', 'value': '% of household consumption'})
    return fig.update_layout(legend_title_text='')


FIGURES = {'ec_by_sector': ec_by_sector, 'ec_by_fuel': ec_by_fuel, 'ec_change_by_fuel': ec_change_by_fuel,
           'domestic_p': domestic_p, 'em_by_sector': em_by_sector, 'distribution': distribution}


def figure(run: ModelRun, country: str, scenario_name: str, kind: str) -> go.Figure:
    """The graph `kind` of a policy scenario of the run."""
    title = GRAPHS_TITLES[kind].format(
        scenario_name=scenario_name, country=ALL_COUNTRIES[country],
        reference_year=run.results.settings.base_year, year=run.distribution_year)
    return FIGURES[kind](run, country, run.number(scenario_name), title)
