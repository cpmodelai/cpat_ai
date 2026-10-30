"""The model's own tables that Excel-AI keeps on its Settings tab (structure, not country data), extracted from the
shipped workbook by cpat_testing/compare/extract_excel_ai.py into core/excel_ai/:

    constants         named constants (key, value, unit, description, source)
    input_rows        the scenario inputs read by the Mitigation sheet: key variable|fuel|sector -> NameOfParameter
    coverage_sectors  the 17 coverage sectors: ETS benchmark group, feebate sector, semi-elasticity group
    main_scenarios    MTInputs ScenarioSelected: explicit pricing, efficiency adjustment, sectors with a shadow price
    ets_volatility    ETS price volatility and its impact, by MTInputs label
"""
import csv
from functools import lru_cache
from pathlib import Path

FOLDER = Path(__file__).with_name('excel_ai')


@lru_cache(maxsize=None)
def table(name):
    with open(FOLDER / f'{name}.csv', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=None)
def constants():
    """{key: float or text}: Excel-AI's named constants (MperBn, Thousand, ...)."""
    out = {}
    for r in table('constants'):
        try:
            out[r['key']] = float(r['value'])
        except ValueError:
            out[r['key']] = r['value']
    return out


def constant(key):
    return constants()[key]
