"""Data step of the road transport engineer model (Mitigation section 5b). EQ-A3.5.

    params          the transport parameters (Excel-AI TransportParams: TrParKey -> TrParVal)
    data_years      the years with country transport data (Excel-AI TrYr: the years of Transport1, any country)
    country_rows    the country's transport data by year (Transport1 TrVal; rows 3699-3769)
    path_rows       global paths by year: BEV fuel economy of the stock, charging cost (TransportPaths TrPathVal; rows
                    3772-3777) and of new BEVs (Manual inputs BEVFEVal; rows 3780-3782)
    vehicle_prices  vehicle prices by year (Transport2 VPVal; rows 3785-3790): a year without data holds the last
    range_anxiety   start values of range anxiety (Transport3 H, N, T: the fitted values where the country has them)
    country_params  the parameter rows trp.* of the country (rows 3611-3695, 3794-3816)
Rows are keyed (variable, sector, fuel) as the Mitigation rows (sector = column C, fuel = column B).
"""
import numpy as np

from cpat_model.data.database import to_float
from cpat_model.mitigation import power_data

# Excel-AI rows 3699-3769: (variable, sector, fuel) and the Transport1 column (TrVar) in column D
COUNTRY_ROWS = [
    ('trshf', 'pas', 'gso', 'share of gasoline for passenger'), ('trshf', 'cyc', 'gso', 'share of gasoline for cycle'),
    ('trshf', 'pas', 'die', 'share of diesel for passenger'), ('trshf', 'bus', 'die', 'share of diesel for bus'),
    ('trshf', 'fre', 'die', 'share of diesel for freight'), ('trshf', 'pas', 'lpg', 'share of lpg for passenger'),
    ('trshf', 'bus', 'lpg', 'share of lpg for bus'), ('trshf', 'fre', 'lpg', 'share of lpg for freight'),
    ('trshf', 'pas', 'nga', 'share of natural gas for passenger'),
    ('trshf', 'bus', 'nga', 'share of natural gas for bus'), ('trshf', 'fre', 'nga', 'share of natural gas for freight'),
    ('trfe', 'lgt', 'ice', 'fuel economy light'), ('trfe', 'pas', 'gso', 'fuel economy gasoline passenger'),
    ('trfe', 'pas', 'die', 'fuel economy diesel passenger'), ('trfe', 'pas', 'lpg', 'fuel economy lpg passenger'),
    ('trfe', 'pas', 'nga', 'fuel economy cng passenger'), ('trfe', 'pas', 'phv', 'fuel economy phev passenger'),
    ('trfe', 'pas', 'bev', 'fuel economy ev passenger'), ('trfe', 'fre', 'die', 'fuel economy diesel freight'),
    ('trfe', 'fre', 'lpg', 'fuel economy lpg freight'), ('trfe', 'fre', 'nga', 'fuel economy lng freight'),
    ('trfe', 'cyc', 'gso', 'fuel economy gasoline cycle'),
    ('trown', 'pas', 'all', 'ownership passenger'), ('trown', 'lgt', 'all', 'ownership light'),
    ('trown', 'fre', 'all', 'ownership freight'), ('trown', 'cyc', 'all', 'ownership cycle'),
    ('trvkd', 'pas', 'all', 'average vkt passenger'), ('trvkd', 'lgt', 'all', 'average vkt light'),
    ('trvkd', 'fre', 'all', 'average vkt freight'), ('trvkd', 'cyc', 'all', 'average vkt cycle'),
    ('trevp', 'pas', 'ev', 'purchases share ev passenger'), ('trevp', 'pas', 'bev', 'purchases share bev passenger'),
    ('trevp', 'lgt', 'bev', 'purchases share bev light'), ('trevp', 'fre', 'bev', 'purchases share bev freight'),
    ('trevp', 'cyc', 'bev', 'purchases share bev cycle'),
    ('trevo', 'pas', 'ev', 'ownership share ev passenger'), ('trevo', 'pas', 'bev', 'ownership share bev passenger'),
    ('trevo', 'lgt', 'bev', 'ownership share bev light'), ('trevo', 'fre', 'bev', 'ownership share bev freight'),
    ('trevo', 'cyc', 'bev', 'ownership share bev cycle'),
    ('trdut', 'cyc', 'bev', 'duty, ev cycle'), ('trdut', 'fre', 'bev', 'duty, ev freight'),
    ('trdut', 'pas', 'bev', 'duty, ev passenger'), ('trdut', 'cyc', 'ice', 'duty, ice cycle'),
    ('trdut', 'fre', 'ice', 'duty, ice freight'), ('trdut', 'pas', 'ice', 'duty, ice passenger'),
    ('trimp', 'pas', 'all', 'share of passenger imports'), ('trimp', 'fre', 'all', 'share of freight imports'),
    ('trusd', 'pas', 'all', 'share used vehicles'), ('trchs', 'all', 'all', 'ev charging stations'),
    ('trsat', 'all', 'all', 'ownership saturation point')]
# rows 3772-3782: TransportPaths keys and the Manual inputs labels of the new-BEV fuel economy
PATH_ROWS = [('trfeb', 'lgt', 'bev', 'bev_fe|light'), ('trfeb', 'fre', 'bev', 'bev_fe|fre'),
             ('trfeb', 'cyc', 'bev', 'bev_fe|cyc'), ('trcpp', 'all', 'all', 'ch_cost_port')]
NEW_BEV_ROWS = [('trfen', 'pas', 'bev', 'BEV - passenger/light, new, fuel economy, vehicles purchases, all'),
                ('trfen', 'fre', 'bev', 'BEV - freight, new, fuel economy, vehicles purchases, all'),
                ('trfen', 'cyc', 'bev', 'BEV - 2-3 wheeler, new, fuel economy, vehicles purchases, all')]
PRICE_ROWS = [('trvp', 'pas', 'ice', 'icev_price_passenger'), ('trvp', 'pas', 'bev', 'ev_price_passenger'),
              ('trvp', 'fre', 'ice', 'icev_price_freight'), ('trvp', 'fre', 'bev', 'ev_price_freight'),
              ('trvp', 'cyc', 'ice', 'icev_price_cycle'), ('trvp', 'cyc', 'bev', 'ev_price_cycle')]
ROAD_FUELS = ['gso', 'die', 'lpg', 'nga']             # columns D-G of the trp rows by fuel


def params(db):
    """The transport parameters {TrParKey: value} (number, or text for the options)."""
    df = db.table('transport_params')
    df = df[df['use'] == 'default']
    return {k: (float(x) if not np.isnan(x) else v) for k, v, x in zip(df['key'], df['value'], to_float(df['value']))}


def data_years(db):
    """Excel-AI TrYr: every year that has a row in Transport1 (all countries)."""
    return {int(y) for y in db.table('transport_country')['year'].unique()}


def country_rows(db, iso, years):
    """{(variable, sector, fuel): values by year} of Transport1 (blank, text or missing: NaN, Excel-AI's "")."""
    df = db.table('transport_country')
    df = df[df['country'] == iso]
    values = {(int(y), v.lower()): x for y, v, x in zip(df['year'], df['variable'], to_float(df['value']))}
    return {(var, s, f): np.array([values.get((y, label.lower()), np.nan) for y in years])
            for var, s, f, label in COUNTRY_ROWS}


def path_rows(db, years):
    """{(variable, sector, fuel): values by year} of the global paths (TransportPaths, BEV new fuel economy)."""
    tp = db.table('transport_paths')
    tp = {(k, int(y)): x for k, y, x in zip(tp['key'], tp['year'], to_float(tp['value']))}
    fe = db.table('mi_ev_fuel_economy')
    fe = {(k, int(y)): x for k, y, x in zip(fe['vehicle'], fe['year'], to_float(fe['value']))}
    out = {(v, s, f): np.array([tp[(key, y)] for y in years]) for v, s, f, key in PATH_ROWS}
    out.update({(v, s, f): np.array([fe[(key, y)] for y in years]) for v, s, f, key in NEW_BEV_ROWS})
    return out


def vehicle_prices(db, iso, years):
    """{(trvp, sector, fuel): values by year} of Transport2; a year without a value holds the year before (0 at the
    start)."""
    df = db.table('vehicle_prices')
    df = df[df['country'] == iso]
    values = {(int(y), v): x for y, v, x in zip(df['year'], df['variable'], to_float(df['value']))}
    out = {}
    for var, s, f, label in PRICE_ROWS:
        row, last = [], 0.0
        for y in years:
            v = values.get((y, label), np.nan)
            last = last if np.isnan(v) else v
            row.append(last)
        out[(var, s, f)] = np.array(row)
    return out


def range_anxiety(db, iso, par):
    """Start value of range anxiety by vehicle class ($/vehicle; Excel-AI Transport3 H, N, T by country name): the
    fitted value where the country has one (range_anxiety_fit, written over Transport3), else Transport3, else the
    average of Transport3."""
    fit = db.table('range_anxiety_fit')
    fit = fit[fit['country'] == iso]
    if len(fit):
        return {c: float(fit[col].iloc[0]) for c, col in (('pas', 'passenger'), ('fre', 'freight'), ('cyc', 'cycle'))}
    ca = db.table('countries_attributes')
    name = ca.loc[ca['code'] == iso, 'name']
    t3 = db.table('transport3_range_anxiety')
    t3 = t3[t3['country_name'] == (name.iloc[0] if len(name) else '')]
    t3 = dict(zip(t3['variable'], to_float(t3['value'])))
    out = {}
    for c, label, avg in (('pas', 'passenger', 'pass'), ('fre', 'freight', 'fre'), ('cyc', 'two_three_wheeler', 'cyc')):
        v = t3.get(f'{label}|range_anxiety', np.nan)
        out[c] = par[f'ra_avg|{avg}'] if np.isnan(v) else v
    return out


def country_params(db, iso, settings, state, par, rows, biofuel):
    """The parameter rows trp.* of the country (rows 3611-3695 and 3794-3816), {name: value}: fuel-table values of
    road fuels (Excel-AI Inputs rows 5-148), base-year fuel use split by vehicle class, taxes and import shares of a
    data year. rows: country_rows; biofuel: base-year road biofuel use {bgs, bdi, obf} (trp.eb2 E-G)."""
    from cpat_model.mitigation import prices_data
    fuel = state['_fuel'][iso]
    rod = lambda f, key: fuel[(f, 'rod')][key]
    years = list(settings.years)
    at_year = lambda key, y: rows[key][years.index(int(y))]
    p = {}
    for f in ROAD_FUELS:
        p[f'gj|{f}'] = rod(f, 'gj')                                   # trp.gj (GJ per liter; gas per GJ)
        p[f'eb|{f}'] = rod(f, 'ener0')                                # trp.eb: base-year fuel use (ktoe)
    for f in ('gso', 'die', 'lpg'):
        p[f'lpk|{f}'] = power_data.PJ_PER_KTOE * 1e6 / p[f'gj|{f}']   # trp.lpk: liters per ktoe
        p[f'ef|{f}'] = rod(f, 'co2ef') * p[f'gj|{f}']                 # trp.ef: tCO2 per liter
    p['lpk|nga'] = p['lpk|gso']                                       # Excel-AI trp.lpk G: gas counted in gasoline liters
    p['ef|nga'] = rod('nga', 'co2ef') / par['gas_l_per_gj']           # tCO2 per liter-equivalent
    p['ela_usage|gso'], p['ela_usage|die'] = rod('gso', 'eu'), rod('die', 'eu')        # trp.ela D, E
    p['ela_eff|gso'], p['ela_eff|die'] = rod('gso', 'ef'), rod('die', 'ef')            # trp.ela F, G
    p['aeei'] = rod('gso', 'alpha')                                   # trp.mod D
    p['ktoe_gwh'] = state['_power'][iso]['par']['ktoe_gwh']           # trp.mod E (Inputs B260)
    dd = prices_data.DomesticData(db, iso, str(settings.base['DomPrTax'])[:1] == 'Y')
    p['vat_weo'] = dd.value(int(par['customs_year']), 'VAT_WEO') + 0  # trp.mod F
    p['eb2|ecy'] = state['_power'][iso]['subs']['rod']['d0']          # trp.eb2 D: road electricity (Inputs E238)
    for name in ('bgs', 'bdi', 'obf'):
        p[f'eb2|{name}'] = biofuel[name]                              # trp.eb2 E-G
    for f, bio in (('gso', 'bgs'), ('die', 'bdi')):                   # trp.efa: fossil share of the blend
        total = p[f'eb|{f}'] + p[f'eb2|{bio}']
        p[f'efa|{f}'] = p[f'eb|{f}'] / total if total != 0 else 1.0
    # trp.bsh: base-year fuel use by vehicle class (share of the data's first year, ktoe, billion liters)
    classes = {'gso': ['pas', 'cyc'], 'die': ['pas', 'bus', 'fre'], 'lpg': ['pas', 'bus', 'fre'],
               'nga': ['pas', 'bus', 'fre']}
    for f, cs in classes.items():
        shares = {c: rows[('trshf', c, f)][0] for c in cs}
        shares['lgt'] = 1 - sum(shares.values())
        for c, sh in shares.items():
            p[f'bsh|{c}|{f}'] = sh
            p[f'bshq|{c}|{f}'] = sh * p[f'eb|{f}']
            p[f'bshl|{c}|{f}'] = p[f'bshq|{c}|{f}'] * p[f'lpk|{f}'] / 1e9
    # trp.tax: VAT, ICEV and BEV duties of the customs data year, import share of the import data year
    for c, imp in (('pas', 'pas'), ('fre', 'fre'), ('cyc', 'pas')):
        p[f'tax_vat|{c}'] = 0.0 if c == 'fre' else p['vat_weo']      # trp.tax.fre D is blank
        p[f'tax_ice|{c}'] = at_year(('trdut', c, 'ice'), par['customs_year'])
        p[f'tax_bev|{c}'] = at_year(('trdut', c, 'bev'), par['customs_year'])
        p[f'tax_imp|{c}'] = at_year(('trimp', imp, 'all'), par['import_year'])
    # trp.bus: base-year bus fuel use (ktoe) and bus electricity (EV share of the stock of a data year x bus fuel)
    for f in ('die', 'lpg', 'nga'):
        p[f'bus|{f}'] = p[f'bshq|bus|{f}']
    p['bus|ecy'] = at_year(('trevo', 'pas', 'ev'), par['bus_ele_year']) * sum(p[f'bus|{f}'] for f in ('die', 'lpg', 'nga'))
    return p
