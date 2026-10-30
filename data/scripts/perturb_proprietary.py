"""Perturb the proprietary tables of an edition's tidy/ (Egypt only) by small random factors, keeping their identities.

A public edition must not hold the real values of the proprietary tables (data/README.md): this script makes one from a
copy of real values (edition folder first copied from the full edition, then perturbed in place). It multiplies their
values by random factors 1 + u, u uniform in [-DELTA, +DELTA] (3%), and rewrites the tables in place. The factors come
from the operating system's random source and are not stored, so the real values cannot be recovered from the script
and its output. Run it once on real values; running it again perturbs the perturbed values again.

Identities kept (each is checked on the input and on the output; the script stops if one fails):

  energy_balances      per fuel: tes = production + imports + exports + stockcha + worldav + worldnav; tfc = the sum of
                       the final-consumption flows; statdiff = tfc - (tes + tottranf + distloss + ownuse + transfer)
                       (the balancing item absorbs the noise); tottranf = power + the other transformation;
                       electricity output: ecy power = eloutput total x the input ratio (ktoe per GWh); hydro, solar and
                       wind: power = -eloutput x their ratio, production = -power. Per flow: total = the sum of the
                       fuels (not obf, totren); obf = bio; totren = wnd + sol + hyd + ore
  energy_consumption   recomputed from energy_balances with legacy's mapping (Excel-AI extract_legacy_tables.py)
  xai_energy_balance, xai_energy_use, xai_power_demand
                       Excel-AI's copies of Balances and EnergyCons values: recomputed from the two tables above
  prices_domestic      the US$ amounts (supply cost sp, excise and other taxes txo, margin mar, production costs) are
                       perturbed; rates and shares (VAT, passthrough, domestic portions) and international spot prices
                       (public) are not; retail price rp = (sp + txo) x (1 + vatrate) + the gap the data had
  prices_domestic_corrections
                       old and new values follow the cells they correct (new = the perturbed price)
  hh_survey            budget shares: each row's shares keep the row's total; other variables: one factor per variable
                       (the decile thresholds and the poverty rates one factor per group: order kept); a percentage
                       at most 100 stays at most 100
  tran_scatter         one factor per cell (not the selection flags, code *.select)
  io_gtap              levels (DOMCONS, Exports, HHD, Imports, Output, TOTD): one factor per GTAP sector (each sector's
                       ratios kept); Leontief coefficients (coa, ely, nga, oil, p_c): one factor per cell

Run from the repository root, then rewrite the workbook, the legacy copy and the manifest, and run the tests:
    python data/scripts/perturb_proprietary.py --edition Public02
    python data/scripts/tidy_convert.py to-xlsx --tidy data/Public02/tidy --out data/Public02/legacy_xlsx/CPAT_LegacyData.xlsx
    python data/scripts/legacy_proprietary.py fill --edition Public02
    python data/scripts/build_edition.py --edition Public02
    python -m pytest data/tests
"""
import csv
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import editions as ED  # noqa: E402

DELTA = 0.03
TIDY = None                                           # the edition's tidy/ (main)
RNG = random.SystemRandom()
TOL = 1e-6


def factor():
    return 1 + RNG.uniform(-DELTA, DELTA)


def read(name):
    with open(os.path.join(TIDY, f'{name}.csv'), encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def write(name, head, rows):
    with open(os.path.join(TIDY, f'{name}.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        w.writerows(rows)


def num(s):
    return float(s) if s != '' else 0.0


def txt(x):
    return '0' if x == 0 else repr(float(x))


def check(ok, what):
    if not ok:
        sys.exit(f'identity fails: {what}')


# ------------------------------------------------------------------------------------------------ energy balances
SUPPLY = ['production', 'imports', 'exports', 'stockcha', 'worldav', 'worldnav']
FINAL = ['cement', 'construc', 'domesair', 'domesnav', 'food_forest', 'info_agrc', 'info_fish', 'info_food',
         'info_wood', 'ironstl', 'machinery', 'mining_chemicals', 'nonenuse', 'nonferrmet', 'ononspec',
         'other_manufact', 'pipeline', 'rail', 'resident', 'road', 'services']
OTHER = ['distloss', 'ownuse', 'transfer', 'heat']
AGG_FUELS = ['total', 'totren', 'obf']
RENEW = ['wnd', 'sol', 'hyd', 'ore']
ELEC_RENEW = ['wnd', 'sol', 'hyd']


def balance_identities(k, g, fuels):
    """Raise unless every identity holds in k (ktoe: {flow: {fuel: v}}) and g (GWh: {fuel: v})."""
    for fu in fuels + AGG_FUELS:
        check(abs(k['tes'][fu] - sum(k[f][fu] for f in SUPPLY)) < 1e-3, f'tes {fu}')
        check(abs(k['tfc'][fu] - sum(k[f][fu] for f in FINAL)) < 1e-3, f'tfc {fu}')
        bal = k['tes'][fu] + k['tottranf'][fu] + k['distloss'][fu] + k['ownuse'][fu] + k['statdiff'][fu] + \
            k['transfer'][fu]
        check(abs(k['tfc'][fu] - bal) < 1e-3, f'balance {fu}')
    for fl in k:
        check(abs(k[fl]['total'] - sum(k[fl][fu] for fu in fuels)) < 1e-3, f'total {fl}')
        check(abs(k[fl]['obf'] - k[fl]['bio']) < 1e-3, f'obf {fl}')
        check(abs(k[fl]['totren'] - sum(k[fl][fu] for fu in RENEW)) < 1e-3, f'totren {fl}')
    check(abs(g['total'] - sum(g[fu] for fu in fuels)) < 1e-3, 'eloutput total')


def perturb_balances():
    head, rows = read('energy_balances')
    k, g = {}, {}
    for country, year, unit, flow, fuel, v in rows:
        (k.setdefault(flow, {}) if unit == 'ktoe' else g)[fuel] = num(v)
    fuels = [fu for fu in k['tes'] if fu not in AGG_FUELS]
    for fl in k:
        for fu in k['tes']:
            k[fl].setdefault(fu, 0.0)
    balance_identities(k, g, fuels)
    ratio = {fu: k['power'][fu] / g[fu] for fu in ELEC_RENEW + ['total'] if g.get(fu)}
    ratio['ecy'] = k['power']['ecy'] / g['total']
    other_tr = {fu: k['tottranf'][fu] - k['power'][fu] for fu in k['tes']}
    n = {fl: dict(v) for fl, v in k.items()}
    ng = {fu: g[fu] * factor() for fu in fuels}
    for fu in fuels:
        for fl in SUPPLY + FINAL + OTHER + ['power']:
            n[fl][fu] = k[fl][fu] * factor()
        other = other_tr[fu] * factor()
        if fu in ELEC_RENEW and g.get(fu):
            n['power'][fu] = ng[fu] * ratio[fu]
            n['production'][fu] = -n['power'][fu]
        if fu == 'ecy':
            n['power'][fu] = sum(ng.values()) * ratio['ecy']
        n['tottranf'][fu] = n['power'][fu] + other
        n['tes'][fu] = sum(n[f][fu] for f in SUPPLY)
        n['tfc'][fu] = sum(n[f][fu] for f in FINAL)
        n['statdiff'][fu] = n['tfc'][fu] - (n['tes'][fu] + n['tottranf'][fu] + n['distloss'][fu] + n['ownuse'][fu]
                                            + n['transfer'][fu])
    for fl in n:
        n[fl]['obf'] = n[fl]['bio']
        n[fl]['totren'] = sum(n[fl][fu] for fu in RENEW)
        n[fl]['total'] = sum(n[fl][fu] for fu in fuels)
    ng['obf'], ng['totren'], ng['total'] = ng['bio'], sum(ng[fu] for fu in RENEW), sum(ng[fu] for fu in fuels)
    balance_identities(n, ng, fuels)
    out = [[c, y, u, fl, fu, txt(n[fl][fu] if u == 'ktoe' else ng[fu])] for c, y, u, fl, fu, _v in rows]
    write('energy_balances', head, out)
    return n, ng, rows[0][1]


# ------------------------------------------------------------------------------------------------ energy consumption
SUB_FLOWS = {'rod': ['road'], 'ral': ['rail'], 'avi': ['domesair'], 'nav': ['domesnav'], 'res': ['resident'],
             'foo': ['food_forest'], 'srv': ['services'], 'mch': ['mining_chemicals'], 'irn': ['ironstl'],
             'nfm': ['nonferrmet'], 'mac': ['machinery'], 'cem': ['cement'], 'omn': ['other_manufact'],
             'cst': ['construc'], 'oen': ['ononspec'], 'ftr': ['-ownuse', '-heat'], 'pow': ['-power'],
             'elec': ['eloutput'], 'wav': ['worldav'], 'neu': ['nonenuse']}      # as extract_legacy_tables.py
ENC_COL = {'ele': 'ecy', 'heat': 'hea'}


def enc_value(k, g, code, sector):
    fu = ENC_COL.get(code, code)
    v = 0.0
    for fl in SUB_FLOWS[sector]:
        sign, fl = (-1, fl[1:]) if fl.startswith('-') else (1, fl)
        v += sign * (g.get(fu, 0.0) if fl == 'eloutput' else k.get(fl, {}).get(fu, 0.0))
    return v


def recompute_consumption(k, g, check_only=False):
    head, rows = read('energy_consumption')
    out = []
    for code, year, sector, v in rows:
        x = enc_value(k, g, code.split('.')[-1], sector)
        if check_only:
            check(abs(x - num(v)) < TOL, f'energy_consumption {code} {sector} from energy_balances')
        out.append([code, year, sector, txt(x)])
    if not check_only:
        write('energy_consumption', head, out)
    return {(c.split('.')[-1], s): num(x) for c, _y, s, x in out}


def recompute_xai(k, enc, check_only=False):
    cols = {'imports': 'imports', 'production': 'production', 'exports': 'exports', 'stock_change': 'stockcha',
            'tpes': 'tes', 'stat_diff': 'statdiff', 'transfers': 'transfer', 'own_use': 'ownuse',
            'dist_loss': 'distloss'}
    head, rows = read('xai_energy_balance')
    out = []
    for r in rows:
        r = list(r)
        for c, fl in cols.items():
            j = head.index(c)
            x = k[fl][r[head.index('fuel')]]
            check(not check_only or abs(x - num(r[j])) < TOL, f'xai_energy_balance {c}')
            r[j] = txt(x)
        out.append(r)
    check_only or write('xai_energy_balance', head, out)
    for name, val, sec, fuel in (('xai_energy_use', 'ktoe', 'subsector', 'fuel'),
                                 ('xai_power_demand', 'ktoe_2022', 'subsector', None)):
        head, rows = read(name)
        out = []
        for r in rows:
            r = list(r)
            x = enc[(r[head.index(fuel)] if fuel else 'ele', r[head.index(sec)])]
            check(not check_only or abs(x - num(r[head.index(val)])) < TOL, f'{name} {r[:4]}')
            r[head.index(val)] = txt(x)
            out.append(r)
        check_only or write(name, head, out)


# ------------------------------------------------------------------------------------------------ domestic prices
def perturbed_code(code):
    return code.startswith(('mit.sp.', 'mit.txo.', 'mit.mar.')) or code.endswith('.prod.cost')


def perturb_prices():
    head, rows = read('prices_domestic')
    p = {(r[1], r[2]): num(r[3]) for r in rows}
    n = {key: v * factor() if perturbed_code(key[1]) else v for key, v in p.items()}
    for (year, code), rp in p.items():
        if code.startswith('mit.rp.'):
            k = code[len('mit.rp.'):]

            def form(d, y=year, k=k):
                return (d.get((y, f'mit.sp.{k}'), 0.0) + d.get((y, f'mit.txo.{k}'), 0.0)) * \
                    (1 + d.get((y, f'mit.vatrate.{k}'), 0.0))
            n[(year, code)] = form(n) + (rp - form(p))
    for (year, code), rp in n.items():                              # the identity, with the data's own gap
        if code.startswith('mit.rp.'):
            k = code[len('mit.rp.'):]
            gap = p[(year, code)] - (p.get((year, f'mit.sp.{k}'), 0) + p.get((year, f'mit.txo.{k}'), 0)) * \
                (1 + p.get((year, f'mit.vatrate.{k}'), 0))
            check(abs(rp - (n.get((year, f'mit.sp.{k}'), 0) + n.get((year, f'mit.txo.{k}'), 0)) *
                      (1 + n.get((year, f'mit.vatrate.{k}'), 0)) - gap) < TOL, f'retail price {year} {k}')
    write('prices_domestic', head, [[c, y, code, txt(n[(y, code)])] for c, y, code, _v in rows])
    head, rows = read('prices_domestic_corrections')
    out = []
    for cy, code, old, new, src in rows:
        key = (cy[3:], code)
        if key in p and new != '':
            check(abs(num(new) - p[key]) < 1e-3, f'correction {cy} {code} equals the price')
            r = n[key] / p[key] if p[key] else factor()
            new = txt(n[key])
            old = txt(num(old) * r) if old != '' else old
        out.append([cy, code, old, new, src])
    write('prices_domestic_corrections', head, out)


# ------------------------------------------------------------------------------------------------ household survey
NOT_SHARES = ('pit_share_income', 'pit_share_region')


def perturb_survey():
    head, rows = read('hh_survey')
    by = {}
    for code, var, v in rows:
        by.setdefault(code, {})[var] = num(v)
    variables = {var for _c, var, _v in rows}
    shares = [v for v in variables if v.endswith('_share') and not v.endswith('_acs_share') and v not in NOT_SHARES]
    group = {v: 'dec' if v.startswith('dec_') else 'pov' if v.startswith('pct_belowpl') else v
             for v in variables if v not in shares}
    gf = {g: factor() for g in set(group.values())}
    n = {}
    for code, d in by.items():
        x = {v: d[v] * factor() for v in shares if v in d}
        tot, tot_new = sum(d[v] for v in x), sum(x.values())
        x = {v: s * tot / tot_new for v, s in x.items()} if tot_new else x
        check(abs(sum(x.values()) - tot) < TOL, f'shares {code}')
        for v in d:
            if v not in x:
                x[v] = d[v] * gf[group[v]]
                if (v.endswith('_acs_share') or v.startswith('pct_belowpl')) and d[v] <= 100:
                    x[v] = min(x[v], 100.0)             # a percentage stays a percentage (some data exceed 100)
        n[code] = x
    write('hh_survey', head, [[c, v, txt(n[c][v])] for c, v, _x in rows])


# ------------------------------------------------------------------------------------------------ GTAP input-output
LEVELS = {'DOMCONS', 'Exports', 'HHD', 'Imports', 'Output', 'TOTD'}


def perturb_scatter():
    head, rows = read('tran_scatter')
    write('tran_scatter', head, [[c, code, y, v if code.endswith('.select') else txt(num(v) * factor())]
                                 for c, code, y, v in rows])


def perturb_io():
    head, rows = read('io_gtap')
    sf = {r[3]: factor() for r in rows}
    out = [[c, y, s, sec, txt(num(v) * (sf[sec] if s in LEVELS else factor()))] for c, y, s, sec, v in rows]
    write('io_gtap', head, out)


def main():
    import argparse
    global TIDY
    p = argparse.ArgumentParser()
    p.add_argument('--edition', required=True, help='a public edition holding a copy of the real values')
    args = p.parse_args()
    if ED.info(args.edition)['type'] != 'public-perturbed':
        sys.exit(f'{args.edition} is not a public-perturbed edition (data/editions.csv)')
    TIDY = ED.tidy(args.edition)
    k0, g0 = {}, {}                                   # the copies agree with the balances before anything changes
    for _c, _y, unit, flow, fuel, v in read('energy_balances')[1]:
        (k0.setdefault(flow, {}) if unit == 'ktoe' else g0)[fuel] = num(v)
    recompute_xai(k0, recompute_consumption(k0, g0, check_only=True), check_only=True)
    k, g, _ = perturb_balances()
    recompute_xai(k, recompute_consumption(k, g))
    perturb_prices()
    perturb_survey()
    perturb_io()
    perturb_scatter()
    print('perturbed (factors not stored): energy_balances, energy_consumption, xai_energy_balance, xai_energy_use, '
          'xai_power_demand, prices_domestic, prices_domestic_corrections, hh_survey, io_gtap, tran_scatter')


if __name__ == '__main__':
    main()
