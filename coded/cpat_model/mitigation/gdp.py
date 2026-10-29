"""Block 16, GDP (Mitigation sections 0 and 16): the level of real GDP after the feedback of the fiscal impulse.

start  at the start of year t: GDP level from the effect of earlier years, GDP growth after the feedback, the GDP
       growth that drives fuel use, the demand shock factor (EQ-M8.3).
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
        eff = R.at('gdp.eff', k - 1, 'all', 'all') if 'gdp.eff' in R._rows else 0.0   # not built yet: 0 (baseline)
        lvl = R.set('gdp.lvl', k, 1 + eff, 'all', 'all')
        growth = R.set('gdp.pos.pct', k, (1 + base) * lvl / R.at('gdp.lvl', k - 1, 'all', 'all') - 1)
    R.set('GDPI', k, (1 + growth) ** R.at('inc.ela.adj', k) - 1)
    R.set('SHOCK', k, 1 + R.at('shock', k) * settings.global_settings.get('ApplyDemandShock', 1))
