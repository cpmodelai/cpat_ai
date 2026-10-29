"""Phase 3: the mitigation blocks built so far match Excel-AI's stored values for Egypt, code by code and year by year
(NORMS 7). Each block lists its variables (core/variables.csv names): every reference code of those variables
(scenarios 1 and 2) must be produced and match."""
import pandas as pd
import pytest

import cpat_model
from cpat_model.core.variables import PATH as VARIABLES_CSV
from cpat_model.inputs import read_scenario_set
from cpat_testing.compare.compare import compare, reference, summary


def section(first, last, without=()):
    """The variables of the Mitigation rows from `first` to `last` (sheet order), less `without`."""
    v = pd.read_csv(VARIABLES_CSV)
    i0, i1 = v.index[v['variable'] == first][0], v.index[v['variable'] == last][-1]
    return sorted(set(v.loc[i0:i1, 'variable']) - set(without))


DEFERRED_1 = ['airpol.mc', 'pig.ap', 'cc.code', 'pig.tr', 'pigx', 'ntxg', 'xcpb', 'xpre', 'ntxb', 'pig.fe0', 'pig.wsh',
              'pig.mu0', 'pig.rsh0', 'pig.kpl', 'pig.trb.acc', 'pig.trb.con', 'pig.trb.rdm', 'pig.phi', 'pig.efw', 'pig.vpm', 'pig.trk', 'pig.trg.acc', 'pig.trg.con', 'pig.trg.rdm']
BUILT = {
    '3.1 header': ['infl', 'defl', 'gdp.usd', 'gdp.lcu', 'xr', 'gdp.base'],
    '3.2 policies': section('CPIntro', 'cptraj', DEFERRED_1),
    '3.3 prices': ['IntEnerPricForeSource', 'IntEnerPricForecastAdjustment', 'gp.src', 'gp.adj', 'gpn', 'gp', 'gpi',
                   'spf', 'esubpu', 'ps', 'sp', 'txf', 'txo', 'fadtx', 'cs', 'etx', 'esub', 'vat', 'pbc', 'pcsw', 'ppcw'],
}


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(read_scenario_set()).by_code('EGY')


@pytest.mark.parametrize('block', BUILT)
def test_block_matches_excel_ai(results, block):
    ref = reference()
    v = pd.read_csv(VARIABLES_CSV)
    stems = set(BUILT[block])
    codes = {c[:-2] for c, var in zip(v['code'], v['variable']) if var in stems}          # without the scenario
    expected = [c for c in ref.index if c[:-2] in codes and c[-1] in '12']
    missing = sorted(set(expected) - set(results.index))
    assert not missing, missing[:20]
    report = compare(results.loc[expected], ref=ref)
    assert report['first_bad'].isna().all(), summary(report[report['first_bad'].notna()])
