"""Command line: run a scenario-set file and write the results (plan task 6.1; spec section 3.2).

    python run_model.py                                    the Excel-AI scenario set, Egypt, results to outputs/
    python run_model.py my_scenarios.csv --countries EGY --scenarios 1 2 --out outputs/run1 --xlsx

The scenario set is a CSV of inputs by NameOfParameter, one column per scenario, scenario 1 (the baseline) first
(`../data/inputs/scenarios_excel_ai.csv` is the example; cpat_model/inputs). The run is `cpat_model.run`, as the Shiny
app's. Written per country: `mitigation_<ISO>.csv` (one row per output code: code, variable, sector, fuel,
description, unit, then the years) and `distribution_<ISO>.csv` (one row per code, basket and deciles 1-10).
"""
import argparse
import time
from pathlib import Path

import pandas as pd

import cpat_model
from cpat_model.core.variables import PATH as VARIABLES_CSV
from cpat_model.inputs import read_scenario_set
from cpat_model.inputs.scenarios import DEFAULT, ScenarioSet
from cpat_model.settings import Settings

OUT = Path(__file__).resolve().parent / 'outputs'


def main(argv=None):
    a = parse(argv)
    scenarios = read_scenario_set(a.scenario_set)
    if a.scenarios:
        cols = [str(n) for n in a.scenarios]
        if cols[0] != '1':
            cols = ['1'] + [c for c in cols if c != '1']             # the baseline always runs first
        scenarios = ScenarioSet(scenarios.rows, cols)
    settings = Settings(database=a.database, countries=tuple(a.countries or countries_of(scenarios)))
    t0 = time.perf_counter()
    results = cpat_model.run(scenarios, settings)
    print(f'ran scenarios {", ".join(scenarios.cols)} for {", ".join(settings.countries)} '
          f'in {time.perf_counter() - t0:.1f} s')
    for path in write(results, settings.countries, Path(a.out), a.xlsx):
        print(f'wrote {path}')
    return results


def parse(argv):
    p = argparse.ArgumentParser(description='Run a Coded CPAT scenario set and write the results.')
    p.add_argument('scenario_set', nargs='?', default=str(DEFAULT), help='scenario-set CSV (default: Excel-AI set)')
    p.add_argument('--countries', nargs='+', help='ISO3 codes (default: the set\'s _Countries row, else EGY)')
    p.add_argument('--scenarios', nargs='+', type=int, help='scenario numbers to run (scenario 1 is always run)')
    p.add_argument('--database', default='dummy', choices=['dummy', 'full'], help='database (NORMS 5.1)')
    p.add_argument('--out', default=str(OUT), help='output folder (default: coded/outputs)')
    p.add_argument('--xlsx', action='store_true', help='also one workbook with a sheet per country and module')
    return p.parse_args(argv)


def countries_of(scenarios):
    """The countries named in the set's _Countries row (scenario 1), or the default (Egypt) for 'all'."""
    names = scenarios.inputs(1).countries
    return Settings().countries if not names or names == ['all'] else [c.upper() for c in names]


def mitigation_table(results, iso):
    """The results by code with their variable, sector, fuel, description and unit (core/variables.csv)."""
    table = results.by_code(iso)
    table = table[sorted(table.columns)]                   # some rows carry years before 2022 or after 2041
    v = pd.read_csv(VARIABLES_CSV, keep_default_na=False)
    v['stem'] = v['code'].str.split('.', n=1).str[1].str.rsplit('.', n=1).str[0]
    info = v.drop_duplicates('stem').set_index('stem')[['variable', 'sector', 'fuel', 'description', 'unit']]
    stem = table.index.str.split('.', n=1).str[1].str.rsplit('.', n=1).str[0]
    meta = info.reindex(stem).set_axis(table.index)
    return pd.concat([meta, table], axis=1).rename_axis('code')


def write(results, countries, out, xlsx=False):
    out.mkdir(parents=True, exist_ok=True)
    written, sheets = [], {}
    for iso in countries:
        sheets[f'mitigation_{iso}'] = mitigation_table(results, iso)
        dist = results.distribution_by_code(iso)
        if len(dist):
            sheets[f'distribution_{iso}'] = dist.rename_axis('code')
    from cpat_model import __version__
    from cpat_model.settings import edition_info
    sheets['about'] = pd.DataFrame([{'model': f'Coded CPAT {__version__}', **edition_info(),
                                     'countries': ' '.join(countries)}]).set_index('model')   # which data made it
    for name, df in sheets.items():
        path = out / f'{name}.csv'
        df.to_csv(path)
        written.append(path)
    if xlsx:
        path = out / 'results.xlsx'
        with pd.ExcelWriter(path) as w:
            for name, df in sheets.items():
                df.to_excel(w, sheet_name=name[:31])
        written.append(path)
    return written


if __name__ == '__main__':
    main()
