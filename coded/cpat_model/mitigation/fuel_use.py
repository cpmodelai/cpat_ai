"""Blocks 5-8, fuel use by subsector and fuel (Mitigation sections 5-8): one block per subsector s, one row per fuel f.

prepare  the quantity-free rows: new carbon tax, ETS cost and new taxes per GJ, existing carbon pricing, consumer
         subsidy and price-control wedges, after-tax price, shadow price, efficiency multiple (EQ-M2.4 to EQ-M2.6,
         EQ-A2.2).
step     one year t (later): fuel use by the elasticity model, emissions and revenues.
"""
import numpy as np

from cpat_model.core.dims import COVERAGE_SECTORS, FUELS, SECTORS
from cpat_model.core.rows import Rows
from cpat_model.mitigation import fuel_data, policies

EXEMPTION_GROUPS = ['all', 'res']                     # rows exf.all.all, exf.res.all
EFFICIENCY_INPUTS = ['AdditionalEfficiencyRoadVehicle', 'AdditionalEfficiencyResidential',
                     'AdditionalEfficiencyIndustrial']   # additional efficiency groups 1-3


def country_table(db, iso, state, settings):
    """The fuel | subsector table of the country (fuel_data; tested in test_data_steps)."""
    d = state['_power'][iso]
    dp = state['_prices']['domestic'][iso]
    return fuel_data.fuel_table(db, iso, settings, d['ela'], d['co2'], d['efcalib'], d['ecp'],
                                policies.ecp_embedded_year(settings), d['nonco2'], dp)


def prepare(state, db, inputs, settings, baseline):
    """EQ-M2.4, EQ-M2.5, EQ-M2.6, EQ-A2.2: the price rows of every fuel block."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    g = lambda name: inputs[name]
    G = lambda name: settings.global_settings.get(name, inputs[name])
    tables = {iso: country_table(db, iso, state, settings) for iso in countries}
    state['_fuel'] = tables
    col = lambda f, s, key: np.array([[tables[iso][(f, s)][key]] for iso in countries])
    first = tables[countries[0]]
    xct_c = (R.of('xct.c')[0] - 1).astype(int)
    xct_p, xets_p = R.of('xct.p'), R.of('xets.p')
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS]
    for s in SECTORS:
        for f in FUELS:
            p = first[(f, s)]
            ef = col(f, s, 'co2ef')
            cov_sector = COVERAGE_SECTORS[p['spos'] - 1]
            exf = R.of('exf', EXEMPTION_GROUPS[p['exempt_group'] - 1], 'all')
            pf = fuel_data.FUELS_ORDER[p['fpos'] - 1]
            ctx = R.put('ctxnew', R.of('ctr', cov_sector, 'all') * ef * R.of('ctcov', 'all', pf) * exf, s, f)
            ets = R.put('ets', R.of('etr', cov_sector, 'all') * ef * exf, s, f)
            rf = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res', 'ecy.ind', 'gso.all',
                  'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all'][p['pfpos'] - 1].split('.')
            ntx = R.put('ntx', R.of('ntxb', rf[1], rf[0]) / col(f, s, 'gj') * exf, s, f)
            nce = R.put('nce', ctx + ets + ntx, s, f)
            def ecp(kind):                    # existing carbon tax or ETS of the ECP sector | fuel, by year
                rows = []
                for iso in countries:
                    k = xkeys[tables[iso][(f, s)]['ecpk'] - 1]
                    rows.append((np.zeros(5) if k == 'none|none' else state['_ecp'][iso][f'{kind}|{k}'])[xct_c])
                return np.array(rows)
            existing = ecp('xct') * xct_p + ecp('xets') * xets_p
            R.put('xcp', ef * existing, s, f)
            xcpd = R.put('xcpd', ef * (existing - col(f, s, 'xcp0')), s, f)
            pf_, ps_ = p['price_code'].split('.')
            csw = R.put('csw', R.of('pcsw', ps_, pf_), s, f)
            pcw = R.put('pcw', R.of('ppcw', ps_, pf_), s, f)
            R.put('atp', np.maximum(R.of('pbc', ps_, pf_) + (nce + xcpd + csw + pcw) * (1 + col(f, s, 'vat')),
                                    G('PriceFloor')), s, f)
            R.put('shp', R.of('shpx', cov_sector, 'all') * ef, s, f)
            add = g(EFFICIENCY_INPUTS[p['eff_group'] - 1])
            R.put('aef', (1 / (1 + col(f, s, 'alpha') + add)) ** (1 + col(f, s, 'eu')), s, f)
    R.finish()
