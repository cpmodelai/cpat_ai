"""Results of a run: the state of every scenario, by code (NORMS 6)."""
import numpy as np
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
        groups = {}                                       # years -> (codes, rows): rows of the same years together
        for n, state in self.states.items():
            for var, arr in state.items():
                if var.startswith('_') or 'year' not in getattr(arr, 'dims', ()):   # working data, not result rows
                    continue
                for code, values, years in flatten(var, arr, country, n):
                    codes, rows = groups.setdefault(tuple(years), ([], []))
                    codes.append(code)
                    rows.append(values)
        tables = [pd.DataFrame(np.array(rows), index=codes, columns=list(years))
                  for years, (codes, rows) in groups.items()]
        return pd.concat(tables).sort_index()


def flatten(var, arr, country, n):
    """Yield (code, values by year, years) for a labelled array: other dimensions become the code slots in the order
    of the array's dimensions (sector, fuel, other), as the codes protocol (C2)."""
    a = arr.sel(country=country) if 'country' in getattr(arr, 'dims', ()) else arr
    years = list(a['year'].values)
    other = [d for d in a.dims if d != 'year']
    a = a.transpose(*other, 'year')
    prefix = f'{country.lower()}.mit.{var}'
    if not other:
        yield f'{prefix}.{n}', a.values, years
        return
    rows = set(map(tuple, a.attrs.get('rows', [])))          # a sparse grid: only these (sector, fuel) are rows
    labels = [list(a[d].values) for d in other]
    values = a.values
    for idx in np.ndindex(*values.shape[:-1]):
        key = tuple(labels[k][i] for k, i in enumerate(idx))
        if rows and key not in rows:
            continue
        yield f'{prefix}.{".".join(map(str, key))}.{n}', values[idx], years
