# Quick check, CPAT-AI-Mitigation v1.2.2

**PASS** (144 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (Documentation, main, inputs, modules, data; 44 tabs): OK
- 370120 formulas; plain formulas over 115 characters (hard limit): []; over the target 90 (reported, not failed): 18765: OK
- numeric literals in formulas: {}: OK
- 780 defined names; names or LAMBDA parameters that read like cells: []: OK
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
- 1.2.2: front tabs ['Documentation', 'Cover', 'Scenarios', 'Mitigation', 'Outputs'] (no dividers), the four after Documentation one colour {'Cover': '00AE49', 'Scenarios': '00AE49', 'Mitigation': '00AE49', 'Outputs': '00AE49'}; opens on Cover: OK
- 1.2.2: no ScenarioCompare, no REF, DATA_OUTPUT or DATA_OTHER divider, no HHSurvey or WHOCooking (Mitigation): OK
- 1.2.2: Documentation columns 35 wide {35.0}: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 []: OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 146278 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution: not in the mitigation workbook (checked by distribution/check_distribution.py): OK
- Outputs equals Mitigation in its 2 scenario groups (32214 cells): differences 0 []: OK
- stored scenarios (stored_scenarios.csv): rows by scenario ID {'1': 708, '3': 708, '4': 708, '5': 708, '6': 708}; rows without values 0 []: OK
- VBA module CPATMaster.bas (the Master workbook): identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v0_7_2.csv writes is decided): OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation_v1.2.1.xlsx: 15100 shared, 0 new, 0 gone; 0 change (max abs diff 0); largest: []; other than bco2 (with max abs diff): []
