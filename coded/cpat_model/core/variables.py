"""The variable dictionary (NORMS 1.2): every coded row of Excel-AI's Mitigation sheet, with its variable stem,
fuel, sector, description and unit (core/variables.csv, written by cpat_testing/compare/extract_excel_ai.py).

    describe('ener')          -> description and unit of the stem
    code_of('ener', 'rod', 'gso')  -> 'mit.ener.rod.gso' (without country and scenario)
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


def code_of(stem, *slots):
    return '.'.join(['mit', stem, *slots])
