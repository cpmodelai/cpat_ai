# Remaining functionality, outputs and alignment with legacy (plan, 2026-10-29; decisions of 2026-10-29 in section 7)

Scope (user 2026-10-29): build every legacy function the prototype lacks, **except the elasticity-based power model**
(legacy Mitigation section C3, not built by decision). MTOutputs of the prototype: comprehensive, like legacy, without
intermediate outputs such as the components of the price build-up. Reference: legacy `CPAT 1.0pre_465`; prototype v8.5.

## 1. Where we are: legacy blocks against the prototype

| Legacy block (Mitigation sheet, 465) | Prototype v8.5 |
|---|---|
| B Key assumptions and inputs (MTInputs, Manual inputs, data) | Built (ScenarioDefinition on 465 rows; Manual inputs in part, below) |
| C1 Policies, C2 Retail prices | Built, except the **Pigouvian (efficient) tax** options (rows 81-82, 111-147, 200, 2202; inputs AddEfficientTaxes, ClimateEffTax, ExternalityAddVAT, AddEfficientTaxesPhaseInYears) and **CBAM process emissions** in the carbon tax and ETS (rows 1832-1836, 1918, 2206, 5867-5874; inputs CBAMProc*) |
| C3 Elasticity-based power model | **Not built, by decision** |
| C4 Engineer power model | Built (power features P1-P5), except the memo tables F6 (generation costs, CostBreakdownYear) and bug L84 (electricity consumer subsidy option) |
| C5 Transport (elasticity and engineer road models) | Built, except road biofuels in the elasticity model (LD62) and the range-anxiety fit (LD63) |
| C6-C9 Buildings, industry, other energy use, methane | Built, except self-generated renewables in aviation and navigation (L47) and the CH4 intensity decline of agriculture and waste (L135, also dead in legacy) |
| C10 Green Public Investment (rows 6215-6267) | **Not built** |
| C11-C17 Results: energy, CO2, non-CO2 and local pollutants, GWP, GHGs, revenues, GDP effects | Built |
| E1 For Distribution | Built (section 19a; standalone Distribution module) |
| E2 For Transport module, E3 For Air Pollution module | **Not built**; decided 2026-10-29: no copies, sections 15 and 5b are the output blocks (section 8) |
| F2-F16 Results for charts | Built: macro drivers, coverage, GDP effects, prices, energy, power, revenues, GHG, CO2, Kaya, methane, transport. **Missing**: F10 monetized social costs and benefits (needs air pollution and transport externalities), F11 balance of payments beyond the energy trade balance (current account, L50) |
| Air pollution sheet (health, mortality, valuation) | **Not built in the prototype** (issue I69, dropped 2026-10-20); a standalone AP v0.3 scaffold exists (`excel_ai/air_pollution/`) |
| Transport externalities (accidents, congestion, road damage) | **Not built** (issue I70, dropped 2026-10-20; plan `Transport_cobenefits.md`) |
| Distribution sheet | Built (all 31 legacy bugs fixed) |
| Industrial emissions intensity of output (MTOutputs emin, tCO2 per USD m GVA) | **Not built** (needs GVA by industrial sector) |

## 2. Outputs: legacy MTOutputs against the prototype

Legacy 465 MTOutputs holds 1,225 codes in 30 sections; the prototype's LiveOutputs holds 246 (plus about 13,400 codes on
the Mitigation sheet itself). Proposal: rebuild LiveOutputs (renamed MTOutputs) section by section like legacy, every
row with the protocol code and the legacy MTOutputs code as alias, **without** the price build-up and other
intermediates.

| Legacy section | Codes | Keep in MTOutputs? | Prototype has the quantity? |
|---|---|---|---|
| Policy characteristics, Macro effects, Emissions, Energy prices (final), Total Carbon Price, Energy consumption, Disaggregated energy consumption, Revenues, Welfare (climate), Distribution (all), Power (sustainability, demand, capacity, new investment), Methane | about 640 | Yes | Yes (codes to map) |
| Pigouvian taxes (efficient prices, externality costs by fuel) | 153 | Yes | **No** (Pigouvian tax; air pollution and transport externality costs) |
| Air pollution effects, Transportation effects, Climate costs, Welfare (air, accidents, congestion) | about 95 | Yes | **No** (AP and TCB modules), climate costs partly (SCC) |
| Industrial emissions intensity and cumulative GVA | 19 | Yes | **No** (GVA data) |
| Subsidies | 124 | The subsidy levels only (about 40) | Yes |
| Energy price components (baseline), Markups, Simplified prices | 121 | **No** (price build-up intermediates) | Yes (on the Mitigation sheet) |
| Input parameters (income elasticities) | 3 | Yes | Yes |

## 3. Data

| Data | Needed for | Status |
|---|---|---|
| Proprietary tables for other countries (Balances, EnergyCons, EF_PM, IO_GTAP, HHSurvey, ASPIRE, WHOCooking) | Any country but Egypt | NoPropData file: Egypt only (issue I90) |
| GAINS combustion factor paths by year, or confirmation of base and final factors | Pollutants, combustion CH4 | Issue I98 (extremely high) |
| Blank VAT cells of the IMF dataset | VAT of household fuels, other countries | Issue I97 (very high) |
| Historical GHGs 2018-2020 | NDC reference years | Issue I95 |
| Air pollution data tabs (WB, GBD, IHME, ILO, ExposureCoefs, IF PP, ConcMat, Air_Data) | Air pollution module | Public extracts recovered (`data/air_pollution/legacy_459/`); to check against 465 |
| Transport externality data (legacy Transport sheet, Tran_Elast) | Transport co-benefits | Not extracted |
| GVA by industrial sector | Emissions intensity of output | Not extracted (legacy source to identify) |
| WEO current account (BCA) | Balance of payments | Not in the WEO extract (L50) |
| Planned retirements (coal plant tracker) | Power, other countries | Egypt has none (U13) |
| Data links of GHGs, EF_GHG, CH4Inputs, Elasticities, Prices_int, OilProductShares, Transport1-2 | The data workbook route | Converters missing (TODO section 6) |

## 4. Alignment with legacy once every legacy bug is fixed

What the register says remains, besides the 168 legacy bug fixes:

| Kind | Items | Effect on Egypt results |
|---|---|---|
| Departures by user decision | I99 corrected Egypt prices (LD4, LD33): electricity 0.054 against 0.097 USD/kWh | **Large** (electricity prices, power demand, subsidies) |
| | LD2 other oil products pass-through and margin from the dataset (with bug L13) | Large for other oil products |
| | LD1 food & forestry elasticities, LD10 policy paths after the target year, I47 methane fee in the fiscal space | Small |
| | LD13, LD14, I6, LD15, LD40, LD69, LD74, I52, I53 (signs, horizon to 2041, form) | None |
| Not classified | LD41 data vintage (energy use via the kernel), LD58 GDP effects (legacy cached values), LD16 margins x CPI | Unknown |
| Simplifications | LD19 producer subsidies (fiscal line, no price effect) | Small (Egypt) |
| Not built | Section 1 above | Missing outputs, not different values |

**Not measured.** No run of legacy 465 with every bug fixed has been compared with the prototype (U2). Until it is,
alignment is a register count, not a number.

## 5. Plan

Each step: build, quick check, register and documents, commit; full check at the end of each phase.

| Phase | Step | Content | Size |
|---|---|---|---|
| A. Measure | A1 | Legacy 465 copy with every cell plan applied (LibreOffice; check the conversion first), Egypt baseline and carbon-tax run, compared with the prototype by output code (U2) | Large |
| | A2 | Explain every difference: a departure in section 4, a new bug, or a new issue; register it | Medium |
| B. Decide | B1 | User: keep or revert each departure by decision (section 4), classify LD41, LD58, LD16 | Small |
| C. Mitigation functions | C1 | Pigouvian (efficient) taxes: climate part now (SCC, phase-in, VAT base option); air pollution and transport parts after D | Medium |
| | C2 | CBAM process emissions in the carbon tax and ETS (MTInputs 117-121) | Medium |
| | C3 | Green public investment (legacy rows 6215-6267) | Medium |
| | C4 | Small items: road biofuels in the elasticity model (LD62), range-anxiety fit (LD63), self-generated renewables in aviation and navigation (L47), electricity consumer subsidy option (L84), producer subsidy manual override (L86), manual domestic prices and manual elasticities (Manual inputs; L100, L101, I53), power memo tables F6, CH4 intensity decline as legacy (L135) | Medium |
| | C5 | Balance of payments (current account, L50) and emissions intensity of output (GVA), once the data are in | Small |
| D. Modules | D1 | Air pollution: exports (19b), the AP model (plan `Air_pollution.md`; Senegal and Egypt regression) | Large |
| | D2 | Transport co-benefits: output block 5b, accidents, congestion, road damage (plan `Transport_cobenefits.md`) | Large |
| | D3 | Monetized social costs and benefits (F10), welfare, Pigouvian taxes with all externalities (completes C1) | Medium |
| E. Outputs | E1 | MTOutputs: legacy sections and order, protocol codes with the legacy code as alias, intermediates left out (section 2) | Medium |
| F. Data | F1 | The data of section 3, as they arrive (data request) | Ongoing |
| G. Release | G1 | Excel 365 review (I1), full check, documents | Medium |

## 6. Decisions for the user

1. **Air pollution and transport co-benefits** were dropped on 2026-10-20 (I69, I70). Building the remaining
   functionality brings them back: inside the prototype, or as standalone modules fed by sections 19b/19c (the
   modules plan, like Distribution)?
2. **Departures by decision** (section 4): keep each, or align with legacy?
3. **MTOutputs codes**: protocol codes with the legacy code as alias (proposed), or legacy codes?
4. **Order**: measure first (phase A, proposed), or functions first?

## 7. Decisions (user 2026-10-29) and the work they define

- **Outputs (MTOutputs, section 2, phase E): out of scope here**; the user decides separately.
- **Departures**: LD1 food & forestry takes the industry elasticities (as legacy); LD10 fuel price reform follows
  ExtendCarbonPriceBeyondOutro as legacy, and legacy's drop to 0 after the target year (any option but Linear* and
  Percentage) becomes legacy bug L171 with a cell plan (hold the target level; check the option list first); feebates
  constant after the target year (as legacy); I47 methane fee in the fiscal space on the scenario's own activity (as
  legacy, exact-year references, full-recalculation test). One release.
- **Air pollution and transport co-benefits**: no separate models. A new Mitigation section **"Inputs from air
  pollution and transport co-benefits"**, just before welfare, holds legacy's Egypt values, typed (hard-coded) from
  legacy 465: per-unit damages (air pollution cost per GJ by fuel and sector, accident, congestion and road-damage cost
  per vehicle-km or per liter, as legacy's Advanced options rows 112-135 and the Air pollution and Transport sheets) so
  that scenario totals follow the prototype's own fuel use and vehicle-km. Other countries: a new issue (the inputs are
  Egypt's legacy values), until the modules exist.

### Remaining functionality (outputs excluded)

| # | Function | Legacy | Depends on |
|---|---|---|---|
| R1 | Inputs from air pollution and transport co-benefits (typed Egypt values) | Air pollution sheet, Transport sheet, Mitigation rows 112-135 | - |
| R2 | Monetized social costs and benefits (F10) and the full welfare (air pollution, accidents, congestion, road damage, climate) | Mitigation F10 rows 17377-18159, welfare rows | R1 |
| R3 | Pigouvian (efficient) taxes: climate, air pollution and transport externalities, phase-in, VAT base option, as a policy option and as reference prices | Mitigation rows 81-82, 111-147, 200, 2202; inputs AddEfficientTaxes, ClimateEffTax, ExternalityAddVAT, AddEfficientTaxesPhaseInYears | R1 |
| R4 | CBAM process emissions in the carbon tax and ETS | rows 1832-1836, 1918, 2206, 5867-5874; inputs CBAMProc* | - |
| R5 | Green public investment | rows 6215-6267 | - |
| R6 | Residential initially-exempt split (most-used cooking fuel) as legacy | LD67; bugs L48, L92, L94 | - |
| R7 | Producer subsidies with the price effect (now a fiscal line only) | LD19 | user decision (simplification) |
| R8 | Manual inputs not yet read: manual domestic prices (I53, L100), manual elasticities (L101), electricity producer subsidy override (L86), CH4 intensity decline (L135) | Manual inputs tab | - |
| R9 | Electricity consumer subsidy option (L84) and the power memo tables (F6: generation costs, CostBreakdownYear) | Mitigation C4, F6 | - |
| R10 | Road biofuels in the elasticity road model (LD62), self-generated renewables in aviation and navigation (L47), range-anxiety fit (LD63) | rows 5380-5537 | - |
| R11 | Balance of payments: current account (L50) | F11; WEO BCA | data (WEO, public) |
| R12 | Emissions intensity of industrial output (MTOutputs emin) | GVA by sector | data |
| R13 | Classify and settle LD16 (margins x CPI), LD41 (data vintage), LD58 (GDP effects) | - | phase A |
| R14 | Measure the alignment (phase A) and the Excel 365 review (I1) | - | - |

Not built, by decision: the elasticity-based power model (legacy C3).

## 8. Decisions (user 2026-10-29, later) and scope of the build

- **Scope: R1-R13 are all built**, green public investment (R5) included. Not built: the elasticity-based power model.
- **R7**: producer subsidies with their price effect, **as legacy**.
- **R11, R12**: the current account (balance of payments) and the GVA of the industrial sectors are **legacy Egypt
  values typed in** (as R1), not new data links; other countries: the same issue as R1.
- **R13**: LD16 margin read from the 2024 column as legacy, and new legacy bug **L172** (margin and production cost
  added unconverted, nominal, into real prices; cell plan: x the CPI index of the data year); LD41 re-extract the price
  forecasts and balances from 465 and compare (then "Same" or a data issue); LD58 "Same" (benchmark: legacy's stored
  carbon-tax run GDP effects, for phase A).
- **Exports to modules** (user 2026-10-29): section 19 holds 19a Distribution only (plain copies, defined name
  ExportDistn, tab FromMitigation). **Air pollution and transport co-benefits are not copied** (to save space): each
  reads its own section of the sheet, and the heading says so.
  - Section 15 is the output block to the air pollution module: **"15. Local air pollutants: outputs to the air
    pollution module"**; the other rows the module reads (fuel use by sector and fuel, as legacy E3 rows 15810-16065)
    sit next to it in the same section. Section 15 stays just before section 19.
  - Section 5b is the output block to the transport co-benefits module: **"5b. Road transport: engineer model and
    outputs to the transport co-benefits module"**; the rows the module reads (total and freight vehicle-km, average
    fuel economy by fuel, the passenger/freight splits of diesel, LPG, gas and electricity, and the road share of each
    fuel in the switched model, as legacy block E rows 15724-15823) sit in the same section. Section 19c is dropped.
- **Transport co-benefits are not self-consistent in legacy** (checked 2026-10-29): legacy takes vehicle-km, freight
  vehicle-km, fuel economy and the class splits from the engineer road model even when TrModel = Elasticity (the
  default), while the road fuel shares follow TrModel. Egypt 2031: engineer vehicle-km -8.6% against road gasoline
  -12.9% and diesel -14.3% in the elasticity model. The prototype matches legacy (section 5b runs in every scenario)
  and registers new issue **I100** (replicated). `Transport_cobenefits.md` section 1.3 and issue I-a.
- **Python build in parallel**: the equations of R1-R13 go in an addendum to the equation list,
  **`excel_ai/mitigation/Equations_addendum.md`** (one entry per new variable: code, equation, legacy rows, inputs),
  written with the build; `Equations.md` and the Methods volume take it in at the next release. Machine-readable plan:
  [`remaining_functionality.json`](remaining_functionality.json).

## 9. Equations addendum (written 2026-10-29)

[`../mitigation/Equations_addendum.md`](../mitigation/Equations_addendum.md): the equations of R1-R13 and the reverts,
from legacy 465, sections A-F; research, cell evidence, cell plans, hook points in `build.py` and Egypt values in
[`../mitigation/Equations_addendum_notes.md`](../mitigation/Equations_addendum_notes.md). New register codes (entered
with the v9.0 build): legacy bugs L173-L222, issues I101-I146, departure LD80. Points taken by default, open to the
user: `remaining_functionality.json` `open_points` (CBAM process emissions in the totals; electricity Pigouvian tax 0
as legacy; transport candidates B-c, B-d, B-e kept as legacy; registered bugs not reproduced in 465 to check).

