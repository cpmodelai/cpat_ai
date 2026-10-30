"""The tidy database: one CSV per table (data/README.md)."""
import csv
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


class Database:
    """The tables of one tidy folder. `table` gives a DataFrame (keys as text, `value` as float where numeric);
    `array` gives a labelled array of one table's values over its key columns."""

    def __init__(self, path):
        self.path = Path(path)
        with open(self.path / '_manifest.csv', encoding='utf-8', newline='') as f:
            self.tables = {r['table']: r for r in csv.DictReader(f) if r['kind'] != 'cells layout'}
        self._cache = {}

    def table(self, name):
        if name not in self.tables:
            raise KeyError(f'{name} is not a table of the data interface (data/<edition>/tidy/_manifest.csv)')
        if name not in self._cache:
            df = pd.read_csv(self.path / f'{name}.csv', dtype=str, keep_default_na=False)
            self._cache[name] = df
        return self._cache[name].copy()

    def values(self, name, keys, value='value', where=None):
        """A Series of `value` (float) indexed by the key columns `keys`, optionally filtered by {column: value}."""
        df = self.table(name)
        for col, v in (where or {}).items():
            df = df[df[col].isin(v if isinstance(v, (list, tuple, set)) else [v])]
        return pd.Series(to_float(df[value]).values, index=pd.MultiIndex.from_frame(df[keys]) if len(keys) > 1
                         else pd.Index(df[keys[0]]), name=value)

    def array(self, name, dims, value='value', where=None):
        """A labelled array (xarray) of `value` over the key columns `dims` (missing combinations: NaN)."""
        s = self.values(name, dims, value, where)
        return xr.DataArray.from_series(s)


def to_float(col):
    """Text -> float: blank -> NaN; a non-numeric text stays NaN (keep text columns as text with table()). Exact:
    Python's float() reads every decimal text to the nearest double (pandas' to_numeric can be 1e-16 relative off)."""
    def number(x):
        try:
            return float(x) if x != '' else np.nan
        except (TypeError, ValueError):
            return np.nan
    return pd.Series([number(x) for x in col], index=getattr(col, 'index', None), dtype=float)


@lru_cache(maxsize=4)
def _open(path):
    return Database(path)


def open_database(settings):
    return _open(str(settings.tidy_path()))


BASE_TABLES = ['energy_balances', 'prices_domestic']   # a country runs only with its base-year energy use and prices


def missing_country_data(db, countries):
    """{country: [base tables without its rows]}: empty when every country can run. Only Egypt has them in the dummy
    database; the full database (private) has every country."""
    have = {t: set(db.table(t)['country']) for t in BASE_TABLES}
    return {iso: [t for t in BASE_TABLES if iso not in have[t]] for iso in countries
            if any(iso not in have[t] for t in BASE_TABLES)}

