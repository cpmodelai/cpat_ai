"""Inputs from the air pollution and transport co-benefit modules (Mitigation section 17b) and welfare (section 18).

air        air pollution cost per GJ by price code weighted by current fuel use, fuel use by sector group, PM2.5
           concentration by source (EQ-A8.3)
transport  accident, congestion and road-damage cost per liter (kWh) and per GJ of road fuel from the road engineer
           model (EQ-A8.4)
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import safe_div
from cpat_model.mitigation.gdp import year_rows
from cpat_model.mitigation.totals import reference
from cpat_model.mitigation.pigouvian import AIRPOL_ROWS, BUILDINGS, INDUSTRY, OIL_SUBSECTORS

APS_POLLUTANTS = ['nox', 'so2', 'bc', 'pom', 'opm', 'voc', 'ch4', 'co', 'pm2', 'oc']   # order of the kappa rows
SOURCES = ['cpp', 'gpp', 'opp', 'rod', 'gro', 'oth', 'foo']
FUQ_FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'oop']
FUQ_GROUPS = {'tra': ['rod', 'ral', 'avi', 'nav'], 'bld': BUILDINGS, 'ind': INDUSTRY, 'oen': ['oen']}
COST_ROWS = [('ind', 'coa', INDUSTRY), ('res', 'coa', BUILDINGS), ('pow', 'coa', None), ('ind', 'nga', INDUSTRY),
             ('res', 'nga', BUILDINGS), ('pow', 'nga', None), ('all', 'gso', OIL_SUBSECTORS),
             ('all', 'die', OIL_SUBSECTORS), ('all', 'lpg', OIL_SUBSECTORS), ('all', 'ker', OIL_SUBSECTORS),
             ('pow', 'oop', None), ('ind', 'oop', INDUSTRY)]                   # rows airpol.cost (8335-8346)
ROAD_FUELS = ['gso', 'die', 'lpg', 'nga', 'ecy']
CLASS_USE = {'gso': ['trfcp.pas.gso', 'trfcc.cyc.gso'], 'ecy': ['trfcep.pas.ecy', 'trfcef.fre.ecy', 'trfcec.cyc.ecy'],
             **{f: [f'trfcp.pas.{f}', f'trfcf.fre.{f}'] for f in ('die', 'lpg', 'nga')}}   # tran.cls: fuel use by class
FREIGHT_USE = {'die': 'trfcf.fre.die', 'lpg': 'trfcf.fre.lpg', 'nga': 'trfcf.fre.nga', 'ecy': 'trfcef.fre.ecy'}
AVERAGE_FE = {'gso': 'trafg.all.gso', 'die': 'trafo.all.die', 'lpg': 'trafo.all.lpg', 'nga': 'trafo.all.nga',
              'ecy': 'trafe.all.ecy'}                                      # average fuel economy (km per liter, kWh)


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
    R.set('air.con.pm2', k, sum(at('air.con.pm2', src) for src in SOURCES), 'mod', None)


def transport(state, db, inputs, settings, baseline, t):
    """EQ-A8.4: transport externalities per unit of road fuel: the cost per km of the module times the km per unit
    (fuel economy) times the marginal share of distance in a change of fuel use (passenger and freight elasticities)
    and the road share; per GJ for the oil products (Mitigation section 17b, rows 8510-8556)."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    countries = list(settings.countries)
    row = lambda name: R.at(name.rsplit('.', 2)[0], k, *name.rsplit('.', 2)[1:])
    ref = lambda var, sector, fuel: reference(R, baseline, k, var, sector, fuel)
    rod = lambda f, key: np.array([state['_fuel'][iso][(f, 'rod')][key] for iso in countries])
    dp = state['_prices']['domestic']
    gj = lambda f: np.array([dp[iso][f'{f}.all']['gj'] for iso in countries])
    # usage and efficiency elasticities of gasoline and diesel (Excel-AI trp.ela, Inputs P and Q of gso|rod, die|rod)
    eu = {f: rod(f, 'eu') for f in ('gso', 'die')}
    ee = {f: rod(f, 'ef') for f in ('gso', 'die')}
    for f in ROAD_FUELS:
        R.set('tran.cls', k, sum(row(n) for n in CLASS_USE[f]), 'rod', f)
    R.set('tran.wcl', k, 1.0, 'rod', 'gso')
    for f, fre in FREIGHT_USE.items():
        var, s, ff = fre.rsplit('.', 2)
        cls0 = ref('tran.cls', 'rod', f)
        R.set('tran.wcl', k, np.where(cls0 == 0, 0.0, 1 - safe_div(ref(var, s, ff), cls0)), 'rod', f)
    for f in ROAD_FUELS:
        w = R.at('tran.wcl', k, 'rod', f)
        mrg = safe_div(eu['die'] + w * (eu['gso'] - eu['die']),
                       eu['die'] + ee['die'] + w * (eu['gso'] + ee['gso'] - eu['die'] - ee['die']))
        R.set('tran.mrg', k, np.where(ref('tran.cls', 'rod', f) == 0, 0.0, mrg), 'rod', f)
    for f, fre in FREIGHT_USE.items():
        R.set('tran.fsh', k, safe_div(row(fre), R.at('tran.cls', k, 'rod', f)), 'rod', f)
    for kind in ('acc', 'con', 'rdm'):
        km = R.at(f'tran.{kind}.km', k)
        for f in ROAD_FUELS if kind != 'rdm' else FREIGHT_USE:
            share = R.at('tran.fsh', k, 'rod', f) if kind == 'rdm' else 1.0
            R.set(f'tran.{kind}.cost', k, km * row(AVERAGE_FE[f]) * R.at('tran.mrg', k, 'rod', f) * share
                  * row(f'tran.rsh.rod.{f}'), 'all', f)
        for f in (('gso', 'die', 'lpg') if kind != 'rdm' else ('die', 'lpg')):
            R.set(f'tran.{kind}.gj', k, R.at(f'tran.{kind}.cost', k, 'all', f) / gj(f), 'all', f)

