"""Engineer road transport model against legacy CPAT: bugs fixed and decisions taken (Methods, chapter Transport).

The bug list (FIXES) and the effect tables come from the Python reference (transport_model_ref.py), so the
document stays in step with the model. Decisions are listed below with who took them and when.

    python make_transport_doc.py
"""
import os

import transport_model_ref as T

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'Methods, chapter Transport')

RULE = ('Rule (user, 2026-10-14): match legacy CPAT except where legacy has a bug; every difference is listed here. '
        'Where a choice was needed, the recommendation in `Transport_Plan.md` section 3 or in the open questions of '
        'Methods, chapter Transport was taken ("Go with recommendations", "Go with suggestions", 2026-10-14).')

SCOPE = [  # topic, legacy, prototype
    ('Model choice', 'Switch `TrModel` (MTInputs F340, from the Dashboard): Engineer or Elasticity; the Egypt run uses '
     'Elasticity', 'Same switch, **default Elasticity**; the engineer model is computed in every run and replaces road '
     'gasoline, diesel, LPG and gas (and road electricity in power demand) when switched on'),
    ('Coverage', 'Road only: passenger and light (new and used), freight, 2-3 wheelers, buses (scaled); coal, kerosene '
     'and other oil products in road, rail, aviation and navigation by elasticities', 'Same'),
    ('Externalities', 'Sheet `Transport` (accidents, congestion, road damage) reads the engineer distance and fuel '
     'economy even under Elasticity', 'Not built (later); legacy bug B16 of the survey noted'),
    ('Mode shift', 'None', 'None'),
]

DECISIONS = [  # topic, legacy, prototype, reason
    ('Default model', 'Template default Engineer; Egypt run Elasticity', 'Elasticity by default, Engineer by switch',
     'Results unchanged until the engineer run is reviewed; a calibration that is not general stays off by default '
     '(user rule v0.3.4)'),
    ('Bugs', 'As found', 'All fixed (list below); legacy behaviour kept as switches in the Python reference only',
     'Same approach as the power model; the reference reproduces legacy to 4e-14 with the switches off'),
    ('Parameters', 'Side-table and Dashboard values; methodology note differs (discount rate 10-30%, distance income '
     'elasticity 0.05, driving elasticities -0.3/-0.2, wage-linked maintenance, ICEV prices rising with income)',
     'Legacy values; the note\'s values listed as alternatives (`data/transport_params.csv`, use = note)',
     'Match legacy; switch after review'),
    ('Range anxiety', 'Transport3: stored per-country solver results', 'The same stored values; the mismatch with the '
     'observed 2025 EV share is reported (legacy 0.35%, all fixes 0.09%, actual 0.15% for Egypt passenger)',
     'General (194 countries); re-solving for the corrected model needs a goal seek (later)'),
    ('Calibration to the energy balance', 'Step 1: distance factors by class; step 2: residual factor by fuel', 'Same, '
     'live formulas; the factors are reported (Egypt: passenger distance x2.67, then gasoline x1.23)',
     'General (from data); the large factors flag data problems'),
    ('Used vehicle depreciation (B20)', 'Used ICEV annuity over 6 years, used BEV over 12', '12 years for both '
     '(used ownership period - 1)', 'User confirmation 2026-10-14'),
    ('Ownership decline (B4)', 'Passenger and freight ownership cannot fall', 'May fall by up to 10% a year (the '
     'legacy 2-3 wheeler value)', 'Placeholder value; no effect for Egypt'),
    ('PHEV range anxiety (B23)', 'PHEV TCO carries the full BEV range anxiety (about 100,000 $)', 'None for PHEVs',
     'PHEVs refuel with gasoline; user decision 2026-10-14'),
    ('Freight distance (survey B14)', 'TCO uses Transport1 average freight distance (48,630 km, floored at 50,000 km, '
     'binding every year); fuel use uses the derived 8,091 km x calibration', 'Kept as legacy', 'Needs a data '
     'decision; not a clear bug'),
    ('Data years in inputs', 'VAT on vehicles and customs from 2024, import shares 2022, bus electricity 2024', 'Kept '
     'as legacy (parameters)', 'Legacy input choices, not bugs'),
    ('Policy inputs', 'Dashboard rows 61-98, 540-558 (outside MTInputs)', 'New MTInputs rows (scenario-specific, run '
     'by the batch macro)', 'Scenarios must carry the transport policies'),
    ('Hardcoded literals', 'Gompertz -5.897, gas /26, PHEV x9, insurance x0.5, station life /15, BEV distance caps, '
     'own and cross price elasticities, BEV fuel-economy and charging-cost paths', 'Named parameters and data '
     '(`transport_params.csv`, `transport_paths.csv`), same values', 'No literal in a formula (user rule)'),
]

KEPT = [  # survey item, why not a fix
    ('B5 large calibration factors', 'data issue, reported'),
    ('B11 lags (EV electricity price of the previous year; lagged feebate intensities; ICE mix from last year\'s '
     'ownership)', 'intended (legacy avoids a circular reference)'),
    ('B13 row 2171 change in ownership', 'unused row'),
    ('B15 unused inputs', 'no effect'),
    ('B16 externality sheet', 'out of scope'),
    ('B17 key-input layout (share / ktoe / liter in year columns)', 'layout only; the prototype uses its own layout'),
]


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return out


def main():
    base = [r for r in T.legacy_test('base', fix=frozenset())]
    pol = [r for r in T.legacy_test('pol', fix=frozenset())]
    worst = lambda res: max(r[0] for r in res) if res else 0.0
    lines = ['# Engineer road transport model against legacy CPAT: bugs and decisions (CPAT-AI-Mitigation-Prototype v0.4.7)', '',
             RULE, '',
             'Sources: legacy `CPAT 1.0pre_456_NoPropData.xlsb`, Mitigation key inputs 15 (rows 2015-2171), section 5 '
             '(rows 4302-5378; policy copy +6331), sheets Transport1-3, Dashboard, Manual inputs; methodology note '
             '`data/source/Transportation_methodology.docx`. Map of legacy: `Transport_Legacy_Survey.md`; equations '
             'and data: Methods, chapter Transport. Generated by `make_transport_doc.py` from '
             '`transport_model_ref.py`.', '',
             f'**Legacy match:** with every fix off, the Python reference reproduces the cached legacy engineer run '
             f'(both scenario blocks, 2022-2041, about 1,091 series each): max relative difference {worst(base):.1e} '
             f'(baseline) and {worst(pol):.1e} (carbon tax). The workbook is checked against this reference.', '',
             '## 1. Scope', '']
    lines += table(['Topic', 'Legacy', 'prototype'], SCOPE)
    lines += ['', '## 2. Decisions relative to legacy', '']
    lines += table(['Topic', 'Legacy', 'prototype', 'Reason'], DECISIONS)
    lines += ['', f'## 3. Legacy bugs fixed ({len(T.FIXES)})', '',
              'Each is a switch of the Python reference (`FIXES`); the prototype applies all of them. Ids follow the survey '
              '(B1-B17) and continue for the bugs found while building the reference (B19-B23).', '']
    order = sorted(T.FIXES, key=lambda k: (int(''.join(c for c in k[1:] if c.isdigit())), k))
    lines += table(['Id', 'Legacy rows', 'Bug and fix'], [(k, T.FIXES[k][0], T.FIXES[k][1]) for k in order])
    lines += ['', 'Survey items kept as legacy (not bugs, or not in scope):', '']
    lines += [f'- {a}: {b}.' for a, b in KEPT]
    for run, name in (('base', 'Baseline (scenario 1)'), ('pol', 'Carbon tax (scenario 2 of the legacy run)')):
        lines += ['', f'## 4{"a" if run == "base" else "b"}. Effects for Egypt: {name}', '',
                  'Levels with legacy behaviour and with all fixes; then the change from each fix alone (2030 / 2035 / '
                  '2041; % for fuel use and vehicles, percentage points for EV sales shares).', '',
                  T.effects_md(run)]
    lines += ['', '## 5. Reading', '',
              '- **B3 (two-sided ownership calibration) dominates:** Egypt\'s ownership was 55 per 1,000 in 2025 '
              'against a Gompertz level of 152, so the calibration factor is 0.36 instead of legacy\'s floor of 1; '
              'passenger ownership reaches 82 per 1,000 in 2041 instead of 173, and road fuel use is a third lower by '
              '2035.',
              '- **B20 is the largest choice-side fix:** legacy front-loads used ICEV depreciation, which raises used '
              'ICEV costs and the EV share; the fix lowers the passenger EV sales share by about 10 points in 2035.',
              '- Fixes with no effect for Egypt act through policies or fuels that are zero in both Egypt runs (distance '
              'tax, EV subsidies, charging subsidy, LPG and LNG trucks); they matter for other countries and scenarios.',
              '', '## 6. Open', '',
              '- Re-solve range anxiety for the corrected model (goal seek, as the ETS goal seek).',
              '- Freight distance (B14) and the data years of customs, VAT and import shares: data decisions.',
              '- The ownership decline limit of 10% a year is a placeholder.',
              '- Review the methodology-note parameters against the legacy values.', '']
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    inp = T.legacy_inputs('base')                       # deck: Egypt engineer baseline, legacy vs all fixes
    leg = T.summary(T.engine(inp, fix=frozenset()))
    fixed = T.summary(T.engine(inp, fix=T.ALL_FIXES))
    deck = {'years': [2030, 2035, 2041], 'nfix': len(T.FIXES),
            'road_legacy': [round(leg[y]['gso'] + leg[y]['die'] + leg[y]['lpg'] + leg[y]['nga']) for y in (2030, 2035, 2041)],
            'road_fixed': [round(fixed[y]['gso'] + fixed[y]['die'] + fixed[y]['lpg'] + fixed[y]['nga'])
                           for y in (2030, 2035, 2041)],
            'ev_legacy': [leg[y]['ev_pass'] for y in (2030, 2035, 2041)],
            'ev_fixed': [fixed[y]['ev_pass'] for y in (2030, 2035, 2041)]}
    import json
    with open(os.path.join(HERE, 'presentation', 'img', 'v0_4_0_transport.json'), 'w', encoding='utf-8') as f:
        json.dump(deck, f, indent=1)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
