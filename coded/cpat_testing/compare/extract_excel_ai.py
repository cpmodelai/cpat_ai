"""Extract from the shipped Excel-AI workbook (its stored values; no recalculation, D8 as decided 2026-10-29):

  data/inputs/scenarios_excel_ai.csv                 its ScenarioDefinition: every MTInputs row, scenarios 1-6,
                                                     plus the Python rows below (cpat_model.inputs.scenarios)
  cpat_testing/compare/reference/excel_ai_<v>.csv    every coded row of sheet Mitigation, scenario groups 1 and 2,
                                                     years as columns: the reference values of the comparison
  cpat_model/core/variables.csv                      the variable dictionary: every coded Mitigation row's variable,
                                                     fuel, sector, description, unit and code (scenario 1)
  data/mvp_legacy_extracts/module_<Tab>_cells.csv    the typed module values of tabs FromAirPollution and
                                                     FromTransportCB (row, col, value), for the placeholder modules
  cpat_model/core/excel_ai/<table>.csv               the model's own tables on Excel-AI's Settings tab (named
                                                     constants, the input rows read by Mitigation, coverage sectors,
                                                     main scenarios, ETS volatility): structure, not country data
  cpat_testing/compare/reference/excel_ai_<v>_inputs.csv   the stored values of sheet Inputs (row, col, value): the
                                                     reference of the data steps
  data/excel_ai_stored/<table>.csv                   values Excel-AI stores from a scenario-1 run (BaselineCO2), read
                                                     as data until Python computes them (user 2026-10-29)
  cpat_testing/compare/reference/excel_ai_distribution_<v>.csv   every coded row of sheet Distribution of the
                                                     distribution module, scenario groups 1 and 2, columns 0
                                                     (basket) and deciles 1-10 (python ... --distribution)
  cpat_model/core/excel_ai/distribution_rows.csv     the Distribution rows: variable, item, sample, parameters, code

Run from coded/:  python cpat_testing/compare/extract_excel_ai.py
"""
import csv
import sys
from pathlib import Path

import openpyxl

CODED = Path(__file__).resolve().parents[2]
REPO = CODED.parent
sys.path.insert(0, str(CODED))
from cpat_model import EXCEL_AI_VERSION  # noqa: E402
from cpat_model.inputs.scenarios import PYTHON_ROWS  # noqa: E402

WORKBOOK = REPO / 'excel_ai' / f'CPAT-AI-Mitigation-Prototype_v{EXCEL_AI_VERSION}.xlsm'
SCENARIOS = REPO / 'data' / 'inputs' / 'scenarios_excel_ai.csv'
REFERENCE = CODED / 'cpat_testing' / 'compare' / 'reference' / f'excel_ai_{EXCEL_AI_VERSION}.csv'
SD_FIRST, SD_LAST, SD_COLS = 8, 600, range(10, 16)          # ScenarioDefinition rows, columns J-O (scenarios 1-6)
GROUPS = [(11, 1), (33, 2)]                                  # Mitigation: code column K, AG; years follow (20)


def text(v):
    if v is None:
        return ''
    if isinstance(v, bool):
        return 'TRUE' if v else 'FALSE'
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() and abs(v) < 1e15 else repr(v)
    return str(v)


def scenarios(wb):
    ws = wb['ScenarioDefinition']
    rows = list(ws.iter_rows(min_row=1, max_row=SD_LAST, values_only=True))
    names = [text(rows[5][c - 1]) for c in SD_COLS]            # row 6: scenario names
    out = [['', '_ScenarioName', 'Scenario name', ''] + names,
           ['', '_Countries', 'Countries', 'ISO3'] + ['EGY'] * len(SD_COLS)]
    last = SD_FIRST
    for i in range(SD_FIRST - 1, len(rows)):
        r = rows[i]
        if any(v not in (None, '') for v in r[:15]):
            last = i + 1
    for i in range(SD_FIRST - 1, last):
        r = rows[i]
        out.append([str(i + 1), text(r[7]), text(r[1]), text(r[2])] + [text(r[c - 1]) for c in SD_COLS])
    for name, label, unit, default in PYTHON_ROWS:
        out.append(['', name, label, unit] + [default] * len(SD_COLS))
    head = ['row', 'name', 'label', 'unit'] + [str(n) for n in range(1, len(SD_COLS) + 1)]
    with open(SCENARIOS, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([head] + out)
    return len(out)


def reference(wb):
    ws = wb['Mitigation']
    rows = list(ws.iter_rows(values_only=True))
    years = [int(y) for y in rows[0][11:31]]
    out, seen = [], set()
    for r in rows:
        for col, _n in GROUPS:
            code = r[col - 1]
            if isinstance(code, str) and code.count('.') >= 2 and code not in seen:   # section 19 repeats codes
                seen.add(code)
                out.append([code] + [text(v) for v in r[col:col + 20]])
    with open(REFERENCE, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([['code'] + years] + out)
    return len(out)


VARIABLES = CODED / 'cpat_model' / 'core' / 'variables.csv'


def variables(wb):
    rows = list(wb['Mitigation'].iter_rows(max_col=11, values_only=True))
    out, seen = [], set()
    for r in rows:
        code = r[10]
        if isinstance(code, str) and code.count('.') >= 2 and code.endswith('.1') and code not in seen:
            seen.add(code)
            out.append([text(r[0]), text(r[1]), text(r[2]), text(r[7]), text(r[8]), code])
    with open(VARIABLES, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([['variable', 'fuel', 'sector', 'description', 'unit', 'code']]
                                                     + out)
    return len(out)


def module_tabs(wb):
    for tab in ('FromAirPollution', 'FromTransportCB'):
        cells = [[r, c, text(v)] for r, row in enumerate(wb[tab].iter_rows(values_only=True), 1)
                 for c, v in enumerate(row, 1) if v not in (None, '')]
        out = REPO / 'data' / 'mvp_legacy_extracts' / f'module_{tab}_cells.csv'
        with open(out, 'w', encoding='utf-8', newline='') as f:
            csv.writer(f, lineterminator='\n').writerows([['row', 'col', 'value']] + cells)
        print(f'{tab}: {len(cells)} cells -> {out}')


STRUCTURE = CODED / 'cpat_model' / 'core' / 'excel_ai'
SETTINGS_TABLES = {   # name: (first row, last row, columns {sheet column: csv column}) of sheet Settings
    'constants': (97, 178, {1: 'key', 2: 'value', 3: 'unit', 4: 'description', 5: 'source'}),
    'input_rows': (333, 743, {1: 'key', 2: 'name'}),
    'coverage_sectors': (746, 762, {1: 'sector', 2: 'position', 3: 'ets_group', 5: 'feebate_sector',
                                    7: 'semi_group'}),
    'main_scenarios': (819, 832, {1: 'selected', 2: 'name', 3: 'explicit', 4: 'adjustment',
                                  **{c: s for c, s in zip(range(5, 22), ['pow', 'rod', 'ral', 'avi', 'nav', 'res', 'foo',
                                     'srv', 'mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr', 'oen'])},
                                  22: 'power_rebated', 23: 'electricity_excise'}),
    'ets_volatility': (16, 18, {2: 'item', 3: 'Medium', 4: 'High', 5: 'Low', 6: 'Zero'}),
    'fuels': (229, 237, {1: 'fuel', 2: 'name', 3: 'elasticity_fuel', 4: 'aeei_fuel', 5: 'price_rule', 6: 'unit',
                         7: 'gj_per_unit', 8: 'position', 9: 'price_fuel'}),
    'subsectors': (186, 201, {1: 'sector', 2: 'name', 3: 'group', 4: 'elasticity_sector', 5: 'ef_sector',
                              6: 'price_sector', 7: 'feebate_sector', 8: 'coverage_position', 9: 'ecp_sector',
                              10: 'flow1', 11: 'sign1', 12: 'flow2', 13: 'sign2'}),
}


def write(path, head, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([head] + rows)


def structure(wb):
    rows = list(wb['Settings'].iter_rows(max_row=900, max_col=30, values_only=True))
    for name, (a, b, cols) in SETTINGS_TABLES.items():
        out = [[text(rows[r - 1][c - 1]) for c in cols] for r in range(a, b + 1)]
        out = [o for o in out if o[0]]
        write(STRUCTURE / f'{name}.csv', list(cols.values()), out)
        print(f'{name}: {len(out)} rows')


INPUTS_REF = CODED / 'cpat_testing' / 'compare' / 'reference' / f'excel_ai_{EXCEL_AI_VERSION}_inputs.csv'


def inputs_reference(wb):
    cells = [[r, c, text(v)] for r, row in enumerate(wb['Inputs'].iter_rows(values_only=True), 1)
             for c, v in enumerate(row, 1) if v not in (None, '')]
    write(INPUTS_REF, ['row', 'col', 'value'], cells)
    print(f'Inputs: {len(cells)} cells')


def stored(wb):
    rows = list(wb['BaselineCO2'].iter_rows(min_row=3, values_only=True))
    years = [int(y) for y in rows[0][3:] if y is not None]
    out = [[r[0].split('|')[0], r[0].split('|', 1)[1], y, text(v)] for r in rows[1:] if r[0]
           for y, v in zip(years, r[3:3 + len(years)]) if v is not None]
    write(REPO / 'data' / 'excel_ai_stored' / 'baseline_co2.csv', ['country', 'key', 'year', 'value'], out)
    print(f'baseline_co2: {len(out)} values')


DISTRIBUTION_VERSION = '0.1.3'           # the Excel-AI distribution module replicated (user 2026-10-29)
DIST_WORKBOOK = REPO / 'excel_ai' / f'CPAT-AI-Distribution-Prototype_v{DISTRIBUTION_VERSION}.xlsm'
DIST_REFERENCE = CODED / 'cpat_testing' / 'compare' / 'reference' / f'excel_ai_distribution_{DISTRIBUTION_VERSION}.csv'
DIST_GROUPS = [(11, 1), (24, 2)]                            # Distribution: code column K, X; columns 0-10 follow


def distribution(wb):
    """The Distribution sheet: reference values by code (both groups) and the row table (group 1 codes)."""
    rows = list(wb['Distribution'].iter_rows(values_only=True))
    ref, table = [], []
    for i, r in enumerate(rows, 1):
        for col, n in DIST_GROUPS:
            code = r[col - 1]
            if isinstance(code, str) and code.count('.') >= 2:
                ref.append([code] + [text(v) for v in r[col:col + 11]])
                if n == 1:
                    table.append([i, text(r[0]), text(r[1]), text(r[2]), text(r[3]), text(r[4]), code.rsplit('.', 1)[0]])
    write(DIST_REFERENCE, ['code'] + [str(d) for d in range(11)], ref)
    write(STRUCTURE / 'distribution_rows.csv', ['row', 'variable', 'item', 'sample', 'param_d', 'param_e', 'code'], table)
    print(f'distribution: {len(ref)} codes, {len(table)} rows')


if __name__ == '__main__' and '--distribution' in sys.argv:
    distribution(openpyxl.load_workbook(DIST_WORKBOOK, read_only=True, data_only=True))
elif __name__ == '__main__':
    book = openpyxl.load_workbook(WORKBOOK, read_only=True, data_only=True)
    print('scenario rows:', scenarios(book), '->', SCENARIOS)
    print('reference codes:', reference(book), '->', REFERENCE)
    print('variables:', variables(book), '->', VARIABLES)
    module_tabs(book)
    structure(book)
    stored(book)
    inputs_reference(book)
