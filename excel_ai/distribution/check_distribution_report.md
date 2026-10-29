# Check of CPAT-AI-Distribution-Prototype v1.0.2
Module `CPAT-AI-Distribution-Prototype_v1.0.2.xlsm`; prototype `CPAT-AI-Mitigation-Prototype_latest.xlsm` v1.0.2.

- tabs: Cover, ScenarioDefinition, FromMitigation, Distribution, Settings, DATA_DISTN->>, DistMapping, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios, WEO OK
- Distribution: 25190 cells, values equal to the prototype's: 0 differ [] OK
- FromMitigation = ExportDistn (Mitigation!$A$9430:$BB$9459, 30 rows) through the macro's row mapping: 0 differ [] OK
- FromMitigation holds values only: 0 formulas OK
- kept tabs (but Cover, Settings, FromMitigation): formulas as the prototype's: 0 differ [] OK
- formulas reading a dropped tab: 0 [] OK
- names read by formulas and not defined: none OK
- VBA project: module CPATDistribution = CPATDistribution.bas (185 lines), document modules match the sheet code names: OK
VBA module CPATDistribution.bas: identifiers not declared, not VBA, Excel or a known constant: none OK
- public macros: UpdateFromMitigation, CalculationOn, CalculationOff, RecalculateNow, ToggleRecalculation; workbook names the macros read (MitLastUpdate, MitSource, MitUsed) defined: OK
- buttons on Cover call public macros: OK
- end to end (live carbon price 60 USD/t on rows [19, 20] of ScenarioDefinition): module updated from the recalculated prototype = the prototype's Distribution: 0 differ []; 4670 values moved from the shipped ones OK
- lint: no problem OK

**Result: PASS**
