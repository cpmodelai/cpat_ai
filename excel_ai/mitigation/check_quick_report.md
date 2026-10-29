# Quick check, CPAT-AI-Mitigation-Prototype v8.5

**FAIL** (122 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 56 tabs): OK
- 408735 formulas; plain formulas over 100 characters: ['Mitigation!L98', 'Mitigation!M98', 'Mitigation!N98', 'Mitigation!O98', 'Mitigation!P98']: FAIL
- numeric literals in formulas: {}: OK
- 770 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 18 section bands with one blank row before and one after: exceptions []: OK
- 144 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (41); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (185482 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 144 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 685 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D40:W49,ScenarioCompare.D57:W66,ScenarioCompare.D74:W83,ScenarioCompare.D91:W100,ScenarioCompare.E34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 129538 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 5.4e-13 ('pct_gini_rec.rur', 0); tef.ove deciles 1, 10: -1.235, -1.076; Gini change with recycling -1.649: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: empty in the quick build (no batch run): skipped
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v8.4.xlsm: 13396 shared, 0 new, 0 gone; 2431 change (max abs diff 2.41e+05); largest: ['egy.mit.pav.spr.all.die.2', 'egy.mit.pav.sp.all.die.2', 'egy.mit.pav.sp0.all.die.2', 'egy.mit.pav.spr.all.gso.2', 'egy.mit.pav.sp.all.gso.2', 'egy.mit.pav.spr.all.nga.2', 'egy.mit.pav.sp0.all.gso.2', 'egy.mit.pav.sp.all.nga.2']; other than bco2 (with max abs diff): [('egy.mit.pav.spr.all.die.2', 240973.421406), ('egy.mit.pav.sp.all.die.2', 221863.259427), ('egy.mit.pav.sp0.all.die.2', 197559.121413), ('egy.mit.pav.spr.all.gso.2', 186431.870561), ('egy.mit.pav.sp.all.gso.2', 178343.911201), ('egy.mit.pav.spr.all.nga.2', 145323.24725), ('egy.mit.pav.sp0.all.gso.2', 140089.854729), ('egy.mit.pav.sp.all.nga.2', 126455.311241), ('egy.mit.pav.sp0.all.nga.2', 91151.393384), ('egy.mit.ch4bs.chk.all.all.1', 64727.696995), ('egy.mit.ch4bs.dg.all.2', 63444.359998), ('egy.mit.ch4bs.dg.all.1', 63444.359998), ('egy.mit.pav.spr.all.lpg.2', 61730.633198), ('egy.mit.pav.sp.all.lpg.2', 55341.576603), ('egy.mit.pav.spr.tot.tot.2', 52419.545193), ('egy.mit.pav.sp.tot.tot.2', 48611.107952), ('egy.mit.pav.sp0.all.lpg.2', 46247.080917), ('egy.mit.pav.sp0.tot.tot.2', 35880.21932), ('egy.mit.pav.spr.all.oop.2', 31387.24393), ('egy.mit.pav.sp.all.oop.2', 27026.505588), ('egy.mit.pav.spr.all.coa.2', 24042.368382), ('egy.mit.pav.sp0.all.bio.2', 22861.021506), ('egy.mit.pav.sp.all.bio.2', 22861.021506), ('egy.mit.pav.spr.all.bio.2', 22861.021506), ('egy.mit.pav.sp0.all.oop.2', 20836.636476), ('egy.mit.pav.sp.all.coa.2', 20691.407732), ('egy.mit.pav.sp0.all.coa.2', 19482.087026), ('egy.mit.rtot.ref.all.all.2', 14902.221286), ('egy.mit.rpol.tot.tot.1', 14902.221286), ('egy.mit.fis.rev.all.all.1', 14902.221286), ('egy.mit.fis.ref.all.all.1', 14902.221286), ('egy.mit.rnet.all.all.1', 14902.221286), ('egy.mit.fis.ref.all.all.2', 14902.221286), ('egy.mit.rev.usd.tot.1', 14902.221286), ('egy.mit.rtot.ref.all.all.1', 14902.221286), ('egy.mit.rpol.all.exi.1', 14902.215596), ('egy.mit.rsub.tot.tot.1', 14279.108265), ('egy.mit.rpol.all.exi.2', 13792.446793), ('egy.mit.rnet.all.all.2', 13744.779114), ('egy.mit.fis.rev.all.all.2', 13370.371294)]
