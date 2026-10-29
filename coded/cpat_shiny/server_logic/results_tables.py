"""Tables of the app from the result rows of a run (Results.by_code): raw results by variable, indicators, Excel files.

A result row is keyed by its output code `<iso>.mit.<code>.<n>` (scenario n); core/variables.csv gives each code its
variable, sector, fuel and unit (coded/NORMS.md 6).
"""
from functools import lru_cache
from io import BytesIO

import pandas as pd

from cpat_model.core import variables

from cpat_shiny.mapping import ALL_INDICATORS, RESULT_ID_COLUMNS
from cpat_shiny.server_logic.run_model import ModelRun

# indicator -> (variable, sector, fuel) of its result row, and how a scenario is set against the baseline:
# 'pct' % change (strictly positive quantities only), 'abs' change in the row's unit, None the level only
INDICATOR_ROWS = {
    'cp': ('cptraj', None, None, None),
    'em': ('co2', 'all', 'all', 'pct'),
    'ec': ('ener', 'all', 'all', 'pct'),
    'rev': ('rtot', 'all', 'all', 'abs'),       # net revenue can be negative (subsidies): change, not %
    'gdp': ('gdp.pos.usd', 'all', 'all', 'pct'),
}
CHANGE_MEASURE = {'pct': '% change vs baseline', 'abs': 'Change vs baseline'}


@lru_cache(maxsize=1)
def code_table() -> pd.DataFrame:
    """Variable, sector, fuel and unit of each output code (without country, module and scenario: 'ener.rod.gso')."""
    rows = variables.rows()
    codes = [r['code'].split('.', 2)[2].rsplit('.', 1)[0] for r in rows]
    return pd.DataFrame({'variable': [r['variable'] for r in rows], 'sector': [r['sector'] for r in rows],
                         'fuel': [r['fuel'] for r in rows], 'unit': [r['unit'] for r in rows]}, index=codes)


def output_code(country: str, variable: str, sector: str | None, fuel: str | None, number: int) -> str:
    return f'{country.lower()}.mit.{variables.slots()[(variable, sector, fuel)]}.{number}'


def result_row(run: ModelRun, country: str, number: int, variable: str, sector=None, fuel=None) -> pd.Series:
    """One result row of scenario `number` over the model years."""
    return run.rows(country).loc[output_code(country, variable, sector, fuel, number)]


def result_rows(run: ModelRun, country: str, number: int, variable: str, keys: dict) -> pd.DataFrame:
    """Several rows of one variable: keys = {label: (sector, fuel)}; index = the labels, columns = years."""
    return pd.DataFrame({label: result_row(run, country, number, variable, *slot)
                         for label, slot in keys.items()}).T


# ---- raw results
def raw_results(run: ModelRun, chosen: list[str]) -> dict[str, pd.DataFrame]:
    """{variable: table} with every row of the variable (all countries and scenarios): index CountryCode,
    SectorCode, FuelCode, ScenarioName; columns CPATCode, Unit and the years."""
    tables = {v: [] for v in chosen}
    for country in run.countries:
        df = run.rows(country)
        stem = df.index.str.split('.', n=2).str[2].str.rsplit('.', n=1).str[0]
        number = df.index.str.rsplit('.', n=1).str[1].astype(int)
        info = code_table().reindex(stem)
        for v in chosen:
            pick = (info['variable'] == v).to_numpy()
            part = df[pick].copy()
            part.columns = [str(y) for y in part.columns]
            part.insert(0, 'Unit', info['unit'].to_numpy()[pick])
            part.insert(0, 'CPATCode', part.index)
            part.index = pd.MultiIndex.from_arrays(
                [[country] * pick.sum(), info['sector'].to_numpy()[pick], info['fuel'].to_numpy()[pick],
                 [run.names[n] for n in number[pick]]],
                names=[*RESULT_ID_COLUMNS, 'ScenarioName'])
            tables[v].append(part)
    return {v: pd.concat(parts).sort_index(level=RESULT_ID_COLUMNS, sort_remaining=False)
            for v, parts in tables.items()}


# ---- indicators
def indicators_table(run: ModelRun, chosen: list[str]) -> pd.DataFrame:
    """The chosen indicators of every country and scenario: the level, and for the policy scenarios the change
    against the baseline. Index CountryCode, ScenarioName, CPATCode; columns Indicator header, Measure, Unit, years."""
    records = []
    for country in run.countries:
        for key in chosen:
            variable, sector, fuel, change = INDICATOR_ROWS[key]
            unit = code_table().loc[variables.slots()[(variable, sector, fuel)], 'unit']
            baseline = result_row(run, country, 1, variable, sector, fuel)
            for number, name in run.names.items():
                code = output_code(country, variable, sector, fuel, number)
                level = result_row(run, country, number, variable, sector, fuel)
                records.append((country, name, code, ALL_INDICATORS[key], 'Level', unit, level))
                if number != 1 and change == 'pct':
                    records.append((country, name, code, ALL_INDICATORS[key], CHANGE_MEASURE[change], '%',
                                    (level / baseline - 1) * 100))
                elif number != 1 and change == 'abs':
                    records.append((country, name, code, ALL_INDICATORS[key], CHANGE_MEASURE[change], unit,
                                    level - baseline))
    index = pd.MultiIndex.from_tuples([r[:3] for r in records], names=['CountryCode', 'ScenarioName', 'CPATCode'])
    columns = pd.DataFrame([r[3:6] for r in records], index=index, columns=['Indicator header', 'Measure', 'Unit'])
    years = pd.DataFrame([r[6].to_numpy() for r in records], index=index, columns=[str(y) for y in records[0][6].index])
    return pd.concat([columns, years], axis=1)


# ---- files
def excel_bytes(tables: dict[str, pd.DataFrame]) -> bytes:
    """An Excel workbook with one sheet per table (sheet name = key)."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        for name, df in tables.items():
            df.to_excel(writer, sheet_name=name[:31])
    return buffer.getvalue()
