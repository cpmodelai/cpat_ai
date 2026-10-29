"""Results of a run: the state of every scenario, by code (NORMS 6)."""
import pandas as pd


class Results:
    def __init__(self, settings):
        self.settings = settings
        self.states = {}

    def add(self, number, state):
        self.states[number] = state

    def by_code(self, country='EGY'):
        """A table of every result row in Excel-AI's form: index = output code of scenario n
        (`<iso>.mit.<variable>[.<sector>][.<fuel>].<n>`), columns = years."""
        rows = {}
        for n, state in self.states.items():
            for var, arr in state.items():
                if var.startswith('_'):                   # working data of a block, not a result row
                    continue
                for code, series in flatten(var, arr, country, n):
                    rows[code] = series
        return pd.DataFrame(rows).T.sort_index()


def flatten(var, arr, country, n):
    """Yield (code, values by year) for a labelled array: other dimensions become the code slots in the order of
    the array's dimensions (sector, fuel, other), as the codes protocol (C2)."""
    a = arr.sel(country=country) if 'country' in getattr(arr, 'dims', ()) else arr
    other = [d for d in a.dims if d != 'year']
    if not other:
        yield f'{country.lower()}.mit.{var}.{n}', a.to_pandas()
        return
    rows = set(map(tuple, a.attrs.get('rows', [])))          # a sparse grid: only these (sector, fuel) are rows
    stacked = a.stack(_k=other)
    for i in range(stacked.sizes['_k']):
        key = stacked['_k'].values[i]
        key = key if isinstance(key, tuple) else (key,)
        if rows and key not in rows:
            continue
        yield f'{country.lower()}.mit.{var}.{".".join(map(str, key))}.{n}', stacked.isel(_k=i).to_pandas()
