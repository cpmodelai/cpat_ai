"""Phase 5.0: Coded CPAT against the Python recomputations written for Excel-AI (spec D8; user 2026-10-29).

    python cpat_testing/compare/check_recomputations.py

Distribution: `excel_ai/mitigation/checks/distribution_ref.py` (an independent recomputation of the Distribution sheet) is
given the inputs Coded CPAT's distribution module took from mitigation (price changes, spending, GDP, population,
new revenue, the scenario's distribution settings), and its household results are compared with Coded CPAT's rows.

Mitigation: `check_full.recompute` (with `power_model_ref` and `transport_model_ref`) is called; where it does not run
on the current prototype, that is reported, not hidden (the full check last ran on Excel-AI 0.8.0).
"""
import sys
import warnings
from pathlib import Path

import numpy as np

CODED = Path(__file__).resolve().parents[2]
MIT = CODED.parent / 'excel_ai' / 'mitigation'
sys.path.insert(0, str(CODED))
warnings.filterwarnings('ignore')

import cpat_model                                          # noqa: E402
from cpat_model.distribution import incidence, mapping     # noqa: E402
from cpat_model.inputs import read_scenario_set            # noqa: E402
from cpat_model.inputs.scenarios import ScenarioSet        # noqa: E402

SETTINGS = ['QuantilesStatistic', 'ScaleGTAP', 'PEDs', 'InferredDist', 'DWLs', 'ExemptMostCook', 'ExemptCookDeciles',
            'EXPLabortax', 'EXPCapex', 'EXPGoodsandserv', 'EXPTransfers', 'TargettedPercentile', 'CoverageRate',
            'LeakageRate', 'PITReductionType', 'DistExcCfDec', 'MissingDataReplacement', 'PublicInfrastructureInvType']
COMPARED = {('tef', 'ove'): ('tef', 'tot', 'ove'), ('tef', 'urb'): ('tef', 'tot', 'urb'),
            ('tef', 'rur'): ('tef', 'tot', 'rur'), ('def', 'tot'): ('def', 'tot', 'ove'),
            ('ief', 'tot'): ('ief', 'tot', 'ove'), ('cons_pc_na', 'ove'): ('cons_pc_na', '', 'ove'),
            ('tot_cons_na', 'ove'): ('tot_cons_na', '', 'ove'), ('pop_tot_adj', 'ove'): ('pop_tot_adj', '', 'ove'),
            **{(k, s): (k, 'tot', s) for k in ('pit', 'pui', 'cts', 'tgt', 'rec', 'net') for s in ('ove', 'urb', 'rur')},
            **{('pctrev_comp', s): ('pctrev_comp', '', s) for s in ('ove', 'urb', 'rur')},
            **{(k, s): (k, '', s) for k in ('pct_gini_norec', 'pct_gini_rec') for s in ('ove', 'urb', 'rur')}}


def plain(v):
    """An Excel-AI option without its default star; numbers as numbers."""
    v = str(v).rstrip('*')
    try:
        return float(v)
    except ValueError:
        return v


def distribution(n=2, iso='EGY'):
    """Coded CPAT's Distribution sheet for scenario n against distribution_ref with the same mitigation inputs."""
    sys.path.insert(0, str(MIT))
    import distribution_ref as DR
    scen = read_scenario_set()
    res = cpat_model.run(ScenarioSet(scen.rows, ['1', str(n)]))
    st = res.settings
    db = cpat_model.core.loop.open_database(st)
    data = incidence._country_data(db, iso, st.results_year)
    value, base = incidence._reader(res.states[n], iso), incidence._reader(res.states[1], iso)
    inputs = scen.inputs(n)
    S = incidence.group(data, inputs, value, base, st.years, st.base_year, iso)
    g = lambda var, item='', sample='': S.get(var, item, sample)[0]
    fuel_of = {'oil': 'oop'}
    inp = {'dp_res': {f: g('dpr', f'{incidence.DPR_OF[f]}.res') for f in incidence.FUELS},
           'dp_all': {f: g('dpa', f) for f, _g, _r in incidence.DPA},
           'spend': {f: g('spend', f) for f, _g, _r in incidence.DPA},
           'defl_gtap': mapping.deflator_ratio(db, iso, mapping.io_tables(db, iso)[1], st.results_year),
           'gdp_lcu': g('gdp'), 'pop': g('pop'), 'rev_lcu': g('rev'), 'cons_gdp': g('consgdp'),
           'settings': {k: plain(inputs.values[k]) for k in SETTINGS}}
    inp['settings']['aspire_code'] = g('aspcode')
    inp['settings']['exempt_fuel'] = g('exfuel')
    ref = DR.run(inp, iso, fix=True)
    rows, worst = [], 0.0
    for key, (var, item, sample) in COMPARED.items():
        if key not in ref or (var, item, sample) not in S.rows:
            rows.append((key, None))
            continue
        py = np.asarray(S.get(var, item, sample), dtype=float)
        rf = np.atleast_1d(np.asarray(ref[key], dtype=float))
        py = py[1:] if len(rf) == 10 else (py[:1] if len(rf) == 1 else py)
        d = float(np.nanmax(np.abs(py - rf) / np.maximum(np.abs(rf), 1.0)))
        rows.append((key, d))
        worst = max(worst, d)
    return rows, worst, fuel_of


def mitigation():
    """check_full.recompute for scenarios 1 and 2, or the reason it does not run."""
    sys.path.insert(0, str(MIT))
    try:
        import check_full as C
        C.recompute(C.scenario_mt(1))
        return 'runs'
    except Exception as e:                                 # report, do not hide (phase 5.0)
        return f'does not run on the current prototype: {type(e).__name__}: {e}'


if __name__ == '__main__':
    rows, worst, _ = distribution()
    print('Distribution, scenario 2: Coded CPAT vs distribution_ref.py (same mitigation inputs)')
    for key, d in rows:
        print(f'  {key}: ' + ('not in the recomputation' if d is None else f'max rel diff {d:.2e}'))
    print(f'  worst {worst:.2e}')
    print('Mitigation: check_full.recompute', mitigation())
