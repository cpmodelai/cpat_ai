# Linked data tables - CPAT-AI-Mitigation-Prototype v1.1.0

Links: 9 (Balances <- L_Balances (country), EnergyCons <- L_EnergyCons (country), Prices_dom <- L_Prices_dom (country), HHSurvey <- L_HHSurvey (country), IO_GTAP <- L_IO_GTAP (country), HH_Elast <- L_HH_Elast (country), WEO <- L_WEO (all), GDPRatios <- L_GDPRatios (all), UNPop <- L_UNPop (all))

## A. Identity: a data workbook made from the prototype tabs (columns reversed, extra column, other rows)
- Balances: 37 rows written, every cell as shipped OK
- EnergyCons: 19 rows written, every cell as shipped OK
- Prices_dom: 6 rows written, every cell as shipped OK
- HHSurvey: 132 rows written, every cell as shipped OK
- IO_GTAP: 11 rows written, every cell as shipped OK
- HH_Elast: 2398 rows written, every cell as shipped OK
- WEO: 3324 rows written, every cell as shipped OK
- GDPRatios: 798 rows written, every cell as shipped OK
- UNPop: 237 rows written, every cell as shipped OK

## B. Dummy data workbook: ../../data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx
- Balances: 37 rows of EGY; prototype columns not in the table: none OK
- EnergyCons: 19 rows of EGY; prototype columns not in the table: none OK
- Prices_dom: 6 rows of EGY; prototype columns not in the table: none OK
- HHSurvey: 132 rows of EGY; prototype columns not in the table: none OK
- IO_GTAP: 11 rows of EGY; prototype columns not in the table: none OK
- HH_Elast: 11 rows of EGY; prototype columns not in the table: none OK
- WEO: 3324 rows of EGY; prototype columns not in the table: none OK
- GDPRatios: 798 rows of EGY; prototype columns not in the table: none OK
- UNPop: 237 rows of EGY; prototype columns not in the table: none OK
- data sanity: negative retail prices (mit.rp.*) of EGY in L_Prices_dom: 0 [] OK
- all 9 links updated, recalculated in LibreOffice: new error values in group 1 (2022-2040) and MTOutputs block 1: 0 []
- the 9 links  updated, recalculated in LibreOffice: new error values in group 1 (2022-2040) and MTOutputs block 1: 0 [] OK
- key results of the baseline (MTOutputs block 1, 2030), shipped Egypt data -> dummy data:
  - mit.rpct.all.tot: -0.0645073757475904 -> -0.0645073757475904
  - mit.ghg.tot.tot: 535.275047672275 -> 535.275047672275
  - mit.co2.tot.tot: 294.159359221644 -> 294.159359221644
  - mit.wel.pct.tot: 0 -> 0
  - mit.co2.tot.tot: 294.159359221644 -> 294.159359221644
  - mit.gdp.eff.tot.tot: 0 -> 0

**Overall: PASS**
