"""Task 6.2: the Shiny app runs on cpat_model.run. The app imports; its scenario table becomes a scenario set (the
Excel-AI baseline and carbon-tax columns with the app's inputs); a run gives results for every app scenario; the raw
results, indicators and graphs of the app are built from the result rows."""
import pandas as pd
import pytest

from cpat_shiny.mapping import ALL_FUELS, ALL_INDICATORS, CPAT_VARIABLES
from cpat_shiny.server_logic.results_tables import excel_bytes, indicators_table, raw_results
from cpat_shiny.server_logic.run_model import countries_with_data, run_ui_scenarios, scenario_set_from_ui
from cpat_shiny.server_logic.visualization.figures import FIGURES, figure


def ui_scenarios(**changes) -> pd.DataFrame:
    """Two scenarios as the app's scenario table holds them (Manual inputs or a loaded csv)."""
    df = pd.DataFrame({
        'ScenarioName': ['CT 20', 'Road 10 to 50'],
        'SelectedCountries': [('EGY',), ('EGY',)],
        'CTintroYear': [2027, 2026], 'CTtargetYear': [2030, 2035],
        'CTintroValue': [20, 10], 'CTtargetValue': [20, 50],
        'CTLinearProjection': ['lin', 'cst'], 'IntPricesSource': ['IMF', 'IMF'],
        'SelectedFuels': [tuple(ALL_FUELS), ()], 'SelectedSectors': [(), ('rod',)],
    })
    return df.assign(**changes)


@pytest.fixture(scope='module')
def run():
    return run_ui_scenarios(ui_scenarios())


def test_app_imports():
    import app
    assert app.app is not None


def test_countries_with_data_are_the_database_countries():
    assert countries_with_data() == ['EGY']                  # the dummy database: Egypt only


def test_scenario_set_from_the_app_table():
    s = scenario_set_from_ui(ui_scenarios())
    assert s.cols == ['1', '2', '3']
    base, ct, road = s.inputs(1), s.inputs(2), s.inputs(3)
    assert base['CPLevelTarget'] == 0 and base.text('IntEnerPricForeSource') == 'IMF'
    assert (road['CPIntro'], road['CPOutro'], road['CPLevelStart'], road['CPLevelTarget']) == (2026, 2035, 10, 50)
    assert road.text('ExtendCarbonPriceBeyondOutro') == 'No' and ct.text('ExtendCarbonPriceBeyondOutro') == 'Linear*'
    assert road.name == 'Road 10 to 50' and road.countries == ['EGY']
    # sector coverage: only road; fuels not chosen keep the Excel-AI carbon-tax coverage (all fuels)
    assert road.text('MCovRod') == 'TRUE' and road.text('MCovPow') == 'FALSE' and road.text('MCovCoa') == 'TRUE'
    assert ct.text('MCovPow') == 'TRUE' and ct.text('MCovOen') == 'FALSE'


def test_scenarios_of_a_run_share_countries_and_price_source():
    with pytest.raises(ValueError, match='prices source'):
        scenario_set_from_ui(ui_scenarios(IntPricesSource=['IMF', 'WB']))
    with pytest.raises(ValueError, match='No data'):
        run_ui_scenarios(ui_scenarios(SelectedCountries=[('USA',), ('USA',)]))


def test_run_gives_results_for_every_app_scenario(run):
    assert run.names == {1: 'Baseline', 2: 'CT 20', 3: 'Road 10 to 50'}
    rows = run.rows('EGY')
    carbon_price = rows.loc[['egy.mit.cptraj.1', 'egy.mit.cptraj.2', 'egy.mit.cptraj.3'], [2026, 2030, 2035, 2040]]
    assert carbon_price.values.tolist() == [[0, 0, 0, 0], [0, 20, 20, 20], [10, pytest.approx(27.7777778), 50, 50]]
    co2 = rows.loc[['egy.mit.co2.tot.tot.1', 'egy.mit.co2.tot.tot.2', 'egy.mit.co2.tot.tot.3'], 2035]
    assert co2.iloc[1] < co2.iloc[2] < co2.iloc[0]             # all-sector tax cuts more than the road-only tax


def test_raw_results_and_indicators(run):
    tables = raw_results(run, list(CPAT_VARIABLES))
    assert set(tables) == set(CPAT_VARIABLES)
    for df in tables.values():
        assert len(df) and set(df.index.get_level_values('ScenarioName')) == set(run.names.values())
    table = indicators_table(run, list(ALL_INDICATORS))
    assert set(table['Indicator header']) == set(ALL_INDICATORS.values())
    co2_change = table[(table['Indicator header'] == 'CO2 emissions') & (table['Measure'] != 'Level')]
    assert (co2_change['2035'] < 0).all()
    assert excel_bytes(tables)[:2] == b'PK'                   # an xlsx file


@pytest.mark.parametrize('kind', list(FIGURES))
def test_graphs_have_data(run, kind):
    fig = figure(run, 'EGY', 'Road 10 to 50', kind)
    assert fig.data and all(len(trace.y) for trace in fig.data)
