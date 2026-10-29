# ISSUES: issues (data problems first), departures and upgrades (v1.0.1)

**The rule (NORMS 0).** Never replicate a legacy bug; always replicate a legacy issue, and track it. A bug: legacy does not compute what it means to (a wrong row, a double application, a dead reference); the prototype fixes it. An issue: legacy does what it means to, but the choice is open to question; the prototype does the same and tracks it. A departure that is not a bug fix is kept only by user decision. Data problems are issues (area Data): replicated; where legacy needs a formula fix, that fix is a legacy bug (L) and the issue is Very high; where no cell plan is possible, the prototype aligns with legacy and the issue is Extremely high.

Generated from the register (`mitigation/register.py`) by `mitigation/make_replication_lists.py`. The same items, every column: the tracker `Tracking_Legacy_Bugs_v1.0.1.xlsx` (the master list). Bugs in detail: `Legacy_CPAT_Bugs_v1.0.1.docx`. Issues in detail: the appendices of the Documentation (`mitigation/CPAT-AI-Mitigation_Documentation.docx`). Lists: [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md).

**135 issues (14 data problems), 35 departures (LegacyDiff), 9 upgrades.**

## 1. Data problems

Most urgent first. Extremely high: no cell plan possible, the prototype does exactly what legacy does. Very high: a legacy bug (L) covers it; the data still need fixing.

| Code | Former | Kind | Priority | Status | Title | In the prototype | Next step |
|---|---|---|---|---|---|---|---|
| I98 | DB1 < I64 | Issue | Extremely high | Open | Combustion emission factors: GAINS base and final factors only | Replicated | The prototype now does exactly what legacy 465 does (v0.8.5). Plan: get the GAINS factor paths by year (proprietary) or confirm that the base and final factors are the intended data; check the 2040-2041 extrapolation and the EFSel average with the CPAT team. |
| I148 |  | Issue | Extremely high | Open | Current account data typed for Egypt only | Replicated | No cell plan possible (the data are missing): Egypt typed, as legacy's corrected values. Plan: the data team adds the current account (BCA, BCA_NGDPD) to the WEO table for every country; then read it instead of the typed values. |
| I97 | DB2 < I65 | Issue | Very high | Open | Blank VAT cells in the IMF price dataset | The prototype has the fix of bug L170 (a blank takes the general VAT rate) | Plan: the data team says which blank VAT cells of the IMF price dataset are missing values and which are true zeros, and fills the dataset. Legacy: apply the cell plan of bug L170 (a blank reads the general VAT rate for the household fuels); the prototype has that fix. No effect for Egypt. |
| I89 | DI1 < I4 | Issue | Major | Closed | Price vintage: data prices end in 2022 (legacy 465: 2024) | Replicated | v0.9.0 (user 2026-10-29): the last historical price year is 2024, as legacy (price data through 2024, projection from 2025). v0.3.7-v0.8.5 held 2022, to stay close to the legacy cached run of an older price vintage (2026-10-09 comparison). |
| I90 | DI2 < I13 | Issue | Major | Open | Data for other countries: proprietary tables are Egypt only | Prototype limitation | Data for other countries (TODO). |
| I91 | DI3 < I17 | Issue | Major | Accepted | Egypt GHG inventory: energy CH4 breaks after 2021 | Replicated | Decided 2026-10-15: calibrate to 2024 as legacy. |
| I92 | DI4 < I22 | Issue | Major | Accepted | Fuel-use shock of 2023-2024 (replicated v0.3.11) | Replicated | Replicated v0.3.11; source of the values to trace. |
| I99 | DB3 < I20 | Issue | Major | Closed | Electricity price data differ from legacy | Replicated | v0.9.0 (user 2026-10-29: legacy prices): legacy 465 Prices_dom already holds the corrected Egypt block; the prototype data equal it cell by cell except the spot coal and gas cells (I150). LD4 and LD33 are Same. |
| L170 | DB2 < I65 | Legacy bug | Medium | Open in legacy | Blank VAT cells of the price dataset read as a VAT rate of 0 | Fixed: a blank VAT cell takes the general VAT rate (VAT_WEO) for residential coal and gas and the oil products, 0 for power, industry and biomass (since v0.0.14; was departure LD3, data bug DB2). | Row 726 (VAT_WEO, the general VAT rate of the year, from the same dataset). Rows 768, 776, 780, 788, 792, 796, 824 (power, industry, electricity, biomass) are not changed: a blank there stays 0, as in the prototype. |
| I93 | DI5 < I37 | Issue | Minor | Accepted | Primary energy of renewables: efficiencies not exactly 1 | Replicated | As legacy (v0.3.18); set the renewable efficiencies to 1 if the data are confirmed. |
| I94 | DI6 < I38 | Issue | Minor | Accepted | Legacy's stored run: wind and solar capex time factors 2039-2041 differ from its Power tab | Replicated | v0.4.7: the formula follows the Power tab; recheck against a fresh legacy run. |
| I95 | DI7 < I68 | Issue | Minor | Open | NDC reference years outside the data | Replicated | v0.5.7: GDP solved (WEO NGDP_R, 2000-2040). v0.6.1: reference years 2021-2024 read the GHGs inventory (rows ndc.hc, ndc.hv), 2022 onwards the model. Still open: historical GHGs 2018-2020 (GHGHist ends 2017, CO2 2020): data request. |
| I96 | DI8 < distribution DI3 | Issue | Minor | Accepted | Elasticities always overall, mean | Replicated |  |
| I150 |  | Issue | Minor | Open | Spot coal and gas prices of Egypt hold a year and 0 in legacy 465 | Departs (user decision) | The CPAT data team fills the spot cells; the prototype keeps the module values (no effect unless the spot option is chosen). |

## 2. Issues (I)

Replicated, a departure by user decision, or a limitation of the prototype.

| Code | Former | Module | Severity | Status | Issue | In the prototype | See also |
|---|---|---|---|---|---|---|---|
| I1 |  | Mitigation | Major | Open | Not yet run in Excel | Prototype limitation |  |
| I2 |  | Mitigation | Minor | Accepted | Excel versions | Prototype limitation |  |
| I3 |  | Mitigation | Minor | Accepted | New sector / fuel pairs need a label | Prototype limitation |  |
| I5 |  | Mitigation | Minor | Accepted | Totals include power since v0.1.09 | Prototype limitation |  |
| I6 |  | Mitigation | Minor | Accepted | Electricity subsidy gap is signed | Departs (user decision) |  |
| I9 |  | Mitigation | Minor | Accepted | The LAMBDA year 2041 needs LAMBDA support | Prototype limitation |  |
| I10 |  | Mitigation | Minor | Accepted | Without LAMBDA support the power model looks ahead without 2041 | Prototype limitation |  |
| I11 |  | Mitigation | Minor | Accepted | Changing the last historical price year | Prototype limitation |  |
| I12 |  | Mitigation | Minor | Accepted | Values after 2030 | Prototype limitation |  |
| I14 |  | Mitigation | Major | Accepted | Distance to the legacy cached baseline | Departs (user decision) |  |
| I15 |  | Mitigation | Minor | Accepted | Subsidy rows changed sign in v0.2.4 | Prototype limitation |  |
| I16 |  | Mitigation | Minor | Accepted | A new block needs its label row | Prototype limitation |  |
| I18 |  | Mitigation | Minor | Resolved | GHG totals use energy CO2 without inventory adjustment (resolved v0.3.2) | Replicated |  |
| I19 |  | Mitigation | Major | Resolved | Jet fuel (replicated v0.3.11) | Replicated |  |
| I21 |  | Mitigation | Major | Accepted | ETS: one auctioned share for every sector (replicated v0.4.15) | Replicated |  |
| I25 |  | Mitigation | Major | Resolved | Industrial process emissions below legacy, not explained | Replicated |  |
| I26 |  | Mitigation | Minor | Resolved | GHG defaults not yet checked against legacy | Replicated |  |
| I28 |  | Mitigation | Minor | Dropped | Engineer road model: calibration open | Replicated |  |
| I29 |  | Mitigation | Minor | Resolved | Excel repair prompt (resolved v0.3.7) | Prototype limitation |  |
| I30 |  | Mitigation | Minor | Open | ETS goal seek short of the cap in definition 5 | Prototype limitation |  |
| I31 |  | Mitigation | Major | Accepted | Average prices mix price and composition changes | Replicated |  |
| I32 |  | Mitigation | Major | Accepted | Energy CO2 calibration to the inventory: as legacy since v0.4.11 | Replicated |  |
| I33 |  | Mitigation | Minor | Resolved | Data step overwrites the corrected Egypt prices | Prototype limitation |  |
| I34 |  | Mitigation | Minor | Accepted | CH4 of the air-pollution input table: methane sources by convention | Replicated |  |
| I36 |  | Mitigation | Minor | Accepted | Effective carbon rate counts VAT and subsidies | Replicated |  |
| I39 |  | Mitigation | Minor | Accepted | VAT on oil products charged on the household share only (replicated v0.4.12) | Replicated |  |
| I40 |  | Mitigation | Minor | Accepted | Road biofuels: feebate CO2 per liter scaled by the fossil share (replicated v0.4.12) | Replicated |  |
| I41 |  | Mitigation | Major | Accepted | GDP effects: the impulse is the change in revenue over this year's GDP (replicated v0.4.15) | Replicated |  |
| I42 |  | Mitigation | Minor | Accepted | GDP effects: impulses only from GDPStartYear (replicated v0.4.15) | Replicated |  |
| I43 |  | Mitigation | Minor | Resolved | GDP effects: revenue uses 0 before the carbon price starts (not replicated) | Replicated |  |
| I44 |  | Mitigation | Minor | Accepted | Multipliers: the income-group spread added to manual and country multipliers (replicated v0.4.15) | Replicated |  |
| I45 |  | Mitigation | Minor | Accepted | Multipliers: excise estimates from the "Excise tax" table (replicated v0.4.15) | Replicated |  |
| I46 |  | Mitigation | Major | Resolved | Revenue by policy: transport and renewable subsidies not modelled | Replicated |  |
| I47 |  | Mitigation | Minor | Accepted | GDP effects: methane fee in the fiscal space on the scenario's own activity | Replicated |  |
| I48 |  | Mitigation | Minor | Accepted | Price-control phase-out uses the consumer subsidy share (replicated v0.4.16) | Replicated |  |
| I49 |  | Mitigation | Minor | Resolved | Producer subsidies spread over world or domestic demand, in the supply cost (replicated v0.9.0) | Replicated |  |
| I50 |  | Mitigation | Minor | Accepted | Residential LPG and kerosene always exempted: all new policy removed (replicated v0.5.1) | Replicated |  |
| I51 |  | Mitigation | Minor | Accepted | Residential leakage: the fossil change is efficiency-weighted (replicated v0.5.1) | Replicated |  |
| I52 |  | Mitigation | Minor | Accepted | ETS inclusion: construction, fuel transformation and other energy use follow the buildings flag | Departs (user decision) |  |
| I53 |  | Mitigation | Minor | Accepted | Manual domestic prices switch on only with a 2021 value | Replicated |  |
| I54 |  | Mitigation | Minor | Accepted | PPAs: phase-out switch only on the exact text "Yes*"; share to phase out typed 1 | Replicated |  |
| I55 |  | Mitigation | Minor | Resolved | Renewable subsidies: nominal inputs used as real | Replicated |  |
| I56 |  | Mitigation | Minor | Accepted | Electricity excise: base-year grid intensity of the energy balance | Replicated |  |
| I57 |  | Mitigation | Minor | Accepted | Final deficit to gas: a typed switch outside MTInputs | Replicated |  |
| I58 |  | Mitigation | Minor | Resolved | Power switches tested for the exact "Yes" | Departs (user decision) |  |
| I59 |  | Mitigation | Minor | Resolved | Electricity fuel price reform not applied to electricity prices (not replicated yet) | Replicated |  |
| I60 |  | Mitigation | Minor | Resolved | End-user electricity price not floored at MinPostSubsidyPowerPrice (not replicated yet) | Replicated |  |
| I61 |  | Mitigation | Major | Accepted | Engineer road model: follow-ups parked | Replicated |  |
| I62 |  | Mitigation | Major | Accepted | Fuel use: no partial-adjustment model | Replicated |  |
| I63 |  | Mitigation | Major | Dropped | Demand responds to real USD prices, not real local-currency prices | Replicated |  |
| I66 |  | Mitigation | Major | Resolved | Fuel production for supply methane held at the base year (not replicated) | Replicated |  |
| I69 |  | Mitigation | Major | Dropped | Air-pollution co-benefits (health, mortality) not built | Departs (user decision) |  |
| I70 |  | Mitigation | Major | Dropped | Transport externalities (congestion, accidents, road damage) not built | Departs (user decision) |  |
| I71 |  | Mitigation | Major | Accepted | Fuel use grows with total GDP: population gets the income elasticity | Replicated |  |
| I72 |  | Mitigation | Major | Resolved | GDP feedback timing: same-year effects must never reach same-year demand | Replicated |  |
| I73 |  | Mitigation | Major | Resolved | Scenario-1 lookups must end at the current column | Prototype limitation |  |
| I74 |  | Mitigation | Major | Resolved | Methane calibration bases must be data or base-year values | Prototype limitation |  |
| I75 |  | Mitigation | Minor | Resolved | Legacy code inconsistencies (CPAT code protocol) | Departs (user decision) |  |
| I76 | distribution DI1 | Distribution | Minor | Accepted | Spending in the base year | Replicated |  |
| I77 | distribution DI2 | Distribution | Minor | Accepted | GTAP values converted with the local GDP deflator | Replicated |  |
| I78 | distribution DI4 | Distribution | Minor | Accepted | Recycled amounts per capita from the overall sample | Replicated |  |
| I79 | distribution DI5 | Distribution | Minor | Accepted | Gini from a fitted Lorenz curve | Replicated |  |
| I80 | distribution DI6 | Distribution | Minor | Accepted | Carbon-pricing revenue stands for the revenue to recycle | Replicated |  |
| I81 | distribution DI7 | Distribution | Minor | Accepted | ASPIRE-targeted transfers (TransferType other than Cash) | Replicated |  |
| I82 | distribution DI8 | Distribution | Minor | Accepted | Poverty-line targeting (TargetBelow, with Cash only) | Replicated |  |
| I83 | distribution DI9 | Distribution | Minor | Accepted | Pass-through switch wired into the production-sector prices only | Replicated |  |
| I84 | distribution DI10 | Distribution | Minor | Accepted | Median statistic: the targeted transfer only reaches deciles where more than half receive | Replicated |  |
| I85 |  | Inputs (ScenarioDefinition) | Minor | Accepted | Percentages typed as whole numbers on 8 inputs | Replicated |  |
| I86 |  | Inputs (ScenarioDefinition) | Minor | Accepted | Input names: spelling not uniform | Replicated | L137 |
| I87 |  | Inputs (ScenarioDefinition) | Minor | Accepted | Inputs without a name | Departs (user decision) | L137 |
| I88 |  | Inputs (ScenarioDefinition) | Minor | Accepted | One Dashboard cell feeds two inputs | Replicated | L137 |
| I89 | DI1 < I4 | Data | Major | Closed | Price vintage: data prices end in 2022 (legacy 465: 2024) | Replicated |  |
| I90 | DI2 < I13 | Data | Major | Open | Data for other countries: proprietary tables are Egypt only | Prototype limitation |  |
| I91 | DI3 < I17 | Data | Major | Accepted | Egypt GHG inventory: energy CH4 breaks after 2021 | Replicated |  |
| I92 | DI4 < I22 | Data | Major | Accepted | Fuel-use shock of 2023-2024 (replicated v0.3.11) | Replicated |  |
| I93 | DI5 < I37 | Data | Minor | Accepted | Primary energy of renewables: efficiencies not exactly 1 | Replicated |  |
| I94 | DI6 < I38 | Data | Minor | Accepted | Legacy's stored run: wind and solar capex time factors 2039-2041 differ from its Power tab | Replicated |  |
| I95 | DI7 < I68 | Data | Minor | Open | NDC reference years outside the data | Replicated |  |
| I96 | DI8 < distribution DI3 | Data | Minor | Accepted | Elasticities always overall, mean | Replicated |  |
| I97 | DB2 < I65 | Data | Very high | Open | Blank VAT cells in the IMF price dataset | The prototype has the fix of bug L170 (a blank takes the general VAT rate) | L170, LD3 |
| I98 | DB1 < I64 | Data | Extremely high | Open | Combustion emission factors: GAINS base and final factors only | Replicated | L58, L59 |
| I99 | DB3 < I20 | Data | Major | Closed | Electricity price data differ from legacy | Replicated | LD4, LD33, I14 |
| I100 |  | Mitigation | Major | Accepted | Transport co-benefits use the engineer road model whatever TrModel | Replicated |  |
| I101 |  | Mitigation | Major | Accepted | Coal and gas margins read at a typed year (2024) | Replicated |  |
| I102 |  | Mitigation | Minor | Accepted | Fuel price reform: strict target test; Percentage rate from the first-year step | Replicated |  |
| I103 |  | Mitigation | Minor | Accepted | Feebates held at the target rate whatever ExtendCarbonPriceBeyondOutro | Replicated |  |
| I104 |  | Mitigation | Major | Closed | Air-pollution unit costs are average, not marginal, damages | Departs (user decision) |  |
| I105 |  | Mitigation | Major | Accepted | wel.air linearised on one legacy policy run | Departs (user decision) |  |
| I106 |  | Mitigation | Minor | Accepted | Typed Egypt values freeze the AP and VSL options of the cached run | Departs (user decision) |  |
| I107 |  | Mitigation | Minor | Accepted | FFS lines: diesel valued at oil-product costs; global SCC; separate welfare | Replicated |  |
| I108 |  | Mitigation | Minor | Accepted | Electricity externalities blank in the subsidy block | Replicated |  |
| I109 |  | Mitigation | Minor | Accepted | Subsidy-block VAT: general rate, household share only | Replicated |  |
| I110 |  | Mitigation | Minor | Accepted | Subsidies computed for scenario 1 only | Departs (user decision) |  |
| I111 |  | Mitigation | Major | Accepted | Transport co-benefits: scenario-1 margins, fixed per-km costs, rectangle welfare | Replicated |  |
| I112 |  | Mitigation | Minor | Accepted | Air pollution horizon 2040: 2041 = 2040 | Replicated |  |
| I113 |  | Mitigation | Major | Accepted | Pigouvian netting: top-up over existing taxes; climate charged twice | Replicated |  |
| I114 |  | Mitigation | Minor | Accepted | Pigouvian phase-in anchored on CPIntro; applied in policy scenarios only | Replicated |  |
| I115 |  | Mitigation | Minor | Accepted | Pigouvian and efficient prices use different externality vintages | Replicated |  |
| I116 |  | Mitigation | Minor | Accepted | Climate damage per unit: national SCC x generic EF | Replicated |  |
| I117 |  | Mitigation | Minor | Accepted | One Pigouvian for all other oil products, at the power-plant AP cost | Replicated |  |
| I118 |  | Mitigation | Minor | Accepted | Road damage only for diesel | Replicated |  |
| I119 |  | Mitigation | Minor | Accepted | Electricity Pigouvian tax always 0 | Replicated |  |
| I120 |  | Mitigation | Minor | Accepted | Efficient prices: VAT on consumer fuels only, 2022 rate, scenario-1 supply cost | Replicated |  |
| I121 |  | Mitigation | Minor | Accepted | Electricity AP cost per kWh assumes a fixed 31% thermal efficiency | Replicated |  |
| I122 |  | Mitigation | Minor | Accepted | Exact switch texts; dead code cells I2202:I2203 | Replicated |  |
| I123 |  | Mitigation | Major | Open | CBAM block: Egypt only, no output read anywhere | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I124 |  | Mitigation | Minor | Open | Green investment: cumulative need uses 35 years, the phase-out 34 | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I125 |  | Mitigation | Minor | Open | Green investment section stops at 2040 | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I126 |  | Mitigation | Minor | Open | Green public investment is report only; constants typed in Mitigation | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I127 |  | Mitigation | Major | Open | Green investment: #N/A for countries outside the CCDR list | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I128 |  | Mitigation | Minor | Open | Green investment: annual GDP shares summed against a discounted ratio | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I129 |  | Mitigation | Minor | Accepted | Current account % GDP: GDP implied by CA / CA% | Replicated |  |
| I130 |  | Mitigation | Minor | Accepted | Current account in current prices: no hold rule after the data | Replicated |  |
| I131 |  | Mitigation | Minor | Open | GVA shares floored at 1% for the chart | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I132 |  | Mitigation | Minor | Open | "GVA" is GTAP gross output; 2014 IO inflated by a fixed CPI index | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I133 |  | Mitigation | Minor | Open | Cumulative table: direct emissions only; repeated MTOutputs codes | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I134 |  | Mitigation | Minor | Open | GTAP mapping: coal mining to food, crude to fuel transformation, gas to power | Not built: deferred by the user (2026-10-29; legacy work in progress) |  |
| I135 |  | Mitigation | Minor | Accepted | Initially exempt demand mutes the usage response to every price change | Replicated |  |
| I136 |  | Mitigation | Major | Accepted | Exempt share denominator: basket spend, not the sum of deciles | Replicated |  |
| I137 |  | Mitigation | Minor | Accepted | Most-used cooking fuel defaults to LPG when the WHO code is missing | Replicated |  |
| I138 |  | Mitigation | Minor | Accepted | Leakage to biomass on the not-exempt use only | Replicated |  |
| I139 |  | Mitigation | Minor | Accepted | Manual price rows switch on only with a 2021 value; years 2021-2026 only | Replicated |  |
| I140 |  | Mitigation | Minor | Accepted | Blank manual elasticity gives "no data" and an error | Replicated |  |
| I141 |  | Mitigation | Minor | Accepted | Methane intensity decline: rates borrowed across sources, decline from 2024 | Replicated |  |
| I142 |  | Mitigation | Minor | Accepted | Power cost breakdown: no shadow-price column, floor ignored | Replicated |  |
| I143 |  | Mitigation | Minor | Accepted | Road other biofuels use oil elasticities and oil AEEI | Replicated |  |
| I144 |  | Mitigation | Minor | Accepted | Self-generated renewables priced at the solar investment cost, no policy | Replicated |  |
| I145 |  | Mitigation | Minor | Accepted | Range anxiety: negative values held; one-year fit | Replicated |  |
| I146 |  | Mitigation | Minor | Accepted | Electricity producer subsidy per kWh floored at -0.3 $/kWh | Replicated |  |
| I147 |  | Mitigation | Major | Closed | Food & forestry local pollutants far above the legacy air-pollution input | Replicated | LD53, LD81 |
| I148 |  | Data | Extremely high | Open | Current account data typed for Egypt only | Replicated | L50, LD89 |
| I149 |  | Mitigation | Minor | Accepted | Other energy use takes the largest emission factor of each fuel across the other subsectors | Replicated |  |
| I150 |  | Data | Minor | Open | Spot coal and gas prices of Egypt hold a year and 0 in legacy 465 | Departs (user decision) |  |
| I151 |  | Mitigation | Major | Accepted | Pigouvian road-transport component: base-year value x growth of the per-km costs | Departs (user decision) |  |
| I152 |  | Mitigation | Minor | Open | Methane abatement curves: no fallback to the Average coefficients | Not replicated yet: queued to be replicated (no user decision) |  |

## 3. Departures (LD, sheet LegacyDiff)

| Code | Type | Area | Departure | Why | See also |
|---|---|---|---|---|---|
| LD2 | Decision | Other oil products: pass-through and margin | Legacy: Hardcoded 1 and 0. Prototype: From the IMF dataset like the other oil products (Egypt 0 and 7.95 $/bbl). | User decision v0.0.10: the legacy rule drove the retail price to the 0.01 floor and fuel use 10x by 2030 |  |
| LD3 | Bug fix | VAT rate where the dataset is blank | Legacy: 0. Prototype: General VAT rate VAT_WEO for residential coal and gas and all-sector oil products; 0 for power, industry, biomass. Only for blank cells (v0.0.14). | Legacy bug L170 (v0.8.5, user 2026-10-29; was data bug DB2): a blank is a missing value, not a zero; the data problem is issue I97 (very high) | L170, I97 |
| LD5 | Bug fix | Oil-product share in the VAT of transport fuels | Legacy: VAT rate x oil-product share. Prototype: VAT rate x household share of the oil product (sheet OilProductShares, as legacy rows 801-816; v0.4.12); VAT payment = (supply cost + taxes) x rate x share. | Replicated (user decision 2026-10-18: an issue, not a bug: legacy means to charge VAT only on the household share, firms reclaim it; issue I39); legacy bug L60 fixed (VAT payment divided by 1 + full rate) |  |
| LD6 | Bug fix | New ETS price | Legacy: Cap relative to baseline; quick estimate (linear in the semi-elasticity) and a VBA goal seek on an override row. Prototype: Same cap; fast estimate in log form LN(cap/baseline)/(semi x effectiveness x volatility adjustment); override row pasted from ets_goalseek.py (Python, same damped log-space step, no VBA); baseline covered emissions are data from scenario 1 (bco2). | Legacy bug L57 (user 2026-10-18): the quick estimate is linear in the semi-elasticity, while the cap is a relative change of emissions (legacy note "arguably exp/ln"); the log form hits the cap. No circular reference |  |
| LD8 | Bug fix | ETS volatility | Legacy: Relative price ETS vs tax hardcoded 1.1 (row 1843); volatility inputs feed a factor not used. Prototype: Volatility adjustment (1 + policy risk x impact)/(1 + volatility x impact) from MTInputs 95-97 (1/1.1 at Medium) on the tax-equivalent price and in the fast estimate. | Legacy bug L15: the relative price is a hardcoded 1.1 and the volatility inputs are not used (user suggestion v0.1.02: volatility-dependent effectiveness) |  |
| LD10 | Bug fix | Policy paths after the target year | Legacy: Per instrument: carbon price and fuel price reform follow the ExtendCarbonPriceBeyondOutro switch (reform: 0 under No, rate x last year under Percentage); feebates constant. Prototype: The same (v0.9.0; v0.0.8-v0.8.5: linear for the reform and feebates); legacy bugs L171 (hold the target under No) and L173 (1 + rate) fixed; ETS benchmarks constant; ETS cap per MTInputs switch. | User decision 2026-10-29: revert to legacy |  |
| LD13 | Decision | Biomass carbon-tax coverage | Legacy: No switch. Prototype: TRUE (EF 0). | User decision v0.0.8 |  |
| LD14 | Decision | Sign of subsidies | Legacy: Subsidy cost reported as a positive number. Prototype: Subsidies negative: esub, esubpu, rsub, prsub, sgap, rgap; net existing revenue rnet = rtx + rsub. | User rule v0.2.4 |  |
| LD15 | Decision | Constants and row pointers | Legacy: Typed in cells and formulas (e.g. 8760, 8.76, 1000, 0.01, MTInputs row numbers, baseline values). Prototype: Looked up: named constants and policy assumptions on sheet Constants, MTInputs rows on Mapping (by NameOfParameter or label), baseline CO2 on sheet BaselineCO2. | User rule v0.2.4 |  |
| LD16 | Bug fix | Margins and production costs | Legacy: Coal and gas margin read at 2024 (typed), oil products at the base year; production cost weighted by the share produced domestically; both added unconverted (nominal). Prototype: The same years and weight (v0.9.0), converted to real with the CPI index of the year read. | User decision 2026-10-29: as legacy; legacy bug L172 fixed (nominal added to real); typed year issue I101; domestic-production weight LD80 |  |
| LD23 | Bug fix | Power: bug fixes (v0.1.06) | Legacy: Ten defects (CPAT-AI-Mitigation-Prototype_BugsIssuesUpgrades_v0.6.4.docx): services demand with the industrial multiple from 2024; efficiency exponent with eps_F; income factor twice; LT storage allocation twice; investment spending at base capital cost; investment logit normalised by non-permitted types; early-retirement units; coal effective retirement uncapped; feebate rebate x 1.22; capacity check on the plan; v0.4.14: new capacity sized for this year's demand although it comes online next year (L67, was I8). Prototype: Fixed. | User request v0.1.06; L67 by user decision 2026-10-18 |  |
| LD28 | Simplification | Power: features not built | Legacy: Power demand from the elasticity model, carbon price on power use (feebate on demand). Prototype: Dropped (user decisions 4 and 5 of the power plan; the rebate covers the demand-side feebate). Built: v0.5.4 PPAs, deficit to gas, renewable subsidies, rebate, electricity excise, every power input by scenario; v0.5.6 manual capacity and investment (P3: rows mancap, mani, needm; Manual inputs 349-357 scenario 1, 363-371 other scenarios; legacy bug L118 fixed: logit investment sized on the need net of manual investment). | Scope (power plan) |  |
| LD38 | Bug fix | Existing carbon pricing | Legacy: ECP data by country (national and regional ETS blocks, carbon tax with fuel-specific rates), coverage by year; ctx and ets inside txo; free allocation and revenue data. Prototype: As legacy (v0.4.12): carbon tax with the single rate or fuel rates (single price? flag), national ETS and the EU ETS (EU ETS? = Yes or Both) added up, coverage of each data year (blank = 0), the last data year after; each scheme read from its own block of sheet ECP; the sector of the price fuel (oil products: transport; other oil products: industry); only the change against the level in the price data enters prices and revenue (legacy: ctx and ets inside txo, same numbers); existing ETS revenue at full price and free-allocation and revenue data unused, as legacy. | User decision 2026-10-18 (replicate legacy, several schemes; was issue I7); legacy bugs fixed: L61 (EU ETS grows with the carbon-tax growth), L62 (transport diesel, LPG, kerosene tax rows take the rate row as coverage), L63 (fuel coverage range cut short), L64 (no ETS on other oil products outside power), L65 (complementary tax with last year's ETS coverage) |  |
| LD40 | Decision | Horizon and indices | Legacy: To 2050 (power block to 2041); CPI held flat after 2031. Prototype: To 2041 (v0.2.3; the last year is the LAMBDA year); same indices; values after 2030 not a legacy target. | User decisions v0.0.9 / v0.0.11 / v0.2.3 |  |
| LD43 | Bug fix | GHGs: non-energy methane (v0.2.8) | Legacy: Livestock, rice and waste CH4 constant (inventory); abatement computed but not applied; waste uses the livestock curve. Prototype: Grow with income and population (legacy elasticities); the methane fee abates each source along its own CH4Inputs curve. | Legacy bugs L18, L21 |  |
| LD44 | Bug fix | GHGs: flaring (v0.2.8) | Legacy: CO2 from flaring abated oil and gas methane added to CH4 (divided by the CH4 GWP). Prototype: Reported as CO2 in energy (ghg.flr). | Legacy bug L19 |  |
| LD45 | Bug fix | GHGs: population (v0.2.8) | Legacy: Growth path 2-4% a year from 2027 (rows 481, 2428). Prototype: UN WPP (sheet UNPop). | Legacy bug L20 |  |
| LD50 | Bug fix | Local pollutants: navigation (v0.2.9) | Legacy: Navigation missing from the pollutant totals. Prototype: Navigation included in the transport and total rows. | Legacy bug L22 |  |
| LD52 | Bug fix | Local pollutants: total (v0.3.0) | Legacy: Total of a pollutant leaves out services and food & forestry (the sectors include them). Prototype: Total = all subsectors + power = sum of the seven air-pollution sectors. | Legacy bug L23 |  |
| LD54 | Bug fix | GDP effects: feedback (v0.3.1) | Legacy: GDP effect (a change of the GDP level) added to GDP growth every year (row 2446 = 2444 + 2445). Prototype: GDP level raised by the effect: growth = (1 + baseline growth) x (1 + effect(t-1)) / (1 + effect(t-2)) - 1. | Legacy bug L24 (user decision v0.3.1: fix) |  |
| LD59 | Decision | Road transport: engineer model (v0.3.5) | Legacy: Key inputs 15 and section 5 (rows 2017-5378), switch TrModel (MTInputs F340; template default Engineer, Egypt run Elasticity). Prototype: Section 5b of every scenario group, every row live (Methods, chapter Transport); TrModel default Elasticity, Engineer by switch; the 17 legacy bugs of Methods, chapter Transport section 3 fixed (B1-B23). | User rule 2026-10-14: match legacy except where legacy has a bug; results unchanged until the engineer run is reviewed |  |
| LD60 | Decision | Road transport: policy inputs (v0.3.5) | Legacy: Dashboard rows 61-98 and 540-559 (outside MTInputs). Prototype: Policies: MTInputs rows 416-477 after the template (scenario-specific, legacy Dashboard defaults, all off); parameters and hardcoded literals (Gompertz constant, gas liters per GJ, PHEV kWh per liter, insurance factor, BEV distance caps, price elasticities): sheets TransportParams, TransportPaths and named constants. | Scenarios carry the transport policies; no literal in a formula (Methods, chapter Transport section 2) |  |
| LD61 | Assumption | Road transport: inputs from the rest of the model (v0.3.5) | Legacy: Legacy rows of the price, power and macro blocks. Prototype: Section 5 road after-tax prices x GJ per liter (gas $/GJ / gas liters per GJ); industrial gas: section 2 price + road new policies; power prices of section 3 G (last year); GDP growth of row 7 (last year); population and real GDP after the feedback; carbon price x road feebate coverage; 2-3 wheelers: the gasoline price incl. new policies (legacy row 4438: before new policies); VAT on vehicles: VAT_WEO of the customs year (Egypt 0.14; legacy 0.1531). | One source for each input in the prototype; carbon pricing reaches 2-3 wheelers |  |
| LD64 | To check (bucket 5) | Road transport: kept as legacy (v0.3.5) | Legacy: Freight distance (survey B14), data years of customs, VAT and import shares, the externality sheet Transport. Prototype: Kept (freight distance, data years: parameters) or not built (externalities). | Data decisions; scope (Methods, chapter Transport section 6) |  |
| LD69 | Decision | ETS goal-seek settings (v0.5.2) | Legacy: Manual inputs E10:E12 (names ETSMaxIterations 30, ETSStartFreshContinue 'Continue', ETSErrorTolerance 0.001), read by the VBA goal seek (SolveFast). Prototype: The same cells and names, read by the macro SolveETS and ets_goalseek.py (before v0.5.2: constants in the code); values 20, Continue, 0.005, the prototype error being the worst yearly /covered / cap - 1/; StartFresh starts from the fast estimate ets.est, Continue from the override row if it holds prices. | User decision 2026-10-19: keep the values the prototype goal seek has always used, so that stored results do not change; the legacy defaults are noted on the sheet |  |
| LD72 | Bug fix | Non-energy GHG elasticities (v0.5.2) | Legacy: Manual inputs K326:M327 never used: K326 is a broken formula (#REF!) and Mitigation K366:M367 test the switch ElastIncAdjustment for "Manual", which it never holds, so the fixed values 0.9, 1, 1, 0.15 apply. Prototype: Read from Manual inputs K326:M327 (legacy default values typed; text "na" = 0) by the rows ghg.dr and ch4.act of section 14; before v0.5.2 sheet Constants (ghg.el). | Legacy bug (the manual cells cannot take effect; L102): fixed, the cells are the input |  |
| LD74 | Decision | Power: inputs by scenario (v0.5.4, P2) | Legacy: Each MTInputs column runs with its own baseline and policy run, so every power input can differ by scenario. Prototype: Every MTInputs power input (rows 242, 262, 340-413, 482) read in the scenario's own column (section-1 rows; section 3 sub-table A0 applies them to the power data); scenario 1 is the baseline of every scenario, so a technical input changed in a policy scenario changes that scenario only. | User decisions 2 and 8 of the power plan (2026-10-18) |  |
| LD76 | Bug fix | Power: renewable subsidies (v0.5.4) | Legacy: Base subsidy (MTInputs 352) + additional subsidy of the policy run (353) phased out over 354 years from the consumer-subsidy phase-out year (MTInputs 132, bug L107); hydro if 355 = Yes; in the levelised cost (C5) and revenue (3665-3669); "Cost of renewable subsidies" counts the base subsidy twice and omits biomass (rows 7897-7903, bug L108); inputs in nominal $/kWh used as real (issue I55). Prototype: Rows rnsp, rns, lfx, prrns: own start year RenSubsidyAddStartYear (MTInputs row 482, default 2027 = the default of row 132); revenue = subsidy x generation by type, in the power subsidies and 12e row ren; nominal inputs used as real, as legacy. | Legacy feature; bugs L107, L108 fixed |  |
| LD77 | Bug fix | Power: revenue rebate and electricity excise (v0.5.4) | Legacy: Rebate: carbon cost removed from end-user prices (PowerRebates or a feebate scenario, policy run; rows 3595, 3615, 3644), memo 3663 incl. VAT never counted as revenue (bug L110). Excise: grid intensity of the base year x carbon price in the scenario Electricity excise (row 2253; issue I56) and the manual excise of Manual inputs 161-162 (AdditionalExcise; rows 3602, 3631), whose revenue memo counts the whole excise (row 3660, bug L111). Prototype: Rows rbs, exs, entxd, entx, pex, rp, rnvat, rreb, rpex, rexs, rexm: rebate = carbon cost x pass-through (its VAT falls out of rnvat); excise revenue = the excise in the price x consumption; switches accept Yes or Yes* (issue I58). | Legacy features; bugs L110, L111 fixed |  |
| LD79 | Bug fix | Power: capex decline options Low and Vhigh (v0.5.4) | Legacy: The Power tab has no Low and Vhigh capex time factors for wind and solar (only the older series oldlow, oldvhg) and no Vhigh for other renewables: the lookup fails (rows 3038-3046; bug L109). Prototype: The missing series falls back to the older series of the same option (wind, solar) or Medium (Inputs_ppath rows tcf/<type>/<option>). | Legacy bug L109 fixed |  |
| LD81 | Bug fix | Welfare: co-benefits | Legacy: wel.air and the road co-benefits from the Air pollution and Transport sheets' own runs (wel.air from AP 3217); unit-cost bugs L189, L190, L191, L192, L193. Prototype: wel.usd = climate + air pollution (value per ug/m3 x change in the modelled PM2.5 of the prototype's emissions, section 17b) + road co-benefits (accidents, congestion, road damage per litre) - efficiency costs (v0.9.0, R1-R2); typed Egypt inputs on the module tabs FromAirPollution and FromTransportCB (other countries 0). | R2, user decision 2026-10-29; never replicate a bug; unit costs as marginal damages (L224); issues I105, I106, I111, I112 |  |
| LD82 | Bug fix | Social costs, FFS and subsidies | Legacy: Rows 17678-17951 with bugs L176, L177, L178, L179, L180, L181, L182, L183, L184, L185, L186, L187, L188. Prototype: Section 18 (v0.9.0, R2): climate costs per GJ, own-sector quantities, consumption-weighted other lines, GDP of the year; explicit and implicit subsidies (16 lines x 8 variables) in every scenario group (I110). | Never replicate a bug; issues I107, I108, I109 replicated |  |
| LD89 | Bug fix | External balance (current account) | Legacy: Rows 18180-18198: #NAME?/#N/A (stale WEO codes, L50); 18195 leaves coal out (L214); gas bill x $/MMBtu (L215). Prototype: Section 16b rows bca.* (v0.9.0, R11): typed WEO values for Egypt (held at 2031), change = - xnim by fuel group, % of GDP over the implied GDP, coal included; other countries 0 (I148). | Never replicate a bug; issues I129, I130 replicated |  |
| LD90 | Not yet | CBAM process emissions, green public investment, emissions intensity of industrial output | Legacy: Rows 5867-6022 (CBAM), 6215-6267 (green investment), 18631-18771 (GVA and intensity): work in progress in legacy, no output read by the model. Prototype: Not built (R4, R5, R12 deferred by the user 2026-10-29; designs on branch wip-r4-r5-r12). | User decision 2026-10-29: the legacy WIP is not linked up |  |
| LD91 | Bug fix | Air-pollution unit costs | Legacy: Average damages per fuel (attributed deaths per ktoe x VSL; AP 3731-4378), used in the Pigouvian taxes, efficient prices, implicit subsidies and FFS. Prototype: Marginal damages (v0.9.0): value of averted PM2.5 x concentration coefficients x emission factors, lines weighted by fuel use; legacy values kept as a memo on FromAirPollution. | Legacy bug L224 (user 2026-10-29; was issue I104) |  |

## 4. Upgrades (U)

| Code | Priority | Upgrade | What and why |
|---|---|---|---|
| U1 | High | Review in Excel 365 | The user runs the checklist (ExcelReview_Checklist.md) on Windows: CheckBatchRun, the batch run, ScenarioCompare, no repair prompt and no circular-reference warning (I1). |
| U2 | High | Numerical check against legacy CPAT for Egypt | Explain the distance to the legacy run (I14) sector by sector, on the latest legacy file (465; was 459). |
| U4 | High | Report the legacy bugs to the CPAT team | Send the register (L1-L128, D1-D31) and the cell-level fix plans; legacy issues for the team, high priority for them: I62 (partial adjustment), I71 (population takes the income elasticity), I72-I74 (circularity). |
| U5 | Medium | Copy-paste stress test | Add a fuel, a subsector and a scenario by dragging; fix what breaks. |
| U6 | Medium | Other gases, local pollutants and process emissions | CH4 and N2O done (v0.2.8), local pollutants (v0.2.9); inventory-adjusted EFs and process CO2 remain. |
| U7 | Medium | Regulations as shadow prices | Fill the regulation rows (placeholder 0) and their efficiency-margin adjustments (MTInputs 247-250). |
| U10 | Medium | Data for more countries | Energy balances, GDP and EFs beyond Egypt (I90). |
| U13 | Low | Planned retirement data for Egypt | Enter PowerPaths pret/<type> where plans exist. |
| U14 | Low | Python port | The check script already recomputes every value in Python. |
