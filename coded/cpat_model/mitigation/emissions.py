"""Emissions of the year (Mitigation sections 13-14): energy CO2 by sector group, fuel and coverage sector, the ETS
check, other greenhouse gases and methane, Kaya decomposition. EQ-M7.1, EQ-M7.2, EQ-A7.2, EQ-A7.3.

co2       section 13: CO2 totals, coverage-sector CO2, ETS cap gap and next-price proposal, changes against the baseline
ghg       section 14: population, non-energy drivers, methane by source (fee abatement), the inventory by UNFCCC
          category and gas (data years from the inventory, later years by drivers), methane fee revenue
kaya      section 13 (end): Kaya identity, reads section 14
ndc       section 14 NDC rows: after the year loop (they read the baseline at the NDC target year)
carbon_pricing  section 17: carbon pricing indicators
pollutants      section 15: local air pollutants by subsector and source (outputs to the air pollution module)
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.dims import COVERAGE_SECTORS, FUELS, SECTOR_GROUP, SECTORS
from cpat_model.core.rows import cached, safe_div
from cpat_model.mitigation import ghg_data, header, policies
from cpat_model.mitigation.gdp import year_rows
from cpat_model.mitigation.power import TYPES
from cpat_model.mitigation.totals import GROUPS, reference

CATS = ['enr', 'ipr', 'agr', 'lucf', 'wst', 'oth']
GASES = ['co2', 'ch4', 'n2o', 'fga']
CH4_SOURCES = ['og', 'dg', 'cm', 'bm', 'liv', 'ric', 'wst']      # oil and gas, downstream gas, coal mining, biomass, ...
CH4_FUEL_SOURCES = CH4_SOURCES[:4]
CH4_KEY = {'og': 'oil', 'dg': 'oil', 'cm': 'coa', 'bm': 'oil', 'liv': 'liv', 'ric': 'ric', 'wst': 'tot'}
CH4_SHARE = {'og': 'per_upstream_og', 'dg': 'per_downstream_g', 'cm': 'per_upstream_c', 'bm': 'per_biomass',
             'liv': 'per_livestock', 'ric': 'per_rice'}
CH4_FEE = {'og': 'fossil fuel production', 'dg': 'downstream gas', 'cm': 'fossil fuel production', 'bm': 'biomass',
           'liv': 'agriculture', 'ric': 'agriculture', 'wst': 'waste'}
CH4_DECLINE = {'og': 'oil and natural gas', 'dg': 'oil and natural gas', 'cm': 'coal', 'bm': 'oil and natural gas',
               'liv': 'agriculture', 'ric': 'agriculture', 'wst': 'waste'}
DRIVER = {'agr': 'Agriculture', 'wst': 'Waste', 'oth': 'Other'}
PRD = {'oil': ('oop', 'oil'), 'coa': ('coa', 'coal'), 'nga': ('nga', 'natural gas')}   # production fuel, elasticity name
PI_GJ = {'oil': 'MethGJperBbl', 'coa': 'MethGJperT', 'nga': 'MethGJperMMBtu'}
PI_FEE = {'oil': 'og', 'coa': 'cm', 'nga': 'og'}


def _yes(x):
    return str(x)[:3] == 'Yes'


def _yes_row(values):
    """A Yes/No input row of the year, by country."""
    return np.array([_yes(v) for v in np.atleast_1d(values)])


def co2(state, db, inputs, settings, baseline, t):
    """EQ-M7.1: CO2 by sector group, fuel and coverage sector; ETS cap gap and next price (Mitigation section 13)."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    c = xt.constant
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    ref = lambda var, sector=None, fuel=None: reference(R, baseline, k, var, sector, fuel)
    for g in GROUPS:
        R.set('co2', k, sum(at('co2', s, f) for s in SECTORS if SECTOR_GROUP[s] == g for f in FUELS), g, 'all')
    R.set('co2', k, sum(at('co2', 'pow', kk) for kk in TYPES), 'pow', 'all')
    for f in FUELS:
        R.set('co2', k, sum(at('co2', s, f) for s in SECTORS) + (at('co2', 'pow', f) if f in TYPES else 0.0), 'all', f)
    total = R.set('co2', k, sum(at('co2', s, f) for s in SECTORS for f in FUELS) + at('co2', 'pow', 'all'), 'all', 'all')
    co2ref = R.set('co2.ref', k, ref('co2', 'all', 'all'), 'all', 'all')
    R.set('co2.pct', k, total / co2ref - 1, 'all', 'all')
    sec = {e: R.set('co2.sec', k, at('co2', 'pow', 'all') if e == 'pow' else sum(at('co2', e, f) for f in FUELS), e, 'all')
           for e in COVERAGE_SECTORS}
    ets = R.set('co2.ets', k, sum(sec[e] * at('etsc', e, 'all') for e in COVERAGE_SECTORS), 'all', 'all')
    cap = R.set('co2.cap', k, at('ets.cap'), 'all', 'all')
    R.set('co2.gap', k, np.where(cap > 0, safe_div(ets, cap) - 1, 0.0), 'all', 'all')
    bce = at('ets.bce')
    with np.errstate(divide='ignore', invalid='ignore'):
        lr = np.where((cap <= 0) | (cap >= bce) | (ets >= bce), 0.0, np.log(cap / bce) / np.log(ets / bce))
    lr = R.set('ets.lr', k, lr, 'all', 'all')
    p = at('ets.p')
    with np.errstate(invalid='ignore'):
        proposal = p * lr ** settings.global_settings['ETSNextPriceExponent']
    R.set('ets.next', k, np.where((p <= 0) | (lr == 0), at('ets.est'), proposal), 'all', 'all')
    R.set('bco2.chk', k, sum(at('bco2', e, 'all') for e in COVERAGE_SECTORS) - co2ref, 'all', 'all')
    R.set('co2.chk', k, np.abs(total - sum(at('co2', g, 'all') for g in GROUPS + ['pow']))
          + np.abs(total - sum(at('co2', 'all', f) for f in FUELS)), 'all', 'all')
    for sector, fuel in [('all', f) for f in FUELS] + [(g, 'all') for g in GROUPS + ['pow']]:
        R.set('cchg', k, at('co2', sector, fuel) - ref('co2', sector, fuel), sector, fuel)
    gtot = at('gtot') * c('HoursYr')
    R.set('co2.grid', k, safe_div(at('co2', 'pow', 'all') * c('Million'), gtot), 'pow', 'all')
    R.set('co2.chg', k, total - co2ref, 'all', 'all')


def country_data(db, iso, settings):
    """The data of section 14 for one country (ghg_data)."""
    inv, pos, ghg_year = ghg_data.inventory(db, iso)
    meth = ghg_data.methane(db, iso)
    mi = ghg_data.methane_inputs(db)
    find = lambda text: next(v for p, v in mi.items() if text in p)
    c = xt.constant
    prd0 = ghg_data.production(db, iso, settings.base_year)
    base = inv.get(ghg_year, {})
    d = {'inv': inv, 'pos': pos, 'ghg_year': ghg_year, 'pop': ghg_data.population(db, iso),
         'ela': ghg_data.nonenergy_elasticities(db),
         'wd': ghg_data.world_demand(db, settings.global_settings['GlobalEnergyDemand']),
         'prd0': {f: prd0[PRD[f][0]] for f in PRD}, 'invb': {g: base.get(g, 0.0) for g in
                                                           ('enr.ch4', 'agr.ch4', 'wst.ch4', 'lucf.co2')}}
    d['prd_ela'] = {f: find(f'Elasticity of demand w/r/price - {PRD[f][1]}') for f in PRD}
    d['pass'] = find('Pass-through of methane fee')
    src = {}
    act0 = {'og': d['prd0']['oil'] + d['prd0']['nga'], 'dg': ghg_data.consumption_total(db, iso, 'nga'),
            'cm': d['prd0']['coa'], 'bm': ghg_data.consumption_total(db, iso, 'bio'), 'liv': 1.0, 'ric': 1.0, 'wst': 1.0}
    meth_avg = ghg_data.methane(db, 'AVG')     # CH4Inputs averages: the curve where the country value is 0 or missing
    for s in CH4_SOURCES:
        row = meth.get(CH4_KEY[s], {})
        curve = lambda k: (row[k] if row.get(k) and row[k] == row[k]          # 0, blank or NaN: the average (legacy;
                           else meth_avg.get(CH4_KEY[s], {}).get(k, 0.0))   # Excel-AI 1.0.2 ch4.abc, issue I152)
        share = 1.0 if s == 'wst' else meth.get(CH4_KEY[s] if s in ('liv', 'ric', 'cm') else 'oil', {}).get(CH4_SHARE[s], 0.0)
        src[s] = {'share': share, 'act0': act0[s], 'a': curve('avg_pow_a'), 'b': curve('avg_pow_b'),
                  'gwp': c('GWPCH4F') if s in CH4_FUEL_SOURCES else c('GWPCH4NF'),
                  'fee': 1.0 if _yes(find(f'Methane fee applies to {CH4_FEE[s]}')) else 0.0,
                  'decline': find(f'autonomous technological improvement - {CH4_DECLINE[s]}')}
    tot = sum(src[s]['act0'] for s in CH4_FUEL_SOURCES)
    for s in CH4_FUEL_SOURCES:
        src[s]['capped'] = min(c('MethShareCap') * src[s]['act0'] / tot, src[s]['share']) if tot else src[s]['share']
    capped = sum(src[s]['capped'] for s in CH4_FUEL_SOURCES)
    for s in CH4_SOURCES:
        if s in CH4_FUEL_SOURCES:
            src[s]['weight'] = src[s]['capped'] / capped if capped else 0.0
        else:
            src[s]['capped'] = src[s]['weight'] = src[s]['share']
        inv_gas = {'liv': 'agr.ch4', 'ric': 'agr.ch4', 'wst': 'wst.ch4'}.get(s, 'enr.ch4')
        src[s]['em0'] = d['invb'][inv_gas] * src[s]['weight'] * c('ktPerMt') / src[s]['gwp']
    d['src'] = src
    d['flare'] = meth.get('oil', {}).get('per_flare', 0.0)
    return d


def ghg(state, db, inputs, settings, baseline, t):
    """EQ-M7.2, EQ-A7.2, EQ-A7.3: other greenhouse gases and methane by source (Mitigation section 14)."""
    R = year_rows(state, settings)
    k, y = settings.years.index(t), t
    c = xt.constant
    countries = list(settings.countries)
    if '_ghg' not in state:
        state['_ghg'] = {iso: cached(state, ('ghg', iso), lambda: country_data(db, iso, settings)) for iso in countries}
    D = [state['_ghg'][iso] for iso in countries]
    col = lambda fn: np.array([fn(d) for d in D])
    at = lambda var, sector=None, fuel=None, kk=k: R.at(var, kk, sector, fuel)
    ref = lambda var, sector=None, fuel=None: reference(R, baseline, k, var, sector, fuel)
    first = k == 0

    pop = R.set('pop', k, col(lambda d: d['pop'][y]), 'all', 'all')
    popg = R.set('pop.g', k, pop / (col(lambda d: d['pop'][y - 1]) if first else at('pop', 'all', 'all', k - 1)) - 1,
                 'all', 'all')
    gpcg = R.set('gdppc.g', k, (1 + at('gdp.pos.pct')) / (1 + popg) - 1, 'all', 'all')
    h = R.set('ghg.h', k, col(lambda d: d['pos'].get(y, 0)), 'all', 'all')
    co2, co2ref = at('co2', 'all', 'all'), at('co2.ref', 'all', 'all')
    m = R.set('ghg.m', k, np.where(_yes_row(at('AdditionMitigationPoliciesNonEnergy')) & (co2ref > 0),
                                   safe_div(co2, co2ref), 1.0), 'all', 'all')
    if first:
        gi = R.set('ghg.gi', k, 0.0, 'ind', 'all')
    else:
        ind0 = at('co2', 'ind', 'all', k - 1)
        gi = R.set('ghg.gi', k, np.where(ind0 == 0, 0.0, safe_div(at('co2', 'ind', 'all'), ind0) - 1), 'ind', 'all')
    dr = {}
    for cat, name in DRIVER.items():
        inc_e, pop_e = D[0]['ela'][name]
        dr[cat] = R.set('ghg.dr', k, 1.0 if first else (1 + gpcg) ** inc_e * (1 + popg) ** pop_e * m
                        / at('ghg.m', 'all', 'all', k - 1), cat, 'all')

    # methane by source (EQ-A7.3)
    mfee = at('mfee')
    G = settings.global_settings
    for f in ('oil', 'coa', 'nga'):
        R.set('ch4.wd', k, col(lambda d: d['wd'][f][y]), 'all', f)
    src = lambda s, key: col(lambda d: d['src'][s][key])
    abt = {}
    for s in CH4_SOURCES:
        abt[s] = R.set('ch4.abt', k, np.minimum(1, np.maximum(0, src(s, 'a') * np.power(mfee * src(s, 'gwp') * src(s, 'fee'),
                                                                                        src(s, 'b')))), 'all', s)
    for s, prd0 in (('og', lambda d: d['prd0']['oil'] + d['prd0']['nga']), ('cm', lambda d: d['prd0']['coa'])):
        fk0 = col(prd0)
        R.set('ch4.fk', k, 0.0 if first else np.where(fk0 == 0, 0.0, safe_div(
            mfee * src(s, 'gwp') * src(s, 'fee') * c('tPerKt') * src(s, 'em0'), fk0) * (1 - abt[s])), 'all', s)
    for f in ('oil', 'coa', 'nga'):
        fk = PI_FEE[f]
        pi = 1.0 if first else 1 + (at('ch4.fk', 'all', fk) - at('ch4.fk', 'all', fk, k - 1)) / (
            at('gp', 'int', f) * c('MethGJperKtoe') / c(PI_GJ[f])) * D[0]['pass']
        R.set('ch4.pi', k, pi, 'all', f)
        if y <= settings.base_year + 1:
            prd = col(lambda d: d['prd0'][f])
        else:
            prd = at('ch4.prd', 'all', f, k - 1) * np.power(pi, col(lambda d: d['prd_ela'][f])) \
                * at('ch4.wd', 'all', f, k - 1) / at('ch4.wd', 'all', f, k - 2)
        R.set('ch4.prd', k, prd, 'all', f)
    act = {'og': at('ch4.prd', 'all', 'oil') + at('ch4.prd', 'all', 'nga'), 'dg': at('ener', 'all', 'nga'),
           'cm': at('ch4.prd', 'all', 'coa'), 'bm': at('ener', 'all', 'bio')}
    for s, cat in (('liv', 'Agriculture'), ('ric', 'Agriculture'), ('wst', 'Waste')):
        inc_e, pop_e = D[0]['ela'][cat]
        act[s] = 1.0 if first else at('ch4.act', 'all', s, k - 1) * (1 + gpcg) ** inc_e * (1 + popg) ** pop_e
    for s in CH4_SOURCES:
        act[s] = R.set('ch4.act', k, act[s], 'all', s)
    em = {}
    for s in CH4_SOURCES:
        intensity = R.set('ch4.int', k, (1 - src(s, 'decline')) ** max(0, y - D[0]['ghg_year']), 'all', s)
        em[s] = R.set('ch4.em', k, safe_div(src(s, 'em0') * act[s], src(s, 'act0')) * intensity * (1 - abt[s]), 'all', s)
    ef_share = {'constant': 0.0, 'Variable': 1.0}.get(str(settings.base['EFSel']), 0.5)
    ef_years = (y - settings.base_year) / (c('EFEndYear') - settings.base_year)
    tables = state['_power']
    for f in ('coa', 'nga', 'oop', 'bio'):
        e0 = np.array([tables[iso]['nonco2'].get(f'pow.{f}.ch4', (0.0, 0.0))[0] for iso in countries])
        e1 = np.array([tables[iso]['nonco2'].get(f'pow.{f}.ch4', (0.0, 0.0))[1] for iso in countries])
        R.set('ch4', k, at('pe', 'pow', f) * (e0 + (e1 - e0) * ef_share * ef_years) / c('tPerKt'), 'pow', f)
    for g in GROUPS:
        R.set('ch4.c', k, sum(at('ch4', s, f) for s in SECTORS if SECTOR_GROUP[s] == g for f in FUELS), g, 'all')
    R.set('ch4.c', k, sum(at('ch4', 'pow', f) for f in ('coa', 'nga', 'oop', 'bio')), 'pow', 'all')
    ch4c = R.set('ch4.c', k, sum(at('ch4.c', g, 'all') for g in GROUPS + ['pow']), 'all', 'all')
    sup = R.set('ch4.sup', k, sum(em[s] for s in CH4_FUEL_SOURCES), 'all', 'all')

    # greenhouse gases by UNFCCC category and gas (EQ-M7.2)
    stored = policies.stored_baseline(policies.settings_stored_path(settings), tuple(countries), tuple(settings.years))
    gy = D[0]['ghg_year']
    kc = np.array([stored['ch4c'].sel(country=iso, year=gy).item() + stored['ch4sup'].sel(country=iso, year=gy).item()
                   for iso in countries]) * c('GWPCH4F') / c('ktPerMt')
    kk = R.set('ghg.k', k, safe_div(col(lambda d: d['invb']['enr.ch4']), kc), 'enr', 'ch4')
    R.set('ghg.flr', k, safe_div(c('FlareCO2perCH4') * col(lambda d: d['flare']) * src('og', 'em0') * act['og'],
                                 src('og', 'act0')) * abt['og'] / c('ktPerMt'), 'enr', 'co2')
    data = lambda key: col(lambda d: d['inv'].get(y, {}).get(key, 0.0))
    has = h > 0
    prev = lambda cat, gas: 0.0 if first else at('ghg', cat, gas, k - 1)
    inv = {}
    for cat in CATS:
        for gas in GASES:
            if (cat, gas) == ('enr', 'co2'):
                v = co2 + at('ghg.flr', 'enr', 'co2')
            elif (cat, gas) == ('enr', 'ch4'):
                v = kk * (ch4c + sup) * c('GWPCH4F') / c('ktPerMt')
            else:
                if first:
                    model = 0.0
                elif cat == 'enr':
                    model = prev(cat, gas) * (np.where(at('co2', 'all', 'all', k - 1) == 0, 1.0, safe_div(
                        co2, at('co2', 'all', 'all', k - 1))) if gas == 'n2o' else 1.0)
                elif cat == 'ipr':
                    model = prev(cat, gas) * (1 + np.where(_yes_row(at('IndustrialProcessEmissionsScaleEner')), gi, 0.0))
                elif cat == 'lucf':
                    if gas == 'co2':
                        p0 = prev(cat, gas)
                        model = np.where(p0 < 0, p0, p0 / at('ghg.m', 'all', 'all', k - 1) * m
                                         - np.abs(col(lambda d: d['invb']['lucf.co2']))
                                         * at('LULUCFAnnualEmissionsDecline'))
                    else:
                        model = prev(cat, gas)
                else:
                    model = prev(cat, gas) * dr[cat]
                if (cat, gas) == ('agr', 'ch4'):
                    model = (em['liv'] + em['ric']) * c('GWPCH4NF') / c('ktPerMt')
                elif (cat, gas) == ('wst', 'ch4'):
                    model = em['wst'] * c('GWPCH4NF') / c('ktPerMt')
                v = np.where(has, data(f'{cat}.{gas}'), model)
            inv[(cat, gas)] = R.set('ghg', k, v, cat, gas)
    for gas in GASES:
        R.set('ghg', k, sum(inv[(cat, gas)] for cat in CATS if cat != 'lucf'), 'all', gas)
    for cat in CATS:
        R.set('ghg', k, sum(inv[(cat, gas)] for gas in GASES), cat, 'all')
    total = R.set('ghg', k, sum(at('ghg', 'all', gas) for gas in GASES), 'all', 'all')
    R.set('ghg.inc', k, total + at('ghg', 'lucf', 'all'), 'all', 'all')
    gref = R.set('ghg.ref', k, ref('ghg', 'all', 'all'), 'all', 'all')
    R.set('ghg.pct', k, np.where(gref == 0, 0.0, safe_div(total, gref) - 1), 'all', 'all')
    R.set('ghg.chg', k, total - gref, 'all', 'all')
    fee = lambda ems: sum(ems[s] * src(s, 'gwp') * src(s, 'fee') for s in CH4_SOURCES) * mfee * c('tPerKt') / c('USDperM')
    R.set('ch4.rev', k, fee(em), 'all', 'all')
    emf = dict(em)
    for s, key in (('dg', 'dg'), ('bm', 'bm')):
        emf[s] = safe_div(src(s, 'em0') * at('ch4bs', key, 'all'), src(s, 'act0')) * at('ch4.int', 'all', s) * (1 - abt[s])
    for s in CH4_SOURCES:
        R.set('ch4.emf', k, emf[s], 'all', s)
    R.set('ch4.revf', k, fee(emf), 'all', 'all')
    R.set('ch4bs.chk', k, np.abs(at('ch4bs', 'dg', 'all') - act['dg']) + np.abs(at('ch4bs', 'bm', 'all') - act['bm'])
          if inputs.number == 1 else 0.0, 'all', 'all')
    for cat in CATS:
        R.set('gchg', k, at('ghg', cat, 'all') - ref('ghg', cat, 'all'), cat, 'all')
    for gas in GASES:
        R.set('gchg', k, at('ghg', 'all', gas) - ref('ghg', 'all', gas), 'all', gas)


def kaya(state, db, inputs, settings, baseline, t):
    """Kaya identity: population, GDP per capita, energy intensity, carbon intensity, and their indices to the base
    year (Mitigation section 13)."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    c = xt.constant
    at = lambda var, sector=None, fuel=None, kk=k: R.at(var, kk, sector, fuel)
    gdp = at('gdp.usd', 'all', 'all')
    pop = R.set('kaya', k, at('pop', 'all', 'all') / c('Thousand'), 'all', 'pop')
    R.set('kaya', k, safe_div(gdp, pop), 'all', 'gpc')
    tpes = R.set('kaya', k, at('ener', 'all', 'all') + sum(at('pe', 'pow', kk) for kk in TYPES[3:8]), 'all', 'tpes')
    R.set('kaya', k, safe_div(tpes, gdp), 'all', 'ei')
    R.set('kaya', k, safe_div(at('ghg', 'all', 'co2') * c('Thousand'), tpes), 'all', 'ci')
    for key, var, sector, fuel in (('pop', 'kaya', 'all', 'pop'), ('gdp', 'gdp.usd', 'all', 'all'),
                                   ('gpc', 'kaya', 'all', 'gpc'), ('ei', 'kaya', 'all', 'ei'),
                                   ('ci', 'kaya', 'all', 'ci'), ('co2', 'ghg', 'all', 'co2')):
        R.set('kidx', k, safe_div(at(var, sector, fuel), at(var, sector, fuel, 0)), 'all', key)   # index, base year = 1
    R.set('kidx', k, at('kidx', 'all', 'pop') * at('kidx', 'all', 'gpc') * at('kidx', 'all', 'ei')
          * at('kidx', 'all', 'ci'), 'all', 'chk')


NDC_TYPES = ['BAU', 'Fixed', 'Historical', 'Intensity', 'Unquantifiable']


def _ndc_row(db, iso, sub):
    df = db.table('ndcs')
    key = sub if sub in ('First round', 'Second round') else 'Latest*'
    g = df[(df['country'] == iso) & (df['round'] == key)]
    return f'{iso}|{key}', (g.iloc[0].to_dict() if len(g) else None)


def _num(x):
    """Excel N() / a blank cell read as a number: the number, else 0."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _value(x):
    """Excel VALUE(): the number, else None (an error)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ndc(state, db, inputs, settings, baseline):
    """EQ-A7.4: the NDC target of the country and the gap to it (Mitigation section 14, NDC rows). After the year loop:
    the target level reads the baseline (scenario 1) at the target year. 'N/A' (Excel-AI's text) is NaN here."""
    R = year_rows(state, settings)
    years, countries = settings.years, list(settings.countries)
    c = xt.constant
    na = np.nan
    G = settings.global_settings
    w = header.weo(db, {f'{iso}.NGDP_R.A' for iso in countries})
    hist = db.table('ghg_history')

    def base_row(var, sector, fuel):
        if baseline is None:
            return R.of(var, sector, fuel)
        return baseline[var].sel(sector=sector, fuel=fuel, country=countries, year=years).values

    bs_base, inc_base = base_row('ndc.bs', 'all', 'all') if baseline is not None else None, base_row('ghg.inc', 'all', 'all')
    rows = {}
    for i, iso in enumerate(countries):
        key, r = _ndc_row(db, iso, str(inputs['NDCs']))
        get = lambda col: (r.get(col, '') if r else None)       # None: no NDC row (IFERROR branch)
        typ = r['type'] if r and r.get('type') else 'Unquantifiable'
        kind = NDC_TYPES.index(typ) + 1 if typ in NDC_TYPES else len(NDC_TYPES)
        ty1, ty2 = get('ty1'), get('ty2')
        ty1 = '' if ty1 is None else _num(ty1)
        ty2 = '' if ty2 is None else _num(ty2)
        alt = str(inputs['NDCTargetYear']) != 'Main*' and _num(ty2) > 0
        try:
            ty = min(c('NDCYrCap'), float(ty2 if alt else ty1))
        except (TypeError, ValueError):
            ty = c('NDCYrCap')
        ref_year = '' if get('ref') is None else (_num(get('ref')) if get('ref') != '' else 0.0)
        x = {s: ('' if get(f'{s}{2 if alt else 1}') is None else str(get(f'{s}{2 if alt else 1}'))) for s in 'uc'}
        lu = '' if get('lulucf') is None else get('lulucf')
        gas = 'CO2' if get('gases') == 'CO2' else 'GHGs'
        co2 = R.of('ghg', 'all', 'co2')[i] + (R.of('ghg', 'lucf', 'co2')[i] if lu == 'Includes' else 0.0)
        inc = R.of('ghg.inc', 'all', 'all')[i]
        bs = co2 if gas == 'CO2' else (inc if lu == 'Includes' else R.of('ghg', 'all', 'all')[i])
        own_bs = bs_base[i] if bs_base is not None else bs
        at_year = lambda row, year: row[years.index(int(year))] if _value(year) is not None and int(_value(year)) in years \
            and float(year) == int(float(year)) else na
        bty, bi = at_year(own_bs, ty), at_year(inc_base[i], ty)
        hk = ('co2|' if gas == 'CO2' else 'inc|' if lu == 'Includes' else 'exc|') + _fmt(ref_year)
        grp, yr = hk.split('|')
        hh = hist[(hist['country'] == iso) & (hist['group'] == grp) & (hist['year'] == yr)]['value']
        hh = float(hh.iloc[0]) if len(hh) and hh.iloc[0] not in ('', None) else na
        hc = ('tinc' if lu == 'Includes' else 'texc') + ('.co2' if gas == 'CO2' else '.tot')
        inv = state['_ghg'][iso]['inv']
        hv = inv.get(int(ref_year), {}).get(hc, na) if _value(ref_year) is not None else na
        h = at_year(own_bs, ref_year)
        if np.isnan(h):
            h = hv if not np.isnan(hv) else hh
        weo_r = w.get(f'{iso}.NGDP_R.A', ({}, 0))[0]
        gdp_ref = weo_r.get(int(ref_year), na) if _value(ref_year) is not None else na
        gdp_ty = weo_r.get(int(ty), na)
        hi = h / gdp_ref * gdp_ty if gdp_ref else na
        f = {s: (1 + _value(x[s])) if _value(x[s]) is not None else na for s in 'uc'}
        lv = {s: [bty * f[s], f[s] - 1, h * f[s], hi * f[s], bty][kind - 1] for s in 'uc'}
        rr = {s: 1 - lv[s] / bty if bty else na for s in 'uc'}
        nums = [v for v in rr.values() if not np.isnan(v)]
        rr['a'] = float(np.mean(nums)) if nums else 0.0
        cond = {'Unconditional': 'u', 'Conditional': 'c'}.get(str(inputs['Conditionality']))
        rr['sel'] = rr['a'] if cond is None or np.isnan(rr[cond]) else rr[cond]
        lvl = {s: na if np.isnan(bi * rr[s]) else min(bi, bi * (1 - rr[s])) for s in ('u', 'c', 'sel')}
        inc0 = inc_base[i][0]
        for kk in range(len(years)):
            for var, sector, fuel, v in (
                    ('ndc.key', 'all', 'all', key), ('ndc.typ', 'all', 'all', typ), ('ndc.k', 'all', 'all', kind),
                    ('ndc.ty', 'all', 'ty1', ty1), ('ndc.ty', 'all', 'ty2', ty2), ('ndc.alt', 'all', 'all', float(alt)),
                    ('ndc.ty', 'all', 'all', ty), ('ndc.ref', 'all', 'all', ref_year), ('ndc.x', 'all', 'u', x['u']),
                    ('ndc.x', 'all', 'c', x['c']), ('ndc.lu', 'all', 'all', lu), ('ndc.gas', 'all', 'all', gas),
                    ('ndc.co2', 'all', 'all', co2[kk]), ('ndc.bs', 'all', 'all', bs[kk]), ('ndc.bty', 'all', 'all', bty),
                    ('ndc.bi', 'all', 'all', bi), ('ndc.hk', 'all', 'all', hk), ('ndc.hh', 'all', 'all', hh),
                    ('ndc.hc', 'all', 'all', hc), ('ndc.hv', 'all', 'all', hv), ('ndc.h', 'all', 'all', h),
                    ('ndc.gdp', 'all', 'ref', gdp_ref), ('ndc.gdp', 'all', 'ty', gdp_ty), ('ndc.hi', 'all', 'all', hi),
                    ('ndc.f', 'all', 'u', f['u']), ('ndc.f', 'all', 'c', f['c']), ('ndc.lv', 'all', 'u', lv['u']),
                    ('ndc.lv', 'all', 'c', lv['c']), ('ndc.r', 'all', 'u', rr['u']), ('ndc.r', 'all', 'c', rr['c']),
                    ('ndc.r', 'all', 'a', rr['a']), ('ndc.r', 'all', 'sel', rr['sel']),
                    ('ndc.lvl', 'all', 'u', lvl['u']), ('ndc.lvl', 'all', 'c', lvl['c']),
                    ('ndc.lvl', 'all', 'sel', lvl['sel']), ('ndc.idx', 'all', 'u', lvl['u'] / inc0),
                    ('ndc.idx', 'all', 'c', lvl['c'] / inc0), ('ndc.bau', 'all', 'all', inc_base[i][kk]),
                    ('ndc.red', 'all', 'all', 0.0 if inc_base[i][kk] == 0 else 1 - inc[kk] / inc_base[i][kk]),
                    ('ndc.gap', 'all', 'all', None), ('ndc.over', 'all', 'all', inc[kk] - lvl['sel'])):
                if var == 'ndc.gap':
                    red = rows[('ndc.red', 'all', 'all')][i][kk]
                    v = red / rr['sel'] if rr['sel'] > 0 else 1.0
                if var == 'ndc.over' and np.isnan(v):
                    v = 0.0
                cell = rows.setdefault((var, sector, fuel), [[None] * len(years) for _ in countries])
                cell[i][kk] = v
    for (var, sector, fuel), values in rows.items():
        arr = np.array(values, dtype=object)
        try:
            arr = arr.astype(float)
        except (TypeError, ValueError):
            pass
        R.put(var, arr, sector, fuel)


def _fmt(x):
    """A number as Excel shows it in a text join (2010, not 2010.0)."""
    return str(int(x)) if isinstance(x, float) and x == int(x) else str(x)


def carbon_pricing(state, db, inputs, settings, baseline, t):
    """EQ-A7.5: carbon pricing indicators (Mitigation section 17): revenue per tonne of CO2 by fuel, the share of CO2
    covered by the carbon tax and the ETS, effective carbon price, revenue per tonne."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    co2 = at('co2', 'all', 'all')
    per_t = lambda v: np.where(co2 == 0, 0.0, safe_div(v, co2))
    power = {'coa', 'nga', 'oop'}                        # power fuels with revenue rows rfg
    for f in ('coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'jfu', 'oop'):
        rev = at('rfu', 'all', f) + (at('rfg', 'pow', f) if f in power else 0.0)
        cf = at('co2', 'all', f)
        R.set('tcp', k, np.where(cf == 0, 0.0, safe_div(rev, cf)), 'all', f)
    R.set('tcp', k, per_t(sum(at('rfu', 'all', f) for f in ('coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'jfu', 'oop'))
                          + sum(at('rfg', 'pow', f) for f in power)), 'all', 'all')
    for g in GROUPS:
        R.set('cov.ct', k, per_t(sum(at('covct', s, 'all') for s in SECTORS if SECTOR_GROUP[s] == g)), g, 'all')
    R.set('cov.ct', k, per_t(at('covct', 'pow', 'all')), 'pow', 'all')
    ct = R.set('cov.ct', k, per_t(sum(at('covct', e, 'all') for e in COVERAGE_SECTORS)), 'all', 'all')
    ets = R.set('cov.ets', k, per_t(at('co2.ets', 'all', 'all')), 'all', 'all')
    R.set('cov.all', k, ct + ets, 'all', 'all')
    R.set('cpeff', k, at('cptraj') * ct, 'all', 'all')
    R.set('ecr', k, per_t(at('rnet', 'all', 'all') + at('rnew', 'all', 'all') + at('rsr', 'all', 'all')), 'all', 'all')


# ---- local air pollutants (Mitigation section 15: outputs to the air pollution module)
AP_POLLUTANTS = ['pm2', 'nox', 'so2', 'voc', 'bc', 'oc', 'co']
AP_GWP = ['bc', 'oc', 'nox', 'so2', 'voc', 'co']                  # rows apf (GWP100 of the GAINS region)
AP_GROUPS = {'tra': ['rod', 'ral', 'avi', 'nav'], 'bld': ['res', 'foo', 'srv'],
             'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr']}
SOURCES = ['cpp', 'gpp', 'opp', 'rod', 'gro', 'oth', 'foo']        # coal and gas plants, other power, road, ground level,
APS_POLLUTANTS = ['nox', 'so2', 'bc', 'pom', 'opm', 'voc', 'ch4', 'co', 'pm2', 'oc']   # other, food and agriculture
GROUND = ['res', 'srv', 'cst']
OTHER = ['ral', 'avi', 'nav', 'mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'ftr', 'oen']


def gwp_region(db, iso):
    ca = db.table('countries_attributes')
    v = ca.loc[(ca['code'] == iso) & (ca['variable'] == 'Region Gains code'), 'value']
    return v.iloc[0] if len(v) else ''


def pollutants(state, db, inputs, settings, baseline, t):
    """EQ-A7.6: local air pollutants by subsector and source, their GWP100 CO2 equivalent (Mitigation section 15)."""
    R = year_rows(state, settings)
    k, y = settings.years.index(t), t
    c = xt.constant
    countries = list(settings.countries)
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    ef_share = {'constant': 0.0, 'Variable': 1.0}.get(str(settings.base['EFSel']), 0.5)
    w = R.set('ap.w', k, ef_share * (y - settings.base_year) / (c('EFEndYear') - settings.base_year), 'all', 'all')
    tables = state['_fuel']
    cache = cached(state, 'ap_coef', dict)              # the factors by country, gathered once per baseline
    def fcol(f, s, key):
        if (f, s, key) not in cache:
            cache[(f, s, key)] = np.array([tables[iso][(f, s)][key] for iso in countries])
        return cache[(f, s, key)]
    def tcol(kk, key):
        if (kk, key) not in cache:
            cache[(kk, key)] = np.array([state['_power'][iso]['types'][kk][key] for iso in countries])
        return cache[(kk, key)]
    if 'ef' not in cache:                               # (pollutant, sector, fuel, country) and food (pollutant, fuel)
        for i in (0, 1):
            cache[f'ef{i}'] = np.array([[[fcol(f, s, f'ef{i}_{pol}') for f in FUELS] for s in SECTORS]
                                        for pol in AP_POLLUTANTS])
        cache['share'] = np.array([fcol(f, 'foo', 'food_share') for f in FUELS])
    tef = lambda kk, pol: (tcol(kk, f'ap0_{pol}') * (1 - w) + w * tcol(kk, f'ap1_{pol}')) / c('tPerKt')
    ef = (cache['ef0'] * (1 - w) + w * cache['ef1']) / c('tPerKt')
    ener = np.array([[at('ener', s, f) for f in FUELS] for s in SECTORS])           # (sector, fuel, country)
    food = ener[SECTORS.index('foo')] * cache['share']
    for i, f in enumerate(FUELS):
        R.set('apfd', k, food[i], 'foo', f)
    by_sector = np.einsum('psfc,sfc->psc', ef, ener)
    by_food = np.einsum('pfc,fc->pc', ef[:, SECTORS.index('foo')], food)
    ap = {}
    for p, pol in enumerate(AP_POLLUTANTS):
        for i, s in enumerate(SECTORS):
            ap[(pol, s)] = R.set('ap', k, by_sector[p, i], s, pol)
        ap[(pol, 'pow')] = R.set('ap', k, sum(at('pe', 'pow', kk) * tef(kk, pol) for kk in TYPES), 'pow', pol)
        for g, subs in AP_GROUPS.items():
            R.set('ap', k, sum(ap[(pol, s)] for s in subs), g, pol)
        fod = R.set('ap', k, by_food[p], 'fod', pol)
        R.set('ap', k, ap[(pol, 'foo')] - fod, 'fag', pol)
        if pol in AP_GWP or pol == 'pm2':          # pm2: the last row of section 15
            ap[(pol, 'all')] = R.set('ap', k, sum(ap[(pol, s)] for s in SECTORS + ['pow']), 'all', pol)
    if 'gwp' not in cache:
        reg = [gwp_region(db, iso) for iso in countries]
        efv = db.table('ef_ghg')
        efv = dict(zip(efv['code'], efv['value']))
        cache['gwp'] = {pol: np.array([float(efv.get(f'{r}.mit.gwp100.{pol}', 0) or 0) for r in reg]) for pol in AP_GWP}
    apf = {pol: R.set('apf', k, ap[(pol, 'all')] * cache['gwp'][pol] / c('ktPerMt'), 'all', pol) for pol in AP_GWP}
    apf_all = R.set('apf', k, sum(apf.values()), 'all', 'all')
    R.set('ghg.enrp', k, at('ghg', 'enr', 'all') + apf_all, 'enr', 'all')

    # by source for the air pollution module
    ch4 = lambda subs: sum(at('ch4', s, f) for s in subs for f in FUELS)
    src = {}
    for pol in ('nox', 'so2', 'bc', 'voc', 'co', 'pm2', 'oc'):
        src[('cpp', pol)] = at('pe', 'pow', 'coa') * tef('coa', pol)
        src[('gpp', pol)] = at('pe', 'pow', 'nga') * tef('nga', pol)
        src[('opp', pol)] = ap[(pol, 'pow')] - src[('cpp', pol)] - src[('gpp', pol)]
        src[('rod', pol)] = ap[(pol, 'rod')]
        src[('gro', pol)] = sum(ap[(pol, s)] for s in GROUND)
        src[('oth', pol)] = sum(ap[(pol, s)] for s in OTHER)
        src[('foo', pol)] = ap[(pol, 'foo')]
    src[('cpp', 'ch4')], src[('gpp', 'ch4')] = at('ch4', 'pow', 'coa'), at('ch4', 'pow', 'nga')
    src[('opp', 'ch4')] = at('ch4', 'pow', 'oop') + at('ch4', 'pow', 'bio')
    src[('rod', 'ch4')], src[('gro', 'ch4')] = ch4(['rod']), ch4(GROUND)
    src[('oth', 'ch4')] = (at('ch4.c', 'all', 'all') - at('ch4.c', 'pow', 'all') - ch4(['rod']) - ch4(GROUND)
                           - ch4(['foo']) + at('ch4.sup', 'all', 'all'))
    src[('foo', 'ch4')] = ch4(['foo']) + sum(at('ch4.em', 'all', s) for s in ('liv', 'ric', 'wst'))
    for s in SOURCES:
        src[(s, 'pom')] = src[(s, 'oc')] * c('PomPerOC')
        src[(s, 'opm')] = np.maximum(0, src[(s, 'pm2')] - src[(s, 'bc')] - src[(s, 'pom')])
        for pol in APS_POLLUTANTS:
            R.set('aps', k, src[(s, pol)], s, pol)
    for pol in APS_POLLUTANTS:
        R.set('aps', k, sum(src[(s, pol)] for s in SOURCES), 'all', pol)
    for f in ('coa', 'nga', 'oop', 'bio'):
        R.set('apen', k, at('pe', 'pow', f), 'pow', f)
    for f in FUELS:
        R.set('apen', k, at('ener', 'res', f), 'res', f)
    R.set('apen', k, at('eldem', 'res', 'ecy'), 'res', 'ecy')
    R.set('apco2', k, at('co2', 'all', 'all'))
