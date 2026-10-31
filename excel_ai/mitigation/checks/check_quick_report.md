# Quick check, CPAT-AI-Mitigation v1.2.0

**PASS** (311 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 51 tabs): OK
- 369632 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 787 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 19 section bands with one blank row before and one after: exceptions []: OK
- 197 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (43); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (208098 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 197 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 743 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v1.2.0: front tabs Cover, ScenarioDefinition, then MAIN (Mitigation) and OUTPUT (MTOutputs, ScenarioCompare): ['Cover', 'ScenarioDefinition', 'MAIN->>', 'Mitigation', 'OUTPUT->>', 'MTOutputs', 'ScenarioCompare']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, []): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 146278 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution: not in the mitigation workbook (checked by distribution/check_distribution.py): OK
- MTOutputs equals Mitigation in its 2 scenario groups (32214 cells): differences 0 []: OK
- ScenarioCompare: slots with a scenario and a key result [0, 1] of the 2 groups: OK
- stored scenarios (stored_scenarios.csv): rows by scenario ID {'1': 708, '3': 708, '4': 708, '5': 708, '6': 708}; rows without values 0 []: OK
- VBA module CPATMaster.bas (the Master workbook): identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v0_7_2.csv writes is decided): OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v1.1.0.xlsm: 15100 shared, 0 new, 0 gone; 0 change (max abs diff 0); largest: []; other than bco2 (with max abs diff): []
