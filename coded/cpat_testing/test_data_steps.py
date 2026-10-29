"""The data steps (what Excel-AI computes on its Inputs sheet) match the stored values of the shipped workbook for
Egypt (cpat_testing/compare/reference/excel_ai_<v>_inputs.csv: row, col, value)."""
from functools import lru_cache

import numpy as np
import pandas as pd
import pytest

from cpat_model import EXCEL_AI_VERSION
from cpat_model.core.excel_ai_tables import constant as c
from cpat_model.data import open_database
from cpat_model.inputs import read_scenario_set
from cpat_model.mitigation import ef_data, elasticity_data, header, policies, power_data, prices_data
from cpat_model.settings import Settings
from cpat_testing.compare.compare import REFERENCE

ISO = 'EGY'


@lru_cache(maxsize=1)
def cells():
    d = pd.read_csv(REFERENCE / f'excel_ai_{EXCEL_AI_VERSION}_inputs.csv', dtype=str, keep_default_na=False)
    return {(int(r), int(k)): v for r, k, v in zip(d['row'], d['col'], d['value'])}


def ref(row, col):
    v = cells().get((row, col), '')
    try:
        return float(v)
    except ValueError:
        return v


def differences(pairs, tol=1e-9):
    bad = []
    for key, py, xl in pairs:
        if isinstance(xl, float):
            ok = (py == xl or (isinstance(py, (int, float, np.floating)) and not np.isnan(py)
                               and abs(py - xl) <= tol * max(1.0, abs(xl))))
        else:
            ok = (xl in ('', 'NA') and isinstance(py, float) and np.isnan(py)) or str(py) == xl
        if not ok:
            bad.append((key, py, xl))
    return bad


@pytest.fixture(scope='module')
def ctx():
    ss = read_scenario_set()
    st = Settings().with_globals(ss.global_settings(), ss.inputs(1))
    db = open_database(st)
    state = {}
    header.prepare(state, db, ss.inputs(1), st, None)
    series = lambda k: dict(zip(state[k]['year'].values, state[k].sel(country=ISO).values))
    ps = power_data.power_settings(db, ISO, st.base, c)
    tech = power_data.power_tech(db, ISO, st.base, st, ps, c)
    return dict(st=st, db=db, cpi=series('macro.cpiidx'), usinfl=series('macro.usinfl'), gdppc=series('macro.gdppc'),
                ps=ps, tech=tech)


def test_prices(ctx):
    ip = prices_data.international_prices(ctx['db'], ctx['usinfl'])
    pairs = [(f'{ref(r, 1)} {2021 + k - 10}', ip[ref(r, 1)][2021 + k - 10], ref(r, k))
             for r in range(539, 595) for k in range(10, 35)]
    bad = [b for b in differences(pairs) if not (b[0].startswith(('IEA', 'EIA|nga', 'AVG', 'IMF-IEA'))
                                                and int(b[0][-4:]) >= 2041)]     # issue I152
    assert not bad, bad[:10]
    dp = prices_data.domestic_prices(ctx['db'], ISO, ctx['st'], ctx['cpi'], 0.25, 0.5, 0.5, 'Bucketed*', False)
    cols = {7: 'gj', 9: 'pccr', 10: 'pccb', 11: 'pcc', 13: 'mar', 15: 'pcost', 16: 'dsh', 18: 'fixsp', 22: 'vr',
            23: 'spL', 24: 'txoL'}
    assert not differences([(f'{ref(r, 1)}.{k}', dp[ref(r, 1)][k], ref(r, col)) for r in range(158, 170)
                            for col, k in cols.items()])


def test_power(ctx):
    st, db, ps, tech = ctx['st'], ctx['db'], ctx['ps'], ctx['tech']
    assert not differences([(ref(r, 1), ps[ref(r, 1)], ref(r, 2)) for r in range(747, 787) if ref(r, 1) in ps])
    paths = power_data.power_paths(db, ISO, st.years, ps, tech, ctx['gdppc'], c)
    assert not differences([(f'{ref(r, 3)}.{y}', paths[ref(r, 3)][y], ref(r, 7 + k)) for r in range(810, 877)
                            for k, y in enumerate(st.years)])
    par = power_data.power_params(db, ISO, st, ps, tech, c)
    assert not differences([(ref(r, 3), par[ref(r, 3)], ref(r, 4)) for r in range(884, 929)])
    co2 = ef_data.co2_efs(db, ISO, c)
    raw = float(policies.stored_baseline(policies.settings_stored_path(st), (ISO,), tuple(st.years))['raw']
                .sel(country=ISO, year=st.base_year))
    nc = ef_data.nonco2_efs(db, ISO, c)
    ecp = policies.ecp_table(db, ISO, ctx['cpi'])
    types = power_data.power_types(tech, ps, par, co2, ef_data.co2_calibration(db, ISO, st, raw), ecp,
                                   policies.ecp_embedded_year(st), nc, st.base, c)
    names = ['cax0', 'life', 'eff', 'cf', 'wacc', 'dtc', 'tcx', 'opf', 'vop', 'ffix', 'rns', 'price_code', 'vre',
             'vre_share', 'dlf', 'acap', 'afix', 'lcap', 'lfix', 'vfix', 'k', 'ppos', 'ef', 'efk', 'fpos', 'pfpos', 'gj',
             'kpu', 'cap0', 'gen0', 'rr', 'permitted', 'start', 'scaleup', 'dispatch', 'planned', 'puse', 'cg', 'eflag',
             'ninv', 'shr0', 'pef', 'co2f', 'tb', 'ecpk', 'xcp0', 'fflag', 'cfa', 'cfs', 'vreb', 'nua', 'nus', 'wcty',
             'wtec', 'wstu', 'rinv', 'afx', 'dtx', 'opfx', 'pfl', 'pefx', 'hydf', 'gasf', 'tpos', 'nvf', 'renf', 'inp0',
             'out0'] + [f'ap{k}_{p}' for p in power_data.POLLUTANTS for k in (0, 1)]
    assert not differences([(f'{f}.{k}', types[f][k], ref(207 + i, 3 + j)) for i, f in enumerate(types)
                            for j, k in enumerate(names)])
    sp = power_data.system_params(par, types, c)
    assert not differences([(k, sp[k], ref(r, 2)) for r, k in ((261, 'req_factor'), (262, 'cf_coal'), (263, 'gint'))])


def test_elasticities_and_efs(ctx):
    ela = elasticity_data.elasticities(ctx['db'], ISO, ctx['st'].base)
    assert not differences([(ref(r, 1), ela[ref(r, 1)], ref(r, 13)) for r in range(330, 460) if ref(r, 1) in ela])
    co2 = ef_data.co2_efs(ctx['db'], ISO, c)
    assert not differences([(ref(r, 1), co2[ref(r, 1)], ref(r, 11)) for r in range(276, 313)])
    nc = ef_data.nonco2_efs(ctx['db'], ISO, c)
    assert not differences([(ref(r, 1), nc[ref(r, 1)][k], ref(r, 9 + k)) for r in range(936, 1472) if ref(r, 1) in nc
                            for k in (0, 1)])
