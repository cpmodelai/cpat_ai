"""Tests of the data folder: every edition present (data/editions.csv), and the generic parts.

- tidy -> xlsx -> tidy gives back every value (numbers to 16 significant digits, openpyxl).
- The committed workbook <edition>/legacy_xlsx/CPAT_LegacyData.xlsx holds the values of <edition>/tidy/.
- Every tidy table is in data/catalog.csv and in <edition>/data_sources.csv; the proprietary tabs are the six.
- EDITION.json: public-perturbed only in this repository, checksums current; no table marked real; proprietary tables
  perturbed.
- The legacy shell (data/legacy/) has the six proprietary tabs empty below their headers; each edition's legacy copy holds
  exactly its tidy tables in those tabs.
- A row added in tidy form (a new country) comes back in the legacy table, in the legacy key case.
"""
import csv
import json
import os
import shutil
import sys
import tempfile

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   # data/
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

# pylint: disable=wrong-import-position
import build_edition as BE
import editions as ED
import tidy_convert as tc
from tidy_specs import LAYOUT_FILES

PROPRIETARY = {'Balances', 'EnergyCons', 'Prices_dom', 'HHSurvey', 'IO_GTAP', 'Tran_Scatter'}
EDITIONS = ED.present()
SHELL_HEADER_ROWS = {'Balances': 12, 'EnergyCons': 0, 'Prices_dom': 7, 'HHSurvey': 0, 'IO_GTAP': 0, 'Tran_Scatter': 0}


def rows(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


@pytest.mark.parametrize('edition', EDITIONS)
def test_round_trip(edition):
    d = tc.check(ED.tidy(edition))
    assert not d, d


@pytest.mark.parametrize('edition', EDITIONS)
def test_committed_xlsx_is_current(edition):
    want = {k: v for k, v in tc.from_tidy(ED.tidy(edition)).items() if k not in LAYOUT_FILES}
    with tempfile.TemporaryDirectory() as tmp:
        got = tc.from_tidy_via(tc.read_legacy(ED.legacy_xlsx(edition)), tmp)
    d = tc.compare(want, got, numeric=True, width=3)
    assert not d, f'{d}: rerun tidy_convert.py to-xlsx'


@pytest.mark.parametrize('edition', EDITIONS)
def test_catalog_covers_tidy(edition):
    tables = {r['table'] for r in rows(os.path.join(ED.tidy(edition), '_manifest.csv')) if r['kind'] != 'cells layout'}
    for path in (os.path.join(ROOT, 'catalog.csv'), os.path.join(ED.root(edition), 'data_sources.csv')):
        rs = rows(path)
        assert tables <= {r['tidy_file'][:-4] for r in rs if r['tidy_file']}, path
        assert {r['proprietary'] for r in rs} == {'proprietary', 'non-proprietary'}
        assert {r['excel_tab'] for r in rs if r['proprietary'] == 'proprietary'} == PROPRIETARY


@pytest.mark.parametrize('edition', EDITIONS)
def test_edition_manifest(edition):
    """Only public-perturbed editions here, each manifest describing its folder as it is."""
    with open(os.path.join(ED.root(edition), 'EDITION.json'), encoding='utf-8') as f:
        man = json.load(f)
    assert man['edition'] == edition and man['type'] == 'public-perturbed', man['type']
    assert man['files'] == BE.checksums(edition), f'data changed: rerun build_edition.py --edition {edition}'
    rs = rows(os.path.join(ED.root(edition), 'data_sources.csv'))
    assert {r['values'] for r in rs} <= {'public', 'perturbed', 'derived-real'}          # never real here
    assert all(r['values'] == 'perturbed' for r in rs if r['proprietary'] == 'proprietary')


def test_legacy_shell_is_empty():
    from pyxlsb import open_workbook
    with open_workbook(ED.SHELL) as wb:
        for tab, hr in SHELL_HEADER_ROWS.items():
            with wb.get_sheet(tab) as sh:
                n = sum(1 for r in sh.rows() for c in r if c.r > hr and c.v not in (None, ''))
            assert n == 0, f'{tab}: {n} values in the shell'


def test_added_country_comes_back():
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(ED.tidy(EDITIONS[0]), tmp, dirs_exist_ok=True)
        path = os.path.join(tmp, 'io_gtap.csv')
        rs = tc.read_csv(path)
        rs.append(['XEG', '2014', 'DOMCONS', 'afs', '1.5'])            # a new country, in tidy form
        tc.write_csv(path, rs[0], rs[1:])
        head, body = tc.from_tidy(tmp)['legacy_IO_GTAP.csv']
        new = [r for r in body if r[head.index('iso3')] == 'xeg']     # written back in the legacy (lower) case
        assert len(new) == 1 and new[0][head.index('afs')] == '1.5'


@pytest.mark.parametrize('edition', EDITIONS)
def test_legacy_copy_holds_the_edition(edition):
    """The edition's legacy workbook holds, in its six proprietary tabs, exactly the edition's tidy tables."""
    from pyxlsb import open_workbook
    import legacy_proprietary as LP
    tables = tc.from_tidy(ED.tidy(edition))
    with open_workbook(ED.legacy_filled(edition)) as wb:
        for tab, (src, hr) in LP.TABS.items():
            head, body = tables[src]
            with wb.get_sheet(tab) as sh:
                rows = {c.r: {} for r in sh.rows() for c in r}
                cols = {}
                for r in sh.rows():
                    for c in r:
                        if c.v not in (None, ''):
                            rows.setdefault(c.r, {})[c.c] = c.v
                            if c.r == hr:
                                cols[LP.label(c.v)] = c.c
            got = [r for r in sorted(rows) if r > hr and rows[r]]
            assert len(got) == len(body), f'{tab}: {len(got)} rows, tidy {len(body)}'
            for i, r in enumerate(body, hr + 1):
                for name, v in zip(head, r):
                    x = rows.get(i, {}).get(cols[name])
                    want = LP.as_value(v) if v != '' else None
                    assert x == want or (isinstance(x, float) and isinstance(want, float)
                                         and abs(x - want) <= 1e-12 * max(1, abs(want))), (tab, i, name, x, want)
