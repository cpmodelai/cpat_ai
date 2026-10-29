"""From the app's scenario table to a model run (coded/NORMS.md 4.1: the app builds the same scenario set as a file).

The scenario set is Excel-AI's (data/inputs/scenarios_excel_ai.csv):
    column 1             the Excel-AI baseline column (no carbon price)
    columns 2, 3, ...    one per scenario of the app: a copy of Excel-AI's carbon-tax scenario (column 2, "Carbon
                         price $20/tCO2 from 2027") with the app's inputs written over it (UI_INPUTS, coverage)
Then `cpat_model.run`; the app keeps the Results with the scenario names (ModelRun).
"""
from dataclasses import dataclass, field, replace

import pandas as pd

import cpat_model
from cpat_model.data import open_database
from cpat_model.inputs import ScenarioSet, read_scenario_set
from cpat_model.results import Results
from cpat_model.settings import Settings

from cpat_shiny.mapping import ALL_COUNTRIES, ALL_FUELS, ALL_SECTORS, BASELINE_SCENARIO

BASELINE_COLUMN = '1'
CARBON_TAX_COLUMN = '2'               # Excel-AI's carbon-tax-only scenario: the template of every app scenario

# app column -> NameOfParameter (MTInputs) it sets, value as typed
UI_INPUTS = {
    'CTintroYear': 'CPIntro',
    'CTtargetYear': 'CPOutro',
    'CTintroValue': 'CPLevelStart',
    'CTtargetValue': 'CPLevelTarget',
    'IntPricesSource': 'IntEnerPricForeSource',
}
# CTLinearProjection -> ExtendCarbonPriceBeyondOutro (legacy options No, Linear*, Percentage); SelectedFuels and
# SelectedSectors -> the coverage switches MCov<code> (coverage_input)
CT_AFTER_TARGET_OPTION = {'lin': 'Linear*', 'cst': 'No'}

# Countries are run only where the database has the country tables (the dummy database: Egypt only)
COUNTRY_TABLES = ['energy_balances', 'prices_domestic']


def coverage_input(code: str) -> str:
    """The MTInputs switch of a fuel or sector of the carbon tax: coa -> MCovCoa, pow -> MCovPow (MCovKer also
    covers jet fuel, as Excel-AI)."""
    return f'MCov{code.capitalize()}'


_COUNTRIES = {}                       # by database folder


def countries_with_data(settings: Settings | None = None) -> list[str]:
    """The countries of the database that the app can run (in every country table)."""
    settings = settings or Settings()
    folder = str(settings.tidy_path())
    if folder not in _COUNTRIES:
        db = open_database(settings)
        sets = [set(db.table(name)['country']) for name in COUNTRY_TABLES]
        _COUNTRIES[folder] = sorted(set.intersection(*sets) & set(ALL_COUNTRIES))
    return _COUNTRIES[folder]


@dataclass
class ModelRun:
    """A run of the app: the model's Results, the scenario names by number (1 = the baseline) and the countries."""
    results: Results
    names: dict                      # {scenario number: name}
    countries: list
    distribution_year: int | None = None
    _rows: dict = field(default_factory=dict, repr=False)

    def rows(self, country: str) -> pd.DataFrame:
        """Every result row of the country by output code (Results.by_code), the model years, as numbers."""
        if country not in self._rows:
            df = self.results.by_code(country)[self.results.settings.years]
            self._rows[country] = df.apply(pd.to_numeric, errors='coerce')
        return self._rows[country]

    def number(self, name: str) -> int:
        return next(n for n, s in self.names.items() if s == name)

    def policy_names(self) -> list[str]:
        return [s for n, s in self.names.items() if n != 1]


def text(value) -> str:
    """A value of the app as the text of an input cell (years and levels as numbers: 2027, 12.5)."""
    if isinstance(value, (int, float)):
        return f'{value:g}'
    return str(value)


def ui_values(scenario: pd.Series) -> dict:
    """{NameOfParameter: text} of one app scenario. An empty fuel or sector selection keeps the coverage of the
    Excel-AI carbon-tax scenario (all fuels; all sectors but other energy use)."""
    values = {name: text(scenario[col]) for col, name in UI_INPUTS.items()}
    values['ExtendCarbonPriceBeyondOutro'] = CT_AFTER_TARGET_OPTION[scenario['CTLinearProjection']]
    for chosen, every in ((scenario['SelectedFuels'], ALL_FUELS), (scenario['SelectedSectors'], ALL_SECTORS)):
        if len(chosen):
            values.update({coverage_input(code): 'TRUE' if code in chosen else 'FALSE' for code in every})
    values['ScenarioName'] = values['_ScenarioName'] = scenario['ScenarioName']
    values['_Countries'] = ' '.join(scenario['SelectedCountries'])
    return values


def one_value(df_scenarios: pd.DataFrame, column: str, what: str):
    """A value every scenario of a run must share (the baseline is run once for all of them)."""
    values = {tuple(v) if isinstance(v, (list, tuple)) else v for v in df_scenarios[column]}
    if len(values) != 1:
        raise ValueError(f'All scenarios of a run must have the same {what}.')
    return values.pop()


def scenario_set_from_ui(df_scenarios: pd.DataFrame, template: ScenarioSet | None = None) -> ScenarioSet:
    """The scenario set of the app's scenarios: column 1 the baseline, then one column per app scenario."""
    template = template or read_scenario_set()
    names = {r['name'] for r in template.rows}
    countries = one_value(df_scenarios, 'SelectedCountries', 'countries')
    price_source = one_value(df_scenarios, 'IntPricesSource', 'prices source')
    # the baseline uses the scenarios' price source, so that a scenario differs from it only by its policy
    columns = {BASELINE_COLUMN: {'IntEnerPricForeSource': price_source, '_Countries': ' '.join(countries)}}
    for i, (_, scenario) in enumerate(df_scenarios.iterrows()):
        columns[str(i + 2)] = {**ui_values(scenario), 'MSTScenarioID': str(i + 2)}
    unknown = {name for values in columns.values() for name in values} - names
    assert not unknown, f'not inputs of the scenario set: {sorted(unknown)}'

    rows = []
    for r in template.rows:
        row = {k: r[k] for k in ('row', 'name', 'label', 'unit') if k in r}
        row[BASELINE_COLUMN] = columns[BASELINE_COLUMN].get(r['name'], r[BASELINE_COLUMN])
        for col, values in columns.items():
            if col != BASELINE_COLUMN:
                row[col] = values.get(r['name'], r[CARBON_TAX_COLUMN])
        rows.append(row)
    return ScenarioSet(rows, list(columns))


def run_ui_scenarios(df_scenarios: pd.DataFrame, settings: Settings | None = None) -> ModelRun:
    """Run the app's scenarios against the baseline. ValueError (a message for the user) where they cannot run."""
    settings = settings or Settings()
    countries = list(one_value(df_scenarios, 'SelectedCountries', 'countries'))
    missing = [c for c in countries if c not in countries_with_data(settings)]
    if missing:
        raise ValueError(f'No data for {", ".join(ALL_COUNTRIES.get(c, c) for c in missing)} in the database '
                         f'({settings.database}); it has data for '
                         f'{", ".join(ALL_COUNTRIES[c] for c in countries_with_data(settings))}.')
    scenarios = scenario_set_from_ui(df_scenarios)
    results = cpat_model.run(scenarios, replace(settings, countries=tuple(countries)))
    names = {1: BASELINE_SCENARIO, **{i + 2: name for i, name in enumerate(df_scenarios['ScenarioName'])}}
    year = scenarios.inputs(1)['YearDistn'] if results.distribution else None
    run = ModelRun(results, names, countries, int(year) if year else None)
    for country in countries:                 # the result tables, once, while the progress bar shows
        run.rows(country)
    return run
