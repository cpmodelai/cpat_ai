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
from cpat_model.core.rows import Rows, safe_div
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
    data = {iso: country_data(db, iso, state, settings) for iso in countries}
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
