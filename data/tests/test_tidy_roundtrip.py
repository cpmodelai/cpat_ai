"""Tests for data/scripts/tidy/tidy_convert.py: legacy layout <-> tidy CSV.

- Every file of the data interface (data/interface_manifest.csv) has a spec, and every spec'd file exists.
- legacy CSV -> tidy -> legacy CSV gives back every cell exactly; through the legacy-style workbook, every value
  (numbers to 16 significant digits, openpyxl).
- The committed tidy database data/tidy/ equals a fresh conversion of data/mvp_legacy_extracts/.
- A row added in tidy form (a new country) comes back in the legacy table, in the legacy key case.
"""
import csv
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   # data/
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'tidy'))

# pylint: disable=wrong-import-position
import tidy_convert as tc
from tidy_specs import CELLS, LAYOUT_FILES, TABLES

LEGACY = os.path.join(ROOT, 'mvp_legacy_extracts')
TIDY = os.path.join(ROOT, 'tidy')


def test_specs_cover_the_interface():
    with open(os.path.join(ROOT, 'interface_manifest.csv'), encoding='utf-8') as f:
        files = {r['file'] for r in csv.DictReader(f)}
    covered = set(TABLES) | set(CELLS) | set(LAYOUT_FILES)
    assert files <= covered, files - covered
    for name in list(TABLES) + list(CELLS):
        assert os.path.exists(os.path.join(LEGACY, name)), name


def test_round_trip():
    d_csv, d_xlsx = tc.check(LEGACY)
    assert not d_csv, d_csv
    assert not d_xlsx, d_xlsx


def test_committed_tidy_is_current():
    with tempfile.TemporaryDirectory() as tmp:
        tc.to_tidy(tc.read_legacy(LEGACY), tmp)
        for dirpath, _dirs, files in os.walk(tmp):
            for name in files:
                rel = os.path.relpath(os.path.join(dirpath, name), tmp)
                with open(os.path.join(tmp, rel), encoding='utf-8') as a, \
                        open(os.path.join(TIDY, rel), encoding='utf-8') as b:
                    assert a.read() == b.read(), f'data/tidy/{rel} is stale: rerun tidy_convert.py to-tidy'


def test_added_country_comes_back():
    with tempfile.TemporaryDirectory() as tmp:
        tc.to_tidy({'legacy_IO_GTAP.csv': tc.read_legacy(LEGACY)['legacy_IO_GTAP.csv']}, tmp)
        path = os.path.join(tmp, 'io_gtap.csv')
        rows = tc.read_csv(path)
        rows.append(['XEG', '2014', 'DOMCONS', 'afs', '1.5'])          # a new country, in tidy form
        tc.write_csv(path, rows[0], rows[1:])
        head, body = tc.from_tidy(tmp)['legacy_IO_GTAP.csv']
        new = [r for r in body if r[head.index('iso3')] == 'xeg']     # written back in the legacy (lower) case
        assert len(new) == 1 and new[0][head.index('afs')] == '1.5'
