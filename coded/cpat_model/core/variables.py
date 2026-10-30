"""The variable dictionary (NORMS 1.2): every coded row of Excel-AI's Mitigation sheet, with its variable stem,
fuel, sector, description and unit (core/variables.csv, written by cpat_testing/compare/extract_excel_ai.py).

    describe('ener')          -> description and unit of the stem
    code_of('ener', 'rod', 'gso')  -> 'mit.ener.rod.gso' (without country and scenario)
    slots()[('rtx', 'all', 'all')] -> 'rtx.tot.tot' (Excel-AI's code of the row)
"""
import csv
from functools import lru_cache
from pathlib import Path

PATH = Path(__file__).with_name('variables.csv')


@lru_cache(maxsize=1)
def rows():
    with open(PATH, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=1)
def stems():
    out = {}
    for r in rows():
        out.setdefault(r['variable'], dict(description=r['description'], unit=r['unit'], codes=[]))
        out[r['variable']]['codes'].append(r['code'])
    return out


def describe(stem):
    if stem not in stems():
        raise KeyError(f'{stem} is not a variable of Excel-AI (core/variables.csv)')
    return stems()[stem]


@lru_cache(maxsize=1)
def slots():
    """{(variable, sector, fuel): code without country and scenario}: Excel-AI's output code of each row, which is not
    always variable.sector.fuel (totals use 'tot' in some rows, some rows are renamed: rfu.all.coa -> rev.usd.tot.coa)."""
    out = {}
    for r in rows():
        code = r['code'].split('.', 2)[2].rsplit('.', 1)[0]
        out[(r['variable'], r['sector'] or None, r['fuel'] or None)] = code
    return out


def code_of(stem, *slots):
    return '.'.join(['mit', stem, *slots])
