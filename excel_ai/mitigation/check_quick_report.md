# Quick check, CPAT-AI-Mitigation-Prototype v0.9.2

**PASS** (127 s; the full check is check_full.py, run on request). Changes of output codes are reported, not failed: compare them with what the change intended.

- tab order (main, inputs, data, reference last; 58 tabs): OK
- 452164 formulas; plain formulas over 100 characters: []: OK
- numeric literals in formulas: {}: OK
- 824 defined names; names or LAMBDA parameters that read like cells: []: OK
- reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: []: OK
- sheets named by formulas and names exist: missing []: OK
- newer functions without the _xlfn. prefix: []: OK
- 19 section bands with one blank row before and one after: exceptions []: OK
- 195 sub-section headings with exactly one blank row before: exceptions []: OK
- rolled up: visible rows below the frozen rows are the bands and summary rows only (43); differences []: OK
- notes in column H not italic: exceptions []: OK
- section 0 numbered: A3 = '0': OK
- scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 (207680 cells; copy-paste left to right): differences []: OK
- no formula reads a later year except ['dsum', 'lvc', 'mani']: exceptions []: OK
- no parameter cell (D:G) reads a model year after the base year: exceptions []: OK
- ['lvc'] levelise inputs only (precedents reach no fuel use, GDP or power quantity row): exceptions []: OK
- 195 sub-section headings bold underlined in column B, nothing in H: exceptions []: OK
- 735 label rows bold with a thin bottom border: exceptions []: OK
- body font sizes on Mitigation (sample): [10.0]: OK
- tab title bars and sub-heading bars of equal width on every tab: exceptions []: OK
- table headers without the input fill: exceptions []: OK
- v0.6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']: OK
- recalculated in LibreOffice (LAMBDAs expanded): error values 0 [] (accepted: the chart data of empty ScenarioCompare slots, [('ScenarioCompare', 'ScenarioCompare.D41:W41,ScenarioCompare.D46:W49,ScenarioCompare.D58:W58,ScenarioCompare.D63:W66,ScenarioCompare.D75:W75,ScenarioCompare.D80:W83,ScenarioCompare.D92:W92,ScenarioCompare.D97:W100,ScenarioCompare.E34,ScenarioCompare.J34:M34')]): OK
- LAMBDA group 2 (the live scenario, LAMBDAs base year to 2041): 146278 numeric cells; tested against plain formulas by the output-code regression (last release) and the Distribution reference: OK
- Distribution group 2 vs the Python reference (distribution_ref, same inputs): 505 values, max relative difference 6.6e-13 ('pct_gini_rec.rur', 0); tef.ove deciles 1, 10: -1.761, -1.454; Gini change with recycling -1.821: OK
- Distribution scenario numbers equal Mitigation group by group (1-2): True: OK
- StoredOutputs: rows by scenario ID {1: 123, 3: 123, 4: 123, 5: 123, 6: 123}; rows without values 0 []: OK
- VBA module CPATScenarios.bas: identifiers not declared, not VBA, Excel or a known constant: none: OK
- code protocol C1 (lower case, digits, underscore, no empty token): 0 codes break it []: OK
- code protocol C7 (no model letter): 0 codes end in a model letter []: OK
- code protocol C10 (unique in a scenario group): 0 duplicates []: OK
- code protocol C5 (a total row writes tot): 0 explicit-sum rows write all [] (a row whose code the rename map code_renames_v0_7_2.csv writes is decided): OK
- Distribution reads Mitigation only through FromMitigation (section 19a): direct references 0 []: OK
- Excel open and recalculation: skipped (no Excel here: ModuleNotFoundError)
- output codes vs CPAT-AI-Mitigation-Prototype_v0.9.1.xlsm: 15082 shared, 4 new, 0 gone; 648 change (max abs diff 9.732e+04); largest: ['egy.mit.gdpn.all.lcu.1', 'egy.mit.gdpn.all.lcu.2', 'egy.mit.gdpn.all.usd.1', 'egy.mit.gdpn.all.usd.2', 'egy.mit.trtcfp.pass.phv.1', 'egy.mit.trtcfp.pass.phv.2', 'egy.mit.trdkmpaui.pau.ice.1', 'egy.mit.trdkmpaui.pau.ice.2']; other than bco2 (with max abs diff): [('egy.mit.gdpn.all.lcu.1', 97323.155099), ('egy.mit.gdpn.all.lcu.2', 97323.155099), ('egy.mit.gdpn.all.usd.1', 1664.942836), ('egy.mit.gdpn.all.usd.2', 1664.942836), ('egy.mit.trtcfp.pass.phv.1', 730.704826), ('egy.mit.trtcfp.pass.phv.2', 730.704826), ('egy.mit.trdkmpaui.pau.ice.1', 0.270861), ('egy.mit.trdkmpaui.pau.ice.2', 0.27052), ('egy.mit.trtofbn.fre.bev.1', 0.217168), ('egy.mit.trra.fre.bev.1', 0.20251), ('egy.mit.trtofbn.fre.bev.2', 0.199008), ('egy.mit.trsum.rod.tot.1', 0.192961), ('egy.mit.trra.fre.bev.2', 0.186619), ('egy.mit.trsum.rod.tot.2', 0.16801), ('egy.mit.trbusp.pass.die.1', 0.137367), ('egy.mit.tot.rod.die.1', 0.129985), ('egy.mit.trbusp.pass.die.2', 0.123226), ('egy.mit.tot.rod.gso.1', 0.119307), ('egy.mit.tot.rod.die.2', 0.116656), ('egy.mit.tot.rod.gso.2', 0.108153), ('egy.mit.trbusp.pass.gso.1', 0.097777), ('egy.mit.trbusp.pass.gso.2', 0.088637), ('egy.mit.tot.rod.ecy.1', 0.066861), ('egy.mit.tot.rod.ecy.2', 0.065698), ('egy.mit.trbuse.pass.ecy.1', 0.062591), ('egy.mit.trbuse.pass.ecy.2', 0.061502), ('egy.mit.trvku.pau.all.1', 0.045323), ('egy.mit.trvku.pau.all.2', 0.04524), ('egy.mit.trvkc.pass.phv.1', 0.032865), ('egy.mit.trtopiu.pau.ice.2', 0.029096), ('egy.mit.trvkc.pass.phv.2', 0.028762), ('egy.mit.trtopiu.pau.ice.1', 0.02527), ('egy.mit.trtopbn.pass.bev.1', 0.024371), ('egy.mit.trra.pass.bev.1', 0.023947), ('egy.mit.trfufbn.fre.bev.1', 0.023257), ('egy.mit.trtopbn.pass.bev.2', 0.022361), ('egy.mit.trra.pass.bev.2', 0.022068), ('egy.mit.trfufbn.fre.bev.2', 0.021795), ('egy.mit.trimpiu.pau.ice.1', 0.019214), ('egy.mit.trimpiu.pau.ice.2', 0.01919)]
