"""The rows of a Mitigation section while a block computes them: numpy arrays (country, year), stored in the state as
labelled arrays when the block finishes (xarray for the results, numpy for speed: a block has hundreds of rows).

    R = Rows(state, countries, years)
    R.t                            the years, shape (year,)
    R.put('cptraj', values)        a row without sector and fuel: code <iso>.mit.cptraj.<n>
    R.put('ctr', values, 'pow', 'all')   a row of a sector and fuel: code <iso>.mit.ctr.pow.all.<n>
    R.of('infl'), R.of('ctr', 'pow', 'all')   a row of this or an earlier block, (country, year)
    R.finish()                     every row to the state; rows of one variable stacked (sector, fuel, country, year)
Values broadcast to (country, year): a scalar, a year array (year,), a country array (country, 1).

In the year loop a block fills one year at a time: R.set(var, k, values) writes year index k (a row starts as NaN),
R.at(var, k) reads it; R.of(var) gives the whole row as filled so far.

The state of a run is a `State`: a dict whose block rows stay numpy arrays (fast for the blocks, which read them with
Rows); a row becomes a labelled xarray array only when something outside the blocks reads it (results, tests).
"""
import numpy as np
import xarray as xr


class Rows:
    def __init__(self, state, countries, years):
        self.state, self.countries, self.years = state, list(countries), list(years)
        self.t = np.array(years, dtype=float)
        self.shape = (len(self.countries), len(self.years))
        self._rows = {}                                   # var -> {(sector, fuel) or None: array}
        self._cache = {}                                  # var -> (values, sector index, fuel index) of the state

    def full(self, values):
        if isinstance(values, xr.DataArray):
            values = values.transpose(*[d for d in ('country', 'year') if d in values.dims]).values
            if values.ndim == 1 and values.shape[0] == len(self.countries) != len(self.years):
                values = values[:, None]
        if isinstance(values, str):
            return np.full(self.shape, values, dtype=object)
        return np.array(np.broadcast_to(values, self.shape))

    def put(self, var, values, sector=None, fuel=None):
        a = self.full(values)
        self._rows.setdefault(var, {})[None if sector is None and fuel is None else (sector, fuel)] = a
        return a

    def set(self, var, k, values, sector=None, fuel=None):
        """Year index k of a row filled year by year: values per country (country,) or a scalar."""
        key = None if sector is None and fuel is None else (sector, fuel)
        rows = self._rows.get(var)
        if rows is None:
            rows = self._rows[var] = {}
        a = rows.get(key)
        if a is None:                                     # a text row (labels, keys) is an object array
            text = np.asarray(values).dtype.kind in 'OUS'
            a = rows[key] = np.full(self.shape, None if text else np.nan, dtype=object if text else float)
        a[:, k] = values
        return a[:, k]

    def at(self, var, k, sector=None, fuel=None):
        """Year index k of a row (this block's or an earlier one's): (country,)."""
        rows = self._rows.get(var)
        if rows is not None:
            a = rows.get(None if sector is None and fuel is None else (sector, fuel))
            if a is not None:
                return a[:, k]
        return self.of(var, sector, fuel)[:, k]

    def of(self, var, sector=None, fuel=None):
        key = None if sector is None and fuel is None else (sector, fuel)
        if var in self._rows and key in self._rows[var]:
            return self._rows[var][key]
        if var not in self._cache:                        # numpy view of a state array, made once per block
            raw = self.state.raw(var, self.countries, self.years) if isinstance(self.state, State) else None
            if raw is not None:
                self._cache[var] = raw
                values, si, fi = raw
                return values if key is None else values[si[sector], fi[fuel]]
            a = self.state[var]
            if 'sector' in a.dims:
                a = a.sel(country=self.countries, year=self.years).transpose('sector', 'fuel', 'country', 'year')
                self._cache[var] = (a.values, {s: i for i, s in enumerate(a['sector'].values)},
                                    {f: i for i, f in enumerate(a['fuel'].values)})
            else:
                a = a.sel(country=self.countries, year=self.years).transpose('country', 'year')
                self._cache[var] = (a.values, None, None)
        values, si, fi = self._cache[var]
        return values if key is None else values[si[sector], fi[fuel]]

    def finish(self):
        """Every row to the state. The rows of a variable with sectors or fuels form one (sector, fuel, country, year)
        array; where they do not fill the grid, `rows` lists the (sector, fuel) pairs that are rows."""
        store = self.state if isinstance(self.state, State) else State()   # a plain dict gets xarray arrays
        for var, rows in self._rows.items():
            if None in rows:
                store.put_raw(var, rows[None], None, None, None, self.countries, self.years)
                continue
            sectors = list(dict.fromkeys(s for s, _f in rows))
            fuels = list(dict.fromkeys(f for _s, f in rows))
            text = any(a.dtype.kind in 'OUS' for a in rows.values())
            data = np.full((len(sectors), len(fuels)) + self.shape, np.nan, dtype=object if text else float)
            for (s, f), a in rows.items():
                data[sectors.index(s), fuels.index(f)] = a
            store.put_raw(var, data, sectors, fuels, list(rows) if len(rows) < len(sectors) * len(fuels) else None,
                          self.countries, self.years)
        if store is not self.state:
            for var in self._rows:
                self.state[var] = store[var]
        self._rows = {}


class State(dict):
    """The state of one scenario run: labelled arrays by variable. Rows written by blocks are kept as numpy
    (`put_raw`); `state[var]` builds the xarray array on first use."""

    def __init__(self):
        super().__init__()
        self._raw = {}                                    # var -> (values, sectors, fuels, rows, countries, years)

    def put_raw(self, var, values, sectors, fuels, rows, countries, years):
        self._raw[var] = (values, sectors, fuels, rows, list(countries), list(years))
        super().pop(var, None)

    def raw(self, var, countries, years):
        """(values, sector index, fuel index) of a block row of these countries and years, else None."""
        r = self._raw.get(var)
        if r is None or r[4] != countries or r[5] != years:
            return None
        values, sectors, fuels = r[0], r[1], r[2]
        if sectors is None:
            return values, None, None
        return values, {x: i for i, x in enumerate(sectors)}, {x: i for i, x in enumerate(fuels)}

    def raw_rows(self, var):
        """(values, sectors, fuels, rows, countries, years) of a block row, or None."""
        return self._raw.get(var)

    def __getitem__(self, var):
        if not super().__contains__(var) and var in self._raw:
            values, sectors, fuels, rows, countries, years = self._raw[var]
            coords = {'country': countries, 'year': years}
            if sectors is None:
                arr = xr.DataArray(values, coords=coords, dims=['country', 'year'])
            else:
                arr = xr.DataArray(values, dims=['sector', 'fuel', 'country', 'year'],
                                   coords={'sector': sectors, 'fuel': fuels, **coords})
                if rows is not None:
                    arr.attrs['rows'] = rows
            super().__setitem__(var, arr)
        return super().__getitem__(var)

    def __setitem__(self, var, value):
        self._raw.pop(var, None)
        super().__setitem__(var, value)

    def __contains__(self, var):
        return super().__contains__(var) or var in self._raw

    def __iter__(self):
        yield from super().__iter__()
        yield from (v for v in self._raw if not dict.__contains__(self, v))

    def __len__(self):
        return len(list(iter(self)))

    def keys(self):
        return list(iter(self))

    def items(self):
        return [(k, self[k]) for k in self]

    def values(self):
        return [self[k] for k in self]

    def update(self, other=(), **kw):
        for var, value in dict(other, **kw).items():
            self[var] = value

    def setdefault(self, var, default=None):
        if var not in self:
            self[var] = default
        return self[var]

    def get(self, var, default=None):
        return self[var] if var in self else default

    def pop(self, var, *default):
        if super().__contains__(var):
            self._raw.pop(var, None)
            return super().pop(var)
        if var in self._raw:
            value = self[var]
            super().pop(var)
            self._raw.pop(var)
            return value
        return super().pop(var, *default)

def cached(state, key, fn):
    """fn() shared by every run with the same baseline (core/loop.py): for data steps that read no scenario input."""
    store = state.get('_cache') if isinstance(state, dict) else None
    if store is None:
        return fn()
    if key not in store:
        store[key] = fn()
    return store[key]


def where(cond, a, b):
    """Excel's IF on arrays (both branches are computed; silence the warnings of the branch not taken)."""
    return np.where(cond, a, b)


def safe_div(a, b, fallback=0.0):
    """a / b where b is not 0, else fallback (Excel-AI's IFERROR / IF(b > 0, ...))."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b != 0, np.divide(a, np.where(b != 0, b, 1.0)), fallback)
