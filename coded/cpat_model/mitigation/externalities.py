"""Inputs from the air pollution and transport co-benefit modules (Mitigation section 17b) and welfare (section 18).

air      air pollution cost per GJ by price code weighted by current fuel use, fuel use by sector group, PM2.5
         concentration by source (EQ-A8.3)
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import safe_div
from cpat_model.mitigation.gdp import year_rows
from cpat_model.mitigation.pigouvian import AIRPOL_ROWS, BUILDINGS, INDUSTRY, OIL_SUBSECTORS

APS_POLLUTANTS = ['nox', 'so2', 'bc', 'pom', 'opm', 'voc', 'ch4', 'co', 'pm2', 'oc']   # order of the kappa rows
SOURCES = ['cpp', 'gpp', 'opp', 'rod', 'gro', 'oth', 'foo']
FUQ_FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'oop']
FUQ_GROUPS = {'tra': ['rod', 'ral', 'avi', 'nav'], 'bld': BUILDINGS, 'ind': INDUSTRY, 'oen': ['oen']}
COST_ROWS = [('ind', 'coa', INDUSTRY), ('res', 'coa', BUILDINGS), ('pow', 'coa', None), ('ind', 'nga', INDUSTRY),
             ('res', 'nga', BUILDINGS), ('pow', 'nga', None), ('all', 'gso', OIL_SUBSECTORS),
             ('all', 'die', OIL_SUBSECTORS), ('all', 'lpg', OIL_SUBSECTORS), ('all', 'ker', OIL_SUBSECTORS),
             ('pow', 'oop', None), ('ind', 'oop', INDUSTRY)]                   # rows airpol.cost (8335-8346)


def air(state, db, inputs, settings, baseline, t):
    """EQ-A8.3: air pollution cost per unit of fuel weighted by fuel use (airpol.cost, per GJ airpol.cost.gj), fuel use
    by sector group (fuq), PM2.5 concentration by source (air.con.pm2)."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    c = xt.constant
    countries = list(settings.countries)
    at = lambda var, sector=None, fuel=None: R.at(var, k, sector, fuel)
    col = lambda fn: np.array([fn(iso) for iso in countries])
    dp = state['_prices']['domestic']
    for s, f in AIRPOL_ROWS:
        if s != 'pow':
            R.set('fus', k, at('ener', s, f), s, f)
    mc = lambda s, f: R.of('airpol.mc', s, f)[:, k]
    for sector, f, subs in COST_ROWS:
        unit = col(lambda iso: dp[iso][f'{f}.all']['gj']) if sector == 'all' else 1.0
        if subs is None:
            cost = mc('pow', f)
        else:
            w = sum(at('fus', s, f) for s in subs)
            cost = np.where(w == 0, sum(mc(s, f) for s in subs) / len(subs),
                            safe_div(sum(mc(s, f) * at('fus', s, f) for s in subs), w))
        cost = R.set('airpol.cost', k, cost * unit, sector, f)
        R.set('airpol.cost.gj', k, cost / unit, sector, f)
    for g, subs in FUQ_GROUPS.items():
        for f in FUQ_FUELS:
            R.set('fuq', k, sum(at('ener', s, f) for s in subs), g, f)
    R.set('airpol.cost.gj', k, at('airpol.cost', 'res', 'coa')
          * (at('fuq', 'bld', 'coa') > c('ApCoalResMin') * at('ener', 'bld', 'all')), 'res', 'coa')
    kappa = state['air.kappa'].reindex(country=countries)
    for src in SOURCES:
        kap = lambda pol: (kappa.sel(pollutant=pol, module_sector=src).values
                           if pol in kappa['pollutant'] else np.zeros(len(countries)))
        R.set('air.con.pm2', k, sum(at('aps', src, pol) * kap(pol) for pol in APS_POLLUTANTS) * c('tPerKt'), src, None)
