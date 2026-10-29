"""Phase 4: the distribution module matches Excel-AI Distribution 0.1.3's stored values for Egypt, scenario groups 1
and 2 (scenarios 1 and 2 against the baseline): every code of the Distribution sheet, the basket and the ten deciles."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import cpat_model
from cpat_testing.compare.known_differences import KNOWN, bug_of
from cpat_model.inputs import read_scenario_set

REFERENCE = Path(__file__).parent / 'compare' / 'reference' / 'excel_ai_distribution_0.1.3.csv'
SECTIONS = {'1 settings': ('YearDistn', 'support'), '2 inputs from mitigation': ('dpr', 'rev'),
            '3 indirect price changes': ('grev', 'dprw'), '4-6 price factors, budget shares, effects': ('eps', 'tef'),
            '7 national accounts': ('consgdpyr', 'tot_cons_na'), '8 revenue recycling': ('rpit', 'rec'),
            '9 net effect, Gini': ('compden', 'net'), '10 chart outputs': ('dname', 'gini.pti'),
            '11 sector prices': ('dps', 'ppic')}


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(read_scenario_set()).distribution_by_code('EGY')


def matches(x, e):
    """A cell: text equal as text, numbers within 1e-9 (relative above 1), both blank or both NaN."""
    blank = lambda v: v is None or (isinstance(v, float) and np.isnan(v)) or v == ''
    if blank(e) or blank(x):
        return blank(e) and blank(x)
    try:
        ef = float(e)
    except ValueError:
        return str(x) == e
    try:
        return abs(float(x) - ef) <= 1e-9 * max(1.0, abs(ef))
    except (TypeError, ValueError):
        return False


def section_codes(ref, first, last):
    """The reference codes from the first row of variable `first` to the last of `last` (sheet order)."""
    stems = [c.split('.')[2] if c.split('.')[2] != 'gini' else '.'.join(c.split('.')[2:4]) for c in ref.index]
    i0, i1 = stems.index(first), len(stems) - 1 - stems[::-1].index(last)
    return list(ref.index[i0:i1 + 1])


@pytest.mark.parametrize('section', SECTIONS)
def test_section_matches_excel_ai(results, section):
    ref = pd.read_csv(REFERENCE, index_col=0, dtype=str, keep_default_na=False)
    codes = section_codes(ref, *SECTIONS[section])
    missing = sorted(set(codes) - set(results.index))
    assert not missing, missing[:20]
    bad = [(c, d, ref.loc[c, str(d)], results.loc[c, d]) for c in codes if not bug_of(c) for d in range(11)
           if not matches(results.loc[c, d], ref.loc[c, str(d)])]
    assert not bad, bad[:10]


def test_known_differences(results):
    """M22 (fixed in Coded CPAT, open in Excel-AI): the percentile recycling rows of scenario group 2, which uses public
    investment, differ from Excel-AI; group 1 (no recycling) still matches. Delete the entry when Excel-AI fixes it."""
    ref = pd.read_csv(REFERENCE, index_col=0, dtype=str, keep_default_na=False)
    for stem in (s for s in KNOWN.get('M22', []) if s.startswith('distn.')):
        for n, differ in (('1', False), ('2', True)):
            code = f'egy.{stem}.{n}'
            same = all(matches(results.loc[code, d], ref.loc[code, str(d)]) for d in range(11))
            assert same != differ, f'{code}: expected {"a difference" if differ else "a match"}'

