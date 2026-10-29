"""Block 1, policies: the scenario inputs read by the Mitigation sheet and the policy paths built from them (Mitigation
section 1). Quantity-free: computed for all years in the prepare stage.

    inputs     every input row (core/excel_ai/input_rows.csv), constant over the years
    carbon     carbon price path, coverage by fuel and sector, exemption phase-out (EQ-M1.1, EQ-M1.2)
    reform     fuel price reform paths (EQ-M1.5)
    scc        social cost of carbon (EQ-M1.6)
    ets        new emissions trading: coverage, benchmarks, cap and the fast price estimate (EQ-M1.3, EQ-A1.1)
    feebates, regulations, sector rates (EQ-M1.3, EQ-M1.4)
    existing   existing carbon pricing factors (EQ-A2.2), subsidy and price-control phase-outs (EQ-M1.7)
    methane    methane fee (EQ-M1.8)
Not yet here (they need prices and emission factors): the Pigouvian taxes (pig.*, airpol.mc, cc.code, pigx, ntxg,
xcpb, xpre, ntxb) and the producer subsidies (pros, psd, psu).

Text inputs are compared as Excel-AI does: `LEFT(x, 3) = "Yes"` (yes()), `x = TRUE` (is_true()), `IF(x, ...)`
(truthy()); Excel text comparison ignores case.
"""
import numpy as np
import xarray as xr

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.dims import COVERAGE_SECTORS, FUELS, PRICE_FUELS

ETS_GROUPS = ['pow', 'tra', 'res', 'ind']             # benchmark groups = feebate sectors
FEEBATE_SECTORS = ['pow', 'tra', 'res', 'ind']
PHASEOUTS = {  # code: policy switch, baseline switch, start year, policy period, baseline period, policy and baseline share
    'ps': ('ProdSubPh', 'ProdSubPhaBaseline', 'YearProdSubPha', 'FFSProdPhaseoutPeriod', 'FFSProdPhaseoutPeriodBA',
           'ShareofProdSubPha', 'ShareOfProdSubPhaBA'),
    'cs': ('ConsSubPha', 'ConsSubPhaBaseline', 'YearConsSubPha', 'FFPhaseOut', 'FFSConsPhaseoutPeriodBA',
           'ShareOfConsSubPha', 'ShareofConsSubPhaBA'),
    'pc': ('PrcContPha', 'PrcContPhaBaseline', 'YearPrcContPha', 'PrcControlPhaseout', 'PrcControlPhaseout',
           'ShareOfConsSubPha', 'ShareofConsSubPhaBA')}   # Excel-AI: price controls use the consumer shares (I48)
REG_ADJUSTMENTS = ['SPPEffAdjEnergyEfficiencyRegulations', 'SPPEffAdjVehicleFuelEconomy', 'SPPEffAdjRes',
                   'SPPEffAdjInd', 'SPPEffAdjFeebates']   # MTInputs rows 247-251, positions 1-5 of the scenario table
FPR_FUELS = PRICE_FUELS[:6] + ['ecy.res', 'ecy.ind'] + PRICE_FUELS[6:]   # fuel price reform: with electricity
ECP_YEARS = [2021, 2022, 2023, 2024, 2025]             # years of the existing carbon pricing data (Inputs, ECPYear)
SCC_SOURCES = {'T': 'tgt', 'R': None, 'M': 'man', 'U': 'epa', 'E': 'epa'}   # NSCCSrc / GSCCSrc by first letter


# ---- Excel's tests of input text
def yes(x):
    return str(x)[:3].lower() == 'yes'


def is_true(x):
    return str(x).upper() == 'TRUE'


def truthy(x):
    if str(x).upper() in ('TRUE', 'FALSE'):
        return str(x).upper() == 'TRUE'
    return bool(x) and float(x) != 0


def num(x):
    """An input in arithmetic: TRUE = 1, FALSE = blank = 0."""
    if x is None or str(x).upper() == 'FALSE':
        return 0.0
    return 1.0 if str(x).upper() == 'TRUE' else float(x)


def linear_path(t, t0, t1, x0, x1, hold=True):
    """EQ-M1.1: 0 before t0, linear from x0 to x1 between t0 and t1, held after t1 (or continued: hold=False)."""
    tt = np.minimum(t, t1) if hold else t
    return xr.where(t < t0, 0.0, x0 + (x1 - x0) / max(t1 - t0, 1) * (tt - t0))


# ---- the sheet's rows by code
class Rows:
    """The rows of one section: `put(var, values, sector=, fuel=)` keeps a (country, year) array under its code."""

    def __init__(self, state, countries, years):
        self.state, self.countries = state, countries
        self.t = xr.DataArray(years, dims='year', coords={'year': years})
        self.coords = {'country': list(countries), 'year': list(years)}
        self._parts = {}

    def full(self, values):
        """Broadcast a scalar, a year array or a country array to (country, year) (numpy: xarray's broadcasting is
        slow for thousands of small rows)."""
        shape = (len(self.countries), self.t.size)
        if isinstance(values, xr.DataArray):
            dims = set(values.dims)
            if dims == {'country', 'year'}:
                data = values.transpose('country', 'year').values
            elif dims == {'year'}:
                data = np.broadcast_to(values.values, shape)
            elif dims == {'country'}:
                data = np.broadcast_to(values.values[:, None], shape)
            else:
                data = np.full(shape, values.item())
        else:
            data = np.full(shape, values, dtype=object if isinstance(values, str) else float)
        return xr.DataArray(np.array(data), dims=['country', 'year'], coords=self.coords)

    def put(self, var, values, sector=None, fuel=None):
        a = self.full(values)
        if sector is None and fuel is None:
            self.state[var] = a
            return a
        self._parts.setdefault(var, []).append((sector, fuel, a))
        return a

    def get(self, var, sector=None, fuel=None):
        if sector is None and fuel is None:
            return self.state[var]
        return next(a for s, f, a in self._parts[var] if s == sector and f == fuel)

    def finish(self):
        """Stack the sector/fuel rows of each variable into one (sector, fuel, country, year) array; where the rows do
        not fill the grid, attrs['rows'] lists the (sector, fuel) pairs that are rows (the others are NaN)."""
        for var, parts in self._parts.items():
            sectors = list(dict.fromkeys(s for s, _f, _a in parts))
            fuels = list(dict.fromkeys(f for _s, f, _a in parts))
            first = parts[0][2]
            text = any(a.dtype.kind in 'OUS' for _s, _f, a in parts)
            data = np.full((len(sectors), len(fuels)) + first.shape, np.nan, dtype=object if text else float)
            for s, f, a in parts:
                data[sectors.index(s), fuels.index(f)] = a.values
            arr = xr.DataArray(data, dims=['sector', 'fuel', 'country', 'year'],
                               coords={'sector': sectors, 'fuel': fuels, 'country': first['country'].values,
                                       'year': first['year'].values})
            if len(parts) < len(sectors) * len(fuels):
                arr.attrs['rows'] = [(s, f) for s, f, _a in parts]
            self.state[var] = arr
        self._parts = {}


def input_rows(rows, inputs):
    """Every input row read by the Mitigation sheet (constant over the years); returns {key: value}."""
    out = {}
    for r in xt.table('input_rows'):
        var, fuel, sector = r['key'].split('|')
        value = inputs[r['name']]
        out[r['key']] = value
        if var == 'ctcov':                             # computed from the input (prepare)
            continue
        v = 0.0 if value is None else value              # a blank input cell reads as 0 (INDEX)
        if isinstance(v, str) and v.upper() in ('TRUE', 'FALSE'):
            v = num(v)                                   # Excel-AI stores the switches as 1 / 0
        if fuel or sector:
            rows.put(var, v, sector, fuel)
        else:
            rows.put(var, v)
    return out


# ---- data of the country
def ecp_table(db, iso, infl):
    """Existing carbon pricing of the country (Excel-AI Inputs rows 611-661): {code: values over ECP_YEARS}.
    Tax rates and permit prices are made real with the CPI index of the year; the regional (EU) ETS counts only if
    the country is in it."""
    info = db.table('ecp_general_information')
    info = dict(zip(info.loc[info['country'] == iso, 'variable'], info.loc[info['country'] == iso, 'value']))
    single = info.get('Single price?', '') == 'Yes'
    eu = info.get('Is it EU ETS?', '') in ('Yes', 'Both')
    real = np.array([infl.get(y, np.nan) for y in ECP_YEARS])

    def series(table, code):
        df = db.table(table)
        df = df[df['code'] == code]
        v = dict(zip(df['year'].astype(int), df['value']))
        return np.array([float(v[y]) if v.get(y, '') not in ('', None) else 0.0 for y in ECP_YEARS]), len(df) > 0

    p = f'{iso.lower()}.mit.'
    out = {}
    out['ecr.all'] = series('ecp_tax_rate', p + 'ecr.all')[0] * real
    for f in FUELS:
        v, found = series('ecp_tax_rate', p + f'ecr.{f}')
        out[f'ecr.{f}'] = out['ecr.all'] if single or not found else v * real
    for s in ('pow', 'trs', 'res', 'ind'):
        out[f'ecs.{s}'] = series('ecp_tax_sector_coverage', p + f'ecs.{s}')[0]
        out[f'ees.{s}'] = series('ecp_ets_sector_coverage_national', p + f'ees.{s}')[0]
        out[f'res.{s}'] = series('ecp_ets_sector_coverage_regional', p + f'ees.{s}')[0] * eu
    for f in FUELS:
        out[f'ecf.{f}'] = series('ecp_tax_fuel_coverage', p + f'ecf.{f}')[0]
        out[f'eef.{f}'] = series('ecp_ets_fuel_coverage_national', p + f'eef.{f}')[0]
        out[f'ref.{f}'] = series('ecp_ets_fuel_coverage_regional', p + f'eef.{f}')[0] * eu
    out['eer.all'] = series('ecp_ets_price_national', p + 'eer.all')[0] * real
    out['rer.all'] = series('ecp_ets_price_regional', 'eu.mit.eer.all')[0] * real * eu
    return out


def stored_baseline(db_path, countries, years):
    """Excel-AI's stored scenario-1 values (sheet BaselineCO2; data/excel_ai_stored), {key: (country, year)}."""
    import pandas as pd
    df = pd.read_csv(db_path, dtype={'country': str, 'key': str})
    out = {}
    for key, g in df.groupby('key'):
        s = g.set_index(['country', 'year'])['value'].astype(float)
        a = xr.DataArray.from_series(s).reindex(country=countries, year=years)
        out[key] = a
    return out


# ---- the block
def prepare(state, db, inputs, settings, baseline):
    """EQ-M1.1 to EQ-M1.8, EQ-A1.1, EQ-A2.2 (Mitigation section 1)."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    t, n = R.t, inputs.number
    i = input_rows(R, inputs)
    g = lambda name: inputs[name]
    G = lambda name: settings.global_settings.get(name, inputs[name])    # D16: read from the baseline column
    cov = xt.table('coverage_sectors')
    cov_group = {r['sector']: r['ets_group'] for r in cov}
    cov_feebate = {r['sector']: r['feebate_sector'] for r in cov}
    cov_semi = {r['sector']: r['semi_group'] for r in cov}

    # carbon price path (EQ-M1.2) and coverage
    linear_after = str(g('ExtendCarbonPriceBeyondOutro')).lower() == 'linear*'
    cp_t = R.put('cp.t', (t if linear_after else np.minimum(t, g('CPOutro'))) - g('CPIntro'))
    cp_nom = R.put('cp.nom', state['infl'] if str(g('NomorReal'))[:7].lower() == 'nominal' else 1.0)
    cptraj = R.put('cptraj', xr.where(t < g('CPIntro'), 0.0, g('CPLevelStart') + (g('CPLevelTarget') - g('CPLevelStart'))
                                      / max(g('CPOutro') - g('CPIntro'), 1) * cp_t) * cp_nom)
    exph = R.put('exph', xr.where(t >= g('CPIntro'), np.clip((t + 1 - g('YearPha')) / g('ExemptPhaseoutPeriod'), 0, 1),
                                  0.0) if n > 1 and is_true(g('ExemptPhaseout')) else 0.0)
    for key, v in i.items():
        var, fuel, sector = key.split('|')
        if var == 'ctcov':
            R.put('ctcov', 1.0 if truthy(v) else exph, sector, fuel)

    # fuel price reform (EQ-M1.5): linear from the start to the final increase, then linear or by the growth rate
    y0, y1 = g('FprIntro'), g('FprOutro')
    for pc in FPR_FUELS:
        fu, se = pc.split('.')
        s0, s1 = num(i[f'fpr.s|{fu}|{se}']), num(i[f'fpr.f|{fu}|{se}'])
        slope = (s1 - s0) / (y1 - y0) if y1 > y0 else 0.0
        rate = ((s1 / (s0 if s0 > 0 else s0 + slope)) ** (1 / (y1 - y0)) - 1) if y1 > y0 and max(s0, s1) > 0 else 0.0
        base = s0 + slope * max(y1 - y0 - 1, 0)
        after = (base * (1 + rate) ** (t - y1 + 1) if str(g('ExtendCarbonPriceBeyondOutro')).lower() == 'percentage'
                 else (s1 if y1 > y0 else s0))
        R.put('fprj', slope, se, fu)
        R.put('fprk', rate, se, fu)
        R.put('fprp', base, se, fu)
        R.put('fpra', after, se, fu)
        R.put('fpr', xr.where(t < y0, 0.0, xr.where((t < y1) | linear_after, s0 + slope * (t - y0), after)), se, fu)

    # social cost of carbon (EQ-M1.6)
    gr, base_year = G('SCCRise'), settings.base_year
    scc = {'tgt': G('SCCTargetConsistentCP') * (1 + gr) ** (t - G('SCCTargetYear')),
           'epa': G('SCCEpaBaseYear') * (1 + gr) ** (t - base_year)}
    rate_key = lambda: f"{str(G('NSCCDiscountRate'))[:1]}.{str(G('NSCCMargUtilofCons')).split('%')[0].replace('.', 'p')}"
    ricke = dict(zip(db.table('scc')['code'], db.table('scc')['value'].astype(float)))
    man = db.table('mi_scc')
    man = man[man['item'].str.startswith('National')]
    man = dict(zip(man['year'].astype(int), man['value'].astype(float)))
    scc['man'] = xr.DataArray([man.get(y, np.nan) for y in years], dims='year', coords={'year': years})
    scc['rkg'] = ricke.get(f'wld.{rate_key()}', np.nan) * (1 + gr) ** (t - base_year)
    rkn = xr.DataArray([ricke.get(f'{c.lower()}.{rate_key()}', np.nan) for c in countries], dims='country',
                       coords={'country': countries})
    scc['rkn'] = rkn * (1 + gr) ** (t - base_year)
    for k in ('tgt', 'rkn', 'rkg', 'man', 'epa'):
        R.put('scc', scc[k], 'all', k)
    for k, src, ricke_k in (('nat', 'NSCCSource', 'rkn'), ('glo', 'GSCCSource', 'rkg')):
        pick = SCC_SOURCES[str(G(src))[:1].upper()] or ricke_k
        R.put('scc', scc[pick], 'all', k)

    # new ETS (EQ-M1.3, EQ-A1.1)
    on = yes(g('NewETS')) & (t >= g('ETSIntro'))
    R.put('ets.on', on.astype(float))
    etsc = {s: R.put('etsc', xr.where(on, 1.0 if truthy(i[f'etscov|all|{s}']) else 0.0, 0.0), s, 'all')
            for s in COVERAGE_SECTORS}
    for grp in ETS_GROUPS:
        R.put('etsb.s', 1 - g('ETSAuctStart'), grp, 'all')
    for grp in ETS_GROUPS:
        R.put('etsb.t', 1 - g('ETSAuctTarget'), grp, 'all')
    etsb = {grp: R.put('etsb', linear_path(t, g('ETSIntro'), g('ETSOutro'), 1 - g('ETSAuctStart'),
                                           1 - g('ETSAuctTarget')), grp, 'all') for grp in ETS_GROUPS}
    obr = {s: R.put('obr', np.clip(etsb[cov_group[s]], 0, 1), s, 'all') for s in COVERAGE_SECTORS}
    stored = stored_baseline(settings_stored_path(settings), countries, years)
    bco2 = {s: R.put('bco2', stored.get(s, R.full(np.nan)).fillna(0) if s in stored else R.full(0.0), s, 'all')
            for s in COVERAGE_SECTORS}
    for k in ('dg', 'bm'):
        R.put('ch4bs', stored[k] if k in stored else R.full(0.0), k, 'all')
    semi = db.table('ets_semi_elasticities')
    semi = {(c, s): float(v) for c, s, v in zip(semi['country'].str.upper(), semi['sector'], semi['value'])}
    vol = {r['item'][:7]: r for r in xt.table('ets_volatility')}
    ets_vol = R.put('ets.vol', float(vol['Assumed'][str(g('ETSVolatility')).replace('*', '')]))
    ets_imp = R.put('ets.imp', float(vol['Abateme'][str(g('ETSVolImpact')).replace('*', '')]))
    vadj = R.put('ets.vadj', (1 + g('ETSCTRisk') * ets_imp) / (1 + ets_vol * ets_imp))
    bce = R.put('ets.bce', sum(bco2[s] * etsc[s] for s in COVERAGE_SECTORS))
    chg = R.put('ets.chg', g('ETSChangeRelStart') + (g('ETSChangeRelTarget') - g('ETSChangeRelStart'))
                / max(g('ETSOutro') - g('ETSIntro'), 1) * (np.minimum(t, g('ETSOutro')) - g('ETSIntro')))
    cap = (bce * (1 + chg)).where(on, 0.0)
    if str(g('ETSCapCont'))[:8].lower() == 'constant':          # held at the last value after the target year
        for k, y in enumerate(years):
            if y > g('ETSOutro') and k > 0:
                cap[:, k] = xr.where(on.isel(year=k), cap[:, k - 1], 0.0)
    R.put('ets.cap', cap)
    semi_el = {s: xr.DataArray([semi.get((c, cov_semi[s]), np.nan) for c in countries], dims='country',
                               coords={'country': countries}) for s in COVERAGE_SECTORS}
    obr_eff = G('ETSOBREffectiveness')
    se_num = sum(bco2[s] * etsc[s] * semi_el[s] * (1 - (1 - obr_eff) * obr[s]) for s in COVERAGE_SECTORS)
    se = R.put('ets.se', xr.where(bce > 0, se_num / bce.where(bce > 0, 1.0), 0.0))
    ok = on & (cap > 0) & (cap < bce) & (se < 0) & (vadj > 0)
    est = R.put('ets.est', xr.where(ok, np.log((cap / bce).where(ok, 1.0)) / (se * vadj).where(ok, 1.0), 0.0))
    R.put('ets.ovr', np.nan)
    price = (cptraj if yes(g('ETSPriceOverride')) else est).where(on, 0.0)
    pe = R.put('ets.pe', R.put('ets.p', price) * vadj)
    R.put('ets.rf', xr.where(vadj > 0, 1 / vadj.where(vadj > 0, 1.0), 0.0))

    # feebates
    fb = {s: R.put('fb', linear_path(t, g('FeebateIntro'), g('FeebateOutro'), num(i[f'fb.s|all|{s}']),
                                     num(i[f'fb.t|all|{s}'])), s, 'all') for s in FEEBATE_SECTORS}

    # main scenario: explicit or shadow pricing, regulations (EQ-M1.4)
    table = xt.table('main_scenarios')
    names = [r['selected'].lower() for r in table]
    sel = str(g('ScenarioSelected')).lower()
    scn = names.index(sel) + 1 if sel in names else 0
    row = table[scn - 1] if scn else None
    R.put('scn', float(scn))
    explicit = R.put('cp.exp', 1.0 if not scn else float(row['explicit'] == 'Yes'))
    cpx = R.put('cpx', cptraj * explicit)
    shadow = R.put('cp.shd', cptraj - cpx)
    adj_pos = int(float(row['adjustment'])) if scn else 0
    regadj = R.put('regadj', num(g(REG_ADJUSTMENTS[adj_pos - 1])) if adj_pos else 0.0)
    regc = {s: R.put('regc', float(bool(scn) and row[s] == 'Yes'), s, 'all') for s in COVERAGE_SECTORS}
    reg = {s: R.put('reg', shadow * regadj * regc[s], s, 'all') for s in COVERAGE_SECTORS}
    ssc = {s: R.put('ssc', (1.0 if truthy(i[f'fbcov|all|{s}']) else 0.0) * num(g('SPPEffAdjFeebates')), s, 'all')
           for s in COVERAGE_SECTORS}

    # existing carbon pricing (EQ-A2.2): data column of the year, growth after the last data year
    ecp_last = ECP_YEARS[-1]
    xct_c = R.put('xct.c', xr.DataArray([ECP_YEARS.index(min(y, ecp_last)) + 1 for y in years], dims='year',
                                        coords={'year': years}).astype(float))
    for k, sw, gr_ in (('xct.p', 'ExistingCTApply', 'ExistingCTGrowth'), ('xets.p', 'ExistingETSApply',
                                                                          'ExistingETSGrowth')):
        R.put(k, (1 + num(g(gr_))) ** np.maximum(0, t - ecp_last) if yes(g(sw)) else 0.0)
    infl = state['macro.infl'].sel(country=countries)
    ecp = {c: ecp_table(db, c, dict(zip(infl['year'].values, infl.sel(country=c).values))) for c in countries}
    state['_ecp'] = ecp                              # read by section 2 (not a result row)

    # policy rates by sector (EQ-M1.3, EQ-M1.4)
    ees_of = {'pow': 'pow', 'tra': 'trs', 'res': 'res', 'ind': 'ind'}
    for s in COVERAGE_SECTORS:
        if yes(g('CTaxComplimentaryToETS')):
            col = (xct_c - 1).astype(int)
            share = xr.DataArray([[ecp[c][f'ees.{ees_of[cov_group[s]]}'][k] for k in col.values] for c in countries],
                                 dims=['country', 'year'], coords={'country': countries, 'year': years})
            cover = 1 - share
        else:
            cover = R.get('ctcov', s, 'all')
        R.put('ctr', cpx * cover * (1 - etsc[s]), s, 'all')
    for s in COVERAGE_SECTORS:
        R.put('etr', pe * etsc[s] * (1 - obr[s]), s, 'all')
    for s in COVERAGE_SECTORS:
        R.put('shpx', fb[cov_feebate[s]] * ssc[s] + reg[s] + pe * etsc[s] * obr[s], s, 'all')

    # phase-outs of subsidies and price controls (EQ-M1.7)
    pof = {}
    for k, (pol, base, start, per_p, per_b, sh_p, sh_b) in PHASEOUTS.items():
        yes_ = lambda x: is_true(x) or yes(x)
        on_ = (yes_(g(pol)) and (n > 1 or yes_(g(base)))) if k == 'pc' else (yes_(g(base)) if n == 1 else yes_(g(pol)))
        period = g(per_b) if n == 1 else g(per_p)
        share = num(g(sh_b)) if n == 1 else max(num(g(sh_b)), num(g(sh_p)))
        R.put('po.on', float(on_), k, 'all')
        R.put('po.n', period, k, 'all')
        R.put('po.sh', share, k, 'all')
        pof[k] = R.put('pof', np.maximum(1 - share, xr.where(on_ & (t > g(start)), 1 - share * (t - g(start))
                                                             / max(num(period), 1), 1.0)), k, 'all')
    for v, inc, k in (('csf', 'csi', 'cs'), ('pcf', 'pci', 'pc')):
        for pc in PRICE_FUELS:
            fu, se = pc.split('.')
            R.put(v, 1 - num(i[f'{inc}|{fu}|{se}']) * (1 - pof[k]), se, fu)
    for f in ('coa', 'nga', 'oil', 'bio', 'ecy'):
        R.put('psf', 1 - num(i[f'psi|{f}|all']) * (1 - pof['ps']), 'all', f)

    # exemptions, methane fee (EQ-M1.8)
    R.put('exf', xt.constant('exf|all|all'), 'all', 'all')
    R.put('exf', 0.0 if yes(g('AlwaysExemptResLPGKer')) else 1.0, 'res', 'all')
    mfee_p = R.put('mfee.p', linear_path(t, g('MPIntro'), g('MPOutro'), g('MPLevelStart'), g('MPLevelTarget'),
                                         hold=False))
    R.put('mfee', mfee_p * (n > 1) + (cptraj if yes(g('CTforMethane')) else 0.0))
    R.finish()


def settings_stored_path(settings):
    from cpat_model.settings import REPO
    return REPO / 'data' / 'excel_ai_stored' / 'baseline_co2.csv'
