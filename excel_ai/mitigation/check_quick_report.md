# Quick check, CPAT-AI-Mitigation-Prototype v9.0

**PASS** (192 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 58 tabs): OK
- 452077 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 823 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 19 section bands with one blank row before and one after: exceptions []: OK
- 194 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (43); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (207570 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 194 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 734 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D41:W41,ScenarioCompare.D46:W49,ScenarioCompare.D58:W58,ScenarioCompare.D63:W66,ScenarioCompare.D75:W75,ScenarioCompare.D80:W83,ScenarioCompare.D92:W92,ScenarioCompare.D97:W100,ScenarioCompare.E34,ScenarioCompare.J34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 146238 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 6.6e-13 ('pct_gini_rec.rur', 0); tef.ove deciles 1, 10: -1.761, -1.454; Gini change with recycling -1.821: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: rows by scenario ID {1: 123, 3: 123, 4: 123, 5: 123, 6: 123}; rows without values 0 []: OK
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v8.5.xlsm: 13076 shared, 2006 new, 320 gone; 3615 change (max abs diff 7.355e+07); largest: ['egy.mit.psd.all.nga.1', 'egy.mit.psd.all.nga.2', 'egy.mit.psd.all.bio.2', 'egy.mit.psd.all.bio.1', 'egy.mit.psd.all.coa.2', 'egy.mit.psd.all.coa.1', 'egy.mit.trtofbn.fre.bev.1', 'egy.mit.trtofbn.fre.bev.2']; other than bco2 (with max abs diff): [('egy.mit.psd.all.nga.1', 73552463.377365), ('egy.mit.psd.all.nga.2', 73552463.377365), ('egy.mit.psd.all.bio.2', 2116893.980159), ('egy.mit.psd.all.bio.1', 2116893.980159), ('egy.mit.psd.all.coa.2', 969080.633194), ('egy.mit.psd.all.coa.1', 969080.633194), ('egy.mit.trtofbn.fre.bev.1', 162443.795276), ('egy.mit.trtofbn.fre.bev.2', 162443.795276), ('egy.mit.trra.fre.bev.2', 162443.795276), ('egy.mit.trra.fre.bev.1', 162443.795276), ('egy.mit.pav.sp0.all.die.1', 73403.660778), ('egy.mit.pav.sp0.all.die.2', 73403.660778), ('egy.mit.pav.sp0.all.gso.1', 59107.67314), ('egy.mit.pav.sp0.all.gso.2', 59107.67314), ('egy.mit.rpol.tot.tot.1', 36618.016255), ('egy.mit.fis.ref.all.all.2', 36618.016255), ('egy.mit.rtot.ref.all.all.1', 36618.016255), ('egy.mit.fis.rev.all.all.1', 36618.016255), ('egy.mit.rnet.all.all.1', 36618.016255), ('egy.mit.rtot.ref.all.all.2', 36618.016255), ('egy.mit.fis.ref.all.all.1', 36618.016255), ('egy.mit.rev.usd.tot.1', 36618.016255), ('egy.mit.rsub.tot.tot.1', 35972.813417), ('egy.mit.pav.spr.all.gso.1', 35966.040767), ('egy.mit.pav.sp.all.gso.1', 35966.040767), ('egy.mit.pav.sp.all.die.1', 34826.778315), ('egy.mit.pav.spr.all.die.1', 34826.778315), ('egy.mit.pav.sp.all.gso.2', 33684.952218), ('egy.mit.pav.sp.all.die.2', 32992.84822), ('egy.mit.rnet.all.all.2', 32190.025584), ('egy.mit.rsub.tot.tot.2', 31622.972876), ('egy.mit.fis.rev.all.all.2', 31067.985757), ('egy.mit.rev.usd.tot.2', 31067.985757), ('egy.mit.rpol.tot.tot.2', 31067.985757), ('egy.mit.rpol.all.exi.1', 30400.574719), ('egy.mit.pav.spr.all.gso.2', 29802.759181), ('egy.mit.pav.spr.all.die.2', 26550.286221), ('egy.mit.rpol.all.exi.2', 26442.278713), ('egy.mit.cap.pow.tot.1', 22905.182349), ('egy.mit.trtofin.fre.ice.2', 21669.316061)]
