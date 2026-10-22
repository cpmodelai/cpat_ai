# Procedure: fix a bug in the main CPAT workbook and confirm it all works

Worked example: legacy bug **L1** (services electricity demand grows with the industrial multiple after 2023; register: [`../mitigation/LegacyBugFixes_v3_6.md`](../mitigation/LegacyBugFixes_v3_6.md)). Macro: [`FixL1_ServicesElectricity.bas`](FixL1_ServicesElectricity.bas).

## 1. Why L1 is the example

It breaks both protocols of legacy CPAT, so one fix exercises both tests:

| Protocol | What L1 violates (read from `CPAT 1.0pre_456_NoPropData.xlsb`, sheet `Mitigation`) |
|---|---|
| **Drag left to right**: every year cell of a row has the same R1C1 formula | Row 3731 ("Services (public & private)"): `M3731 = RC[-1]*R[-18]C` (services multiple, row 3713) but `N3731:AE3731 = RC[-1]*R[-24]C` (industrial multiple, row 3707). The row cannot be dragged. |
| **Copy-paste baseline to policy**: the policy block is the baseline block shifted by a fixed number of rows | Baseline starts at row 2173 (name `BaselineFirstRow`), policy at 8504 (`PolicyScenarioFirstRow`): offset **6,331**. The bug is in both blocks: row 10062 is the same wrong formula. |

It is also a High-priority bug with a large, measurable effect (below), downstream of a single row, and it needs no new input.

## 2. The procedure (what the macro does, in order)

Run the macro in a **copy** of the workbook. It never saves; you decide.

| Stage | Step | Pass rule |
|---|---|---|
| **P** Preflight ("has CPAT changed?") | Find the rows by label and code, not by row number: `Overall Multiple, Services` and `Overall Multiple, Industrial` (column D, twice each), then the first row below with code `srv` in column C. Find the column of 2024 in row 1. Check the block offset equals `PolicyScenarioFirstRow - BaselineFirstRow`. Check that the row has exactly the bug formula in every year, in both blocks. | Every item PASS. If the formulas are already fixed, or differ from the register, **the macro stops before changing anything**. |
| **S** Snapshot | Full recalculation in your Excel, then keep all formulas (R1C1) and all values of the sheet in memory. | n/a |
| **F** Fix | Baseline: write one formula in the first wrong year and `FillRight` (a real drag). Policy: copy the baseline cells and paste formulas (a real copy-paste). Full recalculation. | n/a |
| **T1** Drag | Row has one identical R1C1 formula from 2023 to the last year, in both blocks. | 0 cells differ |
| **T2** Copy-paste | Policy row R1C1 = baseline row R1C1. | 0 cells differ |
| **T3** Nothing else moved (formulas) | Whole sheet, before vs after: exactly the intended cells (2 rows x 18 years = 36) changed. | 36 of 36, 0 others |
| **T4** Independent calculation | Each year's value = previous year x services multiple, recomputed in VBA from the recalculated values. | 0 years differ |
| **T5** Past unchanged | Years before 2024 (L:M) unchanged everywhere on the sheet. Column K is reported separately (summary rows put totals and maxima there). | 0 changed, else REVIEW |
| **T6** No new errors | Count of error cells does not increase. | after <= before |
| **T7** Reconciliation | Change of total demand (row 3741 / 10072) equals the services change, within 5%; the gap is other sectors moving through price feedback. | REVIEW if > 5% |
| **R** Report | Number of changed rows; the 15 rows with the largest change as a share of the row's own size, for you to read. | judgement |

The result is written to a new sheet `FixLog` (Overall = PASS / REVIEW / FAIL). `FixL1_Revert` restores the two rows in the same session; otherwise close without saving.

## 3. How to use it

1. Copy the workbook; never fix the only copy (repo rule: [`../NORMS.md`](../NORMS.md) section 5, new version for every saved change).
2. Open the copy, enable macros. `Alt+F11`, `File > Import File...` and pick `FixL1_ServicesElectricity.bas` (or `Insert > Module` and paste its text).
3. `Alt+F8`, run `FixL1_ApplyAndVerify`. Takes about 1 minute on the NoPropData file (two full recalculations).
4. Read `FixLog`. FAIL: close without saving. REVIEW: open the cells named, decide, write the decision down. PASS: `Save As` the next version.
5. Optional, not done by the macro: switch the scenario (`MTInputs!D6`, name `_ScenarioToRun`) to a policy scenario and run it again; T1 to T4 must still pass and the policy block will show a different (non-baseline) effect.
6. Record it: the register entry (L1) gets "fixed in legacy version x", and the workbook's version log gets a row.

## 4. Result of the test run (scratch copy of the NoPropData legacy file, Excel 365, 2026-10-15)

| Check | Result |
|---|---|
| Preflight P1 to P6 | PASS: rows 3713/10044 (services multiple), 3707/10038 (industrial), 3731/10062 (demand); offset 6,331; bug formula in all 18 years of both blocks. So, for this file, **nothing has changed from the register** |
| Run on an already-fixed file | stops at P5/P6 with FAIL "state = FIXED", nothing changed |
| T1 drag, T2 copy-paste | PASS (`=RC[-1]*R[-18]C` in M:AE, both blocks) |
| T3 | PASS: 36 of 36 formula cells changed, 0 others |
| T4 | PASS |
| T6 | PASS: 2,160 error cells before and after (inherited from the stripped NoPropData file) |
| T7 | PASS: total demand moves with services; other sectors add at most 2.4% (baseline) and 4.1% (policy) of the services change from 2026 on (price feedback) |
| T5 | **REVIEW**, 72 cells in column M (2023) in rows 14399 to 14592 and similar: the fiscal-multiplier tables ("Effects of year 2:" `=INDEX($K14375:$AE14375, MATCH(M14398,...))*$F14399`), whose columns are lags (M14398 = 1), not calendar years. So "2023" is not what the column means there. **Why the multipliers respond to electricity demand is not established**; it needs the CPAT team |
| Revert | restores `=RC[-1]*R[-24]C` in both rows, rerun passes again |

Effect of the fix on this file (services electricity demand, ktoe/y, 2041): baseline **6,685 to 8,743 (+30.8%)**, policy **5,508 to 6,397 (+16.1%)**. 3,979 rows change, among them energy and CO2 totals, the power investment logit and solar investment.

## 5. Reusing the harness for the next bug

Same stages P, S, F, T, R. Change only:

| Part of the `.bas` | What to change |
|---|---|
| Constants at the top (`LBL_*`, `CODE_SRV`, `YEAR_FIX`) | Labels and codes that locate the rows; first year of the wrong formula |
| `Locate`, `FindSrvRow` | How the row is found (always by label/code, never a typed row number) |
| `RowState` | The wrong and the right R1C1 formula (this is the "has CPAT changed" test) |
| `ApplyFix` | The new formula; keep "drag in the baseline, paste into the policy" |
| `TestIndependent`, `TestTotals` | The independent recomputation and reconciliation of the new bug |

Keep: the whole-sheet formula diff (T3), the values-before-the-change test (T5), the error count (T6), the `FixLog` sheet and "never saves".

## 6. Limits

- Tested on the NoPropData legacy file only. Your current CPAT may differ: the preflight is there to say so, and stops without changing anything.
- Runs on the active workbook's sheet `Mitigation` only; effects on other sheets (Dashboard, Transport) are not compared.
- Does not shift inputs by itself (step 5 in section 3 is manual).
- The report ranks changed rows; it cannot say whether a change is right. The independent check (T4) covers the fixed row only; everything downstream is judged by reading the report.
- Needs macros enabled and the file kept as `.xlsb` or `.xlsm`.
