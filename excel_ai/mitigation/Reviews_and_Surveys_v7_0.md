# Reviews and surveys of legacy CPAT (CPAT-AI-Mitigation-MVP v6.4)

Reviews of legacy CPAT made while rebuilding it, in one note: the health scan of every results row, the survey of the sector equations and the survey of what reads the legacy outputs downstream. Each section is a former note, unchanged apart from its headings; its former file name is in the section title.

1. [Legacy CPAT mitigation results: assessment of every results row, and a strategy to fix them](#1-legacy-cpat-mitigation-results-assessment-of-every-results-row-and-a-strategy-to-fix-them-results_assessment) (former `Results_Assessment_v6_4.md`)
2. [Legacy fuel-use equations by subsector against the MVP: survey](#2-legacy-fuel-use-equations-by-subsector-against-the-mvp-survey-sector_equations_survey) (former `Sector_Equations_Survey_v6_4.md`)
3. [Legacy downstream results processing after the two scenario blocks: survey](#3-legacy-downstream-results-processing-after-the-two-scenario-blocks-survey-downstream_survey) (former `Downstream_Survey_v6_4.md`)

## 1. Legacy CPAT mitigation results: assessment of every results row, and a strategy to fix them (Results_Assessment)

Assessment of the results rows of the legacy mitigation module, `CPAT 1.0pre_456_NoPropData.xlsb`, sheet Mitigation (Egypt, cached values). It covers two places:
- **the results inside each scenario block:** sections 11-17 and the cross-check tests of block C (baseline, rows 6282-8403), repeated in block D (carbon tax, rows 12613-14734);
- **the results area after the two scenario blocks:** E (hand-offs to other modules), F (report sections) and G (other purposes), rows 14770-19220.

Sources:
- a scan of the cached values of every row, baseline and carbon tax, for this note;
- `Reviews_and_Surveys_v7_0.md` (section Downstream_Survey) (blocks E, F, G in detail);
- `Reviews_and_Surveys_v7_0.md` (section Sector_Equations_Survey) (fuel-use equations);
- `Transport_Legacy_Survey_v7_0.md`;
- the method notes;
- the register (`issues_register_v7_0.py`, lists `../BUGS.md` and `../ISSUES.md`).

Bug ids L.. and issue ids I.. refer to the register. Row numbers are legacy rows.

---

### 1. Summary

1. **The two scenario blocks hold the real results; the results area mostly rearranges them.**
   - **Scenario blocks.** Sections 11-17 are about 2,100 rows per scenario, and most of them are computed values: energy use, CO2, non-CO2 and local pollutants, GHGs, revenues, GDP effects.
   - **Results area.** Its blocks E, F and G (about 4,400 rows) mostly re-arrange scenario rows by code lookup. Real computation happens only in a few report sections: prices (F5), welfare and externalities (F10), balance of payments (F11), NDC (F12) and Kaya (F14).
2. **The values that matter have errors, in the scenario blocks and the results area alike.**
   - **Scenario blocks.** Their 1,757 numeric rows (sections 11-17) have no error values, but the sector and power bugs feed into them (L1-L24, L42-L48), and so do the missing fuel-use shock and jet fuel (I22, I19).
   - **Results area.** Error values cluster in the sections that compute: F10 welfare (15 rows, including the total welfare benefits), F11 balance of payments (9 rows of `#NAME?`), F12 NDC (6) and G (14).
3. **A large share of rows carry nothing in the Egypt run.** 525 of the 1,757 numeric rows in sections 11-17 are zero in both the baseline and the carbon-tax run. The reasons:
   - features switched off (the elasticity power model, biomass leakage, renewable subsidies, vehicle policies);
   - data stripped from the NoPropData file (the GDP-effect rows; the combustion factor paths, so combustion CH4 is zero);
   - sectors that do not use a fuel in Egypt.
   These rows cannot be validated on this file.
4. **The design itself causes several of the problems** (section 2): two scenarios only, results duplicated in two blocks, lookups by code string, a loop through the downstream modules, unit values reported as price changes (I31), and labels that disagree with the formulas.
5. **The MVP has already rebuilt most of the scenario results (sections 11-17)** with the legacy bugs fixed. It has rebuilt only a little of the results area (section 4, table B).

---

### 2. Cross-cutting problems of the legacy results layer

| # | Problem | Where | Effect | Kind |
|---|---|---|---|---|
| S1 | **Two scenarios only.** Every results row exists twice: block C and the copy in block D, 6,331 rows lower. The results area reads one baseline and one policy scenario. | C, D, E, F, G | A third scenario needs a re-run with the scenario number swapped. A change to one block has to be copied to the other by hand. | Design (issue) |
| S2 | **Results re-arranged by code lookup.** E, F and G build a code string in column G and use `MATCH` over rows 2173-14770, then `INDEX` by year. | E, F, G | Fragile: one changed code silently returns another row, or `#N/A`. Labels and codes disagree in places (E2 15771-15775 "baseline" holds policy values; F5 `H16332` builds its code from the industry row). | Design (issue); the mislabels are bugs |
| S3 | **Loop through the downstream modules.** Mitigation E feeds Air pollution and Transport, whose results return to F10. MTOutputs (legacy) reads F and feeds three cells back into F (carbon price, GDP, policy GHG). | E, F, MTOutputs | The order of calculation is unclear, and results depend on sheets outside the module. | Design (issue) |
| S4 | **Unit values reported as price changes (I31, major).** Average prices weight by each scenario's own consumption. | F5b-c, E1 price tables | The "price change" mixes composition with price (Egypt 2030: gas +71%, oil +104%). | Issue (I31) |
| S5 | **Proprietary data stripped.** The NoPropData file lacks the price forecasts and the factor paths. | C17, F4, C13 | 189 of 231 numeric GDP rows are zero in the baseline (77 in both scenarios); combustion CH4 is zero. The legacy GDP effects cannot be validated. | Data (issue) |
| S6 | **Dead and inactive rows.** Rows for switched-off features, or always zero. | All sections (counts in section 3) | Hard to tell a feature that is off from a broken row. Dead code: residential exemption rows (L48), aviation and navigation renewables (L47). | Mixed: dead code is a bug, inactive features are issues |
| S7 | **Hard-coded ranges and offsets.** Lookup ranges that stop early (E3 `oc` range to 15266), one-row offsets (F9 17336-17339 columns L:M), fixed-column sums (F11 18215 uses column K for L). | E, F | Mostly harmless today; wrong as soon as data or years change. | Bugs |
| S8 | **Labels that mis-state the effect.** The fuel-use shock is called "Covid factor" with effect "Small" (I22). F5 titles name a carbon price for a year before the policy starts. F12 16672 is labelled CO2 change but computes the change in ECR. | C, F | Readers draw wrong conclusions. | Bugs in labels |

---

### 3. Health scan of the cached values

Columns L-AE hold 2022-2041. Error values: `#N/A` / `#DIV/0!` / `#NAME?`. "All zero" counts rows whose numeric values are all 0 in the baseline. For sections 11-17, the second table counts rows that are zero in **both** scenarios (so not a policy row that is simply zero in the baseline) and rows that differ between the scenarios.

**Scenario blocks (block C; block D is the same layout):**

| Section | Rows | Numeric rows | Zero in baseline | Zero in both scenarios | Differ between scenarios | Error rows |
|---|---|---|---|---|---|---|
| 11 Energy consumption (6282-6506) | 225 | 197 | 90 | 50 | 130 | 0 |
| 12 Energy-related CO2 (6507-6602) | 96 | 81 | 22 | 11 | 61 | 0 |
| 13 Non-CO2 GHGs and local pollutants (6603-7447) | 845 | 767 | 451 | 310 | 412 | 0 |
| 14 GWP of non-CO2 GHGs and pollutants (7448-7531) | 84 | 68 | 5 | 1 | 51 | 0 |
| 15 GHGs (7532-7640) | 109 | 92 | 10 | 1 | 81 | 0 |
| 16 Fiscal revenues (7641-8027) | 387 | 321 | 156 | 75 | 217 | 0 |
| 17 GDP effects (8028-8290) | 263 | 231 | 189 | 77 | 148 | 0 |
| Cross-check tests (8291-8403) | 113 | 78 | 9 | 7 | 51 | 0 (69 cells read "PASSED") |

**Results area:**

| Block | Rows | Numeric rows | All zero | Error rows (N/A / DIV0 / NAME) |
|---|---|---|---|---|
| E1 Distribution hand-off (14770-15720) | 951 | 717 | 145 | 0 (the GTAP block has `#N/A` outside the year columns) |
| E2 Transport hand-off (15721-15823) | 103 | 85 | 12 | 4 (0/4/0) |
| E3 Air pollution hand-off (15824-16080) | 257 | 210 | 38 | 0 |
| F2 Macro drivers | 44 | 23 | 0 | 0 |
| F3 Policy coverage | 31 | 20 | 4 | 0 |
| F4 GDP effects | 43 | 33 | 2 | 0 |
| F5 Prices | 520 | 330 | 58 | 4 (0/4/0) |
| F6 Power costs | 60 | 48 | 0 | 0 |
| F7 Energy consumption | 196 | 179 | 46 | 0 |
| F8 Power | 161 | 134 | 42 | 1 (0/1/0) |
| F9 Revenues | 244 | 196 | 50 | 0 |
| F10 Welfare and externalities | 774 | 642 | 125 | 15 (13/2/0) |
| F11 Balance of payments | 45 | 27 | 0 | 9 (0/0/9) |
| F12 GHG, NDC, grid | 322 | 173 | 10 | 6 (6/0/0) |
| F13 CO2 detail | 330 | 258 | 47 | 2 (2/0/0) |
| F14 Kaya | 64 | 49 | 0 | 0 |
| F15 Methane | 41 | 32 | 15 | 0 |
| F16 EV, VKT, CBAM | 54 | 44 | 3 | 0 |
| G Prices, markups, energy balance | 188 | 126 | 29 | 14 (14/0/0) |

A row with no error value can still be wrong. F14 Kaya has no error values, but its primary energy is -97% (a bug); F9 has a one-row offset.

---

### 4. Section by section

Strategy codes (section 5):
- **V** = built in the MVP: validate against legacy and close the gaps;
- **R** = rebuild as a report from rows the MVP already has (no new data);
- **D** = needs a small data table;
- **M** = needs a downstream module;
- **X** = not carried over (design or plumbing, not a result).

#### A. Results inside the scenario blocks (sections 11-17)

| Section | What it holds | Legacy quality | MVP status | Strategy |
|---|---|---|---|---|
| **11 Energy consumption** (6282-6506) | Power sector (model switch: elasticity or engineer); transport by fuel incl. jet fuel and biofuels; buildings, industry and other energy use by subsector and fuel; total energy consumption (TEC) by fuel and sector | The sector bugs feed in: aviation swapped form (L42), other energy use without GDP growth (L43), road engineer bugs (L25-L41, latent), power bugs (L1-L10). The fuel-use shock is applied in every row (I22, not replicated). 50 rows zero in both scenarios (elasticity power model, biofuels, unused fuels). | Section 11 (`ener`, `ener.pct`, totals incl. power). **Missing: jet fuel (I19) and the shock (I22).** The elasticity power model is not built (later item). | **V**; close I19, I22, I23, I24 |
| **12 Energy-related CO2** (6507-6602) | CO2 by fuel and sector; power emission factor (t/MWh); totals by sector and fuel | Correct given fuel use. IIASA factors without inventory adjustment; legacy offers a switch (row 7534). | Section 13 (`co2`, `co2.chg`, by fuel and sector, power, ETS sectors); calibration switch (v3.2, off as legacy). No t/MWh row (F12 grid intensity uses it). | **V**; add the t/MWh row (R) |
| **13 Non-CO2 GHGs and local pollutants** (6603-7447) | 8 pollutants (PM2.5, NOx, SO2, VOC, BC, OC, CH4, CO) by sector and subsector; totals by subsector and by the 8 air-pollution sectors; POM, other PM2.5 | Navigation left out of the totals (L22); services and food & forestry left out of the totals (L23). 310 rows zero in both scenarios: combustion CH4 (factor paths stripped), zero sectors. | Section 15 (v2.9-v3.0: `ap`, `aps`, POM, other PM2.5), bugs fixed. Factor mapping where GAINS has no match differs (I27, to replicate: zero as legacy). | **V**; I27 |
| **14 GWP of non-CO2 GHGs and pollutants** (7448-7531) | GWP100 of CH4 and of each local pollutant by sector; net forcers and net coolants; totals by pollutant and sector | Consistent. Memo values, not in the GHG totals. | Section 15 memo `apf` by pollutant (GAINS region GWP); not by sector | **V** (by-sector split: R if wanted) |
| **15 GHGs** (7532-7640) | Option switches; non-energy growth (income, population, effort); categories (energy, industrial processes, agriculture, LULUCF, waste, other); totals by sector and by gas | Non-energy methane constant and abatement not applied (L18); flaring CO2 counted as methane (L19); population path (L20); waste on the livestock curve (L21). Industrial processes above the MVP for unexplained reasons (I25). | Section 14 (v2.8), bugs fixed. I25 and I26 open. | **V**; I25, I26 |
| **16 Fiscal revenues** (7641-8027) | Info: fuel expenditures by fuel and sector, revenue lost to price controls; baseline coverage; revenue by fuel; additional excise; auctioned ETS; existing excises incl. consumer subsidies; consumer subsidies (info); producer subsidies; VAT; renewable subsidies cost; methane fee; vehicle purchases, vehicle feebates, ad-valorem vehicle taxes, vehicle subsidies, charging subsidies, distance tax, all transport revenue; totals by fuel and by policy | No error values. 75 rows zero in both scenarios (vehicle policies off, renewable subsidies, producer subsidies 0 for Egypt). | Section 12 (`rtx`, `rsub`, `rnew`, `rnet`, `rtot`, `rmf`, power rows `rvat`, `rgap`, `rcarb`, `rnvat`; `rtot.chg`). **Missing:**<br>- fuel expenditures;<br>- price-control losses;<br>- producer subsidies;<br>- renewable subsidies cost;<br>- the vehicle revenues of the engineer road model (feebates, purchase taxes, subsidies, charging, distance tax);<br>- revenues by fuel in the legacy layout. | **V** + **R** (expenditures, by-fuel table); vehicle revenues with the engineer road model (V) |
| **17 GDP effects** (8028-8290) | Fiscal space by revenue use, multipliers, effect on GDP, adjusted GDP | GDP effect added to growth every year (L24). The NoPropData file strips the effect rows (S5), so 77 rows are zero in both scenarios. | Section 16 (v3.1), L24 fixed, multipliers by income group | **V** (no legacy benchmark: issue) |
| **Cross-check tests** (8291-8403) | Subsection checks (totals = sum of parts, "PASSED") | 69 cells PASSED in the baseline | Replaced by the MVP check scripts (`check_quick`, `check`) and check rows (`rev.chk`, `bco2.chk`) | **X** |

#### B. Results area (blocks E, F, G)

| Block | What it holds | Legacy quality | MVP status | Strategy |
|---|---|---|---|---|
| **E1 Distribution hand-off** (14770-15720) | GDP, carbon price, revenue % GDP, power EF, price grids baseline and policy (17 subsectors × 10 fuels), % price and consumption changes, revenue by fuel, inflation, GTAP IO table | Mostly lookups. Scenario taken from different cells (harmless); GTAP block `#N/A` outside the year columns. Price changes are unit values where averaged (I31). | Price grids exist per scenario (section 2). The % change tables, consumption changes and GTAP extract are missing. | **R** + **D** (GTAP IO); then **M** (Distribution) |
| **E2 Transport hand-off** (15721-15823) | Road fuel by vehicle class (bn litres), efficiency and driving margins, shares, VKT, fuel economy | "Baseline" rows hold policy values (15771-15775); LPG margins `#DIV/0!` when road LPG is 0; the diesel margin is a blend; reads the engineer rows even when the elasticity switch is on | Section 5b has fuel by class, VKT, fuel economy. Margins, shares and the table are missing. | **R**; then **M** (transport externalities) |
| **E3 Air pollution hand-off** (15824-16080) | GDP; power and residential energy use; 10 pollutants × 8 source groups, baseline and policy; CO2 and GWP; revenue | `oc` lookup range stops early (harmless); food/agriculture pollutant units look inconsistent (check) | Section 15 `aps` holds the content; the layout is missing | **R**; then **M** (air pollution) |
| **F2 Macro drivers** (16086-16125) | GDP, population, international prices, elasticities, implied CO2 income elasticity | 2 issues in the survey | Inputs exist; summary rows missing | **R** |
| **F3 Policy coverage** (16127-16157) | Coverage of CO2 by the carbon tax and by sector; revenue-recycling shares | No bugs found | Coverage switches and ETS coverage exist; % covered missing | **R** |
| **F4 GDP effects** (16160-16201) | Growth decomposition; year-of-reform profile | 2 issues; stripped data (S5) | Section 16 has the effects; the decomposition and profile are missing | **R** |
| **F5 Prices** (16204-16725) | Price components; consumption-weighted average prices; policy/baseline change; index 2022 = 100; total (implicit) carbon price by fuel and sector; effective carbon rate (ECR); price breakdown chart | Unit values as price changes (I31, major); coal ECR sums price ratios; ECR "CO2 reduction" row computes the ECR change, so the implied elasticity is garbage; biomass total carbon price `#DIV/0!`; misleading title; a code built from the wrong row | Section 2 builds every price; no averages, indices, total carbon price or ECR | **R** (v3.9 for the averages and indices; then total carbon price and ECR) |
| **F6 Power generation costs** (16726-16784) | Generation costs, switching prices, tipping points, system costs | No bugs found | Section 3 has the costs; the report tables are missing | **R** |
| **F7 Energy consumption** (16788-16983) | Energy by fuel and sector, changes | No bugs found | Section 11 by sector and totals; by fuel only on Mitigation | **V** + **R** (by-fuel change table, MTOutputs) |
| **F8 Power** (16987-17145) | Generation, shares, demand, capacity, investment | One `#DIV/0!` row | Section 3; MTOutputs rows | **V** |
| **F9 Revenues** (17148-17389) | Totals and by fuel; base erosion (PIIE); carbon tax revenue by sector; consumer and producer subsidies, % GDP | One-row offset in 17336-17339 for 2022-23 (harmless while the price is 0); 3 issues in the survey | Section 12 totals, by sector, power; by-fuel net, % GDP, base erosion and the consumer/producer split missing | **R** |
| **F10 Welfare and externalities** (17392-18172) | Efficiency (deadweight) costs; methane-fee efficiency cost; SCC and global warming costs; welfare benefits; externalities; explicit and implicit subsidies (IMF method); efficient prices; Pigouvian taxes | **Worst block.** The "non-road oil" global-warming cost is `#N/A`, which spreads to total environmental benefits and total national welfare benefits including fuel subsidies. LPG pre-existing tax row empty, so the LPG average tax is halved. Diesel and kerosene converted with the wrong factors. LPG residential row holds a subsidy formula, so LPG VAT is 0. Coal row offsets; electricity "other" column mix. | Not built | **R** (efficiency costs, climate part) + **D** (SCC data) + **M** (air and transport co-benefits, externalities) |
| **F11 Balance of payments** (18175-18219) | Net imports, current account, % GDP | Pre-policy current account `#NAME?`, so the whole % of GDP panel errors; one-year column lag; sign of policy net imports looks reversed; oil has no import-share factor | Not built | **D** (net imports, import shares) |
| **F12 GHG, NDC, grid** (18222-18541) | GHG by broad sector and gas, abatement; NDC comparison and goal seek; grid intensity | NDC target level adjusted twice when the target year is before 2030; baseline/target ratio inverted between rows; 6 `#N/A` rows | Section 14 by gas and category; broad-sector allocation, NDC and grid intensity missing | **R** (broad sectors, grid) + **D** (NDC data) |
| **F13 CO2 detail** (18544-18870) | CO2 by fuel, sector, subsector; industry CO2 incl. indirect; intensity per GVA | 2 `#N/A` rows | Section 13 by fuel and sector; indirect and per-GVA missing (need GTAP) | **V** + **D** |
| **F14 Kaya** (18874-18935) | Population, GDP per capita, energy intensity, carbon intensity | Primary energy -97% (bug) | Not built | **R** |
| **F15 Methane** (18938-18978) | Methane by source, abatement, fee | No bugs found; 15 zero rows | Section 14 | **V** |
| **F16 EV, VKT, CBAM** (18979-19031) | EV shares, VKT, ownership; CBAM | No bugs found | Section 5b on Mitigation, not in MTOutputs; CBAM sheet not built | **V** + **R** (MTOutputs rows); CBAM later |
| **G Prices, markups, energy balance** (19033-19218) | Intermediate prices and markups; energy-balance matrix | 14 `#N/A` rows | Built internally (section 2); not exported | **R** |
| Legacy MTOutputs (separate sheet, about 1,313 rows) | Export of F, D and G by code | Reads F; feeds three cells back into F (S3) | MVP MTOutputs (71 indicators × N scenarios), StoredResults, ScenarioCompare | **X** for the layout; rows added as each report is rebuilt |

---

### 5. Strategy to fix them

#### 5.1 Options

| Option | What it means | For | Against |
|---|---|---|---|
| **1. Fix legacy in place** | Apply each bug fix in the legacy workbook with the bug-fix procedure (`../bugfix_procedure/`, worked example L1). Each fix gets a verification harness. | Legacy users get correct numbers in the tool they use | Slow: 47 legacy bugs in the scenario blocks plus about 30 bugs and issues in the results area, each needing a harness and a full-workbook diff. The design problems S1-S3 stay. Needs the legacy team's current file. |
| **2. Rebuild in the MVP under the replication rule** | Build each results group in the MVP, per scenario, with one formula per row. Copy legacy's issues, fix its bugs, and track both. Validate against legacy's cached values with a Python reference that has one switch per bug, as for the power and road models. | Fixes S1, S2, S4 and S6 by construction. Small increments. Each result is checked against legacy. | The legacy tool stays wrong until its team ports the fixes. Some items need modules or data first. |
| **3. Both, with the MVP as the test oracle** | Option 2 for everything. Option 1 only for the high-priority legacy bugs, using the MVP and its Python references to tell the legacy team what the right numbers are. | Gives the legacy team a short, verified list and the expected values | Two code bases to keep in step for those few bugs |

**Recommendation: option 3.**
- **The MVP rebuild is the main line**, in small versions.
- **Legacy fixes are limited to the bugs that change standard results.** The 7 high-priority bugs, plus the F10 `#N/A` chain and the F11 `#NAME?` panel once those sections exist in the MVP, go to the legacy team through the bug-fix procedure.

#### 5.2 Rules for each increment

1. One results group per version. It ships with:
   - a regression of 0 on all other codes;
   - a Python recomputation in the check;
   - a comparison against legacy's cached values (`legacy_compare`);
   - the legacy bugs it fixes listed as L items, and the issues it copies listed as I items.
2. Results rows are per scenario (column groups); differences against scenario 1 use the existing `.ref` pattern. No code lookups.
3. Before rebuilding a group, list its legacy bugs and issues, so each one is classified up front: fix, replicate or decide.
4. Rows that are always zero in the Egypt run are built only with the feature that feeds them, never as empty placeholders.
5. Each group adds its headline rows to MTOutputs, StoredResults and ScenarioCompare.

#### 5.3 Recommended order (incremental)

| Step | Version (proposed) | Content | Strategy code | Why now |
|---|---|---|---|---|
| 1 | v3.9 | Average prices, Laspeyres price index against the baseline, time index, mix effect (I31) | R | Agreed; memo only, no result changes |
| 2 | v3.10 | Fuel-use shock (I22) and jet fuel (I19) | V | They move every result (energy, CO2, GHG, pollutants, revenue); later reports should be compared with legacy only after them |
| 3 | v3.11 | Energy and CO2 change tables by fuel, grid intensity (t/MWh), Kaya (F7, F12 grid, F13, F14) | R | Pure arithmetic; fixes the Kaya bug by construction |
| 4 | v3.12 | Revenues: by fuel net of subsidies, % of GDP, base erosion, consumer/producer split, fuel expenditures (F9, section 16 info rows) | R | Pure arithmetic on section 12 |
| 5 | v3.13 | Policy coverage, total (implicit) carbon price, effective carbon rate (F3, F5d-e) | R | Uses step 1 and step 4 |
| 6 | v3.14 | GHG by broad sector and abatement (F12) | R | The allocation must be documented, not hardcoded |
| 7 | v3.15 | Efficiency (deadweight) costs and climate welfare with SCC options (F10a-e, climate part) | R + D | Needs the SCC data sheet; fixes the F10 conversion and LPG bugs |
| 8 | v3.16 | Balance of payments and NDC comparison (F11, F12 NDC) | D | Small data tables; fixes `#NAME?`, sign and double-adjustment bugs |
| 9 | later | Hand-off tables E1-E3 in the legacy layout, then the Distribution, Transport-externality and Air pollution modules; F10f-h (externalities, subsidies, Pigouvian taxes) | R, then M | Large; each module is its own project (survey, reference, build) |
| 10 | later | Vehicle revenues of the engineer road model; power report tables (F6); energy-balance export (G); EV and VKT rows in MTOutputs (F16); CBAM | V / R | When the related feature is next touched |

Steps 3-6 are independent of each other and could be bundled if fewer, larger versions are preferred.

#### 5.4 Decisions for the user

1. Option 1, 2 or 3 (recommended: 3).
2. One results group per version (recommended), or bundles of steps 3-6.
3. Whether the cross-check tests and the legacy MTOutputs layout are dropped (X), as proposed: the MVP checks and MTOutputs replace them.

---

### 6. Where each result goes in the scenario calculations

Rules: `../NORMS.md` section 3c (user decisions 2026-10-15).
- **Sections 1-16 keep their numbers.** Legacy's post-processing goes into the existing section it belongs to, as a memo or a lettered sub-block.
- **Two new sections** take what has no home: 17 Carbon pricing and 18 Welfare and externalities.
- **Modules sit on their own sheets** (same column-group geometry) and read `Mitigation` rows directly; there is no hand-off block.
- **Output sheets only select and compare.**

#### 6.1 All sections, legacy and MVP

Legacy sections the MVP does not use are in parentheses. *New* marks additions from legacy's results area (blocks E, F, G), with the legacy source.

| MVP section | Legacy | Content | Additions (legacy source) |
|---|---|---|---|
| 1 Policies | 1 | Policy paths, carbon tax, ETS, feebates, fuel price reform, methane fee, existing carbon pricing | — |
| 2 Retail energy prices | 2 | International prices; domestic build-up by fuel and sector | *New* memo at the end: average prices (unit value), Laspeyres price index against scenario 1, time index with 2022 quantities, mix effect; per fuel, electricity, all energy; on after-tax prices incl. new policies (F5b-c, I31) |
| (—) | (3 Elasticity-based power model) | | Not built (later) |
| 3 Power sector | 4 Engineer power model | Costs, prices, demand, dispatch, capacity, investment | *New* memo: switching (tipping-point) prices, system cost (F6) |
| 5 Transport, 5b Road engineer model | 5 | Fuel use by mode; road engineer model | Vehicle revenues are reported in 12b. EV, VKT and ownership go to MTOutputs (F16) |
| 6 Buildings | 6 | Fuel use | — |
| 7 Industry | 7 | Fuel use | — |
| 8 Other energy use | 8 | Fuel use | — |
| (in 14) | (9 Methane) | Methane by source | Merged into MVP 14 |
| (—) | (10 Green public investment) | | Not built (TODO, remaining policies) |
| 11 Energy consumption | 11 | Fuel use by sector and fuel, totals | *New* sub-block 11b: energy change by fuel and sector (F7); energy-balance matrix sector × fuel (G) |
| 12 Revenues (**the one fiscal section**) | 16 Fiscal revenues | 12a existing taxes and subsidies; 12b new policies by instrument; 12c totals and change against scenario 1 | 12a: producer subsidies (0 for Egypt). 12b: vehicle revenues of the road engineer model (feebates, purchase taxes, subsidies, charging, distance tax). *New* sub-block **12d fiscal reports**: revenue by fuel net of subsidies; revenue % of GDP; base erosion (policy fuel use × baseline taxes); consumer and producer subsidies, % of GDP; fuel expenditures by fuel and sector; revenue lost to price controls; carbon tax revenue by sector (F9, legacy 16 info rows) |
| 13 Emissions | 12 Energy-related CO2 | CO2 by fuel and sector | *New* sub-block 13b: CO2 change by fuel and sector (F13); grid emission intensity, t/MWh (legacy row 6582, F12); Kaya decomposition (F14). Later: industry CO2 incl. indirect, per GVA (F13, needs GTAP) |
| 14 GHG emissions | 15 GHGs + 9 Methane | Inventory categories, methane by source | *New* sub-block 14b: GHG by broad sector and abatement (F12); NDC comparison and gap (F12; NDC data table; an NDC goal seek as a macro, like the ETS goal seek) |
| 15 Local air pollutants (**the air-pollution module's input table**) | 13 Non-CO2 GHGs and local pollutants + 14 GWP | Pollutants by subsector, totals, forcing memo, pollutants by air-pollution source group (`aps`) | Add `aps.ch4.<group>` (combustion CH4 by source group) and `aps.<pollutant>.all`; order the `aps` block like legacy's input table (NOx, SO2, BC, POM, OPM, VOC, CH4, CO, PM2.5, OC, each by cpp, gpp, opp, rod, gro, oth, foo, all) (E3) |
| 16 GDP effects and external balance | 17 GDP effects | 16a fiscal space, multipliers, GDP effect, adjusted GDP | 16a memo: growth decomposition, year-of-reform profile (F4). *New* sub-block **16b external balance**: net energy imports by fuel (fuel use × international price × import share), change against scenario 1, current account effect and % of GDP (F11; data: net imports and import shares, legacy rows 741-743) |
| **17 Carbon pricing** (new) | (F3, F5d-e) | Implicit carbon price of existing taxes and subsidies by fuel and sector, economy-wide; effective carbon rate; CO2 covered by the carbon tax and the ETS, by sector | Reads 2, 12, 13 |
| **18 Welfare and externalities** (new) | (F10) | Efficiency (deadweight) costs by fuel; methane-fee efficiency cost; climate damages with SCC options (national, global); welfare summary. Later: air-pollution and transport co-benefits, externalities per unit, explicit and implicit subsidies, efficient prices, Pigouvian taxes | Reads 2, 11-14, `.ref`; SCC data; later the modules |
| (—) | (Cross-check tests) | | Not carried: check scripts and check rows |

**Header rows** (above section 1, every scenario group):
- move the real GDP level (baseline, USD) up from section 16, so that 12d reads it from above;
- add the exchange rate and nominal GDP in local currency (WEO data, needed by Distribution).

The % of GDP rows use baseline GDP, which is data. Adjusted GDP would be circular, because the GDP effect depends on revenue; 16b may use adjusted GDP, since the GDP effect does not read the external balance.

#### 6.2 Downstream modules on their own sheets

They have the same column-group geometry as `Mitigation` (NORMS 3c rule 4). They read `Mitigation` rows of their group directly, and the baseline through their own `.ref` rows (NORMS 3c rule 6).

| Module sheet | Reads from Mitigation | On the module sheet only | Data sheets |
|---|---|---|---|
| `AirPollution` | Section 15 `aps` (all pollutants incl. CH4, by source group); power and residential energy use (3, 6); GDP; CO2 total (13); forcing (15); revenue (12) | Baseline `.ref` rows, concentrations, risks, deaths, valuation, unit damages | WB, GBD, IHME, ILO, ExposureCoefs, IF PP, ConcMat, Air_Data |
| `Distribution` | GDP, GDP effect, exchange rate, nominal GDP (header, 16); population; carbon price (1); revenue % of GDP and revenue by fuel (12d); grid intensity (13b); after-tax prices by subsector × fuel (3, 5-8); fuel use (11); US CPI (header) | % price change and % consumption change by subsector × fuel (one price per cell, so a pure price change); incidence | GTAP IO table and mapping, household surveys |
| `TransportExternalities` (later) | Road fuel use, VKT, fuel economy by class (5b); GDP growth | Margins, shares, accidents, congestion, road damage | Transport data |

The module results flow back into section 18 (co-benefits, unit damages) through rows on the module sheet, which section 18 reads by code. This is the one cross-sheet read into `Mitigation`; it is not circular, because the modules do not read section 18.

#### 6.3 Output sheets

- Each addition puts its headline rows into `MTOutputs` (and so into `StoredResults` and `ScenarioCompare`).
- The legacy price-breakdown chart (F5f) and the legacy Dashboard become `Charts` content.
- The legacy cross-check tests and the legacy MTOutputs layout are not carried over.

#### 6.4 Order

| Version (proposed) | Content |
|---|---|
| v3.9 | Section 2 memo: average prices, price indices, mix effect (I31) |
| v3.10 | Fuel-use shock and jet fuel (I22, I19); they move every result |
| v3.11 | Section 15 input table: `aps.ch4.*`, `aps.*.all`, legacy order |
| v3.12 | Header rows (GDP level up, exchange rate, nominal GDP); section 12 consolidation and 12d fiscal reports |
| v3.13 | Sub-blocks 11b, 13b, 14b (energy and CO2 changes, energy balance, grid intensity, Kaya, GHG by broad sector) |
| v3.14 | Section 17 Carbon pricing |
| v3.15 | Sub-block 16b External balance (import data) |
| v3.16 | Section 18 Welfare, climate part (SCC data) |
| later | Memos in 3 and 16a; NDC in 14b; vehicle revenues in 12b; module sheets (air pollution, distribution, transport externalities) and their feedback into 18 |

## 2. Legacy fuel-use equations by subsector against the MVP: survey (Sector_Equations_Survey)

Source: legacy `CPAT 1.0pre_456_NoPropData.xlsb`, sheet Mitigation, baseline block rows 2173-8503 (formulas with defined names restored: recovered with `tools/xlsb_*.py`, cached Egypt values from the xlsb). The policy block (+6331 rows; +6320 from the industry block on) was compared row by row after normalising references. Every fuel-use equation is structurally identical to its baseline row. The only exceptions are the baseline-only iron & steel memo rows 5667-5676/5714/5727-5728, which nothing references. MVP: `build_v7_0.py` (`calc_formula` var `enel`, LAMBDA `FUELUSE`, `build_inputs`, `SUBSECTORS`, `FUELS`, `LEGACY_DIFFS`), `Equations_v7_0.md` E69, `data/energy_use.csv`, `data/elasticities.csv`.

### 1. The legacy standard form and its drivers

Standard row (e.g. 5399 road diesel, M column = 2023):

```
Q = L * (1+M2446)^(εY*M2433) * (1+M2439) * (P/P0)^εU * [ ((P+Sh*cov)/(P0+Sh0*cov0))^εF / (1+α+$M<addeff>) ]^(1+εU)
```

This is algebraically E69 plus four extra terms: the income factor M2433, the shock (1+M2439), the additional efficiency $M2199/2200/2201, and the shadow price × sector coverage. The MVP's shadow price is the sector shadow price × EF, which is equivalent.

| Driver row | Label | Egypt cached values | In the MVP? |
|---|---|---|---|
| 2446 | Post-policy GDP growth (= 2444 + 2445) | 6.7% (2022), 3.8% (2023), 2.4% (2024), 4.4%, ... 4.3% (2040) | Yes: row 7 `gdp.pos.pct` (with the L24 feedback fix) |
| 2433 | Income factor: "Discount factor (proportion of estimated to average calibrated income elasticity)" = est. elasticity(GDP pc)/0.74, switch IncElAdj = Yes* | 1.027 (2023), 1.021, 1.017, 1.008, 1.001, 0.992 (2028) ... 0.947 (2040) | **No** in fuel blocks (used for power demand only, E136 `incf`) |
| 2439 | Exogenous shock on energy consumption (= row 483, the "Covid factor") | −20.81% (2023), +9.24% (2024), 0 afterwards | **No** (power: switch Settings C19, off) |
| 2440 | (blank row) | empty → 0 | n/a. Used by other energy use **by mistake** |
| 2199 / 2200 / 2201 | Additional efficiency: road vehicles / residential / industrial (= MTInputs F243/F244/F245) | 0 / 0 / 0 (baseline and policy block 8530-8532) | No (documented "Not yet") |
| 2259 | Exemption-phaseout factor of **coal** (sector coverage table) | 0 | n/a. Used by road "other biofuels" **by mistake** |
| 2271-2286 | New-policy coverage per sector (rod 2271, ral 2272, nav 2273, avi 2274, res 2275, foo 2276, srv 2277, mch 2278, irn 2279, ..., oen 2286) | 0 in the baseline | Price block (`nce`, sector coverage) |
| 2377-2388 | Shadow price $/GJ: coal res 2378 / ind 2379; gas res 2381 / ind 2382; gso 2383, die 2384, lpg 2385, ker 2386, oop 2387, bio 2388 | 0 (baseline) | `shp` = sector shadow price × EF |
| 2404-2419 | Share of shadow price on efficiency by sector (rod 2404 ... oen 2419) | 0 (baseline) | in `shpx` |
| 2473, 2512 | blank row / "coal ind new excise tax" (= 0) | 0 | n/a. Used as "shock" in avi/nav renewables **by mistake** |
| 2258 | Years since carbon-price introduction (counter) | 0 → 1, 2, ... from CPIntro | only in the dead "initially exempted" rows |
| MTInputs F326 BiomassNormal | Biomass is a normal good | **No** (Egypt) | No |
| MTInputs F325 BiomassLeakage | Leakage to biomass (row 1785, E1785 = 0) | No | No |
| MTInputs F268 AlwaysExemptResLPGKer | Residential LPG/kerosene always exempt (price rows 5546-5547) | No* | No |

Elasticity names: `_el_inc|_el_dem|_el_eff_<fuel>_<grp>`, `_eff_imp_<fuel>_<grp>`. The groups are `rod` (all transport), `res`, `srv`, `ind`, and the fuels are coa, nga, gso, die, oil (lpg, ker, oop), bio, ren. AEEI for gso/die is `oil`. These values match `data/elasticities.csv` (tra = rod) for LMIC, and the MVP's fuel/AEEI mapping is the same, with one exception: food & forestry, see below.

### 2. Inventory by subsector × fuel

Notation: **STD(g=2446, inc=2433, shock=2439, add=…)**, the standard form above. Price rows: coal/gas use residential prices (2490/2559) for rod and res, and industry prices (2513/2582) elsewhere. This matches the MVP's `SUBSECTORS` price sector.

Classes:
1. Legacy bug.
2. Legacy feature not in the MVP.
3. MVP difference already documented in LEGACY_DIFFS.
4. Undocumented MVP difference.
5. No effect for Egypt or dead code.

Every row below also carries the common differences C1-C3, which are not repeated in each row:

- **C1, shock (1+M2439).** Class 3, documented as "Covid factor", but the documented effect "Small" is wrong.
- **C2, income factor M2433.** Class 4.
- **C3, additional efficiency $M2199/2200/2201.** Class 3 / 5.

| Subsector | Fuel(s) | Legacy rows | Legacy form and drivers | Differences vs MVP E69 | Class | Egypt effect |
|---|---|---|---|---|---|---|
| Road (elasticity) | coa, nga, gso, die, lpg, ker, oop | 5396-5402 (prices 5382-5388; "used" rows 5428-5434 with TrModel switch) | STD, add = 2199 (road vehicles); shadow coa 2378 / nga 2381 (res rows) × cov 2404; elasticities `_rod` (lpg/ker/oop = oil) | C1-C3 only. TrModel switch = MVP ROADSWITCH | 3/4/5 | gso 6126, die 8102, nga 457 ktoe (2023) carry C1: −20.8% 2023, −13.5% from 2024 |
| Road | bgs, bdi | 5404-5405 (5436-5437) | Share rows: L × gso(t)/gso(t−1), resp. die | MVP: biofuels separate, scale with engineer model | 3 | 0 (no road biofuels) |
| Road | obf | 5406 (5438) | **Non-standard**: uses bioethanol price 5390 (obf price row 5392 empty), adds ((P+Sh·cov)/(…))^εU (shadow price through the usage elasticity), efficiency term (M5390/M5390)^εF ≡ 1, and `$M2259` (coal exemption-phaseout factor) as additional efficiency | Bug in structure, price row and add-eff row | 1 / 5 | 0 |
| Road | ren | 5407 | STD without shadow price: ((P/P0)^εF/(1+α+$M2199))^(1+εU) | MVP has no self-generated renewables | 5 | 0 |
| Road | memo power | 5408 (5440) | = L (flat) or engineer EV demand | MVP: power memo, power sector | – | – |
| Rail | all 8 + ren | 5458-5466 (prices 5447-5455, cov 2272) | STD, add = **2199 (road vehicles)**; `_rod` elasticities; shadow coal/gas = industry rows 2379/2382, cov 2405 | C1-C3 only (MVP elasticity group `tra` = legacy `rod`) | 3/4/5 | 0 (no rail fuel use) |
| Domestic aviation | coa, nga | 5483-5484 | **Swapped**: (1+M2439)^(εY·M2433) × (1+M2446) × … × **(1+M2439)** again: the shock is applied twice and GDP growth has elasticity 1 | Bug; MVP standard | 1 / 5 | 0 |
| Domestic aviation | gso, die, lpg, ker, oop, bio | 5485-5490 | Swapped: (1+shock)^(εY·incf) × (1+g) (GDP elasticity 1, shock damped) | Bug | 1 / 5 | 0 |
| Domestic aviation | ren | 5491 | Swapped and the "shock" is (1+**M2512**) (coal-industry new excise, 0); no shadow price | Bug | 1 / 5 | 0 |
| Domestic aviation | **jfu (jet fuel)** | 5492 | Swapped form; εY = `_el_inc_die_rod` (0.6, diesel!) applied to the shock only; growth (1+g)^1; εU, εF, α = oil/rod; price = **kerosene** price 5477, shadow = kerosene 2386 × cov 2406 | **MVP has no jet fuel at all**: `extract_data_v7_0.py` FUELS has no `jfu`, so `energy_use.csv` gives avi ker = 0 and the MVP's domestic aviation is empty. `legacy_compare_v7_0.py` also leaves jfu out, which hides the gap. Only the CH4/AP factor mapping `('avi','ker') → jfu` hints at the intended mapping | **4** (MVP); legacy form **1** | **Large**: 707 ktoe (2022), 652 (2023), 826 (2028), 1,308 (2040); legacy CO2 tra.avi 1.95 Mt (2022), ~3.6 Mt (2040) missing from the MVP. With the swap fixed (standard form, εY 0.6, full shock) legacy jet would be ×0.90 (2023), ×0.82 (2030), ×0.68 (2040). Legacy vs an MVP-style oil εY 0.8 with no shock/incf: ×0.87 (2023), ×0.98 (2030), ×1.07 (2040) |
| Domestic navigation | coa-bio | 5508-5515 (cov 2273/2407) | STD, add = 2199; `_rod`; shadow coal/gas industry rows | C1-C3 only | 3/4/5 | oop 291 → 225 (2023) → 664 (2040); C1 −13.5% level |
| Domestic navigation | ren | 5516 | STD without shadow price; "shock" = (1+**M2473**) (blank row) | Bug | 1 / 5 | 0 |
| Residential | coa, gso, die, oop | 5553, 5555, 5556, 5559 | STD, add = 2200 (residential), `_res` elasticities, shadow coal 2378 × cov 2408 | C1-C3. **5559 oop uses the biomass price M5549/L5549** (should be 5548) | 3/4 + 1 (oop) | coal 1.3 ktoe; oop 0 |
| Residential | nga, lpg, ker (totals) | 5554, 5557, 5558 = not-exempt + initially-exempt + SUM($M change:M change) | Not-exempt 5564-5566: STD (add 2200) **minus** the leakage change (5577/5583/5588). Initially exempt 5568-5570: (1+g)^εY **without** M2433, εU × MIN(years since CP/ExemptPhaseoutPeriod, 1), otherwise STD | MVP: one STD row. The initially exempt rows start from IFNA(IF($L$1784=B, $K$1795 x base, 0), 0) (L5568:L5570, read from the .xlsb): the split is live but 0 in Egypt (ExemptMostCook off), so total = not-exempt row = STD | 5 (dead), 1 (no incf in exempt rows) | nga 1,703, lpg 2,494, ker 2.3 ktoe (2023) = STD with C1 |
| Residential | bio | 5560 = 5567 + 5593 | 5567: L × **IF(BiomassNormal="Yes", (1+g)^(εY·incf), 1)** × (1+shock) × price/efficiency terms (add 2200). Egypt BiomassNormal = **No**: no GDP growth at all | MVP always grows biomass with GDP (εY bio res 0.1) | **2** (undocumented) | Legacy 1,261 (2023) falls to 1,309 (2040); MVP-style income term gives ≈ +4% (2025: ×1/0.990), +3.5% (2030: ≈ +48 ktoe), +8% (2040: ≈ +108 ktoe) |
| Residential | leakage to biomass | 5571-5593 | Most-used cooking fuel (L1784 = lpg); fossil change = −L(not-exempt) × fuel efficiency × ((1+Δtax/P)^(E5572/E5571) − 1) × E1785; biomass gain = −BioEff × Σ equivalents × E1785 | Not in the MVP. Bugs: (a) the not-exempt rows subtract the change (5564 `−M5577`) while the totals add it back cumulatively (`SUM($M5577:M5577)`), so the fossil total is not reduced consistently while biomass rises; (b) kerosene uses the LPG price base L5546 (5587) and the LPG transfer share M5582 (5588), and there are two "Change in kerosene" rows (5588 feeds the total, 5590 feeds the biomass equivalent); (c) E1785 applied twice (harmless 0/1) | 2 + 1 / 5 | 0 (BiomassLeakage = No) |
| Residential | lpg, ker price | 5546-5547 | Policy part dropped if AlwaysExemptResLPGKer = "Yes" (test without the `*` of the default strings) | Price-side feature not in the MVP | 2 / 5 | 0 (No*) |
| Residential | ren | 5561 | STD without shadow price | MVP has no ren | 5 | 0 |
| Food & forestry | coa-bio | 5609-5616 (cov 2276/2409) | STD, add = **2201 (industrial)**, `_ind` elasticities, shadow industry rows | MVP uses services elasticities (LegacyDiff "Elasticities: food & forestry", decision). Additional efficiency group industrial vs (MVP none) | 3 | die 726 ktoe (2023) → 1,209 (2040): eps ind die (0.5/−0.7/−1.2) vs srv (0.5/−0.5/−0.4) |
| Food & forestry | ren | 5617 | STD without shadow price | – | 5 | 0 |
| Services | coa-bio | 5634-5641 (cov 2277/2410) | STD, add = **2201 (industrial)**, `_srv` elasticities; shadow coal/gas = **residential** rows 2378/2381 while the price is industry (2513/2582) | C1-C3; shadow EF res (MVP EF sector res, consistent) | 3/4/5 | 0 (no services fuel use) |
| Services | ren | 5642 | STD without shadow price | – | 5 | 0 |
| Industry: mch, irn, nfm, mac, cem, omn, cst, ftr | coa-bio | 5691-5698, 5716-5723, 5743-5750, 5768-5775, 5793-5800, 5818-5825, 5843-5850, 5868-5875 | STD, add = 2201, `_ind`, shadow industry rows × cov 2411-2418 | C1-C3 only | 3/4/5 | Large volumes (ftr nga 6,394, omn die 2,993, cem nga/coa 1,499/1,191, irn nga 1,432 ktoe, 2023): C1 −13.5% level |
| Industry | ren | 5699, 5724, … 5876 | STD without shadow price | – | 5 | 0 |
| Iron & steel memo | – | 5667-5676, 5714, 5727-5728 | Weighted average price/elasticity multiple; 5667 reads **N2446** (next year's growth). Referenced nowhere | – | 5 (dead; would be bug) | 0 |
| Other energy use (oen) | coa-bio | 6077-6084 (prices 6066-6073, cov 2286/2419) | (1+M2446)^(εY·**M2440**) with M2440 a **blank row** → no GDP growth at all; **no additional-efficiency term**; `_ind` elasticities; shock applied. Price row 6072 (oop) lacks the IF(cov=0, retail) branch of the other sectors | MVP grows oen with GDP (εY oil ind 0.8): it silently "fixes" the bug, but this is not documented | **1** + **4** (document) | oop 101 (2022) → 75 (2023) → 140 (2040) legacy; the income term alone is ×1/0.759 (2030, ≈ +46 ktoe) and ×1/0.532 (2040, ≈ +124 ktoe) |
| Other energy use | ren | 6085 | Same, but with $M2201; total 6087 excludes ren (6086 includes it) | – | 5 | 0 |

#### Quantified common terms (Egypt, legacy GDP path, ceteris paribus; legacy level / MVP-style level)

| Term | 2023 | 2024 | 2025 | 2030 | 2035 | 2040 |
|---|---|---|---|---|---|---|
| C1 shock (all STD rows) | 0.792 | 0.865 | 0.865 | 0.865 | 0.865 | 0.865 |
| C2 income factor, εY = 0.5 | 1.0005 | 1.0007 | 1.0011 | 1.000 | 0.995 | 0.990 |
| C2 income factor, εY = 0.8 | 1.0008 | 1.0012 | 1.0018 | 1.000 | 0.992 | 0.984 |
| C2 income factor, εY = 1.0 | 1.001 | 1.0015 | 1.0022 | 1.000 | 0.990 | 0.980 |
| Res. biomass, BiomassNormal = No (εY 0.1) | 0.996 | 0.994 | 0.990 | 0.966 | 0.944 | 0.924 |
| oen, blank income factor (εY 0.8) | 0.971 | 0.953 | 0.921 | 0.759 | 0.632 | 0.532 |
| Jet fuel, swapped form vs εY 0.8 no shock | 0.873 | 0.925 | 0.933 | 0.979 | 1.025 | 1.071 |

C1 is by far the largest equation difference. It lowers all legacy fuel use (about 57,000 ktoe excluding power in 2030) by 13.5% from 2024 onwards, about 8,800 ktoe in 2030. On its own it explains more than the +8% gap of the "prices to 2022" comparison in `legacy_comparison_v6_4.md`. The `LEGACY_DIFFS` row "Fuel-use equation" gives the effect as "Small", which is wrong.

### 3. Summary of differences by class

| # | Difference | Class | Documented? | Egypt effect |
|---|---|---|---|---|
| D1 | Jet fuel (domestic aviation, 707 ktoe in 2022) missing from MVP data/model | 4 | No | Large: −0.65 to −1.3 Mtoe, −1.9 to −3.6 MtCO2/yr |
| D2 | Exogenous shock 2439 (−20.8% 2023, +9.2% 2024) on every fuel row | 3 | Yes ("Covid factor"), effect mis-stated "Small" | −13.5% level from 2024 on all fuel use |
| D3 | Income factor 2433 on εY (fuel blocks) | 4 | No (only power E136 / L3) | +0.1-0.2% 2023-25, −1 to −2% by 2040 |
| D4 | Additional efficiency 2199 (rod, ral, avi, nav), 2200 (res), 2201 (foo, srv, industry, oen ren), none for oen fossil | 3 | Yes ("Not yet") | 0 (inputs 0) |
| D5 | Aviation: GDP growth and shock swapped, double shock for coal/gas, jet εY from diesel | 1 | No | Jet ×0.87-1.07 vs MVP-style (see table); coal/gas 0 |
| D6 | Other energy use: blank income-factor row 2440, no GDP growth; no additional efficiency | 1 (+4 for documentation) | No | MVP +46 ktoe (2030), +124 (2040) vs legacy |
| D7 | Residential biomass: BiomassNormal switch (Egypt No, so no income growth) | 2 | No | MVP +48 ktoe (2030), +108 (2040) |
| D8 | Residential exemption split (not-exempt / initially-exempt rows, phase-out of the usage elasticity) | 5 (dead: the initial exempt share is a NoPropData stub, cached 0; ExemptMostCook never reaches Mitigation, L92) | Yes (LegacyDiff "Exemption phase-out", not built) | 0 |
| D9 | Residential leakage to biomass (switch BiomassLeakage) incl. bugs (a)-(c) | 2 + 1 | Yes (v5.1: section 6b; L45, L90, L91 fixed; LegacyDiff "Residential leakage") | 0 (switch No) |
| D10 | Residential oop uses the biomass price | 1 | No | 0 |
| D11 | Road other biofuels: wrong price, shadow price via εU, efficiency term ≡ 1, coal-exemption row as add. efficiency | 1 | No | 0 |
| D12 | Self-generated renewables: no shadow price; avi/nav ren shock rows 2512/2473 | 1 / 5 | – | 0 (MVP has no ren; Egypt ren 0 outside power) |
| D13 | Road bgs/bdi follow gasoline/diesel | 3 | Yes ("Road transport: biofuels") | 0 |
| D14 | Food & forestry elasticities ind (legacy) vs srv (MVP) | 3 | Yes (decision v0.11) | Food & forestry diesel response |
| D15 | Services/rail/aviation/navigation coal and gas shadow price rows (res vs ind EF) | 5 | – | 0 (no coal/gas use; shadow 0 in baseline) |
| D16 | Res LPG/ker price switch AlwaysExemptResLPGKer (string test "Yes" never matches starred defaults) | 2 / 1 (low) | Yes (v5.1: rows exf, starred test fixed; LegacyDiff "Residential LPG and kerosene always exempted") | 0 (switch No*) |
| D17 | Iron & steel memo rows (5667 uses next year's growth N2446), unused | 5 | – | 0 |
| D18 | oop price rows: IF(coverage = 0, retail price 2681, pre-policy 2697 + policy × coverage) in every sector except oen | to check (price block) | – | 0 in baseline |

### 4. Recommended actions

**MVP fixes**

1. **D1 (high): add jet fuel.**
   - Extract `jfu` from Data_Energy column `avi` (707 ktoe) and map it to `avi|ker`, which already uses the jet CH4 and pollutant factors. Alternatively, add a fuel `jfu` that uses the kerosene price.
   - Check the CO2 EF for jet kerosene.
   - Add `jfu` to `legacy_compare_v7_0.py` so the transport comparison includes it.
   - Decide on εY: oil/tra 0.8 (MVP mapping) or die/tra 0.6 (legacy name). Document either choice.
2. **D2: correct the LegacyDiff "Fuel-use equation" row.**
   - Name the shock (row 2439 = row 483, −20.8% in 2023 and +9.2% in 2024).
   - Give the real effect: −13.5% level on all legacy fuel use from 2024.
   - Consider letting Settings C19 switch the shock into FUELUSE as well, for like-for-like legacy checks.
3. **D3: apply the income factor `incf(t)` in FUELUSE** (exponent εY × incf). The data is already in PowerPaths, and it makes fuels consistent with E136. The alternative is to add a LegacyDiff row. *Done in v4.12 (user decision 2026-10-18, issue I23 closed): Mitigation row 14 = (1 + g)^incf − 1 feeds every fuel row; Egypt fuel use outside power +0.1% in 2025, −0.9% in 2040.*
4. **D6: add a LegacyDiff and a bug entry.** Legacy other energy use has no GDP growth because the income-factor row 2440 is blank. The MVP grows other energy use with GDP; mark this as a bug fix.
5. **D7: decide on `BiomassNormal`.** Either add a switch (Egypt: No, meaning residential biomass has no income growth) or document the difference as a decision. *Done in v4.13 (I24): MTInputs `BiomassNormal`, scenario 1 (Settings C53), as legacy.*
6. **D4: extend the LegacyDiff text with the legacy grouping**, for when additional efficiency is built: road vehicles → rod, ral, avi, nav; residential → res; industrial → foo, srv, industry; none for oen. *Built in v4.13 with this grouping; other energy use takes the industrial gain on every fuel (legacy bug L66).*

**Features to add later (legacy features, no Egypt effect today)**

- Residential leakage to biomass (D9), with the bugs fixed: subtract the fossil change once, use the kerosene rows for kerosene, conserve the substituted energy. *Done in v5.1: section 6b (`Equations_v7_0.md` 4a); legacy bugs L45, L90, L91 fixed; the legacy design kept (most-used cooking fuel only, coefficient σ e_b / e_m / lag capped at 1, reversible, permanent level shift, efficiency-weighted fossil change: issue I51).*
- The AlwaysExemptResLPGKer price switch (D16). *Done in v5.1: Section-1 rows `AlwaysExemptResLPGKer` (per scenario) and `exf`, Inputs column `exg`; no new carbon tax, ETS or excise (nor their VAT) on residential LPG and kerosene; the starred test fixed (LEFT(x, 3)); issue I50.*
- Self-generated renewables (D12).
- The exemption phase-out demand split (D8) only if exemptions by demand share are wanted; it is inactive in legacy.

**Legacy bug register (proposed new IDs after L41)**

- L42 (Medium): domestic aviation rows 5483-5492. GDP growth and shock are swapped (GDP elasticity 1; the shock carries εY × incf), coal and gas get the shock twice, and jet fuel takes the diesel income elasticity.
- L43 (Medium): other energy use rows 6077-6085. The income factor points to blank row 2440, so there is no GDP growth; rows 6077-6084 have no additional-efficiency term.
- L44 (Low): residential other oil products row 5559 uses the biomass price (5549 instead of 5548).
- L45 (Low): residential leakage block 5574-5593 has the sign and cumulation inconsistency between 5564 and 5554, uses LPG price and share rows for kerosene (5587, 5588), and has duplicate kerosene change rows.
- L46 (Low): road other biofuels row 5406. It uses the bioethanol price, applies the shadow price through εU, has an efficiency term ≡ 1, and uses M2259 (coal exemption phase-out) as additional efficiency.
- L47 (Low): self-generated renewables in aviation/navigation (5491, 5516) take the shock from rows 2512 and 2473.
- L48 (Low): residential "initially exempted" rows 5568-5570 have no income factor (the split itself is live, 0 in Egypt with ExemptMostCook off). The AlwaysExemptResLPGKer test misses the starred defaults.
- To check (price block): other oil products price rows jump from the retail price (coverage 0) to the pre-policy price + policy × coverage (coverage > 0); oen lacks the branch.

## 3. Legacy downstream results processing after the two scenario blocks: survey (Downstream_Survey)

Survey of the legacy workbook `CPAT 1.0pre_456_NoPropData.xlsb` (Egypt, cached values), Mitigation rows 14770-19227 and the sheets that read Mitigation. Formulas come from the legacy xlsb with defined names restored (`tools/xlsb_*.py`). Cross-references come from a scan of every formula and every chart series in the formula xlsx. Egypt values are shown as 2023 / **2030** / 2039 (columns M / T / AC), with the year of each column starting at L = 2022. Units are the legacy units.

Helper outputs of the survey (cross-reference table, row digests of blocks E and F) were scratch files and are not kept.

---

### 0. Overview

| Block | Rows | Role | Main consumers |
|---|---|---|---|
| C (baseline) | 2173-8503 | Scenario 1 (`C2173`=1) | everything below |
| D (policy) | 8504-14769 | Scenario 2 (`{ScenarioNum}`), a full copy offset by +6331 | everything below; CBAM (8578-8583) |
| **E** | 14770-16080 | "Results for other modules": hand-off tables, by code lookup | Distribution, Transport, Air pollution |
| **F** | 16081-19032 | "Results for charts": 16 report sections | Dashboard (about 75 charts), MTOutputs (legacy), NDCs, GHGs, Transport3 |
| **G** | 19033-19218 | "Results for other purposes": intermediate prices and markups; energy-balance matrix | MTOutputs (legacy) |
| H | 19219 | `NotesRow` anchor | |

**How the lookups work (E, F, G).** Almost every row builds a code in column G: country, then `.mit.<var>.<sector>.<fuel>.`, then a scenario number. The scenario number is `$F$224`=1 for the baseline or `$G$224`=`{ScenarioNum}`=2 for the policy (sometimes `$C$2173` or `$C$8504`). Column J does `MATCH(G, $H$2173:$H$14770, 0)`, and the year columns do `INDEX(L$2173:L$14770, $J, 0)`. So E, F and G mostly re-arrange the code-indexed scenario rows. Real computation happens only in some F sections: prices, welfare, subsidies, balance of payments (BoP), NDC and Kaya. Only two scenarios are ever live: the policy block holds whichever scenario is selected (the legacy re-runs a scenario by swapping its number).

**The flow is not one-way.** F reads results back from the downstream sheets and from the legacy MTOutputs sheet:
- `'Air pollution'!K3217`, `K3731:K4382` (mortality and air-pollution unit costs)
- `Transport!I322:I364` (accidents, congestion, road damage)
- `SCC!F8:F687` (Ricke national social cost of carbon)
- `NDCs!C39/C41`
- `MTOutputs!K7` (carbon price), `K34` (GDP), `K60` (policy GHG in the target year)

The chain Mitigation E → Air pollution / Transport → Mitigation F is therefore a cross-sheet loop. MTOutputs reads F, and F reads MTOutputs in three places.

---

### 1. Block E: hand-offs to other modules (14770-16080)

#### E1. For the Distribution module (14771-15720)

**Consumer.** `Distribution` sheet: 2,166 references into E, plus F 16209-16343 (prices).

**Inputs pulled from the scenario blocks:**

| Rows | Content | Scenarios and units |
|---|---|---|
| 14774-14785 | Baseline real GDP growth and levels; "Effect on GDP" (`mit.gdp.cha.pct.2`); adjusted GDP (= baseline × (1+effect)), in LCU and in USD; exchange rate; population | — |
| 14786 | Carbon price trajectory (`mit.cptraj.2`) | Egypt 2030: 50 $/t |
| 14787-14789 | Total revenues as % of GDP, baseline and policy (`mit.rev.new.pct`), and the difference | Egypt 2030: -2.51% → -0.71%, +1.80 pp |
| 14790-14795 | Power emission factor in t/MWh (baseline 0.322, policy 0.308); baseline gasoline, diesel, kerosene and LPG totals | — |
| 14798-15004 | Post-tax prices (`atp`) by 17 subsectors (pow, rod, ral, nav, avi, res, foo, srv, mch, irn, nfm, mac, cem, omn, cst, ftr, oen) × 10 fuels | baseline |
| 15005-15211 | The same price grid | policy |
| 15212-15419 | Percent price change, policy/baseline − 1, by subsector × fuel. Electricity res/ind from F 16356/16279 | — |
| 15421-15630 | Percent consumption change, by subsector × fuel | — |
| 15631-15641 | Baseline fiscal revenue by fuel (`mit.exp.<fuel>.usd.1`), real US$bn | — |
| 15643-15646 | US inflation index (WEO) | — |
| 15647-15720 | GTAP country code and the GTAP IO table by sector (exports, household, imports, output, total demand) mapped to CPAT codes | — |

At 15720 there is a GTAP-to-WEO GDP adjustment: Egypt +36.6%. It is reused in F 18762 (industry gross value added, GVA).

**Computation.** Almost none: ratios and lookups. Distribution does the incidence (budget shares, IO price pass-through).

**Issues:**
- 14792-14794 take the scenario from `C2173` while 14795 uses `B14795` (inconsistent, harmless).
- The GTAP block has `#N/A` in C15652+ in the cached file. Only the first row is a dynamic array, `TRANSPOSE({IOCols_NEW})`, which spills.

#### E2. For the Transport module (15722-15823)

**Consumer.** `Transport` sheet: 925 references, plus F 16166/16173 (GDP growth).

**Content:**
- **Fuel use by vehicle class**, in billion litres, from the road engineer rows: gasoline passenger and 2-3 wheeler; diesel passenger and freight; LPG and natural gas passenger and freight; electricity.
- **Efficiency and driving margins** (15736-15745). These are the elasticities `_el_eff_*_rod` and `_el_dem_*_rod`, blended by freight share.
- **Road and total consumption by fuel**, baseline (15759-15769) and policy (15771-15781).
- **Shares**: freight share and transport share of each fuel (15783-15801).
- **VKT and fuel economy** (rows 15803-15823).

**Issues:**
- Rows 15771-15775 are labelled "baseline" but hold the policy values (B=2).
- LPG margins (15740-15741) and the LPG freight share (15786, 15796) are `#DIV/0!` when Egypt's road LPG is 0.
- "Road diesel - efficiency margin" is a gasoline/diesel blend weighted by passenger/freight litres, not a diesel margin.
- See also `Transport_Legacy_Survey_v7_0.md`: E pulls the engineer-model outputs even when the elasticity switch is on.

#### E3. For the Air pollution module (15825-16078)

**Consumer.** `Air pollution` sheet: 3,948 references into E, plus 8,950 into block A/B data.

**Content:**
- Baseline GDP.
- Energy use of the power sector (4 fuels) and the residential sector (6 fuels), baseline and policy.
- Emissions of 10 pollutants (NOx, SO2, BC, POM, OPM, VOC, CH4, CO, PM2.5, OC) for 8 source groups: coal, gas and other power plants (cpp, gpp, opp); ground-level transport (rod); ground-level other (gro: residential, services, food); other industry (oth); food and agriculture (foo); all. Baseline (15859-15961) and policy (15963-16065).
- Total CO2 and GWP100 of the non-CO2 gases (16067-16073). Egypt 2030 CO2: 232.3 → 190.2 Mt.
- Total fiscal revenue, baseline and policy, $bn (16075-16078). Egypt 2030: -19.40 → -5.49.

**Issues:**
- The `oc` rows use the range `$L$2173:$L$15266` (inconsistent, harmless).
- The food/agriculture pollutants are tiny next to the others (NOx 1.2 against about 1e5 for other groups), so their units look different. Methane for foo is 2.2e6. Check the units.

---

### 2. Block F: report sections (16081-19032)

Each heading below gives the legacy section number, its rows, and its downstream consumers.

#### F1. Testing cross-checks (16082-16084)
The test row `egy.mit.tests.2` is looked up from the policy block. **Consumer:** none outside.

#### F2. Macro drivers (16086-16125)
**Consumers:** Dashboard charts 24-26, legacy MTOutputs.

**Content:**
- International energy prices (from rows 704-706).
- Baseline GDP and population growth.
- Income elasticities of energy demand (sector averages × the per-capita adjustment `mit.inc.ela.adj`).
- Implied income elasticity of CO2, baseline and policy (16112-16113).
- **Price elasticity tables** (16117-16122), before and after the rebound effect: `dem + eff + dem×eff`.

**Bugs:**
- Every sector column of the price-elasticity table (Road, Rail, Navigation, Aviation, Residential, Industries) uses the `_rod` (road) elasticities. The table is wrong for all sectors other than road. It is display only.
- The implied income elasticity of carbon (16112) gives -2.3 in 2023 and 5.1 in 2024 (noise from year-on-year ratios). Display only.

#### F3. Policy coverage (16127-16157)
**Consumers:** Dashboard charts 3, 5, 23; legacy MTOutputs rows 6-14.

**Content:**
- Carbon tax in the year of interest (`{YearFuelPrices}`).
- Emissions coverage (`mit.co2cov.2`). Egypt 2030: 98.8%.
- Carbon tax trajectory (`mit.cptraj.2`, `RealPriceTrajectory`).
- Effective carbon tax = trajectory × coverage. Egypt 2030: 49.4.
- "Needed for 2°C" bands: 40 and 80 $/t (2017 prices) × the 2017→2021 deflator. These are hardcoded values.
- ETS price shown only if `ETSOnDash`.
- Revenue-recycling shares (labour tax 30%, public investment 50%, transfers 20% for Egypt).
- Sector contributions to covered CO2: power 39.8%, transport 24.1%, residential 6.3%, industry 28.5%.

**Issues:** row K16135 holds the hardcoded row offset `=J16135+1729`.

#### F4. GDP effects (16160-16201)
**Consumers:** Dashboard charts 32, 33, 46, 144; Transport (16166, 16173); legacy MTOutputs 16-22, 33-35.

**Content:**
- **Growth decomposition** (16166-16173): baseline growth, the effect of the scenario, and the GDP effects of each revenue use (personal income tax, public investment, current spending, transfers). Codes `mit.gdp.{pre,exc,pit,inv,cur,tra,tot}.pct`.
- Policy growth = sum of the above. Difference vs baseline: Egypt 2030 -0.07 pp; 2039 +1.07 pp.
- **Year-of-reform profile** (16180-16195): the impulse of year k of the reform, `mit.gdp.yrK.pct`, read with a moving column offset. Net effect 2039: +0.91%.
- **GDP levels** (16197-16201): baseline 771.8 against post-policy 771.6 $bn in 2030 (-0.2); 2039: 1155 against 1165.

**Issues:**
- The growth rows only fill in when `GDPEndogenous="Yes*"`.
- The year-profile lookup range ends at `$H$14595` (other rows use 14770).

#### F5. Energy prices (16204-16725)
**Consumers:** Distribution (16209, 16281-16343); Dashboard charts 56-59, 64, 145; legacy MTOutputs 144-271.

**(a) Price components by fuel and sector (16206-16291), baseline.** Codes `sp` (supply cost), taxes, VAT, carbon and `rp` (retail) for electricity ind/res, coal/gas × pow/res/ind, other oil products, gasoline, diesel, LPG and kerosene.

**(b) Consumption-weighted average prices** (16293-16352), baseline and policy. Coal and gas are weighted over power, residential and industry. Electricity is weighted by industry and buildings demand (17073-17082).

**(c) Price change, policy against baseline** (16354-16386). Egypt 2030:

| Fuel | Change |
|---|---|
| Electricity | +25.7% |
| Coal | +55% |
| Gas | +71% |
| Oil | +104% |
| Gasoline | +19% |
| Diesel | +28% |
| LPG | +59% |
| Kerosene | +30% |

The policy prices are indexed to 2022 = 100 (16387-16402).

**(d) "Total carbon price" per fuel and sector** (16408-16656). The net tax or subsidy per unit (taxes + subsidies, read from two adjacent scenario rows) is converted to $/tCO2 with `_conv_ktoe_to_gj`/EF. It is then averaged with consumption weights: by fuel, then economy-wide.

| Total carbon price, $/tCO2 | Egypt 2030 |
|---|---|
| Baseline | -85 (net subsidy) |
| Policy | -35 |
| Policy, 2039 | +78 |

This is the implicit carbon price of existing taxes and subsidies.

**(e) Effective carbon rate (ECR)** (16660-16676). Economy-wide ECR = total revenue net of subsidies (17208/17219) ÷ energy CO2: baseline -83.5, policy -28.9 $/t in 2030. The section also compares this with the NDC (16673-16676).

**(f) Price breakdown chart for one fuel and year** (16678-16722). The breakdown is supply, taxes, VAT, carbon, efficient price and tax gap, from F12 (efficient prices). It covers gasoline, coal and gas power, and electricity.

**Bugs:**
- 16663: the coal ECR formula sums the price ratios `L16281/L16211+...` (a leftover). The other fuel rows are empty.
- 16672 is labelled "Reduction in energy-related CO2" but computes the change in ECR. As a result 16674 (implied elasticity) is garbage: 2978 in 2023. Rows 16675-16676 are empty.
- The biomass total carbon price (16467, 16522) is `#DIV/0!` (its emission factor is zero).
- The section title reads "for $0/tCO2 in 2025". The tax in the year of interest is 0 because `YearFuelPrices`=2025 falls before the policy start, so the title is misleading.
- `H16332` (residential electricity, policy) builds its code from `C16331`, the industry row.

#### F6. Power generation costs (16726-16784)
**Consumers:** Dashboard charts 35, 54, 73, 74.

**Content:**
- Levelised generation cost components ($/kWh) by technology: baseline, and policy in 2030.
- Variable generation cost for the tipping-point charts (new solar against new or existing coal).
- System costs by fuel, including storage.
- Coal-to-gas switching carbon prices (`c2ginv`, `c2gdis`). Egypt: -120 and -64 $/t, meaning gas is already cheaper than coal.

**Issue:** the titles hardcode "US$30 Carbon tax" (16752, 16757) and "2018-2030".

#### F7. Energy consumption (16788-16983)
**Consumers:** Dashboard charts 2, 70, 71; F9 and F12 (weights); BoP; legacy MTOutputs 426-588.

**Content:**
- Final energy by fuel (7 fossil fuels + nuclear + renewables + biomass), baseline and policy. Egypt 2030 totals: 101.2 → 84.6 Mtoe.
- Changes by fuel, absolute and %. 2030: coal -22.6%, gas -18.4%, gasoline -10.6%, diesel -15.9%, LPG -24.5%.
- Totals by sector (pow, tra, bld, ind, oen).
- Full sector × fuel grid (16864-16983, `mit.ener.<sec>.<fuel>`).

**Issue:** 16807 uses the hardcoded row offset `=J16807+1550-1`.

#### F8. Power sector (16987-17145)
**Consumers:** Dashboard charts 6, 9, 34, 40, 41, 53, 55; legacy MTOutputs 1063-1137; names `M_baseline*` and `M_policy*`.

**Content:**
- **Sustainability indicators** (16990-16997): CO2/GDP, renewable share, variable renewable (VRE) share, grid CO2 intensity (0.370 → 0.308 t/MWh in 2030).
- Generation by source in TWh and %: baseline 266.7, policy 246.1 TWh in 2030. Renewable share 24.1% → 28.2%.
- Change in generation against baseline.
- Electricity demand by sector.
- New capacity investment in MW and US$bn, baseline and policy, and the difference.

#### F9. Revenues (17148-17389)
**Consumers:** Dashboard charts 1, 10, 11, 12, 67; legacy MTOutputs 23-32, 777-809; names `QC_VarRevenues`.

**(a) Totals** (17151-17157):

| Total revenue | 2030 | 2039 |
|---|---|---|
| Baseline, $bn | -19.40 | -3.77 |
| Policy, $bn | -5.49 | +34.72 |
| Change, $bn | +13.9 | +38.5 |
| Baseline, % GDP | -2.51% | |
| Policy, % GDP | -0.71% | |

Further rows split the change into existing taxes, the carbon tax, evasion and fossil-fuel subsidy reform (FFSR). The evasion and FFSR rows are 0 for Egypt.

**(b) Revenue by fuel, net of subsidies** (17183-17240), baseline and policy, with the changes. In 2030 gas gives +6.4, diesel +2.2, oil +2.0, LPG/kerosene +1.3, gasoline +0.9 and electricity +0.8 $bn.

**(c) "PIIE paper" calculations** (17242-17345):
- Revenue from existing taxes, by fuel × sector: baseline consumption × baseline taxes.
- Counterfactual: policy consumption × baseline taxes.
- **Base erosion** in % of GDP.
- Carbon tax revenue = sector CO2 × carbon price: Egypt 2030 9.50 $bn = 1.23% of GDP. It ignores coverage and exemptions.

**(d) Consumer-side and producer-side subsidies** by fuel, baseline and policy, $bn and % GDP. Consumer side 2030: 19.2 → 15.5 $bn. Producer side (electricity): 11.6 → 10.7.

**Bugs:**
- 17336-17339 (carbon tax revenue by sector): columns L:M point one row too high (18595..18598) while columns from N onward point at 18596..18599. Harmless only because the carbon price is 0 in 2022-23.
- 17250-17293 hardwire row numbers inside the scenario blocks (`L$2526+...+L$2532`, `L$7990`, `L$14086`).
- 17283 and 17341 divide by `MTOutputs!K34` (legacy MTOutputs) instead of an F row.

#### F10. Monetized social costs and benefits (17392-18172)
**Consumers:** Dashboard charts 60, 62, 63, 72, 75; legacy MTOutputs 810-909 and 1223-1319.

This is the largest computational block.

**(a) Price grids** (17394-17594): retail, VAT, pre-tax and pre-existing taxes for baseline, policy and shadow prices. Then the new tax, the consumption-weighted total carbon tax, and the average of new and pre-existing tax (the trapezoid height).

**(b) Methane-fee efficiency cost** (17596-17634): emissions and abatement for 7 sources, cost `a/(b+1)·x^(b+1)` from marginal abatement cost (MAC) curve parameters. 0 for Egypt (no fee).

**(c) Deadweight / efficiency costs** (17636-17653), the trapezoid: −avg tax × Δconsumption per fuel. Total 2030 = -3.27 $bn, which is a gain because consumption of subsidised fuels falls. 0.42% of GDP. An "info only" Harberger-triangle variant follows (17656-17669).

**(d) Global warming costs and social cost of carbon (SCC)** (17670-17724). Four options, both for the national SCC (NSCC) and for the global SCC (GSCC):

| SCC option | Egypt 2030, $/t | Selected? |
|---|---|---|
| Target-consistent price | 75 | yes, for both NSCC and GSCC |
| Ricke et al. (from sheet `SCC`) | 9.4 | |
| Manual | 96 | |
| US EPA 2.5% | 85 | |

Climate damages = SCC × total GHG. Avoided damages in 2030: 5.0 $bn. A global-warming cost per unit of each fuel follows.

**(e) Total welfare benefits** (17727-17749), national, 2030:

| Item | $bn |
|---|---|
| Climate | 5.02 |
| Air-pollution mortality (from `Air pollution`) | 0.91 |
| Road accidents + congestion + road damage (from `Transport`) | 0.47 |
| Efficiency | +3.27 |
| **Total** | **9.67 (1.25% GDP)** |

Chart helper rows follow.

**(f) Externality unit costs** (17751-17799):
- Air-pollution cost per unit of fuel and sector, from `Air pollution`.
- Transport externalities per litre, from `Transport`.
- Environmental benefit by Harberger triangles; total "FFS welfare" (17799).

**(g) Subsidies, explicit and implicit** (17801-17966), IMF method. Efficient price = supply cost + externalities + VAT. Explicit subsidy = max(0, supply − retail) × quantity. Implicit subsidy = (efficient − max(retail, supply)) × quantity. This is done for gasoline, diesel, LPG, kerosene, other oil, gas (ind/res/pow/other), coal (ind/res/pow/other) and electricity (ind/res/other). Egypt 2030: explicit 29.5 $bn (4.0% GDP); implicit `#N/A`.

**(h) Efficient prices and Pigouvian taxes** (17968-18128). For each fuel and sector: efficient price, tax gap, baseline excise in CO2-equivalent, Pigouvian tax and its CO2-equivalent. Consumption-weighted averages (18130-18138): Pigouvian tax 160 $/t CO2e in the baseline (2030), of which 68 is air pollution. The section ends with the breakdown chart data for one year (18140-18172).

**Bugs (several change Egypt numbers):**
1. **The "Non-road oil" global-warming cost per unit (17695, 17719) is `#N/A`.** It propagates to 17792, 17793, 17797, the **total environmental benefits (17798), total national welfare benefits including FFS (17799)**, the oil efficient price (17853-17859) and **total implicit subsidies (17964, 17966)**. All of these are `#N/A` for Egypt.
2. 17463 (LPG pre-existing tax, consumption weighted) has no formula, so it reads 0. The LPG average tax (17593) is halved.
3. 17789 converts diesel with `_conv_ktoe_liter_gso`; 17846 converts kerosene with `_conv_ktoe_liter_die`. Wrong conversion factors.
4. 17829 ("LPG portion used for residential") holds an implicit-subsidy formula pointing at 17825-17827, so it reads 0. LPG VAT is 0.
5. 17912 (coal residential retail price) points at `L17400` (gas, industry). 17921 (coal power retail price) points at `L17401` (coal residential). These are off-by-one rows that change the coal subsidies.
6. 17954 and 17958 ("Electricity, other", supply cost and retail price): column L is correct, but from column M the formulas are `=M16219` (diesel supply cost) and gasoline. Inconsistent formulas across columns.
7. 17761 (LPG air-pollution cost) uses the absolute `$K$4314`, so the value is flat at 1.244 in every year. 17762 (kerosene) uses `K$4313`. Check whether LPG and kerosene are swapped.
8. 17775 (road damage, gasoline) is empty, flagged `[**]` in the sheet.
9. 17666 duplicates 17669 without the /1000. 17754 hardcodes 9127.
10. 17985 and later: the "Retail price" used for the tax gap is the **policy** retail price, not the baseline one.

#### F11. Balance of payments (18175-18219)
**Consumers:** Dashboard chart 4; legacy MTOutputs.

**Content:**
- Change in consumption of oil, gas and coal × international price (rows 707, 709, 732) gives the value of the change in net imports. 2030: oil -3.17, gas -0.45, coal -0.09 $bn. Gas and coal are also × an import share (`$H741`, `$H743`).
- First-order current account effect, in $bn and % of GDP.
- Net oil and gas imports, baseline and policy.

**Bugs:**
- The "Pre-policy" current account (18197) is `#NAME?`, so the whole % of GDP panel (18199-18210) is an error.
- 18215 takes `SUM(K741:K743)` (column K, one year lag) for column L.
- 18218 is policy net imports = baseline − Δ, where Δ is already signed. The sign looks reversed (policy net imports rise when imports fall). Check.
- Oil has no import-share factor; gas and coal do.

#### F12. GHG emissions and NDC (18222-18541)
**Consumers:** Dashboard charts 31, 39, 45, 47-49, 65, 68, 69, 76-78; NDCs (18493, 18508-18518); legacy MTOutputs 38-122; names `NDC_gap`, `NDCPrice`, `QC_VarEmissions`.

**Content:**
- **Total GHG excluding LULUCF**: 487.2 → 420.3 Mt CO2e in 2030; 623.4 → 452.5 in 2039.
- By UNFCCC source: energy 235.8 → 193.4; industrial processes 87.7 → 63.1 (IPPU falls under the policy); agriculture; waste and other (114.1).
- By gas: CO2 372.3 → 311.4; CH4, N2O, F-gases.
- Methane by source.
- Historical inventory by sector × gas.
- Energy GHGs plus short-lived forcers: BC, OC, VOC, CO, SO2 in CO2e (SO2 and OC negative). Abatement by pollutant.
- **GHGs by broad sector** (18346-18381). Power = CO2 + all energy CH4 + N2O/3; transport = CO2 + 2/3 of N2O. These are hardcoded allocations.
- Abatement by sector in 2030: power -10.2, transport -7.0, buildings -3.9, industry -45.7 (of which IPPU -24.6).
- Intensity per GDP and per capita, indexed to `ResultsYear`.
- **NDC comparison** (18384-18520):
  - NDC characteristics from `{_NDC_*}` names. Egypt: BAU type, -27% unconditional by 2030, no conditional target.
  - One target calculation for each NDC type (BAU, fixed, historical, intensity, unquantifiable).
  - Selected target: 355.7 Mt in 2030.
  - Policy GHG in the target year: 420.3 (read through `MTOutputs!K60`).
  - **Gap: 64.6 Mt.** The policy achieves -13.7% against the -27% needed (ratio 0.51).
  - `NDCPrice` (H18501 = 150) is the solver's changing cell for the goal seek.
  - Net-zero pathway flag.
- Grid emission intensities (18530-18541).

**Bugs:**
- 18425-18427 multiply the target *level* by the year adjustment `F18414` after the reduction was already scaled by it in 18422. This double-counts the adjustment whenever the target year is before 2030.
- 18497-18498 compute baseline/target while 18499 computes target/baseline. Row 18509 ("unconditional") then shows the average ratio.
- 18526 (baseline GHG including PM, indexed) divides by the policy row 18525.
- 18348 puts all energy CH4 in power.

#### F13. CO2 emissions (18544-18870)
**Consumers:** Dashboard charts 27-30, 37, 42-44, 50-52, 127, 130, 133, 141, 142; GHGs!D1196 (18566); legacy MTOutputs.

**Content:**
- Total CO2 including non-energy, baseline and policy, % change.
- Energy CO2 by fuel and by sector, with the changes. 2030 by sector: power -10.1, transport -6.8, buildings -3.9, industry -21.1, total -42.1.
- Power CO2 by fuel (engineer model).
- Buildings CO2 by subsector and by fuel.
- **Industry**: CO2 by subsector and by fuel; indirect CO2 from electricity; direct + indirect.
- **Emission intensity per $m GVA**, using GTAP output from E1 scaled by the 15720 adjustment.
- Cumulative CO2 against GVA by sector.
- Transport CO2 by mode.

**Issue:** 18709 "Other liquid fuels" sums oil, gasoline and diesel, and leaves out LPG and kerosene.

#### F14. Kaya identity (18874-18935)
**Consumer:** Dashboard chart 38.

**Content:** population, GDP, primary energy and CO2, with the ratios GDP/capita, energy/GDP and CO2/energy indexed to 2022, for baseline and policy. Egypt 2030 baseline: CO2 +21% = population +16%, GDP per capita +22%, energy intensity -20%, carbon intensity +7%. A "simplified" variant follows.

**Bugs:**
- 18910: the column-L formula of policy energy/GDP uses the baseline rows (later columns are correct).
- 18931 "Total primary energy consumption" uses row 16804 (renewables) instead of 16806, so it reads -97%.

#### F15. Methane (18938-18978)
**Consumers:** legacy MTOutputs 1196-1222.

**Content:**
- CH4 emission factors after abatement (oil and gas, coal).
- CH4 by source, baseline and policy.
- Methane-fee trajectories.
- Methane-fee efficiency cost in % of GDP (from F10b).
- Producer prices and the price increase from the fee.

**Issue:** the labels of 18977 and 18978 are swapped (codes coa/nga against the labels gas/coal).

#### F16. Transportation results and CBAM (18979-19031)
**Consumers:** Transport3 (EV shares 18981-18987); Dashboard chart 146; legacy MTOutputs 1320-1348.

**Content:**
- EV sales shares, calculated and actual, by class (baseline and policy).
- VKT and fuel economy.
- EV stock shares.
- Vehicle ownership.
- "Results - CBAM goods" (19028-19031): a stub, mostly 0.

---

### 3. Block G: other purposes (19033-19218)

| Rows | Content | Consumer |
|---|---|---|
| 19035-19094 | Intermediate prices: inflation, VAT, international prices, conversion to $/GJ, markups (global → retail and pre-tax → retail) and forecast pre-tax and retail prices by fuel and sector | legacy MTOutputs 1138-1195 (a "simplified prices" export, used to rebuild prices outside CPAT) |
| 19096-19210 | Energy-balance matrix: CPAT energy use (sector × fuel) in a chosen base or future year, a base-year matrix from rows 583+, and a checksum | legacy MTOutputs 1075-1094 |

The checksum differs from 0 for Egypt (e.g. gas -4022 / +950).

---

### 4. Sheets of the workbook and their relation to the Mitigation results

The workbook has 67 sheets.

| Group | Sheet | Role relative to the scenario results |
|---|---|---|
| Front | Cover, Data sources | text |
| | **Dashboard** | **Output.** 146 charts. About 75 read Mitigation F directly (F2-F16; the 16081+ ranges above). The rest read Air pollution, Transport and Distribution. 170 formula cells read F section titles, scenario names and a few C/D cells. |
| | Manual inputs | input |
| Modules | Mitigation | the scenarios (C, D) and the reports (E, F, G) |
| | **Air pollution** | **Downstream module.** Reads E3 (energy and emissions by source × pollutant; GDP). Returns mortality, morbidity and unit air-pollution costs to F10 (17732, 17753-17764) |
| | **Distribution** | **Downstream module.** Reads E1 (GDP, carbon price, revenue, prices and price changes by sector, consumption changes, GTAP IO) and F5 prices. Produces household incidence (2 charts on its own sheet; Dashboard incidence charts) |
| | **Transport** | **Downstream module.** Reads E2 (road fuel by class, margins, shares, VKT) and F4 GDP growth. Returns accident, congestion and road-damage costs to F10 (17733-17735, 17771-17776, 17980-17997) |
| DATA_MITIGATION | MTInputs | scenario inputs (upstream) |
| | Power | data |
| | **MTOutputs (legacy)** | **Output export.** About 1,313 indicator rows (codes × years): policy characteristics, macro, emissions, prices, price components, total carbon price, Pigouvian taxes, energy use (also disaggregated for the policy), revenues, air-pollution, climate, transport, welfare and distribution effects, revenue-recycling gains, indirect price changes, power indicators, simplified prices and markups, methane, subsidies, transportation. 17,029 references into F, 3,904 into D, 1,579 into G. It also feeds three cells back into F (K7, K34, K60) |
| | GHGs | data (one reference to F 18566) |
| | **NDCs** | data plus NDC text that reads the F12 gap (18493, 18508-18518) |
| | GoalSeekCoal | helper on the baseline power block (3796-3797) |
| | **CBAM** | **Downstream calculation.** Reads the policy carbon price (D 8578-8583) and computes CBAM-relevant carbon costs per good (steel routes, etc.) |
| | Countries, ECP, Balances, EnergyCons, CoC, CH4Inputs, UNPop, OilProductShares, Prices_int, Prices_dom, Elasticities, ETS+LTS, WEO, WDI, SSPs, EF_GHG, OtherPowerUse, **SCC** (read by F10d), EF_PM, CalVal, Meta_mit | data (upstream) |
| DATA_DISTN | Mapping, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios | Distribution data (Mapping and IO_GTAP are also used by E1) |
| DATA_TRAN | Transport1, Transport2, **Transport3** (reads F16 EV shares), Notes, Tran_Elast, Tran_Scatter | transport data |
| DATA_OUTPUT | Glossary, Multipliers | reference |
| DATA_AIR_POLL | WB, GBD, IHME, ILO, ExposureCoefs, IF PP, ConcMat, Air_Data, Air_meta | air-pollution data |
| | VersionTracker | admin |

No sheet is named "Results" or "Summary". The output layers are F (charts), Dashboard and the legacy MTOutputs export.

---

### 5. Mapping: legacy downstream item → MVP v4.7 status

**What the MVP has.** The MVP runs N scenarios as column groups. Results live in Mitigation sections 11-16. MTOutputs holds 71 indicators per scenario block (`MTO_INDICATORS`, `build_v7_0.py` l.5157). StoredResults keeps the stored runs as values (macro `RunAllScenarios`). ScenarioCompare compares one year against the baseline. Charts has 15 line charts.

| Legacy item | Rows | MVP status | Where / what is missing |
|---|---|---|---|
| E1 Distribution hand-off | 14771-15720 | **Not built** | Price grids by subsector × fuel exist (Mitigation section 2, `rp`/`atp`, per scenario). Missing: the % change tables, the consumption-change table, revenue % GDP, GTAP IO table, inflation. TODO item 5 |
| E2 Transport hand-off | 15722-15823 | **Partial** | Section 5b has fuel use by class, VKT and fuel economy per scenario. Missing: margins, shares, the hand-off table, and the Transport externality sheet |
| E3 Air-pollution hand-off | 15825-16078 | **Built (data), not handed off** | Section 15: `ap`, `aps` (kt by the 8 air-module sectors), `apf`. Missing: power/residential energy tables in the hand-off layout and the Air pollution module itself |
| F2 Macro drivers | 16086-16125 | **Partial** | GDP, population, international prices and elasticities are inputs. Missing: the income-elasticity summary and the implied CO2 income elasticity (trivial) |
| F3 Policy coverage, revenue-recycling shares | 16127-16157 | **Partial** | `cptraj`, `ctcov` switches, ETS coverage `co2.ets`, `EXP*` shares (section 16). Missing: % of CO2 covered by the carbon tax and the coverage contribution by sector; effective carbon tax |
| F4 GDP effects | 16160-16201 | **Partial** | Section 16 (v3.1): `fis.sp`, `fis.eff` by revenue use, `gdp.eff`, `gdp.pos.usd`; in MTOutputs. Missing: the growth-decomposition table and the year-of-reform profile |
| F5a-c Prices by fuel/sector; weighted price changes | 16204-16402 | **Partial** | Section 2 per scenario (`rp`, `atp`, `rpb`); MTOutputs has 7 price rows. Missing: consumption-weighted averages, % change against the baseline, index 2022=100 |
| F5d-e Total carbon price; ECR | 16408-16676 | **Not built** | `xcp`/`ccp` are carbon-price components only. Implicit carbon price of taxes and subsidies and the ECR not built |
| F6 Power generation costs, switching prices | 16726-16784 | **Partial** | Power section 3 (costs, `ccp`, `gncav`, `ccpav`). Missing: the tipping-point and system-cost report tables |
| F7 Energy consumption by fuel/sector, changes | 16788-16983 | **Built** (by sector, totals); **partial** (by fuel) | Section 11 `ener`, `ener.pct`; MTOutputs `mit.ener.*`. Fuel-by-fuel changes only on Mitigation, not in MTOutputs |
| F8 Power: generation, shares, demand, capacity, investment | 16987-17145 | **Built** | Section 3 `gen`, `shr`, `vre`, `eldem`, `cap`, `nim`, `usd`; MTOutputs v1.07 rows. The investment difference against the baseline is via ScenarioCompare |
| F9a-b Revenues total and by fuel | 17148-17240 | **Built** (totals, by sector and power); **partial** (by fuel) | Section 12 `rtx`, `rsub`, `rnew`, `rnet`, `rtot`, `rtot.chg`, `rmf`. Missing: the by-fuel net table in the legacy layout and % of GDP |
| F9c PIIE: base erosion, sector carbon tax revenue | 17242-17345 | **Not built** | Easy from `rtx` at baseline taxes (needs a counterfactual: policy consumption × baseline taxes) |
| F9d Consumer/producer subsidies | 17347-17389 | **Partial** | `rsub`/`esub` give the subsidy cost by fuel and sector. Missing: the consumer/producer split and % of GDP |
| F10a-c Efficiency (deadweight) costs; methane-fee efficiency cost | 17394-17669 | **Not built** | Needs the average of old and new tax × Δconsumption. All inputs exist |
| F10d SCC, global warming costs | 17670-17724 | **Not built** | Needs the `SCC` data sheet (Ricke), EPA, target-consistent and manual options |
| F10e Welfare benefits | 17727-17749 | **Not built** | Climate part feasible now. Air-pollution and transport co-benefits need those modules (or unit damages) |
| F10f-h Externalities, explicit/implicit subsidies, efficient prices, Pigouvian taxes | 17751-18172 | **Not built** | Needs air-pollution unit costs (`Air pollution`/GBD) and transport externalities |
| F11 Balance of payments | 18175-18219 | **Not built** | Simple: Δ fuel use × international price × import share. Needs net-import data (legacy rows 741-743) |
| F12 GHG by source/gas/sector, short-lived forcers | 18222-18381 | **Built** (by gas and source, totals); **partial** (broad sectors, abatement tables) | Section 14 `ghg`, `ghg.inc`, `ghg.chg`, `ch4.*`; section 15 `apf`. Missing: the broad-sector allocation table and its abatement table |
| F12 NDC comparison and goal seek | 18384-18520 | **Not built** | Needs NDC data (`NDCs` sheet, `_NDC_*` names). ETS goal seek exists, an NDC goal seek does not |
| F12 Grid emission intensity | 18530-18541 | **Partial** | `mit.co2.pow.all.e` and `gtot` give it; no row |
| F13 CO2 by fuel/sector/subsector, industry CO2 incl. indirect, intensity per GVA | 18544-18870 | **Built** (by fuel and sector, `co2`, `co2.chg`); **not built** (industry indirect and per-GVA intensity) | Per-GVA intensity needs GTAP IO |
| F14 Kaya | 18874-18935 | **Not built** | Trivial from `pop`, GDP, `ener`, `co2` |
| F15 Methane results | 18938-18978 | **Built** | Section 14 `ch4.src/act/abt/em/sup`, `ch4.rev`, `mfee`. Producer-price effect of the fee not built (a TODO decision item) |
| F16 EV shares, VKT, ownership | 18979-19026 | **Built on Mitigation, not exported** | Section 5b (`trevsh`, `trvkt*`, `trown*`); none in MTOutputs |
| F16 / CBAM sheet | 19028-19031, CBAM | **Not built** | Needs the CBAM sheet (production, EF per route) |
| G Intermediate prices / markups | 19035-19094 | **Built internally** | Section 2 builds markups; not exported as a table |
| G Energy-balance matrix | 19096-19210 | **Partial** | Data sheet `Balances` and its calibration. The projected sector × fuel matrix is not exported |
| Dashboard (146 charts) | | **Partial** | Charts sheet (15 line charts from MTOutputs); ScenarioCompare |
| MTOutputs legacy (about 1,313 rows) | | **Partial** | MVP MTOutputs has 71 indicators × N scenarios; StoredResults/ScenarioCompare go beyond legacy (N scenarios) |

---

### 6. Recommended order of work

The order follows the user-agreed sequence in `../TODO.md` (item 4 remaining policies → item 5 hand-offs, Distribution first → item 6 report blocks and Dashboard). Cheap report items that are pure arithmetic on rows the MVP already has are pulled forward, because they need no new data and fill most of the F-block gap.

1. **Add a "Reports" section 17 on Mitigation, one formula per row, per scenario.** It contains differences against scenario 1 (using the existing `*.ref` pattern), with no new data:
   - consumption-weighted price changes by fuel (F5c);
   - fuel-by-fuel energy and CO2 changes (F7, F13);
   - revenues by fuel net of subsidies and % of GDP (F9a-b, F9d split);
   - broad-sector GHG allocation and abatement (F12), with the N2O/CH4 allocation documented, not hardcoded;
   - grid intensity, Kaya (F14), base erosion (F9c), effective carbon tax and CO2 coverage by sector (F3);
   - ECR and the total implicit carbon price (F5d-e).
   Extend `MTO_INDICATORS`, StoredResults and ScenarioCompare with the headline rows (about 25 rows). This also fixes the legacy bugs seen in F5 and F14 by construction.
2. **Hand-off to Distribution (E1), TODO item 5.** Build the price-change table (subsector × fuel, % against scenario 1), the consumption-change table, revenue % of GDP and the GDP-effect rows in the legacy E1 layout, plus the GTAP IO extract (`Mapping`, `IO_GTAP`). This also unblocks the industry per-GVA intensity (F13).
3. **Efficiency costs and climate welfare (F10a-e, climate part).**
   - Trapezoid deadweight costs per fuel.
   - SCC options: add the `SCC` data, EPA path, manual, target-consistent.
   - National and global avoided climate damages.
   - Welfare table with the air and transport co-benefit rows left as 0 or memo until those modules exist.
   - Fix the legacy bugs F10 #2-#6 and #10 while porting.
4. **Balance of payments (F11)** and **NDC comparison with a goal seek (F12)**. Both need small data tables (net imports and import shares; the NDC type, year, reduction and LULUCF flag). The NDC goal seek can reuse the ETS goal-seek macro pattern. Fix the double year-adjustment and the sign issues.
5. **Air pollution module and its hand-off (E3).** `aps` is ready. Then plug the unit damages into the welfare table and the externality costs (F10f).
6. **Transport externalities (E2 + `Transport` sheet)**: accidents, congestion, road damage. Then F10f-h: efficient prices, Pigouvian taxes, explicit and implicit subsidies (IMF method). Fix the `#N/A` of the non-road-oil SCC chain, the LPG and kerosene conversions, and the coal row offsets.
7. **Remaining reports:**
   - the year-of-reform GDP profile (F4);
   - power tipping-point and system-cost tables (F6);
   - energy-balance export and simplified prices (G);
   - EV and VKT rows in MTOutputs (F16);
   - the CBAM sheet.
8. **Dashboard**: a chart sheet driven by the Reports section and ScenarioCompare, replacing the 146 legacy charts with a curated set. The current Charts sheet is the seed.

Legacy bugs to report to the CPAT team are flagged per section above. The ones that change Egypt numbers:
- F10 `#N/A` chain: total welfare including FFS and implicit subsidies;
- F10 #2-#6: LPG tax, wrong conversions, coal row offsets, electricity "other" column mix;
- F11 `#NAME?` and the sign of net imports;
- F12 NDC double year adjustment (bites when the target year is before 2030);
- F14 -97% primary energy.
