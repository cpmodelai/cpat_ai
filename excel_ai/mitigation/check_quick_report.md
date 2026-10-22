# Quick check, CPAT-AI-Mitigation-Prototype v8.0

**PASS** (192 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 55 tabs): OK
- 399839 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 767 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 17 section bands with one blank row before and one after: exceptions []: OK
- 143 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (39); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (184734 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 143 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 685 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D41:W41,ScenarioCompare.D46:W49,ScenarioCompare.D58:W58,ScenarioCompare.D63:W66,ScenarioCompare.D75:W75,ScenarioCompare.D80:W83,ScenarioCompare.D92:W92,ScenarioCompare.D97:W100,ScenarioCompare.E34,ScenarioCompare.J34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 128938 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 5.1e-13 ('pct_gini_rec.ove', 0); tef.ove deciles 1, 10: -1.159, -1.010; Gini change with recycling -1.543: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: rows by scenario ID {1: 123, 3: 123, 4: 123, 5: 123, 6: 123}; rows without values 0 []: OK
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v7_2.csv writes is decided): OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v7.2.xlsm: 13396 shared, 0 new, 0 gone; 0 change (max abs diff 0); largest: []; other than bco2 (with max abs diff): []
