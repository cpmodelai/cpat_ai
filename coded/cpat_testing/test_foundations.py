"""Phase 2 foundations: version, scenario set, database, placeholder modules, a run end to end."""
import re

import cpat_model
from cpat_model.data import open_database
from cpat_model.inputs import read_scenario_set
from cpat_model.settings import Settings


def test_version():
    assert re.fullmatch(r'\d+\.\d+\.\d+p\d+\.\d+', cpat_model.__version__)
    assert cpat_model.__version__.startswith(cpat_model.EXCEL_AI_VERSION + 'p')


def test_scenario_set_is_excel_ai():
    ss = read_scenario_set()
    assert ss.numbers() == [1, 2, 3, 4, 5, 6]
    assert ss.inputs(1)['CPLevelTarget'] in (0.0, None) or ss.inputs(1).name.startswith('Baseline')
    assert ss.inputs(2)['CPLevelTarget'] == 20.0
    assert ss.inputs(2)['ModelForm'] == 'CPAT'
    assert set(ss.global_settings()) >= {'BiomassLeakage', 'NatGasEff'}


def test_database_reads_tidy_tables():
    db = open_database(Settings())
    assert 'energy_balances' in db.tables
    v = db.array('energy_balances', ['country', 'flow', 'fuel']).sel(country='EGY', flow='cement', fuel='coa').item()
    assert v == 1422.2413


def test_run_end_to_end_with_placeholders():
    res = cpat_model.run(read_scenario_set(), Settings(countries=('EGY', 'XXX')))
    s2 = res.states[2]
    assert s2['air.vpm'].sel(country='EGY', year=2023).item() == 0.290688
    assert s2['air.vpm'].sel(country='XXX').sum().item() == 0.0          # I106: other countries 0
    assert s2['tran.rdm.km'].sel(country='EGY', year=2030).item() == 0.12
