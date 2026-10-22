"""v3.5 (phase 2 of Transport_Plan_v7_0.md): Python reference of the legacy CPAT engineer road transport model.

Source: legacy CPAT `CPAT 1.0pre_456_NoPropData.xlsb`, sheet Mitigation, key inputs 15 (rows 2017-2171) and section 5
"Transport sector" (rows 4302-5378; policy copy at +6331), as surveyed in Transport_Legacy_Survey_v7_0.md. Reads only
data/*.csv written by extract_transport_v7_0.py (and countries.csv); independent of any workbook.

Classes: passenger/light (new and used; gasoline, diesel, LPG, CNG, PHEV, BEV), freight (diesel, LPG, LNG, BEV),
2-3 wheelers (gasoline, BEV), buses (scaled, no stock). Chain per year, as legacy: stock openings and retirement;
charging stations, charging mark-up and range anxiety; new fuel economy; distance for the purchase decision; total
cost of ownership (TCO); Gompertz demand, logit EV choice, ICE fuel split, purchases and closings; stock fuel economy;
distance and fuel use; calibration step 1 (distance factors) and step 2 (fuel factors); buses; outputs by fuel
(ktoe, incl. road electricity), distance, vehicles.

engine(inp, years, fix): inp from legacy_inputs(run) (cached legacy inputs of the Egypt run). For another country,
replace data/prices (country_data(iso)), ra (range_anxiety(iso)) and the inputs from the rest of the model.
The result o maps legacy row numbers (baseline numbering) to year series, and 'cXXXX' to side-table scalars, so
every row can be compared with the cached legacy row. fix: the bug fixes to apply (names in FIXES); fix = frozenset()
reproduces legacy, ALL_FIXES is the corrected model.

    python transport_model_ref_v7_0.py          # legacy test (both runs) and the effect of each fix
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
YEARS = list(range(2022, 2042))
DATA_YEARS = [2022, 2023, 2024, 2025]        # Transport1 years (legacy columns L-O)
CLS = ('pass', 'fre', 'cyc')
FIXES = {  # name: (legacy rows, short description)
    'B1': ('4451, 4720', 'passenger distance tax and 2-3 wheeler EV subsidy test ($C2227>1), text "res" > 1 is TRUE, '
                         'so they also apply in the baseline; fix: scenario number > 1'),
    'B2': ('4487 AB:AE (also 4501)', 'freight and 2-3 wheeler income growth read row 2455 (coal producer subsidies) '
                                     'from 2038; fix: lagged GDP growth (row 2446) in all years'),
    'B3': ('H4787:J4787, H4903:J4903', 'ownership calibration MAX(1, actual/expected) at 2024 (column N); fix: '
                                       'actual/expected in both directions at the last data year found in the data'),
    'B3b': ('$N2168, J2169', 'freight-share cap and 2-3 wheeler peak read 2024 (column N); fix: last data year'),
    'B4': ('T4328, U4328', 'ownership cannot fall (max annual decrease 0 for passenger and freight); fix: allow a '
                           'decrease of up to own_decline_fix a year (legacy 2-3 wheeler value, 10%)'),
    'B6': ('5310-5314, 5318', 'bus fuel scaled by the wrong rows (LPG, gas and PHEV distance, BEV vehicles) and bus '
                              'electricity from a sum of liters and kWh; fix: passenger fuel use by fuel in ktoe '
                              '(5195-5198) and passenger electricity (5223), base bus energy in ktoe'),
    'B6b': ('O5171:O5173', 'bus share added to the bottom-up fuel use as x(1+bus share); fix: /(1-bus share)'),
    'B7': ('G4376-G4378, G4419-G4421', 'stale emission-factor names: diesel and LPG use industry EFs, CNG/LNG the '
                                       'residential gas EF; fix: road EFs'),
    'B8': ('M5261, M5295, M5232, M4646', 'BEV freight distance uses the 2-3 wheeler income elasticity; BEV 2-3 wheeler '
                                         'distance uses the cost ratio twice and no income term; LPG freight base row; '
                                         'freight ICE depreciation switches to the passenger discount rate from 2023; '
                                         'fix: as the sibling rows'),
    'B8w': ('K4329', 'freight discounted at the average power-sector WACC; fix: the consumer discount rate (row 4531)'),
    'B9': ('4850 L:O', 'PHEV sales share = passenger EV share - blended passenger/light BEV share (negative); fix: '
                       '(EV - BEV passenger share) x passenger share, ICE shares scaled to the rest'),
    'B10': ('4343', 'charging-station subsidy ramp accumulates before the start year and is not capped at the target '
                    'year; fix: 0 before the start year, linear to the target level, then constant'),
    'B19': ('4573', 'new BEV maintenance uses the ICEV maintenance cost (J4327); fix: EV maintenance (J4328)'),
    'B20': ('4598', 'used ICEV depreciation annuity over own_years-1 (6) years, used BEV over 12; fix: used '
                    'ownership period - 1 (J4323-1) for both'),
    'B21': ('5267', 'freight distance output omits LPG and LNG trucks; fix: all fuels'),
    'B22': ('5368, 5373', 'average gas fuel economy weights freight by LPG freight fuel (5244) instead of LNG (5245); '
                          'the EV fuel-economy fallback tests diesel (5326) instead of electricity; fix: right rows'),
    'B23': ('4555', 'PHEV TCO includes the full BEV range anxiety (about 100,000 $/vehicle), so PHEV sales vanish; fix '
                    '(user decision 2026-10-14): no range anxiety for PHEVs (they refuel with gasoline)'),
}
ALL_FIXES = frozenset(FIXES)
OWN_DECLINE_FIX = 0.1           # B4: maximum annual decrease of ownership once a decline is allowed


def read(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


def params(use=('default',)):
    return {r['key']: fnum(r['value']) for r in read('transport_params.csv') if r['use'] in use}


def paths(years):
    return {r['key']: [float(r[str(y)]) for y in years] for r in read('transport_paths.csv')}


def country_data(iso):
    """Transport1 values of a country {variable: {year: value}} (blank = 0, as legacy INDEX of an empty cell);
    Transport2 prices {variable: {year: value}}; Transport3 range anxiety {cls: value or None}."""
    d = {}
    for r in read('transport_data.csv'):
        if r['iso'] == iso:
            d[r['variable']] = {y: (float(r[str(y)]) if r[str(y)] != '' else 0.0) for y in DATA_YEARS}
    pr = {}
    for r in read('vehicle_prices.csv'):
        if r['iso'] == iso:
            pr[r['variable']] = {int(k): float(v) for k, v in r.items() if k.isdigit() and v != ''}
    ra = {c: None for c in CLS}
    for r in read('range_anxiety.csv'):
        if r['iso'] == iso:
            ra = {'pass': float(r['passenger']), 'fre': float(r['freight']), 'cyc': float(r['cycle'])}
    return d, pr, ra


def range_anxiety(iso, par=None):
    """Start value of range anxiety ($/vehicle) by class: Transport3 stored calibration of the country; if the country
    has none, the Transport3 average (legacy IFERROR fallback), flagged. Returns (values, flag)."""
    par = par or params()
    ra = country_data(iso)[2]
    if all(v is not None for v in ra.values()):
        return ra, ''
    return {c: par[f'ra_avg|{c}'] for c in CLS}, 'no Transport3 value: average of all countries used'


def pv(r, n, pmt):
    """-PV(r, n, pmt) of Excel (end-of-period annuity)."""
    return pmt * n if r == 0 else pmt * (1 - (1 + r) ** -n) / r


def engine(inp, years=YEARS, fix=ALL_FIXES):
    n = len(years)
    P, PA, T1, T2 = inp['par'], inp['paths'], inp['data'], inp['prices']
    nd = sum(1 for y in years if y in DATA_YEARS)            # data columns (legacy L-O)
    o = {}

    def S(r, v=None):
        o[r] = [v] * n
        return o[r]

    def d(var, k):                                           # Transport1 lookup of a data column, else blank
        return T1.get(var, {}).get(years[k], 0.0) if k < nd else None

    z = lambda v: 0.0 if v is None else v
    isnum = lambda v: v is not None
    scen = inp['scen']
    pol = scen > 1
    flag_b1 = pol if 'B1' in fix else True                   # legacy ($C2227 > 1): text > number is TRUE
    el_dg, el_dd, el_eg, el_ed, aei = (inp['el_dem_gso'], inp['el_dem_die'], inp['el_eff_gso'], inp['el_eff_die'],
                                       inp['aei_oil'])
    L = inp['l_ktoe']
    pop, gpc = inp['pop'], inp['gdppc']
    g = lambda key, c: P[f'{key}|{c}']
    J4322, J4324, K4324, L4324 = g('own_years', 'pass'), g('life', 'pass'), g('life', 'fre'), g('life', 'cyc')
    J4323 = J4324 - J4322
    # ================================================================ key inputs 15 (rows 2017-2171)
    y0 = years[0]
    eb = inp['eb']
    sh = {}
    for r, var in ((2017, 'share of gasoline for passenger'), (2018, 'share of gasoline for cycle'),
                   (2020, 'share of diesel for passenger'), (2021, 'share of diesel for bus'),
                   (2022, 'share of diesel for freight'), (2024, 'share of lpg for passenger'),
                   (2025, 'share of lpg for bus'), (2026, 'share of lpg for freight'),
                   (2028, 'share of natural gas for passenger'), (2029, 'share of natural gas for bus'),
                   (2030, 'share of natural gas for freight')):
        sh[r] = T1.get(var, {}).get(y0, 0.0)
    sh[2019] = 1 - sh[2017] - sh[2018]
    sh[2023] = 1 - sh[2020] - sh[2021] - sh[2022]
    sh[2027] = 1 - sh[2024] - sh[2025] - sh[2026]
    sh[2031] = 1 - sh[2028] - sh[2029] - sh[2030]
    for r in range(2017, 2032):
        if r in sh:
            fu, ebv = (('gso', eb['gso'] + eb['bgs']) if r < 2020 else ('die', eb['die'] + eb['bdi']) if r < 2024
                       else ('lpg', eb['lpg']) if r < 2028 else ('nga', eb['nga']))
            m = sh[r] * ebv
            o[f'cL{r}'], o[f'cM{r}'], o[f'cN{r}'] = sh[r], m, m * L[fu] / 10 ** 9
    N_ = lambda r: o[f'cN{r}']
    for r, var in ((2034, 'fuel economy light'), (2036, 'ownership passenger'), (2037, 'ownership light'),
                   (2040, 'fuel economy gasoline passenger'), (2042, 'fuel economy diesel passenger'),
                   (2044, 'fuel economy lpg passenger'), (2046, 'fuel economy cng passenger'),
                   (2048, 'fuel economy phev passenger'), (2050, 'fuel economy ev passenger'),
                   (2058, 'average vkt passenger'), (2059, 'average vkt light'),
                   (2063, 'purchases share ev passenger'), (2064, 'ownership share ev passenger'),
                   (2065, 'purchases share bev passenger'), (2066, 'ownership share bev passenger'),
                   (2067, 'purchases share bev light'), (2068, 'ownership share bev light'),
                   (2092, 'fuel economy diesel freight'), (2093, 'fuel economy lpg freight'),
                   (2094, 'fuel economy lng freight'), (2101, 'purchases share bev freight'),
                   (2102, 'ownership share bev freight'), (2108, 'ownership freight'),
                   (2115, 'average vkt freight'), (2121, 'fuel economy gasoline cycle'),
                   (2126, 'purchases share bev cycle'), (2127, 'ownership share bev cycle'),
                   (2129, 'ownership cycle'), (2133, 'average vkt cycle'), (2150, 'share used vehicles'),
                   (2157, 'duty, ev cycle'), (2158, 'duty, ev freight'), (2159, 'duty, ev passenger'),
                   (2160, 'duty, ice cycle'), (2161, 'duty, ice freight'), (2162, 'duty, ice passenger'),
                   (2163, 'share of passenger imports'), (2164, 'share of freight imports'),
                   (2165, 'ev charging stations'), (2166, 'ownership saturation point')):
        o[r] = [d(var, k) for k in range(n)]
    o[2051], o[2095], o[2122], o[2170] = PA['bev_fe|light'], PA['bev_fe|fre'], PA['bev_fe|cyc'], PA['ch_cost_port']
    rp0 = inp['rp0']
    for r in (2038, 2041, 2043, 2045, 2047, 2049, 2052, 2054, 2055, 2056, 2060, 2061, 2069, 2070, 2072, 2073, 2074,
              2075, 2076, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2086, 2087, 2088, 2097, 2098, 2099, 2104, 2105,
              2106, 2109, 2110, 2112, 2113, 2114, 2116, 2117, 2118, 2124, 2130, 2131, 2134, 2135, 2136, 2137):
        S(r)
    for k in range(nd):
        f = lambda r: o[r][k]
        o[2038][k] = f(2036) / (f(2036) + f(2037))
        s = o[2038][k]
        o[2041][k] = f(2040) * s + f(2034) * (1 - s)
        o[2043][k] = f(2042) * s + f(2034) * (1 - s)
        o[2045][k] = f(2044) * s + f(2034) * f(2044) / f(2040) * (1 - s)
        o[2047][k] = f(2046) * s + f(2034) * f(2046) / f(2040) * (1 - s)
        o[2049][k] = f(2040) / f(2048)
        o[2052][k] = f(2050) * s + f(2051) * (1 - s)
        o[2054][k] = rp0['gso'][k] / f(2041)
        o[2055][k] = (inp['rp0_ele_res_2021'] if k == 0 else rp0['ele_res'][k - 1]) / f(2052)
        o[2056][k] = 1.0 if f(2055) == 0 else min(g('bev_vkt_cap', 'pass'), (f(2055) / f(2054)) ** el_dg)
        o[2060][k] = f(2058) * s + f(2059) * (1 - s)
        o[2061][k] = f(2060) * f(2056)
        o[2069][k] = f(2064) * s + f(2068) * (1 - s)
        o[2070][k] = (f(2064) - f(2066)) * f(2049) * s
        o[2072][k] = f(2041) * (N_(2017) + N_(2019)) * (1 - f(2070))
        o[2073][k] = f(2043) * (N_(2020) + N_(2023))
        o[2074][k] = f(2045) * (N_(2024) + N_(2027))
        o[2075][k] = f(2047) * (N_(2028) + N_(2031))
        o[2076][k] = f(2048) * (N_(2017) + N_(2019)) * f(2070)
    v0 = [o[r][0] for r in (2072, 2073, 2074, 2075)]
    for k in range(nd):
        f = lambda r: o[r][k]
        for i, r in enumerate((2078, 2079, 2080, 2081)):
            o[r][k] = v0[i] / sum(v0) * (1 - f(2069))           # $L2072: the 2022 split in every data year
        o[2083][k] = f(2066) * f(2038) + f(2068) * (1 - f(2038))
        o[2082][k] = f(2069) - f(2083)
        o[2084][k] = sum(f(r) for r in range(2078, 2084))
        o[2086][k] = (f(2036) + f(2037)) * (1 - f(2083))
        o[2087][k] = (f(2036) + f(2037)) - o[2086][k]
        o[2088][k] = f(2065) * f(2038) + f(2067) * (1 - f(2038))
        o[2097][k], o[2098][k], o[2099][k] = N_(2022) * f(2092), N_(2026) * f(2093), N_(2030) * f(2094)
    fv0 = [o[r][0] for r in (2097, 2098, 2099)]
    for k in range(nd):
        f = lambda r: o[r][k]
        o[2104][k] = 1.0 if sum(fv0) == 0 else fv0[0] / sum(fv0) * (1 - f(2102))
        o[2105][k] = 0.0 if sum(fv0) == 0 else fv0[1] / sum(fv0) * (1 - f(2102))
        o[2106][k] = 0.0 if sum(fv0) == 0 else fv0[2] / sum(fv0) * (1 - f(2102))
        o[2109][k] = f(2108) * (1 - f(2102))
        o[2110][k] = f(2108) - o[2109][k]
        o[2112][k] = rp0['die'][k] / (1 + rp0['vatr_die'][k]) / f(2092)
        o[2113][k] = rp0['ele_ind'][k] / f(2095)
        o[2114][k] = 1.0 if f(2113) == 0 else min(g('bev_vkt_cap', 'fre'), (f(2113) / f(2112)) ** el_dd)
        o[2116][k] = f(2114) * f(2115)
        if k == 0:
            o[2117][0] = f(2115) if f(2104) == 0 else f(2097) / (f(2104) * f(2108) / 10 ** 3 * pop[0]) * 10 ** 3
            o[2118][0] = f(2114) * o[2117][0]
        else:
            o[2117][k] = o[2117][k - 1] * f(2060) / o[2060][k - 1]
            o[2118][k] = o[2118][k - 1] * f(2061) / o[2061][k - 1]
        o[2124][k] = N_(2018) * f(2121)
        o[2130][k] = f(2129) * (1 - f(2127))
        o[2131][k] = f(2129) - o[2130][k]
        o[2134][k] = rp0['gso'][k] / f(2121)
        o[2135][k] = rp0['ele_ind'][k] / f(2122)
        o[2136][k] = 1.0 if f(2135) == 0 else min(g('bev_vkt_cap', 'cyc'), (f(2135) / f(2134)) ** el_dg)
        o[2137][k] = f(2133) * f(2136)
    ky = years.index(int(P['bus_ele_year']))
    o['cL2140'], o['cL2141'], o['cL2142'] = o['cM2021'], o['cM2025'], o['cM2029']
    o['cL2143'] = o[2064][ky] * (o['cL2140'] + o['cL2141'] + o['cL2142'])
    for r in (2140, 2141, 2142, 2143):
        o[r] = [o[f'cL{r}']] + [None] * (n - 1)
    for r, fu in ((2017, 'gso'), (2020, 'die'), (2024, 'lpg'), (2028, 'nga')):
        o[f'cC{r}'] = L[fu]
    o['cE2146'] = eb['gso'] / (eb['gso'] + eb['bgs']) if eb['gso'] + eb['bgs'] else 1.0
    o['cE2147'] = eb['die'] / (eb['die'] + eb['bdi']) if eb['die'] + eb['bdi'] else 1.0
    o[2171] = [None] + [(o[2129][k] + o[2108][k] + o[2036][k] + o[2037][k]) /
                        (o[2036][k - 1] + o[2108][k - 1] + o[2129][k - 1]) for k in range(1, nd)] + [None] * (n - nd)
    o[2089] = [years[k] if isnum(o[2036][k]) else 0 for k in range(n)]
    o['cE2089'] = max(o[2089])
    klast = years.index(int(o['cE2089']))                     # last data year found in the data
    kc = klast if 'B3b' in fix else years.index(int(P['own_calib_year']))
    for r, var in ((2151, 'icev_price_passenger'), (2152, 'ev_price_passenger'), (2153, 'icev_price_freight'),
                   (2154, 'ev_price_freight'), (2155, 'icev_price_cycle'), (2156, 'ev_price_cycle')):
        S(r)
        for k in range(n):
            o[r][k] = T2.get(var, {}).get(years[k], o[r][k - 1] if k else 0.0)   # IFERROR(..., previous year)
    o[2167] = list(gpc)
    H2168, I2168 = P['fre_inc_target'], P['fre_share_target']
    N2168 = o[2108][kc] / (o[2036][kc] + o[2037][kc])
    o['cH2168'], o['cI2168'] = H2168, I2168
    o[2168] = [o[2108][k] / (o[2036][k] + o[2037][k]) if isnum(o[2108][k]) else
               min(N2168, max(I2168, N2168 - (N2168 - I2168) * gpc[k] / H2168)) for k in range(n)]
    H2169, I2169 = P['cyc_peak_inc'], P['cyc_scale']
    J2169 = (1 + (1 - gpc[kc] / H2169) * I2169) * o[2129][kc]
    o['cH2169'], o['cI2169'], o['cJ2169'] = H2169, I2169, J2169
    o[2169] = [o[2129][k] if isnum(o[2129][k]) else 2 * J2169 * H2169 * gpc[k] / (gpc[k] ** 2 + H2169 ** 2)
               for k in range(n)]
    # ================================================================ side table: country-specific policy cells
    ycu = years.index(int(P['customs_year']))
    yim = years.index(int(P['import_year']))
    vat = inp['vat_veh']
    side = {'V4304': vat, 'V4305': vat, 'V4306': vat * P['vat_pol_factor'],
            'X4304': vat, 'X4305': vat, 'X4306': vat * P['vat_pol_factor'],
            'V4308': o[2162][ycu], 'W4308': o[2161][ycu], 'X4308': o[2160][ycu],
            'V4309': o[2159][ycu], 'W4309': o[2158][ycu], 'X4309': o[2157][ycu],
            'V4312': o[2163][yim], 'W4312': o[2164][yim]}
    side['V4310'], side['W4310'], side['X4310'] = (side['V4309'] * P['cust_pol_factor'],
                                                   side['W4309'] * P['cust_pol_factor'],
                                                   side['X4309'] * P['cust_pol_factor'])
    side['X4312'] = side['V4312']
    for c in ('V', 'X'):
        side[f'{c}4307'] = P['vat_year|' + ('pass' if c == 'V' else 'cyc')]
    for c, cl in zip('VWX', CLS):
        side[f'{c}4311'] = P['cust_year|' + cl]
    for kk, vv in side.items():
        o['c' + kk] = vv
    # emission factors (tCO2 per liter) and the biofuel adjustment
    ef = inp['ef'] if 'B7' in fix else inp['ef_name']
    G4375 = inp['ef']['gso'] * o['cE2146']
    G4376 = ef['die'] * o['cE2147']
    G4377 = ef['lpg']
    G4378 = ef['nga_gj'] / P['gas_l_per_gj']
    G4419, G4420, G4421, G4441 = G4376, G4377, G4378, G4375
    for kk, vv in (('G4375', G4375), ('G4376', G4376), ('G4377', G4377), ('G4378', G4378), ('G4419', G4419),
                   ('G4420', G4420), ('G4421', G4421), ('G4441', G4441)):
        o['c' + kk] = vv
    # discount rates
    wacc = inp['wacc_avg']
    o['cK4329'] = wacc
    disc = [min(P['disc_max'], max(P['disc_min'], P['disc_max'] - (gpc[k] - P['disc_inc_low']) /
                                   (P['disc_inc_high'] - P['disc_inc_low']) * (P['disc_max'] - P['disc_min'])))
            for k in range(n)]
    o[4531] = disc
    o[4530] = list(gpc)
    rfre = (lambda k: disc[k]) if 'B8w' in fix else (lambda k: wacc)
    # ================================================================ allocate section rows
    rows_sec = [r for r in range(4334, 5379)]
    for r in rows_sec:
        if r not in o:
            S(r)
    rp = inp['rp']
    gdpg = inp['gdp_growth']
    gdpg_lag = [inp['gdp_growth_2021']] + gdpg[:-1]
    ra0 = inp['ra']
    for c, r in zip(CLS, (4354, 4355, 4356)):
        for k in range(min(3, n)):
            o[r][k] = ra0[c]                                  # L = M = N = Transport3 (or Dashboard)
    eb_rod = inp['eb']
    # ================================================================ year loop
    for k in range(n):
        y = years[k]
        dk = k < nd
        col = k + 1
        X = lambda r, kk=k: o[r][kk]
        Xp = lambda r: o[r][k - 1] if k > 0 else None           # K column: blank
        zp = lambda r: z(Xp(r))

        def put(r, v):
            o[r][k] = v
        # ---------------- stock openings (rows 4740-4779, 4876-4895, 4956-4975)
        put(4739, col)
        put(4740, o[2150][k] if dk else o[4740][k - 1])
        put(4741, J4322 * (1 - X(4740)) + J4324 * X(4740))
        put(4742, o[2086][k] if dk else None)
        put(4760, X(4740))
        put(4761, o[2087][k] if dk else None)
        own_old = lambda r: (z(X(r[0])) > 0)

        def opening(r, base, frac, closing_row):
            v = o[base][k]
            put(r, z(v) * frac if z(v) > 0 else zp(closing_row))

        def depr(r_open, life, r_base, r_dep, r_after):
            m = int(min(life, col))
            put(r_base, sum(o[r_open][k - m + 1:k + 1]) / m)
            put(r_dep, min(X(r_base) / life, X(r_open)))
            put(r_after, X(r_open) - X(r_dep))
        opening(4744, 4742, 1 - X(4740), 4750)
        depr(4744, J4322, 4745, 4746, 4747)
        opening(4752, 4742, X(4740), 4758)
        depr(4752, J4324 - J4322, 4753, 4754, 4755)
        opening(4763, 4761, 1 - X(4760), 4769)
        depr(4763, J4322, 4764, 4765, 4766)
        opening(4771, 4761, X(4760), 4777)
        depr(4771, J4324 - J4322, 4772, 4773, 4774)
        put(4778, (X(4771) + X(4763)) / (X(4771) + X(4763) + X(4752) + X(4744)))
        put(4779, X(4771) + X(4763) + X(4752) + X(4744))
        put(4875, col)
        put(4876, o[2109][k] if dk else None)
        put(4886, o[2110][k] if dk else None)
        opening(4878, 4876, 1.0, 4884)
        depr(4878, K4324, 4879, 4880, 4881)
        opening(4888, 4886, 1.0, 4894)
        depr(4888, K4324, 4889, 4890, 4891)
        put(4895, X(4888) / (X(4888) + X(4878)))
        put(4955, col)
        put(4956, o[2130][k] if dk else None)
        put(4966, o[2131][k] if dk else None)
        opening(4958, 4956, 1.0, 4964)
        depr(4958, L4324, 4959, 4960, 4961)
        opening(4968, 4966, 1.0, 4974)
        depr(4968, L4324, 4969, 4970, 4971)
        put(4975, X(4968) / (X(4968) + X(4958)))
        # ---------------- charging stations and range anxiety (4334-4356)
        put(4334, y)
        put(4335, X(4763)); put(4336, X(4771)); put(4337, X(4888)); put(4338, X(4968)); put(4339, pop[k])
        put(4340, (X(4335) + X(4336) + X(4337) + X(4338)) * X(4339) / 1000)
        put(4342, o[2170][k])
        if scen == 1:
            sub = 0.0
        elif 'B10' in fix:
            y1, y2, l1, l2 = P['cs_start_year'], P['cs_target_year'], P['cs_start_level'], P['cs_target_level']
            sub = 0.0 if y < y1 else (l2 if y >= y2 else l1 + (l2 - l1) * (y - y1) / (y2 - y1))
        elif y == P['cs_start_year']:
            sub = P['cs_start_level']
        else:
            sub = min(1, max(0, zp(4343) + (P['cs_target_level'] - P['cs_start_level']) /
                             (P['cs_target_year'] - P['cs_start_year'])))
        put(4343, sub)
        put(4344, X(4342) * (1 - X(4343)))
        put(4345, X(4342) * X(4343))
        if dk:
            put(4347, o[2165][k])
        else:
            put(4347, o[4347][k - 1] * (X(4340) / o[4340][k - 1]) ** P['ch_el_stock'] *
                (X(4344) / o[4344][k - 1]) ** P['ch_el_cost'])
        if k > 0:
            put(4348, X(4347) - o[4347][k - 1] + o[4347][k - 1] / P['station_life'])
        put(4349, X(4778))
        put(4350, max(P['ch_cost_min'], P['ch_cost_max'] * (P['ch_sat'] - X(4349)) / (1 - P['ch_sat'])) *
            P['ch_public'])
        put(4351, inp['pp_res'][max(k - 1, 0)] + X(4350))
        put(4352, inp['pp_ind'][max(k - 1, 0)] + X(4350))
        if k >= 3:
            for r, c in ((4354, 'pass'), (4355, 'fre'), (4356, 'cyc')):
                prev = o[r][k - 1]
                put(r, prev if prev < 0 else max(prev * (1 - P['ra_decline|' + c]) *
                                                  (X(4347) / o[4347][k - 1]) ** P['ra_el_stations'], 0))
        # ---------------- fuel economy, passenger (4358-4407)
        put(4358, y); put(4359, col)
        for i, r in enumerate(range(4360, 4365)):
            put(r, o[2078 + i][k] if dk else o[4861 + i][k - 1])
        put(4365, X(4351))
        put(4366, o[2049][k] if dk else o[4366][k - 1])
        put(4367, rp['gso'][k]); put(4368, rp['die'][k]); put(4369, rp['lpg'][k])
        put(4370, rp['nga_res'][k] / P['gas_l_per_gj'])
        put(4371, X(4367) * X(4366) + X(4365) * (1 - X(4366)) * P['phev_l_per_kwh'])
        sw = sum(X(r) for r in range(4360, 4365))
        put(4372, sum(X(4367 + i) * X(4360 + i) for i in range(5)) / sw)
        put(4374, ((P['fb_rate|pass'] if y >= P['fb_year|pass'] else 0) + inp['cprice'][k] * inp['fb_cov'][k]) * pol)
        for r, G in ((4375, G4375), (4376, G4376), (4377, G4377), (4378, G4378), (4379, G4375)):
            put(r, X(4374) * G)
        if k > 0:
            for i in range(4):
                put(4380 + i, (X(4367 + i) + X(4375 + i)) / (o[4367 + i][k - 1] + o[4375 + i][k - 1]))
            put(4384, (X(4372) + X(4379)) / (o[4372][k - 1] + o[4379][k - 1]))
        for i, (rr, src) in enumerate(((4386, 2041), (4387, 2043), (4388, 2045), (4389, 2047), (4390, 2048))):
            put(rr, o[src][k] * (1 + g('fe_gap', 'pass')) if dk else
                o[rr][k - 1] * X(4380 + i) ** abs(el_eg) * (1 + aei))
        put(4391, sum(X(4386 + i) * X(4360 + i) for i in range(5)) / sw)
        Gp = (G4375, G4376, G4377, G4378, G4375)
        for i in range(5):
            put(4392 + i, Gp[i] / X(4386 + i) * 10 ** 6)
        put(4397, sum(X(4360 + i) * Gp[i] for i in range(5)) / X(4391) * 10 ** 6 / sw)
        put(4399, PA['bev_fe_new|pass'][k])
        m7 = min(col, J4322)
        put(4401, sum(o[4391][k - int(m7) + 1:k + 1]) / m7)
        put(4402, o[4397][k - int(m7) + 1])
        put(4403, o[4399][k - int(m7) + 1])
        # 4404/4405 need this year's lagged choice shares (rows 4808/4821 = last year's 4806/4819)
        put(4808, 1 - o[2088][0] if k == 0 else o[4806][k - 1])
        put(4821, None if k == 0 else o[4819][k - 1])
        put(4404, X(4808))
        put(4406, o[2150][k] if dk else o[4406][k - 1])
        # ---------------- fuel economy, freight (4409-4435)
        put(4409, y)
        put(4410, rp['die'][k] - inp['vat_die'][k])
        put(4411, rp['lpg'][k] - inp['vat_lpg'][k])
        put(4412, (rp['nga_ind'][k] - inp['vat_nga_ind'][k]) / P['gas_l_per_gj'])
        for i in range(3):
            put(4413 + i, o[2104 + i][k] if dk else o[4945 + i][k - 1])
        swf = sum(X(4413 + i) for i in range(3))
        put(4416, sum(X(4413 + i) * X(4410 + i) for i in range(3)) / swf)
        put(4418, ((P['fb_rate|fre'] if y >= P['fb_year|fre'] else 0) + inp['cprice'][k] * inp['fb_cov'][k]) * pol)
        for i, G in enumerate((G4419, G4420, G4421)):
            put(4419 + i, X(4418) * G)
        if k > 0:
            for i in range(3):
                put(4422 + i, (X(4410 + i) + X(4419 + i)) / (o[4410 + i][k - 1] + o[4419 + i][k - 1]))
        for i, src in enumerate((2092, 2093, 2094)):
            put(4425 + i, o[src][k] * (1 + g('fe_gap', 'fre')) if dk else
                o[4425 + i][k - 1] * X(4422 + i) ** abs(el_ed) * (1 + aei))
        put(4428, sum(X(4425 + i) * X(4413 + i) for i in range(3)) / swf)
        for i, G in enumerate((G4419, G4420, G4421)):
            put(4429 + i, G / X(4425 + i) * 10 ** 6)
        put(4432, sum((G4419, G4420, G4421)[i] * X(4413 + i) for i in range(3)) / swf / X(4428) * 10 ** 6)
        put(4433, PA['bev_fe_new|fre'][k])
        put(4919, o[4917][k - 1] if k > 0 else 1 - z(o[2101][0]))   # L4919 = L4917 = 1 - L4916 (data)
        put(4434, X(4919))
        if k > 0:
            put(4435, X(4434) * o[4432][k - 1])
        # ---------------- fuel economy, 2-3 wheelers (4437-4448)
        put(4437, y)
        put(4438, (inp['sp_gso'][k] + inp['txo_gso'][k]) * (1 + inp['vatr_gso'][k]))
        put(4440, ((P['fb_rate|cyc'] if y >= P['fb_year|cyc'] else 0) + inp['cprice'][k] * inp['fb_cov'][k]) * pol)
        put(4441, X(4440) * G4441)
        if k > 0:
            put(4442, (X(4438) + X(4441)) / (o[4438][k - 1] + o[4441][k - 1]))
        put(4444, o[2121][k] * (1 + g('fe_gap', 'cyc')) if dk else o[4444][k - 1] * X(4442) ** abs(el_eg) * (1 + aei))
        put(4445, G4441 / X(4444) * 10 ** 6)
        put(4446, PA['bev_fe_new|cyc'][k])
        put(4995, 1 - z(o[2126][0]) if k == 0 else o[4993][k - 1])
        put(4447, X(4995))
        if k > 0:
            put(4448, X(4447) * o[4445][k - 1])
        # ---------------- distance driven (4450-4505)
        put(4450, y)
        for r, c, flag in ((4451, 'pass', flag_b1), (4479, 'fre', pol), (4497, 'cyc', pol)):
            if y == P['dt_year|' + c]:
                v = P['dt_start|' + c]
            else:
                v = min(P['dt_target|' + c], zp(r) + (P['dt_target|' + c] - P['dt_start|' + c]) /
                        (P['dt_target_year|' + c] - P['dt_year|' + c]))
            put(r, v * (y >= P['dt_year|' + c]) * flag)
        for i in range(5):
            put(4452 + i, X(4367 + i) / X(4386 + i) + X(4451))
            if k > 0:
                put(4457 + i, X(4452 + i) / o[4452 + i][k - 1])
        put(4463, gdpg_lag[k])
        vp = P['vkt_new_price'] != 'No'
        if dk:
            put(4464, o[2060][k])
            put(4465, X(4464)); put(4466, X(4465)); put(4467, X(4466)); put(4468, X(4467)); put(4469, X(4466))
        else:
            for i in range(5):
                put(4465 + i, o[4465 + i][k - 1] * (X(4457 + i) if vp else 1) ** el_dg *
                    (1 + X(4463)) ** g('inc_el_vkt', 'pass'))
        put(4470, sum(X(4465 + i) * X(4360 + i) for i in range(5)) / sw)
        put(4472, X(4351) / X(4399) + X(4451))
        if k > 0:
            put(4473, X(4472) / o[4472][k - 1])
        put(4474, o[2061][k] if dk else o[4474][k - 1] * (X(4473) if vp else 1) ** el_dg *
            (1 + X(4463)) ** g('inc_el_vkt', 'pass'))
        put(4475, X(4470) * (X(4391) / X(4401)) ** el_dg)
        put(4476, X(4474) * (X(4399) / X(4403)) ** el_dg)
        put(4478, y)
        for i in range(3):
            put(4480 + i, X(4410 + i) / X(4425 + i) + X(4479))
            if k > 0:
                put(4483 + i, X(4480 + i) / o[4480 + i][k - 1])
        put(4487, X(4463) if (y < 2038 or 'B2' in fix) else inp['row2455'][k])
        vmin, vmax = P['fre_vkt_min'], P['fre_vkt_max']
        for i in range(3):
            put(4488 + i, o[2115][k] if dk else max(vmin, min(vmax, o[4488 + i][k - 1] * (X(4483 + i) if vp else 1)
                                                              ** el_dd * (1 + X(4487)) ** g('inc_el_vkt', 'fre'))))
        put(4491, sum(X(4488 + i) * X(4413 + i) for i in range(3)) / swf)
        put(4492, X(4352) / X(4433) + X(4479))
        if k > 0:
            put(4493, X(4492) / o[4492][k - 1])
        put(4494, o[2116][k] if dk else max(vmin, min(vmax, o[4494][k - 1] * (X(4493) if vp else 1) ** el_dd *
                                                      (1 + X(4487)) ** g('inc_el_vkt', 'fre'))))
        put(4496, y)
        put(4498, X(4438) / X(4444) + X(4497))
        if k > 0:
            put(4499, X(4498) / o[4498][k - 1])
        put(4501, X(4487))
        put(4502, o[2133][k] if dk else o[4502][k - 1] * (X(4499) if vp else 1) ** el_dg *
            (1 + X(4501)) ** g('inc_el_vkt', 'cyc'))
        put(4503, X(4351) / X(4446) + X(4497))
        if k > 0:
            put(4504, X(4503) / o[4503][k - 1])
        put(4505, o[2137][k] if dk else o[4505][k - 1] * (X(4504) if vp else 1) ** el_dg *
            (1 + X(4501)) ** g('inc_el_vkt', 'cyc'))
        # ---------------- TCO, passenger new (4507-4582)
        r_ = disc[k]
        put(4507, y)
        put(4508, X(4470)); put(4509, pv(r_, J4322, X(4508))); put(4510, pv(r_, J4324, X(4508)))
        put(4512, X(4474)); put(4513, pv(r_, J4322, X(4512))); put(4514, pv(r_, J4324, X(4512)))
        # feebate pivot (4517) needs this year's 4516 = 4407 (lagged fuel economy of sales)
        put(4405, X(4821))
        if k > 0:
            put(4407, o[4397][k - 1] * X(4404) * (1 - X(4406)) + o[4402][k - 1] * X(4405) * X(4406))
        put(4516, z(X(4407)))

        def pivot(r_piv, r_avg, c):
            if k < 2:
                return
            if P['fb_pivot_type|' + c] == 'Average':
                put(r_piv, o[r_avg][k] * o[r_avg][k] / o[r_avg][k - 1])
            elif y == P['fb_year|' + c]:
                put(r_piv, P['fb_pivot|' + c])
            elif y > P['fb_year|' + c]:
                put(r_piv, max(0, z(o[r_piv][k - 1]) - P['fb_pivot_chg|' + c]))
            else:
                put(r_piv, 0)
        pivot(4517, 4516, 'pass')
        put(4518, X(4374)); put(4519, X(4397))
        if k > 0:
            put(4520, (X(4519) - z(X(4517))) * X(4518) / 10 ** 6 * X(4509))
            put(4521, (0 - z(X(4517))) * X(4518) / 10 ** 6 * X(4513))
        J4325, J4326, J4327, J4328 = g('dep1', 'pass'), g('ins', 'pass'), g('maint_ice', 'pass'), g('maint_ev', 'pass')
        insf = P['ins_factor']
        put(4523, o[2151][k])
        put(4524, side['V4308'] * side['V4312'])
        put(4525, P['adv_ice_base|pass'] if scen == 1 or y < P['adv_year|pass'] else P['adv_ice_pol|pass'])
        put(4526, side['V4304'])
        put(4527, X(4523) * (1 + X(4524)) * (1 + X(4525)) * (1 + X(4526)) + z(X(4520)))
        put(4528, X(4527) - X(4523) - z(X(4520)))
        put(4533, X(4527) * J4325)
        put(4534, ((X(4527) - X(4533)) / (J4324 - 1)) / r_ * (1 - (1 / (1 + r_) ** (J4324 - 1))))
        put(4535, min(0, X(4527) * -1 * ((J4324 - J4322) / J4324 * (1 - J4325)) / (1 + r_) ** J4322))
        put(4537, X(4523) * (1 - (J4325 + (J4322 - 1) / (J4324 - 1) * (1 - J4325))))
        put(4538, X(4537) * (1 + X(4524)) * (1 + X(4525)) * (1 + X(4526)))
        put(4539, X(4538) - X(4537))
        put(4541, (X(4527) * J4326) / r_ * (1 - (1 / (1 + r_) ** (J4322 + 1))) * insf + J4327 * X(4509))
        put(4543, X(4372)); put(4544, X(4391)); put(4545, X(4451))
        put(4546, X(4543) / X(4544) * X(4509) + X(4545) * X(4509))
        put(4548, X(4533) + X(4534) + X(4535) + X(4541) + X(4546))
        put(4549, X(4548) / X(4509))
        dep_ice = X(4533) + X(4534) + X(4535)
        for i in range(4):
            put(4551 + i, X(4509) * X(4452 + i) + dep_ice + X(4541) + z(X(4520)) * X(4392 + i) / X(4397))
        put(4557, o[2152][k])
        put(4558, (side['V4309'] if scen == 1 or y < side['V4311'] else side['V4310']) * side['V4312'])
        put(4559, P['adv_bev_base|pass'] if scen == 1 or y < P['adv_year|pass'] else P['adv_bev_pol|pass'])
        put(4560, side['V4305'] if scen == 1 or y < side['V4307'] else side['V4306'])
        if y == P['sub_year|pass']:
            v = -P['sub_amount|pass']
        elif y > P['sub_year|pass']:
            v = min(0, zp(4561) - P['sub_chg|pass'])
        else:
            v = 0
        put(4561, v * pol)
        put(4562, X(4557) * (1 + X(4558)) * (1 + X(4560)) * (1 + X(4559)) + X(4561) + z(X(4521)))
        put(4563, X(4562) - X(4557) - z(X(4521)) - X(4561))
        put(4565, X(4562) * J4325)
        put(4566, ((X(4562) - X(4565)) / (J4324 - 1)) / r_ * (1 - (1 / (1 + r_) ** (J4324 - 1))))
        put(4567, min(0, X(4562) * -1 * ((J4324 - J4322) / J4324 * (1 - J4325)) / (1 + r_) ** J4322))
        put(4569, X(4557) * (1 - (J4325 + (J4322 - 1) / (J4324 - 1) * (1 - J4325))))
        put(4570, X(4569) * (1 + X(4558)) * (1 + X(4559)) * (1 + X(4560)))
        put(4571, X(4570) - X(4569))
        put(4573, (X(4562) * J4326) / r_ * (1 - (1 / (1 + r_) ** (J4322 + 1))) * insf +
            (J4328 if 'B19' in fix else J4327) * X(4513))
        put(4575, X(4351)); put(4576, X(4399))
        put(4577, X(4575) / X(4576) * X(4513) + X(4545) * X(4513))
        put(4579, X(4354))
        put(4581, X(4565) + X(4566) + X(4567) + X(4573) + X(4577) + X(4579))
        put(4582, X(4581) / X(4513))
        put(4555, X(4509) * X(4456) + X(4565) + X(4566) + X(4567) + X(4541) + z(X(4520)) * X(4396) / X(4397) +
            (0.0 if 'B23' in fix else X(4579)))
        # ---------------- TCO, passenger used (4584-4624)
        put(4584, y)
        put(4585, X(4475)); put(4586, pv(r_, J4323, X(4585)))
        put(4587, X(4476)); put(4588, pv(r_, J4323, X(4587)))
        put(4590, z(X(4517))); put(4591, X(4374)); put(4592, X(4402))
        if k > 0:
            put(4593, (X(4592) - z(X(4590))) * X(4591) / 10 ** 6 * X(4586))
            put(4594, (0 - z(X(4590))) * X(4591) / 10 ** 6 * X(4588))
        put(4596, X(4538)); put(4597, X(4596) + z(X(4593)))
        nused = (J4323 if 'B20' in fix else J4322) - 1
        put(4598, (X(4597) / nused) / r_ * (1 - (1 / (1 + r_) ** nused)))
        put(4600, (X(4597) * J4326) / r_ * (1 - (1 / (1 + r_) ** (J4323 + 1))) * insf + J4327 * X(4586))
        put(4602, X(4372)); put(4603, X(4401)); put(4604, X(4451))
        put(4605, X(4602) / X(4603) * X(4586) + X(4604) * X(4586))
        put(4607, X(4598) + X(4600) + X(4605))
        put(4608, X(4607) / X(4586))
        put(4610, X(4570)); put(4611, X(4561)); put(4612, X(4610) + z(X(4594)) + X(4611))
        put(4613, (X(4612) / (J4323 - 1)) / r_ * (1 - (1 / (1 + r_) ** (J4323 - 1))))
        put(4615, (X(4612) * J4326) / r_ * (1 - (1 / (1 + r_) ** (J4323 + 1))) * insf + J4328 * X(4588))
        put(4617, X(4351)); put(4618, X(4403))
        put(4619, X(4617) / X(4618) * X(4588) + X(4604) * X(4588))
        put(4621, X(4579) * X(4612) / X(4562))
        put(4623, X(4613) + X(4615) + X(4619) + X(4621))
        put(4624, X(4623) / X(4588))
        # ---------------- TCO, freight new (4626-4681)
        K4325, K4326, K4327, K4328 = g('dep1', 'fre'), g('ins', 'fre'), g('maint_ice', 'fre'), g('maint_ev', 'fre')
        rf = rfre(k)
        put(4626, y)
        put(4627, X(4491)); put(4628, pv(rf, K4324, X(4627)))
        put(4629, X(4494)); put(4630, pv(rf, K4324, X(4629)))
        put(4632, z(X(4435)))
        pivot(4633, 4632, 'fre')
        put(4634, X(4418)); put(4635, X(4432))
        if k > 0:
            put(4636, (X(4635) - z(X(4633))) * X(4634) / 10 ** 6 * X(4628))
            put(4637, (0 - z(X(4633))) * X(4634) / 10 ** 6 * X(4628))
        put(4639, o[2153][k])
        put(4640, side['W4308'] * side['W4312'])
        put(4641, P['adv_ice_base|fre'] if scen == 1 or y < P['adv_year|fre'] else P['adv_ice_pol|fre'])
        put(4642, X(4639) * (1 + X(4640)) * (1 + X(4641)) + z(X(4636)))
        put(4643, X(4642) - X(4639) - z(X(4636)))
        put(4645, X(4642) * K4325)
        rd = rf if (k == 0 or 'B8' in fix) else disc[k]
        put(4646, ((X(4642) - X(4645)) / (K4324 - 1)) / rd * (1 - (1 / (1 + rd) ** (K4324 - 1))))
        put(4648, (X(4642) * K4326) / rf * (1 - (1 / (1 + rf) ** (K4324 + 1))) * insf + K4327 * X(4628))
        put(4650, X(4416)); put(4651, X(4428)); put(4652, X(4479))
        put(4653, X(4650) / X(4651) * X(4628) + X(4628) * X(4652))
        put(4655, X(4645) + X(4646) + X(4648) + X(4653))
        put(4656, X(4655) / X(4628))
        for i in range(3):
            put(4658 + i, X(4628) * X(4480 + i) + X(4645) + X(4646) + X(4648) + z(X(4636)) * X(4429 + i) / X(4432))
        put(4662, o[2154][k])
        put(4663, (side['W4309'] if scen == 1 or y < side['W4311'] else side['W4310']) * side['W4312'])
        put(4664, P['adv_bev_base|fre'] if scen == 1 or y < P['adv_year|fre'] else P['adv_bev_pol|fre'])
        if y == P['sub_year|fre']:
            v = -P['sub_amount|fre']
        elif y > P['sub_year|fre']:
            v = min(0, zp(4665) - P['sub_chg|fre'])
        else:
            v = 0
        put(4665, v * pol)
        put(4666, X(4662) * (1 + X(4663)) * (1 + X(4664)) + z(X(4637)) + X(4665))
        put(4667, X(4666) - X(4662) - z(X(4637)) - X(4665))
        put(4669, X(4666) * K4325)
        put(4670, ((X(4666) - X(4669)) / (K4324 - 1)) / rf * (1 - (1 / (1 + rf) ** (K4324 - 1))))
        put(4672, (X(4666) * K4326) / rf * (1 - (1 / (1 + rf) ** (K4324 + 1))) * insf + K4328 * X(4630))
        put(4674, X(4352)); put(4675, X(4433))
        put(4676, X(4674) / X(4675) * X(4630) + X(4630) * X(4652))
        put(4678, X(4355))
        put(4680, X(4669) + X(4670) + X(4672) + X(4676) + X(4678))
        put(4681, X(4680) / X(4630))
        # ---------------- TCO, 2-3 wheelers (4683-4736)
        L4325, L4326, L4327, L4328 = g('dep1', 'cyc'), g('ins', 'cyc'), g('maint_ice', 'cyc'), g('maint_ev', 'cyc')
        put(4683, y)
        put(4684, X(4502)); put(4685, pv(r_, L4324, X(4684)))
        put(4686, X(4505)); put(4687, pv(r_, L4324, X(4686)))
        put(4689, z(X(4448)))
        pivot(4690, 4689, 'cyc')
        put(4691, X(4440)); put(4692, X(4445))
        if k > 0:
            put(4693, (X(4692) - z(X(4690))) * X(4691) / 10 ** 6 * X(4685))
            put(4694, (0 - z(X(4690))) * X(4691) / 10 ** 6 * X(4687))
        put(4696, o[2155][k])
        put(4697, side['X4308'] * side['X4312'])
        put(4698, P['adv_ice_base|cyc'] if scen == 1 or y < P['adv_year|cyc'] else P['adv_ice_pol|cyc'])
        put(4699, side['X4304'])
        put(4700, X(4696) * (1 + X(4697)) * (1 + X(4699)) * (1 + X(4698)) + z(X(4693)))
        put(4701, X(4700) - X(4696) - z(X(4693)))
        put(4703, X(4700) * L4325)
        put(4704, ((X(4700) - X(4703)) / (L4324 - 1)) / r_ * (1 - (1 / (1 + r_) ** (L4324 - 1))))
        put(4706, (X(4700) * L4326) / r_ * (1 - (1 / (1 + r_) ** (L4324 + 1))) * insf + L4327 * X(4685))
        put(4708, X(4438)); put(4709, X(4444)); put(4710, X(4497))
        put(4711, X(4708) / X(4709) * X(4685) + X(4710) * X(4685))
        put(4713, X(4703) + X(4704) + X(4706) + X(4711))
        put(4714, X(4713) / X(4685))
        put(4716, o[2156][k])
        put(4717, (side['X4309'] if scen == 1 or y < side['X4311'] else side['X4310']) * side['X4312'])
        put(4718, P['adv_bev_base|cyc'] if scen == 1 or y < P['adv_year|cyc'] else P['adv_bev_pol|cyc'])
        put(4719, side['X4305'] if scen == 1 or y < side['X4307'] else side['X4306'])
        if y == P['sub_year|cyc']:
            v = -P['sub_amount|cyc']
        elif y > P['sub_year|cyc']:
            v = min(0, zp(4720) - P['sub_chg|cyc'])
        else:
            v = 0
        put(4720, v * flag_b1)
        put(4721, X(4716) * (1 + X(4717)) * (1 + X(4719)) * (1 + X(4718)) + z(X(4694)) + X(4720))
        put(4722, X(4721) - X(4716) - X(4720) - z(X(4694)))
        put(4724, X(4721) * L4325)
        put(4725, ((X(4721) - X(4724)) / (L4324 - 1)) / r_ * (1 - (1 / (1 + r_) ** (L4324 - 1))))
        put(4727, (X(4721) * L4326) / r_ * (1 - (1 / (1 + r_) ** (L4324 + 1))) * insf + L4328 * X(4687))
        put(4729, X(4351)); put(4730, X(4446))
        put(4731, X(4729) / X(4730) * X(4687) + X(4710) * X(4687))
        put(4733, X(4356))
        put(4735, X(4724) + X(4725) + X(4727) + X(4731) + X(4733))
        put(4736, X(4735) / X(4687))
        # ---------------- demand, choice and stock, passenger (4781-4872)
        put(4738, y)
        put(4781, o[2166][k] if dk else o[4781][k - 1])
        put(4782, o[2168][k])
        put(4783, X(4781) * (1 - X(4782)))
        put(4784, gpc[k])
        gomp = lambda sat, inc, b: sat * math.exp(P['gomp_a'] * math.exp(inc * b / 1000))
        if k == 0:
            kx = klast if 'B3' in fix else years.index(int(P['own_calib_year']))
            # H4787/I4787 (expected and actual ownership) need columns kx: computed from data rows directly
            sat_kx = o[2166][kx] * (1 - o[2168][kx])
            H = gomp(sat_kx, gpc[kx], g('own_gomp_b', 'pass'))
            I = o[2087][kx] + o[2086][kx]
            o['cH4787'], o['cI4787'] = H, I
            o['cJ4787'] = I / H if 'B3' in fix else max(1, I / H)
            satf = o[2166][kx] * o[2168][kx]
            H = gomp(satf, gpc[kx], g('own_gomp_b', 'fre'))
            I = o[2110][kx] + o[2109][kx]
            o['cH4903'], o['cI4903'] = H, I
            o['cJ4903'] = I / H if 'B3' in fix else max(1, I / H)
        dec_p = OWN_DECLINE_FIX if 'B4' in fix else g('own_max_decline', 'pass')
        dec_f = OWN_DECLINE_FIX if 'B4' in fix else g('own_max_decline', 'fre')
        if z(X(4742)) > 0:
            put(4786, X(4742) + X(4761)); put(4787, X(4742) + X(4761))
        else:
            a = g('own_adj', 'pass')
            put(4786, a * gomp(X(4783), X(4784), g('own_gomp_b', 'pass')) * o['cJ4787'] + (1 - a) * zp(4787))
            put(4787, max(zp(4787) * (1 - dec_p), min(zp(4787) * (1 + g('own_max_growth', 'pass')), X(4786))))
        put(4788, X(4747) + X(4755) + X(4766) + X(4774))
        put(4789, X(4787) - X(4788))
        put(4790, X(4789) * (1 - X(4740)))
        put(4791, X(4789) - X(4790))
        if k > 0:
            put(4792, (X(4787) - o[4787][k - 1]) / X(4787))
            put(4793, (X(4787) - X(4788)) / X(4787))
            put(4794, 1 - X(4792) - X(4793))
        put(4796, X(4808)); put(4797, X(4549)); put(4798, X(4582))
        put(4799, X(4797) * X(4796) + X(4798) * (1 - X(4796)))
        kp = g('k', 'pass')
        put(4800, math.exp(-kp * X(4797) / X(4799)) * 10 ** 3)
        put(4801, math.exp(-kp * X(4798) / X(4799)) * 10 ** 3)
        put(4802, X(4800) / (X(4800) + X(4801)))
        put(4803, 1 - X(4802))
        put(4805, o[2088][k] if dk else None)
        put(4806, 1 - X(4805) if isnum(X(4805)) else X(4802))
        put(4807, 1 - X(4806))
        if k == 0:
            put(4821, None)
        put(4810, X(4821)); put(4811, X(4608)); put(4812, X(4624))
        w = X(4796) if k == 0 else X(4810)
        put(4813, X(4811) * w + X(4812) * (1 - w))
        put(4814, math.exp(-kp * X(4811) / X(4813)) * 10 ** 3)
        put(4815, math.exp(-kp * X(4812) / X(4813)) * 10 ** 3)
        put(4816, X(4814) / (X(4814) + X(4815)))
        put(4817, 1 - X(4816))
        put(4819, 1 - X(4805) if isnum(X(4805)) else X(4816))
        put(4820, 1 - X(4819))
        if k == 0:
            put(4821, X(4819)); put(4810, X(4821))
            put(4405, X(4821))
        put(4823, X(4806) * X(4790)); put(4824, X(4807) * X(4790))
        put(4825, X(4819) * X(4791)); put(4826, X(4820) * X(4791))
        put(4827, X(4817) * X(4740) + X(4803) * (1 - X(4740)))
        put(4828, X(4805) if z(X(4805)) > 0 else X(4817) * X(4740) + X(4803) * (1 - X(4740)))
        put(4829, zp(4828))
        # closings
        put(4748, X(4823))
        put(4749, z(X(4742)) * (1 - X(4740)) - X(4747) - X(4748) if z(X(4742)) > 0 else 0)
        put(4750, X(4747) + X(4748) + X(4749))
        put(4756, X(4825))
        put(4757, z(X(4742)) * X(4740) - X(4755) - X(4756) if z(X(4742)) > 0 else 0)
        put(4758, X(4755) + X(4756) + X(4757))
        put(4767, X(4824))
        put(4768, z(X(4761)) * (1 - X(4760)) - X(4766) - X(4767) if z(X(4761)) > 0 else 0)
        put(4769, X(4766) + X(4767) + X(4768))
        put(4775, X(4826))
        put(4776, z(X(4761)) * X(4760) - X(4774) - X(4775) if z(X(4761)) > 0 else 0)
        put(4777, X(4774) + X(4775) + X(4776))
        put(4831, 1 / (X(4740) * J4322 + J4324 * (1 - X(4740))))
        den = X(4769) + X(4777)
        put(4832, (X(4769) - X(4766)) / den if den else 0)
        put(4833, (X(4777) - X(4774)) / den if den else 0)
        # ICE fuel split (4835-4865)
        for i in range(5):
            put(4835 + i, o[2078 + i][k] if dk else None)
            if k > 0:
                put(4840 + i, X(4551 + i) / o[4551 + i][k - 1])
        put(4845, o[2063][k] if dk else None)
        te, tc = P['own_price_el'], P['cross_price_el']
        if dk:
            s4 = sum(X(4835 + i) for i in range(4))
            phev = (max(0.0, o[2063][k] - o[2065][k]) * o[2038][k]) if 'B9' in fix else X(4845) - X(4805)
            ice_tot = (1 - X(4805) - phev) if 'B9' in fix else (1 - X(4845))
            for i in range(4):
                put(4846 + i, X(4835 + i) / s4 * ice_tot)
            put(4850, phev)
        else:
            prev = [o[4846 + i][k - 1] for i in range(5)]
            for i in range(5):
                oth = [j for j in range(5) if j != i]
                cross = sum(prev[j] * X(4840 + j) for j in oth) / sum(prev[j] for j in oth)
                put(4846 + i, prev[i] * (X(4840 + i) ** te) * cross ** tc)
        s5 = sum(X(4846 + i) for i in range(5))
        for i in range(5):
            put(4851 + i, X(4846 + i) if isnum(X(4835 + i)) else X(4846 + i) / s5 * (1 - X(4828)))
        for i in range(5):
            put(4856 + i, X(4835 + i) if isnum(X(4835 + i)) else
                o[4856 + i][k - 1] * (X(4741) - 1) / X(4741) + X(4851 + i) / X(4741))
        so = sum(X(4856 + i) for i in range(5)) + X(4778)
        for i in range(5):
            put(4861 + i, X(4856 + i) / so)
        put(4866, pop[k])
        for i in range(5):
            put(4867 + i, X(4779) * X(4861 + i) * X(4866) / 1000)
        put(4872, (X(4769) + X(4777)) * X(4866) / 1000)
        # ---------------- freight (4897-4952)
        put(4874, y)
        put(4897, o[2166][k] if dk else o[4897][k - 1])
        put(4898, o[2168][k])
        put(4899, X(4897) * X(4898))
        put(4900, gpc[k])
        if z(X(4876)) > 0:
            put(4902, X(4876) + X(4886)); put(4903, X(4876) + X(4886))
        else:
            a = g('own_adj', 'fre')
            put(4902, a * gomp(X(4899), X(4900), g('own_gomp_b', 'fre')) * o['cJ4903'] + (1 - a) * zp(4903))
            put(4903, max(zp(4903) * (1 - dec_f), min(zp(4903) * (1 + g('own_max_growth', 'fre')), X(4902))))
        put(4904, X(4881) + X(4891))
        put(4905, X(4903) - X(4904))
        put(4908, X(4656)); put(4909, X(4681))
        kf = g('k', 'fre')
        put(4916, o[2101][k] if dk else None)
        w = (1 - X(4916)) if k == 0 else X(4919)
        put(4907, w)
        put(4910, X(4908) * X(4907) + X(4909) * (1 - X(4907)))
        put(4911, math.exp(-kf * X(4908) / X(4910)) * 10 ** 3)
        put(4912, math.exp(-kf * X(4909) / X(4910)) * 10 ** 3)
        put(4913, X(4911) / (X(4911) + X(4912)))
        put(4914, 1 - X(4913))
        put(4917, 1 - X(4916) if isnum(X(4916)) else X(4913))
        put(4918, 1 - X(4917))
        put(4921, X(4917) * X(4905)); put(4922, X(4918) * X(4905))
        put(4923, X(4914)); put(4924, zp(4923))
        put(4926, 1 / K4324)
        put(4882, X(4921))
        put(4883, X(4876) - X(4881) - X(4882) if z(X(4876)) > 0 else 0)
        put(4884, X(4881) + X(4882) + X(4883))
        put(4892, X(4922))
        put(4893, X(4886) - X(4891) - X(4892) if z(X(4886)) > 0 else 0)
        put(4894, X(4891) + X(4892) + X(4893))
        put(4927, (X(4894) - X(4891)) / X(4894) if X(4894) else 0)
        for i in range(3):
            put(4929 + i, o[2104 + i][k] if dk else None)
            if k > 0:
                put(4932 + i, X(4658 + i) / o[4658 + i][k - 1])
        put(4935, X(4916))
        uo, uc = P['own_price_el'], P['cross_price_el']
        prev = [zp(4936 + i) for i in range(3)]
        for i in range(3):
            if isnum(X(4929 + i)):
                put(4936 + i, X(4929 + i))
            else:
                oth = [j for j in range(3) if j != i]
                so_ = sum(prev[j] for j in oth)
                put(4936 + i, prev[i] if so_ == 0 else prev[i] * (X(4932 + i) ** uo) *
                    (sum(prev[j] * X(4932 + j) for j in oth) / so_) ** uc)
        s3 = sum(X(4936 + i) for i in range(3))
        for i in range(3):
            put(4939 + i, X(4936 + i) if isnum(X(4929 + i)) else X(4936 + i) / s3 * (1 - X(4918)))
        for i in range(3):
            put(4942 + i, X(4929 + i) if isnum(X(4929 + i)) else
                zp(4942 + i) * (K4324 - 1) / K4324 + X(4939 + i) / K4324)
        so = sum(X(4942 + i) for i in range(3)) + X(4895)
        for i in range(3):
            put(4945 + i, X(4942 + i) / so)
        put(4948, pop[k])
        for i in range(3):
            put(4949 + i, (X(4884) + X(4894)) * X(4945 + i) * X(4948) / 1000)
        put(4952, X(4894) * X(4948) / 1000)
        # ---------------- 2-3 wheelers (4977-5007)
        put(4954, y)
        put(4977, o[2169][k])
        if z(X(4956)) > 0:
            put(4978, X(4956) + X(4966)); put(4979, X(4956) + X(4966))
        else:
            put(4978, X(4977))
            put(4979, max(zp(4979) * (1 - g('own_max_decline', 'cyc')),
                          min(zp(4979) * (1 + g('own_max_growth', 'cyc')), X(4978))))
        put(4980, X(4961) + X(4971))
        put(4981, X(4979) - X(4980))
        put(4983, X(4995)); put(4984, X(4714)); put(4985, X(4736))
        put(4986, X(4984) * X(4983) + X(4985) * (1 - X(4983)))
        kc_ = g('k', 'cyc')
        put(4987, math.exp(-kc_ * X(4984) / X(4986)) * 10 ** 3)
        put(4988, math.exp(-kc_ * X(4985) / X(4986)) * 10 ** 3)
        put(4989, X(4987) / (X(4987) + X(4988)))
        put(4990, 1 - X(4989))
        put(4992, o[2126][k] if dk else None)
        put(4993, 1 - X(4992) if isnum(X(4992)) else X(4989))
        put(4994, 1 - X(4993))
        put(4997, X(4993) * X(4981)); put(4998, X(4994) * X(4981))
        put(4999, X(4990)); put(5000, zp(4999))
        put(5002, 1 / L4324)
        put(4962, X(4997))
        put(4963, X(4956) - X(4961) - X(4962) if z(X(4956)) > 0 else 0)
        put(4964, X(4961) + X(4962) + X(4963))
        put(4972, X(4998))
        put(4973, X(4966) - X(4971) - X(4972) if z(X(4966)) > 0 else 0)
        put(4974, X(4971) + X(4972) + X(4973))
        put(5003, (X(4974) - X(4971)) / X(4974) if X(4974) else 0)
        put(5005, pop[k])
        put(5006, X(4964) * X(5005) / 1000); put(5007, X(4974) * X(5005) / 1000)
        # ---------------- stock fuel economy, uncalibrated distance and fuel use (5009-5167)
        put(5009, y)
        put(5010, X(4831))
        for i, src in enumerate((2041, 2043, 2045, 2047, 2048)):
            put(5011 + i, o[src][k] if dk else None)
        for i, (ro, rn) in enumerate(((5017, 4386), (5021, 4387), (5025, 4388), (5029, 4389), (5033, 4390))):
            dat = X(5011 + i)
            put(ro, dat if isnum(dat) else zp(ro + 2))
            put(ro + 1, X(rn))
            put(ro + 2, dat if isnum(dat) else X(ro + 1) * X(5010) + X(ro) * (1 - X(5010)))
        for i, (rfe, rpr) in enumerate(((5037, 4367), (5043, 4368), (5048, 4369), (5053, 4370), (5058, 4371))):
            put(rfe, X((5017, 5021, 5025, 5029, 5033)[i])); put(rfe + 1, X(rpr))
            put(rfe + 3 if i == 0 else rfe + 2, X(rfe + 1) / X(rfe) + X(4451))
        put(5039, X(4451))
        cpk = {5040: 5041, 5045: 5046, 5050: 5051, 5055: 5056, 5060: 5061}
        if k > 0:
            for a_, b_ in cpk.items():
                put(b_, X(a_) / o[a_][k - 1])
        put(5063, gpc[k])
        if k > 0:
            put(5064, X(5063) / o[5063][k - 1])
        put(5066, o[2060][k] if dk else None)
        for i, rc in enumerate((5041, 5046, 5051, 5056, 5061)):
            put(5067 + i, X(5066) if isnum(X(5066)) else
                zp(5067 + i) * X(rc) ** el_dg * X(5064) ** g('inc_el_vkt', 'pass'))
        for i in range(5):
            put(5073 + i, X(4867 + i))
            put(5079 + i, X(5073 + i) * X(5067 + i) / 1000)
        put(5085, X(5079) / X(5019) + X(5083) / X(5035))
        put(5086, X(5080) / X(5023)); put(5087, X(5081) / X(5027)); put(5088, X(5082) / X(5031))
        put(5090, y)
        put(5091, X(4926))
        for i, src in enumerate((2092, 2093, 2094)):
            put(5092 + i, o[src][k] if dk else None)
        for i, (ro, rn) in enumerate(((5096, 4425), (5100, 4426), (5104, 4427))):
            dat = X(5092 + i)
            put(ro, dat if isnum(dat) else zp(ro + 2))
            put(ro + 1, X(rn))
            put(ro + 2, dat if isnum(dat) else X(ro + 1) * X(5091) + X(ro) * (1 - X(5091)))
        put(5110, X(4479))
        for rfe, ro, rpr in ((5108, 5096, 4410), (5114, 5100, 4411), (5119, 5104, 4412)):
            put(rfe, X(ro)); put(rfe + 1, X(rpr)); put(rfe + 2 if rfe != 5108 else 5111, X(rfe + 1) / X(rfe) + X(5110))
        if k > 0:
            for a_, b_ in ((5111, 5112), (5116, 5117), (5121, 5122)):
                put(b_, X(a_) / o[a_][k - 1])
        put(5124, gpc[k])
        if k > 0:
            put(5125, X(5124) / o[5124][k - 1])
        put(5126, o[2117][k] if dk else None)
        for i, rc in enumerate((5112, 5117, 5122)):
            put(5127 + i, X(5126) if isnum(X(5126)) else
                zp(5127 + i) * X(rc) ** el_dd * X(5125) ** g('inc_el_vkt', 'fre'))
        for i in range(3):
            put(5131 + i, X(4949 + i))
            put(5135 + i, X(5131 + i) * X(5127 + i) / 1000)
            put(5139 + i, X(5135 + i) / X((5098, 5102, 5106)[i]))
        put(5143, y)
        put(5144, X(5002))
        put(5145, o[2121][k] if dk else None)
        put(5147, X(5145) if isnum(X(5145)) else zp(5149))
        put(5148, X(4444))
        put(5149, X(5145) if isnum(X(5145)) else X(5148) * X(5144) + X(5147) * (1 - X(5144)))
        put(5151, X(5147)); put(5152, X(4438)); put(5153, X(4497))
        put(5154, X(5152) / X(5151) + X(5153))
        if k > 0:
            put(5155, X(5154) / o[5154][k - 1])
        put(5157, gpc[k])
        if k > 0:
            put(5158, X(5157) / o[5157][k - 1])
        put(5160, o[2133][k] if dk else None)
        put(5161, X(5160) if isnum(X(5160)) else zp(5161) * X(5155) ** el_dg * X(5158) ** g('inc_el_vkt', 'cyc'))
        put(5163, X(5006))
        put(5165, X(5163) * X(5161) / 1000)
        put(5167, X(5165) / X(5149))
        # ---------------- calibration step 1 (5170-5173), base year
        if k == 0:
            Lc = {5170: X(5167) + X(5085), 5171: X(5086) + X(5139), 5172: X(5087) + X(5140), 5173: X(5088) + X(5141)}
            Mc = {5170: 0.0, 5171: o['cL2021'], 5172: o['cL2025'], 5173: o['cL2029']}
            Nc = {5170: L['gso'], 5171: L['die'], 5172: L['lpg'], 5173: L['nga']}
            Pc = {5170: eb_rod['gso'], 5171: eb_rod['die'], 5172: eb_rod['lpg'], 5173: eb_rod['nga']}
            sp_ = X(5085) + X(5086) + X(5087) + X(5088)
            sf_ = X(5139) + X(5140) + X(5141)
            for r in range(5170, 5174):
                gross = (1 / (1 - Mc[r])) if 'B6b' in fix else (1 + Mc[r])
                Oc = Lc[r] / Nc[r] * 10 ** 9 * gross
                Qc = 1.0 if (Oc == 0 or Pc[r] == 0) else Pc[r] / Oc
                Rc = X(5085 + r - 5170) / sp_
                o[f'cL{r}'], o[f'cM{r}'], o[f'cN{r}'], o[f'cO{r}'] = Lc[r], Mc[r], Nc[r], Oc
                o[f'cP{r}'], o[f'cQ{r}'], o[f'cR{r}'] = Pc[r], Qc, Rc
                if r > 5170:
                    o[f'cS{r}'] = X(5139 + r - 5171) / sf_
            o['cT5170'] = 1.0 if X(5167) == 0 else X(5167) / X(5167)
            Q = [o[f'cQ{r}'] for r in range(5170, 5174)]
            o['cU5170'] = sum(o[f'cR{r}'] * Q[r - 5170] for r in range(5170, 5174))
            o['cV5170'] = sum(o.get(f'cS{r}', 0.0) * Q[r - 5170] for r in range(5170, 5174))
            o['cW5170'] = o['cT5170'] * Q[0]
            o['cG5177'], o['cG5231'], o['cG5273'] = o['cU5170'], o['cV5170'], o['cW5170']
        Gp_, Gf_, Gc_ = o['cG5177'], o['cG5231'], o['cG5273']
        # ---------------- calibrated distance and fuel use, passenger (5175-5227)
        put(5175, y)
        put(5176, o[2060][k] if dk else None)
        for i, rc in enumerate((5041, 5046, 5051, 5056, 5061)):
            put(5177 + i, X(5176) * Gp_ if isnum(X(5176)) else
                zp(5177 + i) * X(rc) ** el_dg * X(5064) ** g('inc_el_vkt', 'pass'))
        for i in range(5):
            put(5183 + i, X(4867 + i))
            put(5189 + i, X(5183 + i) * X(5177 + i) / 1000)
        put(5195, X(5189) / X(5019) + X(5193) / X(5035))
        put(5196, X(5190) / X(5023)); put(5197, X(5191) / X(5027)); put(5198, X(5192) / X(5031))
        put(5199, (X(5195) * G4375 + X(5196) * G4376 + X(5197) * G4377 + X(5198) * G4378) * 10 ** 3)
        put(5201, X(4399)); put(5202, X(4403)); put(5203, X(4832)); put(5204, X(4833))
        s_ = X(5203) + X(5204)
        put(5205, X(5201) * X(5203) / s_ + X(5202) * X(5204) / s_ if s_ else (X(5201) + X(5202)) / 2)
        put(5207, zp(5209) if zp(5209) > 0 else X(5205))
        put(5208, X(5205))
        put(5209, X(5207) * (1 - X(5203) - X(5204)) + X(5208) * (X(5203) + X(5204)))
        put(5211, X(5207)); put(5212, X(4351))
        put(5213, X(5212) / X(5211) + X(5039))
        if k > 0:
            put(5214, X(5213) / o[5213][k - 1])
        put(5216, o[2061][k] if dk else None)
        put(5217, X(5216) * Gp_ if isnum(X(5216)) else
            zp(5217) * X(5214) ** el_dg * X(5064) ** g('inc_el_vkt', 'pass'))
        put(5219, X(4872))
        put(5220, X(5217) * X(5219) / 1000)
        put(5221, o[2049][k] if dk else o[5221][k - 1])
        put(5222, X(5193) / X(5209) * (1 - X(5221)))
        put(5223, X(5220) / X(5209) + X(5222))
        put(5225, sum(X(r) for r in range(5189, 5194)) + X(5220))
        put(5226, X(5199) / X(5225) * 1000)
        put(5227, zp(5226))
        # ---------------- freight (5229-5269)
        put(5229, y)
        put(5230, o[2117][k] if dk else None)
        for i, rc in enumerate((5112, 5117, 5122)):
            base_ = X(5126) if (i == 1 and 'B8' not in fix) else X(5230)
            put(5231 + i, base_ * Gf_ if isnum(base_) else
                zp(5231 + i) * X(rc) ** el_dd * X(5125) ** g('inc_el_vkt', 'fre'))
        for i in range(3):
            put(5235 + i, X(4949 + i))
            put(5239 + i, X(5235 + i) * X(5231 + i) / 1000)
            put(5243 + i, X(5239 + i) / X((5098, 5102, 5106)[i]))
        put(5246, (X(5243) * G4419 + X(5244) * G4420 + X(5245) * G4421) * 10 ** 3)
        put(5248, X(4433)); put(5249, X(4927))
        put(5251, zp(5253) if zp(5253) > 0 else X(5248))
        put(5252, X(4433))
        put(5253, X(5251) * (1 - X(5249)) + X(5252) * X(5249))
        put(5255, X(5251)); put(5256, X(4352))
        put(5257, X(5256) / X(5255) + X(5110))
        if k > 0:
            put(5258, X(5257) / o[5257][k - 1])
        put(5260, o[2118][k] if dk else None)
        put(5261, X(5260) * Gf_ if isnum(X(5260)) else
            zp(5261) * X(5258) ** el_dd * X(5125) ** g('inc_el_vkt', 'fre' if 'B8' in fix else 'cyc'))
        put(5263, X(4952))
        put(5264, X(5261) * X(5263) / 1000)
        put(5265, X(5264) / X(5253))
        put(5267, X(5239) + X(5264) + ((X(5240) + X(5241)) if 'B21' in fix else 0.0))
        put(5268, G4419 / X(5096) * 10 ** 6 if X(5267) == 0 else X(5246) / X(5267) * 1000)
        put(5269, zp(5268))
        # ---------------- 2-3 wheelers (5271-5303)
        put(5271, y)
        put(5272, o[2133][k] if dk else None)
        put(5273, X(5272) * Gc_ if isnum(X(5272)) else
            zp(5273) * X(5155) ** el_dg * X(5158) ** g('inc_el_vkt', 'cyc'))
        put(5275, X(5006))
        put(5277, X(5275) * X(5273) / 1000)
        put(5279, X(5277) / X(5149))
        put(5280, X(5279) * G4441 * 10 ** 3)
        put(5282, X(4446)); put(5283, X(5003))
        put(5285, zp(5287) if zp(5287) > 0 else X(5282))
        put(5286, X(4446))
        put(5287, X(5285) * (1 - X(5283)) + X(5286) * X(5283))
        put(5289, X(5285)); put(5290, X(4351))
        put(5291, X(5290) / X(5289) + X(5153))
        if k > 0:
            put(5292, X(5291) / o[5291][k - 1])
        put(5294, o[2137][k] if dk else None)
        if isnum(X(5294)):
            put(5295, X(5294) * Gc_)
        elif 'B8' in fix:
            put(5295, zp(5295) * X(5292) ** el_dg * X(5158) ** g('inc_el_vkt', 'cyc'))
        else:
            put(5295, zp(5295) * X(5292) ** el_dg * X(5292) ** g('inc_el_vkt', 'cyc'))
        put(5297, X(5007))
        put(5298, X(5295) * X(5297) / 1000)
        put(5299, X(5298) / X(5287))
        put(5301, X(5277) + X(5298))
        put(5302, X(5280) / X(5301) * 1000)
        put(5303, zp(5302))
        # ---------------- buses (5305-5318)
        put(5305, y)
        E = {5306: L['die'], 5307: L['lpg'], 5308: L['nga'], 5309: inp['gwh_ktoe'] * 10 ** 6,
             5310: L['gso'], 5311: L['die'], 5312: L['lpg'], 5313: L['nga'], 5314: inp['gwh_ktoe'] * 10 ** 3}
        if k == 0:
            for r, v in E.items():
                o[f'cE{r}'] = v
            put(5306, o['cL2140']); put(5307, o['cL2141']); put(5308, o['cL2142']); put(5309, o['cL2143'])
        if 'B6' in fix:
            for i, fu in enumerate(('gso', 'die', 'lpg', 'nga')):
                put(5310 + i, X(5195 + i) / L[fu] * 10 ** 9)
            put(5314, X(5223) * 1000 / inp['gwh_ktoe'])
        else:
            put(5310, X(5191) * E[5310] / 10 ** 3); put(5311, X(5192) * E[5311] / 10 ** 3)
            put(5312, X(5193) * E[5312] / 10 ** 3); put(5313, z(X(5194)) * E[5313] / 10 ** 3)
            put(5314, X(5219) * E[5314])
        b0 = sum(o[r][0] for r in range(5310, 5315))
        bf = sum(X(r) for r in range(5310, 5314))
        put(5315, o[5306][0] * E[5306] / 10 ** 9 * bf / b0)
        put(5316, o[5307][0] * E[5307] / 10 ** 9 * bf / b0)
        put(5317, o[5308][0] * E[5308] / 10 ** 9 * bf / b0)
        if 'B6' in fix:      # base bus energy in ktoe (legacy adds bln liters and bln kWh), to bln kWh
            put(5318, sum(o[r][0] for r in range(5306, 5310)) * inp['gwh_ktoe'] / 10 ** 3 * X(5314) / b0)
        else:
            put(5318, sum(o[r][0] * E[r] for r in range(5306, 5310)) / 10 ** 9 * X(5314) / b0)
        # ---------------- calibration step 2 and results (5320-5378)
        put(5320, y)
        put(5321, X(5195) + X(5279))
        put(5322, X(5196) + X(5243) + X(5315))
        put(5323, X(5197) + X(5244) + X(5316))
        put(5324, X(5198) + X(5245) + X(5317))
        put(5330, X(5318) + X(5299) + X(5265) + X(5223))
        if k == 0:
            for r, rb, fu in ((5325, 5321, 'gso'), (5326, 5322, 'die'), (5327, 5323, 'lpg'), (5328, 5324, 'nga')):
                I = X(rb) / L[fu] * 10 ** 9
                Jv = eb_rod[fu]
                o[f'cI{r}'], o[f'cJ{r}'] = I, Jv
                o[f'cE{r}'] = 1.0 if (I == 0 or Jv == 0) else Jv / I
            I = X(5330) / inp['gwh_ktoe'] * 10 ** 3
            Jv = eb_rod['ele']
            o['cI5331'], o['cJ5331'] = I, Jv
            o['cE5331'] = 1.0 if (I == 0 or Jv == 0 or P['recon_ele'] == 'No') else Jv / I
        for r, rb, fu in ((5325, 5321, 'gso'), (5326, 5322, 'die'), (5327, 5323, 'lpg'), (5328, 5324, 'nga')):
            put(r, X(rb) / L[fu] * 10 ** 9 * o[f'cE{r}'])
        put(5331, X(5330) * 1000 / inp['gwh_ktoe'] * o['cE5331'])
        e5, e6, e7, e8, e1 = o['cE5325'], o['cE5326'], o['cE5327'], o['cE5328'], o['cE5331']
        put(5333, X(5225) * e5); put(5334, X(5267) * e6); put(5335, X(5301) * e5)
        put(5336, X(5333) + X(5334) + X(5335))
        put(5339, e5 * X(5195)); put(5340, e6 * X(5196)); put(5341, e7 * X(5197)); put(5342, e8 * X(5198))
        put(5343, X(5223) * e1)
        put(5345, X(5243) * e6); put(5346, X(5244) * e7); put(5347, X(5245) * e8); put(5348, e1 * X(5265))
        put(5350, X(5279) * e5); put(5351, X(5299) * e1)
        put(5353, y)
        put(5354, X(5037)); put(5355, X(5151))
        put(5356, X(5354) * 3 / 4 + X(5355) * 1 / 4 if X(5321) == 0 else
            X(5354) * X(5195) / (X(5195) + X(5279)) + X(5279) / (X(5195) + X(5279)) * X(5355))
        put(5358, X(5043)); put(5359, X(5108))
        put(5360, (X(5358) + X(5359)) / 2 if X(5322) == 0 else
            X(5358) * X(5196) / (X(5196) + X(5243)) + X(5243) / (X(5196) + X(5243)) * X(5359))
        put(5362, X(5048)); put(5363, X(5100))
        put(5364, (X(5362) + X(5363)) / 2 if X(5323) == 0 else
            X(5362) * X(5197) / (X(5244) + X(5197)) + X(5244) / (X(5244) + X(5197)) * X(5363))
        put(5366, X(5053)); put(5367, X(5104))
        fr_g = X(5245) if 'B22' in fix else X(5244)
        put(5368, (X(5367) + X(5366)) / 2 if X(5324) == 0 else
            X(5366) * X(5198) / (X(5198) + fr_g) + fr_g / (X(5198) + fr_g) * X(5367))
        put(5370, X(5207)); put(5371, X(5251)); put(5372, X(5285))
        te_ = X(5223) + X(5265) + X(5299)
        test = X(5330) if 'B22' in fix else X(5326)
        put(5373, X(5370) * 0.5 + X(5371) * 0.25 + X(5372) * 0.25 if test == 0 else
            X(5370) * X(5223) / te_ + X(5265) / te_ * X(5371) + X(5299) / te_ * X(5372))
        put(5375, sum(X(r) for r in range(5183, 5188)) + X(5219))
        put(5376, X(5235) + X(5236) + X(5237) + X(5263))
        put(5377, X(5275) + X(5297))
        put(5378, X(5375) + X(5376) + X(5377))
    # memo outputs (ktoe by fuel and EV shares), for reports
    o['road_ktoe'] = {'gso': o[5325], 'die': o[5326], 'lpg': o[5327], 'nga': o[5328], 'ele': o[5331]}
    return o


# ==================================================================== inputs
def _ref(run):
    return {r['key']: r for r in read('legacy_transport_reference.csv') if r['run'] == run}


def legacy_inputs(run):
    """Engine inputs of the cached legacy run ('base' or 'pol'): Egypt data from the CSVs, and the inputs the engineer
    model takes from the rest of Mitigation (prices, power prices, macro, carbon price, elasticities, energy balance,
    VAT, power WACC, range anxiety start values) as cached in legacy_transport_reference.csv."""
    ref = _ref(run)
    iso = LEGACY_ISO
    ser = lambda key: [float(ref[key][str(y)]) if ref[key][str(y)] != '' else None for y in YEARS]
    sc = lambda key: fnum(ref[key]['2022'])
    data, prices, ra = country_data(iso)
    assert ra == {'pass': sc('in|ra|pass'), 'fre': sc('in|ra|fre'), 'cyc': sc('in|ra|cyc')}, ra
    return {
        'iso': iso, 'par': params(), 'paths': paths(YEARS), 'data': data, 'prices': prices, 'ra': ra,
        'scen': sc('in|scen'),
        'rp': {'gso': ser('in|rp_gso'), 'die': ser('in|rp_die'), 'lpg': ser('in|rp_lpg'),
               'nga_res': ser('in|rp_nga_res'), 'nga_ind': ser('in|rp_nga_ind')},
        'sp_gso': ser('in|sp_gso'), 'txo_gso': ser('in|txo_gso'), 'vatr_gso': ser('in|vatr_gso'),
        'vat_die': ser('in|vat_die'), 'vat_lpg': ser('in|vat_lpg'), 'vat_nga_ind': ser('in|vat_nga_ind'),
        'pp_res': ser('in|pp_res'), 'pp_ind': ser('in|pp_ind'),
        'gdp_growth': ser('in|gdp_growth'), 'gdp_growth_2021': sc('in|gdp_growth_2021'),
        'row2455': ser('in|row2455'), 'cprice': ser('in|cprice'), 'fb_cov': ser('in|fb_cov'),
        'pop': ser('in|pop'), 'gdppc': ser('in|gdppc'),
        'rp0': {'gso': ser('in|rp0_gso'), 'ele_res': ser('in|rp0_ele_res'), 'die': ser('in|rp0_die'),
                'vatr_die': ser('in|vatr0_die'), 'ele_ind': ser('in|rp0_ele_ind')},
        'rp0_ele_res_2021': sc('in|rp0_ele_res_2021'),
        'vat_veh': sc('in|vat_veh'), 'wacc_avg': sc('in|wacc_avg'),
        'el_dem_gso': sc('in|el_dem_gso'), 'el_dem_die': sc('in|el_dem_die'), 'el_eff_gso': sc('in|el_eff_gso'),
        'el_eff_die': sc('in|el_eff_die'), 'aei_oil': sc('in|aei_oil'),
        'l_ktoe': {f: sc(f'in|l_ktoe|{f}') for f in ('gso', 'die', 'lpg', 'nga')}, 'gwh_ktoe': sc('in|gwh_ktoe'),
        'ef': {'gso': sc('in|ef|gso'), 'die': sc('in|ef|die'), 'lpg': sc('in|ef|lpg'), 'nga_gj': sc('in|ef|nga_gj')},
        'ef_name': {'gso': sc('in|ef|gso'), 'die': sc('in|ef_name|die'), 'lpg': sc('in|ef_name|lpg'),
                    'nga_gj': sc('in|ef_name|nga_gj')},
        'eb': {f: sc(f'in|eb|{f}') for f in ('gso', 'die', 'lpg', 'nga', 'bgs', 'bdi', 'ele')},
    }


def _legacy_iso():
    for r in read('legacy_cached_baseline.csv'):
        return r['code'].split('.')[0].upper()


LEGACY_ISO = _legacy_iso()


def legacy_test(run, fix=frozenset(), years=YEARS):
    """Engine on the legacy inputs vs the cached legacy rows: sorted [(max relative diff, key, year)] over every
    cached row and side-table scalar of the engineer model (relative to max(1e-6, |legacy|))."""
    o = engine(legacy_inputs(run), years, fix=fix)
    out = []
    for r in read('legacy_transport_reference.csv'):
        if r['run'] != run or r['key'].startswith('in|'):
            continue
        key = r['key']
        if key.startswith('c'):
            leg = r['2022']
            if leg == '' or key not in o:
                if leg != '':
                    out.append((float('inf'), key, 'missing'))
                continue
            got, leg = o[key], float(leg)
            out.append((abs(got - leg) / max(1e-6, abs(leg)), key, 'scalar'))
            continue
        row = int(key[1:])
        got = o.get(row)
        worst = (0.0, key, 0)
        for kk, yy in enumerate(years):
            leg = r[str(yy)]
            if leg == '':
                continue
            leg = float(leg)
            g_ = None if got is None else got[kk]
            if g_ is None:
                worst = max(worst, (float('inf'), key, yy))
                continue
            dd = abs(g_ - leg) / max(1e-6, abs(leg))
            worst = max(worst, (dd, key, yy))
        out.append(worst)
    return sorted(out, key=lambda t: -t[0])


def summary(o, years=YEARS, at=(2030, 2035, 2041)):
    """Road fuel use (ktoe), EV sales shares and vehicle stocks (mln) at the given years."""
    res = {}
    for y in at:
        k = years.index(y)
        res[y] = {
            'gso': o[5325][k], 'die': o[5326][k], 'lpg': o[5327][k], 'nga': o[5328][k], 'ele': o[5331][k],
            'ev_pass': o[4828][k], 'ev_fre': o[4918][k], 'ev_cyc': o[4994][k],
            'veh_pass': o[5375][k], 'veh_fre': o[5376][k], 'veh_cyc': o[5377][k]}
    return res


METRICS = [('gso', 'Gasoline ktoe', '%'), ('die', 'Diesel ktoe', '%'), ('nga', 'Gas ktoe', '%'),
           ('ele', 'Electricity ktoe', '%'), ('ev_pass', 'EV sales share passenger', 'pp'),
           ('ev_fre', 'EV sales share freight', 'pp'), ('ev_cyc', 'EV sales share 2-3 wheeler', 'pp'),
           ('veh_pass', 'Vehicles passenger mln', '%'), ('veh_fre', 'Vehicles freight mln', '%'),
           ('veh_cyc', 'Vehicles 2-3 wheeler mln', '%')]


def effects_md(run, at=(2030, 2035, 2041)):
    """Markdown tables: legacy and all fixes (levels), and the change from each fix alone (cells 2030 / 2035 / 2041;
    % change for fuel use and vehicles, percentage points for EV sales shares)."""
    inp = legacy_inputs(run)
    leg = summary(engine(inp, fix=frozenset()), at=at)
    res = {f: summary(engine(inp, fix=frozenset([f])), at=at) for f in FIXES}
    res['all'] = summary(engine(inp, fix=ALL_FIXES), at=at)
    fmt = lambda key, v: f'{100 * v:.1f}%' if key.startswith('ev') else (f'{v:,.0f}' if len(key) == 3 else f'{v:.2f}')
    lines = ['| Series | ' + ' | '.join(f'Legacy {y} | All fixes {y}' for y in at) + ' |',
             '|---|' + '---:|' * (2 * len(at))]
    for key, name, _u in [('lpg', 'LPG ktoe', '%')] + METRICS:
        lines.append(f'| {name} | ' + ' | '.join(f'{fmt(key, leg[y][key])} | {fmt(key, res["all"][y][key])}'
                                                 for y in at) + ' |')
    lines += ['', '| Fix | ' + ' | '.join(name for _k, name, _u in METRICS) + ' |', '|---|' + '---|' * len(METRICS)]

    def delta(f, key, u, y):
        a, b = leg[y][key], res[f][y][key]
        v = 100 * (b - a) if u == 'pp' else (100 * (b / a - 1) if a else 0.0)
        return '0' if abs(v) < 0.005 else f'{v:+.2f}'
    for f in list(FIXES) + ['all']:
        cells = [' / '.join(delta(f, key, u, y) for y in at) for key, _n, u in METRICS]
        if all(set(c.replace(' / ', '')) <= {'0'} for c in cells):
            lines.append(f'| {f} | no effect on these series' + ' |' * len(METRICS))
        else:
            lines.append(f'| {f} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)


def main():
    for run in ('base', 'pol'):
        res = legacy_test(run)
        print(f'legacy test {run}: {len(res)} series, max rel diff {res[0][0]:.3e} ({res[0][1]} {res[0][2]})')
        for t in res[:8]:
            print('   ', t)
    for run in ('base', 'pol'):
        print(f'\n{run}: legacy and fixes (cells 2030 / 2035 / 2041)')
        print(effects_md(run))


if __name__ == '__main__':
    main()
