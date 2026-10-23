# Changelog: CPAT-AI Mitigation Prototype

One line per release, newest first. Full notes: the version log in the workbook (tab `Version Log, About, and Diff`) and `CAVEATS.md`.

| Version | Date | Change |
|---|---|---|
| 8.2 | 2026-10-23 | Register and documents: legacy cell references moved from CPAT 1.0pre_456 to the latest file, 1.0pre_465; the 62 bugs the CPAT team marked fixed in 465 checked cell by cell (52 confirmed, 8 with caveats, 2 not fixed): status in legacy in the register (Appendices B, C), BUGS.md, the register spreadsheet and the tracker (tabs BUGS, ISSUES-OTHER). Workbook formulas and results unchanged. |
| 8.1 | 2026-10-22 | Modules M1-M2: one money-unit vocabulary (USD, never $); section 15 moved to the end; new section 19 Exports to modules (19a Distribution, defined name ExportDistn); tab FromMitigation is Distribution's only Mitigation input. |
| 8.0 | 2026-10-22 | Renamed CPAT-AI-Mitigation-Prototype (was MVP). |
| 7.2 | 2026-10-22 | Codes (CPAT code protocol, plan R0-R9): one rename map (data/mvp_legacy_extracts/code_renames_v7_2.csv) applied where text is written: Mitigation columns A-C... |
| 7.1 | 2026-10-21 | Linked data tables: nine tabs refresh from the data workbook (was Balances only): Balances, EnergyCons, Prices_dom, HHSurvey, IO_GTAP, HH_Elast (rows of the ... |
| 7.0 | 2026-10-21 | Release 7.0: v6.6 (speed: values shipped, manual calculation, two scenario groups) and v6.7 (the dashboard) with a full rebuild and full check; |
| 6.7 | 2026-10-21 | Dashboard: front tabs Cover (with the status of the linked data tables, was sheet DataLinks), ScenarioCompare (every user entry: Live or Stored results, year... |
| 6.6 | 2026-10-21 | Speed: the workbook ships with its calculated values and opens in manual calculation (no recalculation on open; |
| 6.5 | 2026-10-20 | Linked data tables, first one (prototype): sheet DataLinks with a data-source dropdown (Embedded = shipped data, default; |
| 6.4 | 2026-10-20 | Dashboard on ScenarioCompare: every macro button there (none on the reference tab); |
| 6.3 | 2026-10-20 | Excel repair fixed: Excel repaired every earlier version on open ("Named range from /xl/workbook.xml"): the comment of the LAMBDA name FUELUSE had 305 charac... |
| 6.2 | 2026-10-20 | User decisions 2026-10-20: subsidy reforms always separate from the before-tax build-up: the producer subsidy phase-out is the wedge ppsw (block) / psw (subs... |
| 6.1 | 2026-10-20 | Open items without new data: I49 producer subsidies enter the supply cost as legacy (rows psd, psu, block row psp; |
| 6.0 | 2026-10-19 | Consolidated release of v5.0-v5.7 (full rebuild, full check). |
| 5.7 | 2026-10-19 | Results blocks (item 8 A+B): 14c NDC comparison (sheets NDCs and GHGHist from legacy; |
| 5.6 | 2026-10-19 | Also: Settings C27, C36-C39 read MTInputs; |
| 5.5 | 2026-10-19 | Register and documents: cell-level fix plans for the 15 engineer-power bugs (legacy_bugfix_plans); |
| 5.4 | 2026-10-19 | Power engineer features (PowerFeatures_Plan P1, P2, P4): every MTInputs power input read in the scenario's own column (section-1 rows; |
| 5.3 | 2026-10-19 | Full check repaired (independent Python power data step with the v4.10 fixes L52-L55, missing recomputations, stale expectations); |
| 5.2 | 2026-10-19 | Whole legacy Manual inputs tab at the legacy addresses (17 blocks, rows 5-378; |
| 5.1 | 2026-10-18 | Residential LPG and kerosene always exempted (MTInputs AlwaysExemptResLPGKer, per scenario: no new carbon tax, ETS or excise, nor their VAT; |
| 5.0 | 2026-10-18 | Release 5.0 (user: bump everything to v5.0, consistent): the overnight decisions of v4.15-v4.16 consolidated; |
| 4.16 | 2026-10-18 | User decisions: consumer subsidy and price-control phase-outs and producer subsidies as separate policy lines by sector and fuel (LD18, LD19; |
| 4.15 | 2026-10-18 | User decisions: ETS benchmarks = 1 - the MTInputs auctioned share (I21); |
| 4.14 | 2026-10-18 | Power: new capacity sized for next year's required generation, when it comes online (legacy bug L67, was issue I8; |
| 4.13 | 2026-10-18 | Residential biomass grows with income only if MTInputs BiomassNormal = Yes, as legacy (I24); |
| 4.12 | 2026-10-18 | User decisions: income factor on the GDP elasticity of fuel use as legacy (was I23); |
| 4.11 | 2026-10-18 | Bugs and issues split (user decisions): CO2 calibrated to the inventory as legacy (switch on; |
| 4.10 | 2026-10-18 | Legacy bugs no longer replicated (user rule): L14 pass-through applied once (prices); |
| 4.9 | 2026-10-17 | Faster full build (user rule: the full build as fast as possible): the baseline CO2 refresh and the emulation of RunAllScenarios run in one LibreOffice sessi... |
| 4.8 | 2026-10-17 | Distribution readability (user request): every section shows its band, its summary row last and one blank row (one row group per section; |
| 4.7 | 2026-10-17 | Power data from the legacy tabs (user request, align fully): legacy Power and CoC tabs at legacy addresses (and GHGs, for the 2023-2024 shocks); |
| 4.6 | 2026-10-17 | Data tabs aligned more fully (user request): legacy tabs with several tables kept at their legacy cell addresses (Countries, Elasticities, ETS+LTS, Multiplie... |
| 4.5 | 2026-10-17 | Data tabs aligned with legacy (user request): grouped and ordered as legacy (DATA_MITIGATION, DATA_DISTN, DATA_TRAN, DATA_OUTPUT, then DATA_OTHER); |
| 4.4 | 2026-10-17 | Distribution module (user decisions): sheet Distribution with one analysis year (MTInputs YearDistn) and deciles across, the scenario groups and LAMBDA test ... |
| 4.3 | 2026-10-17 | LAMBDA test group (user rule): scenario groups 1 and 2 hold plain formulas in every year (2041 included); |
| 4.2 | 2026-10-16 | Presentation (user requests): Cover tab as legacy (contents, cell and tab colours, abbreviations); |
| 4.1 | 2026-10-16 | Layout (user requests): every section numbered (0-18) and rolled up to its summary row(s), detail and lettered sub-blocks before the summary; |
| 4.0 | 2026-10-16 | Release 4.0: v3.18 renumbered as 4.0 (files, labels and references); |
| 3.18 | 2026-10-16 | Kaya identity on total primary energy supply as legacy (row 18880): fuel use incl. |
| 3.17 | 2026-10-16 | New section 18 Welfare and externalities, climate part: SCC options and selection as legacy (target-consistent, Ricke national and global from sheet SCC, man... |
| 3.16 | 2026-10-16 | Sub-block 16b External balance: change in net energy imports by fuel and group (change in use x supply price x import share), energy trade balance (legacy ro... |
| 3.15 | 2026-10-16 | New section 17 Carbon pricing: implicit carbon price by fuel and economy-wide (legacy F5d), effective carbon rate and effective carbon tax (F5e, row 16137), ... |
| 3.14 | 2026-10-16 | Sub-blocks 11b (energy change by fuel and sector, %), 13b (CO2 change, grid emission intensity, Kaya identity as legacy F14), 14b (GHG change by category and... |
| 3.13 | 2026-10-16 | Header rows: real GDP (USD, moved up from section 16; |
| 3.12 | 2026-10-16 | Section 15 hand-off as the air-pollution module input table (legacy rows 15859-15961): one block per module sector, pollutants in legacy order, CH4 added (co... |
| 3.11 | 2026-10-16 | Replicated from legacy: the 2023-2024 fuel-use shock on every fuel row and on power demand (header row 11, Settings C19 on; |
| 3.10 | 2026-10-16 | Section 2 memo (I31): per fuel, electricity and all energy: spending, fuel use, average price (unit value, legacy F5b), Laspeyres price index against scenari... |
| 3.9 | 2026-10-16 | Style guide (NORMS 2): two blank rows before each section band and one after, one between blocks, two before a sub-section; |
| 3.8 | 2026-10-15 | Rebuild of v3.7 from the merged builder: the v3.7 defaults (prices to 2022, ETS benchmarks 1.0) with the LAMBDAs SCALEBY and SHAREOF. |
| 3.7 | 2026-10-15 | Excel repair error fixed: Excel 365 removed the cell formulas calling the LAMBDAs SCALE and SHARE (sheet Mitigation); |
| 3.6 | 2026-10-15 | Tabs consolidated (user request): Inputs = Inputs + Inputs_prices + Inputs_power; |
| 3.5 | 2026-10-14 | Engineer road transport model (legacy section 5 with 17 bugs fixed, Transport_vs_Legacy.md) as section 5b of every scenario group: data sheets Transport1-3, ... |
| 3.4 | 2026-10-14 | No numeric literal in any formula: pass-through buckets, GJ per kWh, capex average share and dispatch tie breaker are named constants (sheet Constants); |
| 3.3 | 2026-10-14 | No country-specific number outside the reference tables: ETS semi-elasticities from sheet ETSSemi (legacy ETS+LTS, 175 countries) by country instead of typed... |
| 3.2 | 2026-10-14 | Energy CO2 calibrated to the GHG inventory: every CO2 EF (Inputs, Inputs_power) x EFCalib (Settings C27-C30) = inventory energy CO2 / scenario-1 energy CO2 w... |
| 3.1 | 2026-10-14 | GDP effects: new section 16 (fiscal space = new-policy revenue above scenario 1; |
| 3.0 | 2026-10-14 | Air-pollution module inputs in section 15: the seven pollutants by air-pollution sector (coal, gas and other power plants, ground level road, ground level ot... |
| 2.9 | 2026-10-14 | Local air pollutants: new section 15 (PM2.5, NOx, SO2, VOC, black and organic carbon, CO by subsector and power; |
| 2.8 | 2026-10-14 | Non-CO2 GHGs and methane: new section 14 (methane by source with the methane fee and its abatement curves, combustion CH4 by sector, GHG inventory categories... |
| 2.7 | 2026-10-13 | Excel repair error fixed: LAMBDA parameters y1, co2, c, tco2_kwh read as cell references, so Excel removed the 2041 cells calling them (2041 power fell to 0); |
| 2.6 | 2026-10-13 | Formatting: each price block opens with a parameter table (heading row, parameter row pset) and the international reference price (gpi) and fixed part rows, ... |
| 2.5 | 2026-10-13 | Section 2 as a price build-up by fuel (heading row) and sector (block): fixed part of the supply cost (new row spf), supply cost, excise and other taxes befo... |
| 2.4 | 2026-10-13 | Mitigation: years in row 1; |
| 2.3 | 2026-10-12 | Last year 2041 (legacy horizon) as the LAMBDA year: every calculated cell of 2041 calls its named LAMBDA; |
| 2.2 | 2026-10-11 | One version number (2.2) for the workbook, scripts, method notes, VBA module, documents and deck; |
| 1.09 | 2026-10-11 | Existing carbon pricing (sheet ECP: legacy data for 52 countries, none for Egypt; |
| 1.08 | 2026-10-11 | Works without LAMBDA support: plain formulas (at most 100 characters) in every cell, the right column (2040) included; |
| 1.07 | 2026-10-11 | Short formulas: every cell formula has at most 100 characters (defined names for the data tables, helper rows and columns, policy rates by sector in section ... |
| 1.06 | 2026-10-10 | Power engineer model: demand, dispatch, retirement and capacity, investment (legacy H, I, K, L) with D6, D9, E1; |
| 1.05 | 2026-10-10 | Power sector, price side: section 3 with legacy sub-tables A, B, C, D, E, G, J (generation costs by type, average generation cost, storage cost of variable r... |
| 1.04 | 2026-10-10 | First-run test for Excel: macro CheckBatchRun (lookups, baseline recalculated by the host vs stored, batch rerun vs stored values) with its report on the new... |
| 1.03 | 2026-10-09 | Multiple scenarios: scenario definitions on MTInputs (combined packages), VBA module CPATScenarios (batch run with ETS goal seek, results stored as values), ... |
| 1.02 | 2026-10-09 | New ETS with a cap: baseline covered emissions (data from scenario 1), fast price estimate, override row and goal-seek script; |
| 1.01 | 2026-10-09 | MTOutputs sheet: key results per scenario by output code (copy-pasteable row blocks); |
| 1.00 | 2026-10-09 | Renamed CPAT-AI-Mitigation-Prototype and upgraded to v1.00 (content as v0.16). |
| 0.16 | 2026-10-09 | Layout: one level of column groups (B:G, I:K, 2030-2039 per scenario); |
| 0.15 | 2026-10-09 | Layout: columns B:C and I:K grouped (D:G nested), row group buttons below, opens rolled up; |
| 0.14 | 2026-10-09 | Corrected Egypt price block (user); |
| 0.13 | 2026-10-09 | CO2 emissions from fuel combustion per subsector and fuel (fuel use x EF); |
| 0.12 | 2026-10-09 | Revenues: existing tax revenue, existing subsidy cost and new-policy revenue as separate calculations per subsector and fuel; |
| 0.11 | 2026-10-09 | Horizon 2040; |
| 0.10 | 2026-10-08 | Other oil products treated like the other oil products (pass-through and margin from data); |
| 0.9 | 2026-10-08 | Domestic price projection (legacy method) in section 2: international prices by source, supply cost, excise and other taxes with pass-through, retail price b... |
| 0.8 | 2026-10-08 | Shadow price on the efficiency margin of fuel use; |
| 0.7 | 2026-10-08 | Legacy CPAT section layout (1 Policies, 3 Power, 5-8 sectors, 11 Results; |
| 0.6 | 2026-10-08 | MTInputs sheet per scenario; |
| 0.5 | 2026-10-08 | White band text; |
| 0.4 | 2026-10-08 | Row outline: blocks roll up. |
| 0.3 | 2026-10-08 | Variable codes in column A; |
| 0.2 | 2026-10-08 | Inputs sheet by fuel/subsector (lookups separated from formulas); |
| 0.1 | 2026-10-08 | First build: design 2 price -> fuel-use prototype, Egypt base data, 2 scenarios. |

## CPAT-AI Distribution Prototype (standalone module, `excel_ai/distribution/`)

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-22 | First standalone module, cut from the mitigation prototype v8.1; input from Mitigation by the button Update from Mitigation (section 19a). |
