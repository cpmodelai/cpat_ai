"""Data step: the table by fuel and subsector that the fuel blocks of Mitigation sections 5-8 read (Excel-AI Inputs
rows 5-148). EQ-A3.2.

One row per fuel f and subsector s: elasticities (income, usage, efficiency, autonomous efficiency improvement),
price code and its VAT rate, CO2 and other emission factors, base-year fuel use (energy balance or EnergyCons),
existing carbon pricing embedded in the price data, and positions used by the blocks.
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.mitigation import power_data

ROAD_FUELS = ['gso', 'die', 'lpg', 'nga', '', '', 'bio']      # Excel-AI TrFuelKey: rows of the road model results
LEAKAGE_FUELS = ['none', 'nga', 'lpg', 'ker', 'bio']           # Excel-AI LkFuelKey: residential leakage rows
POLLUTANTS = power_data.POLLUTANTS + ['ch4']
FUELS_ORDER = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'jfu', 'oop', 'bio']


def fuel_table(db, iso, settings, ela, co2, efcalib, ecp, ecp_year, nonco2, prices):
    """{(fuel, subsector): {column: value}}. prices: prices_data.domestic_prices of the country."""
    base = settings.base
    fuels = {r['fuel']: r for r in xt.table('fuels')}
    subs = {r['sector']: r for r in xt.table('subsectors')}
    pf_pos = {pc: i + 1 for i, pc in enumerate(['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'ecy.res',
                                               'ecy.ind', 'gso.all', 'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all'])}
    xkeys = ['none|none'] + [f'{s}|{f}' for s in ('pow', 'trs', 'res', 'ind') for f in FUELS_ORDER]
    k_emb = [2021, 2022, 2023, 2024, 2025].index(ecp_year)
    bal = power_data.balances(db, iso, settings.base_year)
    cons = db.table('energy_consumption')
    cons = cons[cons['code'].str.startswith(f'{iso.lower()}.mit.enc.')]
    first = cons.groupby('code')['year'].first()
    cons = {(code[len(iso) + 9:], s): float(v) if v not in ('', None) else 0.0
            for code, y, s, v in zip(cons['code'], cons['year'], cons['sector'], cons['value']) if y == first[code]}
    info_flows = [fl for fl in bal if fl.startswith('info_')]
    use_bal = str(base['BalancesOrConsumption'])[:3] == 'Bal'
    out = {}
    for r in xt.table('fuel_subsector_rows'):
        f, s = r['fuel'], r['sector']
        fu, su = fuels[f], subs[s]
        p = {'ela_sector': su['elasticity_sector'], 'ela_fuel': fu['elasticity_fuel'], 'aeei_fuel': fu['aeei_fuel'],
             'price_rule': fu['price_rule'], 'price_sector': su['price_sector']}
        p['price_code'] = f"{fu['price_fuel']}.{p['price_sector'] if p['price_rule'] == 'sub' else 'all'}"
        p['ef_sector'] = su['ef_sector']
        p['gj'] = float(fu['gj_per_unit'])
        p['fpos'] = int(fu['position'])
        p['spos'] = int(su['coverage_position'])
        p['pfpos'] = pf_pos[p['price_code']]
        p['ey'] = ela[f"inc|{p['ela_fuel']}|{p['ela_sector']}"]
        if (f, s) == ('bio', 'res') and str(base['BiomassNormal'])[:3] != 'Yes':
            p['ey'] = 0.0                  # residential biomass grows with income only if it is a normal good (I24)
        p['eu'] = ela[f"usg|{p['ela_fuel']}|{p['ela_sector']}"]
        p['ef'] = ela[f"eff|{p['ela_fuel']}|{p['ela_sector']}"]
        p['alpha'] = ela[f"aei|{p['aeei_fuel']}|{p['ela_sector']}"]
        p['eff_group'] = int(r['efficiency_group'])
        p['eff_exp'] = p['ef'] * (1 + p['eu'])
        p['vat'] = prices[p['price_code']]['vr']
        p['co2ef'] = co2[f"{f}|{p['ef_sector']}"] * efcalib
        p['flow1'], p['sign1'] = su['flow1'], float(su['sign1'])
        p['flow2'], p['sign2'] = su['flow2'], float(su['sign2'] or 0)
        p['bal1'] = bal.get(p['flow1'], {}).get(f, 0.0)
        p['bal2'] = bal.get(p['flow2'], {}).get(f, 0.0) if p['flow2'] else 0.0
        p['cons'] = cons.get((f, s), 0.0)
        p['ener0'] = p['bal1'] * p['sign1'] + p['bal2'] * p['sign2'] if use_bal else p['cons']
        p['ecp_sector'] = p['price_sector'] if p['price_rule'] == 'sub' else ('ind' if f == 'oop' else 'trs')
        key = f"{p['ecp_sector']}|{f}"
        p['ecpk'] = xkeys.index(key) + 1 if key in xkeys else 1
        p['xcp0'] = (ecp[f'xct|{key}'][k_emb] + ecp[f'xets|{key}'][k_emb]) if key in xkeys else 0.0
        p['nc_sector'], p['nc_fuel'] = r['ef_sector'], r['ef_fuel']
        for pol in POLLUTANTS:
            p[f'ef0_{pol}'], p[f'ef1_{pol}'] = nonco2.get(f"{r['ef_sector']}.{r['ef_fuel']}.{pol}", (0.0, 0.0))
        p['road_pos'] = ROAD_FUELS.index(f) + 1 if s == 'rod' and f in ROAD_FUELS else 0
        p['food'] = bal.get('info_food', {}).get(f, 0.0)
        p['food_all'] = sum(bal[fl].get(f, 0.0) for fl in info_flows)
        p['food_share'] = p['food'] / p['food_all'] if p['food_all'] else 0.0
        p['exempt_group'] = int(r['exemption_group'])
        p['leak_pos'] = LEAKAGE_FUELS.index(f) + 1 if s == 'res' and f in LEAKAGE_FUELS else 1
        out[(f, s)] = p
    return out
