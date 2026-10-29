"""The rows of a Mitigation section while a block computes them: numpy arrays (country, year), stored in the state as
labelled arrays when the block finishes (xarray for the results, numpy for speed: a block has hundreds of rows).

    R = Rows(state, countries, years)
    R.t                            the years, shape (year,)
    R.put('cptraj', values)        a row without sector and fuel: code <iso>.mit.cptraj.<n>
    R.put('ctr', values, 'pow', 'all')   a row of a sector and fuel: code <iso>.mit.ctr.pow.all.<n>
    R.of('infl'), R.of('ctr', 'pow', 'all')   a row of this or an earlier block, (country, year)
    R.finish()                     every row to the state; rows of one variable stacked (sector, fuel, country, year)
Values broadcast to (country, year): a scalar, a year array (year,), a country array (country, 1).
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

    def of(self, var, sector=None, fuel=None):
        key = None if sector is None and fuel is None else (sector, fuel)
        if var in self._rows and key in self._rows[var]:
            return self._rows[var][key]
        if var not in self._cache:                        # numpy view of a state array, made once per block
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
        array; where they do not fill the grid, attrs['rows'] lists the (sector, fuel) pairs that are rows."""
        coords = {'country': self.countries, 'year': self.years}
        cy = xr.Coordinates(coords)                       # built once: a DataArray per row is then cheap
        for var, rows in self._rows.items():
            if None in rows:
                self.state[var] = xr.DataArray(rows[None], coords=cy)
                continue
            sectors = list(dict.fromkeys(s for s, _f in rows))
            fuels = list(dict.fromkeys(f for _s, f in rows))
            text = any(a.dtype.kind in 'OUS' for a in rows.values())
            data = np.full((len(sectors), len(fuels)) + self.shape, np.nan, dtype=object if text else float)
            for (s, f), a in rows.items():
                data[sectors.index(s), fuels.index(f)] = a
            arr = xr.DataArray(data, dims=['sector', 'fuel', 'country', 'year'],
                               coords={'sector': sectors, 'fuel': fuels, **coords})
            if len(rows) < len(sectors) * len(fuels):
                arr.attrs['rows'] = list(rows)
            self.state[var] = arr
        self._rows = {}


def where(cond, a, b):
    """Excel's IF on arrays (both branches are computed; silence the warnings of the branch not taken)."""
    return np.where(cond, a, b)


def safe_div(a, b, fallback=0.0):
    """a / b where b is not 0, else fallback (Excel-AI's IFERROR / IF(b > 0, ...))."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b != 0, np.divide(a, np.where(b != 0, b, 1.0)), fallback)
