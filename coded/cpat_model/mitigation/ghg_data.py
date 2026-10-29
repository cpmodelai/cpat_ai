"""Data steps of the emissions blocks (Mitigation sections 13-14). EQ-A7.2.

    inventory      the GHG inventory of the country by year (Excel-AI sheet GHGs, Mt CO2e), columns enr.co2 ... fug.n2o
                   (Settings A772:A814), and the position of each year's row in the sheet (ghg.h)
    methane        methane abatement curves and source shares (sheet CH4Inputs; key: the first three letters of the source)
    population     UN population, thousands (sheet UNPop)
    world_demand   world production of oil, coal and gas, Mtoe, of the IEA scenario (Prices_int rows 323-333)
    nonenergy_elasticities, methane_inputs   legacy Manual inputs K325:M327 and J185:J200
"""
import numpy as np

from cpat_model.data.database import to_float
from cpat_model.mitigation import power_data

CATEGORIES = {'enr': 'energy', 'ipr': 'ippu', 'agr': 'agriculture', 'lucf': 'lulucf', 'wst': 'waste', 'oth': 'other',
              'tinc': 'total_incl_lucf', 'texc': 'total_excl_lucf', 'fug': 'memo_fugitive'}
GASES = {'CO2': 'co2', 'CH4': 'ch4', 'N2O': 'n2o', 'F-gas': 'fga', 'Aggregate GHGs': 'tot', 'Total GHGs': 'tot',
         'Total CO₂': 'co2', 'Total CH₄': 'ch4', 'Total N₂O': 'n2o', 'Total F-gases': 'fga', 'Total Aggregate GHGs': 'tot'}
WD_SCENARIOS = ['Stated Policies*', 'Announced Pledges', 'Sustainable Development', 'Net Zero']   # Excel-AI WDIdx
WD_ROWS = [1, 2, 4]                                     # scenario_no of the three rows of each fuel block


def inventory(db, iso):
    """({year: {column: value}}, {year: position of the row in sheet GHGs}, the latest year of the country)."""
    order = db.table('ghg_inventory_category')
    pos = {int(y): i + 1 for i, (c, y) in enumerate(zip(order['iso'], order['year'])) if c == iso}
    out = {y: {} for y in pos}
    for cat, name in CATEGORIES.items():
        df = db.table(f'ghg_inventory_{name}')
        df = df[df['iso'] == iso]
        for y, gas, v in zip(df['year'], df['gas'], to_float(df['value'])):
            out[int(y)][f'{cat}.{GASES[gas]}'] = 0.0 if np.isnan(v) else float(v)
    return out, pos, max(pos) if pos else 0


def methane(db, iso):
    """{source key (oil, coa, liv, ric, tot): {column: value}} of the country."""
    df = db.table('ch4_inputs')
    df = df[df['country'] == iso]
    cols = [c for c in df.columns if c not in ('country', 'source')]
    return {src[:3].lower(): {c: float(v) if v not in ('', None) else 0.0 for c, v in zip(cols, row)}
            for src, row in zip(df['source'], df[cols].itertuples(index=False))}


def population(db, iso):
    df = db.table('un_population')
    df = df[df['country'] == iso]
    return {int(y): float(v) for y, v in zip(df['year'], to_float(df['value']))}


def world_demand(db, scenario):
    """{fuel (oil, coa, nga): {year: Mtoe}} of the IEA scenario (GlobalEnergyDemand)."""
    names = [s.rstrip('*') for s in WD_SCENARIOS]
    idx = next((i for i, s in enumerate(names) if str(scenario).rstrip('*') == s), 0)
    no = str(WD_ROWS[min(idx, 2)])
    df = db.table('pint_world_demand')
    df = df[df['scenario_no'] == no]
    fuels = {'Oil': 'oil', 'Coal': 'coa', 'Natural gas': 'nga'}
    out = {f: {} for f in fuels.values()}
    for fu, y, v in zip(df['fuel'], df['year'], to_float(df['value'])):
        out[fuels[fu]][int(y)] = float(v)
    return out


def nonenergy_elasticities(db):
    """{Agriculture | Waste | Other: (per capita income elasticity, population elasticity)}; 'na' is 0 (Excel N())."""
    df = db.table('mi_nonenergy_elasticities')
    val = {(i, s): float(v) for i, s, v in zip(df['item'], df['sector'], to_float(df['value'])) if not np.isnan(v)}
    return {s: (val.get(('Per capita income elasticity', s), 0.0), val.get(('Population elasticity', s), 0.0))
            for s in ('Agriculture', 'Waste', 'Other')}


def methane_inputs(db):
    """{parameter: value} of the methane fee inputs (Manual inputs J185:J200)."""
    df = db.table('mi_methane_fee')
    df = df[df['variable'] == 'value']
    out = {}
    for p, v in zip(df['parameter'], df['value']):
        try:
            out[p] = float(v)
        except ValueError:
            out[p] = v
    return out


def consumption_total(db, iso, fuel):
    """Excel-AI ConsGas, ConsBio: EnergyCons enc.<fuel> of the first year, every column but elec and wav."""
    cons = db.table('energy_consumption')
    g = cons[cons['code'] == f'{iso.lower()}.mit.enc.{fuel}']
    if not len(g):
        return 0.0
    g = g[g['year'] == g['year'].iloc[0]]
    return float(sum(v for s, v in zip(g['sector'], to_float(g['value'])) if s not in ('elec', 'wav') and not np.isnan(v)))


def production(db, iso, base_year):
    """Base-year production of oil products, coal and gas (energy balance 'production', ktoe)."""
    bal = power_data.balances(db, iso, base_year).get('production', {})
    return {f: bal.get(f, 0.0) for f in ('oop', 'coa', 'nga')}
