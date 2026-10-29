"""Data step: the elasticities of the country by type, fuel group and sector group (Excel-AI Inputs_ela; legacy
Elasticities tab, column G 'Elasticity use'). EQ-A3.1.

Types: inc (income), usg (own-price, usage), eff (own-price, efficiency), aei (autonomous efficiency improvement).
Each row is the value of the country in a row of the legacy table (core/excel_ai/elasticity_rows.csv: the data
table and its key). Manual elasticities (MTInputs ElIncMainSrc / ElPrcMainSrc = Manual, Manual inputs K279:N307)
replace income and price rows: income at least 0, price at most 0.
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.data.database import to_float

MANUAL_SECTORS = ['tra', 'res', 'ind', 'srv']          # Manual inputs columns K:N


def elasticities(db, iso, base):
    """{type|fuel|sector: value} for the country."""
    tables = {}
    rows = xt.table('elasticity_rows')
    for t in {r['table'] for r in rows}:
        df = db.table(t)
        df = df[df['country'] == iso]
        tables[t] = {(ty, fu, se, co): v for ty, fu, se, co, v in
                     zip(df['type'], df['fuel'], df['sector'], df['code'], to_float(df['value']))}
    inc_manual = str(base['ElIncMainSrc']) == 'Manual'
    prc_manual = str(base['ElPrcMainSrc']) == 'Manual'
    if inc_manual or prc_manual:
        raise NotImplementedError('manual elasticities (Manual inputs K279:N307) are not in Coded CPAT yet')
    out = {}
    for r in rows:
        v = tables[r['table']].get((r['data_type'], r['data_fuel'], r['data_sector'], r['legacy_code']), np.nan)
        out[r['key']] = 0.0 if np.isnan(v) else float(v)            # a blank cell reads as 0
    return out
