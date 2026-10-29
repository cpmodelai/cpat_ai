"""The run: the baseline first, then each policy scenario in turn (D15); each in three stages (D1).

    prepare   everything that depends on no model quantity, for all years at once
    year loop for t = base year ... last year, every block of mitigation/chain.py in order (the base year sets the
              starting values)
    finish    all-year results
Spec section 4.2. The blocks are added in phase 3. Then distribution: every scenario against the baseline in the
analysis year (distribution/incidence.py), where the scenario set has the distribution inputs.
"""
from cpat_model.core.rows import State
from cpat_model.data import open_database
from cpat_model.distribution import incidence
from cpat_model.mitigation import chain
from cpat_model.results import Results


_BASELINES = {}                                           # baseline runs by their inputs and settings (phase 5.4)
_CACHES = {}                                              # data steps shared by the runs of one baseline (rows.cached)


def run_scenarios(scenarios, settings):
    settings = settings.with_globals(scenarios.global_settings(), scenarios.inputs(1))
    db = open_database(settings)
    results = Results(settings)
    baseline = None
    for number in scenarios.numbers():                    # 1 = baseline, first
        if number == 1:
            key = baseline_key(scenarios.inputs(1), settings)
            if key not in _BASELINES:
                if len(_BASELINES) >= 4:
                    old = next(iter(_BASELINES))
                    _BASELINES.pop(old), _CACHES.pop(old, None)
                _CACHES[key] = {}
                _BASELINES[key] = run_one(db, scenarios.inputs(1), settings, None, _CACHES[key])
            state = baseline = _BASELINES[key]
        else:
            state = run_one(db, scenarios.inputs(number), settings, baseline, _CACHES[key])
        results.add(number, state)
    if 'YearDistn' in scenarios.inputs(1).values:
        results.distribution = incidence.run(results, db, settings, scenarios)
    return results


def run_one(db, inputs, settings, baseline, cache=None):
    """One scenario: prepare, year loop, finish. `state` holds the labelled arrays by code; `cache` the data steps
    shared with the other scenarios of the baseline."""
    state = State()
    state['_cache'] = cache if cache is not None else {}
    for block in chain.PREPARE:
        block(state, db, inputs, settings, baseline)
    for t in settings.years:
        for block in chain.YEAR:
            block(state, db, inputs, settings, baseline, t)
    for block in chain.FINISH:
        block(state, db, inputs, settings, baseline)
    if '_year' in state:                                  # the rows filled year by year, to the state
        state.pop('_year').finish()
    return state


def baseline_key(inputs, settings):
    """What a baseline run depends on: its inputs, the database folder and the run settings. A run with the same key
    reuses the baseline state (the database is read once per folder: a changed file needs a new session)."""
    return (tuple(sorted(inputs.values.items())), str(settings.tidy_path()), tuple(settings.countries),
            settings.base_year, settings.last_year, settings.last_hist_price_year, settings.results_year,
            tuple(sorted((k, str(v)) for k, v in settings.global_settings.items())))

