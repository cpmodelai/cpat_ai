"""Section 1, Pigouvian taxes and existing pre-tax wedges (Mitigation rows 185-418). Quantity-free: computed for all
years in the prepare stage, after the fuel | subsector table. EQ-A1.2.

    air pollution   airpol.mc by subsector and fuel: value of averted PM2.5 x the module's concentration coefficients
                    x the combustion factors (base and final); pig.ap by price code: weighted by base-year fuel use
    transport       pig.trb, pig.trg, pig.tr: accident, congestion and road-damage costs per unit of road fuel, from
                    the typed transport co-benefit costs per km and base-year fuel economy
    climate         cc.code: the national social cost of carbon x the generic CO2 factor of the fuel
    totals          pigx (phased in), xcpb (existing carbon pricing change against the embedded year), xpre
The tax itself (ntxg) is in policies (AddEfficientTaxes = Yes is not in Coded CPAT yet).
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.dims import FUELS
from cpat_model.core.rows import Rows, cached, safe_div
from cpat_model.mitigation import ef_data, policies, power_data
from cpat_model.mitigation.prices_data import PRICES

AP_POLLUTANTS = power_data.POLLUTANTS
INDUSTRY = ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr']
BUILDINGS = ['res', 'foo', 'srv']
OIL_SUBSECTORS = ['rod', 'ral', 'avi', 'nav', 'res', 'foo', 'srv'] + INDUSTRY + ['oen']
AIRPOL_ROWS = ([(s, f) for f in ('coa', 'nga') for s in INDUSTRY + BUILDINGS + ['pow']]
               + [(s, f) for f in ('gso', 'die', 'lpg', 'ker') for s in OIL_SUBSECTORS]
               + [('pow', 'oop')] + [(s, 'oop') for s in INDUSTRY])            # Excel-AI row order (191-287)
POWER_SOURCE = {'coa': 'cpp', 'nga': 'gpp', 'oop': 'opp'}                       # module source of the power type
GENERIC_EF = {'coa': ['pow', 'res', 'ind'], 'nga': ['pow', 'res', 'ind'], 'gso': ['rod', 'res'], 'die': ['rod', 'res'],
              'lpg': ['res', 'res', 'ind'], 'ker': ['res', 'ind']}          # EF sectors averaged (Inputs rows 316-322)
XKEY = {'coa.pow': 'pow|coa', 'coa.res': 'res|coa', 'coa.ind': 'ind|coa', 'nga.pow': 'pow|nga', 'nga.res': 'res|nga',
        'nga.ind': 'ind|nga', 'gso.all': 'trs|gso', 'die.all': 'trs|die', 'lpg.all': 'res|lpg', 'ker.all': 'res|ker',
        'oop.all': 'ind|oop', 'bio.all': 'res|bio'}                         # ECP sector | fuel of the price code
CODES = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res', 'ecy.ind', 'gso.all', 'die.all',
         'lpg.all', 'ker.all', 'oop.all', 'bio.all']                        # rows pig.ap ... xpre, in sheet order


def module_sector(s):
    """The air pollution module's source of a subsector (Excel-AI: road, ground level, food, other)."""
    return 'rod' if s == 'rod' else 'gro' if s in ('res', 'srv', 'cst') else 'foo' if s == 'foo' else 'oth'


def generic_ef(db, iso, c):
    """Excel-AI EFGen: the CO2 factor of the fuel averaged over EF sectors (uncalibrated; oil products IEA)."""
    co2 = ef_data.co2_efs(db, iso, c)
    out = {f: float(np.mean([co2[f'{f}|{s}'] for s in sectors])) for f, sectors in GENERIC_EF.items()}
    out['oop'] = c('EFOilIEA')
    return out


def transport_base(db, iso, base_year):
    """Base-year road transport data of the country (Excel-AI Transport1 at row pig.trk): {variable: value}, and the
    row position (0 if missing)."""
    df = db.table('transport_country')
    pairs = list(dict.fromkeys(zip(df['country'], df['year'])))
    key = (iso, str(base_year))
    if key not in pairs:
        return {}, 0
    g = df[(df['country'] == iso) & (df['year'] == str(base_year))]
    vals = {}
    for v, x in zip(g['variable'], g['value']):
        try:
            vals[v] = float(x)
        except (TypeError, ValueError):
            pass
    return vals, pairs.index(key) + 1


def prepare(state, db, inputs, settings, baseline):
    """EQ-A1.2: the Pigouvian rows of section 1."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    c = xt.constant
    t = R.t
    g = lambda name: inputs[name]
    col = lambda fn: np.array([[fn(iso)] for iso in countries])
    tables = state['_fuel']
    ft = lambda f, s, key: col(lambda iso: tables[iso][(f, s)][key])
    yes = lambda name: str(g(name))[:3] == 'Yes'

    R.put('pig.phi', np.minimum(np.maximum(t - R.of('CPIntro') + 1, 0) / max(float(g('AddEfficientTaxesPhaseInYears')
                                                                                    or 0), 1), 1))
    ef_share = {'constant': 0.0, 'Variable': 1.0}.get(str(settings.base['EFSel']), 0.5)
    efw = R.put('pig.efw', ef_share * (t - settings.base_year) / (c('EFEndYear') - settings.base_year))
    vpm = state['air.vpm'].reindex(country=countries)
    vpm = R.put('pig.vpm', np.array([[float(vpm.sel(country=iso, year=max(y, settings.base_year + 1)))
                                      if max(y, settings.base_year + 1) in vpm['year'] else 0.0 for y in years]
                                     for iso in countries]))

    # air pollution cost per GJ by subsector and fuel (airpol.mc), by price code (pig.ap)
    coef = _coefficients(db, countries)
    types = lambda kk, key: col(lambda iso: state['_power'][iso]['types'][kk][key])
    mc, weight = {}, {}
    for s, f in AIRPOL_ROWS:
        src = POWER_SOURCE[f] if s == 'pow' else module_sector(s)
        ef = (lambda i, pol: types(f, f'ap{i}_{pol}')) if s == 'pow' else (lambda i, pol: ft(f, s, f'ef{i}_{pol}'))
        d0, d1 = (sum(col(lambda iso: coef.get(f'{iso}|{src}|{i}', {}).get(f'ap{j}_{pol}', 0.0)) * ef(j, pol)
                      for pol in AP_POLLUTANTS for j in (0, 1)) for i in (0, 1))
        mc[(s, f)] = R.put('airpol.mc', vpm * (d0 * (1 - efw) + d1 * efw) * c('Billion') / power_data.PJ_PER_KTOE
                           / c('Million'), s, f)
        weight[(s, f)] = 1.0 if s == 'pow' else ft(f, s, 'ener0')

    def average(rows):                       # weighted by base-year fuel use; the plain average where it is 0
        w = sum(weight[r] for r in rows)
        return np.where(w == 0, sum(mc[r] for r in rows) / len(rows), safe_div(sum(mc[r] * weight[r] for r in rows), w))
    dp = state['_prices']['domestic']
    gj = lambda code: col(lambda iso: dp[iso][code]['gj'])
    res_coal = col(lambda iso: float(sum(tables[iso][('coa', s)]['ener0'] for s in BUILDINGS)
                                     > c('ApCoalResMin') * sum(p['ener0'] for (f, s), p in tables[iso].items()
                                                               if s in BUILDINGS)))
    ap = {'coa.pow': mc[('pow', 'coa')], 'coa.res': average([(s, 'coa') for s in BUILDINGS]) * res_coal,
          'coa.ind': average([(s, 'coa') for s in INDUSTRY]), 'nga.pow': mc[('pow', 'nga')],
          'nga.res': average([(s, 'nga') for s in BUILDINGS]), 'nga.ind': average([(s, 'nga') for s in INDUSTRY]),
          'ecy.res': 0.0, 'ecy.ind': 0.0, 'oop.all': mc[('pow', 'oop')] * gj('oop.all'), 'bio.all': 0.0}
    for f in ('gso', 'die', 'lpg', 'ker'):
        ap[f'{f}.all'] = average([(s, f) for s in OIL_SUBSECTORS]) * gj(f'{f}.all')

    # transport externalities per unit of road fuel (pig.trb, pig.tr)
    trk = {iso: cached(state, ('transport_base', iso), lambda: transport_base(db, iso, settings.base_year))
           for iso in countries}
    R.put('pig.trk', col(lambda iso: trk[iso][1]))
    tv = lambda name: col(lambda iso: trk[iso][0].get(name, 0.0))
    fe0 = {}
    for f, name in (('gso', 'gasoline'), ('die', 'diesel')):
        own_p, own_l = tv('ownership passenger'), tv('ownership light')
        fe_p, fe_l = tv(f'fuel economy {name} passenger'), tv('fuel economy light')
        fe0[f] = R.put('pig.fe0', np.where(own_p + own_l == 0, fe_p, safe_div(fe_p * own_p + fe_l * own_l, own_p + own_l)),
                       'pas', f)
    wsh = {'gso': R.put('pig.wsh', 1 - tv('share of gasoline for cycle'), 'rod', 'gso')}
    bus, fre = tv('share of diesel for bus'), tv('share of diesel for freight')
    wsh['die'] = R.put('pig.wsh', np.where(bus >= 1, 0.0, 1 - safe_div(fre, 1 - bus)), 'rod', 'die')
    fe_all = {'gso': R.put('pig.fe0', wsh['gso'] * fe0['gso'] + (1 - wsh['gso']) * tv('fuel economy gasoline cycle'),
                           'all', 'gso'),
              'die': R.put('pig.fe0', wsh['die'] * fe0['die'] + (1 - wsh['die']) * tv('fuel economy diesel freight'),
                           'all', 'die')}
    eu, ef = (lambda f: ft(f, 'rod', 'eu')), (lambda f: ft(f, 'rod', 'ef'))
    mu = {'gso': R.put('pig.mu0', safe_div(eu('gso'), eu('gso') + ef('gso')), 'rod', 'gso'),
          'die': R.put('pig.mu0', safe_div(eu('die') + wsh['die'] * (eu('gso') - eu('die')),
                                           eu('die') + ef('die') + wsh['die'] * (eu('gso') + ef('gso') - eu('die')
                                                                                 - ef('die'))), 'rod', 'die')}
    rsh = {f: R.put('pig.rsh0', safe_div(ft(f, 'rod', 'ener0'), col(lambda iso: sum(
        p['ener0'] for (ff, s), p in tables[iso].items() if ff == f))), 'rod', f) for f in ('gso', 'die')}
    kpl = {f: R.put('pig.kpl', fe_all[f] * mu[f] * rsh[f], 'rod', f) for f in ('gso', 'die')}
    costs = state.get('_tcb_costs') or {k: state[f'tran.{k}.km'].reindex(country=countries) for k in ('acc', 'con', 'rdm')}
    trg, base = {}, {}
    for k in ('acc', 'con', 'rdm'):
        a = costs[k]
        base[k] = col(lambda iso: float(a.sel(country=iso, year=settings.base_year)) if settings.base_year in a['year']
                      else 0.0)
        path = np.array([[float(a.sel(country=iso, year=y)) if y in a['year'] else np.nan for y in years]
                         for iso in countries])
        trg[k] = R.put(f'pig.trg.{k}', np.where(base[k] == 0, 0.0, safe_div(path, base[k])))
    trb = {('acc', 'gso'): base['acc'] * kpl['gso'], ('con', 'gso'): base['con'] * kpl['gso'],
           ('acc', 'die'): base['acc'] * kpl['die'], ('con', 'die'): base['con'] * kpl['die'],
           ('rdm', 'die'): base['rdm'] * kpl['die'] * (1 - wsh['die'])}
    for (k, f), v in trb.items():
        R.put(f'pig.trb.{k}', v, 'rod', f)
    tr = {code: 0.0 for code in CODES}
    tr['gso.all'] = trb[('acc', 'gso')] * trg['acc'] + trb[('con', 'gso')] * trg['con']
    tr['die.all'] = trb[('acc', 'die')] * trg['acc'] + trb[('con', 'die')] * trg['con'] + trb[('rdm', 'die')] * trg['rdm']

    # climate cost, totals, existing carbon pricing against the embedded year
    efgen = {iso: generic_ef(db, iso, c) for iso in countries}
    scc = R.of('scc', 'all', 'nat')
    phi, climate = R.of('pig.phi'), float(yes('ClimateEffTax'))
    xct_c = (R.of('xct.c')[0] - 1).astype(int)
    xct_p, xets_p = R.of('xct.p'), R.of('xets.p')
    k_emb = [2021, 2022, 2023, 2024, 2025].index(policies.ecp_embedded_year(settings))
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS]
    for code in CODES:
        fuel, sector = code.split('.')
        R.put('pig.ap', ap[code], sector, fuel)
        efg = col(lambda iso: efgen[iso].get(fuel, 0.0))
        cc = R.put('cc.code', scc * efg * (gj(code) if code in PRICES else 0.0), sector, fuel)
        R.put('pig.tr', tr[code], sector, fuel)
        R.put('pigx', phi * (ap[code] + cc * climate + tr[code]), sector, fuel)
        if fuel == 'ecy':
            xcpb = 0.0
        else:
            key = XKEY[code] if XKEY[code] in xkeys else 'none|none'
            ecp = lambda kind: np.array([(np.zeros(5) if key == 'none|none' else state['_ecp'][iso][f'{kind}|{key}'])
                                         for iso in countries])
            xct, xets = ecp('xct'), ecp('xets')
            xcpb = efg * (xct[:, xct_c] * xct_p + xets[:, xct_c] * xets_p - (xct[:, [k_emb]] + xets[:, [k_emb]]))
        xcpb = R.put('xcpb', xcpb, sector, fuel)
        R.put('xpre', 0.0 if fuel == 'ecy' else R.of('txo', sector, fuel) + R.of('pcsw', sector, fuel)
              + R.of('ppcw', sector, fuel) + xcpb, sector, fuel)
    R.finish()


def _coefficients(db, countries):
    """The air pollution module's concentration coefficients (Excel-AI FromAirPollution ApEf): {country|source|0 or 1:
    {ap0_<pollutant>, ap1_<pollutant>: value}}."""
    df = db.table('air_coefficients')
    out = {}
    for key, var, v in zip(df['key'], df['variable'], df['value']):
        if key.split('|')[0] in countries:
            try:
                out.setdefault(key, {})[var] = float(v)
            except (TypeError, ValueError):
                out.setdefault(key, {})[var] = 0.0
    return out
