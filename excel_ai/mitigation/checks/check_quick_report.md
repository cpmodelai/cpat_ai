# Quick check, CPAT-AI-Mitigation-Prototype v1.1.0

**PASS** (393 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 58 tabs): OK
- 497541 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 825 defined names; names or LAMBDA parameters that read like cells: []: OK
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
- v0.6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D41:W41,ScenarioCompare.D46:W49,ScenarioCompare.D58:W58,ScenarioCompare.D63:W66,ScenarioCompare.D75:W75,ScenarioCompare.D80:W83,ScenarioCompare.D92:W92,ScenarioCompare.D97:W100,ScenarioCompare.E34,ScenarioCompare.J34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 146278 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 6.7e-13 ('pct_gini_rec.rur', 0); tef.ove deciles 1, 10: -1.666, -1.489; Gini change with recycling -1.929: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: rows by scenario ID {1: 708, 3: 708, 4: 708, 5: 708, 6: 708}; rows without values 0 []: OK
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v0_7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v1.0.4.xlsm: 15100 shared, 0 new, 0 gone; 4408 change (max abs diff 2.314e+07); largest: ['egy.mit.psd.all.nga.1', 'egy.mit.psd.all.nga.2', 'egy.mit.psd.all.bio.2', 'egy.mit.psd.all.bio.1', 'egy.mit.trtofbn.fre.bev.2', 'egy.mit.trtofbn.fre.bev.1', 'egy.mit.trra.fre.bev.2', 'egy.mit.trra.fre.bev.1']; other than bco2 (with max abs diff): [('egy.mit.psd.all.nga.1', 23141291.645905), ('egy.mit.psd.all.nga.2', 23141291.645905), ('egy.mit.psd.all.bio.2', 1449693.246574), ('egy.mit.psd.all.bio.1', 1449693.246574), ('egy.mit.trtofbn.fre.bev.2', 134138.360553), ('egy.mit.trtofbn.fre.bev.1', 134138.360553), ('egy.mit.trra.fre.bev.2', 133667.891851), ('egy.mit.trra.fre.bev.1', 133667.891851), ('egy.mit.psd.all.coa.1', 19819.61412), ('egy.mit.psd.all.coa.2', 19819.61412), ('egy.mit.pav.sp.all.nga.2', 9476.215546), ('egy.mit.pav.q.tot.ecy.1', 9458.190559), ('egy.mit.pav.sp.all.nga.1', 9415.795185), ('egy.mit.pav.spr.all.nga.1', 9415.795185), ('egy.mit.pav.spr.all.nga.2', 9158.997525), ('egy.mit.con.res.ecy.1', 8339.12436), ('egy.mit.pav.q.tot.ecy.2', 7962.8857), ('egy.mit.trtopbn.pass.bev.2', 7331.749648), ('egy.mit.trra.pass.bev.2', 7328.978458), ('egy.mit.trtopbn.pass.bev.1', 7284.544437), ('egy.mit.trra.pass.bev.1', 7281.933), ('egy.mit.con.res.ecy.2', 7113.127038), ('egy.mit.cons.ind.ecy.1', 5731.642218), ('egy.mit.pav.spr.all.gso.2', 5614.447463), ('egy.mit.pav.sp.all.gso.2', 5614.447463), ('egy.mit.pav.sp.all.gso.1', 5614.447463), ('egy.mit.pav.sp0.all.gso.2', 5614.447463), ('egy.mit.pav.spr.all.gso.1', 5614.447463), ('egy.mit.pav.sp0.all.gso.1', 5614.447463), ('egy.mit.pav.sp0.all.nga.1', 5411.583633), ('egy.mit.pav.sp0.all.nga.2', 5411.583633), ('egy.mit.pav.spr.all.lpg.1', 5366.253704), ('egy.mit.pav.sp0.all.lpg.1', 5366.253704), ('egy.mit.pav.spr.all.lpg.2', 5366.253704), ('egy.mit.pav.sp.all.lpg.1', 5366.253704), ('egy.mit.pav.sp.all.lpg.2', 5366.253704), ('egy.mit.pav.sp0.all.lpg.2', 5366.253704), ('egy.mit.pav.spr.all.die.2', 5180.843523), ('egy.mit.ener.ref.all.all.2', 4669.980972), ('egy.mit.ener.tot.tot.1', 4669.980972)]
