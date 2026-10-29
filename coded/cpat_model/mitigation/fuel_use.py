"""Blocks 5-8, fuel use by subsector and fuel (Mitigation sections 5-8): one block per subsector s, one row per fuel f.

prepare  the quantity-free rows: new carbon tax, ETS cost and new taxes per GJ, existing carbon pricing, consumer
         subsidy and price-control wedges, after-tax price, shadow price, efficiency multiple (EQ-M2.4 to EQ-M2.6,
         EQ-A2.2).
step     one year t (later): fuel use by the elasticity model, emissions and revenues.
"""
import numpy as np

from cpat_model.core.dims import COVERAGE_SECTORS, FUELS, SECTORS
from cpat_model.core.rows import Rows
from cpat_model.mitigation import fuel_data, policies
from cpat_model.mitigation.power_data import DEMAND_SUBSECTORS

EXEMPTION_GROUPS = ['all', 'res']                     # rows exf.all.all, exf.res.all
EFFICIENCY_INPUTS = ['AdditionalEfficiencyRoadVehicle', 'AdditionalEfficiencyResidential',
                     'AdditionalEfficiencyIndustrial']   # additional efficiency groups 1-3


def country_table(db, iso, state, settings):
    """The fuel | subsector table of the country (fuel_data; tested in test_data_steps)."""
    d = state['_power'][iso]
    dp = state['_prices']['domestic'][iso]
    return fuel_data.fuel_table(db, iso, settings, d['ela'], d['co2'], d['efcalib'], d['ecp'],
                                policies.ecp_embedded_year(settings), d['nonco2'], dp)


def prepare(state, db, inputs, settings, baseline):
    """EQ-M2.4, EQ-M2.5, EQ-M2.6, EQ-A2.2: the price rows of every fuel block."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    g = lambda name: inputs[name]
    G = lambda name: settings.global_settings.get(name, inputs[name])
    tables = {iso: country_table(db, iso, state, settings) for iso in countries}
    state['_fuel'] = tables
    col = lambda f, s, key: np.array([[tables[iso][(f, s)][key]] for iso in countries])
    first = tables[countries[0]]
    xct_c = (R.of('xct.c')[0] - 1).astype(int)
    xct_p, xets_p = R.of('xct.p'), R.of('xets.p')
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS]
    for s in SECTORS:
        for f in FUELS:
            p = first[(f, s)]
            ef = col(f, s, 'co2ef')
            cov_sector = COVERAGE_SECTORS[p['spos'] - 1]
            exf = R.of('exf', EXEMPTION_GROUPS[p['exempt_group'] - 1], 'all')
            pf = fuel_data.FUELS_ORDER[p['fpos'] - 1]
            ctx = R.put('ctxnew', R.of('ctr', cov_sector, 'all') * ef * R.of('ctcov', 'all', pf) * exf, s, f)
            ets = R.put('ets', R.of('etr', cov_sector, 'all') * ef * exf, s, f)
            rf = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res', 'ecy.ind', 'gso.all',
                  'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all'][p['pfpos'] - 1].split('.')
            ntx = R.put('ntx', R.of('ntxb', rf[1], rf[0]) / col(f, s, 'gj') * exf, s, f)
            nce = R.put('nce', ctx + ets + ntx, s, f)
            def ecp(kind):                    # existing carbon tax or ETS of the ECP sector | fuel, by year
                rows = []
                for iso in countries:
                    k = xkeys[tables[iso][(f, s)]['ecpk'] - 1]
                    rows.append((np.zeros(5) if k == 'none|none' else state['_ecp'][iso][f'{kind}|{k}'])[xct_c])
                return np.array(rows)
            existing = ecp('xct') * xct_p + ecp('xets') * xets_p
            R.put('xcp', ef * existing, s, f)
            xcpd = R.put('xcpd', ef * (existing - col(f, s, 'xcp0')), s, f)
            pf_, ps_ = p['price_code'].split('.')
            csw = R.put('csw', R.of('pcsw', ps_, pf_), s, f)
            pcw = R.put('pcw', R.of('ppcw', ps_, pf_), s, f)
            R.put('atp', np.maximum(R.of('pbc', ps_, pf_) + (nce + xcpd + csw + pcw) * (1 + col(f, s, 'vat')),
                                    G('PriceFloor')), s, f)
            R.put('shp', R.of('shpx', cov_sector, 'all') * ef, s, f)
            add = g(EFFICIENCY_INPUTS[p['eff_group'] - 1])
            R.put('aef', (1 / (1 + col(f, s, 'alpha') + add)) ** (1 + col(f, s, 'eu')), s, f)
    R.finish()


# ---- the year loop
LEAK_FUELS = ['nga', 'lpg', 'ker']                    # residential fuels that may leak to biomass (6b)
GROUP_TOTALS = {'tra': ['rod', 'ral', 'avi', 'nav'], 'bld': ['res', 'foo', 'srv'],
                'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr']}


def leakage_settings(db, iso, base):
    """Residential leakage to biomass (Excel-AI Settings C59-C89): switch, most-used cooking fuel, stove efficiencies,
    substitution elasticity, initially exempt share of the cooking fuel."""
    who = db.table('who_cooking')
    fuel = who.loc[who['code'] == f'{iso}.distn.pcoff.ove', 'main_fuel']
    cross = db.table('ela_cross_price_global')
    subst = cross.loc[(cross['item'] == 'Biomass with respect to LPG') & (cross['variable'] == 'Elasticity'), 'value']
    if str(base['ExemptMostCook'])[:3] == 'Yes':
        raise NotImplementedError('the initially exempt cooking fuel (ExemptMostCook = Yes) needs the HH survey deciles')
    return {'on': str(base['BiomassLeakage'])[:3] == 'Yes', 'fuel': fuel.iloc[0] if len(fuel) else 'lpg',
            'eff': {'nga': base['NatGasEff'], 'lpg': base['LPGEff'], 'ker': base['KerEff']}, 'eff_bio': base['BioEff'],
            'subst': float(subst.iloc[0]), 'exempt_share': 0.0}


def step(state, db, inputs, settings, baseline, t):
    """EQ-M3.1, EQ-M3.2, EQ-M7.1, EQ-M6.1, EQ-M6.2, EQ-A3.3, EQ-A3.4: fuel use, leakage to biomass, biofuels,
    emissions and revenues of every fuel block in year t."""
    from cpat_model.mitigation.gdp import year_rows
    from cpat_model.mitigation.power_data import PJ_PER_KTOE as pj
    from cpat_model.core import excel_ai_tables as xt
    R = year_rows(state, settings)
    k, y = settings.years.index(t), t
    g = lambda name: inputs[name]
    G = lambda name: settings.global_settings.get(name, inputs[name])
    c = xt.constant
    countries = list(settings.countries)
    tables = state['_fuel']
    col = lambda f, s, key: np.array([tables[iso][(f, s)][key] for iso in countries])
    at = lambda var, sector=None, fuel=None, kk=k: R.at(var, kk, sector, fuel)
    gdpi, shock = at('GDPI'), at('SHOCK')
    if '_leak' not in state:
        state['_leak'] = {iso: leakage_settings(db, iso, settings.base) for iso in countries}
    leak = state['_leak'][countries[0]]

    # fuel use by the elasticity model (EQ-M3.1), all subsectors and fuels at once: (sector, fuel, country)
    if '_enel' not in state:
        grid = lambda fn: np.array([[fn(s, f) for f in FUELS] for s in SECTORS])
        state['_enel'] = {key: grid(lambda s, f: col(f, s, key)) for key in ('ener0', 'ey', 'eu', 'eff_exp')}
        state['_enel'].update({var: grid(lambda s, f: R.of(var, s, f)) for var in ('atp', 'shp', 'aef')})
    E = state['_enel']
    if k == 0:
        enel = E['ener0']
    else:
        prev = np.array([[at('enel', s, f, k - 1) for f in FUELS] for s in SECTORS])
        atp, atp0, shp, shp0 = E['atp'][..., k], E['atp'][..., k - 1], E['shp'][..., k], E['shp'][..., k - 1]
        enel = (prev * E['aef'][..., k] * (1 + gdpi) ** E['ey'] * (atp / atp0) ** E['eu']
                * ((atp + shp) / (atp0 + shp0)) ** E['eff_exp'] * shock)
    for i, s in enumerate(SECTORS):
        for j, f in enumerate(FUELS):
            R.set('enel', k, enel[i, j], s, f)

    # biofuels in road transport, aviation and navigation (EQ-A3.3; Mitigation section 5b)
    ela = state['_power'][countries[0]]['ela']
    elas = lambda fuel: np.array([[state['_power'][i]['ela'][f'{kind}|{fuel}|tra'] for i in countries]
                                  for kind in ('inc', 'usg', 'eff', 'aei')])
    bfe, rne = elas('oil'), elas('ren')
    for name, gas_fuel in (('bgs', 'gso'), ('bdi', 'die')):
        if k == 0:
            R.set('trbe', k, _road_biofuel(state, db, settings, name), 'rod', name)
        else:
            prev = at('enel', 'rod', gas_fuel, k - 1)
            R.set('trbe', k, np.where(prev == 0, at('trbe', 'rod', name, k - 1),
                                      at('trbe', 'rod', name, k - 1) * at('enel', 'rod', gas_fuel) / prev), 'rod', name)
    aea = R.set('trbea', k, (1 / (1 + bfe[3] + g('AdditionalEfficiencyRoadVehicle'))) ** (1 + bfe[1]), 'rod', 'obf')
    if k == 0:
        R.set('trbe', k, _road_biofuel(state, db, settings, 'obf'), 'rod', 'obf')
    else:
        atp, atp0 = at('atp', 'rod', 'bio'), at('atp', 'rod', 'bio', k - 1)
        shp, shp0 = at('shp', 'rod', 'bio'), at('shp', 'rod', 'bio', k - 1)
        R.set('trbe', k, at('trbe', 'rod', 'obf', k - 1) * aea * (1 + gdpi) ** bfe[0] * (atp / atp0) ** bfe[1]
              * ((atp + shp) / (atp0 + shp0)) ** (bfe[2] * (1 + bfe[1])) * shock, 'rod', 'obf')
    R.set('trbe', k, at('trbe', 'rod', 'bgs') + at('trbe', 'rod', 'bdi') + at('trbe', 'rod', 'obf'), 'rod', 'bio')
    ren_price = R.set('trpren', k, at('tic', 'pow', 'sol'), 'tra', 'ren')
    rena = R.set('trrena', k, (1 / (1 + rne[3] + g('AdditionalEfficiencyRoadVehicle'))) ** (1 + rne[1]), 'tra', 'ren')
    for s, col_ in (('avi', 'avi'), ('nav', 'nav')):
        if k == 0:
            R.set('ener', k, _renewable_use(db, countries, col_), s, 'ren')
        else:
            ratio = ren_price / at('trpren', 'tra', 'ren', k - 1)
            R.set('ener', k, at('ener', s, 'ren', k - 1) * rena * (1 + gdpi) ** rne[0] * ratio ** rne[1]
                  * ratio ** (rne[2] * (1 + rne[1])) * shock, s, 'ren')

    # residential leakage to biomass (EQ-A3.4; Mitigation section 6b)
    lkxp = (np.clip((y + 1 - g('YearPha')) / g('ExemptPhaseoutPeriod'), 0, 1)
            if str(g('ExemptPhaseout')).upper() == 'TRUE' else 0.0)
    R.set('lkxp', k, lkxp, 'res', 'none')
    for f in LEAK_FUELS:
        vat = col(f, 'res', 'vat')
        lkt = R.set('lkt', k, at('nce', 'res', f) * (1 + vat), 'res', f)
        on = 1.0 if leak['on'] and leak['fuel'] == f else 0.0
        expo = leak['subst'] * leak['eff_bio'] / leak['eff'][f] / c('ResSubstLag')
        if k == 0:
            lkp = R.set('lkp', k, 0.0, 'res', f)
            lkd = R.set('lkd', k, 0.0, 'res', f)
        else:
            lkp = R.set('lkp', k, on * np.minimum((1 + (lkt - at('lkt', 'res', f, k - 1)) / at('atp', 'res', f, k - 1))
                                                  ** expo - 1, 1), 'res', f)
            lkd = R.set('lkd', k, -(at('ener', 'res', f, k - 1) - at('lkx', 'res', f, k - 1)) * leak['eff'][f] * lkp,
                        'res', f)
        R.set('lkb', k, -lkd * leak['eff'][f] / leak['eff_bio'], 'res', f)
        enel = at('enel', 'res', f)
        share = leak['exempt_share'] if leak['fuel'] == f else 0.0
        if k == 0:
            R.set('lkxe', k, 1.0, 'res', f)
            R.set('lkxr', k, 1.0, 'res', f)
            R.set('lkx', k, share * enel, 'res', f)
            R.set('lkxa', k, 0.0, 'res', f)
        else:
            prev = at('enel', 'res', f, k - 1)
            lkxe = R.set('lkxe', k, np.where(prev == 0, 1.0, safe(enel, prev)), 'res', f)
            atp0 = at('atp', 'res', f, k - 1)
            lkxr = R.set('lkxr', k, np.where(atp0 == 0, 1.0, safe(at('atp', 'res', f), atp0)), 'res', f)
            lkx = R.set('lkx', k, at('lkx', 'res', f, k - 1) * lkxe * lkxr ** (col(f, 'res', 'eu') * (lkxp - 1)),
                        'res', f)
            R.set('lkxa', k, lkx - share * enel, 'res', f)
    R.set('lkz', k, 0.0, 'res', 'none')
    for f in LEAK_FUELS:
        R.set('lkc', k, 0.0 if k == 0 else at('lkc', 'res', f, k - 1) + (at('lkd', 'res', f) + at('lkxa', 'res', f)
                                                                         - at('lkxa', 'res', f, k - 1)), 'res', f)
    R.set('lkcb', k, 0.0 if k == 0 else at('lkcb', 'res', 'bio', k - 1) + sum(at('lkb', 'res', f) for f in LEAK_FUELS),
          'res', 'bio')
    R.set('lks', k, sum(at('lkc', 'res', f) for f in LEAK_FUELS) + at('lkcb', 'res', 'bio'), 'res', 'all')

    # fuel use, emissions and revenues (EQ-M3.2, EQ-M7.1, EQ-M6.1, EQ-M6.2)
    leak_rows = ['lkz.none', 'lkc.nga', 'lkc.lpg', 'lkc.ker', 'lkcb.bio']
    ef_share = {'constant': 0.0, 'Variable': 1.0}.get(str(settings.base['EFSel']), 0.5)
    ef_years = (y - settings.base_year) / (c('EFEndYear') - settings.base_year)
    first = tables[countries[0]]
    if '_fu' not in state:                          # the price rows and factors of every fuel block, (sector, fuel, ...)
        grid = lambda fn: np.array([[fn(s, f) for f in FUELS] for s in SECTORS])
        code = lambda s, f: first[(f, s)]['price_code'].split('.')
        F = {key: grid(lambda s, f: col(f, s, key)) for key in ('co2ef', 'ef0_ch4', 'ef1_ch4', 'vat')}
        F.update({var: grid(lambda s, f: R.of(var, s, f))
                  for var in ('xcpd', 'nce', 'csw', 'pcw', 'ctxnew', 'ntx', 'ets', 'xcp')})
        F.update({f'{var}.p': grid(lambda s, f: R.of(var, code(s, f)[1], code(s, f)[0])) for var in ('etx', 'vat', 'esub')})
        F['leak'] = [[leak_rows[first[(f, s)]['leak_pos'] - 1].split('.') for f in FUELS] for s in SECTORS]
        state['_fu'] = F
    F = state['_fu']
    x = {var: F[var][..., k] for var in ('xcpd', 'nce', 'csw', 'pcw', 'ctxnew', 'ntx', 'ets', 'xcp', 'etx.p', 'vat.p',
                                         'esub.p')}
    leak_now = {name: at(name.split('.')[0], 'res', name.split('.')[1]) for name in leak_rows}
    use = np.array([[at('trbe', 'rod', 'bio') if (s, f) == ('rod', 'bio') else at('enel', s, f) for f in FUELS]
                    for s in SECTORS])
    lk = np.array([[leak_now[f'{v}.{fu}'] for v, fu in row] for row in F['leak']])
    ener = use + lk
    vat = F['vat']
    e = ener * pj
    out = {'ener': ener, 'co2': ener * pj * F['co2ef'],
           'ch4': ener * (F['ef0_ch4'] + (F['ef1_ch4'] - F['ef0_ch4']) * ef_share * ef_years) / c('tPerKt'),
           'rtx': e * (x['etx.p'] + x['vat.p'] + x['xcpd'] * (1 + vat)), 'rsub': e * x['esub.p'],
           'rnew': e * (x['ctxnew'] + x['ntx'] + x['ets'] * at('ets.rf') + x['nce'] * vat), 'rxcp': e * x['xcp'],
           'rex': e * x['ntx'], 'rvt': e * (x['vat.p'] + (x['xcpd'] + x['nce'] + x['csw'] + x['pcw']) * vat),
           'rsr': e * ((x['csw'] + x['pcw']) * (1 + vat))}
    for i, s in enumerate(SECTORS):
        for var, a in out.items():
            for j, f in enumerate(FUELS):
                R.set(var, k, a[i, j], s, f)
        total = sum(ener[i, j] for j in range(len(FUELS))) + (at('ener', s, 'ren') if s in ('avi', 'nav') else 0.0)
        R.set('ener', k, total, s, 'all')
        R.set('eldem', k, at('dem', s, 'ecy') if s in DEMAND_SUBSECTORS else 0.0, s, 'ecy')
    for grp, subs in GROUP_TOTALS.items():
        extra = at('ener', 'avi', 'ren') + at('ener', 'nav', 'ren') if grp == 'tra' else 0.0
        R.set('ener', k, sum(at('ener', s, f) for s in subs for f in FUELS) + extra, grp, 'all')


def safe(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b != 0, a / np.where(b != 0, b, 1.0), 0.0)


def _road_biofuel(state, db, settings, fuel):
    """Base-year road biofuel use (ktoe; Excel-AI trp.eb2): Balances road bgs, bdi, obf, or EnergyCons enc.<fuel> rod."""
    from cpat_model.mitigation import power_data
    use_bal = str(settings.base['BalancesOrConsumption'])[:3] == 'Bal'
    out = []
    for iso in settings.countries:
        if use_bal:
            out.append(power_data.balances(db, iso, settings.base_year).get('road', {}).get(fuel, 0.0))
        else:
            out.append(_consumption(db, iso, fuel, 'rod'))
    return np.array(out)


def _consumption(db, iso, fuel, sector):
    """EnergyCons enc.<fuel> of the subsector (the first row of the code; blank or missing is 0)."""
    cons = db.table('energy_consumption')
    g = cons[(cons['code'] == f'{iso.lower()}.mit.enc.{fuel}') & (cons['sector'] == sector)]
    return float(g['value'].iloc[0]) if len(g) and g['value'].iloc[0] not in ('', None) else 0.0


def _renewable_use(db, countries, sector):
    """Base-year renewable fuel use in aviation and navigation (EnergyCons enc.ren; Excel-AI trp.rn0)."""
    return np.array([_consumption(db, iso, 'ren', sector) for iso in countries])
