# Check of CPAT-AI-Distribution v1.2.1
Module `CPAT-AI-Distribution_v1.2.1.xlsx`; full build of the mitigation builder v1.2.1 (baseline CO2 of `CPAT-AI-Mitigation_latest.xlsx`).

- tabs: Cover, Scenarios, FromMaster, FromMitigation, Distribution, Constants, Mappings, DATA_DISTN->>, DistMapping, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios, WEO OK
- Distribution: 25190 cells, values equal to the prototype's: 0 differ [] OK
- FromMitigation = ExportDistn (Mitigation!$A$9430:$BB$9459, 30 rows) through the macro's row mapping: 0 differ [] OK
- FromMitigation holds values only: 0 formulas OK
- kept tabs (but Cover, Constants and Mappings, FromMitigation, FromMaster): formulas as the prototype's: 0 differ [] OK
- formulas reading a dropped tab: 0 [] OK
- names read by formulas and not defined: none OK
- no VBA project (macros in the Master workbook): OK
- end to end (live carbon price 60 USD/t on rows [19, 20] of Scenarios): module updated from the recalculated prototype = the prototype's Distribution: 0 differ []; 4686 values moved from the shipped ones OK
- lint: no problem OK

**Result: PASS**
