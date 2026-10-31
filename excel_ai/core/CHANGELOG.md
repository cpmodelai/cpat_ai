# Changelog: CPAT-AI Mitigation Prototype

One line per release, newest first. Full notes: the version log in the workbook (tab `Version Log, About, and Diff`) and `CAVEATS.md`.

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-10-31 | **Restructure** (user 2026-10-31; plan `prompts/Master_restructure_prompt.md`): renamed **CPAT-AI-Mitigation** (.xlsx, no macros); every macro in the new **Master workbook** `CPAT-AI-Master_UserGuide.xlsm` (user guide, module table with versions and GitHub links, activation, data update for one country or all countries, distribution update, stored scenarios in ten slots and their comparison). Modules ship with formulas to 2035 and the values of the full model; the Master activates them (fill to 2041, recalculate, save `.xlsb` in `active_workbooks/`). The Distribution tab and the distribution-only data leave the mitigation workbook (Distribution is its own workbook, `CPAT-AI-Distribution` 1.2.0). Tab groups OUTPUT (MTOutputs, ScenarioCompare) and OTHER MODULES (FromMaster, FromAirPollution, FromTransportCB). MTOutputs in the Mitigation column layout (scenarios side by side; legacy rows, additions by topic); ScenarioCompare live only (the empty second slot fixed); StoredOutputs, MacroCheck and the bar chart removed. Settings and Inputs merged into **Constants and Mappings**; the user settings on MTInputs, the rows below the legacy table in three parts (new policies, treatment of existing policies, model settings). Data tables marked by a light green header; zoom 80%; EF_PM and CH4Inputs linked by Power Query. Results unchanged: 15,100 output codes equal to 1.1.0. |
| 1.1.0 | 2026-10-30 | Data edition **Public01** (user 2026-10-30): the shipped data are the public tables plus the six proprietary tables (Balances, EnergyCons, Prices_dom, IO_GTAP, HHSurvey, Tran_Scatter) as perturbed Egypt values (±3%, identities kept); the real data only in the private edition Full01. Cover: a line "Data shipped (data edition)". Data links: sources renamed (Public01 - GitHub, Public01 - local file, data repository, SharePoint), the GitHub source reads `data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx`. Range-anxiety start values refitted on the perturbed data (passenger 64,064, freight 469,574, cycle 1,027 USD; residuals below 1e-6). Baseline CO2 and stored results recomputed. Distribution 1.1.0 and Coded CPAT 1.1.0p1.3 aligned. Results differ from 1.0.4 by the data only (formulas unchanged). |
| 1.0.4 | 2026-10-29 | Outputs tab **MTOutputs** (was LiveOutputs) in the legacy MTOutputs layout (user 2026-10-29): columns A Include? ... J SubScenario as legacy, years K:AD, F = the legacy CPAT code (was MTCode, always N/A); E and F built from the component columns; the 465 sections and rows in legacy order, one row per quantity in each scenario block, mapped to the prototype's codes (`data/mvp_legacy_extracts/mtoutputs_map_465.csv`: of 1,284 legacy rows 198 exact, 267 reordered, 492 renamed, 64 guess, 263 none); rows the prototype lacks kept with Include? = No and the reason; distribution rows in the blocks (deciles in K:T); StoredOutputs stores the Mitigation rows. Legacy bugs L231-L233 (MTOutputs rows reading the wrong cells, swapped codes). Model values unchanged. |
| 1.0.3 | 2026-10-29 | Data links: source "Dummy - GitHub (public repository)" (the data workbook read by Power Query from the public repository, wherever the workbook sits) and a source row for a separate data repository (URL typed; without an address the update stops with a message). Distribution 1.0.3 and Coded CPAT 1.0.3p1.1 aligned. Quick, distribution and full (partial) checks PASS; values unchanged. |
| 1.0.2 | 2026-10-29 | User decisions 2026-10-29; Distribution 1.0.2 and Coded CPAT 1.0.2p1.1 aligned. Methane abatement curves take the CH4Inputs average where the country coefficient is 0 or missing, as legacy (issue I152; helper rows `ch4.abc`; no change for Egypt). Vehicle stocks coded `tot` (`pass/fre/motor.own.tot`, `tot.own.tot`; were `*.own.all`). Input row `ModelForm` (default CPAT) in ScenarioDefinition. Scope: CBAM process emissions, green public investment, emissions intensity of industrial output and the air pollution and transport co-benefits modules are upgrades U15-U19, out of scope. Quick, distribution and full (partial) checks PASS; 0 values changed. |
| 1.0.1 | 2026-10-29 | Layout and norms only, from the repaired full check of 1.0.0: a label row above each variable of the Pigouvian road-transport block (section 1) and for the driving share (section 17b, own block); the air-pollution sector position of section 17b looked up by its code (ApKapHdr) instead of typed; the last row of section 19 without decimals. Quick check: 0 output codes changed against 1.0.0; full check (partial) PASS. Egypt values unchanged. |
| 1.0.0 | 2026-10-29 | First full release (user 2026-10-29): v0.9.2 as released, with the methane fee cap in its short form (M21). Replicated number for number by Coded CPAT 1.0.0p1.0 (Python). Egypt values unchanged. |
| 0.9.2 | 2026-10-29 | Prototype bugs found by Coded CPAT fixed (user rule: prototype bugs are never put into Coded CPAT; the prototype is fixed to align): M15 VAT of the year in section 18 (row vatgen: VAT_WEO to LastHistPriceYear, then held), M16 freight BEV feebate at the BEV distance, M17 PHEV insurance on the BEV price with ICEV maintenance (row im.phv), M19 nominal GDP in bn, M20 World Bank LNG and Europe gas series, M21 methane fee where the curve exponent is 0, M22 Distribution percentile recycling rows. M18 withdrawn (not a bug). Egypt: only gdpn changes in Mitigation (scenarios 1-6); Distribution hrec and hnet of the percentiles where public investment is used. |
| 0.9.1 | 2026-10-29 | Data only: tab Prices_dom holds Egypt only, as the public legacy file (user decision). Egypt values unchanged. |
| 0.9.0 | 2026-10-29 | Remaining functionality and reverts to legacy (Equations_addendum.md). Reverts: LD1 food & forestry industry elasticities; LD10 fuel price reform follows the switch (L171, L173, L174, L175); I47 methane fee on own activity; LD16 margins with the CPI of the year read (L172), LD80 domestic-production weight; LD41 data extracts from legacy 465; LD58 Same. Built: R1 section 17b (co-benefit inputs, typed Egypt values), R2 section 18 (social costs, full welfare wel.usd with air pollution and road co-benefits, FFS, subsidies; L176-L193), R3 Pigouvian taxes in section 1 and efficient prices (AddEfficientTaxes, default No; L194-L196, L203), module output rows in sections 5b and 15, R6 exempt split as legacy, R7 producer subsidies in the supply cost and electricity producer subsidies, R8 Manual inputs (prices, elasticities, methane intensity decline; L101, L135, L220), R9 electricity consumer subsidy, price-chain residual and power cost memos (L222), R10 road biofuels, aviation and navigation renewables, range-anxiety fit, R11 current account in section 16b (L50, L214, L215). R4, R5, R12 deferred by the user. Power model aligned with legacy 465 (no formula change). New legacy bugs L171-L222, issues I101-I148. Results change: wel.usd (co-benefits), electricity prices and demand (price-chain residual), methane (intensity decline), the road model (range anxiety). Last historical price year 2024, as legacy (user; I89 closed). Local-pollutant and combustion-CH4 factors as legacy 465 (table Inputs_nc: country, else region, else world; other energy the maximum, I149; L58, L59 fixed by the CPAT team): section 15 equals legacy in 2022 except navigation (L22) and CH4 (L223). Pigouvian components live and acyclic (base-year value x growth of the per-km costs, I151); air-pollution unit costs as marginal damages (L224); module tabs FromAirPollution and FromTransportCB. Egypt prices equal legacy 465 (I99 closed). |
| 0.8.5 | 2026-10-29 | Data problems as issues (codes DB, DI retired): combustion emission factors as legacy 465 (issue I98: final factor of EFSel, Average by default, extrapolated after 2039; was FE fin, flat); blank VAT cells a legacy bug with a cell plan (L170) and issue I97; the corrected Egypt prices a departure by user decision (I99). Local pollutants and combustion CH4 change; other results unchanged. |
| 0.8.4 | 2026-10-28 | Inputs on legacy 465: ScenarioDefinition has the rows of the 465 MTInputs (456 rows 329-330 gone, later rows 2 higher) and a complete set of names (legacy bug L137: no D_ prefix, no trailing space; issue I87: 87 names added). One register for every module (codes L, DB, M, I, DI, LD, U); files named <name>_v0.8.4 at the top of excel_ai/, the workbook also in permalink/. Results unchanged. |
| 0.8.3 | 2026-10-23 | Legacy bug L134 (price-increase unit labels of other oil products and biomass) registered and fixed in ScenarioDefinition; register spreadsheet built from the register itself; Excel lint in every writer; to-do leads closed (NOx forcing explained, Manual inputs J178:J179 read). Results unchanged. |
| 0.8.2 | 2026-10-23 | Register and documents: legacy cell references moved from CPAT 1.0pre_456 to the latest file, 1.0pre_465; the 62 bugs the CPAT team marked fixed in 465 checked cell by cell (52 confirmed, 8 with caveats, 2 not fixed): status in legacy in the register (Appendices B, C), BUGS.md, the register spreadsheet and the tracker (tabs BUGS, ISSUES-OTHER). Workbook formulas and results unchanged. |
| 0.8.1 | 2026-10-22 | Modules M1-M2: one money-unit vocabulary (USD, never $); section 15 moved to the end; new section 19 Exports to modules (19a Distribution, defined name ExportDistn); tab FromMitigation is Distribution's only Mitigation input. |
| 0.8.0 | 2026-10-22 | Renamed CPAT-AI-Mitigation-Prototype (was MVP). |
| 0.7.2 | 2026-10-22 | Codes (CPAT code protocol, plan R0-R9): one rename map (data/mvp_legacy_extracts/code_renames_v0_7_2.csv) applied where text is written: Mitigation columns A-C... |
| 0.7.1 | 2026-10-21 | Linked data tables: nine tabs refresh from the data workbook (was Balances only): Balances, EnergyCons, Prices_dom, HHSurvey, IO_GTAP, HH_Elast (rows of the ... |
| 0.7.0 | 2026-10-21 | Release 0.7.0: v0.6.6 (speed: values shipped, manual calculation, two scenario groups) and v0.6.7 (the dashboard) with a full rebuild and full check; |
| 0.6.7 | 2026-10-21 | Dashboard: front tabs Cover (with the status of the linked data tables, was sheet DataLinks), ScenarioCompare (every user entry: Live or Stored results, year... |
| 0.6.6 | 2026-10-21 | Speed: the workbook ships with its calculated values and opens in manual calculation (no recalculation on open; |
| 0.6.5 | 2026-10-20 | Linked data tables, first one (prototype): sheet DataLinks with a data-source dropdown (Embedded = shipped data, default; |
| 0.6.4 | 2026-10-20 | Dashboard on ScenarioCompare: every macro button there (none on the reference tab); |
| 0.6.3 | 2026-10-20 | Excel repair fixed: Excel repaired every earlier version on open ("Named range from /xl/workbook.xml"): the comment of the LAMBDA name FUELUSE had 305 charac... |
| 0.6.2 | 2026-10-20 | User decisions 2026-10-20: subsidy reforms always separate from the before-tax build-up: the producer subsidy phase-out is the wedge ppsw (block) / psw (subs... |
| 0.6.1 | 2026-10-20 | Open items without new data: I49 producer subsidies enter the supply cost as legacy (rows psd, psu, block row psp; |
| 0.6.0 | 2026-10-19 | Consolidated release of v0.5.0-v0.5.7 (full rebuild, full check). |
| 0.5.7 | 2026-10-19 | Results blocks (item 8 A+B): 14c NDC comparison (sheets NDCs and GHGHist from legacy; |
| 0.5.6 | 2026-10-19 | Also: Settings C27, C36-C39 read MTInputs; |
| 0.5.5 | 2026-10-19 | Register and documents: cell-level fix plans for the 15 engineer-power bugs (legacy_bugfix_plans); |
| 0.5.4 | 2026-10-19 | Power engineer features (PowerFeatures_Plan P1, P2, P4): every MTInputs power input read in the scenario's own column (section-1 rows; |
| 0.5.3 | 2026-10-19 | Full check repaired (independent Python power data step with the v0.4.10 fixes L52-L55, missing recomputations, stale expectations); |
| 0.5.2 | 2026-10-19 | Whole legacy Manual inputs tab at the legacy addresses (17 blocks, rows 5-378; |
| 0.5.1 | 2026-10-18 | Residential LPG and kerosene always exempted (MTInputs AlwaysExemptResLPGKer, per scenario: no new carbon tax, ETS or excise, nor their VAT; |
| 0.5.0 | 2026-10-18 | Release 0.5.0 (user: bump everything to v0.5.0, consistent): the overnight decisions of v0.4.15-v0.4.16 consolidated; |
| 0.4.16 | 2026-10-18 | User decisions: consumer subsidy and price-control phase-outs and producer subsidies as separate policy lines by sector and fuel (LD18, LD19; |
| 0.4.15 | 2026-10-18 | User decisions: ETS benchmarks = 1 - the MTInputs auctioned share (I21); |
| 0.4.14 | 2026-10-18 | Power: new capacity sized for next year's required generation, when it comes online (legacy bug L67, was issue I8; |
| 0.4.13 | 2026-10-18 | Residential biomass grows with income only if MTInputs BiomassNormal = Yes, as legacy (I24); |
| 0.4.12 | 2026-10-18 | User decisions: income factor on the GDP elasticity of fuel use as legacy (was I23); |
| 0.4.11 | 2026-10-18 | Bugs and issues split (user decisions): CO2 calibrated to the inventory as legacy (switch on; |
| 0.4.10 | 2026-10-18 | Legacy bugs no longer replicated (user rule): L14 pass-through applied once (prices); |
| 0.4.9 | 2026-10-17 | Faster full build (user rule: the full build as fast as possible): the baseline CO2 refresh and the emulation of RunAllScenarios run in one LibreOffice sessi... |
| 0.4.8 | 2026-10-17 | Distribution readability (user request): every section shows its band, its summary row last and one blank row (one row group per section; |
| 0.4.7 | 2026-10-17 | Power data from the legacy tabs (user request, align fully): legacy Power and CoC tabs at legacy addresses (and GHGs, for the 2023-2024 shocks); |
| 0.4.6 | 2026-10-17 | Data tabs aligned more fully (user request): legacy tabs with several tables kept at their legacy cell addresses (Countries, Elasticities, ETS+LTS, Multiplie... |
| 0.4.5 | 2026-10-17 | Data tabs aligned with legacy (user request): grouped and ordered as legacy (DATA_MITIGATION, DATA_DISTN, DATA_TRAN, DATA_OUTPUT, then DATA_OTHER); |
| 0.4.4 | 2026-10-17 | Distribution module (user decisions): sheet Distribution with one analysis year (MTInputs YearDistn) and deciles across, the scenario groups and LAMBDA test ... |
| 0.4.3 | 2026-10-17 | LAMBDA test group (user rule): scenario groups 1 and 2 hold plain formulas in every year (2041 included); |
| 0.4.2 | 2026-10-16 | Presentation (user requests): Cover tab as legacy (contents, cell and tab colours, abbreviations); |
| 0.4.1 | 2026-10-16 | Layout (user requests): every section numbered (0-18) and rolled up to its summary row(s), detail and lettered sub-blocks before the summary; |
| 0.4.0 | 2026-10-16 | Release 0.4.0: v0.3.18 renumbered as 0.4.0 (files, labels and references); |
| 0.3.18 | 2026-10-16 | Kaya identity on total primary energy supply as legacy (row 18880): fuel use incl. |
| 0.3.17 | 2026-10-16 | New section 18 Welfare and externalities, climate part: SCC options and selection as legacy (target-consistent, Ricke national and global from sheet SCC, man... |
| 0.3.16 | 2026-10-16 | Sub-block 16b External balance: change in net energy imports by fuel and group (change in use x supply price x import share), energy trade balance (legacy ro... |
| 0.3.15 | 2026-10-16 | New section 17 Carbon pricing: implicit carbon price by fuel and economy-wide (legacy F5d), effective carbon rate and effective carbon tax (F5e, row 16137), ... |
| 0.3.14 | 2026-10-16 | Sub-blocks 11b (energy change by fuel and sector, %), 13b (CO2 change, grid emission intensity, Kaya identity as legacy F14), 14b (GHG change by category and... |
| 0.3.13 | 2026-10-16 | Header rows: real GDP (USD, moved up from section 16; |
| 0.3.12 | 2026-10-16 | Section 15 hand-off as the air-pollution module input table (legacy rows 15859-15961): one block per module sector, pollutants in legacy order, CH4 added (co... |
| 0.3.11 | 2026-10-16 | Replicated from legacy: the 2023-2024 fuel-use shock on every fuel row and on power demand (header row 11, Settings C19 on; |
| 0.3.10 | 2026-10-16 | Section 2 memo (I31): per fuel, electricity and all energy: spending, fuel use, average price (unit value, legacy F5b), Laspeyres price index against scenari... |
| 0.3.9 | 2026-10-16 | Style guide (NORMS 2): two blank rows before each section band and one after, one between blocks, two before a sub-section; |
| 0.3.8 | 2026-10-15 | Rebuild of v0.3.7 from the merged builder: the v0.3.7 defaults (prices to 2022, ETS benchmarks 1.0) with the LAMBDAs SCALEBY and SHAREOF. |
| 0.3.7 | 2026-10-15 | Excel repair error fixed: Excel 365 removed the cell formulas calling the LAMBDAs SCALE and SHARE (sheet Mitigation); |
| 0.3.6 | 2026-10-15 | Tabs consolidated (user request): Inputs = Inputs + Inputs_prices + Inputs_power; |
| 0.3.5 | 2026-10-14 | Engineer road transport model (legacy section 5 with 17 bugs fixed, Transport_vs_Legacy.md) as section 5b of every scenario group: data sheets Transport1-3, ... |
| 0.3.4 | 2026-10-14 | No numeric literal in any formula: pass-through buckets, GJ per kWh, capex average share and dispatch tie breaker are named constants (sheet Constants); |
| 0.3.3 | 2026-10-14 | No country-specific number outside the reference tables: ETS semi-elasticities from sheet ETSSemi (legacy ETS+LTS, 175 countries) by country instead of typed... |
| 0.3.2 | 2026-10-14 | Energy CO2 calibrated to the GHG inventory: every CO2 EF (Inputs, Inputs_power) x EFCalib (Settings C27-C30) = inventory energy CO2 / scenario-1 energy CO2 w... |
| 0.3.1 | 2026-10-14 | GDP effects: new section 16 (fiscal space = new-policy revenue above scenario 1; |
| 0.3.0 | 2026-10-14 | Air-pollution module inputs in section 15: the seven pollutants by air-pollution sector (coal, gas and other power plants, ground level road, ground level ot... |
| 0.2.9 | 2026-10-14 | Local air pollutants: new section 15 (PM2.5, NOx, SO2, VOC, black and organic carbon, CO by subsector and power; |
| 0.2.8 | 2026-10-14 | Non-CO2 GHGs and methane: new section 14 (methane by source with the methane fee and its abatement curves, combustion CH4 by sector, GHG inventory categories... |
| 0.2.7 | 2026-10-13 | Excel repair error fixed: LAMBDA parameters y1, co2, c, tco2_kwh read as cell references, so Excel removed the 2041 cells calling them (2041 power fell to 0); |
| 0.2.6 | 2026-10-13 | Formatting: each price block opens with a parameter table (heading row, parameter row pset) and the international reference price (gpi) and fixed part rows, ... |
| 0.2.5 | 2026-10-13 | Section 2 as a price build-up by fuel (heading row) and sector (block): fixed part of the supply cost (new row spf), supply cost, excise and other taxes befo... |
| 0.2.4 | 2026-10-13 | Mitigation: years in row 1; |
| 0.2.3 | 2026-10-12 | Last year 2041 (legacy horizon) as the LAMBDA year: every calculated cell of 2041 calls its named LAMBDA; |
| 0.2.2 | 2026-10-11 | One version number (0.2.2) for the workbook, scripts, method notes, VBA module, documents and deck; |
| 0.1.09 | 2026-10-11 | Existing carbon pricing (sheet ECP: legacy data for 52 countries, none for Egypt; |
| 0.1.08 | 2026-10-11 | Works without LAMBDA support: plain formulas (at most 100 characters) in every cell, the right column (2040) included; |
| 0.1.07 | 2026-10-11 | Short formulas: every cell formula has at most 100 characters (defined names for the data tables, helper rows and columns, policy rates by sector in section ... |
| 0.1.06 | 2026-10-10 | Power engineer model: demand, dispatch, retirement and capacity, investment (legacy H, I, K, L) with D6, D9, E1; |
| 0.1.05 | 2026-10-10 | Power sector, price side: section 3 with legacy sub-tables A, B, C, D, E, G, J (generation costs by type, average generation cost, storage cost of variable r... |
| 0.1.04 | 2026-10-10 | First-run test for Excel: macro CheckBatchRun (lookups, baseline recalculated by the host vs stored, batch rerun vs stored values) with its report on the new... |
| 0.1.03 | 2026-10-09 | Multiple scenarios: scenario definitions on MTInputs (combined packages), VBA module CPATScenarios (batch run with ETS goal seek, results stored as values), ... |
| 0.1.02 | 2026-10-09 | New ETS with a cap: baseline covered emissions (data from scenario 1), fast price estimate, override row and goal-seek script; |
| 0.1.01 | 2026-10-09 | MTOutputs sheet: key results per scenario by output code (copy-pasteable row blocks); |
| 0.1.00 | 2026-10-09 | Renamed CPAT-AI-Mitigation-Prototype and upgraded to v0.1.00 (content as v0.0.16). |
| 0.0.16 | 2026-10-09 | Layout: one level of column groups (B:G, I:K, 2030-2039 per scenario); |
| 0.0.15 | 2026-10-09 | Layout: columns B:C and I:K grouped (D:G nested), row group buttons below, opens rolled up; |
| 0.0.14 | 2026-10-09 | Corrected Egypt price block (user); |
| 0.0.13 | 2026-10-09 | CO2 emissions from fuel combustion per subsector and fuel (fuel use x EF); |
| 0.0.12 | 2026-10-09 | Revenues: existing tax revenue, existing subsidy cost and new-policy revenue as separate calculations per subsector and fuel; |
| 0.0.11 | 2026-10-09 | Horizon 2040; |
| 0.0.10 | 2026-10-08 | Other oil products treated like the other oil products (pass-through and margin from data); |
| 0.0.9 | 2026-10-08 | Domestic price projection (legacy method) in section 2: international prices by source, supply cost, excise and other taxes with pass-through, retail price b... |
| 0.0.8 | 2026-10-08 | Shadow price on the efficiency margin of fuel use; |
| 0.0.7 | 2026-10-08 | Legacy CPAT section layout (1 Policies, 3 Power, 5-8 sectors, 11 Results; |
| 0.0.6 | 2026-10-08 | MTInputs sheet per scenario; |
| 0.0.5 | 2026-10-08 | White band text; |
| 0.0.4 | 2026-10-08 | Row outline: blocks roll up. |
| 0.0.3 | 2026-10-08 | Variable codes in column A; |
| 0.0.2 | 2026-10-08 | Inputs sheet by fuel/subsector (lookups separated from formulas); |
| 0.0.1 | 2026-10-08 | First build: design 2 price -> fuel-use prototype, Egypt base data, 2 scenarios. |

## CPAT-AI Distribution Prototype (standalone module, `excel_ai/distribution/`)

| Version | Date | Change |
|---|---|---|
| 1.0.4 | 2026-10-29 | Cut from the mitigation prototype v1.0.4 (outputs tab MTOutputs in the legacy layout); versions aligned. Values unchanged. |
| 1.0.3 | 2026-10-29 | Cut from the mitigation prototype v1.0.3. Update from Mitigation looks in `permalink_countryeditable\` (next to the workbook, then one folder up) before `permalink\`; in `permalink_countryeditable/` it reads the Mitigation copy beside it. Values unchanged. |
| 1.0.2 | 2026-10-29 | Cut from the mitigation prototype v1.0.2 (versions aligned with Mitigation and Coded CPAT; ScenarioDefinition has the input row ModelForm). Distribution method and values unchanged. Replicated by Coded CPAT 1.0.2p1.1. |
| 1.0.0 | 2026-10-29 | First full release (user 2026-10-29), cut from the mitigation prototype v1.0.0: Distribution 0.1.4 as released. Replicated number for number by Coded CPAT 1.0.0p1.0. |
| 0.1.4 | 2026-10-29 | Cut from the mitigation prototype v0.9.2: bug M22 fixed (found by Coded CPAT): the 25th/75th percentile recycling rows (hrec) add the public investment amount per person (pui of the sample, LCU), not its % row. |
| 0.1.3 | 2026-10-29 | Cut from the mitigation prototype v0.9.0 (remaining functionality, reverts to legacy, data from legacy 465, last historical price year 2024); the Distribution method unchanged. |
| 0.1.2 | 2026-10-29 | Cut from the mitigation prototype v0.8.5 (combustion emission factors as legacy, issue I98; data problems as issues). |
| 0.1.1 | 2026-10-28 | Cut from the mitigation prototype v0.8.4: ScenarioDefinition on the rows of legacy 465 with a complete set of names (bug L137, issue I87); the mitigation workbook is looked for in permalink/ too; file named _v0.1.1 at the top of excel_ai/ (NORMS 5a). |
| 0.1.0 | 2026-10-22 | First standalone module, cut from the mitigation prototype v0.8.1; input from Mitigation by the button Update from Mitigation (section 19a). |
