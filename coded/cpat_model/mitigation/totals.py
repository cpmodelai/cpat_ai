"""Totals of the year (Mitigation sections 11-12): energy use by sector group and fuel, electricity demand, changes
against the baseline. EQ-M3.3.

Rows carry Excel-AI's member names ('all' for a total); the results give each row Excel-AI's code (ener.all.all is
ener.tot.tot).
"""
import numpy as np

from cpat_model.core.dims import FUELS, SECTOR_GROUP, SECTORS
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
