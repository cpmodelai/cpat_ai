"""Block 3, power sector (Mitigation section 3).

prepare  the rows that read no quantity of the year loop: the scenario's settings of each generation type (A0:
         capacity factor, efficiency, WACC, lifetime factor, investment permissions, scale-up rates), capital and fuel
         costs, policy costs per kWh, variable cost, levelised variable cost (backward over the years), cost
         breakdown, storage and electrolyser costs, excise of the scenario.
step     one year t (later blocks): demand, dispatch, generation, capacity, investment, prices, revenues.

Generation types k (rows <var>.pow.<k>): coa nga oop nuc wnd sol hyd ore bio. User groups u (res, ind; rows
<var>.<u>.ecy), demand groups d (tra res ind srv; rows <var>.<d>.ecy).
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import Rows, cached, safe_div
from cpat_model.mitigation import ef_data, elasticity_data, policies, power_data, prices_data
from cpat_model.mitigation.policies import yes

TYPES = ['coa', 'nga', 'oop', 'nuc', 'wnd', 'sol', 'hyd', 'ore', 'bio']
USERS = ['res', 'ind']
GROUPS = ['tra', 'res', 'ind', 'srv']
PRICE_FUELS_ALL = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res', 'ecy.ind', 'gso.all',
                   'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all']   # fuel price reform positions (pfpos)
FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'jfu', 'oop', 'bio']      # carbon-tax coverage positions (fpos)
SPOT_POW = 'No'                       # Excel-AI Settings C21 (legacy option; No = centred moving average of prices)
COAL_IC_TARIFF = 'Yes'                # Excel-AI Settings C66 (MTInputs PwCoalICTariff, scenario 1)


def country_data(db, iso, state, settings):
    """The power data steps of one country (power_data, elasticity_data, ef_data; tested in test_data_steps)."""
    c = xt.constant
    base = settings.base
    series = lambda k: dict(zip(state[k]['year'].values, state[k].sel(country=iso).values))
    ps = power_data.power_settings(db, iso, base, c)
    tech = power_data.power_tech(db, iso, base, settings, ps, c)
    paths = power_data.power_paths(db, iso, settings.years, ps, tech, series('macro.gdppc'), c)
    par = power_data.power_params(db, iso, settings, ps, tech, c)
    stored = policies.stored_baseline(policies.settings_stored_path(settings), (iso,), tuple(settings.years))
    raw = float(stored['raw'].sel(country=iso, year=settings.base_year)) if 'raw' in stored else 0.0
    efcalib = ef_data.co2_calibration(db, iso, settings, raw)
    co2 = ef_data.co2_efs(db, iso, c)
    nonco2 = ef_data.nonco2_efs(db, iso, c)
    ecp = state['_ecp'][iso]
    types = power_data.power_types(tech, ps, par, co2, efcalib, ecp, policies.ecp_embedded_year(settings), nonco2,
                                   base, c)
    ela = elasticity_data.elasticities(db, iso, base)
    dd = prices_data.DomesticData(db, iso, str(base['DomPrTax'])[:1] == 'Y')
    users = power_data.user_groups(dd, par, series('macro.cpiidx'), settings.last_hist_price_year)
    return dict(ps=ps, tech=tech, paths=paths, par=par, types=types, ela=ela, users=users, efcalib=efcalib,
                co2=co2, nonco2=nonco2, groups=power_data.demand_groups(ela, par, users),
                subs=power_data.demand_subsectors(db, iso, settings, base),
                system=power_data.system_params(par, types, c), ecp=ecp)


def prepare(state, db, inputs, settings, baseline):
    """EQ-M4.3, EQ-A4.5, EQ-A4.6, EQ-A4.7: the quantity-free rows of section 3."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    t, n, g = R.t, inputs.number, (lambda name: inputs[name])
    c = xt.constant
    data = {iso: cached(state, ('power', iso), lambda: country_data(db, iso, state, settings)) for iso in countries}
    state['_power'] = data
    col = lambda f: np.array([[f(data[iso])] for iso in countries])                  # (country, 1)
    ty = lambda k, key: col(lambda d: d['types'][k][key])
    path = lambda item: np.array([[d['paths'][item][y] for y in years] for d in (data[i] for i in countries)])
    hours = power_data.HOURS

    # A0: the scenario's settings of each type (capacity factor, efficiency, WACC, lifetime factor)
    for k in TYPES:
        low = g('CFOverrideIfBelowWndSol') if ty(k, 'vreb')[0, 0] == 1 else g('CFOverrideIfBelowFosOth')
        cfa, cfs = ty(k, 'cfa'), ty(k, 'cfs')
        R.put('cfu', np.where((cfa > low) & (cfa < g('CFOverrideIfAbove')), cfa, cfs), 'pow', k)
        nua, nus = ty(k, 'nua'), ty(k, 'nus')
        R.put('nuu', np.where(nua < g('MinimumThermalEfficiency'), nus, nua), 'pow', k)
    src = str(g('WACCSource'))
    wsel = 'C' if src[:7] == 'Country' else ('T' if src == 'Tech' else '')
    R.put('wsel', wsel)
    wfx = g('WACCUserGlobal') if src == 'User' else (col(lambda d: d['ps']['PsIncWacc']) if src[:6] == 'Income' else '')
    R.put('wfx', wfx)
    for k in TYPES:
        wac = (ty(k, 'wcty') if wsel == 'C' else ty(k, 'wtec') if wsel == 'T'
               else np.maximum(ty(k, 'wstu') if isinstance(wfx, str) else wfx, g('MinimumWACC')))
        R.put('wac', wac, 'pow', k)
        w = R.of('wac', 'pow', k)
        R.put('dlf', (1 - (1 + w) ** -ty(k, 'life')) / (1 - (1 + w) ** -1), 'pow', k)
    R.put('dlfr', (R.of('dlf', 'pow', 'wnd') + R.of('dlf', 'pow', 'sol')) / 2)
    for k in TYPES:
        R.put('kwh', ty(k, 'pfl') * c('GJperkWh') / R.of('nuu', 'pow', k), 'pow', k)
    for k in TYPES:
        cfu = R.of('cfu', 'pow', k)
        R.put('cap0', np.where(cfu == 0, 0.0, safe_div(ty(k, 'gen0'), cfu)), 'pow', k)
    names = {r['type']: r['mt_name'] for r in xt.table('power_types')}
    cap0_sum = sum(R.of('cap0', 'pow', k) for k in TYPES)
    for k in TYPES:
        R.put('invs', g(f'NewInv{names[k]}'), 'pow', k)
    for k in TYPES:
        inv = g(f'NewInv{names[k]}')
        perm = (np.where(R.of('cap0', 'pow', k) / cap0_sum > c('InvPresentShare'), 'Yes', 'No').astype(object)
                if inv == 'If Present*' else inv)
        R.put('perm', perm, 'pow', k)
    for k in TYPES:
        hyd_first = (ty(k, 'hydf') == 1) & (ty(k, 'shr0') > c('HydInvShare'))
        R.put('start', np.where(hyd_first, float(settings.base_year), float(g(f'NewInv{names[k]}Year'))), 'pow', k)
    rates = {r['category']: r for r in db.table('power_re_scaleup_rates').to_dict('records')}
    cat = str(g('MaxScaleUpRateCategory'))
    scat = float(rates[cat]['value']) if cat in rates else 0.0
    R.put('scat', scat)
    scv = (col(lambda d: d['ps']['PsScCtry']) if cat[:4] == 'Ctry' else
           g('MaxWindSolarScaleup') if cat == 'UserDefined' else scat)
    R.put('scv', scv)
    for k in TYPES:
        R.put('rate', np.where(ty(k, 'nvf') == 1, g('MaxNonVREAsPCOfTotalGen'),
                               np.where(ty(k, 'vreb') == 1, scv, g('MaxNonNucOreBioAsPCOfTotalGen'))), 'pow', k)
    for k in TYPES:
        no_ret = (ty(k, 'hydf') == 1) & (g('HydroDoesntRetire') == 'Yes')
        R.put('rr', np.where(no_ret, 0.0, ty(k, 'rinv')), 'pow', k)
    R.put('erf', 0.0 if n == 1 and g('EarlyRetirementInBaseline') != 'Yes' else g('MaxCostBasedEarlyRetirement'))
    R.put('spot', float(SPOT_POW == 'Yes' or yes(g('UseSpotFuelPricesInEngineerModel'))))
    ctf = power_data.ctf_scenario(g('RenewableCostDeclineRate'))
    R.put('ctf', ctf)
    R.put('stm', g('AllocateSTStorageToVRE') * (c('StMargFactor') * g('TotalHoursStorageFor100pcVRE')))
    R.put('ltu', g('AllocateLTStorageToVRE') * g('LongTermStorageFor100pcVRE'))
    phase = yes(g('PhaseOutCoalAndGasPPAsBaseline') if n == 1 else g('PhaseOutCoalAndGasPPAsPolicy'))
    R.put('ppa', g('PPAProportionCoalGas') * (np.maximum(0, 1 - np.maximum(0, t - g('YearPPACoalGas'))
                                                         / g('YearsToPhaseOutPPAs')) if phase else 1.0))
    add = (g('RenSubsidyAddUSDkwh') * np.maximum(0, 1 - (t - g('RenSubsidyAddStartYear')) / g('RenSubsidyAddPhaseoutYrs'))
           if n > 1 else 0.0)
    rnsp = R.put('rnsp', -(g('RenewableSubsidyBL') + np.where((n > 1) & (t >= g('RenSubsidyAddStartYear')), add, 0.0))
                 * R.of('infl'))
    for k in TYPES:
        R.put('rns', rnsp * np.where(ty(k, 'renf') == 1, 1.0, ty(k, 'hydf') * yes(g('RenewableSubsidyHydro'))),
              'pow', k)
    scn = int(R.of('scn')[0, 0])
    table = xt.table('main_scenarios')
    row = table[scn - 1] if scn else None
    R.put('rbs', float(n > 1 and (yes(g('PowerRebates')) or (row is not None and row['power_rebated'] == 'Yes'))))
    exs = 0.0 if n == 1 or not scn else float(row['electricity_excise'] == 'Yes')
    R.put('exs', exs * col(lambda d: d['system']['gint']) * R.of('cptraj'))
    for k in TYPES:
        R.put('tcf', path(f'tcf|{k}|{ctf}'), 'pow', k)
    for item in ('cbat', 'cint', 'obat', 'elcx', 'eltk', 'elof', 'elov'):
        R.put(item, path(item))
    dlfr = R.of('dlfr')
    R.put('cel', (R.of('elcx') + R.of('eltk') * g('StorageHoursForLTStorage')) / (dlfr * hours)
          + R.of('elof') / hours + R.of('elov'))
    R.put('incp', path('incp'))
    R.put('inc.ela.adj', R.of('incp') if yes(g('IncElAdj')) else 1.0)
    R.put('shock', path('shock'))

    # capital costs, coal implicit cost, fuel and policy costs per kWh, variable cost (EQ-M4.3)
    for k in TYPES:
        R.put('cax', ty(k, 'cax0') * R.of('tcf', 'pow', k), 'pow', k)
    coal_ic = db.table('coal_implicit_price')
    coal_ic = {r['country']: r for r in coal_ic.to_dict('records')}
    aic = str(g('AdditionalCoalIntangibleCost'))
    st_lt = {}
    for v, man, col_ in (('cics', 'ManualCoalIntangibleCostST', 'first_year'),
                         ('cicl', 'ManualCoalIntangibleCostLT', 'year_2030')):
        if aic[:1] == 'N':
            val = 0.0
        elif aic == 'Manual':
            val = g(man)
        else:                                # the coal implicit cost of the country (GoalSeekCoal; 0 if absent)
            val = np.array([[float(coal_ic[i][col_]) if i in coal_ic else 0.0] for i in countries])
        st_lt[v] = R.put(v, val)
    R.put('cic', st_lt['cics'] + (st_lt['cicl'] - st_lt['cics']) * np.minimum(1, (t - settings.base_year)
                                                                            / (c('CoalICYr') - settings.base_year)))
    cic = R.of('cic')
    for k in TYPES:
        pcode = data[countries[0]]['types'][k]['price_code'] or 'coa.pow'
        fu, se = pcode.split('.')
        R.put('fpn', R.of('pbc', se, fu), 'pow', k)
    lag = int(c('PwAvgLag'))
    for k in TYPES:
        fpn = R.of('fpn', 'pow', k)
        avg = np.array([[fpn[i, max(0, j - min(j, lag)):j + 1].mean() for j in range(len(years))]
                        for i in range(len(countries))])
        R.put('fpp', fpn if R.of('spot')[0, 0] == 1 else avg, 'pow', k)
    xct_c = (R.of('xct.c')[0] - 1).astype(int)
    xct_p, xets_p = R.of('xct.p'), R.of('xets.p')
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS]
    for k in TYPES:
        key = lambda d: xkeys[int(d['types'][k]['ecpk']) - 1]
        xct = np.array([(np.zeros(5) if key(data[i]) == 'none|none' else data[i]['ecp'][f'xct|{key(data[i])}'])[xct_c]
                        for i in countries])
        xets = np.array([(np.zeros(5) if key(data[i]) == 'none|none' else data[i]['ecp'][f'xets|{key(data[i])}'])[xct_c]
                         for i in countries])
        kwh = R.of('kwh', 'pow', k)
        R.put('xck', ty(k, 'ef') * kwh * (xct * xct_p + xets * xets_p - ty(k, 'xcp0')), 'pow', k)
    for k in TYPES:
        R.put('vbc', ty(k, 'vfix') + R.of('fpp', 'pow', k) * R.of('kwh', 'pow', k) + R.of('xck', 'pow', k)
              + (k == 'coa') * cic, 'pow', k)
    ctr, etr = R.of('ctr', 'pow', 'all'), R.of('etr', 'pow', 'all')
    for k in TYPES:
        d0 = data[countries[0]]['types'][k]
        fuel = FUELS[int(d0['fpos']) - 1]
        pf = PRICE_FUELS_ALL[int(d0['pfpos']) - 1].split('.')
        kwh = R.of('kwh', 'pow', k)
        R.put('xac', ty(k, 'ef') * kwh * (ctr * R.of('ctcov', 'all', fuel) + etr)
              + R.of('ntxb', pf[1], pf[0]) * kwh / ty(k, 'gj'), 'pow', k)
    shpx = R.of('shpx', 'pow', 'all')
    for k in TYPES:
        R.put('shk', shpx * ty(k, 'ef') * R.of('kwh', 'pow', k), 'pow', k)
    reb = -sum(R.of('shk', 'pow', k) * ty(k, 'shr0') for k in TYPES)
    R.put('reb', np.where(t == settings.base_year, 0.0, reb))
    for k in TYPES:
        R.put('tvc', R.of('vbc', 'pow', k) + R.of('xac', 'pow', k) + R.of('shk', 'pow', k) + R.of('reb'), 'pow', k)
    for k in TYPES:
        R.put('tvcx', R.of('tvc', 'pow', k), 'pow', k)
    # levelised variable cost: discounted average of the variable cost over the remaining years (EQ-A4.5)
    for k in TYPES:
        disc = (1 + R.of('wac', 'pow', k)) ** (settings.base_year - t)
        dsum = np.cumsum(disc[:, ::-1], axis=1)[:, ::-1]
        R.put('dsum', dsum, 'pow', k)
        tvcx = R.of('tvcx', 'pow', k)
        lvc = np.zeros_like(tvcx)
        for j in range(len(years) - 1, -1, -1):
            nxt = lvc[:, j + 1] if j + 1 < len(years) else 0.0
            lvc[:, j] = (disc[:, j] * tvcx[:, j] + (dsum[:, j] - disc[:, j]) * nxt) / dsum[:, j]
        R.put('lvc', lvc, 'pow', k)
    for k in TYPES:
        R.put('fce', R.of('fpp', 'pow', k) * R.of('kwh', 'pow', k), 'pow', k)
    for k in TYPES:
        R.put('cik', ty(k, 'ef') * R.of('kwh', 'pow', k), 'pow', k)
    cik_c, cik_g = R.of('cik', 'pow', 'coa'), R.of('cik', 'pow', 'nga')
    R.put('swd', safe_div(R.of('tvc', 'pow', 'nga') - R.of('tvc', 'pow', 'coa'), cik_c - cik_g))
    R.put('cph', (R.of('cbat') + R.of('cint') / g('StorageToInterfaceRatioSTStorage')) / (dlfr * hours)
          + R.of('obat') / hours)
    # cost breakdown (memo; EQ-A4.6)
    for k in TYPES:
        cfu = R.of('cfu', 'pow', k)
        R.put('pcbcap', R.of('cax', 'pow', k) / (cfu * hours * R.of('dlf', 'pow', k)), 'pow', k)
    for k in TYPES:
        R.put('pcbom', ty(k, 'opfx') / (R.of('cfu', 'pow', k) * hours) + ty(k, 'vop'), 'pow', k)
    for k in TYPES:
        R.put('pcbfu', ty(k, 'ffix') + R.of('fpp', 'pow', k) * R.of('kwh', 'pow', k) + R.of('xck', 'pow', k), 'pow', k)
    for k in TYPES:
        R.put('pcbcp', R.of('xac', 'pow', k), 'pow', k)
    for k in TYPES:
        R.put('pcbrns', R.of('rns', 'pow', k), 'pow', k)
    R.put('pcbct', R.of('cptraj') * (n > 1))
    # excise on electricity of the scenario (manual excise path and fuel price reform; EQ-A4.7)
    man = db.table('mi_excise_reform')
    for u in USERS:
        m = man[man['code'] == f'mit.ntx.ecy.{u}']
        m = dict(zip(m['year'].astype(int), prices_data.to_float(m['value']).fillna(0)))
        entxd = R.put('entxd', np.array([m.get(y, 0.0) for y in years]), u, 'ecy')
        add_exc = entxd * (1.0 if str(g('NomorReal'))[:4] == 'Real' else R.of('defl')) if yes(g('AdditionalExcise')) else 0.0
        R.put('entx', (add_exc + R.of('fpr', u, 'ecy')) if n > 1 else 0.0, u, 'ecy')
    for k in TYPES:
        R.put('pret', path(f'pret|{k}'), 'pow', k)
    for k in TYPES:
        perm = R.of('perm', 'pow', k)
        R.put('permit', ((perm == 'Yes') & (t >= R.of('start', 'pow', k))).astype(float), 'pow', k)
    R.finish()


# ---- the year loop
def step_after_road(state, db, inputs, settings, baseline, t):
    """Power once more in a transport data year after the base year where TrModel = Engineer: road electricity demand
    (trkte) reads this year's industry electricity price, which does not depend on this year's demand, so the second
    run is exact (Excel-AI has no circular reference)."""
    from cpat_model.mitigation import road
    from cpat_model.mitigation.gdp import year_rows
    R = year_rows(state, settings)
    k = settings.years.index(t)
    if t > settings.base_year and road.rerun(state, settings, t) and np.any(R.at('tr.sw', k, 'all', 'all') > 0):
        step(state, db, inputs, settings, baseline, t)


def step(state, db, inputs, settings, baseline, t):
    """EQ-M4.1, EQ-M4.2, EQ-M4.4 to EQ-M4.7, EQ-A4.8, EQ-A4.9: power demand, dispatch, generation, capacity,
    investment, end-user prices, subsidies and revenues of year t."""
    from cpat_model.mitigation.gdp import year_rows
    R = year_rows(state, settings)
    k, y = settings.years.index(t), t
    g, n = (lambda name: inputs[name]), inputs.number
    c = xt.constant
    countries = list(settings.countries)
    data = state['_power']
    col = lambda f: np.array([f(data[iso]) for iso in countries])                     # (country,)
    ty = lambda kk, key: col(lambda d: d['types'][kk][key])
    at = lambda var, sector=None, fuel=None, kk=k: R.at(var, kk, sector, fuel)
    hours, pj = power_data.HOURS, power_data.PJ_PER_KTOE
    last = settings.last_hist_price_year
    k_last = settings.years.index(last)
    min_cost = g('MinPostSubsidyPowerPrice')
    pass_on = g('PowerSectorPriceChangePassOn')

    # demand (EQ-M4.1)
    for d in GROUPS:
        gr = lambda key: col(lambda x: x['groups'][d][key])
        if k == 0:
            pdem = R.set('pdem', k, gr('p2021'), d, 'ecy')
        else:
            pdem = R.set('pdem', k, gr('wres') * at('rp', 'res', 'ecy', k - 1)
                         + (1 - gr('wres')) * at('rp', 'ind', 'ecy', k - 1), d, 'ecy')
        aeef = R.set('aeef', k, (1 / (1 + gr('alpha') + g('AdditionalEfficiencyPower'))) ** (1 + gr('eu')), d, 'ecy')
        if k == 0:
            R.set('mult', k, 1.0, d, 'ecy')
        else:
            R.set('mult', k, aeef * (1 + at('gdp.pos.pct')) ** (gr('ey') * at('inc.ela.adj'))
                  * (pdem / at('pdem', d, 'ecy', k - 1)) ** gr('eps')
                  * (1 + at('shock') * settings.global_settings.get('ApplyDemandShock', 1)
                     * g('EngineerModelProportionOfCovidFactor')), d, 'ecy')
    subs = data[countries[0]]['subs']
    for s in power_data.DEMAND_SUBSECTORS:
        if k == 0:
            R.set('dem', k, col(lambda x: x['subs'][s]['d0']), s, 'ecy')
        else:
            road = subs[s]['tr'] * at('tr.sw', 'all', 'all') > 0         # road under TrModel = Engineer (road.step ran)
            R.set('dem', k, np.where(road, at('trkte', 'rod', 'ecy'),
                                     at('dem', s, 'ecy', k - 1) * at('mult', subs[s]['group'], 'ecy')), s, 'ecy')
    for d in GROUPS:
        R.set('demg', k, sum(at('dem', s, 'ecy') for s in power_data.DEMAND_SUBSECTORS if subs[s]['group'] == d),
              d, 'ecy')
    demtot = R.set('demtot', k, sum(at('dem', s, 'ecy') for s in power_data.DEMAND_SUBSECTORS))
    if k == 0:
        req = R.set('req', k, sum(ty(kk, 'gen0') for kk in TYPES))
    else:
        req = R.set('req', k, demtot * col(lambda x: x['system']['req_factor']))

    # capacity and dispatch (EQ-M4.4)
    for kk in TYPES:
        if k == 0:
            R.set('cap', k, at('cap0', 'pow', kk), 'pow', kk)
        else:
            R.set('cap', k, at('cap', 'pow', kk, k - 1) - at('ret', 'pow', kk, k - 1) + at('nim', 'pow', kk, k - 1),
                  'pow', kk)
    R.set('captot', k, sum(at('cap', 'pow', kk) for kk in TYPES))
    effcap = {kk: R.set('effcap', k, at('cap', 'pow', kk) * at('cfu', 'pow', kk), 'pow', kk) for kk in TYPES}
    cg = {kk: ty(kk, 'cg') for kk in TYPES}
    reqcg = R.set('reqcg', k, np.maximum(req - sum(effcap[kk] * (1 - cg[kk]) for kk in TYPES), 0))
    tvc = {kk: at('tvc', 'pow', kk) for kk in TYPES}
    cg_min = np.min([np.where(cg[kk] == 1, tvc[kk], np.inf) for kk in TYPES], axis=0)
    vcmin = R.set('vcmin', k, np.maximum(np.where(np.isinf(cg_min), 0.0, cg_min), min_cost))
    gmx = {kk: R.set('gmx', k, at('cap', 'pow', kk) * (ty(kk, 'eflag') * g('MaximumCoalCF')
                                                       + ty(kk, 'gasf') * g('MaximumGasCF')), 'pow', kk) for kk in TYPES}
    gmx_sum = sum(gmx.values())
    gmin = {kk: R.set('gmin', k, cg[kk] * np.minimum(np.maximum(reqcg - (gmx_sum - gmx[kk]), 0), gmx[kk]), 'pow', kk)
            for kk in TYPES}
    rem = R.set('rem', k, np.maximum(reqcg - sum(gmin.values()), 0))
    lgd = {kk: R.set('lgd', k, cg[kk] * np.exp(-g('kDispatch') * np.maximum(tvc[kk], min_cost) / vcmin), 'pow', kk)
           for kk in TYPES}
    lgd_sum = sum(lgd.values())
    glg = {kk: R.set('glg', k, np.where(cg[kk] == 1, np.minimum(gmx[kk], gmin[kk] + rem * safe_div(lgd[kk], lgd_sum)),
                                        effcap[kk]), 'pow', kk) for kk in TYPES}
    cg_cap = sum(effcap[kk] * cg[kk] for kk in TYPES)
    ppr = R.set('ppr', k, np.where(cg_cap == 0, 1.0, safe_div(reqcg, cg_cap)))
    gen = {}
    for kk in TYPES:
        gen[kk] = R.set('gen_mwy', k, ty(kk, 'gen0') if k == 0 else
                        glg[kk] + cg[kk] * at('ppa') * (effcap[kk] * ppr - glg[kk]), 'pow', kk)
    gtot = R.set('gtot', k, sum(gen.values()))
    R.set('dgen', k, 0.0 if k == 0 else np.maximum(0, gtot - at('gtot', kk=k - 1)))
    shr = {kk: R.set('shr', k, np.where(gtot == 0, 0.0, safe_div(gen[kk], gtot)), 'pow', kk) for kk in TYPES}
    pe = {}
    for kk in TYPES:
        nuu = at('nuu', 'pow', kk)
        pe[kk] = R.set('pe', k, np.where(nuu == 0, 0.0, safe_div(gen[kk] * ty(kk, 'pefx'), nuu)), 'pow', kk)
    for kk in TYPES:
        R.set('co2', k, pe[kk] * ty(kk, 'co2f'), 'pow', kk)
    vre = R.set('vre', k, sum(shr[kk] * ty(kk, 'vre_share') for kk in TYPES) * c('pw.c|vre'))
    start = g('StartingPointWhenLTStorageIsNeeded')
    msc = R.set('msc', k, at('stm') * vre * at('cph') + 2 * np.maximum(0, vre - start) / (1 - start) ** 2
                * at('cel') * at('ltu'))

    # costs of the year (EQ-M4.3)
    for kk in TYPES:
        cax = at('cax', 'pow', kk)
        if k == 0:
            caxav = R.set('caxav', k, cax, 'pow', kk)
            stoav = R.set('stoav', k, ty(kk, 'vre') * msc, 'pow', kk)
        else:
            phi = at('phi', 'pow', kk, k - 1)
            caxav = R.set('caxav', k, at('caxav', 'pow', kk, k - 1) * (1 - phi) + at('cax', 'pow', kk, k - 1) * phi,
                          'pow', kk)
            stoav = R.set('stoav', k, at('stoav', 'pow', kk, k - 1) * (1 - phi) + ty(kk, 'vre') * msc * phi, 'pow', kk)
        cfu, wac, dlf = at('cfu', 'pow', kk), at('wac', 'pow', kk), at('dlf', 'pow', kk)
        R.set('fix', k, (caxav * (ty(kk, 'rinv') + wac * c('CapAvgShr')) + ty(kk, 'afx')) / (cfu * hours) + stoav,
              'pow', kk)
        R.set('lfx', k, (cax + ty(kk, 'dtx')) / (cfu * hours * dlf) + ty(kk, 'opfx') / (cfu * hours)
              + at('rns', 'pow', kk) + ty(kk, 'vre') * msc, 'pow', kk)
    cic = at('cic')
    for kk in TYPES:
        R.set('gnc', k, at('fix', 'pow', kk) + at('vbc', 'pow', kk)
              - ((kk == 'coa') * cic if COAL_IC_TARIFF == 'No' else 0.0), 'pow', kk)
    gncav = R.set('gncav', k, sum(shr[kk] * at('gnc', 'pow', kk) for kk in TYPES) * c('pw.c|gncav'))
    ccpav = R.set('ccpav', k, sum(shr[kk] * at('xac', 'pow', kk) for kk in TYPES)
                  * col(lambda x: x['par']['gen_per_cons']))
    tic = {kk: R.set('tic', k, np.maximum(at('lfx', 'pow', kk) + at('lvc', 'pow', kk), min_cost), 'pow', kk)
           for kk in TYPES}
    cur = {kk: R.set('cur', k, np.maximum(at('lfx', 'pow', kk) + tvc[kk], min_cost), 'pow', kk) for kk in TYPES}
    R.set('swi', k, safe_div(tic['nga'] - tic['coa'], at('cik', 'pow', 'coa') - at('cik', 'pow', 'nga')))
    for kk in TYPES:
        cfu, dlf = at('cfu', 'pow', kk), at('dlf', 'pow', kk)
        sys_ = R.set('sys', k, ty(kk, 'dtx') / (cfu * hours * dlf) + ty(kk, 'vre') * msc + (kk == 'coa') * cic,
                     'pow', kk)
        R.set('pcbchk', k, at('pcbcap', 'pow', kk) + at('pcbom', 'pow', kk) + at('pcbfu', 'pow', kk) + sys_
              + at('pcbcp', 'pow', kk) + at('pcbrns', 'pow', kk) - cur[kk], 'pow', kk)

    # end-user prices and subsidies (EQ-M4.7, EQ-A4.8)
    user = lambda u, key: col(lambda x: x['users'][u][key])
    cons = {u: R.set('cons', k, (user(u, 'wtot') * demtot + user(u, 'wres') * at('dem', 'res', 'ecy'))
                     * col(lambda x: x['par']['ktoe_gwh']), u, 'ecy') for u in USERS}
    cons_sum = sum(cons.values())
    for u in USERS:
        R.set('sc', k, (gncav if k == 0 else at('gncav', kk=k - 1)) + user(u, 'tmc'), u, 'ecy')
    rbs, exs = at('rbs'), at('exs')
    for u in USERS:
        entx = at('entx', u, 'ecy')
        if k == 0:
            pex = exs
        else:
            pex = exs + (pass_on * (entx - at('entx', u, 'ecy', k_last)) if y > last else 0.0)
        R.set('pex', k, pex, u, 'ecy')
        rpnv = R.set('rpnv', k, user(u, f'rp{y}') / (1 + user(u, 'vr')) if y <= last else at('rpnv', u, 'ecy', k - 1),
                     u, 'ecy')
        sc = at('sc', u, 'ecy')
        txg = R.set('txg', k, rpnv - sc - entx, u, 'ecy')
        if y <= last:
            tx = user(u, f'tx{y}')
            txe = np.where(np.isnan(tx), txg * (g('SupplyCostDeltaSubsidy') == 'Yes'), tx)
        else:
            txe = at('txe', u, 'ecy', k - 1)
        R.set('txe', k, txe, u, 'ecy')
        R.set('scl', k, sc if y <= last else np.minimum(sc, at('scl', u, 'ecy', k_last)), u, 'ecy')
        R.set('psegap', k, np.maximum(0, sc - (rpnv - txe)) * cons[u], u, 'ecy')
    psegs = R.set('psegs', k, sum(at('psegap', u, 'ecy') for u in USERS))
    pros = at('pros', 'all', 'ecy')
    psf = at('psf', 'all', 'ecy')
    for u in USERS:
        if y <= last:
            alt = np.where(cons_sum != 0, safe_div(cons[u], cons_sum), 1 - user(u, 'wtot'))
            sh = np.where(psegs != 0, safe_div(at('psegap', u, 'ecy'), psegs), alt)
        else:
            sh = at('psesh', u, 'ecy', k - 1)
        R.set('psesh', k, sh, u, 'ecy')
        if y <= last:
            pseu = np.where(cons[u] != 0, np.maximum(c('PsElFloor'), safe_div(-pros * sh, cons[u])), 0.0)
        else:
            pseu = at('pseu', u, 'ecy', k_last) * psf
        R.set('pseu', k, pseu, u, 'ecy')
    if y <= last:
        R.set('pser', k, -pros - (cons['res'] * at('pseu', 'res', 'ecy') + cons['ind'] * at('pseu', 'ind', 'ecy')))
    else:
        R.set('pser', k, at('pser', kk=k_last) * psf)
    include = g('PowerSubsidyExemptInclude') == 'Include'
    for u in USERS:
        txe = at('txe', u, 'ecy')
        R.set('csd', k, np.where((y > last) & (txe < 0) & include, txe * (at('pof', 'cs', 'all') - 1), 0.0), u, 'ecy')
        if y <= last:
            ores = at('txg', u, 'ecy') - txe - at('pseu', u, 'ecy')
        else:
            prev = at('ores', u, 'ecy', k - 1)
            ores = np.where(prev < 0, prev * safe_div(at('scl', u, 'ecy'), at('scl', u, 'ecy', k - 1)), prev)
        R.set('ores', k, ores, u, 'ecy')
        R.set('spe', k, at('sc', u, 'ecy') + ores + ccpav * pass_on * (1 - rbs) + at('pex', u, 'ecy'), u, 'ecy')
    for u in USERS:
        vr = user(u, 'vr')
        parts = lambda kk: (at('sc', u, 'ecy', kk) + at('pseu', u, 'ecy', kk) + at('csd', u, 'ecy', kk)
                            + at('ores', u, 'ecy', kk))
        if y <= last:
            rppre = R.set('rppre', k, user(u, f'rp{y}'), u, 'ecy')
        else:
            rppre = R.set('rppre', k, at('rppre', u, 'ecy', k - 1) + pass_on * (parts(k) - parts(k - 1)) * (1 + vr),
                          u, 'ecy')
        pex = at('pex', u, 'ecy')
        R.set('rp', k, np.maximum(rppre + (ccpav * pass_on * (1 - rbs) + pex) * (1 + vr), min_cost), u, 'ecy')
        R.set('sgap', k, rppre / (1 + vr) - at('sc', u, 'ecy'), u, 'ecy')
        R.set('rcarb', k, ccpav * c('pw.c|rcarb') * cons[u], u, 'ecy')
        R.set('rvat', k, rppre * user(u, 'vshare') * cons[u], u, 'ecy')
        R.set('rnvat', k, (ccpav * pass_on * (1 - rbs) + pex) * vr * cons[u], u, 'ecy')
        R.set('rreb', k, -rbs * ccpav * pass_on * cons[u], u, 'ecy')
        R.set('rpex', k, pex * cons[u], u, 'ecy')
        R.set('rgap', k, at('sgap', u, 'ecy') * c('pw.c|rgap') * cons[u], u, 'ecy')
    rexs = R.set('rexs', k, exs * cons_sum)
    R.set('rexm', k, sum(at('rpex', u, 'ecy') for u in USERS) - rexs)

    # retirement and investment (EQ-M4.5, EQ-M4.6, EQ-A4.9)
    early_max = col(lambda x: x['par']['early_max'])
    permit = {kk: at('permit', 'pow', kk) for kk in TYPES}
    eff_sum = sum(effcap.values())
    maxinv = {kk: R.set('maxinv', k, at('rate', 'pow', kk) * eff_sum * permit[kk], 'pow', kk) for kk in TYPES}
    if k == 0:
        egrow = R.set('egrow', k, np.maximum(0, maxinv['wnd'] + maxinv['sol']))
    else:
        rec_prev = sum(at('rec', 'pow', kk, k - 1) for kk in TYPES) - at('rec', 'pow', 'coa', k - 1)
        egrow = R.set('egrow', k, np.maximum(0, maxinv['wnd'] + maxinv['sol'] - at('dgen', kk=k - 1) - rec_prev))
    ecmin = R.set('ecmin', k, np.minimum(np.minimum(tvc['coa'], tic['wnd']), tic['sol']))
    kinv = g('kInvestment')
    ecshr = R.set('ecshr', k, 1 / (1 + np.exp(-kinv * (tic['wnd'] - tvc['coa']) / ecmin)
                                   + np.exp(-kinv * (tic['sol'] - tvc['coa']) / ecmin)))
    early = R.set('early', k, np.maximum(0, np.minimum(effcap['coa'] * early_max, egrow) * (1 - ecshr))
                  / at('cfu', 'pow', 'coa') * at('erf') * (1 - at('ppa')))
    for kk in TYPES:
        cap = at('cap', 'pow', kk)
        base_ret = np.where(ty(kk, 'puse') == 1, at('pret', 'pow', kk), cap * at('rr', 'pow', kk))
        ret = R.set('ret', k, np.minimum(base_ret + ty(kk, 'eflag') * early, cap), 'pow', kk)
        R.set('rec', k, ret * at('cfu', 'pow', kk), 'pow', kk)
    kafter = R.set('kafter', k, eff_sum - sum(at('rec', 'pow', kk) for kk in TYPES))
    growth = 1.0 if k == 0 else np.where(at('req', kk=k - 1) != 0, safe_div(req, at('req', kk=k - 1)), 1.0)
    need = R.set('need', k, np.maximum(req * growth - kafter, 0))
    mani = {}
    for kk in TYPES:
        R.set('mancap', k, 0.0, 'pow', kk)            # manual capacity (Manual inputs; empty in the data)
        mani[kk] = R.set('mani', k, 0.0, 'pow', kk)
    needm = R.set('needm', k, np.maximum(need - sum(mani.values()), 0))
    perm_min = np.min([np.where(permit[kk] == 1, tic[kk], np.inf) for kk in TYPES], axis=0)
    cmin = R.set('cmin', k, np.maximum(np.where(np.isinf(perm_min), 0.0, perm_min), min_cost))
    lgi = {kk: R.set('lgi', k, permit[kk] * np.exp(-kinv * tic[kk] / cmin), 'pow', kk) for kk in TYPES}
    lgi_sum = sum(lgi.values())
    pni = {kk: R.set('pni', k, np.where(lgi_sum == 0, 0.0, safe_div(lgi[kk], lgi_sum)), 'pow', kk) for kk in TYPES}
    first = {kk: R.set('first', k, np.minimum(maxinv[kk], needm * pni[kk]), 'pow', kk) for kk in TYPES}
    deficit = R.set('deficit', k, np.maximum(needm - sum(first.values()), 0))
    space = {kk: R.set('space', k, (maxinv[kk] - first[kk]) * permit[kk], 'pow', kk) for kk in TYPES}
    tb = {kk: ty(kk, 'tb') for kk in TYPES}
    second = {}
    for kk in TYPES:
        cheaper = sum(((tic[j] + tb[j]) < (tic[kk] + tb[kk])) * space[j] for j in TYPES)
        second[kk] = R.set('second', k, permit[kk] * np.maximum(0, np.minimum(space[kk], deficit - cheaper)), 'pow', kk)
    dgas = R.set('dgas', k, deficit - sum(second.values()) if settings.base['PwDeficitGas'] == 'Yes' else 0.0)
    for kk in TYPES:
        nei = R.set('nei', k, first[kk] + (second[kk] + ty(kk, 'gasf') * dgas + mani[kk]), 'pow', kk)
        cfu = at('cfu', 'pow', kk)
        R.set('nim', k, np.where(cfu == 0, 0.0, safe_div(nei, cfu)), 'pow', kk)
    R.set('nimtot', k, sum(at('nim', 'pow', kk) for kk in TYPES))
    for kk in TYPES:
        R.set('nid', k, at('nim', 'pow', kk) * at('cax', 'pow', kk) * c('kWperMW') / c('USDperM'), 'pow', kk)
    R.set('usdtot', k, sum(at('nid', 'pow', kk) for kk in TYPES))
    for kk in TYPES:
        cap, nim, ret = at('cap', 'pow', kk), at('nim', 'pow', kk), at('ret', 'pow', kk)
        den = cap + nim - ret
        R.set('phi', k, np.where(den == 0, 0.0, safe_div(nim, den)), 'pow', kk)

    # revenues of the power sector (EQ-A6.1)
    xct_k = int(R.at('xct.c', k)[0]) - 1
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS]
    for kk in TYPES:
        pcode = (data[countries[0]]['types'][kk]['price_code'] or 'coa.pow').split('.')
        fflag = ty(kk, 'fflag')
        R.set('prtx', k, fflag * pe[kk] * pj * (at('etx', pcode[1], pcode[0]) + at('vat', pcode[1], pcode[0])),
              'pow', kk)
        R.set('prsub', k, fflag * pe[kk] * pj * at('esub', pcode[1], pcode[0]), 'pow', kk)
        R.set('prxc', k, at('xck', 'pow', kk) * c('MWyMkWh') * gen[kk], 'pow', kk)
        co2 = at('co2', 'pow', kk)
        R.set('prnew', k, gen[kk] * c('MWyMkWh') * at('xac', 'pow', kk)
              - co2 * at('etr', 'pow', 'all') * (1 - at('ets.rf')), 'pow', kk)
        key = [xkeys[int(data[i]['types'][kk]['ecpk']) - 1] for i in countries]
        xct = np.array([0.0 if q == 'none|none' else data[i]['ecp'][f'xct|{q}'][xct_k] for i, q in zip(countries, key)])
        xets = np.array([0.0 if q == 'none|none' else data[i]['ecp'][f'xets|{q}'][xct_k] for i, q in zip(countries, key)])
        R.set('prxl', k, co2 * (xct * at('xct.p') + xets * at('xets.p')), 'pow', kk)
        R.set('prrns', k, at('rns', 'pow', kk) * c('MWyMkWh') * gen[kk], 'pow', kk)
    R.set('pet', k, sum(pe[kk] * ty(kk, 'fflag') for kk in TYPES), 'pow', 'all')
