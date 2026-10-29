"""Block 16, GDP (Mitigation sections 0 and 16): the level of real GDP after the feedback of the fiscal impulse.

start    at the start of year t: GDP level from the effect of earlier years, GDP growth after the feedback, the GDP
         growth that drives fuel use, the demand shock factor (EQ-M8.3).
effects  at the end of year t: the fiscal impulse against the baseline, its lags, the GDP effect through the fiscal
         multipliers (EQ-M8.1, EQ-M8.2, EQ-A8.1); read by `start` of year t + 1.
"""
import numpy as np

from cpat_model.core.rows import Rows


def year_rows(state, settings):
    """The rows filled year by year (one Rows for every block of the year loop)."""
    if '_year' not in state:
        state['_year'] = Rows(state, settings.countries, settings.years)
    return state['_year']


def start(state, db, inputs, settings, baseline, t):
    """EQ-M8.3: gdp.lvl, gdp.pos.pct, GDPI (GDP growth raised to the income factor), SHOCK."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    base = R.at('gdp.base', k, 'all', 'all')
    if k == 0:
        lvl = R.set('gdp.lvl', k, 1.0, 'all', 'all')
        growth = R.set('gdp.pos.pct', k, base)
    else:
        eff = R.at('gdp.eff', k - 1, 'all', 'all')
        lvl = R.set('gdp.lvl', k, 1 + eff, 'all', 'all')
        growth = R.set('gdp.pos.pct', k, (1 + base) * lvl / R.at('gdp.lvl', k - 1, 'all', 'all') - 1)
    R.set('GDPI', k, (1 + growth) ** R.at('inc.ela.adj', k) - 1)
    R.set('SHOCK', k, 1 + R.at('shock', k) * settings.global_settings.get('ApplyDemandShock', 1))


# ---- fiscal impulse and GDP effect (Mitigation section 16)
LAGS = 20                                         # lags 0-19 of the fiscal multipliers
MULT_SOURCES = {'Glo': 'global', 'Est': 'est', 'Man': 'man'}     # Excel-AI MultSrcKey -> MultSrcVal; else income group
FMADJ_SIGN = {'base': 0, 'low': -1, 'high': 1}    # range of the multipliers: median + sign x standard deviation
SPENDING = [('pit', 'EXPLabortax'), ('cit', 'EXPCIT'), ('capt', 'EXPCapex'), ('gnfs', 'EXPGoodsandserv'),
            ('trns', 'EXPTransfers')]          # recycling instruments and the input row of the revenue share (%)
INSTRUMENTS = ['exc'] + [s for s, _ in SPENDING]


def multipliers(db, group, rng, instrument):
    """EQ-A8.1: the fiscal multiplier of the instrument by lag 0-19 (Excel-AI Inputs rows 456-486): MFMOD median of the
    group plus sign x standard deviation; lags past the last data lag hold its value."""
    if group in ('est', 'man'):
        raise NotImplementedError('country-estimated or manual multipliers (MultipliersSource Est*, Man*)')
    out = np.zeros(LAGS)
    for kind, sign in (('median', 1.0), ('sd', float(FMADJ_SIGN[rng]))):
        df = db.table(f'mult_mfmod_{kind}_{group}')
        df = df[df['instrument'] == instrument.upper()]
        vals = {int(l): float(v) for l, v in zip(df['lag'], df['value'])}
        last = max(vals)
        out += sign * np.array([vals[min(l, last)] for l in range(LAGS)])
    return out


def effects(state, db, inputs, settings, baseline, t):
    """EQ-M8.1, EQ-M8.2: fiscal impulse (the change in revenue against the baseline, % of GDP), its lags, the GDP effect
    of excises and of the recycled revenue, GDP growth contributions (Mitigation section 16)."""
    from cpat_model.core import excel_ai_tables as xt
    from cpat_model.mitigation.power_data import income_group
    from cpat_model.mitigation.totals import reference
    R = year_rows(state, settings)
    k, y = settings.years.index(t), t
    c = xt.constant
    at = lambda var, sector=None, fuel=None, kk=k: R.at(var, kk, sector, fuel)
    gdp = lambda kk=k: at('gdp.usd', 'all', 'all', kk)
    inp = lambda var: at(var, 'all', 'all') if 'sector' in state[var].dims else at(var)   # an input row of section 16
    rev = R.set('fis.rev', k, at('rnet', 'all', 'all') + at('rnew', 'all', 'all') + at('rsr', 'all', 'all')
                + at('rpsu', 'all', 'all') + at('ch4.rev', 'all', 'all'), 'all', 'all')
    ref = R.set('fis.ref', k, reference(R, baseline, k, 'fis.rev', 'all', 'all'), 'all', 'all')
    sp = R.set('fis.sp', k, (rev - ref) / (gdp() * c('MperBn')), 'all', 'all')
    start = inp('GDPStartYear')
    if k == 0:
        imp = np.where(y < start, 0.0, sp)
    else:
        imp = np.where(y < start, 0.0, sp - at('fis.sp', 'all', 'all', k - 1) * gdp(k - 1) / gdp())
    imp = R.set('fis.imp', k, imp, 'all', 'all')
    impp = R.set('fis.impp', k, np.where(y < at('CPIntro'), 0.0, imp), 'all', 'all')
    for name, now in (('fis.lag', 'fis.imp'), ('fis.lagp', 'fis.impp')):
        for lag in range(1, LAGS):
            prev = (now, 'all', 'all') if lag == 1 else (name, 'all', f'l{lag - 1}')
            R.set(name, k, 0.0 if k == 0 else at(*prev, kk=k - 1), 'all', f'l{lag}')
    stack = lambda now, name: np.stack([at(now, 'all', 'all')] + [at(name, 'all', f'l{lag}') for lag in range(1, LAGS)])
    imps, impps = stack('fis.imp', 'fis.lag'), stack('fis.impp', 'fis.lagp')
    countries = list(settings.countries)
    src = str(inputs['MultipliersSource'])[:3]
    rng = str(inputs['FmAdj']).replace('*', '').lower()
    groups = [MULT_SOURCES.get(src, income_group(db, iso).lower()) for iso in countries]
    R.set('fis.grp', k, np.array(groups, dtype=object), 'all', 'all')
    R.set('fis.key', k, np.array([f'{g}|{rng}|' for g in groups], dtype=object), 'all', 'all')
    if '_mult' not in state:
        state['_mult'] = {(g, i): multipliers(db, g, rng, i) for g in set(groups) for i in INSTRUMENTS}
    mult = lambda i: np.stack([state['_mult'][(g, i)] for g in groups], axis=1)     # (lag, country)
    on = np.array([str(v)[:3] == 'Yes' for v in np.atleast_1d(inp('GDPEndogenous'))])
    eff = {'exc': R.set('fis.eff', k, -np.sum(imps * mult('exc'), axis=0), 'all', 'exc')}
    for inst, share in SPENDING:
        eff[inst] = R.set('fis.eff', k, inp(share) / c('PctPerUnit') * np.sum(impps * mult(inst), axis=0), 'all', inst)
    lvl = at('gdp.lvl', 'all', 'all')
    R.set('gdp.pos.usd', k, gdp() * lvl, 'all', 'all')
    def growth(var, fuel):                       # contribution to GDP growth: last year's change in the effect
        if k == 0:
            return 0.0
        change = at(var, 'all', fuel, k - 1) - (at(var, 'all', fuel, k - 2) if k > 1 else 0.0)
        return (1 + at('gdp.base', 'all', 'all')) * change / at('gdp.lvl', 'all', 'all', k - 1)
    for inst in INSTRUMENTS:
        R.set('gdpg', k, growth('fis.eff', inst) * on, 'all', inst)
    R.set('gdpg', k, growth('gdp.eff', 'all'), 'all', 'all')
    R.set('gdpy', k, y - start + 1, 'all', 'all')
    R.set('gdp.chg.usd', k, gdp() * lvl - gdp(), 'all', 'all')
    R.set('gdp.eff', k, sum(eff.values()) * on, 'all', 'all')
