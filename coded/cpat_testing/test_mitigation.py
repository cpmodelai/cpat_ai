"""Phase 3: the mitigation blocks built so far match Excel-AI's stored values for Egypt, code by code and year by year
(NORMS 7). BUILT lists the variable stems of the blocks done; each block adds its stems."""
import pytest

import cpat_model
from cpat_model.inputs import read_scenario_set
from cpat_testing.compare.compare import compare, reference, summary

BUILT = {
    '3.1 header': ['infl', 'defl', 'gdp.usd', 'gdp.lcu', 'xr', 'gdp.base'],
}


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(read_scenario_set()).by_code('EGY')


@pytest.mark.parametrize('block', BUILT)
def test_block_matches_excel_ai(results, block):
    ref = reference()
    stems = BUILT[block]
    report = compare(results, stems=stems, ref=ref)
    assert not report.empty
    assert report['first_bad'].isna().all(), summary(report)
    expected = [c for c in ref.index if c.startswith('egy.mit.') and c.rsplit('.', 1)[1] in ('1', '2') and any(
        c.split('.', 2)[2] == f'{s}.{c.rsplit(".", 1)[1]}' or c.split('.', 2)[2].startswith(f'{s}.all.') for s in stems)]
    assert set(expected) <= set(report.index), sorted(set(expected) - set(report.index))
