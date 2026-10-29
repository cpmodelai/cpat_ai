# Quick check, CPAT-AI-Mitigation-Prototype v8.5

**PASS** (134 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 56 tabs): OK
- 442835 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 787 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 19 section bands with one blank row before and one after: exceptions []: OK
- 188 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (43); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (203324 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 188 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 726 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D40:W49,ScenarioCompare.D57:W66,ScenarioCompare.D74:W83,ScenarioCompare.D91:W100,ScenarioCompare.E34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 142978 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 5.1e-13 ('pct_gini_rec.ove', 0); tef.ove deciles 1, 10: -1.232, -1.073; Gini change with recycling -1.563: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: empty in the quick build (no batch run): skipped
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v8.4.xlsm: 13396 shared, 1350 new, 0 gone; 3216 change (max abs diff 7.355e+07); largest: ['egy.mit.psd.all.nga.1', 'egy.mit.psd.all.nga.2', 'egy.mit.psd.all.bio.2', 'egy.mit.psd.all.bio.1', 'egy.mit.psd.all.coa.1', 'egy.mit.psd.all.coa.2', 'egy.mit.pav.spr.all.die.2', 'egy.mit.pav.sp.all.die.2']; other than bco2 (with max abs diff): [('egy.mit.psd.all.nga.1', 73552463.377365), ('egy.mit.psd.all.nga.2', 73552463.377365), ('egy.mit.psd.all.bio.2', 2116893.980159), ('egy.mit.psd.all.bio.1', 2116893.980159), ('egy.mit.psd.all.coa.1', 969080.633194), ('egy.mit.psd.all.coa.2', 969080.633194), ('egy.mit.pav.spr.all.die.2', 232301.862951), ('egy.mit.pav.sp.all.die.2', 214011.913272), ('egy.mit.pav.sp0.all.die.2', 190495.266354), ('egy.mit.pav.spr.all.gso.2', 182175.806492), ('egy.mit.pav.sp.all.gso.2', 174243.666345), ('egy.mit.pav.sp0.all.gso.2', 136891.735248), ('egy.mit.pav.spr.all.nga.2', 136071.844844), ('egy.mit.pav.sp.all.nga.2', 118378.835554), ('egy.mit.pav.sp0.all.nga.2', 85364.158662), ('egy.mit.ch4bs.dg.all.2', 63444.359998), ('egy.mit.ch4bs.dg.all.1', 63444.359998), ('egy.mit.ch4bs.chk.all.all.1', 59570.708118), ('egy.mit.pav.spr.all.lpg.2', 58509.419854), ('egy.mit.pav.sp.all.lpg.2', 52453.480887), ('egy.mit.pav.spr.tot.tot.2', 49803.740131), ('egy.mit.pav.sp.tot.tot.2', 46217.173521), ('egy.mit.pav.sp0.all.lpg.2', 43992.569572), ('egy.mit.pav.sp0.tot.tot.2', 34191.226295), ('egy.mit.pav.spr.all.oop.2', 31047.094345), ('egy.mit.pav.sp.all.oop.2', 26717.509087), ('egy.mit.pav.q.tot.ecy.1', 23589.127735), ('egy.mit.pav.spr.all.coa.2', 23386.756763), ('egy.mit.pav.q.tot.ecy.2', 22947.374202), ('egy.mit.pav.sp0.all.bio.2', 22129.373888), ('egy.mit.pav.spr.all.bio.2', 22129.373888), ('egy.mit.pav.sp.all.bio.2', 22129.373888), ('egy.mit.pav.sp0.all.oop.2', 20603.196303), ('egy.mit.pav.sp.all.coa.2', 20124.812044), ('egy.mit.pav.sp0.all.coa.2', 18950.888127), ('egy.mit.rpol.all.exi.1', 13127.184862), ('egy.mit.fis.rev.all.all.1', 12891.945343), ('egy.mit.rtot.ref.all.all.2', 12891.945343), ('egy.mit.rtot.ref.all.all.1', 12891.945343), ('egy.mit.fis.ref.all.all.1', 12891.945343)]
