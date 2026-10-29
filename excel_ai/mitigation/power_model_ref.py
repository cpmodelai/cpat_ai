"""v0.2.3 (version number aligned with CPAT-AI-Mitigation-Prototype v0.4.7; content as the previous version in Old/). 

v0.5.4 (power features P1, P2, P4; excel_ai/plans/Power_features.md): every MTInputs power input of the scenario (inp['par'],
the per-scenario settings; mvp_data(s) with the scenario's own settings: capacity factor and efficiency bounds, WACC,
scale-up rates, capex decline scenario, long-term storage hours); final deficit to gas (par['dgas'], legacy row 4252);
maximum capacity factor of gas (par['maxcf_nga'], legacy row 3784); long-term storage factor for 100% VRE
(par['lt100'], legacy row 3909); PPAs (inp['ppa'], legacy rows 2218, 3794, 3801-3805, 3987, 3993); renewable
subsidies (inp['rns'], legacy rows 2733-2745, 3142-3152, 3303-3313, 3665-3669); power revenue rebate (inp['reb'],
legacy rows 3595, 3615, 3644, 3663); electricity excise (inp['exs'] policy type 11, legacy row 2253; inp['ntx'] the
manual excise of 'Manual inputs' rows 161-162, legacy rows 3602, 3631, 216-217). With none of them given the engine
is the v0.5.3 engine.

v0.2: planned retirement by type (legacy K5 offers it for coal only): where a type's switch planned_retirement is
Yes (power_tech.csv, or inp['pflag']), the planned retirement data pret|<type> (power_paths.csv, nameplate MW, or
inp['pret']) replace the rate-based retirement capacity x 1/lifetime; retirement stays capped at the capacity, and
coal adds the cost-based early retirement. Memo outputs: total capacity, total nameplate investment, demand by group,
the cheapest of coal variable cost and wind and solar investment cost (ecmin) and the coal logit share (ecshr).

Python reference of the CPAT engineer power model (legacy Mitigation section 4, rows 2954-4297): demand (H),
dispatch (I), storage (J), retirement and capacity (K), investment (L), with the price side of v0.1.05 (B, C, D, E, G).

Year by year, as legacy: demand uses last year's electricity price; capacity of year t is last year's capacity less
retirements plus new investment; dispatch fills demand with fixed-output types first, then coal and gas by a logit on
variable cost; investment fills the gap between demand and capacity after retirements by a logit on levelised cost,
capped by scale-up rates, with a second round that fills the rest cheapest first.

fix: the bug fixes to apply (names in FIXES). The prototype runs with ALL_FIXES. v0.9.0 (Power_465, LD41): the data and
the cached rows come from legacy 465, where the CPAT team fixed every bug of FIXES, so legacy_test runs with ALL_FIXES
and reproduces both cached 465 runs (base, ctax) to 2e-12 (456: fix = frozenset(), 4e-13). v0.9.0 also adds the legacy
over/under-estimated cost residual of the price chain (rows 3607, 3636; inp txo_res/txo_ind, outputs ores_*), active
when the residual of the last historical year is negative (Egypt 465 residential); without txo_* it is off. Used by check_v1_07.py and make_bugfix_book.py; independent of the
workbook builder (reads data/*.csv only).
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
T = ['coa', 'nga', 'oop', 'nuc', 'wnd', 'sol', 'hyd', 'ore', 'bio']
GROUPS = ['tra', 'res', 'ind', 'srv']
GROUP_OF = {'rod': 'tra', 'ral': 'tra', 'avi': 'tra', 'nav': 'tra', 'res': 'res', 'srv': 'srv'}   # others: ind
PJ_PER_KTOE = 0.041868
FIXES = {  # name: (legacy rows, short description)
    'services': ('3731', 'services electricity demand grows with the industrial multiple from 2024 (copy error)'),
    'aee': ('3691, 3697, 3703, 3709', 'autonomous efficiency exponent uses the efficiency elasticity instead of the '
                                      'usage elasticity'),
    'income': ('3692, 3698, 3704, 3710', 'income factor on the GDP elasticity applied twice, anchored to 2023 '
                                         '($M3686)'),
    'lt_alloc': ('3911, 3912', 'allocation of long-term storage cost to VRE (33%) applied twice'),
    'invcost': ('4276-4284', 'investment spending uses the capital cost at factor 1 instead of the capital cost of '
                             'the year'),
    'cmin': ('4046, 4073-4081', 'investment logit normalised by the cheapest type including types not permitted'),
    'retlag': ('3973', 'early coal retirement subtracts nameplate retirements from effective capacity additions'),
    'coalret': ('4009-4011', 'effective coal retirement not capped like the nameplate retirement'),
    'rebate': ('3407-3409', 'feebate rebate per kWh consumed added to the cost per kWh generated (x 1.22)'),
    'kcheck': ('4024', 'capacity needed is computed from the planned capacity of last year, not the actual capacity '
                       '(differs when investment could not be placed)'),
    'nextyear': ('4027', 'capacity bought this year (online next year) is sized for this year\'s demand, although the row '
                         'is labelled "Next Year Demand" (L67, was issue I8; v0.4.14; v0.6.2: fixed with this year\'s '
                         'demand x (1 + growth from last year))'),
}
ALL_FIXES = frozenset(FIXES)


def read(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


INCOME = {r['code']: r['income_group'] for r in read('countries.csv')}
# v0.3.3: country of the cached legacy run (data/legacy_*.csv; output codes <country>.mit...): read from the data
LEGACY_RUN = {'iso': read('legacy_cached_baseline.csv')[0]['code'].split('.')[0].upper()}


def base_data(years, iso):
    """v0.3.3: the power data of country iso (column country of the power CSVs)."""
    tech = {r['code']: r for r in read('power_tech.csv') if r['country'] == iso}
    paths = {r['key']: [float(r[str(y)]) for y in years] for r in read('power_paths.csv') if r['country'] == iso}
    par = {r['key']: float(r['value']) for r in read('power_params.csv') if r['country'] == iso}
    dem0 = {r['subsector']: float(r['ktoe_2022']) for r in read('power_demand.csv') if r['country'] == iso}
    return tech, paths, par, dem0


LEG_CODE = {'oop': 'oil'}                     # legacy code of a type in the Power tab
EFF_ONE = ('wnd', 'sol', 'hyd', 'ore')        # legacy A4 P: typed efficiency 1.0 of the studies
BAL_FUELS = {'oop': ['oop', 'gso', 'die', 'ker', 'lpg', 'jfu']}   # Balances fuels of a type (legacy A1 2959-2973)
RENEW = ('wnd', 'sol', 'hyd', 'ore', 'bio')   # capex time factors of the renewable-cost decline scenario


def mvp_data(iso, years, s, base_year, hyd_share, present_share):
    """v0.5.2 (check): the prototype's power data step with the legacy data-step bugs fixed (register L52-L55; L56 and the
    WACC are left to power_tech.csv, which has the CoC chain of the legacy Tech source), recomputed independently from
    the legacy Power tab (data/legacy_Power_cells.csv), the legacy Balances (data/legacy_Balances.csv) and the MTInputs
    settings s (NameOfParameter -> scenario-1 value):
      L52 every type takes the country Power value where it is > 0, else the world value (legacy: world for renewables);
      L53 capacity factor = actual (base-year output / installed capacity of the base year, Power rows 358-1635) inside
          the CFOverride bounds, else the studies value;
      L54 hydro invests from the base year only when its generation share is above hyd_share, else NewInvHydYear;
      L55 the country row is searched in the country block (Power rows 112-294) only;
    and the capex time factors from the Power tab (rows 302-330; legacy's stored 2039-2041 values are stale, I94).
    Returns (tech {code: row}, paths {key: series}, par {key: value}) to override base_data(); the other columns
    (capex, decommissioning and transmission capex, WACC, flags) are the values of power_tech.csv."""
    cells = {}
    for r in read('legacy_Power_cells.csv'):
        cells[(int(r['row']), int(r['col']))] = r['value']
    fv = lambda r, c: float(cells.get((r, c)) or 0)
    code_row = {}
    for r in range(25, 357):                               # Power A25:A356, first match
        v = cells.get((r, 1))
        if v and v.lower() not in code_row:
            code_row[v.lower()] = r
    ctry_row = {}
    for r in range(112, 295):                              # L55: country block only
        v = cells.get((r, 1))
        if v and v.lower() not in ctry_row:
            ctry_row[v.lower()] = r
    col = {'cf': 5, 'capex': 6, 'eff': 7, 'opfix': 8, 'opvar': 9, 'wacc': 10, 'life': 11}
    ic_year = next(c for c in range(6, 60) if cells.get((357, c)) == str(base_year))
    ic = {cells[(r, 3)].lower(): fv(r, ic_year) for r in range(358, 1636) if cells.get((r, 3))}
    yc = {int(float(cells[(302, c)])): c for c in range(6, 60) if cells.get((302, c))}
    bal = {r['flow_code']: r for r in read('legacy_Balances.csv') if r['country_code'] == iso}
    tech0 = {r['code']: dict(r) for r in read('power_tech.csv') if r['country'] == iso}
    dec = str(s['RenewableCostDeclineRate'])
    scen = 'hgh' if dec == 'High' else 'vhg' if dec.startswith('V') else dec[:3].lower()
    tech, paths = {}, {}
    gen0, cap0 = {}, {}
    for f in T:
        t = LEG_CODE.get(f, f)
        w = code_row[f'wld.mpp.{t}']
        c = ctry_row.get(f'{iso.lower()}.mpp.{t}')
        rule_c = lambda k: fv(c, col[k]) if c and fv(c, col[k]) > 0 else fv(w, col[k])   # L52: all types
        fuels = BAL_FUELS.get(f, [f])
        out = sum(float(bal['eloutput'][u] or 0) for u in fuels)          # GWh
        inp_ = -sum(float(bal['power'][u] or 0) for u in fuels)           # ktoe
        studies = 1.0 if f in EFF_ONE else rule_c('eff')
        act = out / (inp_ * 11.63) if inp_ else None
        eff = studies if act is None or act < float(s['MinimumThermalEfficiency']) else act
        g0 = out * 1000 / 8760
        inst = ic.get(f'{iso.lower()}.{t}', 0.0)
        cfa = g0 / inst if inst else 0.0                                     # L53
        lo = float(s['CFOverrideIfBelowWndSol'] if f in ('wnd', 'sol') else s['CFOverrideIfBelowFosOth'])
        cf = cfa if lo < cfa < float(s['CFOverrideIfAbove']) else rule_c('cf')
        life = rule_c('life')
        row = dict(tech0[f])
        row.update({'life_years': life, 'efficiency': eff, 'capacity_factor': cf,
                    'opf_usd_per_kwh': rule_c('opfix') / (8760 * cf), 'vop_usd_per_kwh': rule_c('opvar'),
                    'gen0_mwy': g0, 'cap0_mw': g0 / cf,
                    'retire_rate': 0.0 if f == 'hyd' and s['HydroDoesntRetire'] == 'Yes' else 1 / life})
        tech[f], gen0[f], cap0[f] = row, g0, g0 / cf
        rc = code_row.get(f'wld.ctf.{scen if f in RENEW else "med"}.{t}') or \
            code_row[f'wld.ctf.{"old" + scen if f in ("wnd", "sol") else "med"}.{t}']   # v0.5.4: L109 (missing series)
        paths[f'tcf|{f}'] = [fv(rc, yc[y]) for y in years]
    mt = {'oop': 'Oil'}
    for f in T:
        nm = 'NewInv' + mt.get(f, f.capitalize())
        perm = s[nm]
        if perm == 'If Present*':
            perm = 'Yes' if cap0[f] / sum(cap0.values()) > present_share else 'No'
        start = s[nm + 'Year']
        if f == 'hyd' and gen0[f] / sum(gen0.values()) > hyd_share:      # L54
            start = base_year
        tech[f]['invest_permitted'], tech[f]['invest_start'] = perm, float(start)
    if 'WACCSource' in s:                                  # v0.5.4: WACC of the scenario (legacy rows 2988-2996)
        src = str(s['WACCSource'])
        wmin = float(s['MinimumWACC'])
        inc_code = INCOME[iso]
        inc_w = next(fv(r, 14) for r in range(20, 24) if cells.get((r, 13)) == inc_code)
        coal = float(tech0['coa']['wacc'])                  # power_tech.csv: Tech (country + technology premium)
        for f in T:
            t = LEG_CODE.get(f, f)
            w = code_row[f'wld.mpp.{t}']
            c = ctry_row.get(f'{iso.lower()}.mpp.{t}')
            stud = fv(c, col['wacc']) if c and fv(c, col['wacc']) > 0 else fv(w, col['wacc'])
            tech[f]['wacc'] = (coal if src.startswith('Country') else float(tech0[f]['wacc']) if src == 'Tech' else
                               max(float(s['WACCUserGlobal']) if src == 'User' else inc_w if src.startswith('Income')
                                   else stud, wmin))
    if 'MaxScaleUpRateCategory' in s:                      # v0.5.4: scale-up rates of the scenario (legacy S85:S91)
        cat = str(s['MaxScaleUpRateCategory'])
        ctry = next((fv(r, 3) for r in range(2349, 2571) if cells.get((r, 2)) == iso), 0.0)
        catr = next((fv(r, 10) for r in range(20, 24) if cells.get((r, 9)) == cat), 0.0)
        vre = ctry if cat[:4] == 'Ctry' else float(s['MaxWindSolarScaleup']) if cat == 'UserDefined' else catr
        for f in T:
            tech[f]['scaleup_rate'] = (float(s['MaxNonVREAsPCOfTotalGen']) if f in ('coa', 'nga', 'hyd') else
                                       vre if f in ('wnd', 'sol') else float(s['MaxNonNucOreBioAsPCOfTotalGen']))
    af = lambda f: (1 - (1 / (1 + float(tech[f]['wacc']))) ** float(tech[f]['life_years'])) / \
        (1 - 1 / (1 + float(tech[f]['wacc'])))
    par = {'dlf_ren': (af('wnd') + af('sol')) / 2}
    if 'StorageHoursForLTStorage' in s:                    # v0.5.4: long-term storage cost of the scenario (J2)
        hdr = {c: int(float(cells[(1883, c)])) for c in range(6, 60) if cells.get((1883, c))}
        colof = lambda y: max(c for c, yy in hdr.items() if yy <= y)             # approximate match, as legacy
        for key, row in (('elcx', 1907), ('eltk', 1911), ('elof', 1908), ('elov', 1909)):
            paths[key] = [fv(row, colof(y)) for y in years]
        hrs = float(s['StorageHoursForLTStorage'])
        paths['cel'] = [(paths['elcx'][k] + paths['eltk'][k] * hrs) / (par['dlf_ren'] * 8760) + paths['elof'][k] / 8760
                        + paths['elov'][k] for k in range(len(years))]
    return tech, paths, par


def engine(inp, years, fix=ALL_FIXES, shock=False):
    """inp: elast {group: (eps_y, eps_u, eps_f, alpha)}; gdp, inc, shock, cpf (years); rp2021_res, rp2021_ind;
    rphist_res, rphist_ind (years, used up to last_hist); vat_res, vat_ind; last_hist; vbc[i], d5[i] ($/kWh, years);
    shp_gj[i] ($/GJ fuel, years) or d6[i] ($/kWh incl. rebate, years); tvc_extra[i] (optional values after the last
    year for the D9 window, legacy 2041). Returns {name: series or [series by type]}."""
    n = len(years)
    tech, paths, par, dem0 = base_data(years, inp['iso'])
    if 'data' in inp:                            # v0.5.2: the prototype data step (mvp_data: legacy data-step bugs fixed)
        tech = inp['data'][0]
        paths = {**paths, **inp['data'][1]}
        par = {**par, **inp['data'][2]}
    par = {**par, **inp.get('par', {})}          # v0.5.4: settings of the scenario (MTInputs column of the scenario)
    par.setdefault('maxcf_coa', par['maxcf_cg'])
    par.setdefault('maxcf_nga', par['maxcf_cg'])
    par.setdefault('lt100', 1.0)
    par.setdefault('shock_k', 1.0)
    tf = [tech[f] for f in T]
    num = lambda i, k: float(tf[i][k])
    cf = [num(i, 'capacity_factor') for i in range(9)]
    eff = [num(i, 'efficiency') for i in range(9)]
    gj_kwh = [0.0036 / eff[i] if tf[i]['price_code'] else 0.0 for i in range(9)]
    permit_yes = [tf[i]['invest_permitted'] == 'Yes' for i in range(9)]
    x, alloc_lt = par['lt_start'], par['lt_alloc']
    kd, ki, cmin_floor = par['k_dispatch'], par['k_invest'], par['min_cost']
    shares = par['sh_nxp'] + par['sh_tsd'] + par['sh_eou'] + par['sh_add']
    o = {k: [[0.0] * n for _ in T] for k in (
        'cap', 'effcap', 'gen', 'shr', 'pe', 'co2', 'ret', 'reteff', 'pni', 'first', 'second', 'nei', 'nim', 'usd',
        'phi', 'tic', 'lfx', 'lvc', 'fix', 'gnc', 'cax', 'caxav', 'stoav', 'maxinv', 'tvc', 'shk', 'permit',
        'gmin', 'lgd', 'lgi', 'space', 'dsum')}
    pflag = inp.get('pflag', [1.0 if tf[i].get('planned_retirement') == 'Yes' else 0.0 for i in range(9)])
    pret = inp.get('pret', [paths.get(f'pret|{f}', [0.0] * n) for f in T])
    o['pret'] = [list(pret[i]) for i in range(9)]
    ppa = list(inp.get('ppa', [0.0] * n))       # v0.5.4: PPA share of coal and gas generation (legacy row 3801)
    rns = [list(x) for x in inp.get('rns', [[num(i, 'rns_usd_per_kwh')] * n for i in range(9)])]   # v0.5.4 (A17)
    reb = float(inp.get('reb', 0.0))             # v0.5.4: power revenue rebate switch (legacy J3595 = -1)
    exs = list(inp.get('exs', [0.0] * n))        # v0.5.4: electricity excise, policy type 11 ($/kWh; legacy row 2253)
    ntx = {g: list(inp.get('ntx', {}).get(g, [0.0] * n)) for g in ('res', 'ind')}   # v0.5.4: manual excise ($/kWh)
    maxcf = [par['maxcf_coa'] if f == 'coa' else par['maxcf_nga'] if f == 'nga' else 0.0 for f in T]
    for k_ in ('glg', 'gmx', 'rns', 'prrns'):
        o[k_] = [[0.0] * n for _ in T]
    o['rns'] = rns
    for k_ in ('ppr', 'dgas', 'pex_res', 'pex_ind', 'ntx_res', 'ntx_ind', 'rreb_res', 'rreb_ind', 'rpex_res',
               'rpex_ind', 'rnvat_res', 'rnvat_ind'):
        o[k_] = [0.0] * n
    o['ppa'] = ppa
    o['ntx_res'], o['ntx_ind'] = ntx['res'], ntx['ind']
    kl = years.index(inp['last_hist']) if inp['last_hist'] in years else 0
    for k in ('captot', 'nimtot', 'ecmin', 'ecshr', 'req', 'vre', 'msc', 'cph', 'gncav', 'ccpav', 'demtot', 'early', 'need', 'reb', 'sc_res', 'sc_ind',
              'rppre_res', 'rppre_ind', 'rp_res', 'rp_ind', 'cons_res', 'cons_ind', 'reqcg', 'vcmin', 'rem', 'gtot',
              'dgen', 'egrow', 'kafter', 'cmin', 'deficit', 'usdtot', 'sgap_res', 'sgap_ind', 'rvat_res', 'rvat_ind',
              'rcarb_res', 'rcarb_ind', 'rgap_res', 'rgap_ind', 'ores_res', 'ores_ind'):
        o[k] = [0.0] * n
    o['mult'] = {g: [0.0] * n for g in GROUPS}
    o['aeef'] = {}                               # v0.5.4: efficiency multiple of the scenario (AdditionalEfficiencyPower)
    for g in GROUPS:
        ey, eu, epf, a = inp['elast'][g]
        o['aeef'][g] = [1 / (1 + a + par['extra_eff']) ** (1 + (eu if 'aee' in fix else epf))] * n
    o['pdem'] = {g: [0.0] * n for g in GROUPS}
    dem = {s: [0.0] * n for s in dem0}
    ef = {r['key']: float(r['ef_tco2_per_gj']) for r in read('ef_co2.csv')}
    efp = [ef.get(f'{inp["iso"]}|{f}|pow', 0.0) * inp.get('co2k', 1.0) for f in T]   # v0.3.2: calibrated EF (EFCalib)
    shr0 = [num(i, 'gen0_mwy') / sum(num(j, 'gen0_mwy') for j in range(9)) for i in range(9)]
    for k in range(n):                           # D: variable cost incl. shadow price (D6) and rebate, all years
        for i in range(9):
            o['shk'][i][k] = inp['d6'][i][k] if 'd6' in inp else inp['shp_gj'][i][k] * gj_kwh[i]
        if 'd6' not in inp and k > 0:            # rebate from the second year, fixed base-year shares (legacy D6)
            avg = sum(o['shk'][i][k] * shr0[i] for i in range(9))
            o['reb'][k] = -avg * (1 if 'rebate' in fix else par['gen_per_cons'])
        for i in range(9):
            o['tvc'][i][k] = inp['vbc'][i][k] + inp['d5'][i][k] + o['shk'][i][k] + o['reb'][k]
    for i in range(9):                           # D9: discounted average of variable cost to the end of the horizon
        w = num(i, 'wacc')
        path = o['tvc'][i] + list(inp['tvc_extra'][i] if 'tvc_extra' in inp else [])
        dfs = [(1 + w) ** -j for j in range(len(path))]
        for k in range(n):
            o['lvc'][i][k] = sum(a * b for a, b in zip(dfs[k:], path[k:])) / sum(dfs[k:])
            o['dsum'][i][k] = sum(dfs[k:n])
    k30 = 0.0
    done = set()

    def demand(k):                               # v0.4.14: one year of block H (also next year's, for L67)
        y = years[k]
        done.add(k)
        # ---------------- H demand
        if k == 0:
            for s in dem:
                dem[s][0] = dem0[s]
            w_res = {'tra': 0.5, 'res': 1.0, 'ind': 0.0, 'srv': 0.0}
            for g in GROUPS:
                o['pdem'][g][0] = w_res[g] * inp['rp2021_res'] + (1 - w_res[g]) * inp['rp2021_ind']
                o['mult'][g][0] = 1.0
        else:
            pr = lambda g, kk: (inp['rp2021_' + g] if kk < 0 else o['rp_' + g][kk])   # price of year index kk
            p = {g: (pr(g, k - 1), pr(g, k - 2)) for g in ('res', 'ind')}
            p['tra'] = ((p['res'][0] + p['ind'][0]) / 2, (p['res'][1] + p['ind'][1]) / 2)
            p['srv'] = p['ind']
            for g in GROUPS:
                o['pdem'][g][k] = p[g][0]
                ey, eu, epf, a = inp['elast'][g]
                aee = 1 / (1 + a + par['extra_eff']) ** (1 + (eu if 'aee' in fix else epf)) - 1
                inc = inp['inc'][k] if 'income' in fix else inp['inc'][k] ** 2 / inp['inc'][1]
                gd = (1 + inp['gdp'][k]) ** (ey * inc) - 1
                c0, c1 = inp['cpf'][k], inp['cpf'][k - 1]
                pe_ = (p[g][0] / p[g][1]) ** eu * ((p[g][0] + c0) / (p[g][1] + c1)) ** (epf + eu * epf) - 1
                o['mult'][g][k] = (1 + aee) * (1 + gd) * (1 + pe_) * (1 + (inp['shock'][k] * par['shock_k'] if shock
                                                                           else 0.0))
            for s in dem:
                g = GROUP_OF.get(s, 'ind')
                if s == 'srv' and y >= 2024 and 'services' not in fix:
                    g = 'ind'
                dem[s][k] = dem[s][k - 1] * o['mult'][g][k]
                if s in inp.get('dem_fixed', {}):     # v0.3.5: road demand from the engineer road model (prototype 5b)
                    dem[s][k] = inp['dem_fixed'][s][k]
        tot = sum(dem[s][k] for s in dem)
        o['demtot'][k] = tot
        o['cons_res'][k] = dem['res'][k] * par['ktoe_gwh']
        o['cons_ind'][k] = (tot - dem['res'][k]) * par['ktoe_gwh']
        o['req'][k] = sum(num(i, 'gen0_mwy') for i in range(9)) if k == 0 else \
            tot * (1 + shares) * par['ktoe_gwh'] * 1000 / 8760

    for k, y in enumerate(years):
        if k not in done:
            demand(k)
        # ---------------- K1 capacity
        for i in range(9):
            o['cap'][i][k] = num(i, 'cap0_mw') if k == 0 else \
                o['cap'][i][k - 1] - o['ret'][i][k - 1] + o['nim'][i][k - 1]
            o['effcap'][i][k] = o['cap'][i][k] * cf[i]
            o['permit'][i][k] = 1.0 if permit_yes[i] and y >= num(i, 'invest_start') else 0.0
        toteff = sum(o['effcap'][i][k] for i in range(9))
        o['captot'][k] = sum(o['cap'][i][k] for i in range(9))
        # ---------------- I dispatch
        if True:                                 # dispatch (base year: memo rows only, generation is data)
            cg = [i for i in range(9) if tf[i]['dispatch'] == 'cg']
            for i in range(9):
                if i not in cg:
                    o['gen'][i][k] = o['effcap'][i][k]
            reqcg = max(o['req'][k] - sum(o['gen'][i][k] for i in range(9) if i not in cg), 0.0)
            o['reqcg'][k] = reqcg
            gmax = {i: o['cap'][i][k] * maxcf[i] for i in cg}          # v0.5.4: coal and gas maxima (rows 3783-3786)
            for i in range(9):
                o['gmx'][i][k] = o['cap'][i][k] * maxcf[i]
            gmin = {i: min(max(reqcg - sum(gmax[j] for j in cg if j != i), 0.0), gmax[i]) for i in cg}
            rem = max(reqcg - sum(gmin.values()), 0.0)
            vc = {i: max(o['tvc'][i][k], cmin_floor) for i in cg}
            m = min(vc.values())
            lg = {i: math.exp(-kd * vc[i] / m) for i in cg}
            o['rem'][k], o['vcmin'][k] = rem, m
            for i in cg:
                o['gmin'][i][k], o['lgd'][i][k] = gmin[i], lg[i]
            effcg = sum(o['effcap'][i][k] for i in cg)               # v0.5.4: PPAs (legacy rows 3794, 3804-3805)
            ratio = 1.0 if effcg == 0 else reqcg / effcg
            o['ppr'][k] = ratio
            for i in range(9):
                o['glg'][i][k] = o['gen'][i][k]
            for i in cg:
                o['glg'][i][k] = min(gmax[i], gmin[i] + rem * lg[i] / sum(lg.values()))
                o['gen'][i][k] = o['glg'][i][k] + ppa[k] * (o['effcap'][i][k] * ratio - o['glg'][i][k])
            if k == 0:
                for i in range(9):
                    o['gen'][i][0] = num(i, 'gen0_mwy')
        gtot = sum(o['gen'][i][k] for i in range(9))
        o['gtot'][k] = gtot
        o['dgen'][k] = max(0.0, gtot - o['gtot'][k - 1]) if k else 0.0
        for i in range(9):
            o['shr'][i][k] = o['gen'][i][k] / gtot if gtot else 0.0
            o['pe'][i][k] = o['gen'][i][k] * 8.76 / par['ktoe_gwh'] / eff[i]
            o['co2'][i][k] = o['pe'][i][k] * PJ_PER_KTOE * efp[i]
        v = sum(o['shr'][i][k] for i in range(9) if int(tf[i]['vre_share']))
        o['vre'][k] = v
        # ---------------- J storage
        cph = (paths['cbat'][k] + paths['cint'][k] / par['st_ratio']) / (par['dlf_ren'] * 8760) + paths['obat'][k] / 8760
        m_lt = 2 * (v - x) / (1 - x) ** 2 if v > x else 0.0
        lt = m_lt * par['lt100'] * paths['cel'][k] * alloc_lt * (1 if 'lt_alloc' in fix else alloc_lt)   # v0.5.4: lt100
        o['cph'][k], o['msc'][k] = cph, par['st_alloc'] * par['st_marg_hours'] * v * cph + lt
        # ---------------- B, C, E (v0.1.05) and D9, E1
        for i in range(9):
            N, w, cfi = num(i, 'life_years'), num(i, 'wacc'), cf[i]
            dlf = (1 - (1 + w) ** -N) / (1 - (1 + w) ** -1)
            vflag = int(tf[i]['vre'])
            o['cax'][i][k] = num(i, 'cax0_usd_per_kw') * paths[f'tcf|{T[i]}'][k]
            if k == 0:
                o['caxav'][i][0], o['stoav'][i][0] = o['cax'][i][0], vflag * o['msc'][0]
            else:
                ph = o['phi'][i][k - 1]
                o['caxav'][i][k] = o['caxav'][i][k - 1] * (1 - ph) + o['cax'][i][k - 1] * ph
                o['stoav'][i][k] = o['stoav'][i][k - 1] * (1 - ph) + vflag * o['msc'][k] * ph
            dtc, tcx, opf = num(i, 'dtc_usd_per_kw'), num(i, 'tcx_usd_per_kw'), num(i, 'opf_usd_per_kwh')
            o['fix'][i][k] = (o['caxav'][i][k] * (1 / N + w / 2) + dtc / N) / (cfi * 8760) + o['stoav'][i][k] + opf
            o['lfx'][i][k] = (o['cax'][i][k] + dtc + tcx) / (cfi * 8760 * dlf) + opf + rns[i][k] \
                + vflag * o['msc'][k]                                          # v0.5.4: renewable subsidy (C5)
            o['gnc'][i][k] = o['fix'][i][k] + inp['vbc'][i][k]
        o['gncav'][k] = sum(o['shr'][i][k] * o['gnc'][i][k] for i in range(9))
        o['ccpav'][k] = sum(o['shr'][i][k] * inp['d5'][i][k] for i in range(9)) * par['gen_per_cons']
        # ---------------- G prices (supply cost lagged one year; VAT on the policy term, as legacy)
        for g in ('res', 'ind'):
            sc = (o['gncav'][k - 1] if k else o['gncav'][0]) + par[f'tmc|{g}']
            vat = inp['vat_' + g]
            pre = inp['rphist_' + g][k] if y <= inp['last_hist'] else \
                o['rppre_' + g][k - 1] + par['pass'] * (sc - o['sc_' + g][k - 1]) * (1 + vat)
            if 'txo_' + g in inp and y >= inp['last_hist']:    # v0.9.0 (Power_465): over/under-estimated costs
                if y == inp['last_hist']:                       # (legacy rows 3607, 3636): the residual of the last
                    o['ores_' + g][k] = pre / (1 + vat) - sc - ntx[g][k] - inp['txo_' + g] - inp.get('ps_' + g, 0.0)
                else:                                           # historical year; a negative residual (costs
                    j_, scl = o['ores_' + g][kl], o['sc_' + g][kl]   # underestimated) scales with the supply cost
                    o['ores_' + g][k] = j_ * min(sc, scl) / scl if j_ < 0 and scl else j_   # when it falls
                    pre += par['pass'] * (o['ores_' + g][k] - o['ores_' + g][k - 1]) * (1 + vat)
            o['sc_' + g][k], o['rppre_' + g][k] = sc, pre
            pex = exs[k] + (par['pass'] * (ntx[g][k] - ntx[g][kl]) if y > inp['last_hist'] else 0.0)   # v0.5.4
            pol = o['ccpav'][k] * par['pass'] * (1 - reb) + pex     # v0.5.4: rebate (rows 3615, 3644), excise
            o['pex_' + g][k] = pex
            o['rp_' + g][k] = max(pre + pol * (1 + vat), cmin_floor)   # v0.7.0: floor as the sheet (v0.5.6, I60)
            o['sgap_' + g][k] = pre / (1 + vat) - sc          # v0.2.4: negative = price below cost (subsidy)
            cons = o['cons_' + g][k]
            o['rvat_' + g][k] = pre * vat / (1 + vat) * cons
            o['rcarb_' + g][k] = o['ccpav'][k] * cons
            o['rgap_' + g][k] = o['sgap_' + g][k] * cons
            o['rnvat_' + g][k] = pol * vat * cons                  # VAT on the new policies passed through
            o['rreb_' + g][k] = -reb * o['ccpav'][k] * par['pass'] * cons   # v0.5.4: rebate (legacy row 3663)
            o['rpex_' + g][k] = pex * cons                          # v0.5.4: excise revenue (rows 3660, 3664)
        for i in range(9):
            o['tic'][i][k] = max(o['lfx'][i][k] + o['lvc'][i][k], cmin_floor)
        # ---------------- K4 cost-based early coal retirement, K5/K6 retirements
        maxinv = [num(i, 'scaleup_rate') * toteff * o['permit'][i][k] for i in range(9)]
        incdem = max(0.0, sum(o['gen'][i][k - 1] for i in range(9)) - sum(o['gen'][i][k - 2] for i in range(9))) \
            if k >= 2 else 0.0
        retlag = sum((o['reteff'] if 'retlag' in fix else o['ret'])[i][k - 1] for i in range(1, 9)) if k >= 1 else 0.0
        growth = max(0.0, maxinv[4] + maxinv[5] - incdem - retlag)
        o['egrow'][k] = growth
        mx = min(o['effcap'][0][k] * par['early_max'], growth)
        cc = [o['tvc'][0][k], o['tic'][4][k], o['tic'][5][k]]                # legacy K4: coal cost not floored
        e = [math.exp(-ki * c / min(cc)) for c in cc]
        o['ecmin'][k], o['ecshr'][k] = min(cc), e[0] / sum(e)
        early_np = max(0.0, mx * (1 - e[0] / sum(e))) / cf[0] * par['early_factor'] * (1 - ppa[k]) if cf[0] \
            else 0.0                                 # v0.5.4: not the share under PPA (legacy rows 3987, 3993)
        o['early'][k] = early_np
        for i in range(9):
            planned = pret[i][k] if pflag[i] else o['cap'][i][k] * num(i, 'retire_rate')
            if i == 0:
                o['ret'][0][k] = min(planned + early_np, o['cap'][0][k])
                o['reteff'][0][k] = (o['ret'][0][k] if 'coalret' in fix else planned + early_np) * cf[0]
            else:
                o['ret'][i][k] = min(planned, o['cap'][i][k])
                o['reteff'][i][k] = o['ret'][i][k] * cf[i]
        # ---------------- K7 effective capacity needed (legacy: this year's demand; fixed: next year's)
        chk = toteff if (k == 0 or 'kcheck' in fix) else k30
        after = chk - sum(o['reteff'][i][k] for i in range(9))
        req = o['req'][k]                        # v0.6.2 (L67): next year's estimated as this year's x (1 + growth from
        if 'nextyear' in fix:                    # last year): no later year is read (no circular reference)
            req *= (req / o['req'][k - 1]) if k > 0 and o['req'][k - 1] else 1.0
        need = max(req - after, 0.0)
        o['need'][k], k30 = need, after + need
        o['kafter'][k] = after
        # ---------------- L investment: logit on levelised cost, capped by scale-up rates, then cheapest first
        tic = [o['tic'][i][k] for i in range(9)]
        cmin = min([tic[i] for i in range(9) if o['permit'][i][k]] or [min(tic)]) if 'cmin' in fix else min(tic)
        lg = [o['permit'][i][k] * math.exp(-ki * tic[i] / cmin) for i in range(9)]
        pni = [u / sum(lg) for u in lg]
        o['cmin'][k] = cmin
        raw = [need * q for q in pni]
        first = [min(maxinv[i], raw[i]) for i in range(9)]
        deficit = sum(raw) - sum(first)
        o['deficit'][k] = deficit
        space = [(maxinv[i] - first[i]) * o['permit'][i][k] for i in range(9)]
        order = sorted(range(9), key=lambda i: tic[i] + i * 1.356e-6)     # legacy tie breaker
        second, cum_prev, run_ = [0.0] * 9, 0.0, 0.0
        for i in order:
            run_ += space[i]
            cum = min(deficit, run_)
            second[i] = o['permit'][i][k] * (cum - cum_prev)
            cum_prev = cum
        dgas = deficit - sum(second) if par.get('dgas') else 0.0   # v0.5.4: final deficit to gas (legacy 4247-4252)
        o['dgas'][k] = dgas
        for i in range(9):
            o['pni'][i][k], o['first'][i][k], o['second'][i][k], o['maxinv'][i][k] = pni[i], first[i], second[i], maxinv[i]
            o['nei'][i][k] = first[i] + second[i] + (dgas if T[i] == 'nga' else 0.0)
            o['lgi'][i][k], o['space'][i][k] = lg[i], space[i]
            o['nim'][i][k] = o['nei'][i][k] / cf[i]
            capex = o['cax'][i][k] if 'invcost' in fix else num(i, 'cax0_usd_per_kw')
            o['usd'][i][k] = capex * o['nim'][i][k] / 1000
            den = o['cap'][i][k] + o['nim'][i][k] - o['ret'][i][k]
            o['phi'][i][k] = 0.0 if den == 0 else o['nim'][i][k] / den
        o['usdtot'][k] = sum(o['usd'][i][k] for i in range(9))
        o['nimtot'][k] = sum(o['nim'][i][k] for i in range(9))
    for key, val in (('cfu', cf), ('nuu', eff), ('kwh', gj_kwh), ('wac', [num(i, 'wacc') for i in range(9)]),
                     ('cap0', [num(i, 'cap0_mw') for i in range(9)]), ('rate', [num(i, 'scaleup_rate') for i in range(9)]),
                     ('rr', [num(i, 'retire_rate') for i in range(9)]),
                     ('perm', [1.0 if permit_yes[i] else 0.0 for i in range(9)]),
                     ('start', [num(i, 'invest_start') for i in range(9)]),
                     ('dlf', [(1 - (1 + num(i, 'wacc')) ** -num(i, 'life_years')) / (1 - (1 + num(i, 'wacc')) ** -1)
                              for i in range(9)])):     # v0.5.4: the data step of the scenario (section 3, A0)
        o[key] = [[v] * n for v in val]
    o['dlfr'] = [par['dlf_ren']] * n
    o['erf'] = [par['early_factor']] * n
    for i in range(9):                           # v0.5.4: renewable subsidy revenue by type (legacy rows 3665-3669)
        o['prrns'][i] = [rns[i][k] * o['gen'][i][k] * 8.76 for k in range(n)]
    o['dem'] = dem
    o['demg'] = {g: [sum(dem[s][k] for s in dem if GROUP_OF.get(s, 'ind') == g) for k in range(n)] for g in GROUPS}
    return o


def elasticities(income_group):
    el = {r['key']: float(r[income_group]) for r in read('elasticities.csv')}
    return {g: (el[f'inc|ecy|{g}'], el[f'usg|ecy|{g}'], el[f'eff|ecy|{g}'], el[f'aei|ecy|{g}']) for g in GROUPS}


def legacy_inputs(run):
    """Engine inputs from the cached legacy run ('base' or 'ctax'): exogenous paths, variable costs D4-D6 incl. the
    2041 value for the D9 window, historical prices before policy and VAT."""
    years = list(range(2022, 2041))
    ref = {r['key']: r for r in read('legacy_engineer_reference.csv') if r['run'] == run}
    iso = LEGACY_RUN['iso']
    val = lambda key, y: float(ref[key][str(y)])
    ser = lambda key: [val(key, y) for y in years]
    return {
        'iso': iso, 'elast': elasticities(INCOME[iso]), 'gdp': ser('gdp'), 'inc': ser('inc'), 'shock': ser('shock'), 'cpf': ser('cpf'),
        'rp2021_res': val('rp_res', 2021), 'rp2021_ind': val('rp_ind', 2021),
        'rphist_res': ser('rppre_res'), 'rphist_ind': ser('rppre_ind'),
        'vat_res': val('vat_res', 2024), 'vat_ind': val('vat_ind', 2024), 'last_hist': 2024,
        'vbc': [ser(f'vbc|{f}') for f in T], 'd5': [ser(f'd5|{f}') for f in T], 'd6': [ser(f'd6|{f}') for f in T],
        'txo_res': val('txo_res', 2024), 'txo_ind': val('txo_ind', 2024),     # v0.9.0 (Power_465): rows 3606, 3635
        'tvc_extra': [[val(f'tvc|{f}', 2041)] for f in T]}


def legacy_test(run, fix=ALL_FIXES, shock=True):
    """v0.9.0 (Power_465): legacy 465 has every fix of FIXES (the CPAT team fixed L1-L10, L67), so the test runs with
    ALL_FIXES (456: fix = frozenset()). Engine on the legacy inputs vs the cached legacy rows: [(max relative diff, key, year, legacy, engine)]."""
    years = list(range(2022, 2041))
    o = engine(legacy_inputs(run), years, fix=fix, shock=shock)
    out = []
    for r in read('legacy_engineer_reference.csv'):
        if r['run'] != run:
            continue
        key = r['key']
        name, f = (key.split('|') + [''])[:2]
        if name in ('gdp', 'inc', 'shock', 'cpf', 'vbc', 'd5', 'd6', 'cfp', 'df', 'vat_res', 'vat_ind', 'txo_res',
                    'txo_ind'):
            continue                                       # inputs
        if name == 'dem':
            got = o['dem'][f]
        elif f:
            got = o[name][T.index(f)]
        else:
            got = o[name]
        leg = [float(r[str(y)]) for y in years]
        if name in ('ores_res', 'ores_ind'):               # v0.9.0: the residual from the last historical year on
            leg = [a if y >= 2024 else b for a, b, y in zip(leg, got, years)]
        d, yr = max((abs(a - b) / max(1.0, abs(a)), y) for a, b, y in zip(leg, got, years))
        out.append((d, key, yr))
    return sorted(out, reverse=True)
