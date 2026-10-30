"""The household incidence of a scenario in the analysis year: Excel-AI's distribution module (CPAT-AI-Distribution-
Prototype 0.1.4, sheet Distribution), section by section.

One scenario group at a time: the scenario's mitigation results against scenario 1's (the baseline) in the analysis
year YearDistn. Every row has 11 columns: 0 the basket (whole sample), 1-10 the deciles. Rows are keyed by Excel-AI's
(variable, item, sample); `run` returns them by output code (`<iso>.distn.<...>.<n>`, core/excel_ai/distribution_rows.csv).

    0-1   settings: the distribution inputs of the scenario and the recycling choices they select
    2     inputs from mitigation (section 19a): price changes, base-year spending, GDP, population, new revenue
    3     indirect price changes of the consumption categories through the GTAP input-output table
    4-6   price factors (elasticity adjustment, cooking-fuel exemption), budget shares, direct and indirect effects
    7     survey to national accounts: population and consumption scaled to WEO/WDI totals
    8     revenue recycling: personal income tax cut, public investment, current spending, targeted transfers
    9     net effect, compensation, Gini; 10 outputs for charts; 11 price changes by production sector
"""
import csv
from functools import lru_cache
from pathlib import Path

import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.distribution import mapping
from cpat_model.mitigation.power_data import PJ_PER_KTOE

ROWS = Path(__file__).resolve().parents[1] / 'core' / 'excel_ai' / 'distribution_rows.csv'
D = np.arange(11)                                       # column: 0 basket, 1-10 deciles
DEC = slice(1, 11)
SAMPLES = ['ove', 'urb', 'rur']
FUELS = ['coa', 'ely', 'nga', 'oil', 'gso', 'die', 'ker', 'lpg']        # household fuels (Excel-AI order)
CATS = mapping.CATEGORIES
BIO = ['ccl', 'ethanol', 'fwd']
ITEMS = FUELS + CATS                                    # rows fac, eps; budget shares coa ... tpu
SURVEY_VAR = {'app': 'appliances', 'che': 'chemicals', 'clo': 'clothing', 'com': 'communications', 'edu': 'education',
              'food': 'food', 'hea': 'health_srv', 'hou': 'housing', 'oth': 'other', 'pap': 'paper', 'pha': 'pharma',
              'ret': 'rectourism', 'teq': 'transp_eqt', 'tpu': 'transp_pub'}
DPR = {'coa': ('atp', 'res', 'coa'), 'ely': ('rp', 'res', 'ecy'), 'nga': ('atp', 'res', 'nga'),
       'oop': ('atp', 'res', 'oop'), 'gso': ('atp', 'res', 'gso'), 'die': ('atp', 'res', 'die'),
       'ker': ('atp', 'res', 'ker'), 'lpg': ('atp', 'res', 'lpg')}       # rows dpr.<f>.res: Mitigation row read
DPR_OF = {'coa': 'coa', 'ely': 'ely', 'nga': 'nga', 'oil': 'oop', 'gso': 'gso', 'die': 'die', 'ker': 'ker', 'lpg': 'lpg'}
DPA = [('coa', 'coa', ('rpn', 'ind', 'coa')), ('nga', 'nga', ('rpn', 'ind', 'nga')), ('oop', 'oil', ('rpn', 'all', 'oop')),
       ('gso', 'p_c', ('rpn', 'all', 'gso')), ('die', 'p_c', ('rpn', 'all', 'die')), ('lpg', 'p_c', ('rpn', 'all', 'lpg')),
       ('ker', 'p_c', ('rpn', 'all', 'ker')), ('ecy', 'ely', ('rp', 'ind', 'ecy'))]   # rows dpa, spend: fuel, IO group
CPAT_SECTORS = ['avi', 'nav', 'foo', 'srv', 'mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr', 'res', 'pow']
RANKS = 20


@lru_cache(maxsize=1)
def codes():
    """{(variable, item, sample): output code without the scenario}."""
    with open(ROWS, encoding='utf-8') as f:
        return {(r['variable'], r['item'], r['sample']): r['code'] for r in csv.DictReader(f)}


def yes(x):
    return str(x)[:3] == 'Yes'


class Sheet:
    """The rows of one scenario group: put(variable, item, sample, value): a number or text for every column, or 11
    values; get(...) returns the 11 values."""

    def __init__(self):
        self.rows = {}

    def put(self, var, value, item='', sample='', deciles_only=False):
        if isinstance(value, str):
            a = np.array([value] * 11, dtype=object)
        elif getattr(value, 'dtype', None) == object:
            a = np.array(value, dtype=object)
        else:
            a = np.array(np.broadcast_to(np.asarray(value, dtype=float), 11), dtype=float)
        if deciles_only:
            a = a.copy()
            a[0] = np.nan
        self.rows[(var, item, sample)] = a
        return a

    def get(self, var, item='', sample=''):
        return self.rows[(var, item, sample)]


def group(data, inputs, scenario, baseline, years, base_year, iso):
    """One scenario group of the Distribution sheet. scenario, baseline: functions (variable, sector, fuel, year) ->
    the mitigation value of the scenario and of scenario 1 (section 19a rows)."""
    c = xt.constant
    pct, pj = c('PctPerUnit'), PJ_PER_KTOE
    S = Sheet()
    hh, hh_row = data['survey']
    el, _ = data['elasticities']
    prog, asp = data['programmes'], data['aspire']
    year = int(inputs['YearDistn'])
    stat = str(inputs['QuantilesStatistic'])
    svyb = ['bkt.' if d == 0 else 'dec.' for d in D]
    svyq = ['.' + str(int(c('BasketQ')) if d == 0 else d) for d in D]

    def survey(prefix, var, sample_stat):
        """HHSurvey value of every column: key <iso>.distn.bsh.<bkt|dec>.<sample.stat>.<quantile>."""
        return np.array([mapping.number(hh.get(f'{iso}.distn.bsh.{svyb[d]}{sample_stat}{svyq[d]}', {}).get(var))
                         for d in D])

    # 1 settings
    for name in ('YearDistn', 'QuantilesStatistic', 'PEDs', 'ScaleGTAP', 'InferredDist', 'DWLs', 'ExemptMostCook',
                 'ExemptCookDeciles', 'EXPLabortax', 'EXPCapex', 'EXPGoodsandserv', 'EXPTransfers', 'PITReductionType',
                 'DistExcCfDec', 'MissingDataReplacement', 'TransferType', 'TargetBelow', 'TargettedPercentile',
                 'CoverageRate', 'LeakageRate', 'PublicInfrastructureInvType', 'CurrentSpendingType', 'PassthroughDist',
                 'QuantilesLCU'):
        v = inputs[name]
        S.put(name, v if isinstance(v, str) else float(v))
    acsvar = S.put('acsvar', prog[f"infra|{inputs['PublicInfrastructureInvType']}"])[0]
    aspcode = S.put('aspcode', prog[f"aspire|{inputs['CurrentSpendingType']}"])[0]
    exfuel = S.put('exfuel', data['cooking_fuel'])[0]
    exdec = S.put('exdec', np.where(yes(inputs['ExemptMostCook']) & (D > 0) & (D <= inputs['ExemptCookDeciles']), 1.0, 0))
    tgtcode = S.put('tgtcode', prog.get(f"aspire|{inputs['TransferType']}", 'Cash'))[0]
    tgtdata = S.put('tgtdata', 1.0 if f'{iso}.{tgtcode}1_preT_tot' in asp else 0.0)[0]
    below = str(inputs['TargetBelow'])
    plvar = S.put('plvar', 'popw' if below[:2] == 'No' else 'pct_belowpl_' + below.replace('.', ''))[0]
    tgtmode = S.put('tgtmode', ('ASPIRE' if tgtdata == 1 else 'Cash') if tgtcode != 'Cash' else
                    ('Cash' if plvar == 'popw' else 'PL'))[0]
    S.put('support', 'TransferType: no ASPIRE data, cash used' if tgtcode != 'Cash' and tgtdata == 0 else 'OK')

    # 2 inputs from mitigation (EQ-D1.3)
    change = lambda v, s, f: scenario(v, s, f, year) / baseline(v, s, f, year) - 1
    for f, (v, s, ff) in DPR.items():
        S.put('dpr', change(v, s, ff), f'{f}.res')
    dpa, spend = {}, {}
    for f, g, (v, s, ff) in DPA:
        dpa[f] = S.put('dpa', change(v, s, ff), f)
        sp = baseline('pav.sp', 'all', 'coa' if f == 'coa' else f, base_year)
        spend[f] = S.put('spend', sp * (1.0 if f == 'ecy' else pj), f)
    gdp = S.put('gdp', scenario('gdp.lcu', 'all', 'all', year) * c('Billion'))
    pop = S.put('pop', scenario('pop', 'all', 'all', year) * c('Thousand'))
    rev = S.put('rev', scenario('rnew', 'all', 'all', year) * c('Million') * scenario('xr', 'all', 'all', year))

    # 3 indirect price changes of consumption categories (EQ-D1.2)
    gfac = {}
    for g in mapping.GROUPS:
        fuels = [f for f, gg, _ in DPA if gg == g]
        grev = S.put('grev', sum(spend[f] * dpa[f] for f in fuels), g)
        gspend = S.put('gspend', sum(spend[f] for f in fuels), g)
        gtot = S.put('gtot', data['group_use'][g], g)
        gfac[g] = S.put('gfac', grev / gtot if yes(inputs['ScaleGTAP']) else np.where(gspend > 0, grev / np.where(
            gspend > 0, gspend, 1), 0.0), g)
    gfac_v = np.stack([gfac[g] for g in mapping.GROUPS])                          # (group, column)
    for cat in CATS:
        S.put('dpr', data['category_leontief'][cat] @ gfac_v, cat)

    # 5 budget shares (before 4: the price factors weight by them) (EQ-D1.1)
    for s in SAMPLES:
        items = ITEMS + (BIO if s == 'ove' else [])
        for it in items:
            S.put('bsh', survey('bsh', f'{SURVEY_VAR.get(it, it)}_share', f'{s}.{stat}'), it, s)
    S.put('bsh', sum(S.get('bsh', f, 'ove') for f in FUELS) + sum(S.get('bsh', b, 'ove') for b in BIO), 'ene', 'ove')
    bsh_cats = np.stack([S.get('bsh', cat, 'ove') for cat in CATS])
    S.put('dprw', _safe(np.sum(np.stack([S.get('dpr', cat) for cat in CATS]) * bsh_cats, axis=0), bsh_cats.sum(axis=0)),
          'cat', 'ove')

    # 4 price factors (EQ-D1.4, EQ-B1.4)
    for it in ITEMS:
        S.put('eps', np.array([mapping.number(el.get(f'{iso}.distn.{svyb[d]}ove.mean{svyq[d]}', {}).get(
            f'{SURVEY_VAR.get(it, it)}_elasticity')) for d in D]), it)
    fac = {}
    for it in ITEMS:
        dp = S.get('dpr', f'{DPR_OF[it]}.res') if it in FUELS else S.get('dpr', it)
        f = dp * (np.power(1 + dp, S.get('eps', it)) if yes(inputs['PEDs']) else 1.0)
        if it in FUELS:
            f = np.where((exdec == 1) & (exfuel == it), 0.0, f)
        fac[it] = S.put('fac', f, it)
    bsh_f = np.stack([S.get('bsh', f, 'ove') for f in FUELS])
    S.put('facw', _safe(np.sum(np.stack([fac[f] for f in FUELS]) * bsh_f, axis=0), bsh_f.sum(axis=0)), 'ene', 'ove')

    # 7 survey to national accounts (6 needs tot_cons_na) (EQ-B1.2)
    consyr = data['cons_ratio'][0]
    S.put('consgdpyr', float(consyr))
    consgdp = S.put('consgdp', data['cons_ratio'][1])
    nacons = S.put('nacons', gdp * consgdp / pct)
    popw = {s: S.put('popw', survey('bsh', 'popw', f'{s}.mean'), '', s) for s in SAMPLES}
    cpc = {s: S.put('cons_pc_svy', survey('bsh', 'cons_pc_acrent', f'{s}.mean'), '', s) for s in SAMPLES}
    popadj = S.put('popadj', pop[0] / popw['ove'][0])
    consadj = S.put('consadj', nacons[0] / cpc['ove'][0] / pop[0])
    popn = {s: S.put('pop_tot_adj', popw[s] * popadj, '', s) for s in SAMPLES}
    cpc_na = {s: S.put('cons_pc_na', cpc[s] * consadj, '', s) for s in SAMPLES}
    cons = {s: S.put('tot_cons_na', cpc_na[s] * popn[s], '', s) for s in ('urb', 'rur', 'ove')}

    # 6 price effects (EQ-D1.4, EQ-B1.3)
    fac_all = np.stack([fac[it] for it in ITEMS])
    uloss = {s: S.put('uloss', np.sum(fac_all * np.stack([S.get('bsh', it, s) for it in ITEMS]), axis=0), '', s)
             for s in SAMPLES}
    revimpl = S.put('revimpl', np.sum(uloss['ove'][DEC] * cons['ove'][DEC]) / pct)[0]
    badj = S.put('badj', min(1, max(0, rev[0] / revimpl)) if yes(inputs['InferredDist']) else 1.0)[0]
    lscale = S.put('lscale', badj + (c('DWLTri') * (1 - badj) if yes(inputs['DWLs']) else 0.0))[0]

    def effects(s):
        for f in FUELS:
            S.put('def', -fac[f] * S.get('bsh', f, s) * lscale, f, s)
        dtot = S.put('def', sum(S.get('def', f, s) for f in FUELS), 'tot', s)
        for cat in CATS:
            S.put('ief', -fac[cat] * S.get('bsh', cat, s) * lscale, cat, s)
        itot = S.put('ief', sum(S.get('ief', cat, s) for cat in CATS), 'tot', s)
        return dtot, itot
    dtot, itot = effects('ove')
    tef = {s: S.put('tef', -uloss[s] * lscale, 'tot', s) for s in ('urb', 'rur')}
    tef['ove'] = S.put('tef', dtot + itot, 'tot', 'ove')

    # 8 revenue recycling (EQ-B1.5, EQ-D1.5, EQ-B1.6)
    rpit, rpui, rcts, rtgt = (S.put(n, rev * float(inputs[k]) / pct)[0] for n, k in (
        ('rpit', 'EXPLabortax'), ('rpui', 'EXPCapex'), ('rcts', 'EXPGoodsandserv'), ('rtgt', 'EXPTransfers')))
    poptot = S.put('poptot', np.sum(popn['ove'][DEC]))[0]
    pitind = S.put('pitind', mapping.number(hh[f'{iso}.distn.bsh.dec.ove.{stat}.1'].get('indv')))[0]
    pitbase = S.put('pitbase', gdp * pitind / pct)[0]
    pitvar = S.put('pitvar', f"pit_share_{inputs['MissingDataReplacement']}")[0]
    pitsh = S.put('pitsh', survey('bsh', pitvar, f'ove.{stat}'), '', 'ove', deciles_only=True)
    pitshtot = S.put('pitshtot', np.sum(pitsh[DEC]))[0]
    pn = popn['ove']
    pitpc = S.put('pitpc', pitbase * pitsh / pitshtot / pn, '', 'ove', deciles_only=True)
    pitmax = S.put('pitmax', rpit / poptot)[0]
    pitgap = S.put('pitgap', np.maximum(pitmax - pitpc, 0), '', 'ove', deciles_only=True)
    pitextra = S.put('pitextra', np.sum(pitgap[DEC] * pn[DEC]) / poptot)[0]
    pitpa = S.put('pitpa', np.minimum(pitmax, pitpc) + pitextra, '', 'ove', deciles_only=True)
    pitprop = S.put('pitprop', pitpc * rpit / pitbase, '', 'ove', deciles_only=True)
    cum = np.concatenate([[0.0], np.cumsum(pitpc[DEC] * pn[DEC])])
    pitcum = S.put('pitcum', cum, '', 'ove', deciles_only=True)
    prev = np.concatenate([[0.0], cum[:-1]])                     # pitcum of the column to the left
    pitte = S.put('pitte', np.where(D <= inputs['DistExcCfDec'], np.minimum(pitpc, np.maximum(rpit - prev, 0) / pn), 0.0),
                  '', 'ove', deciles_only=True)
    method = inputs['PITReductionType']
    pit = S.put('pit', pitpa if method == 'Personal Allowance' else pitprop if method == 'Proportional Compensation'
                else pitte, '', 'ove', deciles_only=True)
    popsh = S.put('popsh', pn / poptot, '', 'ove', deciles_only=True)
    popcum = S.put('popcum', np.concatenate([[np.nan], np.cumsum(popsh[DEC])]), '', 'ove', deciles_only=True)
    tgtsh = S.put('tgtsh', np.maximum(0, np.minimum(popsh, inputs['TargettedPercentile'] / pct - popcum + popsh)),
                  '', 'ove', deciles_only=True)
    recv = S.put('recv', (tgtsh * inputs['CoverageRate'] + (popsh - tgtsh) * inputs['LeakageRate']) / pct / popsh,
                 '', 'ove', deciles_only=True)
    aspq = S.put('aspq', np.ceil(D / c('DecPerQuint')), '', 'ove', deciles_only=True)
    aspv = lambda code: np.array([np.nan] + [asp.get(f'{iso}.{code}{int(q)}_preT_tot', 0.0) for q in aspq[DEC]])
    aspt = S.put('aspt', aspv(tgtcode), '', 'ove', deciles_only=True)
    plraw = S.put('plraw', survey('bsh', plvar, 'ove.mean'), '', 'ove', deciles_only=True)
    plsh = S.put('plsh', np.minimum(c('PlDecScale') * plraw, pct) / pct if tgtmode == 'PL' else 1.0, '', 'ove',
                 deciles_only=True)
    tgtw = S.put('tgtw', aspt if tgtmode == 'ASPIRE' else plsh, '', 'ove', deciles_only=True)
    rshare = S.put('rshare', recv * plsh, '', 'ove', deciles_only=True)
    medflag = S.put('medflag', np.where((stat == 'median') & (rshare <= 1 - rshare), 0.0, 1.0), '', 'ove',
                    deciles_only=True)
    den = np.sum(recv[DEC] * tgtw[DEC] * pn[DEC])
    tgtamt = S.put('tgtamt', rtgt / den if den else 0.0)[0]
    tgt = S.put('tgt', tgtamt * recv * tgtw * medflag, '', 'ove', deciles_only=True)
    noacc = {}
    for s in SAMPLES:
        acs = S.put('acs', survey('bsh', acsvar, f'{s}.mean'), '', s, deciles_only=True)
        noacc[s] = S.put('noacc', 1 - acs / pct, '', s, deciles_only=True)
    den = np.sum(noacc['ove'][DEC] * pn[DEC])
    puiamt = S.put('puiamt', rpui / den if den else 0.0)[0]
    pui = {s: S.put('pui', puiamt * noacc[s], '', s, deciles_only=True) for s in SAMPLES}
    aspbase = S.put('aspbase', aspv(aspcode), '', 'ove', deciles_only=True)
    den = np.sum(aspbase[DEC] * pn[DEC])
    ctsamt = S.put('ctsamt', rcts / den if den else 0.0)[0]
    cts = S.put('cts', ctsamt * aspbase, '', 'ove', deciles_only=True)
    rec = {}
    for s in ('urb', 'rur', 'ove'):
        parts = [S.put(n, v / cpc_na[s] * pct, 'tot', s, deciles_only=True)
                 for n, v in (('pit', pit), ('pui', pui[s]), ('cts', cts), ('tgt', tgt))]
        rec[s] = S.put('rec', sum(parts), 'tot', s, deciles_only=True)

    # 9 net effect, compensation, inequality (EQ-D1.6, EQ-B1.7)
    W = np.array(mapping.gini_weights())
    gini = lambda x: 1 - np.sum(x[DEC] * W) / np.sum(x[DEC])
    net = {}
    for s in SAMPLES:
        net[s] = tef[s] + rec[s]
    for s in SAMPLES:
        compden = S.put('compden', np.sum(tef[s][DEC] * cons[s][DEC]), '', s)[0]
        S.put('pctrev_comp', 0.0 if compden == 0 else tef[s] * cons[s] / compden * pct, '', s, deciles_only=True)
    g = {}
    for s in SAMPLES:
        postx = S.put('postx', cons[s] * (1 + tef[s] / pct), '', s, deciles_only=True)
        posti = S.put('posti', cons[s] * (1 + net[s] / pct), '', s, deciles_only=True)
        g[s] = [S.put(n, gini(x), '', s)[0] for n, x in (('gini.g0', cons[s]), ('gini.gx', postx), ('gini.gi', posti))]
    for s in SAMPLES:
        S.put('pct_gini_norec', (g[s][1] / g[s][0] - 1) * pct, '', s)
        S.put('pct_gini_rec', (g[s][2] / g[s][0] - 1) * pct, '', s)
    for s in ('urb', 'rur', 'ove'):
        S.put('net', net[s], 'tot', s, deciles_only=True)

    # 10 outputs for charts
    S.put('dname', np.array(['Poorest' if d == 1 else 'Wealthiest' if d == 10 else f'Decile {d}' for d in D],
                            dtype=object), deciles_only=True)
    hhbk = S.put('hhbk', float(hh_row[f'{iso}.distn.bsh.dec.ove.mean.1']))[0]
    book = list(hh)[int(hhbk) - 1]
    for p in ('p1', 'p99'):
        S.put('dbr', np.array([np.nan] + [mapping.number(hh[book].get(f'dec_{d}_{p}')) * consadj[0] for d in D[1:]]),
              p, deciles_only=True)
    if yes(inputs['QuantilesLCU']):
        raise NotImplementedError('QuantilesLCU = Yes (decile labels in local currency) is not in Coded CPAT yet')
    S.put('dlab', S.get('dname'), deciles_only=True)
    S.put('bshg', sum(S.get('bsh', f, 'ove') for f in FUELS), 'fos', 'ove')
    S.put('bshg', sum(S.get('bsh', b, 'ove') for b in BIO), 'bio', 'ove')
    S.put('bshg', sum(S.get('bsh', cat, 'ove') for cat in CATS), 'nfu', 'ove')
    effects('urb')
    effects('rur')
    for it in ITEMS + BIO:
        S.put('abud', cpc_na['ove'] * S.get('bsh', it, 'ove') / pct, it, 'ove')
    for f in FUELS:
        S.put('adef', cpc_na['ove'] * S.get('def', f, 'ove') / pct, f, 'ove')
    for cat in CATS:
        S.put('aief', cpc_na['ove'] * S.get('ief', cat, 'ove') / pct, cat, 'ove')
    for s in SAMPLES:
        S.put('adef', cpc_na[s] * S.get('def', 'tot', s) / pct, 'tot', s)
        S.put('aief', cpc_na[s] * S.get('ief', 'tot', s) / pct, 'tot', s)
        S.put('atef', cpc_na[s] * tef[s] / pct, 'tot', s)
        S.put('anet', cpc_na[s] * net[s] / pct, 'tot', s, deciles_only=True)
    for s in SAMPLES:
        for n, x in (('lzp', popn[s]), ('lz0', cons[s]), ('lzx', S.get('postx', '', s)), ('lzi', S.get('posti', '', s))):
            S.put(n, np.concatenate([[np.nan], np.cumsum(x[DEC]) / np.sum(x[DEC]) * pct]), '', s, deciles_only=True)
    for s in SAMPLES:
        S.put('ccomp', np.concatenate([[np.nan], np.cumsum(S.get('pctrev_comp', '', s)[DEC])]), '', s, deciles_only=True)
    for s in SAMPLES:
        for p in ('p25', 'p75'):
            rows = [f'{iso}.distn.bsh.{svyb[d]}{s}.{p}{svyq[d]}' for d in D]
            S.put('hrow', np.array([np.nan] + [float(hh_row[r]) for r in rows[1:]]), p, s, deciles_only=True)
            share = lambda it, d: mapping.number(hh[rows[d]].get(f'{SURVEY_VAR.get(it, it)}_share'))
            htef = S.put('htef', np.array([np.nan] + [-sum(fac[it][d] * share(it, d) for it in ITEMS) * lscale
                                                      for d in D[1:]]), p, s, deciles_only=True)
            hcpc = S.put('hcpc', np.array([np.nan] + [mapping.number(hh[rows[d]].get('cons_pc_acrent')) * consadj[0]
                                                      for d in D[1:]]), p, s, deciles_only=True)
            # public investment per person, in local currency as the other three (bug M22, fixed in 0.1.4)
            hrec = S.put('hrec', (pit + pui[s] + cts + tgt) / hcpc * pct, p, s, deciles_only=True)
            S.put('hnet', htef + hrec, p, s, deciles_only=True)
    for s in ('urb', 'rur', 'ove'):
        S.put('gini.ptx', g[s][1] - g[s][0], '', s)
        S.put('gini.pti', g[s][2] - g[s][0], '', s)

    # 11 price changes by production sector (EQ-B1.8)
    sectors, table = data['sectors'], data['table']
    dps = np.where(data['fuel'] == 1, 0.0, data['leontief'] @ gfac_v[:, 0])
    pt = data['passthrough']
    dpsp = dps * np.array([pt.get(table[s][1], 1.0) if yes(inputs['PassthroughDist']) else 1.0 for s in sectors])
    for i, s in enumerate(sectors):
        S.put('dps', dps[i], s)
        S.put('dpsp', dpsp[i], s)
    rank = np.array([1 + np.sum(dpsp > v) + np.sum(dpsp[:i] == v) for i, v in enumerate(dpsp)])   # RANK + earlier ties
    for i, s in enumerate(sectors):
        S.put('dprk', float(rank[i]), s)
    for r in range(1, RANKS + 1):
        i = int(np.where(rank == r)[0][0])
        S.put('rks', sectors[i], f'r{r}')
        S.put('rkn', table[sectors[i]][2], f'r{r}')
        S.put('rkp', dpsp[i], f'r{r}')
    cpat = np.array([table[s][1] for s in sectors])
    hhd, out = data['hhd'], data['output']
    for cs in CPAT_SECTORS:
        m = cpat == cs
        S.put('secshh', _ratio(np.sum(hhd[m]), np.sum(hhd)), cs)
        S.put('secsout', _ratio(np.sum(out[m]), np.sum(out)), cs)
        S.put('ppici', _ratio(np.sum(out[m] * dps[m]), np.sum(out[m])), cs)
        S.put('ppic', _ratio(np.sum(out[m] * dpsp[m]), np.sum(out[m])), cs)
        S.put('outpriin', _ratio(np.sum(hhd[m] * dpsp[m]), np.sum(hhd[m])), cs)
    S.put('ppic', _ratio(np.sum(out * dpsp), np.sum(out)), 'all')
    return S


def _safe(a, b):
    """IFERROR(a / b, 0)."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b != 0, a / np.where(b != 0, b, 1), 0.0)


def _ratio(a, b):
    return a / b if b else 0.0


def country_data(db, iso, results_year):
    """The data of the distribution module for one country (mapping)."""
    d = mapping.country_data(db, iso, results_year)
    d['survey'] = mapping.survey(db, 'hh_survey')
    d['elasticities'] = mapping.survey(db, 'hh_elasticities')
    d['programmes'] = mapping.programmes(db)
    d['aspire'] = mapping.aspire(db)
    d['passthrough'] = mapping.passthrough(db)
    who = db.table('who_cooking')
    fuel = who.loc[who['code'] == f'{iso}.distn.pcoff.ove', 'main_fuel']
    d['cooking_fuel'] = fuel.iloc[0] if len(fuel) else ''
    gr = db.table('gdp_ratios')
    gr = gr[(gr['country'] == iso) & (gr['indicator'] == 'NE.CON.PRVT.ZS')]
    latest = int(gr['latest_year'].iloc[0])
    d['cons_ratio'] = (latest, float(gr.loc[gr['year'].astype(int) == latest, 'value'].iloc[0]))
    return d


@lru_cache(maxsize=8)
def _country_data(db, iso, results_year):
    return country_data(db, iso, results_year)


def run(results, db, settings, scenarios):
    """Every scenario group against scenario 1 for each country: {country: {code: 11 values}}."""
    out = {}
    base = results.states[1]
    for iso in settings.countries:
        data = _country_data(db, iso, settings.results_year)
        rows = {}
        for n, state in results.states.items():
            value = _reader(state, iso)
            sheet = group(data, scenarios.inputs(n), value, _reader(base, iso), settings.years, settings.base_year, iso)
            for (var, item, sample), a in sheet.rows.items():
                code = codes().get((var, item, sample))
                if code:
                    rows[f'{code.replace("egy.", iso.lower() + ".", 1)}.{n}'] = a
        out[iso] = rows
    return out


def _reader(state, iso):
    """(variable, sector, fuel, year) -> the mitigation value of the state."""
    def value(var, sector, fuel, year):
        a = state[var]
        if 'sector' in a.dims:
            a = a.sel(sector=sector, fuel=fuel)
        return float(a.sel(country=iso, year=year))
    return value
