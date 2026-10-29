"""Data steps of block 3 (power): what Excel-AI computes on its Inputs sheet before Mitigation section 3 reads it (EQ-A4.1 to EQ-A4.4).

    power_settings  the scenario-1 power settings and derived values (Excel-AI Inputs_pset, names Ps...)
    power_tech      generation types of the country: costs, lifetime, efficiency, capacity factor, WACC, capacity
                    (Inputs_ptech; legacy Mitigation rows 2954-4130)
EQ-A4.1. Settings are read from the baseline column (Excel-AI SDBase), as Excel-AI does.
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.data.database import to_float

PS_SETTINGS = {  # Excel-AI defined name: MTInputs NameOfParameter
    'PsMinTE': 'MinimumThermalEfficiency', 'PsHydNoRet': 'HydroDoesntRetire', 'PsScNonVRE': 'MaxNonVREAsPCOfTotalGen',
    'PsScNonNuc': 'MaxNonNucOreBioAsPCOfTotalGen', 'PsScCat': 'MaxScaleUpRateCategory', 'PsScUser': 'MaxWindSolarScaleup',
    'PsWaccSrc': 'WACCSource', 'PsWaccUser': 'WACCUserGlobal', 'PsWaccMin': 'MinimumWACC',
    'PsReDecline': 'RenewableCostDeclineRate', 'PsLTHours': 'StorageHoursForLTStorage', 'PsIncElAdj': 'IncElAdj',
    'PsPass': 'PowerSectorPriceChangePassOn', 'PsSTAlloc': 'AllocateSTStorageToVRE',
    'PsSTHours': 'TotalHoursStorageFor100pcVRE', 'PsSTRatio': 'StorageToInterfaceRatioSTStorage',
    'PsLTAlloc': 'AllocateLTStorageToVRE', 'PsLTStart': 'StartingPointWhenLTStorageIsNeeded',
    'PsAddEff': 'AdditionalEfficiencyPower', 'PsMaxCoalCF': 'MaximumCoalCF', 'PsKDisp': 'kDispatch',
    'PsKInv': 'kInvestment', 'PsMinCost': 'MinPostSubsidyPowerPrice', 'PsEarlyMax': 'MaxCostBasedEarlyRetirement',
    'PsEarlyBL': 'EarlyRetirementInBaseline', 'PsCFMinVRE': 'CFOverrideIfBelowWndSol',
    'PsCFMinOth': 'CFOverrideIfBelowFosOth', 'PsCFMax': 'CFOverrideIfAbove'}
MPP = {'cf': 'CapacityFactor', 'cax': 'CapEx.USD_kW', 'eff': 'Efficiency.NCV', 'opfx': 'OpexFixed.USD_kW_y',
       'vop': 'OpexVariable.USD_kWh', 'wacc': 'WACC', 'life': 'TotalLifetime'}   # columns of the legacy Power table
EFF_ONE = ('wnd', 'sol', 'hyd', 'ore')                  # efficiency of the studies typed 1 (legacy A4 P)
HOURS = 8760
PJ_PER_KTOE = 0.041868                   # Excel-AI Settings C13 (ktoe x PJ/ktoe x $/GJ = USD million)


def ctf_scenario(decline):
    """The capex time-factor scenario of RenewableCostDeclineRate: low, med, hgh, vhg."""
    d = str(decline)
    return 'hgh' if d == 'High' else ('vhg' if d[:1].upper() == 'V' else d[:3].lower())


def income_group(db, iso):
    df = db.table('countries_attributes')
    v = df.loc[(df['code'] == iso) & (df['variable'] == 'Income code'), 'value']
    return v.iloc[0] if len(v) else ''


def power_settings(db, iso, base, c):
    """Excel-AI Inputs_pset: the settings (baseline column) and the derived values of the country."""
    ps = {k: base[v] for k, v in PS_SETTINGS.items()}
    ps['PsCtfScen'] = ctf_scenario(ps['PsReDecline'])
    inc = income_group(db, iso)
    rating = db.table('coc_rating')
    rating = rating.loc[(rating['code'] == iso) & (rating['variable'] == 'S&P'), 'value']
    has_data = len(rating) > 0 and rating.iloc[0] != 'Not Found'
    wacc = db.table('coc_real_wacc')
    wacc = wacc.loc[(wacc['code'] == iso) & (wacc['year'] == '2022'), 'value']
    ps['PsCtryWacc'] = float(wacc.iloc[0]) if has_data and len(wacc) else c('WaccDefault')
    adj = db.table('coc_tech_adjustment')
    ps['_adj'] = {(t, g): float(v) for t, g, v in zip(adj['technology'], adj['income_group'], adj['value'])}
    ps['PsCoalAdj'] = ps['_adj'][('coa', inc)]
    wi = db.table('power_wacc_by_income')
    ps['PsIncWacc'] = float(wi.loc[wi['income_level'] == inc, 'value'].iloc[0])
    sc = db.table('power_re_max_scaleup')
    sc = sc.loc[sc['country'] == iso, 'value']
    ps['PsScCtry'] = float(sc.iloc[0]) if len(sc) else np.nan
    rates = db.table('power_re_scaleup_rates')
    rates = dict(zip(rates['category'], to_float(rates['value'])))
    ps['PsScCatRate'] = rates.get(ps['PsScCat'], 0.0)
    cat = str(ps['PsScCat'])
    ps['PsScVRE'] = ps['PsScCtry'] if cat[:4] == 'Ctry' else (ps['PsScUser'] if cat == 'UserDefined' else ps['PsScCatRate'])
    ps['_income'] = inc
    return ps


def balances(db, iso, year):
    """{flow: {fuel: value}} of the country's energy balance in the year (Excel-AI Balances: the base year)."""
    df = db.table('energy_balances')
    df = df[(df['country'] == iso) & (df['year'] == str(year))]
    out = {}
    for fl, fu, v in zip(df['flow'], df['fuel'], to_float(df['value'])):
        out.setdefault(fl, {})[fu] = 0.0 if np.isnan(v) else float(v)
    return out


def _mpp(db):
    world, country, dtc = {}, {}, {}
    for table, store in (('power_mpp_world', world), ('power_mpp_country', country)):
        df = db.table(table)
        for code, var, v in zip(df['code'], df['variable'], to_float(df['value'])):
            var = 'WACC' if var.startswith('WACC') else var
            store.setdefault(code, {})[var] = 0.0 if np.isnan(v) else float(v)
    df = db.table('power_decom_transmission')
    for code, var, v in zip(df['code'], df['variable'], to_float(df['value'])):
        dtc.setdefault(code, {})[var] = float(v)
    return world, country, dtc


def power_tech(db, iso, base, settings, ps, c):
    """EQ-A4.1. {type: {column: value}}: the generation types of the country (Excel-AI Inputs_ptech)."""
    world, country, dtc = _mpp(db)
    bal = balances(db, iso, settings.base_year)
    ic = db.table('power_installed_capacity')
    ic = ic[(ic['country'] == iso) & (ic['year'] == str(settings.base_year))]
    ic = dict(zip(ic['technology'], to_float(ic['value'])))
    flag = db.table('power_coal_retirement_avg_flag')
    flag = flag.loc[flag['country'] == iso, 'value']
    types = xt.table('power_types')
    out = {}
    for r in types:
        f, leg = r['type'], r['legacy']
        w = world.get(f'wld.mpp.{leg}', {})
        cty = country.get(f'{iso.lower()}.mpp.{leg}', w)

        def pick(var):                      # the country's value where it is > 0, else the world's (rule C)
            v = cty.get(MPP[var], 0.0)
            return v if v > 0 else w.get(MPP[var], 0.0)
        p = {'cax0': pick('cax'), 'life': pick('life'), 'opfx': pick('opfx'), 'vop': pick('vop'),
             'wacc_studies': pick('wacc'), 'cf_studies': pick('cf'),
             'eff_studies': 1.0 if f in EFF_ONE else pick('eff')}
        fuels = r['balances_fuels'].split()
        p['out'] = sum(bal.get('eloutput', {}).get(x, 0.0) for x in fuels)
        p['inp'] = -sum(bal.get('power', {}).get(x, 0.0) for x in fuels)
        act = p['out'] / (p['inp'] * c('KtoeGWh')) if p['inp'] != 0 else np.nan
        p['eff'] = p['eff_studies'] if np.isnan(act) or act < ps['PsMinTE'] else act
        p['ic'] = ic.get(leg, 0.0) if not np.isnan(ic.get(leg, np.nan)) else 0.0
        p['gen0'] = p['out'] * c('Thousand') / HOURS
        p['cf_actual'] = p['gen0'] / p['ic'] if p['ic'] else 0.0
        p['cf_min'] = ps['PsCFMinVRE'] if f in ('wnd', 'sol') else ps['PsCFMinOth']
        p['cf'] = p['cf_actual'] if p['cf_min'] < p['cf_actual'] < ps['PsCFMax'] else p['cf_studies']
        p['wacc_adj'] = ps['_adj'][(leg, ps['_income'])]
        src = str(ps['PsWaccSrc'])
        p['wacc_other'] = max(ps['PsWaccUser'] if src == 'User' else (ps['PsIncWacc'] if src[:6] == 'Income'
                                                                     else p['wacc_studies']), ps['PsWaccMin'])
        p['wacc'] = (ps['PsCtryWacc'] + ps['PsCoalAdj'] if src[:7] == 'Country' else
                     ps['PsCtryWacc'] + p['wacc_adj'] if src == 'Tech' else p['wacc_other'])
        d = dtc.get(f'wld.dtc.{leg}', {})
        p['dtc'] = d.get('Decommissioning costs', 0.0) * p['cax0']
        p['tcx'] = d.get('Transmission costs', 0.0) * p['cax0']
        p['opf'] = p['opfx'] / (HOURS * p['cf'])
        p['ffix'] = c('UraniumFuel') if f == 'nuc' else 0.0
        p['rns'] = 0.0
        p['cap0'] = p['gen0'] / p['cf']
        p['rr'] = 0.0 if f == 'hyd' and ps['PsHydNoRet'] == 'Yes' else 1 / p['life']
        p['newinv'], p['newinv_year'] = base[f'NewInv{r["mt_name"]}'], base[f'NewInv{r["mt_name"]}Year']
        p['dlf'] = (1 - (1 / (1 + p['wacc'])) ** p['life']) / (1 - 1 / (1 + p['wacc']))
        p['scaleup'] = (ps['PsScNonVRE'] if f in ('coa', 'nga', 'hyd') else ps['PsScVRE'] if f in ('wnd', 'sol')
                        else ps['PsScNonNuc'])
        p['planned'] = (flag.iloc[0] if len(flag) else 'No') if f == 'coa' else 'No'
        for k in ('price_code', 'dispatch'):
            p[k] = r[k]
        p['vre'], p['vre_share'] = float(r['vre']), float(r['vre_share'])
        out[f] = p
    cap_sum = sum(p['cap0'] for p in out.values())
    gen_sum = sum(p['gen0'] for p in out.values())
    for f, p in out.items():
        p['permitted'] = (('Yes' if p['cap0'] / cap_sum > c('InvPresentShare') else 'No') if p['newinv'] == 'If Present*'
                          else p['newinv'])
        p['start'] = (settings.base_year if f == 'hyd' and p['gen0'] / gen_sum > c('HydInvShare')
                      else p['newinv_year'])
    ps['PsDlfRen'] = (out['wnd']['dlf'] + out['sol']['dlf']) / 2
    return out


# ---- year paths (Excel-AI Inputs_ppath)
CTF_SCENARIOS = ('low', 'med', 'hgh', 'vhg')
RENEWABLES = ('wnd', 'sol', 'hyd', 'ore', 'bio')       # capex time factors of the decline scenario
STORAGE = {'cbat': ('Battery', 'Capex'), 'obat': ('Battery', 'OpexFix'), 'cint': ('Batteryinterface', 'Capex'),
           'elcx': ('WaterElectrolysis', 'Capex'), 'elof': ('WaterElectrolysis', 'OpexFix'),
           'elov': ('WaterElectrolysis', 'VariableOpex.USD_kWh'), 'eltk': ('StorageTank', 'Capex')}


def power_paths(db, iso, years, ps, tech, gdppc, c):
    """EQ-A4.2. {item: {year: value}}: capex time factors, storage costs, income factor, demand shock, planned
    retirement (Excel-AI Inputs_ppath). gdppc: {year: GDP per capita} (macro series)."""
    ctf = {}
    for t in ('power_capex_time_factor', 'power_capex_time_factor_2'):
        df = db.table(t)
        for code, y, v in zip(df['code'], df['year'].astype(int), to_float(df['value'])):
            ctf.setdefault(code, {})[y] = float(v)
    out = {}
    for r in xt.table('power_types'):
        f, leg = r['type'], r['legacy']
        for sc in CTF_SCENARIOS:              # a missing series takes the old series (wind, solar) or medium (L109)
            if f in RENEWABLES:
                code = f'wld.ctf.{sc}.{leg}'
                code = code if code in ctf else (f'wld.ctf.old{sc}.{leg}' if f in ('wnd', 'sol') else f'wld.ctf.med.{leg}')
            else:
                code = f'wld.ctf.med.{leg}'
            out[f'tcf|{f}|{sc}'] = {y: ctf[code].get(y, np.nan) for y in years}
        out[f'tcf|{f}'] = out[f'tcf|{f}|{ps["PsCtfScen"] if f in RENEWABLES else "med"}']
    st = db.table('power_storage_usd')
    for k, (tech_, par) in STORAGE.items():
        g = st[(st['technology'] == tech_) & (st['parameter'] == par)]
        v = dict(zip(g['year'].astype(int), to_float(g['value'])))
        out[k] = {y: v[max(x for x in v if x <= y)] for y in years}          # approximate match on the year
    out['cel'] = {y: (out['elcx'][y] + out['eltk'][y] * ps['PsLTHours']) / (ps['PsDlfRen'] * HOURS)
                  + out['elof'][y] / HOURS + out['elov'][y] for y in years}
    out['gdppc'] = {y: gdppc[y if k == 0 else y - 1] for k, y in enumerate(years)}   # previous year from 2023
    out['incx'] = {y: min(c('IncfLnCap'), np.log(v)) for y, v in out['gdppc'].items()}
    a, b, cc, d, e = (c(f'Incf{k}') for k in 'ABCDE')
    out['incp'] = {y: max(0.0, (((a * x + b) * x + cc) * x + d) * x + e) / c('IncfNorm') for y, x in out['incx'].items()}
    out['incf'] = {y: out['incp'][y] if str(ps['PsIncElAdj'])[:3] == 'Yes' else 1.0 for y in years}
    sh = db.table('ghg_shock')
    sh = dict(zip(sh.loc[sh['code'] == iso, 'year'].astype(int), to_float(sh.loc[sh['code'] == iso, 'value'])))
    out['shock'] = {y: sh.get(y, 0.0) for y in years}
    pr = db.table('power_coal_retirement')
    pr = dict(zip(pr.loc[pr['country'] == iso, 'year'].astype(int), to_float(pr.loc[pr['country'] == iso, 'value'])))
    for r in xt.table('power_types'):
        f = r['type']
        out[f'pret|{f}'] = {y: (pr.get(y, 0.0) if f == 'coa' and tech['coa']['planned'] == 'Yes' else 0.0) for y in years}
    return out


# ---- parameters (Excel-AI Inputs_ppar)
DEMAND_FLOWS = ['road', 'rail', 'domesair', 'domesnav', 'resident', 'food_forest', 'services', 'mining_chemicals',
                'ironstl', 'nonferrmet', 'machinery', 'cement', 'other_manufact', 'construc', 'ononspec']
OTHER_FLOWS = ['imports', 'exports', 'statdiff', 'transfer', 'distloss', 'ownuse']


def power_params(db, iso, settings, ps, tech, c):
    """EQ-A4.3. {item: value}: transmission costs, settings, shares of final power demand (Excel-AI Inputs_ppar)."""
    bal = balances(db, iso, settings.base_year)
    misc = db.table('power_misc_parameters')
    tmc = {s: float(misc.loc[(misc['sector'] == s) & (misc['variable'] == 'Value'), 'value'].iloc[0])
           for s in ('Residential', 'Industrial')}
    p = {'tmc|res': tmc['Residential'], 'tmc|ind': tmc['Industrial'], 'pass': ps['PsPass'], 'dlf_ren': ps['PsDlfRen'],
         'st_alloc': ps['PsSTAlloc'], 'st_marg_hours': c('StMargFactor') * ps['PsSTHours'], 'st_ratio': ps['PsSTRatio'],
         'lt_start': ps['PsLTStart'], 'lt_alloc': ps['PsLTAlloc'], 'extra_eff': ps['PsAddEff'],
         'maxcf_cg': ps['PsMaxCoalCF'], 'k_dispatch': ps['PsKDisp'], 'k_invest': ps['PsKInv'], 'min_cost': ps['PsMinCost'],
         'early_max': c('EarlyMaxShare'), 'early_factor': ps['PsEarlyMax'] if ps['PsEarlyBL'] == 'Yes' else 0.0,
         'ktoe_gwh': c('KtoeGWh')}
    for fl in OTHER_FLOWS + DEMAND_FLOWS:
        p[f'bal|{fl}'] = bal.get(fl, {}).get('ecy', 0.0)
    p['dem'] = sum(p[f'bal|{fl}'] for fl in DEMAND_FLOWS)
    p['gen_ktoe'] = sum(t['gen0'] for t in tech.values()) * HOURS / c('Thousand') / c('KtoeGWh')
    p['gen_per_cons'] = p['gen_ktoe'] / p['dem']
    share = lambda x: 0.0 if p['dem'] == 0 else x / p['dem']
    p['sh_nxp'] = share(-(p['bal|imports'] + p['bal|exports']))
    p['sh_tsd'] = share(-(p['bal|statdiff'] + p['bal|transfer'] + p['bal|distloss']))
    p['sh_eou'] = share(-p['bal|ownuse'])
    p['sh_add'] = p['gen_per_cons'] - 1 - p['sh_nxp'] - p['sh_tsd'] - p['sh_eou']
    return p


# ---- the generation types, user groups, demand groups and subsectors read by Mitigation section 3 (Inputs 204-270)
PRICE_BLOCK_POS = {'coa.pow': 1, 'coa.res': 28, 'coa.ind': 55, 'nga.pow': 84, 'nga.res': 111, 'nga.ind': 138,
                   'gso.all': 167, 'die.all': 196, 'lpg.all': 225, 'ker.all': 254, 'oop.all': 283, 'bio.all': 312}
POLLUTANTS = ['pm2', 'nox', 'so2', 'voc', 'bc', 'oc', 'co']
USER_GROUPS = [('res', 0.0, 1.0), ('ind', 1.0, -1.0)]          # group, weight on total demand, weight on residential
DEMAND_GROUPS = [('tra', 0.5), ('res', 1.0), ('ind', 0.0), ('srv', 0.0)]   # group, price weight on residential
DEMAND_SUBSECTORS = ['rod', 'ral', 'avi', 'nav', 'res', 'foo', 'srv', 'mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst',
                     'oen']
DEMAND_GROUP_OF = {'rod': 'tra', 'ral': 'tra', 'avi': 'tra', 'nav': 'tra', 'res': 'res', 'srv': 'srv'}   # else ind


def power_types(tech, ps, par, co2, efcalib, ecp, ecp_year, nonco2, base, c):
    """EQ-A4.4. {type: {column: value}}: the derived constants of each generation type (Excel-AI Inputs rows 207-215).
    ecp: the existing carbon pricing of the country (policies.ecp_table)."""
    fuels = {r['fuel']: r for r in xt.table('fuels')}
    pf_pos = {pc: i + 1 for i, pc in enumerate(['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res',
                                               'ecy.ind', 'gso.all', 'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all'])}
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in fuels]
    k_emb = [2021, 2022, 2023, 2024, 2025].index(ecp_year)
    gen_sum = sum(t['gen0'] for t in tech.values())
    out = {}
    for i, (f, t) in enumerate(tech.items()):
        p = dict(t)
        has_fuel = t['price_code'] != ''
        N, wacc, cf = t['life'], t['wacc'], t['cf']
        p['acap'] = (1 / N + wacc * c('CapAvgShr')) / (cf * HOURS)
        p['afix'] = t['dtc'] / N / (cf * HOURS) + t['opf']
        p['lcap'] = 1 / (cf * HOURS * t['dlf'])
        p['lfix'] = (t['dtc'] + t['tcx']) * p['lcap'] + t['opf'] + t['rns']
        p['vfix'] = t['vop'] + t['ffix']
        p['k'] = c('GJperkWh') / t['eff'] if has_fuel else 0.0
        p['ppos'] = PRICE_BLOCK_POS[t['price_code']] if has_fuel else 1
        p['ef'] = co2.get(f'{f}|pow', 0.0) * efcalib
        p['efk'] = p['ef'] * p['k']
        p['fpos'] = float(fuels[f]['position']) if has_fuel else 1
        p['pfpos'] = pf_pos[t['price_code']] if has_fuel else 1
        p['gj'] = float(fuels[f]['gj_per_unit']) if has_fuel else 1.0
        p['kpu'] = p['k'] / p['gj']
        p['puse'] = 1.0 if t['planned'] == 'Yes' else 0.0
        p['cg'] = 1.0 if t['dispatch'] == 'cg' else 0.0
        p['eflag'] = 1.0 if f == 'coa' else 0.0
        p['ninv'] = 1 / cf
        p['shr0'] = t['gen0'] / gen_sum
        p['pef'] = c('MWyMkWh') / par['ktoe_gwh'] / t['eff']
        p['co2f'] = p['ef'] * PJ_PER_KTOE
        p['tb'] = i * c('TieBreak')
        p['ecpk'] = xkeys.index(f'pow|{f}') + 1 if f'pow|{f}' in xkeys else 1
        key = xkeys[p['ecpk'] - 1]
        p['xcp0'] = 0.0 if key == 'none|none' else (ecp[f'xct|{key}'][k_emb] + ecp[f'xets|{key}'][k_emb])
        p['fflag'] = 1.0 if f in fuels else 0.0
        p['cfa'], p['cfs'] = t['cf_actual'], t['cf_studies']
        p['vreb'] = 1.0 if f in ('wnd', 'sol') else 0.0
        p['nua'] = t['out'] / (t['inp'] * c('KtoeGWh')) if t['inp'] else -1.0
        p['nus'] = t['eff_studies']
        p['wcty'] = ps['PsCtryWacc'] + ps['PsCoalAdj']
        p['wtec'] = ps['PsCtryWacc'] + t['wacc_adj']
        p['wstu'] = t['wacc_studies']
        p['rinv'] = 1 / N
        p['afx'] = t['dtc'] / N + t['opfx']
        p['dtx'] = t['dtc'] + t['tcx'] * base['TransmissionCostShare']
        p['pfl'] = 1.0 if has_fuel else 0.0
        p['pefx'] = c('MWyMkWh') / par['ktoe_gwh']
        p['hydf'], p['gasf'] = float(f == 'hyd'), float(f == 'nga')
        p['tpos'] = i + 1
        p['nvf'] = float(f in ('coa', 'nga', 'hyd'))
        p['renf'] = float(f in ('wnd', 'sol', 'ore', 'bio'))
        p['inp0'], p['out0'] = t['inp'], t['out']
        for pol in POLLUTANTS:
            p[f'ap0_{pol}'], p[f'ap1_{pol}'] = nonco2.get(f'pow.{f}.{pol}', (0.0, 0.0))
        out[f] = p
    return out


def user_groups(dd, par, cpi_index, last_hist):
    """End-user price groups (residential, industry; legacy G1, G2): transmission, pass-through, VAT and historical
    prices (real $/kWh). dd: prices_data.DomesticData of the country."""
    out = {}
    for pos, (g, wtot, wres) in enumerate(USER_GROUPS, 1):
        vr = dd.used(last_hist, f'mit.vatrate.ecy.{g}')
        u = {'pos': pos, 'wtot': wtot, 'wres': wres, 'tmc': par[f'tmc|{g}'], 'pass': par['pass'], 'vr': vr,
             'vshare': vr / (1 + vr)}
        for y in (2021, 2022, 2023, 2024):
            u[f'rp{y}'] = dd.used(y, f'mit.rp.ecy.{g}') * cpi_index[y]
            t = dd.text(y, f'mit.txo.ecy.{g}')
            try:
                u[f'tx{y}'] = float(t) * cpi_index[y]
            except ValueError:
                u[f'tx{y}'] = np.nan                         # no data ("")
        out[g] = u
    return out


def demand_groups(ela, par, users):
    """Power demand groups (legacy H1): elasticities of electricity, efficiency multiple, 2021 price."""
    out = {}
    for pos, (g, wres) in enumerate(DEMAND_GROUPS, 1):
        d = {'pos': pos, 'wres': wres, 'ey': ela[f'inc|ecy|{g}'], 'eu': ela[f'usg|ecy|{g}'], 'ef': ela[f'eff|ecy|{g}'],
             'alpha': ela[f'aei|ecy|{g}']}
        d['aeef'] = (1 / (1 + d['alpha'] + par['extra_eff'])) ** (1 + d['eu'])
        d['eps'] = d['eu'] + d['ef'] + d['eu'] * d['ef']
        d['p2021'] = wres * users['res']['rp2021'] + (1 - wres) * users['ind']['rp2021']
        out[g] = d
    return out


def demand_subsectors(db, iso, settings, base):
    """Electricity demand by subsector in the base year (legacy H3): Balances or EnergyCons (BalancesOrConsumption)."""
    bal = balances(db, iso, settings.base_year)
    subs = {r['sector']: r for r in xt.table('subsectors')}
    cons = db.table('energy_consumption')
    cons = cons[cons['code'] == f'{iso.lower()}.mit.enc.ele']
    cons = cons[cons['year'] == cons['year'].iloc[0]] if len(cons) else cons
    cons = dict(zip(cons['sector'], to_float(cons['value'])))
    use_bal = str(base['BalancesOrConsumption'])[:3] == 'Bal'
    groups = [g for g, _w in DEMAND_GROUPS]
    out = {}
    for s in DEMAND_SUBSECTORS:
        g = DEMAND_GROUP_OF.get(s, 'ind')
        b = bal.get(subs[s]['flow1'], {}).get('ecy', 0.0)
        e = cons.get(s, 0.0)
        e = 0.0 if np.isnan(e) else e
        out[s] = {'group': g, 'gpos': groups.index(g) + 1, 'd0': b if use_bal else e, 'bal': b, 'cons': e,
                  'tr': float(s == 'rod')}
    return out


def system_params(par, types, c):
    """Derived system parameters: required generation per final demand, coal capacity factor, grid CO2 intensity."""
    req = (1 + par['sh_nxp'] + par['sh_tsd'] + par['sh_eou'] + par['sh_add']) * par['ktoe_gwh'] * c('kWperMW') / HOURS
    gint = sum(t['inp0'] * t['co2f'] for t in types.values()) / sum(t['out0'] for t in types.values())
    return {'req_factor': req, 'cf_coal': types['coa']['cf'], 'gint': gint}
