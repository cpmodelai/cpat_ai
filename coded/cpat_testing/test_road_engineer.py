"""The engineer road model switched on (TrModel = Engineer): road gasoline, diesel, LPG, gas and biofuels from section
5b (EQ-M3.2) and road electricity demand from it after the base year (EQ-M4.1), with everything downstream. Scenario 2
of Excel-AI's scenario set with TrModel = Engineer must equal Excel-AI's release workbook recalculated the same way
(LibreOffice, reference/excel_ai_<v>_engineer.csv, written by compare/make_engineer_reference.py), every code and year
within 1e-9 (relative above 1). LibreOffice reproduces Excel's stored values of the shipped scenarios exactly (the
script checks it each time it writes the reference)."""
from pathlib import Path

import pandas as pd
import pytest

import cpat_model
from cpat_model import EXCEL_AI_VERSION
from cpat_model.inputs import read_scenario_set
from cpat_testing.compare.compare import compare, reference, summary
from cpat_testing.compare.known_differences import bug_of

REF = Path(__file__).parent / 'compare' / 'reference'


def engineer_set():
    """Scenarios 1 and 2 of Excel-AI's scenario set, scenario 2 with the engineer road model."""
    s = read_scenario_set()
    s.cols = ['1', '2']
    for row in s.rows:
        if row['name'] == 'TrModel':
            row['2'] = 'Engineer'
    return s


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(engineer_set()).by_code('EGY')


def test_switch_is_on(results):
    years = list(range(2022, 2042))
    assert (results.loc['egy.mit.tr.sw.all.all.2', years].astype(float) == 1).all()
    assert (results.loc['egy.mit.tr.sw.all.all.1', years].astype(float) == 0).all()


def test_engineer_scenario_matches_excel_ai(results):
    ref = reference(f'{EXCEL_AI_VERSION}_engineer')
    expected = [c for c in ref.index if ref.loc[c].notna().any() and not bug_of(c)]
    missing = sorted(set(expected) - set(results.index))
    assert not missing, missing[:20]
    report = compare(results.loc[expected], ref=ref)
    assert report['first_bad'].isna().all(), summary(report[report['first_bad'].notna()])


def test_switch_changes_the_results(results):
    """The switch reaches fuel use, power demand and CO2 (else the test above would pass trivially)."""
    elastic = reference()
    for code in ('egy.mit.ener.rod.gso.2', 'egy.mit.dem.rod.ecy.2', 'egy.mit.co2.tot.gso.2'):
        assert not (results.loc[code, 2030] == pytest.approx(elastic.loc[code, 2030], rel=1e-6)), code


def test_baseline_unchanged(results):
    """Scenario 1 keeps the elasticity model and Excel-AI's stored values."""
    ref = reference()
    expected = [c for c in ref.index if c.endswith('.1') and ref.loc[c].notna().any() and not bug_of(c)]
    report = compare(results.loc[[c for c in expected if c in results.index]], ref=ref)
    assert report['first_bad'].isna().all(), summary(report[report['first_bad'].notna()])
