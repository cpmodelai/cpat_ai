# Plan: the distribution module in the CPAT-AI-Mitigation-MVP workbook

Status: built as a prototype in CPAT-AI-Mitigation-MVP v4.4 (2026-10-17), following the revised design below; method and bug fixes in `../mitigation/Distribution_Method_v4_4.md`. Steps 1-6 done for the default options (cash transfer, no poverty-line target); open items in `../TODO.md`. Inputs: the standalone prototype (`standalone/`), the legacy sheet `Distribution` of `../legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb`, the Python port `../../coded/cpat_model/distribution/`, the specification `../../other/more/CPAT_Distribution_Module_Pseudocode.docx`, and the MVP norms (`../NORMS.md`).

## 1. What exists

### The standalone prototype (`standalone/`)

- **Current file:** `CPAT_Distribution_Standalone_Egypt_v0.4.xlsx`; older versions are in `standalone/Old/`.
- **How it is built:** `build_workbook.py` writes the file with formulas and names blank. The macro `RebuildDistributionModule.bas` then installs 39 LAMBDAs and about 1,400 formulas through `Names.Add` and `Range.Formula2`. `reference_calc.py` is the Python check of the design.
- **Layout:** sheets `Distribution_Inputs` and `Distribution_Outputs` (1,487 rows), plus data tabs as Excel tables.
  - One country, one analysis year (2030) and one scenario; there are no year columns.
  - P holds the basket, Q:Z the deciles 1-10, filled by one spilled formula per row (`=BSHARE(...,DECILE_ARRAY,...)`).
  - Each item has 24 rows: 4 statistics x 3 samples x basket/deciles.
- **Remaining error:** three `#VALUE!` cells, `Distribution_Outputs!P1408`, `P1411` and `P1414`. These are the basket value of "Net effect, post-recycling" for Overall, Urban and Rural.
  - `NET_EFFECT(0, ...)` reaches `ASPIRE_PC`, which computes `q = ROUNDUP(decile/2, 0)` and returns `CHOOSECOLS(row, q)`. With the basket (decile 0) this is `CHOOSECOLS(row, 0)`, which gives `#VALUE!`, and multiplying it by a zero spending share does not help.
  - Recycled amounts are defined per decile, so the basket value should be the total recycled divided by total consumption. A guard alone (as `ELASTADJ` has) would only hide the error.
- **Not to take as given:**
  - `LESSONS_LEARNED.md` mentions a Tests sheet that v0.4 does not have.
  - The Inputs sheet repeats its section headers at rows 29/31 and 34/36.
  - Targeted transfers and public investment both use the infrastructure-access share instead of legacy's bottom-40% coverage/leakage method.

### Legacy `Distribution` sheet

- **Size:** 3,038 non-empty rows, last row 3382, last column BT.
- **Descriptor columns:** B checks, C country, D code, E statistic, F sample, G scenario, H item, I description, J unit, K source, L-M input codes, N output code, O note, P helper.
- **Value columns change meaning by section:**
  - years 2022-2040 in §B.II;
  - deciles 1-10 in Q:Z in §C.III-C.IX, with the basket on separate rows;
  - GTAP sectors across F:BT in §C.I and §F.
- **Inputs from Mitigation (139 input codes):**
  - `egy.mit.rp.ind.<fuel>.a.{1,2}` and `egy.mit.atp.<fuel>.<sector>.pc`: retail prices by fuel and sector, BAU and carbon tax.
  - `egy.mit.ener.tot.<fuel>.e`.
  - `egy.mit.exp.<fuel>.usd.1`, `egy.mit.cptraj.2`.
  - GDP, deflator and population rows.
- **Sections:**

| Section | Rows | Content |
|---|---|---|
| A | 3-120 | Overview and country coverage |
| B.I | 121-250 | Key assumptions (switches, revenue shares) |
| B.II-B.III | 251-464 | Energy price change data and calculations (8 fuels x sectors) |
| B.IV | 465-489 | Pass-through coefficients |
| C.I | 492-737 | Price changes by GTAP sector |
| C.II | from 738 | Elasticities and deadweight loss |
| C.III-C.VII | 885-2241 | Budget shares, direct, indirect and total effects |
| C.VIII | from 2242 | Survey to national accounts |
| C.IX | from 2396 | Gini |
| C.X-C.XI | 2541-2767 | Transfers, investment, spending, PIT |
| D | 2768-3324 | Chart outputs |
| F | 3360-3382 | Results for MT |

### The Python port (`../../coded/cpat_model/distribution/`)

- It covers all 14 steps of the pseudocode and is tested.
- It equals the old code exactly (merge of 2026-10-17).
- It is the natural independent check for the Excel module.
- **Known gaps:** carbon-pricing revenue units (USD m used as local currency), national totals not wired, sectoral pass-through and GDP chain missing (see `README.md`).

## 2. Recommended design (revised 2026-10-17 after the user's review)

The first proposal (years across, deciles down, every sample and statistic) was too large. It came to about 15,000 rows. Distribution is a short-term analysis (to 2030), and legacy itself works the same way:
- MTOutputs rows 1000-1001 hold one analysis year (`dist.year`) and one statistic (`dist.stat`);
- almost every output is Overall, with deciles across;
- Urban and Rural appear only for the total effect, compensation, Gini and recycling.

The design below follows that.

**One sheet `Distribution`, one analysis year, three scenario groups, deciles across.**

| Choice | Design |
|---|---|
| **Settings (section 0)** | Analysis year (2023-2030, default 2030) and statistic (mean, median, p25, p75; default mean), as legacy `dist.year` and `dist.stat`. One setting for the sheet. |
| **Column group** | Code column + basket + deciles 1-10 + spacer = 13 columns. Row 1 holds `Basket, 1 ... 10` where Mitigation has years. Row 5 holds the scenario number (same formula as Mitigation). Frozen rows and descriptor columns A-J as Mitigation. |
| **Three groups** | Group 1 = scenario 1 (baseline levels: budget shares, consumption, population; effects 0). Group 2 = policy. Group 3 = LAMBDA test group running group 2's scenario (NORMS 3). It reads Mitigation's group 3, so it also tests Mitigation's LAMBDAs end to end. Pasting a group to the right adds a scenario, as in Mitigation: up to 5 policy scenarios (groups 4-7 run scenarios 3-6; NORMS 3e, Scenario capacity). The paste test covers both sheets. |
| **Rows** | One row per item and sample. Overall for every item. Urban and Rural rows only where legacy outputs them. The statistic switch changes the decile values in place, with no extra rows. About 250 rows; one formula per row across the 11 columns (about 8,000 formulas). |
| **Link to Mitigation** | Section 1 only. Each row reads the analysis-year value of the same scenario group with `=INDEX(Mitigation!$K$r:$IZ$r, L$6)` (the range covers Mitigation's 7 groups of the scenario capacity, with room to spare). Row 6 holds the Mitigation column offset (group position x 22 + analysis year - 2021), so the formula is copy-pasteable across groups. Price changes are against group 1 (`x/INDEX(...)-1`, as the Mitigation difference rule). |
| **Items without deciles** | Prices by fuel and GTAP sector, revenue and national totals use the basket column only. |
| **Formulas** | Plain formulas of at most 100 characters in groups 1-2. The prototype's 39 LAMBDAs are rewritten without `DECILE_ARRAY` spills (one decile per cell, the decile taken from row 1) and used in group 3 only. |
| **Sections (rolled up)** | 0 settings; 1 inputs from Mitigation (B.II-B.III); 2 indirect prices by GTAP sector and CPAT category (C.I); 3 elasticities and DWL (C.II); 4 budget shares (C.III-C.IV); 5 direct, indirect and total effects (C.V-C.VII); 6 survey to national accounts (C.VIII); 7 recycling (C.X-C.XI); 8 net effect (C.XII); 9 Gini (C.IX); 10 compensation (C.XIII). Summary row: total effect for the bottom decile (second row: top decile). |
| **MTOutputs** | A standalone distribution section: legacy rows 909-1029 with their legacy codes (`egy.distn.*`), deciles across, read from group 2. These are the outputs compared with legacy's cached Egypt values. |
| **Data** | HHSurvey, HH_Elast, IO_GTAP, ASPIRE, WHOCooking and GDPRatios under a new divider `DATA_DISTRIBUTION->>`. |
| **Standalone tool** | Kept. Later it can be built from the same builder and layout, with section 1 reading a pasted input block instead of Mitigation. For now it is only fixed (v0.5). |

## 3. Steps (one version each, quick check after each, as NORMS 3f)

1. **Fix the standalone tool** (v0.5): the basket value of the net effect is total recycled / total consumption, so the three `#VALUE!` cells go.
2. **Data tabs** and the divider.
3. **Sheet skeleton:** section 0, the 13-column groups, the offset row, the spacer test and the LAMBDA test group.
4. **Sections 1-5:** inputs, prices, budget shares, effects.
5. **Sections 6-10:** rebasing, recycling with Mitigation revenue in LCU, Gini, compensation.
6. **MTOutputs section** with legacy codes. Checks:
   - legacy's cached Egypt values;
   - the prototype v0.5;
   - the Python port, on the workbook's own price changes.
7. **Docs and norms** (About, Cover, method note, NORMS: Distribution geometry).
