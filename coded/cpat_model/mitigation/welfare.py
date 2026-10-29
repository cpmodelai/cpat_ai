"""Welfare and externalities (Mitigation section 18), one year at a time.

    climate     damages at the social cost of carbon and their change against the baseline (EQ-A8.5)
    efficiency  deadweight loss of the change in fuel use at the average wedge between price and supply cost, the
                methane fee's abatement cost, the environmental gain of the change in fossil fuel use (EQ-A8.5)
    welfare     the welfare gain in USD bn and in % of GDP: climate, air pollution, road transport, efficiency (EQ-A8.5)
    subsidies   explicit and implicit fossil fuel subsidies by price row: supply cost, externalities, VAT on both (the
                efficient price) against the retail price (EQ-A8.6)
    efficient   the efficient price by price code: supply cost of the baseline, Pigouvian taxes (air pollution, climate,
                road transport), VAT; the tax gap, the Pigouvian tax per tonne of CO2 (EQ-A8.6)
Rows are named as Excel-AI's (variable, sector, fuel as core/variables.csv); "oth" rows are the averages of the rows
above them weighted by use (con), the plain average where the use is 0.
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import safe_div
from cpat_model.mitigation import pigouvian
from cpat_model.mitigation.gdp import year_rows
from cpat_model.mitigation.power_data import PJ_PER_KTOE
from cpat_model.mitigation.totals import reference

WDG_FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'jfu', 'oop', 'bio']
WDG_POWER = {'coa', 'nga', 'oop', 'bio'}                       # fuel taxes of power generation (rfg) added
CH4_SOURCES = ['og', 'dg', 'cm', 'bm', 'liv', 'ric', 'wst']
CC_FUELS = ['coa', 'nga', 'oop', 'gso', 'die', 'lpg', 'ker']
OILS = ['gso', 'die', 'lpg', 'ker']
# subsidy rows (supcost ... impsub): (sector, fuel); 'oth' rows average the rows of the fuel above them
SUB_ROWS = [('all', f) for f in OILS + ['oop']] + [(s, f) for f in ('nga', 'coa') for s in ('ind', 'res', 'pow', 'oth')] \
    + [('ind', 'ecy'), ('res', 'ecy'), ('oth', 'ecy')]
# efficient price rows (sup.cost ... tgap)
EFF_ROWS = [('all', f) for f in OILS] + [(s, f) for f in ('coa', 'nga') for s in ('ind', 'res', 'pow')] \
    + [('ind', 'ecy'), ('res', 'ecy')]
FFS_COST = [('ind', 'coa', 'coa', 'gj.ind.coa'), ('res', 'coa', 'coa', 'gj.res.coa'), ('pow', 'coa', 'coa', 'gj.pow.coa'),
            ('ind', 'nga', 'nga', 'gj.ind.nga'), ('res', 'nga', 'nga', 'gj.res.nga'), ('pow', 'nga', 'nga', 'gj.pow.nga'),
            ('rd', 'gso', 'gso', 'ext.all.gso'), ('rd', 'die', 'die', 'ext.all.die'), ('all', 'lpg', 'lpg', 'gj.all.lpg'),
            ('all', 'ker', 'ker', 'gj.all.ker'), ('pow', 'oop', 'oop', 'gj.pow.oop'), ('ind', 'oop', 'oop', 'gj.ind.oop'),
            ('oth', 'coa', 'coa', 'gj.oth.coa'), ('oth', 'nga', 'nga', 'gj.oth.nga'), ('oth', 'gso', 'gso', 'gj.all.gso'),
            ('oth', 'die', 'oop', 'gj.oth.odo')]          # env.ffs.cost: (sector, fuel, climate fuel, external cost row)


def step(state, db, inputs, settings, baseline, t):
    """EQ-A8.5, EQ-A8.6: section 18 in year t."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    c = xt.constant
    countries = list(settings.countries)
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    put = lambda var, values, sector=None, fuel=None: R.set(var, k, values, sector, fuel)
    ref = lambda var, sector=None, fuel=None: reference(R, baseline, k, var, sector, fuel)
    col = lambda fn: np.array([fn(iso) for iso in countries])
    dp = state['_prices']['domestic']
    gj = lambda code: col(lambda iso: dp[iso][code]['gj'])
    vatgen = col(lambda iso: dp[iso]['gso.all']['vatgen'])
    osh = lambda f: col(lambda iso: dp[iso][f'{f}.all']['osh'])
    gdp = at('gdp.usd', 'all', 'all')
    mbn = c('MperBn')

    def average(var, fuel, sectors, weight='con'):
        """Excel-AI IFERROR(SUMPRODUCT(rows, weights) / SUM(weights), AVERAGE(rows))."""
        w = sum(at(weight, s, fuel) for s in sectors)
        x = sum(at(var, s, fuel) * at(weight, s, fuel) for s in sectors)
        return np.where(w == 0, sum(at(var, s, fuel) for s in sectors) / len(sectors), safe_div(x, w))

    # climate damages (EQ-A8.5)
    ghg = at('ghg', 'all', 'all')
    for kind in ('nat', 'glo'):
        put('dmg', at('scc', 'all', kind) * ghg / mbn, 'all', kind)
        put('wcli', ref('dmg', 'all', kind) - at('dmg', 'all', kind), 'all', kind)

    # efficiency: average wedge (fuel taxes per ktoe) times the change in use
    for f in WDG_FUELS:
        tax = at('rfu', 'all', f) + (at('rfg', 'pow', f) if f in WDG_POWER else 0.0)
        put('wdg', safe_div(tax, at('ener', 'all', f)), 'all', f)
    put('wdg', safe_div(at('rfu', 'pow', 'ecy'), at('eldem', 'all', 'ecy')), 'all', 'ecy')
    for f in WDG_FUELS:
        put('eff', -(at('wdg', 'all', f) + ref('wdg', 'all', f)) / 2 * at('echg', 'all', f) / mbn, 'all', f)
    put('eff', -(at('wdg', 'all', 'ecy') + ref('wdg', 'all', 'ecy')) / 2
        * (at('eldem', 'all', 'ecy') - ref('eldem', 'all', 'ecy')) / mbn, 'all', 'ecy')
    eff = put('eff', sum(at('eff', 'all', f) for f in WDG_FUELS + ['ecy']), 'all', 'all')

    # methane fee: marginal price of abatement and abatement cost by source
    src = lambda s, key: col(lambda iso: state['_ghg'][iso]['src'][s][key])
    mfee = at('mfee')
    for s in CH4_SOURCES:
        a, b = src(s, 'a'), src(s, 'b')
        with np.errstate(divide='ignore', invalid='ignore'):        # Excel-AI bug M21: #DIV/0 where b = 0 (here 1)
            cap = np.power(safe_div(1.0, a), safe_div(1.0, b))
        mfp = put('mfp', np.where(a == 0, 0.0, np.minimum(mfee * src(s, 'gwp') * src(s, 'fee'), cap)), 'all', s)
        em = safe_div(src(s, 'em0') * at('ch4.act', 'all', s), src(s, 'act0'))
        put('mfc', em * at('ch4.abt', 'all', s) * mfp * b / (1 + b) / c('Million'), 'all', s)
    mfc = put('mfc', sum(at('mfc', 'all', s) for s in CH4_SOURCES), 'all', 'all')

    # climate cost per GJ (generic CO2 factors)
    if '_efgen' not in state:
        state['_efgen'] = {iso: pigouvian.generic_ef(db, iso, c) for iso in countries}
    for kind in ('nat', 'glo'):
        for f in CC_FUELS:
            put(f'cc.{kind}', at('scc', 'all', kind) * col(lambda iso: state['_efgen'][iso].get(f, 0.0)), 'all', f)

    # air pollution: electricity, the weights of the averages, averages of the sector rows
    pe = lambda f: at('pe', 'pow', f)
    apc = lambda s, f: at('airpol.cost.gj', s, f)
    put('airpol.ecy', sum(apc('pow', f) * pe(f) for f in ('coa', 'nga', 'oop')) * PJ_PER_KTOE
        / (at('gtot') * c('MWyMkWh')))
    for s, f, v in (('ind', 'coa', at('fuq', 'ind', 'coa')), ('bld', 'coa', at('fuq', 'bld', 'coa')), ('pow', 'coa', pe('coa')),
                    ('ind', 'nga', at('fuq', 'ind', 'nga')), ('bld', 'nga', at('fuq', 'bld', 'nga')), ('pow', 'nga', pe('nga')),
                    ('tra', 'die', at('fuq', 'tra', 'die')), ('pow', 'oop', pe('oop')), ('ind', 'oop', at('fuq', 'ind', 'oop'))):
        put('apq', v, s, f)
    q = lambda s, f: at('apq', s, f)
    for f in ('coa', 'nga'):
        pairs = [('ind', 'ind'), ('res', 'bld'), ('pow', 'pow')]
        w = sum(q(qs, f) for _s, qs in pairs)
        put('airpol.cost.gj', np.where(w == 0, sum(apc(s, f) for s, _q in pairs) / 3,
                                       safe_div(sum(apc(s, f) * q(qs, f) for s, qs in pairs), w)), 'oth', f)
    oop = apc('pow', 'oop') * q('pow', 'oop') + apc('ind', 'oop') * q('ind', 'oop')
    w_oop = q('pow', 'oop') + q('ind', 'oop')
    put('airpol.cost.gj', safe_div(apc('all', 'die') * q('tra', 'die') + oop, q('tra', 'die') + w_oop), 'oth', 'odo')
    put('airpol.cost.gj', safe_div(oop, w_oop), 'avg', 'oop')
    put('tot.ext', apc('all', 'gso') + at('tran.acc.gj', 'all', 'gso') + at('tran.con.gj', 'all', 'gso'), 'all', 'gso')
    put('tot.ext', apc('all', 'die') + at('tran.acc.gj', 'all', 'die') + at('tran.con.gj', 'all', 'die')
        + at('tran.rdm.gj', 'all', 'die'), 'all', 'die')

    # welfare (EQ-A8.5)
    wair = put('wel', at('air.vpm') * (ref('air.con.pm2', 'mod') - at('air.con.pm2', 'mod')), 'air', 'usd')
    km = ref('trkmt', 'all', 'all') - at('trkmt', 'all', 'all')
    rod = [put('wel.rod', at('tran.acc.km') * km, 'aci', 'usd'), put('wel.rod', at('tran.con.km') * km, 'con', 'usd'),
           put('wel.rod', at('tran.rdm.km') * (ref('trkmf', 'fre', 'all') - at('trkmf', 'fre', 'all')), 'dmg', 'usd')]
    wcli = at('wcli', 'all', 'nat')
    wtot = put('wel', wcli + wair + sum(rod) - eff - mfc, 'all', 'usd')
    put('wel', safe_div(wtot, gdp), 'all', 'pct')
    put('wel', safe_div(wcli, gdp), 'all', 'cli')
    put('wel', wair / gdp, 'air', 'pct')
    put('wel', sum(rod) / gdp, 'rod', 'pct')
    put('wel', safe_div(eff + mfc, gdp), 'all', 'eff')

    # environmental cost of the change in fossil fuel use
    fq = lambda s, f: at('fuq', s, f)
    for (s, f), v in {('ind', 'coa'): fq('ind', 'coa'), ('res', 'coa'): fq('bld', 'coa'), ('pow', 'coa'): pe('coa'),
                      ('ind', 'nga'): fq('ind', 'nga'), ('res', 'nga'): fq('bld', 'nga'), ('pow', 'nga'): pe('nga'),
                      ('rd', 'gso'): fq('tra', 'gso'), ('rd', 'die'): fq('tra', 'die'),
                      ('all', 'lpg'): at('ener', 'all', 'lpg'),
                      ('all', 'ker'): at('ener', 'all', 'ker') + at('ener', 'all', 'jfu'), ('pow', 'oop'): pe('oop'),
                      ('ind', 'oop'): fq('ind', 'oop') + fq('ind', 'die'), ('oth', 'coa'): fq('tra', 'coa') + fq('oen', 'coa'),
                      ('oth', 'nga'): fq('tra', 'nga') + fq('oen', 'nga'),
                      ('oth', 'gso'): at('ener', 'all', 'gso') - fq('tra', 'gso'),
                      ('oth', 'die'): fq('bld', 'die') + fq('oen', 'die') + fq('tra', 'oop') + fq('bld', 'oop')
                      + fq('oen', 'oop')}.items():
        put('ffs.q', v, s, f)
    for s, f, cf, ext in FFS_COST:
        kind, es, ef = ext.split('.')
        cost = at('tot.ext', 'all', ef) if kind == 'ext' else apc(es, ef)
        put('env.ffs.cost', -(at('cc.glo', 'all', cf) + cost) * (at('ffs.q', s, f) - ref('ffs.q', s, f))
            * PJ_PER_KTOE / mbn, s, f)
    env = put('env.ffs.cost', sum(at('env.ffs.cost', s, f) for s, f, _c, _e in FFS_COST), 'tot', None)
    put('wel.ffs', env - eff - mfc)

    # subsidies (EQ-A8.6): use in PJ (GWh), supply cost, external cost, VAT on both, retail price
    E = lambda s, f: at('ener', s, f)
    con = {('all', 'gso'): E('all', 'gso'), ('all', 'die'): E('all', 'die'), ('all', 'lpg'): E('all', 'lpg'),
           ('all', 'ker'): E('all', 'ker') + E('all', 'jfu'), ('all', 'oop'): E('all', 'oop')}
    for f in ('nga', 'coa'):
        con.update({('ind', f): fq('ind', f), ('res', f): fq('bld', f), ('pow', f): pe(f),
                    ('oth', f): fq('tra', f) + fq('oen', f)})
    for (s, f), v in con.items():
        put('con', v * PJ_PER_KTOE, s, f)
    el = lambda s: at('eldem', s, 'ecy')
    for s, v in (('ind', el('ind')), ('res', el('bld')), ('oth', el('tra') + el('oen'))):
        put('con', v * c('KtoeGWh'), s, 'ecy')

    def rows(var, values):
        """The sector rows of every fuel, then its 'oth' average weighted by use."""
        for (s, f) in SUB_ROWS:
            if s != 'oth':
                put(var, values(s, f), s, f)
        for f, sectors in (('nga', ['ind', 'res', 'pow']), ('coa', ['ind', 'res', 'pow']), ('ecy', ['ind', 'res'])):
            put(var, average(var, f, sectors), 'oth', f)
    rows('supcost', lambda s, f: at('spe', s, f) if f == 'ecy' else at('sp', s, f))
    cc = lambda f: at('cc.glo', 'all', f)
    rows('extcost', lambda s, f: 0.0 if f == 'ecy' else cc(f) + (
        at('tot.ext', 'all', f) if f in ('gso', 'die') else apc('avg', 'oop') if f == 'oop' else apc(s, f)))
    vat_rate = lambda s, f: (vatgen * osh(f) if f in OILS else 0.0) if s == 'all' else (vatgen if s == 'res' else 0.0)
    rows('vatext', lambda s, f: (at('supcost', s, f) + at('extcost', s, f)) * vat_rate(s, f))
    rows('effprice', lambda s, f: at('supcost', s, f) + at('extcost', s, f) + at('vatext', s, f))
    rows('rpsub', lambda s, f: at('rp', s, f) if f == 'ecy' else at('rpn', s, f))
    exp_tot = imp_tot = 0.0
    for s, f in SUB_ROWS:
        sup, rp, eff_p, q_ = at('supcost', s, f), at('rpsub', s, f), at('effprice', s, f), at('con', s, f)
        exp_tot = exp_tot + put('expsub.con', np.maximum(0, sup - rp) * q_ / mbn, s, f)
        imp_tot = imp_tot + put('impsub.con', (rp <= eff_p) * (eff_p - np.maximum(rp, sup)) * q_ / mbn, s, f)
    put('expsubgdp.con', put('expsub.con', exp_tot, 'tot', None) / gdp, 'tot', None)
    put('impsubgdp.con', put('impsub.con', imp_tot, 'tot', None) / gdp, 'tot', None)

    # efficient prices by price code (EQ-A8.6), per price unit
    put('airpol.ecy.g', sum(apc('pow', f) * at('gen_mwy', 'pow', f) for f in ('coa', 'nga', 'oop')) / at('gtot')
        * c('KtoeGWh') / c('Thousand'))
    put('acc.cost', at('tran.acc.cost', 'all', 'gso'), 'all', 'gso')
    put('acc.cost', at('tran.acc.cost', 'all', 'die'), 'all', 'die')
    put('con.cost', at('tran.con.cost', 'all', 'gso'), 'all', 'gso')
    put('con.cost', at('tran.con.cost', 'all', 'die'), 'all', 'die')
    put('rdm.cost', at('tran.rdm.cost', 'all', 'die'), 'all', 'die')
    yes_vat = np.array([str(x)[:3] == 'Yes' for x in at('ExternalityAddVAT')])
    q_eff = {}
    for s, f in EFF_ROWS:
        code = f'{f}.{s}'
        unit = 1.0 if f == 'ecy' else gj(code)
        sup = put('sup.cost', ref('spe' if f == 'ecy' else 'sp', s, f) * unit, s, f)
        ap = put('airpol.cost.s', ref('airpol.ecy.g') if f == 'ecy' else
                 at('airpol.cost', s, f) if s == 'all' else apc(s, f), s, f)
        sc = put('scc.cost', 0.0 if f == 'ecy' else at('cc.code', s, f), s, f)
        pig = ap + sc
        if f == 'gso':
            pig = pig + at('acc.cost', 'all', f) + at('con.cost', 'all', f)
        if f == 'die':
            pig = pig + at('acc.cost', 'all', f) + at('con.cost', 'all', f) + at('rdm.cost', 'all', f)
        pig = put('pig', pig, s, f)
        rate = vatgen if s in ('all', 'res') else 0.0
        vat = put('vat.cost', (sup + pig * yes_vat) * rate, s, f)
        price = put('eff.price', sup + pig + vat, s, f)
        rpe = put('rp.eff', at('rp', s, f) if f == 'ecy' else at('rpn', s, f) * unit, s, f)
        put('tgap', rpe - price, s, f)
        glo = at('scc', 'all', 'glo')
        co2e = put('pig.co2e', safe_div(pig * glo, sc), s, f)
        put('app', safe_div(co2e * ap, pig), s, f)
        put('txo.co2e', 0.0 if f == 'ecy' else safe_div(ref('txo', s, f) * unit * glo, sc), s, f)
        if f != 'ecy':
            use = {'all': lambda: at('ener', 'all', f) + (at('ener', 'all', 'jfu') if f == 'ker' else 0.0),
                   'ind': lambda: fq('ind', f), 'res': lambda: fq('bld', f), 'pow': lambda: pe(f)}[s]
            q_eff[(s, f)] = put('effp.q', use(), s, f)
    w = sum(q_eff.values())
    for var in ('pig.co2e', 'app'):
        put(var, safe_div(sum(at(var, s, f) * v for (s, f), v in q_eff.items()), w), 'avg', None)
