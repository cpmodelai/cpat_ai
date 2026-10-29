# Quick check, CPAT-AI-Mitigation-Prototype v8.5

**PASS** (204 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 56 tabs): OK
- 408711 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 769 defined names; names or LAMBDA parameters that read like cells: []: OK
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
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D41:W41,ScenarioCompare.D46:W49,ScenarioCompare.D58:W58,ScenarioCompare.D63:W66,ScenarioCompare.D75:W75,ScenarioCompare.D80:W83,ScenarioCompare.D92:W92,ScenarioCompare.D97:W100,ScenarioCompare.E34,ScenarioCompare.J34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 129538 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 5.1e-13 ('pct_gini_rec.ove', 0); tef.ove deciles 1, 10: -1.159, -1.010; Gini change with recycling -1.543: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: rows by scenario ID {1: 123, 3: 123, 4: 123, 5: 123, 6: 123}; rows without values 0 []: OK
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v8.4.xlsm: 13396 shared, 0 new, 0 gone; 546 change (max abs diff 2.388e+05); largest: ['egy.mit.pav.spr.all.die.2', 'egy.mit.pav.sp.all.die.2', 'egy.mit.pav.sp0.all.die.2', 'egy.mit.pav.spr.all.gso.2', 'egy.mit.pav.sp.all.gso.2', 'egy.mit.pav.spr.all.nga.2', 'egy.mit.pav.sp0.all.gso.2', 'egy.mit.pav.sp.all.nga.2']; other than bco2 (with max abs diff): [('egy.mit.pav.spr.all.die.2', 238795.27303), ('egy.mit.pav.sp.all.die.2', 221528.799957), ('egy.mit.pav.sp0.all.die.2', 195981.940038), ('egy.mit.pav.spr.all.gso.2', 185495.885586), ('egy.mit.pav.sp.all.gso.2', 177913.341817), ('egy.mit.pav.spr.all.nga.2', 143538.175622), ('egy.mit.pav.sp0.all.gso.2', 139386.530781), ('egy.mit.pav.sp.all.nga.2', 125954.706753), ('egy.mit.pav.sp0.all.nga.2', 90023.786268), ('egy.mit.pav.spr.all.lpg.2', 61003.016848), ('egy.mit.pav.sp.all.lpg.2', 55055.194349), ('egy.mit.pav.spr.tot.tot.2', 52005.132479), ('egy.mit.pav.sp.tot.tot.2', 48481.821695), ('egy.mit.pav.sp0.all.lpg.2', 45701.96854), ('egy.mit.pav.sp0.tot.tot.2', 35648.347521), ('egy.mit.pav.spr.all.oop.2', 30915.746646), ('egy.mit.pav.sp.all.oop.2', 26859.562928), ('egy.mit.pav.spr.all.coa.2', 24386.726781), ('egy.mit.pav.spr.all.bio.2', 22861.021506), ('egy.mit.pav.sp.all.bio.2', 22861.021506), ('egy.mit.pav.sp0.all.bio.2', 22861.021506), ('egy.mit.pav.sp.all.coa.2', 21544.678934), ('egy.mit.pav.sp0.all.oop.2', 20523.691645), ('egy.mit.pav.sp0.all.coa.2', 19482.087026), ('egy.mit.pav.spr.all.jfu.2', 12265.484697), ('egy.mit.pav.sp.all.jfu.2', 11511.382007), ('egy.mit.pav.sp0.all.jfu.2', 8688.707476), ('egy.mit.aps.all.ch4.2', 2879.677863), ('egy.mit.em.foo.ch4.2', 2606.036761), ('egy.mit.aps.all.co.2', 2473.353952), ('egy.mit.em.tot.co.2', 2473.353952), ('egy.mit.em.tra.all.co.2', 1994.181059), ('egy.mit.em.rod.all.co.2', 1991.138203), ('egy.mit.em.rod.co.2', 1991.138203), ('egy.mit.aps.all.nox.2', 979.297001), ('egy.mit.em.tot.nox.2', 979.297001), ('egy.mit.em.tra.all.nox.2', 622.311351), ('egy.mit.em.rod.nox.2', 602.788756), ('egy.mit.em.rod.all.nox.2', 602.788756), ('egy.mit.ndc.bs.all.all.2', 544.232803)]
