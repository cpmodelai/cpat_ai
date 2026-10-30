"""Typed module values by key `<ISO3>|<code>[|...]`, as labelled arrays over the run's countries (0 where a country
has no value: Excel-AI's module tabs give 0 to every country but Egypt, issue I106)."""
import numpy as np
import xarray as xr

from cpat_model.data.database import to_float


def keyed_array(db, table, countries, label, prefix_parts=2):
    """Rows keyed `ISO|code|...`; returns {code: DataArray(country, <label>)}."""
    df = db.table(table)
    parts = df['key'].str.split('|', expand=True)
    df['country'], df['code'] = parts[0], parts[1] if prefix_parts == 2 else parts[1] + '.' + parts[2]
    df['v'] = to_float(df['value'])
    out = {}
    for code, g in df.groupby('code'):
        arr = xr.DataArray.from_series(g.set_index(['country', label])['v'])
        arr = arr.reindex(country=list(countries)).fillna(0.0)
        out[code] = arr
    return out


def as_year(arr):
    return arr.assign_coords(year=arr['year'].astype(int)) if 'year' in arr.dims else arr


def zeros(countries, **dims):
    shape = [len(countries)] + [len(v) for v in dims.values()]
    return xr.DataArray(np.zeros(shape), dims=['country', *dims], coords={'country': list(countries), **dims})
