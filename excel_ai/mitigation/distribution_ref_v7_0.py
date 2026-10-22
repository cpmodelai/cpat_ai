"""v4.4: Python reference of the Distribution sheet (one scenario group, one analysis year), the independent check of
its formulas. Same chain and data as the sheet (data/legacy_*.csv, distn_catmap.csv); inputs from Mitigation are passed in.
python distribution_ref_v7_0.py  ->  runs it on legacy's cached Egypt inputs and compares with legacy's cached
outputs (legacy Distribution / MTOutputs, $50 carbon tax in 2030), listing the differences the bug fixes cause.
Units: price changes as fractions; budget shares and effects in % of consumption (loss negative); money in LCU."""
import csv, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
D = list(range(1, 11))
FUELS = ['coa', 'ely', 'nga', 'oil', 'gso', 'die', 'ker', 'lpg']          # household fuels (legacy order)
CATS = ['app', 'che', 'clo', 'com', 'edu', 'food', 'hea', 'hou', 'oth', 'pap', 'pha', 'ret', 'teq', 'tpu']
BIO = ['ccl', 'ethanol', 'fwd']
VAR = {'app': 'appliances', 'che': 'chemicals', 'clo': 'clothing', 'com': 'communications', 'edu': 'education',
       'food': 'food', 'hea': 'health_srv', 'hou': 'housing', 'oth': 'other', 'pap': 'paper', 'pha': 'pharma',
       'ret': 'rectourism', 'teq': 'transp_eqt', 'tpu': 'transp_pub'}
SAMPLES = {'ove': 'Overall', 'urb': 'Urban', 'rur': 'Rural'}
GROUPS = ['coa', 'ely', 'nga', 'oil', 'p_c']                 # IO fuel groups (Leontief rows)
GROUP_OF = {'coa': 'coa', 'ecy': 'ely', 'nga': 'nga', 'oop': 'oil', 'gso': 'p_c', 'die': 'p_c', 'lpg': 'p_c',
            'ker': 'p_c'}                                     # Mitigation fuel -> IO group (legacy C.I rows 549-556)
INFRA = {'All Infr.': 'all_acs_share', 'ICT Infr.': 'ICT_acs_share', 'Electricity Infr.': 'ely_acs_share',
         'Water Infr.': 'wtr_acs_share', 'Sanitation Infr.': 'sani_acs_share',
         'Public Transport Infr.': 'transp_pub_acs_share'}   # legacy Distribution rows 184-189


def table(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def num(x):
    return float(x) if x not in ('', None) else 0.0


def _hh_wide(name):
    """v4.5: legacy HHSurvey / HH_Elast (one row per sample, statistic and quantile; variables across) as
    {iso|sample|stat|variable: {'b': basket, '1'..'10': deciles}}."""
    out = {}
    for r in table(name):
        q = int(float(r['quant_cons']))
        for k, v in r.items():
            if k not in ('code', 'iso3', 'year', 'sample', 'type', 'stat_type', 'quant_cons'):
                out.setdefault(f"{r['iso3']}|{r['sample']}|{r['stat_type']}|{k}", {})['b' if q == 9999 else str(q)] = v
    return out


HH = {**_hh_wide('legacy_HHSurvey.csv'), **_hh_wide('legacy_HH_Elast.csv')}
IO = {}                                                   # v4.7: legacy IO_GTAP (series rows, sectors across)
for _r in table('legacy_IO_GTAP.csv'):
    _iso, _ser = _r['dis'].split('.', 1)
    for _k, _v in list(_r.items())[4:]:
        IO.setdefault(f'{_iso.upper()}|{_k}', {})[_ser.replace('.leontiefs', '')] = num(_v)
ASP = {r['Series_Code']: num(r['(firstnm) Value']) for r in table('legacy_ASPIRE.csv')}
CATMAP = {r['gtap']: r['item'] for r in table('distn_catmap.csv')}


def hh(iso, sample, stat, var, d):
    return num(HH[f'{iso}|{sample}|{stat}|{var}']['b' if d == 0 else str(d)])


def gini_weights():
    """Legacy C.IX: L(x) = a x^2 + b x fitted to the cumulative shares L_1..L_10 (x = 1..10, no intercept, LINEST);
    Gini = (n/2 - area under L over 0..n) / (n/2). The fit is linear in L, so Gini = 1 - sum_j s_j W_j with s_j the
    decile shares and W_j = sum_{d>=j} w_d / (n/2), w_d the area weight of L_d. Returns W_1..W_10 (Constants
    DGiniW)."""
    n = len(D)
    s2, s3, s4 = (sum(x ** k for x in D) for k in (2, 3, 4))
    det = s4 * s2 - s3 ** 2
    w = [(n ** 3 / 3 * (s2 * d * d - s3 * d) + n ** 2 / 2 * (s4 * d - s3 * d * d)) / det for d in D]
    return [sum(w[k:]) / (n / 2) for k in range(n)]


GINI_W = gini_weights()


def gini(x):
    return 1 - sum(a * b for a, b in zip(x, GINI_W)) / sum(x)


def io_tables(iso, defl_ratio):
    """Fuel totals T_f (USD m, ref-year prices; legacy rows 588-600) and the household-demand weighted Leontief
    coefficients of the 14 categories (legacy rows 668-736)."""
    sec = {k.split('|')[1]: v for k, v in IO.items() if k.startswith(iso + '|')}
    T = {f: defl_ratio * (sum((s['totd'] + s['exports']) * s[f] for k, s in sec.items() if k not in GROUPS)
                          + sec[f]['totd']) for f in GROUPS}
    lcat = {}
    for c in CATS:
        ss = [k for k, v in CATMAP.items() if v == c]
        hhd = sum(sec[s]['hhd'] for s in ss)
        lcat[c] = {f: sum(sec[s]['hhd'] * sec[s][f] for s in ss) / hhd for f in GROUPS}
    return T, lcat


def run(inp, iso='EGY', fix=True):
    """inp: dp_res (fuel -> fraction), dp_all and spend (Mitigation fuel -> fraction, USD m), defl_gtap (ratio),
    gdp_lcu, pop, rev_lcu (LCU), cons_gdp (%), settings (MTInputs names). fix=False keeps the legacy bugs that
    change Egypt's numbers (targeting cap, basket elasticity, compensation denominator) for the comparison."""
    s = inp['settings']
    stat = s['QuantilesStatistic']
    T, lcat = io_tables(iso, inp['defl_gtap'])
    R = {g: sum(inp['spend'][f] * inp['dp_all'][f] for f in GROUP_OF if GROUP_OF[f] == g) for g in GROUPS}
    E = {g: sum(inp['spend'][f] for f in GROUP_OF if GROUP_OF[f] == g) for g in GROUPS}
    gfac = {g: R[g] / T[g] if s['ScaleGTAP'] == 'Yes' else (R[g] / E[g] if E[g] else 0) for g in GROUPS}
    dp = dict(inp['dp_res'])
    dp.update({c: sum(lcat[c][g] * gfac[g] for g in GROUPS) for c in CATS})
    items = FUELS + CATS
    var = {i: VAR.get(i, i) for i in items + BIO}

    def ea(i, d):
        if s['PEDs'] != 'Yes':
            return 1.0
        e = hh(iso, 'Overall', 'mean', f'{var[i]}_elasticity', d if (d or fix) else 1)
        return (1 + dp[i]) ** e

    ex_fuel = s.get('exempt_fuel', '')
    def fac(i, d):                                            # price factor (fraction) incl. exemption
        f = dp[i] * ea(i, d)
        if s['ExemptMostCook'] == 'Yes' and i == ex_fuel and d <= float(s['ExemptCookDeciles']) and d > 0:
            f = 0.0
        return f

    bsh = {(sm, i, d): hh(iso, SAMPLES[sm], stat, f'{var[i]}_share', d) for sm in SAMPLES for i in items + BIO
           for d in [0] + D}
    uloss = {(sm, d): sum(fac(i, d) * bsh[(sm, i, d)] for i in items) for sm in SAMPLES for d in [0] + D}
    # rebasing (legacy C.VIII; the deflator ratios cancel)
    nacons = inp['gdp_lcu'] * inp['cons_gdp'] / 100
    popadj = inp['pop'] / hh(iso, 'Overall', 'mean', 'popw', 0)
    pop = {(sm, d): hh(iso, SAMPLES[sm], 'mean', 'popw', d) * popadj for sm in SAMPLES for d in [0] + D}
    cpc = {(sm, d): hh(iso, SAMPLES[sm], 'mean', 'cons_pc_acrent', d) * nacons
           / (hh(iso, 'Overall', 'mean', 'cons_pc_acrent', 0) * inp['pop']) for sm in SAMPLES for d in [0] + D}
    tcons = {k: cpc[k] * pop[k] for k in pop}
    rev_impl = sum(tcons[('ove', d)] * uloss[('ove', d)] / 100 for d in D)
    b = min(1, max(0, inp['rev_lcu'] / rev_impl)) if s['InferredDist'] == 'Yes' else 1.0
    scale = b + (0.5 * (1 - b) if s['DWLs'] == 'Yes' else 0)
    out = {}
    for i in items:
        out[('def' if i in FUELS else 'ief', i)] = [-fac(i, d) * bsh[('ove', i, d)] * scale for d in [0] + D]
    for i in items + BIO:
        out[('bsh', i)] = [bsh[('ove', i, d)] for d in [0] + D]
    out[('def', 'tot')] = [sum(out[('def', i)][k] for i in FUELS) for k in range(11)]
    out[('ief', 'tot')] = [sum(out[('ief', i)][k] for i in CATS) for k in range(11)]
    tef = {sm: [-uloss[(sm, d)] * scale for d in [0] + D] for sm in SAMPLES}
    # revenue recycling (per capita LCU; legacy C.X-C.XI)
    rev = inp['rev_lcu']
    rpit, rpui, rcts, rtgt = (rev * float(s[k]) / 100 for k in ('EXPLabortax', 'EXPCapex', 'EXPGoodsandserv',
                                                               'EXPTransfers'))
    popd = [pop[('ove', d)] for d in D]
    ptot = sum(popd)
    pitbase = inp['gdp_lcu'] * hh(iso, 'Overall', stat, 'indv', 1) / 100
    sh = [hh(iso, 'Overall', stat, 'pit_share_' + s['MissingDataReplacement'], d) for d in D]
    pitd = [pitbase * x / sum(sh) for x in sh]
    pitpc = [a / p for a, p in zip(pitd, popd)]
    mx = rpit / ptot
    extra = sum(max(mx - x, 0) * p for x, p in zip(pitpc, popd)) / ptot
    pa = [min(mx, x) + extra for x in pitpc]
    prop = [x * rpit / pitbase for x in pitpc]
    te, cum = [], 0
    for d, a, p in zip(D, pitd, popd):
        g_ = min(a, max(rpit - cum, 0)) if d <= float(s['DistExcCfDec']) else 0
        cum += a
        te.append(g_ / p)
    pit = {'Personal Allowance': pa, 'Proportional Compensation': prop}.get(s['PITReductionType'], te)
    share = [p / ptot for p in popd]
    pct, cov, leak = (float(s[k]) / 100 for k in ('TargettedPercentile', 'CoverageRate', 'LeakageRate'))
    recv, c0 = [], 0
    for k, x in enumerate(share):
        if fix:
            t = max(0, min(x, pct - c0))                      # targeted part of the decile (population share)
        elif k == 0:
            t = x if pct >= x else 0                          # legacy R2562: decile 1 all or nothing,
        else:
            t = min(pct - c0, 0.1) if pct >= c0 else 0        # later deciles capped at 10 points (bug)
        recv.append((t * cov + max(x - t, 0) * leak) / x if fix else (t * cov + (x - t) * leak) / x)
        c0 += x
    w = [1.0] * len(D)                                       # v6.0: weight of the decile (cash: 1)
    mode, code = 'Cash', s.get('tgt_code', 'Cash')
    if fix and code != 'Cash' and f'{iso}.{code}1_preT_tot' in ASP:   # ASPIRE incidence (fix D10, D11)
        mode, w = 'ASPIRE', [ASP.get(f'{iso}.{code}{math.ceil(d / 2)}_preT_tot', 0) for d in D]
    elif fix and code == 'Cash' and not str(s.get('TargetBelow', 'No')).startswith('No'):   # poverty line (D14, D15)
        var = 'pct_belowpl_' + str(s['TargetBelow']).replace('.', '')
        mode, w = 'PL', [min(10 * (hh(iso, 'Overall', 'mean', var, d) or 0), 100) / 100 for d in D]
    rshare = [r * (x if mode == 'PL' else 1) for r, x in zip(recv, w)]
    flag = [0 if fix and stat == 'median' and x <= 0.5 else 1 for x in rshare]   # median flag (fix D12, D13)
    den = sum(r * x * p for r, x, p in zip(recv, w, popd))
    amt = rtgt / den if den else 0
    tgt = [amt * r * x * f for r, x, f in zip(recv, w, flag)]
    acs = INFRA[s['PublicInfrastructureInvType']]
    noacc = {sm: [1 - hh(iso, SAMPLES[sm], 'mean', acs, d) / 100 for d in D] for sm in SAMPLES}
    pamt = rpui / sum(n * p for n, p in zip(noacc['ove'], popd))
    pui = {sm: [pamt * n for n in noacc[sm]] for sm in SAMPLES}
    prog = s['aspire_code']
    base = [ASP.get(f'{iso}.{prog}{math.ceil(d / 2)}_preT_tot', 0) for d in D]   # prog: per_<program>.avt_q
    den = sum(x * p for x, p in zip(base, popd))
    cts = [rcts * x / den if den else 0 for x in base]
    rec = {}
    for sm in SAMPLES:
        c = [cpc[(sm, d)] for d in D]
        parts = {'pit': pit, 'pui': pui[sm], 'cts': cts, 'tgt': tgt}
        for k, v in parts.items():
            rec[(k, sm)] = [a / b_ * 100 for a, b_ in zip(v, c)]
        rec[('rec', sm)] = [sum(rec[(k, sm)][j] for k in parts) for j in range(10)]
    for sm in SAMPLES:
        out[('tef', sm)] = tef[sm]
        net = [a + b_ for a, b_ in zip(tef[sm][1:], rec[('rec', sm)])]
        out[('net', sm)] = net
        for k in ('pit', 'pui', 'cts', 'tgt', 'rec'):
            out[(k, sm)] = rec[(k, sm)]
        c = [tcons[(sm, d)] for d in D]
        w = c if fix or sm == 'ove' else [tcons[('ove', d)] for d in D]
        loss = [-x for x in tef[sm][1:]]
        out[('pctrev_comp', sm)] = [l * x / sum(a * b_ for a, b_ in zip(loss, w)) * 100 for l, x in zip(loss, c)]
        g0 = gini(c)
        out[('pct_gini_norec', sm)] = (gini([x * (1 + t / 100) for x, t in zip(c, tef[sm][1:])]) / g0 - 1) * 100
        out[('pct_gini_rec', sm)] = (gini([x * (1 + t / 100) for x, t in zip(c, net)]) / g0 - 1) * 100
    out[('cons_pc_na', 'ove')] = [cpc[('ove', d)] for d in D]
    out[('tot_cons_na', 'ove')] = [tcons[('ove', d)] for d in D]
    out[('pop_tot_adj', 'ove')] = popd
    out['dp'] = dp
    out['gfac'] = gfac
    return out


LEGACY_INPUTS = {   # legacy Distribution cache (Egypt, 2030, $50 carbon tax): rows 771-778, 539-546, 528-535, I233-I249
    'dp_res': {'coa': .37812, 'ely': .254535, 'nga': .594393, 'oil': 1.03958, 'gso': .191707, 'die': .280679,
               'ker': .301018, 'lpg': .586722},
    'dp_all': {'coa': .554589, 'nga': .548977, 'oop': 1.03958, 'gso': .191707, 'die': .280679, 'lpg': .586722,
               'ker': .301018, 'ecy': .258634},
    'spend': {'coa': 748.223, 'nga': 8109.05, 'oop': 1879.22, 'gso': 5556.12, 'die': 8767.51, 'lpg': 1448.85,
              'ker': 3.79815, 'ecy': 17776.4},
    'defl_gtap': 234.718325 / 41.125541 * 1000 / 1000,
    'gdp_lcu': 3.79706e13, 'pop': 1.20298263e8, 'rev_lcu': 6.84024e11, 'cons_gdp': 82.5718,
    'settings': {'QuantilesStatistic': 'mean', 'ScaleGTAP': 'Yes', 'PEDs': 'Yes', 'InferredDist': 'No', 'DWLs': 'No',
                 'ExemptMostCook': 'No', 'ExemptCookDeciles': 4, 'EXPLabortax': 30, 'EXPCapex': 50,
                 'EXPGoodsandserv': 0, 'EXPTransfers': 20, 'TargettedPercentile': 40, 'CoverageRate': 100,
                 'LeakageRate': 0, 'PITReductionType': 'Personal Allowance', 'DistExcCfDec': 4,
                 'MissingDataReplacement': 'income', 'PublicInfrastructureInvType': 'All Infr.',
                 'aspire_code': 'per_allsp.avt_q'}}

LEGACY_OUT = {   # legacy cache, deciles 1-10 (D.II rows; legacy_distribution_spec.md sections 5-9)
    ('tef', 'ove'): [-2.599, -2.395, -2.302, -2.147, -2.169, -2.155, -2.208, -2.223, -2.138, -2.195],
    ('rec', 'ove'): [10.657, 7.590, 4.602, 4.076, 2.798, 1.691, 1.134, 0.876, 1.001, 0.419],
    ('net', 'ove'): [8.058, 5.195, 2.299, 1.929, 0.629, -0.464, -1.075, -1.346, -1.136, -1.776],
    ('pctrev_comp', 'ove'): [4.710, 5.434, 7.337, 7.336, 7.973, 9.260, 11.074, 13.387, 14.080, 19.411],
    ('pct_gini_norec', 'ove'): 0.128379, ('pct_gini_rec', 'ove'): -4.71179,
    ('pct_gini_norec', 'urb'): 0.0146884, ('pct_gini_rec', 'urb'): -2.73272,
    ('pct_gini_norec', 'rur'): 0.0264184, ('pct_gini_rec', 'rur'): -5.40479,
}


def compare(out, ref, tol):
    worst = 0
    for k, v in ref.items():
        a = out[k]
        a, v = (a, v) if isinstance(v, list) else ([a], [v])
        a = a[1:] if len(a) == 11 else a
        d = max(abs(x - y) / max(abs(y), 1e-9) for x, y in zip(a, v))
        worst = max(worst, d)
        print(f'  {k}: max rel diff {d:.2e}' + ('' if d < tol else '  <--'))
    return worst


if __name__ == '__main__':
    print('legacy bugs kept (fix=False) vs legacy cache:')
    w = compare(run(LEGACY_INPUTS, fix=False), LEGACY_OUT, 2e-3)
    print(f'worst {w:.2e} (legacy values cached to 4-6 digits)')
    a, b = run(LEGACY_INPUTS, fix=False), run(LEGACY_INPUTS)
    print('effect of the bug fixes (fix=True minus legacy):')
    for k in [('tef', 'ove'), ('rec', 'ove'), ('tgt', 'ove'), ('pctrev_comp', 'urb'), ('pct_gini_rec', 'ove')]:
        x, y = a[k], b[k]
        print(f'  {k}:', [round(q - p, 4) for p, q in zip(x, y)] if isinstance(x, list) else round(y - x, 5))
