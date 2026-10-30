"""Data step of the distribution module (Excel-AI Distribution 0.1.4, sheet DistMapping and the data tabs). EQ-B1.1.

    survey          household survey (HHSurvey) and price elasticities (HH_Elast) by code and variable, in sheet order
    io_tables       the country's GTAP input-output data by sector: total demand, exports, household demand, output,
                    Leontief coefficients of the five fuel groups; the category and CPAT sector of each GTAP sector
    fuel_group_use  total use of each fuel group (embedded in non-fuel sectors plus own demand) x the deflator ratio
                    (ResultsYear / GTAP year, WEO GDP deflator): DIOTot
    category_leontief   household-demand weighted Leontief coefficients by consumption category: DLcat
    gini_weights    the weights of the legacy Gini (fit L = a x^2 + b x to the Lorenz points): DGiniW
"""
from functools import lru_cache

import numpy as np

from cpat_model.data.database import to_float

GROUPS = ['coa', 'ely', 'nga', 'oil', 'p_c']           # IO fuel groups (DistMapping rows 28-32)
CATEGORIES = ['app', 'che', 'clo', 'com', 'edu', 'food', 'hea', 'hou', 'oth', 'pap', 'pha', 'ret', 'teq', 'tpu']
IO_SERIES = {'totd': 'TOTD', 'exports': 'Exports', 'hhd': 'HHD', 'output': 'Output'}


def survey(db, table):
    """{code: {variable: value}} and the 1-based row of each code (sheet order) of HHSurvey or HH_Elast."""
    df = db.table(table)
    rows = {}
    for code, var, v in zip(df['code'], df['variable'], df['value']):
        rows.setdefault(code, {})[var] = v
    position = {code: i + 1 for i, code in enumerate(rows)}
    return rows, position


def number(x):
    """A survey cell as a number (blank: 0, Excel's arithmetic on an empty cell)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def io_tables(db, iso):
    """{series: {gtap sector: value}} of the country, its GTAP year, the GTAP sectors in sheet order."""
    df = db.table('io_gtap')
    df = df[df['country'] == iso]
    io = {}
    for ser, sec, v in zip(df['series'], df['gtap_sector'], to_float(df['value'])):
        io.setdefault(ser, {})[sec] = float(v)
    sectors = list(io.get('HHD', {}))
    year = int(df['year'].iloc[0]) if len(df) else 0
    return io, year, sectors


def sector_table(db, sectors):
    """{gtap sector: (consumption category, CPAT sector, name)} (DistMapping rows 40, 86-149)."""
    cat = dict(zip(*[db.table('distn_category_map')[c] for c in ('gtap_sector', 'item')]))
    gm = db.table('distn_gtap_map')
    cpat = dict(zip(gm['gtap_sector'], gm['cpat']))
    name = dict(zip(gm['gtap_sector'], gm['description']))
    return {s: (cat.get(s, ''), cpat.get(s, ''), name.get(s, '')) for s in sectors}


def deflator_ratio(db, iso, gtap_year, results_year):
    """WEO GDP deflator of ResultsYear / of the GTAP year (DistMapping row 58: the raw WEO data)."""
    df = db.table('weo')
    df = df[df['series_code'] == f'{iso}.NGDP_D.A']
    v = dict(zip(df['year'].astype(int), to_float(df['value'])))
    return v[results_year] / v[gtap_year]


def country_data(db, iso, results_year):
    """Everything the Distribution sheet reads from DistMapping, for one country."""
    io, year, sectors = io_tables(db, iso)
    table = sector_table(db, sectors)
    leon = {g: np.array([io[g][s] for s in sectors]) for g in GROUPS}
    series = {k: np.array([io[v][s] for s in sectors]) for k, v in IO_SERIES.items()}
    fuel = np.array([1.0 if table[s][0] in GROUPS else 0.0 for s in sectors])
    ratio = deflator_ratio(db, iso, year, results_year)
    non_fuel = (series['totd'] + series['exports']) * (1 - fuel)
    totd = dict(zip(sectors, series['totd']))
    use = {g: ratio * (float(np.dot(non_fuel, leon[g])) + totd[g]) for g in GROUPS}
    cats = np.array([table[s][0] for s in sectors])
    hhd = series['hhd']
    lcat = {c: np.array([float(np.sum((hhd * leon[g])[cats == c]) / np.sum(hhd[cats == c])) for g in GROUPS])
            for c in CATEGORIES}
    return {'sectors': sectors, 'table': table, 'leontief': np.stack([leon[g] for g in GROUPS], axis=1),
            'fuel': fuel, 'hhd': hhd, 'output': series['output'], 'group_use': use, 'category_leontief': lcat}


def programmes(db):
    """{kind|label: code} of the recycling choices (DistMapping rows 4-25)."""
    df = db.table('distn_programs')
    return dict(zip(df['key'], df['code']))


def passthrough(db):
    df = db.table('distn_passthrough')
    return {s: float(c) for s, c in zip(df['sector'], df['coefficient'])}


def aspire(db):
    df = db.table('aspire')
    return {c: float(v) for c, v in zip(df['code'], to_float(df['value']))}


@lru_cache(maxsize=1)
def gini_weights(n=10):
    """Legacy C.IX: L(x) = a x^2 + b x fitted to the cumulative shares L_1..L_n (x = 1..n, no intercept, LINEST); Gini =
    (n/2 - area under L over 0..n) / (n/2), linear in L: Gini = 1 - sum_d s_d W_d / sum_d s_d (DistMapping DGiniW)."""
    d = np.arange(1, n + 1, dtype=float)
    s2, s3, s4 = (np.sum(d ** k) for k in (2, 3, 4))
    det = s4 * s2 - s3 ** 2
    w = (n ** 3 / 3 * (s2 * d * d - s3 * d) + n ** 2 / 2 * (s4 * d - s3 * d * d)) / det
    return tuple(np.cumsum(w[::-1])[::-1] / (n / 2))
