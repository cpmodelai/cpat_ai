"""Block 0, header: the macro series (Excel-AI sheet Inputs_macro, the data step of legacy Mitigation rows 417-467)
and the header rows of the Mitigation sheet that read them (rows 8-13): inflation and deflator indices, real GDP in
USD and local currency, the exchange rate. Quantity-free: computed for all years in the prepare stage.

The macro series run over Excel-AI's macro years (2018-2045), are WEO data up to the last data year of each series,
then extended by the rules of EQ-M0.1. State keys: `macro.<series>` (country, year) for the series, and the Mitigation
codes `infl`, `defl`, `gdp.usd`, `gdp.lcu`, `xr`, `gdp.base` (`all.all` in their codes, as Excel-AI).
"""
import numpy as np
import xarray as xr

from cpat_model.core.rows import cached
from cpat_model.data.database import to_float

MACRO_YEARS = list(range(2018, 2046))     # Excel-AI IMAC_YEARS
GDP_EXT_HALF = 0.5                        # Excel-AI GdpExtHalf: share of the recent average growth kept when falling
EURO_SERIES = 'G163'                      # WEO code of the euro area (exchange rate of euro countries)
WEO_SERIES = ['NGDP_D', 'PCPI', 'NGDP_RPCH', 'NGDP_R', 'NGDP', 'NGDPD', 'XDC_USD.PA_RT', 'LP']


def weo(db, codes=None):
    """{series code: ({year: value}, last data year)} of the WEO table (only `codes` if given)."""
    df = db.table('weo')
    if codes is not None:
        df = df[df['series_code'].isin(codes)]
    df = df.assign(v=to_float(df['value']), y=df['year'].astype(int))
    return {code: (dict(zip(g['y'], g['v'])), int(last)) for (code, last), g in df.groupby(['series_code', 'last_year'])}


def euro_countries(db):
    df = db.table('countries_attributes')
    return set(df.loc[(df['variable'] == 'Using euro') & (df['value'].astype(str).str.strip() != ''), 'code'])


def extend(series, rule):
    """WEO data up to the last data year, then `rule(previous values)` (EQ-M0.1). Missing series -> NaN."""
    if series is None:
        return {y: np.nan for y in MACRO_YEARS}
    data, last = series
    out = {}
    for y in MACRO_YEARS:
        out[y] = data.get(y, np.nan) if y <= last else rule(out, y)
    return out


def macro_series(w, iso, euro, base_year, results_year):
    """The macro series of one country (EQ-M0.1), as Excel-AI Inputs_macro."""
    get = lambda s: w.get(f'{s}.A')
    s = {}
    p = lambda name, y, k=1: s[name].get(y - k, np.nan)
    s['ngdp_d'] = extend(get('USA.NGDP_D'), lambda o, y: o[y - 1] + (o[y - 1] - o[y - 2]))
    s['pcpi'] = extend(get('USA.PCPI'), lambda o, y: o[y - 1])
    defl_res, cpi_res = s['ngdp_d'][results_year], s['pcpi'][results_year]
    s['deflidx'] = {y: defl_res / s['ngdp_d'][y] for y in MACRO_YEARS}

    def growth_ext(o, y):                 # past the last data year: hold, or ease off a falling growth rate
        g1, g2, g3 = o.get(y - 1, np.nan), o.get(y - 2, np.nan), o.get(y - 3, np.nan)
        if g1 < g2:
            return max(np.nanmean([g3, g2, g1]) * GDP_EXT_HALF, g1 + g1 - g2)
        return g1
    g = get(f'{iso}.NGDP_RPCH')
    s['gdp_growth'] = extend(g and ({y: v / 100 for y, v in g[0].items()}, g[1]), growth_ext)
    s['ngdp_r'] = extend(get(f'{iso}.NGDP_R'), lambda o, y: o[y - 1] * (1 + s['gdp_growth'][y]))

    ngdp, ngdp_g = get(f'{iso}.NGDP'), {}
    last_ngdp = ngdp[1] if ngdp else -1

    def ngdp_rule(o, y):
        ngdp_g[y] = ngdp_g[y - 1]
        return o[y - 1] * (1 + ngdp_g[y])
    s['ngdp'] = {}
    for y in MACRO_YEARS:                 # Excel-AI: ngdp_g holds from the last data year of ngdp (not after it)
        if y <= last_ngdp:
            s['ngdp'][y] = ngdp[0].get(y, np.nan)
            ngdp_g[y] = (ngdp_g.get(y - 1, np.nan) if y >= last_ngdp else
                         s['ngdp'][y] / s['ngdp'].get(y - 1, np.nan) - 1)
        else:
            s['ngdp'][y] = ngdp_rule(s['ngdp'], y) if ngdp else np.nan
    s['ngdp_g'] = ngdp_g
    s['ngdpd'] = extend(get(f'{iso}.NGDPD'), lambda o, y: o[y - 1] * (1 + ngdp_g.get(y, np.nan)))
    s['xr'] = extend(get(f'{EURO_SERIES if iso in euro else iso}.XDC_USD.PA_RT'), lambda o, y: o[y - 1])
    s['gdp_usd'] = {}
    for y in MACRO_YEARS:
        s['gdp_usd'][y] = (s['ngdp'][y] / s['xr'][y] * s['deflidx'][y] if y < base_year else
                           s['gdp_usd'].get(y - 1, np.nan) * (1 + s['gdp_growth'][y]))
    s['gdp_lcu'] = s['ngdp_r']
    s['lp'] = extend(get(f'{iso}.LP'), lambda o, y: o[y - 1] * (o[y - 1] / o[y - 2]))
    s['gdppc'] = {y: s['gdp_usd'][y] / s['lp'][y] * 1000 for y in MACRO_YEARS}
    return s, cpi_res, defl_res


def all_all(arr):
    """A country-year quantity whose Excel-AI code carries the sector and fuel `all`."""
    return arr.expand_dims(sector=['all'], fuel=['all'])


def prepare(state, db, inputs, settings, baseline):
    """EQ-M0.1, EQ-M0.2. The macro series and the header rows, for the run's countries and all years (data only: shared
    by the runs of a baseline)."""
    state.update(cached(state, 'header', lambda: _header(db, settings)))


def _header(db, settings):
    state = {}
    countries = list(settings.countries)
    euro = euro_countries(db)
    w = weo(db, {f'{iso}.{s}.A' for iso in countries + ['USA', EURO_SERIES] for s in WEO_SERIES})
    rows = {}
    for iso in countries:
        s, cpi_res, defl_res = macro_series(w, iso, euro, settings.base_year, settings.results_year)
        s['cpiidx'] = {y: cpi_res / s['pcpi'][y] for y in MACRO_YEARS}       # US CPI of ResultsYear / of t
        s['usinfl'] = {y: s['ngdp_d'][y] / s['ngdp_d'].get(y - 1, np.nan) - 1 for y in MACRO_YEARS}   # USA|infl
        rows[iso] = s
    names = rows[countries[0]].keys()
    for name in names:
        arr = xr.DataArray([[rows[c][name].get(y, np.nan) for y in MACRO_YEARS] for c in countries],
                           dims=['country', 'year'], coords={'country': countries, 'year': MACRO_YEARS})
        state[f'macro.{name}'] = arr
    years = settings.years
    m = lambda name: state[f'macro.{name}'].sel(year=years)
    state['infl'] = m('cpiidx')                                     # US CPI of ResultsYear / US CPI of t
    state['defl'] = m('deflidx')                                    # US deflator of ResultsYear / of t
    state['gdp.usd'] = all_all(m('gdp_usd'))
    state['gdp.lcu'] = all_all(m('gdp_lcu'))
    state['xr'] = state['gdp.lcu'] / state['gdp.usd']               # LCU per USD, real
    state['gdp.base'] = all_all(m('gdp_growth'))                    # baseline real GDP growth
    return state
