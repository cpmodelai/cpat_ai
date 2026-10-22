# CPAT policy taxonomy, extended to cover every FTT policy (plan, 2026-10-20; decisions open)

Proposal for one policy taxonomy that serves both CPAT projects (ScenarioDefinition, the prototype scenario definitions and `coded/cpat_model/constants.py`). It keeps every policy CPAT has today and adds every policy instrument in the FTT (Future Technology Transformations) models, so that a policy in either model has a slot in the taxonomy.

Sources:
- CPAT: `templates/MTInputs_template.xlsx` (legacy MTInputs rows), the prototype road and power rows (`Transport_Method.md` section 2, excel_ai/plans/Power_features.md), the main-scenario list (`Scenarios_Method.md` section 2b; `constants.py` `ALL_SCENARIOS`).
- FTT: the open-source stand-alone FTT, `github.com/cpmodel/FTT_StandAlone` at commit 8cf4bfd (2026-10-13): `Utilities/titles/VariableListing.csv`, `ftt_source/ftt_core/` (mandates, emissions regulation, exogenous sales and capacity), `ftt_source/Power/ftt_p_phase_out.py` and the LCOE/LCOT/LCOH cost functions where each policy enters. Modules: FTT:Power (P), FTT:Transport, passenger road (Tr), FTT:Freight (Fr), FTT:Heat, residential (H), FTT:Industrial Heat (IH: chemicals CHI, food-beverages-tobacco FBT, machinery and transport equipment MTM, non-metallic minerals NMM, other industry OIS).

## 1. Structure

Three levels:

1. **Family** (what kind of instrument): 10 families, section 2.
2. **Instrument** (one policy lever, with its own inputs): code `<family>.<instrument>`, section 3.
3. **Application**: sector coverage, fuel or technology coverage, and timing (start year, target year, start and target level, continuation). These stay as the ScenarioDefinition coverage switches and paths CPAT already has; they are not separate instruments.

Each instrument also carries a **representation** tag, because CPAT and FTT model policies differently. FTT chooses between technologies (shares equation on levelised costs, with regulations, mandates and exogenous changes acting on capacity or sales); CPAT models fuel demand with elasticities, with technology choice only in the engineer power model (and the dropped engineer road model).

| Tag | Meaning in CPAT |
|---|---|
| **D** direct | Changes a price, tax or quantity CPAT computes (retail price, power LCOE, power capacity) |
| **S** shadow price | Converted into an implicit carbon price on the efficiency margin (`reg.<sector>`, ScenarioDefinition rows 247-251), as CPAT does for its regulation scenarios |
| **X** exogenous path | An exogenous efficiency gain, demand path or capacity path (ScenarioDefinition rows 241-245, power manual capacity) |
| **N** needs a technology module | Cannot be represented faithfully without technology shares in that sector; at most S or X as an approximation |

## 2. Families

| Code | Family | Covers |
|---|---|---|
| PRC | Carbon and emissions pricing | Carbon tax, ETS, methane fee, existing carbon pricing |
| FTX | Energy taxes and price reform | Fuel excises, fuel price reform, electricity excise, VAT on energy, existing non-carbon taxes, Pigouvian tax |
| FFS | Fossil-fuel subsidy and price-control reform | Producer and consumer subsidy phase-out, price liberalisation, tax-exemption phase-out |
| TEC | Technology purchase and ownership taxes and subsidies | Upfront subsidies, purchase and registration taxes, annual ownership taxes, feebates on technology |
| OUT | Output and production support | Feed-in tariffs, per-kWh renewable subsidies, power revenue rebates |
| STD | Performance standards and regulations | Efficiency regulations, fleet CO2 standards, technology caps and bans |
| MAN | Quantity mandates and deployment | Sales mandates (ZEV, heat pumps), kick-starters, blending mandates, exogenous capacity and sales |
| PHO | Phase-outs of existing assets and contracts | Coal phase-out, PPA phase-out, investment-permission dates |
| BRD | Border measures | CBAM coverage |
| REV | Revenue use | Labour and corporate tax cuts, public investment, current spending, targeted transfers, rebates |

## 3. Instruments

Status: **C** in CPAT now; **C+F** in both; **F** FTT only (new for CPAT). "CPAT sector" names the CPAT sector the FTT module maps to.

### PRC: carbon and emissions pricing

| Code | Instrument | Status | CPAT now (ScenarioDefinition) | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| PRC.CTAX | Carbon tax, by sector and fuel | C+F | rows 18-47 | `CO2taxP`, `CO2taxTr`, `CO2taxFr`, `CO2taxH` (USD 2023/tCO2, region x year; added to LCOE/LCOT/LCOH as emissions x price) | P, Tr, Fr, H | D | All |
| PRC.ETS | New ETS (cap, auctioning, benchmarks) | C | rows 83-115 | (FTT takes a permit price only, via the sector carbon price) | | D | Covered sectors |
| PRC.EXIST | Existing carbon tax and ETS | C | rows 208-214 | | | D | All |
| PRC.CH4 | Methane fee | C | rows 184-189 | | | D | Fossil-fuel supply, non-energy |
| PRC.TCP | Total carbon price measure | C | `TCP` scenario | | | D | All |

FTT has no carbon price variable for industrial heat; the IH modules price carbon through their fuel tax (FTX.FUEL below).

### FTX: energy taxes and price reform

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| FTX.FUEL | Fuel excise by fuel and sector | C+F | Fuel price reform rows 139-183; `Coal excise`, `Road fuel tax` scenarios | `MTFT` (P, by technology, multiplies fuel cost), `RTFT` (Tr, cents/litre), `RZFT` (Fr, $/MJ), `HTRT` (H, % of fuel cost, also a subsidy if negative), `IFT1`-`IFT5` (IH, 2010 EUR/MWh) | P, Tr, Fr, H, IH | D | Power, road, residential, industry subsectors |
| FTX.ELEC | Electricity excise and electricity emissions tax | C | `Electricity excise`, `Electricity emissions tax` scenarios; Manual inputs 161-162 | | | D | Power |
| FTX.VAT | VAT reform on energy | C | row 284 | | | D | Residential, transport |
| FTX.EXIST | Existing non-carbon taxes | C | rows 286-294 | | | D | All |
| FTX.PIGOU | Pigouvian (externality) tax | C | rows 212, 216-218 | | | D | All |
| FTX.DIST | Distance tax | C | road rows 418-479 | | | D (road model) | Road |

### FFS: fossil-fuel subsidy and price-control reform

| Code | Instrument | Status | CPAT now | FTT | Rep. |
|---|---|---|---|---|---|
| FFS.PROD | Producer subsidy phase-out | C | rows 122-129 | | D |
| FFS.CONS | Consumer subsidy phase-out | C | rows 130-138 | (a negative `HTRT` is a fuel subsidy in heat) | D |
| FFS.PCTRL | Price-control phase-out (liberalisation) | C | rows 190-195 | | D |
| FFS.EXEMPT | Carbon-tax exemption phase-out | C | rows 48-51 | | D |

### TEC: technology purchase and ownership taxes and subsidies

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| TEC.UPSUB | Upfront capital subsidy (% of investment cost) by technology | F (C for EVs) | EV purchase subsidy, road rows | `MEWT` (P), `HTVS` (H), `ISB1`-`ISB5` (IH) | P, H, IH | D in power (capital cost of the engineer model); N elsewhere (S as approximation) | Power, residential, industry |
| TEC.PURTAX | Purchase tax or subsidy per vehicle, by technology | C+F | ad-valorem purchase taxes, VAT and customs on BEVs (road rows) | `TTVT` (Tr, th $/veh), `ZTVT` (Fr, $) | Tr, Fr | N (road model dropped) | Road |
| TEC.REGTAX | CO2-differentiated registration tax | F | | `RTCO` (Tr, $/gCO2/km) with `Base registration rate` (share of price, by technology); `RZCO` (Fr) | Tr, Fr | N; S as approximation | Road |
| TEC.ANNTAX | Annual road (circulation) tax by technology | F | | `TTRT` (Tr, $/y), `ZTRT` (Fr, $/vehicle-y) | Tr, Fr | N; S as approximation | Road |
| TEC.FEEBATE | Feebate on emission intensity, by sector or vehicle class | C | rows 52-82 (power, transport, residential, industry); road feebates by class; `Feebates`, `Power feebate` scenarios | (FTT: a registration tax with a negative base rate for clean technologies acts as a feebate) | | S (D in power) | Power, road, residential, industry |
| TEC.INFRA | Charging-infrastructure subsidy | C | road rows | | | N | Road |

### OUT: output and production support

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. |
|---|---|---|---|---|---|---|
| OUT.FIT | Feed-in tariff / per-unit output subsidy by technology | C+F | Renewable subsidy $/kWh, rows 352-357 (all renewables, optional hydro) | `MEFI` (P, USD/MWh, subtracted from LCOE, by technology), `HEFI` (H, renewable-heat tariff) | P, H | D in power; N in residential |
| OUT.REBATE | Power revenue rebate | C | row 342 (PowerRebates) | | | D |

### STD: performance standards and regulations

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| STD.EEREG | Energy-efficiency regulation by sector | C | `Energy efficiency regulations`, `Residential ...`, `Industrial efficiency regulations` scenarios; rows 241-251 | | | S / X | Residential, industry, services |
| STD.FUELECON | Vehicle fuel-economy standard | C | `Vehicle fuel economy` scenario; row 248 | | | S | Road |
| STD.FLEETCO2 | Fleet-average CO2 standard on new sales (`[start, end, max reduction]`, linear to the target; sales move from high- to low-emitting technologies) | F | | `EV CO2 regulation` (Tr), `EV truck CO2 regulation` (Fr); exclusive with MAN.SALES in the same sector | Tr, Fr | N; S as approximation (the fuel-economy shadow price is the nearest CPAT slot) | Road |
| STD.TECHCAP | Technology capacity cap or ban on new capacity (cap in GW or share; -1 = no new capacity) | F (part C) | Power: investment-permission dates and new-investment overrides, rows 396-415 | `MEWR` (P, GW), `TREG` (Tr, share), `HREG` (H), `ZREG` (Fr), `IRG1`-`IRG5` (IH, GW) | P, Tr, Fr, H, IH | D in power (extends rows 396-415 from on/off by date to a cap path); N elsewhere | Power, road, residential, industry |

### MAN: quantity mandates and deployment

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| MAN.SALES | Sales mandate for clean technologies (`[start, end, max share]`, linear from 0 to the max share of new sales) | F | | `EV mandate` (Tr), `EV truck mandate` (Fr), `HP mandate` (H) | Tr, Fr, H | N; X as approximation (fuel switch path) | Road, residential |
| MAN.KICK | Kick-starter (a sales mandate with a low max share, early years only) | F | | `EV truck kickstarter` (Fr); seeding of clean technologies in low-adoption regions is built into Tr, Fr and H (not a policy input) | Fr | N | Road |
| MAN.BLEND | Fuel blending mandate | F | | `RBFM` (Tr, biofuel %), `ZBFM` (Fr, biofuel %), `RHSM` (hydrogen share in freight) | Tr, Fr | D (changes the fuel mix and emission factor of road fuels; needs biofuel and hydrogen prices) | Road |
| MAN.EXOCAP | Exogenous capacity target by technology | C+F | Power manual capacity and investment (Manual inputs 342-371, P3) | `MWKA` (P, GW) | P | D / X | Power |
| MAN.EXOSALES | Exogenous sales or share shift by technology (sums to zero; capped at 80% of replacement sales) | F | | `TWSA` (Tr), `HWSA` (H), `ZWSA` (Fr), `IXS1`-`IXS5` (IH) | Tr, Fr, H, IH | N; X as approximation | Road, residential, industry |

### PHO: phase-outs of existing assets and contracts

| Code | Instrument | Status | CPAT now | FTT | Rep. |
|---|---|---|---|---|---|
| PHO.COAL | Coal-power phase-out (linear to zero; FTT: by 2035 in high-income regions, 2045 elsewhere) | C+F | Cost-based coal retirement (rows 378-379); no mandated path | `coal phaseout` switch, applied through `MWKA` | D (as a capacity path in the engineer power model) |
| PHO.PPA | Coal and gas PPA phase-out | C | rows 381-386 | | D |
| PHO.PERMIT | Investment-permission dates by technology | C | rows 406-415 | | D |

### BRD and REV

| Code | Instrument | Status | CPAT now |
|---|---|---|---|
| BRD.CBAM | CBAM goods process-emission coverage | C | rows 116-121 |
| REV.LABOUR, REV.CIT, REV.PUBINV, REV.CURR, REV.TRANSF | Revenue use shares and transfer targeting | C | rows 196-205, 305-313 |

FTT has no border measures and no revenue recycling (in E3ME-FTT these sit in E3ME).

## 4. What changes for CPAT

1. **Instruments new to CPAT (from FTT): 9.** TEC.UPSUB (outside EVs), TEC.REGTAX, TEC.ANNTAX, STD.FLEETCO2, STD.TECHCAP (as a cap path), MAN.SALES, MAN.KICK, MAN.BLEND, MAN.EXOSALES; plus PHO.COAL as a mandated path. All other FTT policies map onto an existing CPAT instrument.
2. **Main-scenario list (ScenarioDefinition row 13, `ALL_SCENARIOS`).** The list mixes instruments and packages. Proposal: keep the 14 legacy names (paste compatibility with legacy) and record for each its taxonomy code(s) in the Mapping sheet and `constants.py`, rather than adding FTT instruments to the list. New instruments get their own ScenarioDefinition rows, so they combine with any main scenario, as feebates and ETS do.
3. **Where each new instrument can be built.**
   - Power (engineer model): TEC.UPSUB, OUT.FIT by technology, STD.TECHCAP, PHO.COAL are direct: they enter the investment cost, the LCOE or the capacity paths the model already has.
   - Road: TEC.REGTAX, TEC.ANNTAX, STD.FLEETCO2, MAN.SALES, MAN.KICK, MAN.EXOSALES need the engineer road model, which the user dropped on 2026-10-20 (I61). Without it they can only be shadow prices (STD.FLEETCO2 through the fuel-economy margin) or exogenous paths. MAN.BLEND is direct in the elasticity model.
   - Residential and industry: technology-specific instruments need a technology module that CPAT does not have; S or X approximations only.
4. **Sector mapping FTT to CPAT:** P to power; Tr to road (passenger); Fr to road (freight; CPAT has no passenger/freight split); H to residential (heating only); IH CHI to mining & chemicals, FBT to food & forestry (closest), MTM to machinery, NMM to cement, OIS to other manufacturing.

## 5. Decisions needed (user)

1. Is this the FTT meant? This plan uses the open-source stand-alone FTT (P, Tr, Fr, H, IH). E3ME-FTT versions also have FTT modules for steel, hydrogen and agriculture; their policies are not in the stand-alone code.
2. Taxonomy only, or also build? Recommendation: adopt the taxonomy now (codes in Mapping and `constants.py`, a code next to each ScenarioDefinition policy row), then build the power instruments (TEC.UPSUB, OUT.FIT by technology, STD.TECHCAP, PHO.COAL) and MAN.BLEND, which CPAT can represent directly.
3. For the instruments tagged N: list them with their approximation (S or X), or leave them out of the ScenarioDefinition until a technology module exists?
4. Codes: keep the family.instrument codes here, or align them with the codes of `CPATMasterProcessesCodesAndDefaults.xlsx` once that alignment exercise runs?

