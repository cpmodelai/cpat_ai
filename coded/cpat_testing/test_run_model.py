"""Plan task 6.1: the command line runs a scenario set and writes the results by country (run_model.py)."""
import pandas as pd

import run_model


def test_run_model_writes_results(tmp_path):
    run_model.main(['--scenarios', '1', '2', '--out', str(tmp_path)])
    mit = pd.read_csv(tmp_path / 'mitigation_EGY.csv', index_col='code')
    dist = pd.read_csv(tmp_path / 'distribution_EGY.csv', index_col='code')
    assert {'variable', 'unit', '2022', '2041'} <= set(mit.columns)
    assert float(mit.loc['egy.mit.co2.tot.tot.2', '2030']) > 0
    assert 'egy.distn.net.tot.dec.ove.2' in dist.index


def test_country_without_data_is_a_clear_error(tmp_path):
    """Phase 5.2: only Egypt has its base tables in the dummy database; another country stops with the reason."""
    import pytest
    with pytest.raises(ValueError, match='KEN: energy_balances, prices_domestic'):
        run_model.main(['--countries', 'KEN', '--scenarios', '1', '2', '--out', str(tmp_path)])
