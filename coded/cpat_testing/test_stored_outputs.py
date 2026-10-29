"""Phase 5.1: every scenario of Excel-AI's scenario set, not only the two live groups. Excel-AI's StoredOutputs sheet
keeps the key output codes of scenarios 1 and 3-6 (filled by the builder's emulation of RunAllScenarios, without the
ETS goal seek); Coded CPAT must equal them within 1e-9 (relative above 1), every year."""
from pathlib import Path

import pandas as pd
import pytest

import cpat_model
from cpat_model import EXCEL_AI_VERSION
from cpat_model.inputs import read_scenario_set

STORED = Path(__file__).parent / 'compare' / 'reference' / f'excel_ai_{EXCEL_AI_VERSION}_stored_outputs.csv'


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(read_scenario_set()).by_code('EGY')


@pytest.mark.parametrize('scenario', ['1', '3', '4', '5', '6'])
def test_stored_outputs(results, scenario):
    ref = pd.read_csv(STORED, index_col='code')
    ref = ref[ref.index.str.endswith('.' + scenario)]
    assert len(ref) > 100
    missing = sorted(set(ref.index) - set(results.index))
    assert not missing, missing[:10]
    bad = []
    for code, row in ref.iterrows():
        for y, x in row.dropna().items():
            p = float(results.loc[code, int(y)])
            if abs(p - x) > 1e-9 * max(1.0, abs(x)):
                bad.append((code, y, x, p))
                break
    assert not bad, bad[:10]
