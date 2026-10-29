"""Totals of the year (Mitigation sections 11-12): energy use by sector group and fuel, electricity demand, revenues
by sector group, fuel and policy instrument, changes against the baseline. EQ-M3.3, EQ-M6.3, EQ-A6.2.

Rows carry Excel-AI's member names ('all' for a total); the results give each row Excel-AI's code (ener.all.all is
ener.tot.tot).
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.dims import COVERAGE_SECTORS, FUELS, SECTOR_GROUP, SECTORS
from cpat_model.core.rows import safe_div
from cpat_model.mitigation.gdp import year_rows
from cpat_model.mitigation.power import TYPES

GROUPS = ['tra', 'bld', 'ind', 'oen']


def reference(R, baseline, k, var, sector=None, fuel=None):
    """The baseline value of a row in year index k (Excel-AI REFCOL: scenario 1's column of the same year); in the
    baseline itself, the row."""
    if baseline is None:
        return R.at(var, k, sector, fuel)
    a = baseline[var]
    if sector is not None:
        a = a.sel(sector=sector, fuel=fuel)
    return a.sel(country=R.countries, year=R.years[k]).values


def energy(state, db, inputs, settings, baseline, t):
    """EQ-M3.3: energy use by subsector, sector group and fuel (ktoe), its change against the baseline."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    ren = at('ener', 'avi', 'ren') + at('ener', 'nav', 'ren')
    R.set('ener', k, at('pet', 'pow', 'all'), 'pow', 'all')
    for f in FUELS:
        R.set('ener', k, sum(at('ener', s, f) for s in SECTORS) + (at('pe', 'pow', f) if f in TYPES else 0.0), 'all', f)
    total = R.set('ener', k, sum(at('ener', s, 'all') for s in SECTORS) + at('ener', 'pow', 'all'), 'all', 'all')
    R.set('ener.chk', k, np.abs(sum(at('ener', s, 'all') for s in SECTORS) + at('ener', 'pow', 'all') - total)
          + np.abs(sum(at('ener', 'all', f) for f in FUELS) + ren - total))
    ref = R.set('ener.ref', k, reference(R, baseline, k, 'ener', 'all', 'all'), 'all', 'all')
    R.set('ener.pct', k, total / ref - 1, 'all', 'all')
    for g in GROUPS:
        R.set('eldem', k, sum(at('eldem', s, 'ecy') for s in SECTORS if SECTOR_GROUP[s] == g), g, 'ecy')
    R.set('eldem', k, sum(at('eldem', g, 'ecy') for g in GROUPS), 'all', 'ecy')
    for sector, fuel in [('all', f) for f in FUELS] + [(g, 'all') for g in GROUPS + ['pow']]:
        v = at('ener', sector, fuel)
        chg = R.set('echg', k, v - reference(R, baseline, k, 'ener', sector, fuel), sector, fuel)
        R.set('epct', k, safe_div(chg, v - chg), sector, fuel)
    R.set('echg', k, total - reference(R, baseline, k, 'ener', 'all', 'all'), 'all', 'all')


REV_VARS = ['rtx', 'rsub', 'rnew', 'rxcp', 'rsr']
POWER_USER_ROWS = ['rvat', 'rnvat', 'rreb', 'rpex', 'rgap']      # power revenue rows by user (res, ind), in sheet order
PRODUCER_FUELS = ['coa', 'nga', 'oil', 'bio', 'ecy']             # producer subsidy rows pros, psf


def revenues(state, db, inputs, settings, baseline, t):
    """EQ-M6.3, EQ-A6.2: revenue totals by sector group, fuel and policy instrument (USD m), as % of GDP."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    c = xt.constant
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    types = lambda var: sum(at(var, 'pow', kk) for kk in TYPES)
    users = lambda var: at(var, 'res', 'ecy') + at(var, 'ind', 'ecy')
    power = {'rtx': types('prtx') + types('prxc') + users('rvat'),
             'rsub': types('prsub') + users('rgap') + types('prrns'),
             'rnew': types('prnew') + users('rnvat') + users('rreb') + users('rpex'),
             'rxcp': types('prxl'), 'rsr': 0.0}
    for var in REV_VARS:
        for g in GROUPS:
            R.set(var, k, sum(at(var, s, f) for s in SECTORS if SECTOR_GROUP[s] == g for f in FUELS), g, 'all')
        R.set(var, k, power[var], 'pow', 'all')
        R.set(var, k, sum(at(var, s, f) for s in SECTORS for f in FUELS) + at(var, 'pow', 'all'), 'all', 'all')
    tot = lambda var: at(var, 'all', 'all')
    rmf = R.set('rmf', k, at('ch4.rev', 'all', 'all'), 'all', 'all')
    rpsu = R.set('rpsu', k, -sum(at('pros', 'all', f) * at('psf', 'all', f) for f in PRODUCER_FUELS), 'all', 'all')
    rnet = R.set('rnet', k, tot('rtx') + tot('rsub'), 'all', 'all')
    rtot = R.set('rtot', k, rnet + tot('rnew') + tot('rsr') + rpsu + rmf, 'all', 'all')
    rref = R.set('rtot.ref', k, reference(R, baseline, k, 'rtot', 'all', 'all'), 'all', 'all')
    R.set('rev.chk', k, sum(np.abs(tot(v) - sum(at(v, g, 'all') for g in GROUPS + ['pow'])) for v in ('rtx', 'rsub', 'rnew')),
          'all', 'all')
    for f in FUELS:
        R.set('rfu', k, sum(at(v, s, f) for v in ('rtx', 'rsub', 'rnew', 'rsr') for s in SECTORS), 'all', f)
    R.set('rfu', k, sum(users(v) for v in POWER_USER_ROWS) + types('prrns'), 'pow', 'ecy')
    for f in ('coa', 'nga', 'oop', 'bio'):
        R.set('rfg', k, sum(at(v, 'pow', f) for v in ('prtx', 'prxc', 'prsub', 'prnew')), 'pow', f)
    R.set('rfu.chk', k, np.abs(sum(at('rfu', 'all', f) for f in FUELS) + at('rfu', 'pow', 'ecy')
                               + sum(at('rfg', 'pow', f) for f in ('coa', 'nga', 'oop', 'bio'))
                               - rnet - tot('rnew') - tot('rsr')), 'all', 'all')
    rbe = R.set('rbe', k, rnet - reference(R, baseline, k, 'rnet', 'all', 'all'), 'all', 'all')
    rchg = R.set('rtot.chg', k, rtot - rref, 'all', 'all')
    gdp = at('gdp.usd', 'all', 'all') * c('MperBn')
    for key, v in (('tot', rtot), ('net', rnet), ('sub', tot('rsub')), ('new', tot('rnew')), ('chg', rchg), ('be', rbe)):
        R.set('rpct', k, v / gdp, 'all', key)
    for key, series in (('lcu', 'ngdp'), ('usd', 'ngdpd')):     # nominal GDP / Billion (WEO values are in billions)
        R.set('gdpn', k, state[f'macro.{series}'].sel(country=R.countries, year=t).values / c('Billion'), 'all', key)

    # revenue by policy instrument; covct (covered CO2) is a row of section 17
    cov = {}
    for e in COVERAGE_SECTORS:
        fuels = ('coa', 'nga', 'oop') if e == 'pow' else FUELS
        cov[e] = R.set('covct', k, sum(at('co2', e, f) * at('ctcov', 'all', f) for f in fuels)
                       * (at('ctr', e, 'all') > 0), e, 'all')
    ets_rf = at('ets.rf')
    ctp = R.set('rpol', k, cov['pow'] * at('ctr', 'pow', 'all'), 'all', 'ctp')
    etp = R.set('rpol', k, at('co2.sec', 'pow', 'all') * at('etr', 'pow', 'all') * ets_rf, 'all', 'etp')
    pol = {'ct': sum(cov[e] * at('ctr', e, 'all') for e in COVERAGE_SECTORS) + users('rreb') + at('rexs'),
           'exc': sum(at('rex', s, f) for s in SECTORS for f in FUELS) + types('prnew') - ctp - etp + at('rexm'),
           'vat': sum(at('rvt', s, f) for s in SECTORS for f in FUELS) + users('rvat') + users('rnvat'),
           'ets': sum(at('co2.sec', e, 'all') * at('etr', e, 'all') for e in COVERAGE_SECTORS) * ets_rf,
           'psu': users('rgap') + rpsu, 'ren': types('prrns'), 'mf': rmf, 'trs': 0.0}
    pol['exi'] = rtot - rmf - pol['ct'] - pol['exc'] - pol['vat'] - pol['ets'] - pol['psu'] - pol['ren']
    for key in ('ct', 'exc', 'exi', 'vat', 'ets', 'psu', 'ren', 'mf', 'trs'):
        R.set('rpol', k, pol[key], 'all', key)
    total = R.set('rpol', k, sum(pol[key] for key in ('ct', 'exc', 'exi', 'vat', 'ets', 'psu', 'ren', 'mf', 'trs')),
                  'all', 'tot')                             # ctp and etp are memo rows (power), not in the total
    R.set('rpol.chk', k, np.abs(total - rtot), 'all', 'all')
