# Non-CO2 GHGs and methane: method (CPAT-AI-Mitigation-Prototype v6.4)

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

The model adds methane, nitrous oxide and F-gases to energy CO2 and covers every UNFCCC inventory category, so it reports total GHG emissions. It includes a methane fee, its revenue, and combustion methane for every sector.

Units: methane in kt CH4 where it is a physical quantity, otherwise Mt CO2e with IPCC AR6 GWP100 (fossil methane 29.8, non-fossil 27.2). GHGYear is the last year the country has in the inventory (Egypt: 2024).

## 1. Data

| Sheet | Content | Source |
|---|---|---|
| GHGs | Inventory by country, year, category (energy, industrial processes, agriculture, LULUCF, waste, other) and gas (CO2, CH4, N2O, F-gases), Mt CO2e | Legacy sheet GHGs |
| CH4Inputs | Methane abatement curves (a, b) by country and source; shares that split inventory methane by source; flared share | Legacy sheet CH4Inputs |
| EF_NonCO2 | Combustion emission factors (kt per PJ) by subsector, fuel and pollutant, base year and final | Legacy sheet EF_PM (GAINS) |
| UNPop | Population by country and year (thousands) | Legacy sheet UNPop (UN WPP) |
| Balances | Base-year production of gas, oil, coal | Legacy Mitigation rows 503-509 |

The non-energy elasticities (section 4) are on sheet `Manual inputs` K325:M327, the legacy addresses (agriculture, waste, other: population elasticity row 326, per capita income elasticity row 327; a text entry such as "na" counts as 0). Their values reproduce the cached results of the legacy run exactly: legacy Mitigation uses the same values (it never reads the manual cells: their formula is broken, `#REF!`).

## 2. Methane by source

Seven sources: oil and gas extraction, downstream gas, coal mining and biomass use (fossil methane, part of energy); livestock and rice (agriculture); waste.

1. **Allocation.** Inventory methane of each category in GHGYear is split between its sources. Fossil sources: weight = MIN(10 x the source's share of the four activities, the country's input share), normalized to sum to 1. Livestock and rice take their input shares; waste takes all waste methane.
2. **Activity.** Oil and gas: gas and oil production; coal: coal production (both held at the base-year balance). Downstream gas and biomass: total gas and biomass use of the scenario, power included. Livestock, rice, waste: an index (1 in the base year) that grows with income and population.
3. **Abatement.** Fee per tonne CH4 = methane fee (USD per t CO2e) x GWP x 1 if the fee applies to the source (below), else 0. Abatement share = MIN(1, MAX(0, a x fee^b)) on the source's curve. Biomass and downstream gas use the oil-and-gas curve, as legacy.
4. **Emissions** = the source's inventory methane x activity / activity in GHGYear x (1 - abatement). Shares and GHGYear activity are from scenario 1: the calibration is to the observed (baseline) inventory.
5. **Flaring.** The flared share of abated oil and gas methane burns to CO2 (44/16 t CO2 per t CH4), reported as energy CO2.
6. **Revenue** = fee x the sum over the sources the fee applies to of CH4 x GWP (fossil or non-fossil), USD million, part of total revenue.
7. **Fiscal space (v6.2, I47; user 2026-10-20: as close to legacy as possible with no vulnerability to circular references).** The GDP feedback counts the fee revenue as legacy (row 8024) through `ch4.revf`: the same sum over `ch4.emf`, which equals `ch4.em` except for downstream gas and biomass use. Those two read the stored scenario-1 activity (sheet BaselineCO2 rows dg, bm, refreshed by the build; check row `ch4bs.chk` = 0 in scenario 1), so the fiscal space reads no fuel use and no later change to the demand or power blocks can close a loop through it. Fee, abatement and the other sources are the scenario's own. The reported revenue (rmf, rtot, block 12e) keeps the own activity. (The v6.0 loop came from price-block average ranges that ran into section 11, fixed in v6.2.)

The methane fee (ScenarioDefinition) runs linearly from `MPLevelStart` in `MPIntro` to `MPLevelTarget` in `MPOutro` and keeps its slope after the target year (as legacy). It adds the carbon price when `CTforMethane` = Yes. As legacy (v4.12, user decision 2026-10-18; LD46):

- the fee path applies only in policy scenarios (scenario number above 1, legacy row 2238); the carbon price part has no such condition, as legacy row 2239;
- a switch per source on sheet `Manual inputs` J196:J200, the legacy addresses (names MFeeBio, MFeeDG, MFeeFF, MFeeAgr, MFeeWst; shown on Settings rows 47-51): biomass (No), downstream gas, fossil fuel production (oil, gas and coal), agriculture (livestock, rice), waste (all Yes). The switches are legacy inputs outside ScenarioDefinition (NORMS 4: main inputs on ScenarioDefinition, 'Manual inputs' the second source).

## 3. Energy methane and N2O

- Combustion methane = fuel use x emission factor, by subsector and fuel, and for power by generation type. A fuel that its GAINS subsector has no factor for takes the nearest GAINS match (v4.12, legacy bug L59, as the local pollutants: `AirPollutants_Method.md`). The factor moves linearly from its base-year value to its final value in 2039 (`EFEndYear`, the legacy column), flat after.
- Energy methane = calibration factor x (combustion + fossil supply methane) x fossil GWP. The factor = inventory energy methane / modelled energy methane in GHGYear (scenario 1). Energy methane thus equals the inventory in GHGYear and later moves with fuel use, supply activity and abatement. v6.2: the modelled GHGYear combustion and supply methane of scenario 1 are stored on sheet BaselineCO2 (rows ch4c, ch4sup, refreshed by the build), so the factor, used in every year, reads no later model year (circular-reference rule, user 2026-10-20).
- Energy N2O and F-gases: the inventory while it has the year; then N2O moves with energy CO2 and F-gases are held.
- Energy CO2 = fuel combustion (power included) + flaring.

## 4. Other inventory categories

Each category and gas takes the inventory value while the inventory has the year. After that it grows with a growth factor = (1 + GDP per capita growth)^income elasticity x (1 + population growth)^population elasticity x the change in mitigation effort. GDP per capita growth = (1 + real GDP growth) / (1 + population growth) - 1. Effort is 1, or, if ScenarioDefinition `AdditionMitigationPoliciesNonEnergy` = Yes, the scenario's energy CO2 divided by scenario 1's.

| Category | Projection |
|---|---|
| Industrial processes (all gases) | grows with industrial energy CO2 year on year (it may decline, as legacy rows 7553 and 7566-7569; v5.6) if `IndustrialProcessEmissionsScaleEner` = Yes, else held |
| Agriculture CO2, N2O, F-gases | growth factor (income 0.15, population 0.9) |
| Agriculture CH4 | livestock + rice methane |
| Waste CO2, N2O, F-gases; other | growth factor (population 1) |
| Waste CH4 | waste methane |
| LULUCF CO2 | if positive: previous x effort change - `LULUCFAnnualEmissionsDecline` x the last inventory value; sinks (negative values) held |
| LULUCF CH4, N2O, F-gases | held |

Totals by gas and by category; total GHGs excluding and including LULUCF; the change against scenario 1.

## 5. Validation and differences with legacy

- `check_full.py` recomputes every GHG and combustion-methane row in Python from the data files (scenarios 1 and 2, every year).
- When introduced (v2.8), every earlier output was unchanged (the methane fee is 0 in the shipped scenarios).
- The non-energy elasticities reproduce the legacy run exactly where the legacy method is kept.
- Sheet LegacyDiff lists the differences with legacy; the register of bugs, issues and upgrades describes the legacy bugs fixed: L18 (non-energy methane constant, abatement not applied), L19 (flaring CO2 counted as methane), L20 (population growth path), L21 (waste abated with the livestock curve). Local air pollutants: `AirPollutants_Method.md`.

## 6. Open issues

- **Egypt's inventory breaks after 2021** (I17): energy CH4 is 21.9 Mt CO2e in 2021 and 1.9-2.0 in 2022-2024, while the fugitive-emissions memo alone is 20.3 in 2023. Calibrating to 2024 (as legacy) may understate energy methane by about 19 Mt CO2e.
- **Energy CO2 calibration to the inventory (as legacy since v4.11; switch on)**: every CO2 emission factor is scaled by the 2021 inventory over the 2022 estimate (Egypt 0.930; `CO2Calibration_Method.md`); the 2021-2022 inventory break (I17) carries into every year, as legacy.
- **Combustion factors** use only the GAINS base and final values (the yearly paths are proprietary). Combustion methane exceeds inventory energy methane, so the calibration factor is about 0.25 for Egypt.
- **Oil, gas and coal production** is held at the base year (no production model).


## Fuel production for supply methane (v5.6, I66)

Oil, gas and coal production (rows ch4.prd) start from Balances and hold in the base year and the next, then grow with the producer-price response to the methane fee (ch4.pi = 1 + change of the fee per unit / international price x pass-through, Manual inputs J194; elasticities J190:J192) and the growth of world demand of the global demand scenario a year earlier (ch4.wd, Prices_int rows 323-333), as legacy rows 6132-6149. The methane source shares use base production as the inventory-year activity (no loop).

## NDC comparison (v5.7, section 14c; legacy F12 rows 18403-18518)

Data: sheet NDCs (legacy NDCs rows 48-242 latest, 250-444 second, 451-644 first round, columns C-P, stacked with a round
column; key ISO|round) and sheet GHGHist (legacy GHGs rows 954-1189: GHGs excl./incl. LULUCF, CO2 excl. LULUCF, energy
CO2 by year; header group|year). Both from `extract_legacy_tables.py ndc`.

Choice (ScenarioDefinition scenario 1, as legacy): NDCs (First round, Second round, else the latest), NDCTargetYear (Main* = first
target year, else the second where given), Conditionality (Unconditional, Conditional, else the average). Target year
at most NDCYrCap (2035).

Target on the NDC's own basis (gases CO2 or GHGs; LULUCF included or excluded), against the modelled BAU = scenario 1
in the target year: BAU: BAU x (1 + x) (x the reduction as given, negative); Fixed: x (Mt CO2e); Historical: emissions
of the reference year (scenario 1 where modelled, from 2022; else the GHGs inventory, 2021-2024, rows ndc.hc and ndc.hv, v6.1; else GHGHist) x (1 + x); Intensity: reference-year emissions x real
GDP of the target year / real GDP of the reference year x (1 + x); Unquantifiable: BAU. Reduction = 1 - target / BAU,
for the unconditional (u) and conditional (c) targets; a = their average (the one given if only one; 0 if none);
sel = the Conditionality choice (a if the chosen one is not given). Target GHGs incl. LULUCF = MIN(BAU incl. LULUCF,
BAU incl. LULUCF x (1 - reduction)), as legacy rows 18494-18496. Per scenario and year: reduction of GHGs incl. LULUCF
against scenario 1 (ndc.red), share of the NDC reduction achieved (ndc.gap = ndc.red / ndc.r.sel, legacy "Gap to NDC"),
GHGs above the chosen target (ndc.over; in the target year the legacy goal-seek difference, G18501). No goal seek (user
2026-10-19: comparison only).

Legacy bugs fixed: L119 (year adjustment applied twice for BAU, never for Fixed or Historical: the prototype compares in the
target year), L120 (index ratios inverted), L121 (Historical "level" is the cut), L122 (Intensity adds a blank cell
for LULUCF), L123 (Intensity reference GDP from a fixed cell). Issues: I67 (China CO2 hard-coded in legacy: not
replicated), I68 (reference years outside the data: N/A; v6.1 reads 2021-2024 from the GHGs inventory; 2018-2020 need data).

Egypt (latest NDC: BAU, 2030, -27% unconditional, GHGs excl. LULUCF): target 344.3 Mt CO2e (legacy 355.7 = its BAU
487.2 x 0.73; the prototype BAU is 471.7, the known baseline GHG difference); scenario 2 achieves 21% of the required
reduction in 2030 (legacy 51% for its cached policy scenario, which is not the prototype's scenario 2).
