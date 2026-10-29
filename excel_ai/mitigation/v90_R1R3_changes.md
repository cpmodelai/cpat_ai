# v9.0 group R1R3: changes for the integrator

Items: R1 (section 17b), F (output blocks 5b and 15), R2 (section 18: social costs and benefits, full welfare,
subsidies), R3 (Pigouvian taxes in section 1, efficient prices in section 18). Spec: `Equations_addendum.md` B, C (R3),
F; evidence: `Equations_addendum_notes.md` B, C. Bug and issue numbers as in the notes (the addendum's placeholder
codes L-R2-1 .. L-R2-13 are L176 .. L188 of the notes).

## What is built (build.py)

- **Section 1 (policies)**: the SCC options and selection (`scc.tgt` .. `scc.glo`, same codes) **moved here from section
  18** (section-18 references go through aliases in `R_WEL`); the four MTInputs inputs `AddEfficientTaxes`,
  `ClimateEffTax`, `AddEfficientTaxesPhaseInYears`, `ExternalityAddVAT` are now read (they existed, unread); new rows by
  price fuel (the 14 of PRICE_FUELS): `pig.phi` (R3.1), `pig.ap` (R3.4), `cc.code` (R3.2-R3.3), `pig.tr` (R3.5), `pigx`
  (R3.6), `ntxg` (R3.7), `xcpb`, `xpre` (R3.8), `ntxb` (R3.9). `ntx` [f,s] and the power cost `ccp` read `ntxb` instead
  of `fpr` (R3.10, R3.11); electricity `entx` unchanged (R3.12, I119: electricity Pigouvian 0).
- **Section 5b**: new rows `trq` (road and total use by fuel, gasoline, diesel, LPG, gas, electricity; switched model)
  and `tran.rsh` (road share) under a heading "Outputs to the transport co-benefits module". Vehicle-km, fuel economy and
  class use were there already.
- **Section 15**: new block `apen` (energy use of power generation by type and residential by fuel, ktoe) and `apco2`
  (energy CO2 reference).
- **Section 17b (new band, between 17 and 18; summary row: modelled ambient PM2.5 `air.con.pm2.mod`)**: typed
  `airpol.cost` (T1), `airpol.cost.gj` (R1.2-R1.3), fuel use by sector group `fuq`, modelled PM2.5 by module sector
  (R1.5, coefficients x section-15 emissions), `air.vpm` (T3), `tran.*.km` (T4), class use / passenger weight of
  scenario 1 / driving share / freight share (R1.7-R1.9), `tran.acc|con|rdm.cost` per litre (R1.10), per GJ (R1.11),
  `pig.trs` (transport externalities per litre for the Pigouvian tax).
- **Section 18**: `cc.nat`, `cc.glo` per GJ (R2.1), `airpol.ecy` (R2.2), weights `apq` and other-use costs (R2.3),
  `tot.ext` (R2.4), `wel.air.usd`, `wel.rod.*` (R2.5-R2.6), `wel.air.pct`, `wel.rod.pct` (R2.7), **`wel.usd` redefined**
  (R2.8), FFS lines and totals (R2.9-R2.10), the 16 subsidy lines x 8 variables and totals (R2.11-R2.12), efficient
  prices by the 12 price fuels (R3.13-R3.21) and the weighted averages (R3.22).
- **New sheet Inputs_cob** (merged into the Inputs tab): typed Egypt values T1, T3, T4 (key `EGY|...`, 2022-2041,
  bright yellow `F_CHANGED`) and the concentration coefficients T2 (pollutants down, module sectors across). Names
  `CobKey`, `CobVal`, `CobYear`, `CobKap`. **Inputs_ef**: generic CO2 factor table by fuel (legacy 961-967; names
  `EFGenKey`, `EFGen`). Name `VatGen` = VAT_WEO of the base year (Inputs_prices).
- **Sheet BaselineCO2**: three more stored scenario-1 rows (`R3_STORE`: `apcr` residential coal AP cost, `trgso`,
  `trdie` transport externalities per litre), written by `fast_batch` / `write_bco2` like the CH4 rows. The Pigouvian
  tax reads them, because reading the scenario's own fuel use would be circular through ntx (and the quick check's rule
  "lvc levelises inputs only" forbids any section-5+ row behind `ccp`). In the quick build they are empty (0): with
  AddEfficientTaxes = Yes the quick file's Pigouvian tax lacks the transport part until a full build fills them.
- `MIT_MAX` 9000 -> 12000 (rows now reach 9230); **CPATScenarios.bas `MIT_MAX_ROW` 9000 -> 12000** (changed, the build
  asserts equality). `VR1` (Variables rows) 1200 -> 1400.
- check_full.py: `wel.usd` expectation adds the co-benefit rows (read from the sheet). Not updated (no effect on the
  default scenarios): the Python `ntx` and `ccp` (d5) still use `fpr` without the [scenario > 1] factor and without the
  Pigouvian netting; no Python re-computation of the new 17b/18 rows (to add: R1.10, R2.11, R3.17 are cheap).

## Quick check

PASS (see report). Output codes against the HEAD quick build: the only changed shared codes are `wel.tot.2` and
`wel.pct.tot.2` (wel.usd now adds the air-pollution and road co-benefits; scenario 1 unchanged = 0); 1,212 new codes.
Every other shared code is identical (AddEfficientTaxes defaults to No*; `ntxb` = [scenario > 1] x `fpr`, and the
default scenarios have no fuel price reform). A test with AddEfficientTaxes = Yes in scenario 2 recalculates without an
error value (Pigouvian per litre 2030: gasoline 0.187, diesel 0.339 $/l, other oil 54.8 $/bbl; coal power 6.37 $/GJ).

## Egypt comparison (legacy 465 cached values; legacy scenario 2 is a small carbon tax, ours $20)

Per-unit rows (scenario-independent or 2022) match legacy:
- transport per litre 2022: acc gso 0.04237 (legacy 0.042386), con gso 0.035938 (0.035952), acc die 0.013369
  (0.013174, -1.5%: 5b class weights), con die 0.01134 (0.011174), rdm die 0.148525 (0.148468), acc nga 0.000444
  (0.000444); 2026 acc gso 0.032194 (0.032205); 2030 +1% (prototype road model).
- `airpol.ecy` (R2.2, L177 fixed) 2022 0.008818 (notes: 0.00882); `airpol.ecy.g` (R3.15, as legacy) 0.011034
  (0.0110344).
- climate cost coal 5.272 $/GJ (5.27208); `tot.ext` gso 3.978 $/GJ = 0.1391 $/l (0.139122), die 10.483 $/GJ = 0.3906
  $/l (0.39055).
- efficient prices 2022: gasoline 1.40343 (1.40346), diesel 1.84099 (1.84052), LPG 1.64460 (1.6446), kerosene 2.12186
  (2.12185), coal ind 18.7686, res 29.199, pow 19.3211 (all equal), gas ind 15.6125 (equal), gas pow 15.1054 (equal),
  gas res 22.790 (22.7498: L189 fixed, +0.0356 x 1.14); Pigouvian gasoline 0.26819 (0.268223), diesel 0.53834
  (0.537921); CO2e gasoline 113.84 (113.857). **Electricity efficient prices differ**: ind 0.1086 (0.0747), res 0.1523
  (0.0802): the prototype power model's supply cost `sc` 2022 is ~0.098 $/kWh against legacy ~0.064 (not this group).
- subsidies, scenario 1, 2022: explicit gasoline 3.2148 (3.21727), diesel 11.320 (11.3289), LPG 4.338 (4.3415), oop
  4.389 (4.38892), gas ind 3.2113, res 0.9864, pow 10.729 (equal); implicit gasoline 3.905 (3.90868), diesel 9.316
  (9.31645), LPG 8.515 (notes, L184 fixed: 8.52), oop 5.211 (fixed 5.11), gas ind 1.5545, res 0.4741 (0.4708, L189),
  pow 4.4599, coal ind 0.5043, coal res 0.00040 (fixed 0.00040). Differences: kerosene explicit 0.0029 (0.2737; the
  prototype's kerosene excludes jet fuel, and L186), **electricity explicit res 7.76 + ind 1.41 bn (legacy ~0)** and
  implicit res 2.18 (0.43), from the same power supply-cost difference; totals 2022 explicit 47.56 (38.65), implicit
  36.21 (39.55).
- **Modelled PM2.5**: gas plants 1.6458, other plants 2.7429, road 7.1316 (all equal to legacy AP 975-977 in 2022),
  ground level 7.666 (7.680), industry and other 11.14 (8.23), **food & forestry 85.28 (legacy 2.74)**: the section-15
  food & forestry emissions of the prototype are far above the legacy AP input (BC 2,199 t against 3.8 t; NOx 40 kt
  against 5.5 kt; SO2 0.78 kt against 3.3 kt): total 115.6 against 30.2 ug/m3, and the food & forestry change drives
  `wel.air.usd` (2030: 3.76 bn for the $20 tax). To decide: the section-15 food & forestry block (LD53) against legacy
  E3 rows; candidate issue or bug for the integrator.

## Deviations from the addendum (and why)

1. **Codes** follow the prototype order `<variable>.<sector>.<fuel>` (B = fuel, C = sector), e.g. `airpol.cost.ind.coa`,
   `pig.ap.pow.coa`, `expsub.con.res.nga`; totals use the member `tot` (C5). The R2.1 global-SCC rows are `cc.glo`
   (the addendum names both the R2 global row and the R3 $/pu row `cc.code`); `cc.code` is the R3 row ($/price unit).
2. **SCC rows moved to section 1** (same codes): the Pigouvian tax enters `ccp`, whose precedents must lie above
   section 5 (quick-check rule lvc). Not in the addendum.
3. **Pigouvian components read stored scenario-1 values** (`pig.tr` gso/die and `pig.ap` residential coal, sheet
   BaselineCO2): R3.5 asks for mf.1 (scenario 1); reading the scenario-1 group directly is a structural circular
   reference (ref range includes the own group) and breaks the lvc rule. Residential coal: the switch of R1.3 needs fuel
   use; scenario 1's switched cost is stored instead (legacy Egypt: 0).
4. R3.8 `xcpb` uses the generic EF and the ECP table row of a representative ECP sector of the block (pow, res, ind;
   all-sector blocks: gasoline and diesel trs, LPG, kerosene, biomass res, other oil ind).
5. R3.9 also applies [scenario > 1] when AddEfficientTaxes is off (legacy rows are policy-only); the default scenarios
   have no reform, so nothing changes.
6. R3.23 (year table at YearFuelPrices) **not built**: a row selecting a later year would read later columns (quick
   check: forward reads); it belongs to the output sheets (NORMS 3c). YearFuelPrices stays unread.
7. R1.11 per-GJ rows only for gasoline, diesel, LPG (gas and electricity are not priced per litre; nothing reads them).
8. R2.3 coal/gas "other": IFERROR(SUMPRODUCT/SUM, AVERAGE) (the AVERAGE fallback as specified, shorter formula); odo
   and oop.avg 0 when the weights are 0.
9. R1.5 uses one set of coefficients for every country (Egypt's); other countries read `air.vpm` = 0, so `wel.air` is 0.

## LegacyDiff rows (new; integrator assigns LD numbers)

| Type | Area | This model | Legacy | Why | Effect | Codes |
|---|---|---|---|---|---|---|
| Different (fix) | Welfare: co-benefits | wel.usd = climate + air pollution (value per ug/m3 x change in modelled PM2.5 of the prototype's emissions) + road co-benefits - efficiency costs | AP and Transport sheets' own runs (wel.air from AP 3217) | R2, user decision 2026-10-29; unit costs are average damages (I104) | wel.usd +co-benefits; Egypt $20: 2030 +3.9 bn | L189-L193, I104-I106, I111, I112 |
| Different (fix) | Social costs, FFS, subsidies | per-GJ climate costs, own-sector quantities, consumption-weighted other lines, GDP of the year | rows 17678-17951 with bugs | never replicate a bug | see Egypt comparison | L176-L188 |
| Same | Pigouvian taxes | option AddEfficientTaxes (default No), netting over existing taxes, phase-in from CPIntro | rows 111-160, 199-218, 8782-9012 | R3 | none by default | L194-L196 fixed; I113-I119 |
| Same | Efficient prices | by price fuel, every scenario group | live scenario only | R3.13-R3.22 | reference rows | I120, I121; L203 |
| Different | Electricity efficient prices and subsidies | power-model supply cost | legacy power cost | not this group | elec explicit subsidy 2022 9.2 bn vs ~0 | (power model) |

## Register status changes (issues_register / bugs)

- Bugs fixed in v9.0 (not replicated): L176, L177, L178, L179, L180, L181, L182, L183, L184, L185, L186, L187, L188,
  L189, L190, L191, L192, L193 (R1/R2); L194, L195, L196, L203 (R3). L197-L202 are R4 (CBAM, not this group).
- Issues replicated (cite): I100 (5b rows whatever TrModel), I104-I112 (R1/R2), I113-I121 (R3; I119 decided:
  electricity Pigouvian 0), I122 (switch texts: LEFT(x,3)="Yes").
- Candidate (new): food & forestry emissions of section 15 far above the legacy AP input (see above).

## Version-log sentence

v9.0 (R1-R3): section 17b with the typed Egypt inputs of the air pollution and transport co-benefits modules (sheet
Inputs_cob) and the costs per unit computed from the model; section 18 adds the social costs, the full welfare (air
pollution and road co-benefits), the fossil-fuel-subsidy environmental benefits, explicit and implicit subsidies and the
efficient prices; Pigouvian taxes as a policy option (AddEfficientTaxes, default No) in the new excise of the price
blocks; the SCC rows moved to section 1; sections 5b and 15 carry the rows the modules read.

## Caveats

- Typed values are Egypt only (legacy cached run, options frozen: I106); other countries 0.
- The quick build's BaselineCO2 rows are empty: the Pigouvian transport part (and residential coal AP) appear only in a
  full build (fast_batch fills them; the build cache fingerprint changes, so it recomputes).
- Food & forestry PM2.5 dominates the modelled concentration (see above): wel.air should be read with that caveat until
  section 15 is reconciled with legacy.
- Electricity subsidy and efficient-price lines inherit the power model's supply cost (higher than legacy's).

## New inputs / settings

- No new MTInputs or ScenarioDefinition rows; four existing rows now read (212, 216, 217, 218). `MT_LAST` unchanged.
- New named constants (sheet Constants): `EFOilIEA` (0.0733 tCO2/GJ, legacy row 967), `ApCoalResMin` (0.001, L192).
- New sheet Inputs_cob (in the Inputs tab); new tables on Inputs_ef; three rows on BaselineCO2.
