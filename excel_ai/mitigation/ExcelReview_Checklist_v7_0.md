# Excel 365 review checklist (CPAT-AI-Mitigation-MVP v6.4; issue I1)

The workbook is built with openpyxl and checked in LibreOffice, which does not run LAMBDAs or VBA the way Excel does. This list is the review in Excel 365 on Windows. For each step, note OK or what you see (sheet, cell, message) in the last column, and send the list back. Do not save over the shipped file: work on a copy.

| # | Step | Expected | Result |
|---|---|---|---|
| 1 | Open a copy of `CPAT-AI-Mitigation-MVP-v6.4.xlsm` and enable macros. | Opens without a repair prompt. No external-link warning. | |
| 2 | Formulas > Calculate Now, then Ctrl+Alt+F9 (full recalculation). | No circular-reference warning; the status bar shows no "Circular References". | |
| 3 | Formulas > Name Manager: filter the names for errors. | No name shows #REF! or #NAME?. The LAMBDA names (FUELUSE, SUPPLYCOST, PRODSUBUNIT, ...) are listed. | |
| 4 | Sheet Mitigation, LAMBDA year 2041 and test group 3: look for error values (Home > Find & Select > Go To Special > Formulas > Errors). | None found. | |
| 5 | Check rows (sheet Mitigation, all ten groups): `ener.chk`, `rev.chk`, `co2.chk`, `bco2.chk`, `ch4b.chk`, `rpol.chk`. | 0 in every column (rounding below 1e-6). | |
| 6 | Sheet LiveOutputs, scenario 2, 2030: compare a few results (CO2 change, total revenue, GDP effect) with sheet StoredOutputs. | Same values (StoredOutputs was written by the build's LibreOffice run). | |
| 7 | Developer > Macros > `CheckBatchRun`. | Sheet with the macro checks; every line OK. | |
| 8 | Developer > Macros > `RunAllScenarios`. Do not use a definition with a new ETS for this step: the user tests the ETS goal seek separately (I30). | All definitions with Run? = Yes run and are stored; scenario 1 is restored at the end. Note the run time. | |
| 9 | Sheet Distribution: change ScenarioDefinition `TransferType` to an ASPIRE program, then to a poverty line, recalculate. | Transfers change; no error values; the charts update. | |
| 10 | Charts (Distribution and results sheets). | Every chart shows data, with no empty series or broken axes. | |
| 11 | Rolled-up view: the outline buttons (1 and 2) on Mitigation. | Rows collapse to one summary row per section and expand back. | |
| 12 | Paste test: copy ScenarioDefinition column of scenario 2 into an empty definition column, set Run? = Yes, run `RunAllScenarios`. | The new definition's stored results equal scenario 2. | |
| 13 | Sheet ScenarioCompare (the dashboard): the six macro buttons top right (Run all scenarios, Store baseline, Store live scenario, Solve ETS (live scenario), Clear stored scenarios, First-run test). Click First-run test. | Each button shows its label in full; the click runs CheckBatchRun. | |
| 14 | Sheet ScenarioCompare: the eight charts right of the table, after step 12. | The baseline (dashed) and one line per stored scenario, the new definition of step 12 included, in the scenario slots of row 6; empty slots draw nothing (#N/A in the chart data at the bottom of the tab); no line at 0. | |
| 15 | Save as a new .xlsm, close, reopen. | Opens cleanly; values unchanged after recalculation. | |

Send the filled list, with screenshots of any error, to the MVP team. Fixes follow in the next release (step 3.3 of the plan).
