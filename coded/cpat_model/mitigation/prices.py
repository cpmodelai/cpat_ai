"""Block 2, prices: international prices, the producer subsidies, and the price build-up before new policies by price
fuel (Mitigation section 2, rows gp to ppcw). Quantity-free: computed for all years in the prepare stage. The rows that
average the after-tax prices over the fuel blocks (pnq, pctx, ..., rpn, pav.*) need fuel use: block 3.9.

    international   gpn, gp: the international price of the scenario's source (real), with the High / Low factors
    producer        pros, psd, psu: producer subsidies (from section 1 of Excel-AI)
    build-up        gpi, spf, ps, sp, txf, txo, fadtx, cs, etx, esub, esubpu, vat, pbc, pcsw, ppcw (EQ-M2.1-M2.3)
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import Rows, safe_div
from cpat_model.mitigation import prices_data as pdx
from cpat_model.mitigation.policies import is_true

GP_ROWS = ['oil', 'coa', 'nga', 'one']                       # international price rows (gp position 1-4)
GP_POS = {'gso': 1, 'die': 1, 'lpg': 1, 'ker': 1, 'oop': 1, 'coa': 2, 'nga': 3, 'bio': 4}
PSU_FUELS = ['oil', 'coa', 'nga', 'bio']                     # producer subsidy per unit, in gp order
PROS_FUELS = ['coa', 'nga', 'oil', 'bio', 'ecy']
WORLD_DEMAND = {'oil': 'Oil', 'coa': 'Coal', 'nga': 'Natural gas'}
DEMAND_SCENARIOS = ['stated policies', 'announced pledges', 'sustainable development', 'net zero']


def world_demand(db, scenario):
    """{fuel: {year: MTOE}}: global fuel production of the IEA scenario (MTInputs GlobalEnergyDemand; Excel-AI WDIdx:
    the first, second or third scenario row of the fuel)."""
    s = str(scenario).lower()
    idx = next((i + 1 for i, k in enumerate(DEMAND_SCENARIOS) if s.startswith(k) and (i == 0 or s == k)), 1)
    idx = min(idx, 3)
    df = db.table('pint_world_demand')
    out = {}
    for f, name in WORLD_DEMAND.items():
        g = df[df['fuel'] == name]
        no = sorted(g['scenario_no'].unique(), key=int)[idx - 1]
        g = g[g['scenario_no'] == no]
        out[f] = dict(zip(g['year'].astype(int), g['value'].astype(float)))
    return out


def domestic_use(db, iso, fuel):
    """Excel-AI ConsCoa / ConsGas / ConsBio: energy use of the fuel over the sectors other than electricity output and
    international bunkers (EnergyCons, the first row of the code)."""
    df = db.table('energy_consumption')
    df = df[df['code'] == f'{iso.lower()}.mit.enc.{fuel}']
    if df.empty:
        return 0.0
    df = df[df['year'] == df['year'].iloc[0]]
    return float(pdx.to_float(df.loc[~df['sector'].isin(['elec', 'wav']), 'value']).fillna(0).sum())


def prepare(state, db, inputs, settings, baseline):
    """EQ-M2.1 to EQ-M2.3, EQ-A2.1, EQ-A2.3 to EQ-A2.5 (Mitigation section 2, the build-up before new policies)."""
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    t, n = R.t, inputs.number
    g = lambda name: inputs[name]
    G = lambda name: settings.global_settings.get(name, inputs[name])
    c = xt.constant
    last = settings.last_hist_price_year
    hist = t <= last
    k_last = years.index(last)
    defl = R.of('defl')

    # international prices (EQ-A2.3): the scenario's source, real, x High / Low factor after the last historical year
    src = str(g('IntEnerPricForeSource')).replace('*', '')
    adj = str(g('IntEnerPricForecastAdjustment'))
    adj = 2 if adj[:4].lower() == 'high' else (3 if adj[:3].lower() == 'low' else 1)
    R.put('gp.src', src)
    R.put('gp.adj', float(adj))
    gp = {}
    pint, market = {}, {}
    for iso in countries:
        usinfl = dict(zip(state['macro.usinfl']['year'].values, state['macro.usinfl'].sel(country=iso).values))
        pint[iso] = pdx.international_prices(db, usinfl)
        market[iso] = pdx.gas_market(db, iso)
    for k in GP_ROWS:
        if k == 'one':
            gpn = 1.0
        else:
            com = {'oil': 'oil', 'coa': 'coa', 'nga': None}[k]
            gpn = np.array([[pint[iso][f'{src}|{com or market[iso]}'][y] for y in years] for iso in countries])
        R.put('gpn', gpn, 'int', k)
        factor = 1.0 if k == 'one' or adj == 1 else c(f'gp.{"hi" if adj == 2 else "lo"}|{k}')
        gp[k] = R.put('gp', 1.0 if k == 'one' else gpn * defl * np.where(t > last, factor, 1.0), 'int', k)

    # producer subsidies (pros, psd, psu): data up to the last historical year, then held x the phase-out factor
    cpi = R.of('infl')
    data = {iso: pdx.DomesticData(db, iso, is_true(G('DomPrTax')) or str(G('DomPrTax'))[:3].lower() == 'yes')
            for iso in countries}
    wd = world_demand(db, G('GlobalEnergyDemand'))
    cons = {f: np.array([[domestic_use(db, iso, f)] for iso in countries]) for f in ('coa', 'nga', 'bio')}
    for f in PROS_FUELS:
        v = np.array([[data[iso].used(y, f'mit.pros.{f}.all') for y in years] for iso in countries])
        held = np.where(hist, v * cpi * c('MperBn'), np.nan)
        for k in range(k_last + 1, len(years)):
            held[:, k] = held[:, k - 1]
        R.put('pros', held, 'all', f)
    for f in PSU_FUELS:
        w = np.array([wd[f].get(y, np.nan) for y in years]) * c('Thousand') if f != 'bio' else None
        psd = {'oil': lambda: w * c('LitersPerKtoeOil'), 'coa': lambda: (w + cons['coa']) / 2 * c('MethGJperKtoe'),
               'nga': lambda: (w + cons['nga']) / 2 * c('MethGJperKtoe'),
               'bio': lambda: cons['bio'] * c('MethGJperKtoe')}[f]()
        R.put('psd', psd, 'all', f)
    psu = {}
    for f in PSU_FUELS:
        pros = R.of('pros', 'all', f)
        per_unit = np.nan_to_num(safe_div(-pros * c('USDperM'), R.of('psd', 'all', f), np.nan))
        psu[f] = R.put('psu', np.where(hist, per_unit, per_unit[:, [k_last]] * R.of('psf', 'all', f)), 'all', f)

    # domestic prices before new policies (EQ-A2.4, EQ-M2.1-M2.3)
    cpi_idx = {iso: dict(zip(state['macro.cpiidx']['year'].values, state['macro.cpiidx'].sel(country=iso).values))
               for iso in countries}
    dp = {iso: pdx.domestic_prices(db, iso, settings, cpi_idx[iso], G('PassLo'), G('PassMid'), G('PassHi'),
                                   G('GovPriceControls'),
                                   is_true(G('DomPrTax')) or str(G('DomPrTax'))[:3].lower() == 'yes')
          for iso in countries}
    col = lambda pc, k: np.array([[dp[iso][pc][k]] for iso in countries])            # (country, 1)
    hist_val = lambda pc, v: np.array([[dp[iso][pc].get(f'{v}{y}', np.nan) for y in years] for iso in countries])
    for pc in pdx.PRICES:
        fuel, sec = pc.split('.')
        pos = GP_POS[fuel]
        pcc, vr, gj = col(pc, 'pcc'), col(pc, 'vr'), col(pc, 'gj')
        gpi = R.put('gpi', gp[GP_ROWS[pos - 1]], sec, fuel)
        spf = R.put('spf', col(pc, 'fixsp'), sec, fuel)
        ps = R.put('ps', psu[PSU_FUELS[pos - 1]] * (c('LitersPerBbl') if fuel == 'oop' else 1.0) / gj, sec, fuel)
        sp, txf, txo = hist_val(pc, 'sp'), hist_val(pc, 'txo'), hist_val(pc, 'txo')
        txo_last = txo[:, [k_last]]
        for k in range(k_last + 1, len(years)):            # after the last historical year (EQ-M2.1, EQ-M2.2)
            sp[:, k] = spf[:, 0] + (sp[:, k - 1] - spf[:, 0] - ps[:, k - 1]) * gpi[:, k] / gpi[:, k - 1] + ps[:, k]
            txf[:, k] = txf[:, k - 1] - (sp[:, k] - sp[:, k - 1]) * (1 - pcc[:, 0])
            txo[:, k] = np.where(txo_last[:, 0] >= 0, np.maximum(txo_last[:, 0], txf[:, k]), txf[:, k])
        R.put('sp', sp, sec, fuel)
        R.put('txf', txf, sec, fuel)
        R.put('txo', txo, sec, fuel)
        fadtx = R.put('fadtx', pcc * np.where(hist, txo, txo_last), sec, fuel)
        cs = R.put('cs', txo - fadtx, sec, fuel)
        R.put('etx', np.maximum(txo, 0), sec, fuel)
        esub = R.put('esub', np.minimum(txo, 0), sec, fuel)
        R.put('esubpu', esub * gj, sec, fuel)
        R.put('vat', (sp + txo) * vr, sec, fuel)
        R.put('pbc', (sp + txo) * (1 + vr), sec, fuel)
        R.put('pcsw', -(1 - R.of('csf', sec, fuel)) * np.minimum(fadtx, 0), sec, fuel)
        R.put('ppcw', -(1 - R.of('pcf', sec, fuel)) * cs, sec, fuel)
    state['_prices'] = {'domestic': dp, 'international': pint, 'gas_market': market}
    R.finish()
