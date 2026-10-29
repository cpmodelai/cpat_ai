# Emissions

## Non-CO2 GHGs and methane: method

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

The model adds methane, nitrous oxide and F-gases to energy CO2 and covers every UNFCCC inventory category, so it reports total GHG emissions. It includes a methane fee, its revenue, and combustion methane for every sector.

Units: methane in kt CH4 where it is a physical quantity, otherwise Mt CO2e with IPCC AR6 GWP100 (fossil methane 29.8, non-fossil 27.2). GHGYear is the last year the country has in the inventory (Egypt: 2024).

### 1. Data

| Sheet | Content | Source |
|---|---|---|
| GHGs | Inventory by country, year, category (energy, industrial processes, agriculture, LULUCF, waste, other) and gas (CO2, CH4, N2O, F-gases), Mt CO2e | Legacy sheet GHGs |
| CH4Inputs | Methane abatement curves (a, b) by country and source; shares that split inventory methane by source; flared share | Legacy sheet CH4Inputs |
| EF_NonCO2 | Combustion emission factors (kt per PJ) by subsector, fuel and pollutant, base year and final | Legacy sheet EF_PM (GAINS) |
| UNPop | Population by country and year (thousands) | Legacy sheet UNPop (UN WPP) |
| Balances | Base-year production of gas, oil, coal | Legacy Mitigation rows 503-509 |

The non-energy elasticities (section 4) are on sheet `Manual inputs` K325:M327, the legacy addresses (agriculture, waste, other: population elasticity row 326, per capita income elasticity row 327; a text entry such as "na" counts as 0). Their values reproduce the cached results of the legacy run exactly: legacy Mitigation uses the same values (it never reads the manual cells: their formula is broken, `#REF!`).

### 2. Methane by source

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

### 3. Energy methane and N2O

- Combustion methane = fuel use x emission factor, by subsector and fuel, and for power by generation type. A fuel that its GAINS subsector has no factor for takes the nearest GAINS match (v4.12, legacy bug L59, as the local pollutants: chapter Emissions). The factor moves linearly from its base-year value to its final value in 2039 (`EFEndYear`, the legacy column), flat after.
- Energy methane = calibration factor x (combustion + fossil supply methane) x fossil GWP. The factor = inventory energy methane / modelled energy methane in GHGYear (scenario 1). Energy methane thus equals the inventory in GHGYear and later moves with fuel use, supply activity and abatement. v6.2: the modelled GHGYear combustion and supply methane of scenario 1 are stored on sheet BaselineCO2 (rows ch4c, ch4sup, refreshed by the build), so the factor, used in every year, reads no later model year (circular-reference rule, user 2026-10-20).
- Energy N2O and F-gases: the inventory while it has the year; then N2O moves with energy CO2 and F-gases are held.
- Energy CO2 = fuel combustion (power included) + flaring.

### 4. Other inventory categories

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

### 5. Validation and differences with legacy

- `check_full.py` recomputes every GHG and combustion-methane row in Python from the data files (scenarios 1 and 2, every year).
- When introduced (v2.8), every earlier output was unchanged (the methane fee is 0 in the shipped scenarios).
- The non-energy elasticities reproduce the legacy run exactly where the legacy method is kept.
- Sheet LegacyDiff lists the differences with legacy; the register of bugs, issues and upgrades describes the legacy bugs fixed: L18 (non-energy methane constant, abatement not applied), L19 (flaring CO2 counted as methane), L20 (population growth path), L21 (waste abated with the livestock curve). Local air pollutants: chapter Emissions.

### 6. Open issues

- **Egypt's inventory breaks after 2021** (I91): energy CH4 is 21.9 Mt CO2e in 2021 and 1.9-2.0 in 2022-2024, while the fugitive-emissions memo alone is 20.3 in 2023. Calibrating to 2024 (as legacy) may understate energy methane by about 19 Mt CO2e.
- **Energy CO2 calibration to the inventory (as legacy since v4.11; switch on)**: every CO2 emission factor is scaled by the 2021 inventory over the 2022 estimate (Egypt 0.930; chapter Emissions); the 2021-2022 inventory break (I91) carries into every year, as legacy.
- **Combustion factors** use only the GAINS base and final values (the yearly paths are proprietary). Combustion methane exceeds inventory energy methane, so the calibration factor is about 0.25 for Egypt.
- **Oil, gas and coal production** is held at the base year (no production model).


### Fuel production for supply methane (v5.6, I66)

Oil, gas and coal production (rows ch4.prd) start from Balances and hold in the base year and the next, then grow with the producer-price response to the methane fee (ch4.pi = 1 + change of the fee per unit / international price x pass-through, Manual inputs J194; elasticities J190:J192) and the growth of world demand of the global demand scenario a year earlier (ch4.wd, Prices_int rows 323-333), as legacy rows 6132-6149. The methane source shares use base production as the inventory-year activity (no loop).

### NDC comparison (v5.7, section 14c; legacy F12 rows 18403-18518)

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
for LULUCF), L123 (Intensity reference GDP from a fixed cell). Issues: L169 (China CO2 hard-coded in legacy: not
replicated), I95 (reference years outside the data: N/A; v6.1 reads 2021-2024 from the GHGs inventory; 2018-2020 need data).

Egypt (latest NDC: BAU, 2030, -27% unconditional, GHGs excl. LULUCF): target 344.3 Mt CO2e (legacy 355.7 = its BAU
487.2 x 0.73; the prototype BAU is 471.7, the known baseline GHG difference); scenario 2 achieves 21% of the required
reduction in 2030 (legacy 51% for its cached policy scenario, which is not the prototype's scenario 2).


## Calibration of energy CO2 to the GHG inventory: method

Equations: `Equations.md`; workbook formulas: `Formulas.md`. Decision and numbers: `Old/Calibration_Plan_v3_6.md`.

### 1. Method

Every CO2 emission factor (EF), by subsector and fuel and by generation type, is multiplied by one factor, `EFCalib`. **Since v4.11 this is legacy's rule (user decision 2026-10-18: go with legacy; issue I32 replicated)**: legacy Mitigation rows 623, 839 and 976-977.

`EFCalib` = inventory energy CO2 of the year before the base year / scenario-1 energy CO2 of the base year with uncalibrated EFs (the base-year energy balance x the EFs); 1 if the switch is off. **The switch is Settings C27, Yes by default**, as legacy (EFsAdjustmentAnnexI and EFsAdjustmentNonAnnexI are both Yes*). With the shipped data (Egypt): 2021 inventory 211.05 Mt against the 2022 estimate 226.97 Mt, **EFCalib = 0.930** (legacy: 0.930).

The uncalibrated scenario-1 CO2 is data written by the build, like the ETS baseline: a live formula would be circular (EFs feed carbon prices, which feed fuel use). Scenario-1 fuel use does not depend on the EFs in value (no new carbon price; existing carbon pricing changes only after the historical years), so the calibrated baseline is the uncalibrated one times the factor. The rows are keyed by country (`EGY|raw`, `EGY|pow`, ...), so another country finds no rows (#N/A) rather than Egypt's: rebuild with its code (about 2 minutes since v4.9), or paste its scenario-1 values under its key.

Everything downstream follows: CO2 by subsector, fuel and power type; carbon tax, ETS cost and existing carbon pricing per unit of fuel and their revenue; the ETS baseline; energy CO2 in the GHG totals. Scenario-1 fuel use and prices do not change. In policy scenarios, carbon prices per unit of fuel are 7% lower for Egypt, so fuel use, revenue and the GDP effect change.

### 2. Results for Egypt (scenario 1, energy CO2, Mt; v4.11)

| Year | Inventory | Uncalibrated | Calibrated (x 0.930) |
|---|---|---|---|
| 2022 | 252.2 | 227.0 | 211.1 |
| 2023 | 267.4 | 196.7 | 182.9 |
| 2024 | 285.3 | 218.9 | 203.5 |

The calibrated base year equals the 2021 inventory (211.1), as legacy. Egypt's inventory jumps 19% from 2021 to 2022 (register I91), and legacy's rule carries that break into every year: calibrated CO2 is 16-29% below the 2022-2024 inventory. The 2023 dip is the fuel-use shock of legacy row 483 (I92, replicated).

### 3. Differences with legacy (sheet LegacyDiff)

- **Year and switch**: as legacy since v4.11 (before: the last inventory year GHGYear and the switch off, user decisions v3.2 and v3.4).
- **Switch**: legacy reads one switch for Annex I countries (ScenarioDefinition row 237) and another for the others, both Yes*; the prototype has one switch on Settings (C27), Yes.
- **Scope**: inventory energy CO2 includes fugitive CO2 (7.1 Mt in 2024), which the model does not compute separately. The factor absorbs it, as in legacy.


## Local air pollutants: method

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

The model computes emissions of seven local air pollutants from the fuel use of every subsector and of power generation: fine particulate matter (PM2.5), nitrogen oxides (NOx), sulphur dioxide (SO2), volatile organic compounds (VOC), black carbon (BC), organic carbon (OC) and carbon monoxide (CO). A memo converts them into CO2 equivalents (forcing). The emissions are also grouped into the sectors of the legacy air-pollution module, with primary organic matter and other PM2.5, its inputs. The pollutants are not part of the GHG totals. LiveOutputs reports total PM2.5, NOx, SO2, black carbon and the forcing for every scenario; the Charts sheet plots PM2.5 and SO2.

Units: emissions in kt; factors in t per ktoe; forcing in Mt CO2e (GWP100).

### 1. Data

| Sheet | Content | Source |
|---|---|---|
| EF_NonCO2 | Combustion emission factors by GAINS subsector, fuel and pollutant, base year and final, kt per PJ | Legacy sheet EF_PM (GAINS); also used for combustion CH4 |
| GWP_AP | GWP100 of the pollutants by GAINS region | Legacy GWP table of the pollutant forcing |
| Countries (column O) | GAINS region of every country (Egypt: `afr`) | Legacy Countries tab |

Each subsector takes the GAINS subsector of its CH4 factor: services use the residential factors, rail the road factors, and industry and other energy use the manufacturing factors (legacy bug L58). Power uses factors by generation type.

A fuel that its GAINS subsector has no factor for takes the nearest GAINS match (v4.12, legacy bug L59, user decision 2026-10-18; was issue I35; Inputs columns `efxs` to `eff`):

- LPG takes natural gas of the same GAINS subsector (both are gaseous fuels burnt in similar appliances; the only LPG factors in the data are for construction, i.e. off-road engines, with a CO factor about 300 times that of a gas stove);
- food & forestry takes construction (off-road machinery);
- biomass takes residential;
- any other fuel takes manufacturing (construction for manufacturing itself).

Egypt 2022: residential LPG (3,182 ktoe) takes residential gas, other mining diesel (3,819) and fuel transformation LPG (2,466; manufacturing gas) the manufacturing factors, food & forestry diesel (927) construction diesel. A pollutant missing for a fuel that the subsector does have factors for (for example organic carbon of manufacturing coal) stays 0: GAINS lists no zero factors.

### 2. Method

1. **Factor path**: the weight of the final factor rises linearly from 0 in the base year to 1 in 2039 (`EFEndYear`) and stays at 1, as for combustion CH4.
2. **Emissions**: for each subsector and pollutant, the sum over the eight fuels of fuel use x the weighted factor. Fuel use is the modelled one, so prices, policies and scenarios carry through. Power uses the same equation over the nine generation types.
3. **Totals**: transport, buildings and industry sum their subsectors, navigation included. A pollutant's total is the subsectors plus power.
4. **Forcing (memo)**: emissions x the region's GWP100 for BC, OC, NOx, SO2, VOC and CO, and their sum. Cooling pollutants (OC, SO2, NOx) have a negative GWP, so the net forcing can be negative: about -17.5 Mt CO2e for Egypt in 2022.
5. **Air-pollution module sectors**: coal power plants and gas power plants (fuel use of the type x the power factors); other power plants (power less coal and gas); ground level road (road); ground level other (residential, services, construction); other (rail, aviation, navigation, industry without construction, other energy use); food & forestry. The seven sectors add up to the pollutant's total.
6. **Primary organic matter (POM) and other PM2.5**, per sector: POM = 1.3 x organic carbon; other PM2.5 = MAX(0, PM2.5 - black carbon - POM).
7. **The module's input table (v3.12)**: the block takes the layout of the legacy input table (Mitigation rows 15859-15961):
   - one block per module sector (coal, gas and other power plants, ground level road, ground level other, other, food & forestry) and one for all sectors;
   - in each block the ten pollutants in legacy order: NOx, SO2, BC, POM, other PM2.5, VOC, CH4, CO, PM2.5, OC;
   - codes `aps.<pollutant>.<sector>`, in kt (legacy: tonnes).

   The air-pollution module reads these rows directly (NORMS 3c).
8. **CH4 in the table, as legacy (issue I34)**:
   - coal, gas and other power plants: combustion CH4 of the generation types (section 14);
   - road, ground level other: combustion CH4 of their subsectors (`ch4` rows of sections 5-8);
   - other: combustion CH4 of its subsectors plus fossil fuel supply methane (`ch4.sup`; legacy has oil and gas extraction only);
   - food & forestry: combustion CH4 plus agriculture (livestock, rice) and waste methane, as legacy.

   Legacy has no combustion CH4 factors, so its combustion part is zero. CH4 here is uncalibrated: it is not scaled to the inventory (`ghg.k`).

### 3. Results for Egypt (scenario 1)

v4.12 (with the nearest GAINS factors, bug L59): PM2.5 is 95.6 kt in 2022 and 94.8 kt in 2040; NOx 886 kt in 2022. The check recomputes all rows of the block in Python for scenarios 1 and 2.

The module's input table in 2022 (kt): NOx 886, SO2 317, BC 33.2, POM 48.3, other PM2.5 14.1, VOC 377, CH4 2,150, CO 2,473, PM2.5 95.6, OC 37.2. Sectors without the fuels of bug L59 match the legacy input table (rows 15861-15948, in tonnes): gas power plants' NOx is 104,502 t and road NOx 569,560 t in both. Before v4.12 (fuels without a factor at 0, as legacy) the totals were NOx 801, SO2 300, PM2.5 90.8: the fix adds residential LPG (as gas), mining and food & forestry diesel and fuel transformation LPG. CH4 is above legacy's 1,936 kt also because the prototype adds combustion CH4 and all fuel-supply methane, while legacy has extraction only (I34).

Forcing in 2022: total -18.6 Mt CO2e (v4.11: -17.5; legacy cached -16.3); black carbon 11.9, CO 4.9, VOC 2.3, organic carbon -4.5, NOx -6.3, SO2 -27.0. The legacy values differ by the fuels of bug L59, and by 2040 also because fuel use and the factor paths differ.

### 4. Differences with legacy CPAT (sheet LegacyDiff)

- Legacy omits navigation from the pollutant totals (bug L22). It is included here.
- Legacy leaves services and food & forestry out of each pollutant's total (bug L23), although its air-pollution sectors include them. Here the total is the sum of the sectors.
- Legacy gives fuels with no GAINS factor zero emissions (legacy bug L59, user decision 2026-10-18; was issue I35). Egypt 2022: residential LPG, mining diesel, food & forestry diesel and fuel transformation LPG, about 10 Mtoe in all; food & forestry shows about 1 t of NOx in legacy (row 15939). Here they take the nearest GAINS match (section 1).
- Legacy gives a zero factor to subsectors with no GAINS match (legacy bug L58, user decision 2026-10-18; was issue I27). Here every subsector is mapped to a GAINS subsector.
- Food & forestry is split into food and forestry/agriculture as legacy (v4.11, LD53): the food share of each fuel is info_food over the four info_ flows of the processed Balances (legacy rows 501-504, 1666-1673); rows apfd (food fuel use) and ap.<pollutant>.fod / .fag (memo rows, not in the totals). The share is 0 for Egypt.
- Legacy has no ammonia (NH3) from fuel combustion, so neither does the prototype.
- Legacy reads factor paths by year, which are proprietary and empty in the NoPropData file. The prototype draws a linear path between the base and final factors (simplification, as for CH4).
- Not built yet: the air-pollution (health) module that would use these sectors.

