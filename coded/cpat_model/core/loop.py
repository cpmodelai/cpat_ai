"""The run: the baseline first, then each policy scenario in turn (D15); each in three stages (D1).

    prepare   everything that depends on no model quantity, for all years at once
    year loop for t = base year ... last year, every block of mitigation/chain.py in order (the base year sets the
              starting values)
    finish    all-year results
Spec section 4.2. The blocks are added in phase 3. Then distribution: every scenario against the baseline in the
analysis year (distribution/incidence.py), where the scenario set has the distribution inputs.
"""
from cpat_model.data import open_database
from cpat_model.distribution import incidence
from cpat_model.mitigation import chain
from cpat_model.results import Results


def run_scenarios(scenarios, settings):
    settings = settings.with_globals(scenarios.global_settings(), scenarios.inputs(1))
    db = open_database(settings)
    results = Results(settings)
    baseline = None
    for number in scenarios.numbers():                    # 1 = baseline, first
        state = run_one(db, scenarios.inputs(number), settings, baseline)
        results.add(number, state)
        if number == 1:
            baseline = state
    if 'YearDistn' in scenarios.inputs(1).values:
        results.distribution = incidence.run(results, db, settings, scenarios)
    return results


def run_one(db, inputs, settings, baseline):
    """One scenario: prepare, year loop, finish. `state` holds the labelled arrays by code."""
    state = {}
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
