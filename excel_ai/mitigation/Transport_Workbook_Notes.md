# Engineer road transport model in the workbook: implementation notes (CPAT-AI-Mitigation-Prototype v6.4)

Phase 3 and 4 of `Transport_Plan.md`: the engineer road model of legacy CPAT, with the bug fixes of
`Transport_vs_Legacy.md`, as section **5b** of the Mitigation sheet (`build.py`), checked row by row against
the Python reference `transport_model_ref.engine(..., fix=ALL_FIXES)` (`check_full.py`). The method itself is in
`Transport_Reference_Notes.md`; this note covers the workbook layout, the names, the switch and the deviations.

## 1. Section 5b on Mitigation

Band row 1684 (`5b. Road engineer model`), directly after section 5 (Transport); summary row 2635 `trsum` (road fuel
and electricity use of the engineer model, ktoe), visible when the section is rolled up. 855 rows with year values or
parameters, 75 label rows (a label row names the D:G parameters above every run of rows of one variable that has D:G
values; the ScenarioDefinition rows share one), 19 heading rows. Row keys are the legacy row numbers (baseline numbering) where a
row reproduces one; other keys name helper rows (`R_TR` in the builder; layout `TR_LAYOUT`).

| Rows | Block | What it computes |
|---|---|---|
| 1685-1691 | Switch and timing | `TrModel` (ScenarioDefinition row 340), `tr.sw` = 1 if Engineer (`ENGINEERON`), `tr.dk` data year (Transport1 has the year, 2022-2025), `tr.col` years from the base year, `tr.pol` policy scenario (scenario number > 1, fix B1) |
| 1692-1755 | Policies | 62 ScenarioDefinition rows (feebate, distance tax, EV subsidy, ad-valorem and customs taxes, VAT on BEVs, charging-station subsidy; by class) |
| 1756-1808 | Parameters (D:G) | Lifetimes, depreciation, insurance, maintenance, elasticities, logit k, ownership (adjustment, Gompertz, limits; decline `TrOwnDecline`, fix B4), freight distance limits, charging and range anxiety, discount rate, ICE split elasticities, data years, road elasticities and AEI (Inputs), GWh per ktoe, VAT on vehicles, GJ and liters per ktoe, EFs (road, fix B7), base-year energy balance |
| 1809-1888 | Key inputs | Transport1 lookups (data years, blank = 0), BEV fuel-economy and charging-cost paths, vehicle prices (Transport2, last price carried) |
| 1889-1911 | Derived parameters | Base-year split of road fuel by vehicle type (share, ktoe, bln liters), purchase taxes (customs year), bus fuel of the base year |
| 1912-1928 | Inputs from the model | Road prices incl. new policies in $/liter, gas, PHEV and freight prices (net of VAT), industrial gas price, population, GDP per capita, lagged GDP growth (fix B2), consumer discount rate |
| 1929-1996 | Data-year derivations | Legacy rows 2038-2137 (blends, distance and vehicle shares, freight share and the 2-3 wheeler hump; held values `trnc`, `trjc`: last data year, fix B3b) |
| 1997-2068 | Stocks | Opening, trailing-average stock, retirement, after retirement, purchases, data-year adjustment, closing (passenger new and used, freight, 2-3 wheelers) |
| 2069-2080 | Charging and range anxiety | BEV stock, charging subsidy (fix B10), stations, mark-up, EV electricity price (last year's power price), range anxiety (Transport3) |
| 2081-2151 | New fuel economy | Fuel mix, prices incl. vehicle feebate per liter, new fuel economy, CO2 intensity; used vehicles |
| 2152-2195 | Distance for the purchase | Distance tax (fix B1), cost per km, distance per new and used vehicle |
| 2196-2304 | TCO | Discounted km, feebate pivots (average and manual rows, then the one used), taxes (`POLPICK`), subsidies, prices after taxes, depreciation (fixes B8, B8w, B20), insurance and maintenance (B19), fuel, range anxiety (no PHEV range anxiety, B23), TCO per km |
| 2305-2430 | Demand and choice | Gompertz demand with two-sided calibration at the last data year (B3), purchases, logit EV choice, ICE fuel split (B9), vehicles |
| 2431-2494 | Stock fuel economy, uncalibrated use | Opening and closing stock fuel economy, cost per km, distance per vehicle, fuel use before calibration |
| 2495-2508 | Calibration step 1 | Bottom-up base-year use incl. buses (/(1 - bus share), B6b), factor by fuel, distance factors by class (held) |
| 2509-2569 | Calibrated distance and fuel | Distance per vehicle, fuel use, CO2, BEV stock fuel economy, electricity (B8, B21) |
| 2570-2583 | Buses | Passenger fuel and electricity in ktoe, bus fuel and electricity (B6) |
| 2584-2629 | Step 2 and results | Calibration factors by fuel (held), **road fuel use by fuel 2598-2601 (ktoe), biofuels 2603, electricity 2604**, distance, fuel use by class, average fuel economy (B22), vehicles |
| 2630-2634 | Range anxiety fit | EV sales share calculated - actual (data years) |

Every calculated row has one formula per row for the base year, 2023-2040 and 2041; 2041 calls a named LAMBDA (light
beige), 2023-2040 hold its body with the arguments substituted (at most 100 characters). Rows whose base year is
data or a held base-year value have their own base-year formula (95 rows); the values of the base year that a formula
reads from the previous column (the code column) are guarded by `IF` or `N()`. Held values (calibration factors, base-
year distance split, last-data-year values) carry forward from the previous column, so no cell reads a later
column. References are relative in the row (column-relative copy across years and scenario groups).

## 2. Names, LAMBDAs, constants, data sheets

- 80 new LAMBDAs (`TR_LAMBDAS`, notes in `TR_LAMBDA_NOTES`): ENGINEERON, TRDATA, TRBLEND, OPENING, TRAILAVG, LAGVALUE,
  RETIRED, MARKUP, STATIONS, RANGEANX, NEWFE, FEEBATE, RATIO, WAVG, MIXTWO, GROWVKT, CLAMPVKT, USEDVKT, DISCKM, COSTKM,
  DISTTAX, CSRAMP, PIVOTAVG, PIVOTMAN, PIVOTPICK, FBVEH, GROSSUP, POLPICK, EVSUB, ANNUITY, SALVAGE, RESALE, INSMAINT,
  FUELKM, TOTAL, TOTALRA, TCOFUEL, LOGITICE, ACTSHARE, REST, ACTORCALC, OWNEXP, GOMPTGT, OWNDEM, CLAMPOWN, PLUG, ADDTHREE,
  TURNOVER, NEWINSTOCK, CROSSRATIO, ICESPLIT, NORMSH, OWNSH, PERTH, OPENFE, STOCKFE, VKTFUEL, TWOFUEL, BEVFENEW,
  BEVFEOPEN, PHEVELE, EMITFUEL, INTENSITY, INTENS0, KTOE, KTOEELE, BUSFUEL, BUSELE, AVGFE, AVGFEEV, PROD3SUM, BIOSCALE,
  HOLD, DISCRATE, FRESHARE, CYCHUMP, BEVUPLIFT, INTAVG, ROADSWITCH, DEMROAD. Reused: SCALEBY, DIFF, SHAREOF, ADDED, POSTTAX.
- Named constants (sheet Constants): Thousand, Million, Billion, TrRALag (3: range anxiety holds its start value for
  three years), TrPivotLag (2: feebate pivot blank in the first two years), TrOwnDecline (0.1, fix B4), TrFEWGso,
  TrFEWHalf, TrFEWEvP, TrFEWEvO (fixed weights of the average fuel economy without fuel use).
- Data sheets (DATA group): Transport1 (`TrKey`, `TrVal`, `TrYr`; key country|variable), Transport2 (`VPKey`, `VPVal`,
  `VPYr`), Transport3 (`RAKey`, `RAPas`, `RAFre`, `RACyc`, `RAPasA`, `RAPasC`, `RAFreA`, `RAFreC`, `RACycA`, `RACycC`),
  TransportParams (`TrParKey`, `TrParVal`), TransportPaths (`TrPathKey`, `TrPathVal`, `TrPathYr`); `TrFuelKey` = column
  B of the result rows 2598-2603 (position of a fuel for the switch).
- Mapping: sector labels pas, pau, lgt, fre, cyc, bus; fuel labels phv, bev, ev, ice. Variables: 552 new entries
  (550 section-5b variables, `trsum`, `enel`).

## 3. ScenarioDefinition rows

Template rows 1-415 unchanged; row 417 heading; rows 418-479 the transport policies (`TR_MT`: per class passenger /
freight / 2-3 wheeler: feebate year, rate, pivot type, manual pivot, pivot decline; distance tax year, start, target
year, target; EV subsidy year, amount, change; ad-valorem tax ICEV and BEV baseline and policy, its year; customs
year; then VAT years (passenger, 2-3 wheeler), VAT and customs policy factors, charging-subsidy start year and level,
target year and level). NameOfParameter `Tr<Stem><Pas|Fre|Cyc>` (e.g. `TrSubAmountPas`); defaults are the legacy
Dashboard values (`data/transport_params.csv`), all policies off. Every scenario column gets them; Mitigation finds
them through the Mapping table (`MT_KEYS`) like the other ScenarioDefinition rows. All ScenarioDefinition ranges end at row 479
(`MT_END`: Mapping, Variables lookups, `mt_lookup`, `mt_setting`, the batch emulation; macro constant `MT_LAST` in
`CPATScenarios.bas`). The Mitigation search range grows to row 8000 (`MIT_MAX`, macro `MIT_MAX_ROW`).

## 4. Switch wiring

- Section 5: the elasticity fuel use is now variable `enel` (the former `ener` formula, `FUELUSE`, base year from
  Inputs). `ener` = `ROADSWITCH($D, tr.sw, result rows 2598:2603, enel)`; D = Inputs column `trpos` = position of the
  fuel in `TrFuelKey` for road (gasoline 1, diesel 2, LPG 3, gas 4, biofuels 6), 0 elsewhere. With `TrModel` =
  Elasticity (default) `ener` = `enel` everywhere, so every v3.4 output is unchanged (regression 0). With Engineer the
  road gasoline, diesel, LPG, gas and biofuels of section 5 are those of section 5b in every year (base year: the
  calibrated value = the energy balance); CO2, revenues, CH4, air pollutants and the totals follow.
- Section 3 H: `dem` = `DEMROAD($F, tr.sw, road electricity 2604, previous, multiple)`; F = Inputs_power column `tr`
  (1 for road). From 2023 road electricity demand is the engineer value when switched on (base year: the data).
- Biofuels: road biofuels = base year x (gasoline + diesel) / base year of the engineer model (`BIOSCALE`).
- No circular reference: the engineer model reads the power price of the previous year (base year: same year), GDP
  growth of the previous year and the GDP level after the feedback (which uses last year's effect); fuel prices do not
  depend on fuel use.

## 5. Deviations from the reference and why

The reference engine is reproduced exactly (section 6); the deviations are in the inputs it gets from the prototype:

- 2-3 wheeler gasoline price: the road gasoline price incl. new policies (as passenger); legacy row 4438 uses the
  price before new policies, so carbon pricing did not reach 2-3 wheelers.
- VAT on vehicles: VAT_WEO of the customs year from Prices_dom (Egypt 0.14; the legacy run had 0.1531).
- Industrial gas price for LNG trucks: section 2 industrial price + the road new policies (POSTTAX).
- Biofuels: the prototype keeps biofuels as a fuel; the engineer EF adjustment for blending is 1 and road biofuels scale with
  engineer gasoline and diesel.
- Formulas: the charging-subsidy ramp is written as start + (target - start) x MIN(1, (year - start year) / MAX(1,
  target year - start year)) (same values; no division by zero when the two years are equal); the cross-TCO ratio of
  the ICE split uses IFERROR for "other fuels without share" (blank, as the reference's guard); the average EV fuel
  economy uses a helper row (`trafen`); the price-response switch of the purchase distance is a 0/1 parameter. All
  for the 100-character limit; values identical.
- Road electricity in the base year of section 3 H stays the data (the engineer value replaces it from 2023).

## 6. Check results

`check_full.py` (report `check_report_v6.4.md`):

- Section 5b against `transport_model_ref.engine(fix=ALL_FIXES)`, inputs from the Python recomputation (an
  independent copy of the input mapping, `tr_inputs`): every row with year values and the side-table parameters
  (base-year split, purchase taxes, bus fuel), scenarios 1 and 2, as shipped and with the Lambdas library over every
  row: max relative difference about 4e-14.
- Copied scenarios with TrModel = Engineer (11: copy of 1; 12: copy of 2, carbon tax; 13: + EV subsidy; 14: +
  distance tax; 15: + subsidy, distance tax, feebates, charging subsidy): section 5b vs the engine (max 5e-14) and
  the whole model vs the Python recomputation with the engine's road fuels and road electricity (iterated to the
  fixed point; max 7e-12). Road fuels of section 5 = section 5b; road electricity demand = section 5b from 2023.
- Directions (2035 unless noted): carbon tax lowers road fuel use (24,580 -> 22,564 ktoe); EV subsidy raises the
  passenger EV sales share in 2030 (0.55% -> 3.3%); distance tax lowers passenger distance (285 -> 183 bln km); all
  policies of 15 lower road fuel use (22,564 -> 14,177 ktoe).
- Regression vs v3.4: 0 on every shared output code (Elasticity by default); new variables reported as added.
- The scenario-copy test (copy of 2 with carbon price 0 = scenario 1) skips the row `tr.pol` (scenario number > 1),
  as it skips the scenario number itself.
- Python interface changes needed for the check: `power_model_ref.engine` takes an optional
  `inp['dem_fixed']` (road demand from the engineer model; default behaviour unchanged).
