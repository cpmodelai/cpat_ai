"""Data steps of block 2 (prices): what Excel-AI computes on its Inputs sheet before Mitigation section 2 reads it.

    international_prices   international energy prices by source and commodity, nominal USD, 2021-2045
                           (Excel-AI Inputs_pint; legacy Mitigation rows 633-695)
    domestic_prices        historical domestic prices (real $/GJ) and forecasting coefficients by price fuel
                           (Excel-AI Inputs_prices; legacy Mitigation rows 745-829)
EQ-A2.3, EQ-A2.4.
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.data.database import to_float

PINT_YEARS = list(range(2021, 2046))
COMMODITIES = ['oil', 'coa', 'nga.lng', 'nga.nam', 'nga.eur']
# source: {commodity: (rule, tidy table, series, first extended year)}; data: the series up to the year before the first
# extended year, then grown with US GDP deflator inflation; trend: then the last growth factor; IEA: the IEA series
SOURCES = {
    'IMF': {'oil': ('data', 'pint_imf', 'POILBRE', 2032), 'coa': ('data', 'pint_imf', 'PCOALAU', 2032),
            'nga.lng': ('data', 'pint_imf', 'PNGASJP', 2032), 'nga.nam': ('data', 'pint_imf', 'PNGASUS', 2032),
            'nga.eur': ('data', 'pint_imf', 'PNGASEU', 2032)},
    # bug M20 fixed: each World Bank series by its name (Excel-AI reads the rows by position: LNG <- Europe, Europe <- LNG)
    'WB': {'oil': ('data', 'pint_wb', 'Crude oil, Brent', 2027), 'coa': ('data', 'pint_wb', 'Coal, Australia', 2027),
           'nga.lng': ('data', 'pint_wb', 'Liquefied natural gas, Japan', 2027),
           'nga.nam': ('data', 'pint_wb', 'Natural gas, US', 2027),
           'nga.eur': ('data', 'pint_wb', 'Natural gas, Europe', 2027)},
    'IEA': {'oil': ('data', 'pint_iea', 'Crude Oil', 2100), 'coa': ('data', 'pint_iea', 'Coal', 2031),
            'nga.lng': ('data', 'pint_iea', 'Natural Gas - LNG', 2100),
            'nga.nam': ('data', 'pint_iea', 'Natural Gas - North Am', 2100),
            'nga.eur': ('data', 'pint_iea', 'Natural Gas - Europe', 2100)},
    'EIA': {'oil': ('trend', 'pint_eia', 'Crude Oil (Brent)', 2051), 'coa': ('trend', 'pint_eia', 'Coal (metric ton)', 2041),
            'nga.lng': ('IEA',), 'nga.nam': ('trend', 'pint_eia', 'Natural Gas - North Am (Henry hub)', 2051),
            'nga.eur': ('IEA',)},
    'AVG': {'oil': ('avg', 'EIA IEA WB IMF'), 'coa': ('avg', 'EIA IEA WB IMF'), 'nga.lng': ('avg', 'IEA WB IMF'),
            'nga.nam': ('avg', 'EIA IEA WB IMF'), 'nga.eur': ('avg', 'IEA WB IMF')},
    'IMF-IEA': {c: ('avg', 'IMF IEA') for c in COMMODITIES},
    'IMF-WB': {c: ('avg', 'WB IMF') for c in COMMODITIES},
    'Manual': {c: ('manual', 2026) for c in COMMODITIES}}
MANUAL_LABEL = {'oil': 'Crude Oil', 'coa': 'Coal', 'nga.lng': 'Natural Gas - LNG', 'nga.nam': 'Natural Gas - North Am',
                'nga.eur': 'Natural Gas - Europe'}
EU_LNG = {2022: 0.58, 2023: 0.603, 2024: 1 - (0.303 + 0.229) / 2, 2025: 1 - (0.303 + 0.229) / 2 + 0.1}
GAS_MARKET = {'LNG': 'lng', 'Europe': 'eus', 'North Am': 'nam'}          # else global (glo)


def _series(db, table, name):
    df = db.table(table)
    key = 'subject_code' if table == 'pint_imf' else 'commodity'
    df = df[df[key] == name]
    return dict(zip(df['year'].astype(int), to_float(df['value']).fillna(0.0)))   # a blank cell reads as 0


def _avg(values):
    v = [x for x in values if not np.isnan(x)]                     # AVERAGE skips the "NA" text
    return sum(v) / len(v) if v else np.nan


def international_prices(db, us_inflation):
    """EQ-A2.3. {source|commodity: {year: nominal price}} for 2021-2045; NaN where Excel-AI shows "NA".
    us_inflation: {year: US GDP deflator growth} (macro series usinfl)."""
    out = {}
    for src in ('IMF', 'WB', 'IEA', 'EIA'):
        for com in COMMODITIES:
            spec = SOURCES[src][com]
            if spec[0] == 'IEA':
                out[f'{src}|{com}'] = dict(out[f'IEA|{com}'])
                continue
            rule, table, name, first_ext = spec
            data, v = _series(db, table, name), {}
            for y in PINT_YEARS:
                if y < first_ext:
                    # past its data a series reads nothing (Excel-AI reads a misaligned cell there: issue I152)
                    v[y] = data.get(y, np.nan)
                elif rule == 'data':
                    v[y] = v.get(y - 1, np.nan) * (1 + us_inflation[y])
                else:
                    v[y] = v[y - 1] * (v[y - 1] / v[y - 2])
            out[f'{src}|{com}'] = v
    for src in ('AVG', 'IMF-IEA', 'IMF-WB'):
        for com in COMMODITIES:
            parts = SOURCES[src][com][1].split()
            out[f'{src}|{com}'] = {y: _avg([out[f'{p}|{com}'][y] for p in parts]) for y in PINT_YEARS}
    man = db.table('mi_intl_prices')
    for com in COMMODITIES:
        m = man[man['commodity'] == MANUAL_LABEL[com]]
        m = dict(zip(m['year'].astype(int), to_float(m['value'])))
        out[f'Manual|{com}'] = {y: out[f'IMF|{com}'][y] if y < 2026 else m.get(y, np.nan) for y in PINT_YEARS}
    for src in SOURCES:
        lng, nam, eur = (out[f'{src}|nga.{k}'] for k in ('lng', 'nam', 'eur'))
        out[f'{src}|nga.glo'] = {y: (out[f'IMF|nga.glo'][y] if src == 'Manual' and y < 2026
                                     else _avg([lng[y], nam[y], eur[y]])) for y in PINT_YEARS}
        share = {y: EU_LNG.get(min(y, 2025), 0) if y >= 2022 else 0 for y in PINT_YEARS}
        out[f'{src}|nga.eus'] = {y: eur[y] * (1 - share[y]) + lng[y] * share[y] for y in PINT_YEARS}
    return out


def gas_market(db, iso):
    """The gas price commodity of the country (Prices_int regional assumptions): nga.lng, nga.eus, nga.nam or nga.glo."""
    ra = db.table('pint_regional_assumptions')
    names = db.table('countries_attributes')
    name = names.loc[names['code'] == iso, 'name']
    name = name.iloc[0] if len(name) else ''
    m = ra.loc[(ra['country'] == name) & (ra['variable'] == 'Natural gas market assumption'), 'value']
    return 'nga.' + GAS_MARKET.get(m.iloc[0] if len(m) else '', 'glo')


# ---- domestic prices
PRICES = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind', 'gso.all', 'die.all', 'lpg.all',
          'ker.all', 'oop.all', 'bio.all']
HIST_YEARS = [2021, 2022, 2023, 2024]
MARGIN_YEAR = 2024                       # Excel-AI reads the coal and gas margins at 2024 (typed; issue I101)
RP_FROM_DATA = {'coa', 'nga', 'bio'}     # historical retail price from data; oil products: supply cost + taxes
OIL_SHARE = {'gso.all', 'die.all', 'lpg.all', 'ker.all'}
VAT_CONSUMER = {'coa.res', 'nga.res', 'gso.all', 'die.all', 'lpg.all', 'ker.all', 'oop.all'}
MPU_VARS = ('sp', 'vatrate', 'txo', 'rp', 'pros')   # the domestic price codes that a manual value can replace (R8)


class DomesticData:
    """The domestic price data of one country (Prices_dom, manual values where MTInputs DomPrTax is on)."""

    def __init__(self, db, iso, manual_on):
        df = db.table('prices_domestic')
        df = df[df['country'] == iso]
        self.raw = {(int(y), c): v for y, c, v in zip(df['year'], df['code'], df['value'])}
        self.manual = {}
        if manual_on:
            for t in [n for n in db.tables if n.startswith('mi_prices_')]:
                m = db.table(t)
                for c, y, v in zip(m['code'], m['year'], m['value']):
                    if v not in ('', None):
                        self.manual[(int(y), c)] = v

    def value(self, year, code):
        """A Prices_dom value, blank = 0."""
        try:
            return float(self.raw.get((year, code), ''))
        except ValueError:
            return 0.0

    def text(self, year, code):
        """The value used (manual where flagged, else Prices_dom) as Excel-AI's table MPU holds it: text, '' = blank."""
        if code.split('.')[1] in MPU_VARS and (year, code) in self.manual:
            return str(self.manual[(year, code)])
        return self.raw.get((year, code), '')

    def used(self, year, code):
        """mp_use: the value used, blank = 0 (only the codes of table MPU; others 0)."""
        if code.split('.')[1] not in MPU_VARS:
            return 0.0
        t = self.text(year, code)
        try:
            return float(t)
        except ValueError:
            return 0.0


def domestic_prices(db, iso, settings, cpi_index, pass_lo, pass_mid, pass_hi, price_controls, manual_on):
    """EQ-A2.4. {price code: {coefficient: value}} for one country; cpi_index: {year: CPI index (ResultsYear = 1)}."""
    d = DomesticData(db, iso, manual_on)
    fuels = {r['fuel']: r for r in xt.table('fuels')}
    ops = db.table('oil_product_shares')
    ops = dict(zip(ops.loc[ops['country'] == iso, 'variable'], to_float(ops.loc[ops['country'] == iso, 'value'])))
    ctrl = db.table('mi_price_controls')
    ctrl = dict(zip(ctrl['code'], to_float(ctrl.iloc[:, -1])))
    base, last = settings.base_year, settings.last_hist_price_year
    out = {}
    for pc in PRICES:
        fuel = pc.split('.')[0]
        gj = float(fuels[fuel]['gj_per_unit'])
        p = {'gj': gj, 'rpd': 1.0 if fuel in RP_FROM_DATA else 0.0}
        p['pccr'] = 1.0 if fuel == 'bio' else d.value(base, f'mit.ps.{pc}')
        p['pccb'] = 0.0 if p['pccr'] <= pass_lo else (pass_mid if p['pccr'] <= pass_hi else 1.0)
        pcm = ctrl.get(f'mit.rp.{pc}.ctrl', np.nan)
        p['pcm'] = 1.0 if np.isnan(pcm) else pcm
        pcs = str(price_controls)
        p['pcc'] = p['pcm'] if pcs[:6].lower() == 'manual' else (1.0 if pcs[:4].lower() == 'none' else p['pccb'])
        p['mary'] = MARGIN_YEAR if fuel in ('coa', 'nga') else base
        p['mar'] = 0.0 if fuel == 'bio' else d.value(p['mary'], f'mit.mar.{pc}')
        p['mcpi'] = cpi_index[p['mary']]
        p['dsh'] = max(0.0, min(1.0, d.value(base, f'mit.{fuel}.prod'))) if fuel in ('coa', 'nga') else 0.0
        p['pcost'] = d.value(base, f'mit.{fuel}.prod.cost') if fuel in ('coa', 'nga') else 0.0
        p['bcpi'] = cpi_index[base]
        p['fixsp'] = (p['mar'] * p['mcpi'] + p['dsh'] * p['pcost'] * p['bcpi']) / gj
        p['vatc'] = 1.0 if pc in VAT_CONSUMER else 0.0
        osh = ops.get(f'{fuel}_share', np.nan) if pc in OIL_SHARE else 1.0
        p['osh'] = 1.0 if np.isnan(osh) else osh
        for y in HIST_YEARS:
            vat_weo = d.value(y, 'VAT_WEO')
            rpn, spn, txn = (d.used(y, f'mit.{v}.{pc}') for v in ('rp', 'sp', 'txo'))
            vrb = d.text(y, f'mit.vatrate.{pc}') == ''
            vry = p['vatc'] * vat_weo if vrb else d.used(y, f'mit.vatrate.{pc}')
            p[f'vry{y}'] = vry
            p[f'sp{y}'] = spn * cpi_index[y] / gj
            p[f'txo{y}'] = ((rpn / (1 + vry) - spn) if p['rpd'] == 1 else txn) * cpi_index[y] / gj
        p['vr'] = p[f'vry{last}'] * p['osh']
        p['vat_weo'] = {y: d.value(y, 'VAT_WEO') for y in HIST_YEARS}   # the general VAT rate (bug M15: by year)
        p['spL'], p['txoL'] = p[f'sp{last}'], p[f'txo{last}']
        out[pc] = p
    return out
