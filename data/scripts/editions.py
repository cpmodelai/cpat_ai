"""The data editions (data/editions.csv) and the paths inside one: every script that reads or writes data uses this.

An edition is a folder with the same structure in every edition (data/README.md):
    <edition>/EDITION.json, data_sources.csv, tidy/, legacy_xlsx/CPAT_LegacyData.xlsx,
    legacy/CPAT 1.0pre_465_<edition>.xlsb, inputs/
The edition used: the argument, else the environment variable CPAT_DATA_EDITION, else the default row of
data/editions.csv. An edition outside this repository (Full01, in the private data repository) is found through the
environment variable CPAT_DATA_<EDITION> (e.g. CPAT_DATA_FULL01=/path/to/Full01).
"""
import csv
import os

DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.dirname(DATA)
REGISTRY = os.path.join(DATA, 'editions.csv')
SHELL = os.path.join(DATA, 'legacy', 'CPAT 1.0pre_465_Shell.xlsb')   # the legacy model, six proprietary tabs empty
LEGACY_BASE = 'CPAT 1.0pre_465'


def registry():
    with open(REGISTRY, encoding='utf-8') as f:
        return {r['edition']: r for r in csv.DictReader(f)}


def name(edition=None):
    if edition:
        return edition
    if os.environ.get('CPAT_DATA_EDITION'):
        return os.environ['CPAT_DATA_EDITION']
    return next(e for e, r in registry().items() if r['default'] == 'yes')


def root(edition=None):
    """The edition's folder: in data/, or where CPAT_DATA_<EDITION> points."""
    e = name(edition)
    env = os.environ.get(f'CPAT_DATA_{e.upper()}')
    if env:
        return os.path.abspath(env)
    p = os.path.join(DATA, e)
    if not os.path.isdir(p):
        raise FileNotFoundError(f'edition {e}: no folder {p}; set CPAT_DATA_{e.upper()} to its path')
    return p


def info(edition=None):
    return registry()[name(edition)]


def tidy(edition=None):
    return os.path.join(root(edition), 'tidy')


def legacy_xlsx(edition=None):
    return os.path.join(root(edition), 'legacy_xlsx', 'CPAT_LegacyData.xlsx')


def legacy_filled(edition=None):
    return os.path.join(root(edition), 'legacy', f'{LEGACY_BASE}_{name(edition)}.xlsb')


def inputs(edition=None):
    return os.path.join(root(edition), 'inputs')


def present():
    """The editions whose folder is here (tests run on each)."""
    out = []
    for e in registry():
        try:
            root(e)
            out.append(e)
        except FileNotFoundError:
            pass
    return out
