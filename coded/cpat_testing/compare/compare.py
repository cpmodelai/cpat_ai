"""Compare Coded CPAT results with Excel-AI, code by code and year by year (NORMS 7; D8 as decided 2026-10-29: the
stored values of the shipped workbook, reference/excel_ai_<version>.csv).

    report = compare(results.by_code(), stems=['infl', 'defl'])   # one row per code: largest differences
    summary(report)                                                # by variable stem
Tolerance: relative 1e-9, absolute 1e-9 near zero (NORMS 7.2).
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from cpat_model import EXCEL_AI_VERSION

REFERENCE = Path(__file__).with_name('reference')
RTOL = ATOL = 1e-9


def reference(version=EXCEL_AI_VERSION):
    df = pd.read_csv(REFERENCE / f'excel_ai_{version}.csv', index_col=0, dtype=str, keep_default_na=False)
    df.columns = [int(c) for c in df.columns]
    return df.apply(lambda c: pd.to_numeric(c.replace('', np.nan), errors='coerce'))


def stem_of(code):
    """`egy.mit.atp.res.coa.2` -> 'atp' (the variable's first token; stems with dots are matched by prefix)."""
    return code.split('.')[2]


def compare(python, stems=None, ref=None, years=None):
    """python: DataFrame index = output code, columns = years. Returns one row per Python code that the reference
    has: max absolute and relative difference, the first year out of tolerance (or None)."""
    ref = reference() if ref is None else ref
    codes = [c for c in python.index if c in ref.index and (stems is None or any(
        c.split('.', 2)[2].startswith(s + '.') or c.split('.', 2)[2] == s + '.' + c.rsplit('.', 1)[1] for s in stems))]
    years = years or [y for y in python.columns if y in ref.columns]
    rows = []
    warnings.filterwarnings('ignore', 'All-NaN slice', RuntimeWarning)
    warnings.filterwarnings('ignore', 'invalid value', RuntimeWarning)
    for c in codes:
        a = pd.to_numeric(python.loc[c, years], errors='coerce').astype(float).values
        b = ref.loc[c, years].astype(float).values
        diff = np.abs(a - b)
        bad = ~((diff <= ATOL) | (diff <= RTOL * np.abs(b)) | (np.isnan(a) & np.isnan(b)))
        rel = np.where(np.abs(b) > ATOL, diff / np.abs(b), diff)
        rows.append(dict(code=c, stem=stem_of(c), max_abs=np.nanmax(diff) if len(diff) else 0.0,
                         max_rel=np.nanmax(rel) if len(rel) else 0.0,
                         first_bad=int(np.array(years)[bad][0]) if bad.any() else None))
    return pd.DataFrame(rows).set_index('code') if rows else pd.DataFrame(
        columns=['stem', 'max_abs', 'max_rel', 'first_bad'])


def missing(python, stems, ref=None):
    """Reference codes of these stems that Python does not produce."""
    ref = reference() if ref is None else ref
    return [c for c in ref.index if stem_of(c) in stems and c not in python.index]


def summary(report):
    if report.empty:
        return report
    g = report.groupby('stem')
    return pd.DataFrame({'codes': g.size(), 'failing': g['first_bad'].apply(lambda s: s.notna().sum()),
                         'max_rel': g['max_rel'].max(), 'first_bad': g['first_bad'].min()})
