<!-- Research note (2026-10-29): notation, core equations and interfaces extracted verbatim from docs/01_MainDocumentation/*.qmd, with a list of notation clashes and apparent errors. Reference for completing equations.yaml; not generated, not maintained: the methodology is the authority. -->

# CPAT notation authority: notation extracted from the methodology docs

Source files (all read in full): `docs/01_MainDocumentation/02_Summary.qmd`, `03_Mitigation.qmd`, `04_Multipliers.qmd`, `05_Distribution.qmd`, `06_Air_pollution.qmd`, `07_Road_Transport.qmd` (repo `/home/user/cpat_ai`).

Conventions used in this file:

- Every LaTeX string shown in backticks or in a ```tex block is copied verbatim from the qmd source (equation blocks were extracted programmatically by line number; every symbol in the tables was machine-checked to occur verbatim in the cited file). Odd spacing such as `\text{va}t` or `\text{ocsf}` is the docs' own (Word-to-Markdown conversion artefacts) and is preserved on purpose.
- Line numbers refer to the files as checked out at the time of extraction.
- 'core' = an equation a Python rebuild must implement to reproduce the module's main outputs; 'adjustment/detail' = calibration, memo accounts, data preparation, alternative options, or derivations.
- `02_Summary.qmd` contains no mathematical notation at all (prose only); it is cited only for interfaces.

## 1. Index conventions

### 1.1 Mitigation module master indices (`03_Mitigation.qmd`, "Notation and Acronyms > Dimensions" `{#sec-ExecSummDimensions}`, lines 419–444)

Docs: *"CPAT exists across multiple dimensions. Each will be given the following index notation in the same order as described below."* and *"a typical variable might be defined as follows $x_{\text{ocsf},t}$ -- with $x$ being specific to scenario, country, sector, fuel type, and time. Particular values for these general indices are indicated with capitals, for example, o=B for baseline."*

Canonical subscript order: `o c u g s f p t` (scenario, country, UNFCCC sector, sector grouping, sector, fuel, pollutant, year), time usually after a comma: `x_{\text{ocsf},t}`.

| Index | Dimension (docs) | Members / values (docs) | Where |
|---|---|---|---|
| `o` | Scenario | `o`=(B) baseline; `o`=(P) policy ("e.g. carbon tax"). Appendix F also numbers scenarios 1–13: 1 Baseline, 2 Carbon tax, 3 ETS, 4 Feebates, 5 Energy efficiency regulations, 6 Coal excise, 7 Road fuel tax, 8 Electricity emissions tax, 9 Power feebate, 10 Electricity excise, 11 Vehicle fuel economy, 12 Residential efficiency regulations, 13 Industrial efficiency regulations | Dimensions table + footnote 7; Appendix F "Scenarios" |
| `c` | Country | ~150 calibrated countries | Dimensions |
| `u` | UNFCCC emissions sector | "energy-related (E), (which includes power, transport, buildings, industry and other energy use), Industrial Processes and Product Use (I), Agriculture (A), Land Use, Land-Use Change and Forestry (L), Waste (W), and Other (O)" | Dimensions footnote 8; used in "Emissions" |
| `g` | Sector grouping | Context-dependent (footnote 9): *energy/emissions aggregation*: buildings (residential, services, food & forestry), industry, transport, power; *prices*: residential, industry including services, transport, power; *elasticities*: residential, industrial, services (incl. food & forestry), transport, power. Appendix F SectorGroupCodes: `ind`, `pow`, `bld`, `tra`, `oth`, `all`, `ele` (eloutput) | Dimensions footnote 9; "Notation" `{#sec-PricesNotation}` ("for prices meaning Residential, Industrial-including-Services, Transport and Power"); Appendix F "Sectors" |
| `s` | Sector (sub-sector) | Appendix F SubSectorCodes: industry: `cem`, `cst`, `foo`, `ftr`, `irn`, `mac`, `mch`, `neu`, `nfm`, `oen`, `omn`, `srv`, `wav`; power: `pow`; buildings: `res`, `foo`, `srv`; transport: `avi`, `nav`, `rod`; other: `oth`. Exec summary says "CPAT brackets the economy into 17 sectors" | Dimensions; Appendix F "Sectors" |
| `f` | Fuel and generation type | Footnote 10: Coal (COA), Natural gas (NGA), Oil (OIL), Nuclear (NUC), Wind (WND), Solar (SOL), Hydro (HYD), Other renewables (REN), Biomass (BIO). Appendix F FuelCodes (lower case): `bio` (expanded: `bgs`, `bdi`, `obf`), `coa`, `die`, `ecy`, `gso`, `hyd`, `jfu`, `ker`, `lpg`, `nga`, `nuc`, `oop`, `ore`, `ren`, `sol`, `wnd`. Electricity as a fuel: `f = P` (power-demand section) | Dimensions footnote 10; "Fuels" `{#sec-ExecSummFuels}`; Appendix B "CPAT fuels"; Appendix F "Fuel types" |
| `p` | Pollutant | GHG: $CO_{2}$, $CH_{4}$, $N_{2}O$, F-gases ("$p = \text{PF}C_{s}$, $\text{HF}C_{s}$, $SF6$, $NF3$"); local pollutant codes (Appendix F): `bc`, `oc`, `tc`, `nox`, `so2`, `voc`, `co`, `ch4`, `nh3` | Dimensions; "Emissions > Overview" ("We use the index $p$ to refer to the type of GHG"); Appendix F "Pollutants" |
| `t` | Year | `t_{0}` = "first year of model calculations, also known as the base year (as of the time of writing, 2019)"; horizon 2019–2035 (exec summary also says 2018–2035) | Dimensions footnote 11 |

Secondary / local indices in `03_Mitigation.qmd`:

| Index / marker | Meaning | Where |
|---|---|---|
| `B`, `P` (as subscripts, e.g. `vc_{B,\text{cft}}`, `F_{P,ft}`) | particular values of `o` (baseline / policy) | Power prices; Welfare `ddw` |
| `E` as sector index (e.g. `F_{\text{cEf},t_{0}}`, `p_{\text{cEt}}`, `u = E`) | electricity sector (footnote 21: "Note that the electricity sector is denoted by E."; Elasticity model: "The index $E$ denotes the sector Electricity.") **and** energy-related UNFCCC sector (`u = E`) | Power data; Elasticity model; Emissions |
| `T` superscript (`sp_{B,\text{cg}}^{T}`, `p_{P,\text{cgt}}^{T}`, `mu^{T}`) | "the index $T$ holds for technoeconomic model" | Concept 4: End-user prices |
| `q` | component of levelized cost ("We separate the components $q$ (capital cost) of the levelized costs") | Concept 2: LCOE |
| `N`, `n`, `r`, `\tau` | years of production (N payments, t = 0..N−1), switch year, discount rate, constant log growth rate of a cost component | LCOE methodology: Simplification |
| `i`, `j` | "bound variables ranging over the same range as $f$ (i.e., OIL, NGA, COA, NUC, WND, SOL, BIO, REN, HYD)" | Elasticity model > Total power supply |
| `i` (in multilogit denominator, `K_{i}`, `H_{i}`) | generation-type alternative in the sum; also subscript `i` = investment in `K_{i}` | Engineer model > Logit function / Investment |
| `lc` (super/subscript: `vc^{\text{lc}}`, `\text{ti}c_{\text{lc}}`) | lowest-cost option between coal and natural gas (dispatch) or across fuel types (investment) | Engineer model notation |
| `oen` (e.g. `F_{oc,oen,ft}`) | Other Energy Use sector grouping | Fiscal revenues |
| `Eind` | "energy-related emissions in the industrial sector" | Emissions > Industrial processes |
| `fl` superscript (`\text{fi}x^{\text{fl}}`) | forward-looking | Concept 2 |
| `av` superscript (`\text{ca}x^{\text{av}}`, `\text{gn}c^{\text{av}}`) | weighted average | Concept 3/4 |
| `DIR`, `IND` superscripts on `tcp` | direct / indirect carbon pricing elements | Appendix C |
| `j` | country (energy-balance identities `\text{TPE}S_{j}`) | Appendix B "CPAT energy sectors" |
| `i`, `t` | country, year in the panel regression `fc_{\text{it}}` | Validation > Panel estimation > Methodology |
| Sub-model codes `t`, `e`, `b`, `a` | Technoeconomic, Elasticity, Both, All | Appendix F "Sub-models" |
| Income groups HIC, UMIC, LMIC, LIC; CPAT regions EAS, ECS, LNC, MENA, NAC, SAS, SSF (+ China, Japan, Korea separately) | used for WACC, data averaging | Concept 2; footnote 22 |

### 1.2 Distribution module indices (`05_Distribution.qmd`)

| Index | Meaning (docs wording) | Members | Where |
|---|---|---|---|
| `j` | household ("household $j$'s annual consumption"); in sec-5_3_1 "individual *j*" | HBS households | "Household budget shares" `{#sec-5_2_1}` |
| `g` | expenditure category ("category $g$ item"); in tax-incidence text also "sector *g*" of consumption items | direct fuel/energy categories: electricity, natural gas, gasoline, diesel, coal, oil/lubricants, LPG, kerosene, charcoal, ethanol, firewood (tbl-5_2 codes `ely`, `nga`, `gso`, `die`, `coa`, `oil`, `lpg`, `ker`, `ccl`, `fwd`, `ethanol`); 14 indirect categories: appliances, chemicals, clothing, communications, education, food, health services, housing, paper, pharmaceuticals and medicine, recreation and tourism, transportation equipment, public transportation, other (tbl-5_4 maps GTAP-10 sectors to these); GTAP-10 has 65 sectors | `{#sec-5_2_1}`, `{#sec-5_3_1}` |
| `f` | fuel ("fuel *f* of consumption items from each sector *g (note that f* ∈ *g*)") | CPAT fossil fuels (tbl-5_1): Coal (coa), Electricity (ely), Natural gas (nga), Other oil products (oop), Gasoline (gso), Diesel (die), LPG (lpg), Kerosene (ker); mapped to GTAP `coa`, `ely`, `gas/gdt`, `oil`, `p_c` | `{#sec-5_3_1}`, `{#tbl-5_1}` |
| `d` | consumption decile ("household in decile $d$") | 1..10; percentiles p25/p75 for horizontal distribution | `{#sec-5_2_1}`, `{#sec-5_4_1}` |
| `i` | infrastructure category ("access to infrastructure category *i*") | water, electricity, sanitation, ICT, public transportation | `{#sec-5_2_2}` |
| `y` | year of interest ("for year y"; "(2022 $\leq$ y $\leq$ 2030)") | — | `{#sec-5_3_2_1}` |
| `t` | time, only in eq-5_7 (`p_{t}/p_{t - 1}`) | — | `{#sec-5_3_2_2}` |
| `c` | country (PIT section `l_{\text{dcy}}`; also `\theta_{c}`) | — | `{#sec-5_4_3_1}` |
| `a` | social protection scheme ("protection scheme *a*") | ASPIRE schemes | `{#sec-5_4_2}` |
| `T` (sub/superscript on pop, C) | targeted population | — | `{#sec-5_4_1}` |
| `D`, `M` subscripts (`P_{D}`, `P_{M}`) | Distribution Module, Mitigation Module | — | `{#sec-5_3_2_1}` |
| `TE`, `PE`, `PC` suffixes on `g_{dcy\_ ...}` | Targeted Exemption, Personal Allowance (written PE), Proportional Compensation | — | `{#sec-5_4_3_2}` |
| Samples | overall (national), urban, rural; statistics mean, median, p25, p75 | — | `{#sec-5_2_1}` |

### 1.3 Multipliers (`04_Multipliers.qmd`, "Methodology for estimating dynamic multipliers using panel data")

| Index | Meaning | Members |
|---|---|---|
| `i` | country (panel unit) | 75 countries with >10 obs |
| `t` | year | — |
| `h` | horizon, "$h = 0,1,\ldots,H - 1$" | tables label horizons H1..H11 ("from the year of the policy change until 10 years after") |
| instrument | fiscal instrument | EET (energy excise), PIT, VAT, GIS (public investment), GCS (public consumption), TRS (transfers); estimation also uses EGT (energy taxes), EVT (total environmental taxes), EXT (excise taxes) |
| subsample | pooled panel; income levels (HIC & UMIC, LIC & LMIC); regions; debt levels; trade openness | — |

### 1.4 Air pollution (`06_Air_pollution.qmd`) – indices are local to each subsection

| Index | Meaning (docs) | Where |
|---|---|---|
| `x`, `y` | source region, receptor point | Option 1: TM5-FASST `{#sec-tmfasst}` |
| `j` | component (PM2.5 and O3) in eq-sourcerecep / eq-deltae; but emissions pollutant in eq-modeled; pollutant (SO2, PM1, ...) in eq-ifeach; age in market output losses | various |
| `i` | precursor of `j` (BC, POM, SO2, NOx, OPM for PM2.5; NOx, NMVOC, SO2, CH4 for O3) in FASST; PM2.5/O3 in eq-modeled; distance band (1–4) in eq-ifeach; "state" in eq-wij; risk factor in eq-pafsum | various |
| `k` | documented as "pollutant" but used as summation index over source regions `x_{k}` in eq-deltae | `{#sec-tmfasst}` |
| `s` | sector (AP sectors: Coal/Gas/Other power plants `pow`, Road transport `rod`, Residential/services/construction `res`,`cst`,`srv`, Industries and other energy `mnf` (`irn`,`nfm`,`mac`,`cem`,`ftr`), `mch`, `omn`, `oen`, `ral`, `avi`, Food & forestry `foo`); elastic net: `s \in \{ agr, roa, pow, inx, otr, oth, ser\}`; sex in DALY equations | tbl-aggsec; Option 3; Health outcomes |
| `p` | pollutant `p \in \{BC, OC, NH_3, NO_x, NMVOC, SO_2\}`; power plant in eq-ifeach; period (year) in eq-wpshare | Option 3; Option 4; Market output losses |
| `m` | month 1..12 | Option 3 |
| `t`, `t_0`/`to` | year, baseline year 2019 | Options 2, 5 |
| `l` | location: inside country / outside country | Option 4 |
| `c`, `s`, `a`, `t` | cause, sex, age, year (DALY/YLL/YLD); `c` = country in VSL and BoD equations; `c` = disease in eq-msum | Health outcomes; VSL; Health expenditure |
| `d` | disease | Health expenditure |
| superscripts `0`, `1` | baseline, carbon-price (policy) scenario (`\text{RR}_{\text{HAP}}^{0}`, `p_{H}^{1}`) | Quantification of health effects `{#sec-quanthealtheff}` |
| `OAP`, `HAP`, `PM`, `O3` | ambient (outdoor), household air pollution, PM2.5 total, ozone | Joint ambient and household air pollution |
| Age groups | neonates, post neonates, under 15, 15 to 64, 65+ (5-year buckets for IHD/stroke RR) | Joint ambient and household |

### 1.5 Road transport (`07_Road_Transport.qmd`, "Methods for elasticity estimation")

| Index | Meaning |
|---|---|
| `c` | country ("in country $c$") |
| `t` | year |
| `k` (superscript of `v_{\text{ct}}^{k}`) | k-th additional variable influencing the elasticity (five used in practice) |
| superscripts `baseline`, `policy`, `simple` | scenario / naive forecast (`Y_{t}^{\text{baseline}}`) |
| outcomes `Y` | VKT, congestion (TomTom index), road accident fatalities, road damage (maintenance cost) |

## 2. Symbol tables per module

Units are as printed in the docs' notation tables ("units are reported as input into CPAT, but further conversions are made"). Blank unit = none given. Symbols not in a notation table but used in equations are marked *(eq only)*.

### 2.1 Mitigation – Fuel prices, taxes and subsidies (`03_Mitigation.qmd` "Fuel prices, taxes, and subsidies" > "Notation" `{#sec-PricesNotation}`; Appendix C `{#sec-Appendix_C_Prices}`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `p` | Retail price | US\$/Gj | Prices > Notation |
| `P` | Aggregate retail price | US\$/Gj | Prices > Notation; Price aggregation |
| `sp` | Supply price ("price before net taxes") | US\$/Gj | Prices > Notation |
| `fixsp` | Fixed portion of supply price | US\$/Gj | Prices > Notation |
| `fltsp` | Floating portion of supply price | US\$/Gj | Prices > Notation |
| `ps` | Producer-side subsidy ("outstanding producer-side subsidy") | US\$/Gj | Prices > Notation |
| `vat` | Value added tax (VAT payment per energy unit) | US\$/Gj | Prices > Notation |
| `vatrate` | VAT rate (text also writes `VATrate`) *(eq only)* |  | Appendix C > Price components |
| `\overline{vatrate}` | general (economy) VAT rate in TCP formula *(eq only)* |  | Appendix C > Forecasted prices |
| `txo` | Excise and all other taxes (net of consumer subsidies) | US\$/Gj | Prices > Notation |
| `ttx` | total net taxes ("or net subsidy if negative") *(eq only)* |  | Appendix C > Price components |
| `fixtax` | Fixed portion of taxes | US\$/Gj | Prices > Notation |
| `fixsub` | Fixed portion of subsidies | US\$/Gj | Prices > Notation |
| `flts` | Floating portion of taxes and subsidies | US\$/Gj | Prices > Notation |
| `flts^{+}_{cgf,t}` | positive components of the floating taxes or subsidies *(eq only)* |  | Appendix C |
| `gp` | Global fuel price | US\$/bbl for oil, \$/ton for coal and \$/MMBtu for natural gas | Prices > Notation |
| `\phi_{\text{PS}}` | Phase-out factor for producer-side subsidies (eq: `\phi_{\text{PS}, t}`) |  | Prices > Notation |
| `\phi_{\text{CS}}` | Phase-out factor for consumer-side subsidies |  | Prices > Notation |
| `\phi_{\text{PC}}` | Phase-out factor for price controls (eq: `\phi_{\text{PC}_t}`) |  | Prices > Notation |
| `pcc` | Price control coefficient |  | Prices > Notation |
| `\Delta gp` | Difference between current and previous global prices |  | Prices > Notation |
| `\delta_{\text{CT} / \text{ETS}}` | Fix growth rate for existing carbon tax or existing ETS permit price (eqs use `\delta_{\text{CT}}`, `\delta_{\text{ETS}}`, `\delta_{CT}`, `\delta_{ETS}`) |  | Prices > Notation |
| `xct` | Existing carbon taxes (per energy unit) | US\$/Gj | Prices > Notation |
| `xetsp` | Existing ETS permit prices (per energy unit) | US\$/Gj | Prices > Notation |
| `xcp` | Existing carbon price | US\$/Gj | Prices > Notation |
| `XCT_{c,t_0}` | existing national carbon tax per ton in base year *(eq only)* |  | Appendix C |
| `XETSP_{c,t}` | existing ETS permit price per ton CO2 ("adjusted values after the penalization") *(text only)* |  | Forecasted years |
| `\varphi_{XCT,cgf,t_0}` | coverage of existing carbon tax *(eq only)* |  | Appendix C |
| `\varphi_{XETS,cgf,t_0}` | coverage of existing ETS *(eq only)* |  | Appendix C |
| `nct` | New carbon tax (per energy unit) | US\$/Gj | Prices > Notation |
| `netsp` | New ETS price (per energy unit) | US\$/Gj | Prices > Notation |
| `ncp` | New carbon price | US\$/Gj (Fiscal-revenue table says US\$/ton of CO2) | Prices > Notation |
| `nexc` | New excise tax (if applicable) | US\$/Gj | Prices > Notation |
| `NCT` | National price per ton of $CO2$ under a carbon tax | US\$/ton of CO2 | Prices > Notation |
| `NETSP` | National price per ton of $CO2$ under an ETS | US\$/ton of CO2 | Prices > Notation |
| `ef` | Emission factors | $\text{tC}O_{2}e$/ktoe | Prices > Notation |
| `\varphi_{\text{NCT} / \text{ETS}}` | Sector-fuel coverage for the new policies (Carbon tax or ETS); eqs use `\varphi_{\text{NCT},cgft}`, `\varphi_{\text{NETS},cgft}` | \% | Prices > Notation |
| `F` | Use of fuel | ktoe | Prices > Notation |
| `n_{t_0}` | number of historical years (2018–2022) in averages *(eq only)* |  | Appendix C |
| `tcp^{DIR}_{cgf,t}` | Direct carbon pricing elements (memo account) *(eq only)* | constant USD per volume or energy unit | Appendix C |
| `tcp^{IND}_{cgf,t}` | Indirect carbon pricing elements (memo account) *(eq only)* | constant USD per volume or energy unit | Appendix C |
| `\theta^{PS}_{TCP}` | "boolean variable to control the inclusion of producer subsidies" in TCP *(eq only)* |  | Appendix C |
| `tcp_{cgf,t}` | total carbon price per energy unit *(eq only)* |  | Appendix C |
| `TCP_{cgf,t}` | sector-fuel total carbon price; aggregated `TCP_{cf, t}`, `TCP_{c,t}` *(eq only)* | constant USD/tCO2 | Appendix C |

### 2.2 Mitigation – Fuel consumption (`03_Mitigation.qmd` "Fuel Consumption" > "Notation" `{#sec-3_3_2}`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `F` | Use of fuel | ktoe | Fuel Consumption > Notation |
| `Y` | Total real GDP ("total real GDP, not per capita GDP") | US\$ | Fuel Consumption > Notation |
| `p` | Retail price | US\$/Gj | Fuel Consumption > Notation |
| `\alpha` | Autonomous annual energy efficiency improvement (eq: `\alpha_{\text{sf}}`; "set to 0.5% or 1%, depending on the sector") | \% | Fuel Consumption > Notation |
| `\Psi` | Covid adjustment factor to energy demand (eq: `\Psi_{\text{ct}}`) | \% | Fuel Consumption > Notation |
| `\epsilon_{Y}` | Forward-looking real GDP-elasticity of fuel demand (eq: `\epsilon_{Y,\text{csf}}`) | \% | Fuel Consumption > Notation |
| `\epsilon_{U}` | Elasticity of usage of energy products and services ("intensive margin"; negative) | \% | Fuel Consumption > Notation |
| `\epsilon_{F}` | Efficiency price elasticity ("efficiency and extensive margin") | \% | Fuel Consumption > Notation |
| `\epsilon_{\text{bio},f}` | Substitution elasticity between the most cooking fuel used and biomass (= 0.25) | US\$/Gj (sic) | Fuel Consumption > Notation |
| `\text{Ef}f_{f}` | Natural gas, LPG and kerosene efficiency (0.58, 0.56, 0.45) | \% | Fuel Consumption > Notation |
| `\text{Ef}f_{\text{bio}}` | Biomass efficiency (0.20) | \% | Fuel Consumption > Notation |
| `\epsilon_{G,\text{csf}}` | GDP elasticity in the power-demand equations; never defined (presumably = `\epsilon_{Y}`) *(eq only)* |  | Engineer model > Power demand; Elasticity model > Total power demand |
| `P_{t}` | price in the rebound-effect exponent term (capital P; presumably `p`) *(eq only)* |  | Income and Price Elasticities > Rebound effect |

### 2.3 Mitigation – Power prices and generation costs (`03_Mitigation.qmd` "Power prices and generation costs" > "Notation" `{#sec-Notation}`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `g` | Electricity generation | GWh | Power prices > Notation (table 1) |
| `\nu` | Thermal efficiency (eq: `\nu_{\text{cf}}`) | \% | Power prices > Notation |
| `\text{cf}` | Capacity factor (eq: `cf_{\text{cf}}`) | \% | Power prices > Notation |
| `\text{cap}` | Capacity | MWy | Power prices > Notation |
| `\text{PV}` | Present value of costs (eq: `PV_{q}`) |  | Power prices > Notation |
| `\text{tic}` | Levelized total investment costs | US\$/kWh | Power prices > Notation |
| `\text{wacc}` | Weighted Average Cost of Capital (default HIC 0.075, UMIC 0.100, LMIC 0.125, LIC 0.150) | \% | Power prices > Notation |
| `\text{lif}` | Lifetime | Years | Power prices > Notation |
| `\text{dlf}` | Discounted lifetime | Years | Power prices > Notation |
| `\Phi_{\text{inv}}` | New investment expressed as a proportion of total existing capacity less retirements | \% | Power prices > Notation |
| `\text{gns}` | Generation shares | \% | Power prices > Notation |
| `\text{fc}` | Projected unit fuel costs ("before the introduction of the carbon pricing policy") | US\$/kWh | Power prices > Notation (table 2) |
| `\text{opv}` | Variable costs for operating and maintenance (OpEx) — equations write `\text{vo}p` | US\$/kWh | Power prices > Notation |
| `\text{vc}` | Current variable costs | US\$/kWh | Power prices > Notation |
| `\text{cax}` | Capital cost (CapEx) | US\$/kW | Power prices > Notation |
| `\text{opf}` | Fixed costs for operating and maintenance (OpEx) | US\$/kW (text: "expressed in USD per kWh") | Power prices > Notation |
| `\text{tfc}` | Fixed OpEx | US\$/kWy | Power prices > Notation |
| `\text{sto}` | Storage cost | US\$/kWh | Power prices > Notation |
| `\text{dtc}` | Decommissioning costs | US\$/kWh (text: "in USD per kW") | Power prices > Notation |
| `\text{ipc}` | Implicit price component for coal (eq writes `ip_{\text{cft}}`; calibration text `\text{im}p_{c,\text{coa},t}`) | US\$/kWh | Power prices > Notation |
| `\text{pusRen}` | Per-unit renewable subsidies | US\$/kWh | Power prices > Notation |
| `\text{LCOE}` | Levelized cost of electricity (eq: `\text{LCO}E_{q}`, `\text{LCO}E_{P,\text{cft}}`) | US\$/kWh | Power prices > Notation |
| `\text{hrp}` | Historical retail prices in the electricity sector | US\$/Gj | Power prices > Notation (table 3) |
| `\text{gnc}` | Current generation cost | US\$/kWh | Power prices > Notation |
| `\text{fix}` | Amortized fixed costs | US\$/kWh | Power prices > Notation |
| `\text{ca}x^{\text{av}}` | Weighted average CapEx | US\$/kW | Power prices > Notation |
| `\text{acc}` | Yearly amortization of capital costs | US\$/kWh | Power prices > Notation |
| `\text{int}` | Interest costs | US\$/kWh | Power prices > Notation |
| `\text{dec}` | Yearly amortization of decommissioning costs | US\$/kWh | Power prices > Notation |
| `sp_{T}` | Supply power price determined in the engineer model (equations: `sp_{B,\text{cg}}^{T}`) | US\$/kWh | Power prices > Notation |
| `\text{tmc}` | Transmission cost (allowance \$15/MWh industrial, \$40/MWh residential) | US\$/kWh | Power prices > Notation |
| `mu^{T}` | Markup used in the calculation of supply power prices (eq: `mu_{B,\text{cgt}}^{T}`) | US\$/kWh | Power prices > Notation |
| `\text{pex}` | Power excise | US\$/kWh | Power prices > Notation |
| `\text{reb}` | Rebate | US\$/kWh | Power prices > Notation |
| `p^{T}` | End-user power price (engineer model) (eq: `p_{P,\text{cgt}}^{T}`) | US\$/kWh | Power prices > Notation |
| `\text{df}c_{\text{cft}}` | discount factor "$1 + \text{wac}c_{\text{cft}}^{t - t_{0}}$" *(eq only)* |  | Concept 2 |
| `\text{fi}x^{\text{fl}}` | forward-looking levelized fixed costs *(eq only)* |  | Concept 2 |
| `C_{q,t}` | the $q$ component of costs at time $t$ *(eq only)* |  | Concept 2 |
| `\text{dem}` | discounted power produced *(eq only)* |  | Concept 2 |
| `\tau` | consistent real (logarithmic) growth rate of a cost component *(eq only)* |  | LCOE methodology: Simplification |
| `\text{gn}c_{B,\text{ct}}^{\text{av}}` | weighted current generation cost *(eq only)* |  | Concept 4 |

### 2.4 Mitigation – Techno-economic ('engineer') power model (`03_Mitigation.qmd` `{#sec-EngineerModel}` > "Notation")

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `E` | Total quantity of power demanded by sector (eq: `E_{\text{ocsf},t}`; text: "$E$ is expressed in ktoe") | GWh | Engineer model > Notation |
| `\text{net}` | Net exports (imports) | ktoe | Engineer model > Notation |
| `\text{eiu}` | Energy industry's own use | ktoe | Engineer model > Notation |
| `\Delta^{\text{dif}}` | Transmission and statistical differences | ktoe | Engineer model > Notation |
| `x` | "used in the logit formula to alternatively represent investment, $x = \text{inv}$, or generation $x = \text{gen}$" | GWh | Engineer model > Notation |
| `K` | "Parameter adjusting the shape of the sigmoidal function. It determines the speed of transitioning between generation types with a different cost." Default 2; `K_{\text{dispatch}}`, `K_{i}` (investment), text also `K_{g}` |  | Engineer model > Notation |
| `\text{reqge}n_{\text{COA} + \text{GAS}}` | Remaining generation allocated to coal and gas after nuclear, renewables, biomass and oil generation are subtracted | GWh | Engineer model > Notation |
| `\text{minge}n_{\text{COA},\text{GAS}}` | Minimum coal/gas needed assuming gas runs at maximum capacity | GWh | Engineer model > Notation |
| `\text{residualreqge}n_{COA/GAS}` | residual power generation from coal and gas | GWh | Engineer model > Notation |
| `\text{maxC}f_{\text{GAS},\text{COA}}` | Maximum capacity for coal/gas (default 90%) | GWh | Engineer model > Notation |
| `\lambda_{f}` | Proportion of the residual generation (after the 'minimum coal' and minimum gas' allocation given limited capacity of the other) allocated to each of coal and gas | GWh (sic) | Engineer model > Notation |
| `H_{f}` | ratio of variable cost to lowest variable cost, $\frac{vc_{P,\text{cft}}}{vc_{P,\text{cft}}^{\text{lc}}}$ (text also writes `H_{g}`) *(eq only)* |  | Dispatch decision |
| `vc_{\text{lc}}` | Lowest current variable costs between coal and natural gas (eq: `vc_{P,\text{cft}}^{\text{lc}}`) | US\$/kWh | Engineer model > Notation |
| `\widetilde{\gamma}` | Generation shares before PPAs (eq: `{\widetilde{\gamma}}_{\text{ocf},t}`) | \% | Engineer model > Notation |
| `\gamma` | Generation shares after PPAs | \% | Engineer model > Notation |
| `\omega` | Percentage of PPAs | \% | Engineer model > Notation |
| `\Omega` | Downscaling factor if needed generation is different from that which is determined by the raw capacity factors | \% | Engineer model > Notation |
| `\text{inv}` | Generation investments | MWh | Engineer model > Notation |
| `\text{ret}` | Generation retirements | MWh | Engineer model > Notation |
| `\text{re}p_{\text{COA}}` | Proportion of coal replacement (cost-based early retirement; max 80%) | \% | Engineer model > Notation |
| `H_{r,\text{COA}}` | ratio $\frac{vc_{\text{oc},\text{coa},t}}{vc_{\text{ocft}}^{\text{lc}}}$, f ∈ {coal, solar, wind} *(eq only)* |  | Retirement and capacity needed |
| `\zeta` | New investments permitted (eq: `\zeta_{\text{cft}}`, "in percentage") | MWh | Engineer model > Notation |
| `\text{ivp}` | Proportion of new investments | \% | Engineer model > Notation |
| `H_{i}` | ratio $\frac{\text{ti}c_{P,\text{cft}}}{\text{ti}c_{P,\text{cft}}^{\text{lc}}}$ *(eq only)* |  | Investment decision |
| `\text{ti}c_{\text{lc}}` | Lowest levelized total investment costs between coal and natural gas | US\$/kWh | Engineer model > Notation |
| `\text{iv}^{\max}` | Maximum effective investments *(eq only)* |  | Investment decision |
| `iv^{\text{new}}` | whether new investments are permitted / new effective investment *(eq only)* |  | Investment decision |
| `iv^{\text{rem}}` | remaining investments needed *(eq only)* |  | Investment decision |
| `iv^{\text{tot}}` | total new investments *(eq only)* |  | Investment decision |
| `VRE_{\text{cft}}` | non-VRE and VRE limits (defaults 5% coal/gas; 2% hydro, oil, other ren., nuclear, biomass; 2% wind and solar) *(eq only)* |  | Investment decision |
| `v` | Variable renewable energy (VRE) share ("VRE, $v$, includes solar and wind but not hydro") | \% | Engineer model > Notation |
| `\text{sst}` | Short-term storage ("kWh of storage per kW of average generation") | Hours | Engineer model > Notation |
| `\text{slt}` | Long-term storage | MW/MW, i.e. dimensionless units (%) | Engineer model > Notation |
| `\text{im}p_{c,\text{coa},t}` | additional implicit price for coal (systems cost from coal-share calibration) *(text only)* |  | Calibration and systems costs |
| `\text{co}a_{t}^{\text{est}}` | coal share estimated by the power model (text also `\text{coa}l_{t}^{\text{est}}`); observed `\text{co}a_{t}^{\text{obs}}` *(text only)* |  | Calibration and systems costs |

### 2.5 Mitigation – Elasticity power model (`03_Mitigation.qmd` `{#sec-ElasticityModel}` > "Notation"; Appendix C "Power generation costs")

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `\Phi` | Production share (eq: `\Phi_{\text{ocft}}`) | \% | Elasticity model > Notation |
| `\text{gn}c^{*}` | Total unit cost adjusted of thermal efficiency | US\$/kWh | Elasticity model > Notation |
| `\epsilon_{\widetilde{E}}` | Conditional own-price elasticity of generation from fuel $f$ with respect to generation cost ("$\epsilon_{\widetilde{E}} < 0$") | \% | Elasticity model > Notation |
| `\delta^{\text{add}}` | Additional share of electricity generation attributed to non-nuclear and non-hydro energy (eq: `\delta_{\text{oct}}^{\text{add}}`) | \% | Elasticity model > Notation |
| `\text{TotExcess}` | Total surplus of nuclear and hydro power generation to be redistributed | \% | Elasticity model > Notation |
| `\iota_{\text{cft}}` | $\frac{\text{gn}c_{\text{ocft}}^{*}}{\text{gn}c_{\text{ocf},t - 1}^{*}}$ *(eq only)* |  | Total power supply |
| `\alpha_{f}` | efficiency improvement over time specific to generation type $f$ ("annual generation productivity improvements": coal 0.5%, gas 1%, oil 0.5%, nuclear 1%, wind/solar/other ren. 5%, hydro 1%, biomass 1%) *(eq only)* |  | Total power demand / supply |
| `gnc_{ocft}` | "total unit costs of generation" in the 'old' IMF cost model |  | Appendix C > Power generation costs |
| `efc_{ocft}` | effective fuel unit costs (after autonomous efficiency gains) |  | Appendix C |
| `nfc_{ocft}` | effective non-fuel unit costs |  | Appendix C |
| `rps_{o,cgft}` | renewable producer subsidies (wind, solar, hydro, other renewables) |  | Appendix C |
| `tex_{P,tcft}` | undefined in text (presumably tax exemption share) |  | Appendix C |
| `\gamma` | "fixed proportion through the period of costs that are non-fuel" (old cost model) |  | Appendix C |

Power data (`{#sec-PowerDataSources}`, `{#sec-PowerCharacteristics}`):

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `\varphi = \frac{W}{Q_{I}}` | thermal efficiency as work output over heat input (text only; differs from `\nu`) |  | Description and definition of the variables |
| `n_{\text{cons}}` | construction time | years | Consistency across data sources |
| `\text{Cos}t_{t}` | unit cost of the technology in year $t$ |  | Estimation of the power sector characteristics |
| `\text{Ca}p_{t}` | cumulative installed capacity |  | idem |
| `\varepsilon` | experience parameter (learning curve); learning-rate values: solar 0.276/0.319/0.362, wind 0.153/0.194/0.235 |  | idem |
| `\text{LR}` | learning rate |  | idem |

### 2.6 Mitigation – Emissions (`03_Mitigation.qmd` "Emissions" > "Notation")

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `\text{em}` | Emissions (eq: `em_{\text{ocupt}}`, "under scenario $o$, country $c$, UNFCC sector $u$, and for pollutant $p$ and at year $t$") | $\text{tC}O_{2}$/GJ (sic; text: mtCO2e) | Emissions > Notation |
| `\text{Δe}m_{\text{LUCF},t}` | LULUCF emissions decline (default 2.5%; eq `\text{Δe}m_{L,t}`) | \% per annual in absolute value of start year | Emissions > Notation |
| `\text{ef}` | Emission factors (eq: `ef_{\text{cEsfp}}`) | $\text{tC}O_{2}$/ktoe | Emissions > Notation |
| `\text{fug}` | Methane fugitive and venting emissions (listed, not used in any equation) | $\text{tC}O_{2}$/ktoe | Emissions > Notation |
| `\text{gwp}` | Global warming potential from methane emissions (not used in any equation) | $\text{tC}O_{2}$/ktoe | Emissions > Notation |
| `red` | Percentage of reduction of methane emission factor, due do abatement | \% | Emissions > Notation |
| `mf` | Methane fee | \$/$tCH_{4}$ | Emissions > Notation |
| `Y_{\text{grow}}` | GDP growth (eq writes `Y_{\text{growth}}`) | \% | Emissions > Notation |
| `lp_{\text{grow}}` | Population growth | \% | Emissions > Notation |
| `\text{ame}` | Additional (e.g. non-pricing) mitigation effort; "$a\text{me}_{cLp,t} = \ \frac{em_{P,cLt}}{em_{B,cLt}}$" | \% | Emissions > Notation |
| `\epsilon_{\text{lp}}` | Population elasticity | \% | Emissions > Notation |
| `prod_{oc,oil/nga/coa,t}` | production of crude oil or natural gas or coal *(eq only)* | ktoe | Methane |
| `A * mf_{t}^{B}` | abatement curve; "A and B are the inputs for the abatment curve" *(eq only)* |  | Methane |

### 2.7 Mitigation – Fiscal revenues and welfare (`03_Mitigation.qmd` "Fiscal revenues" > "Notation"; "Monetized social costs and benefits")

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `rev` | Fiscal revenues | Real 2021 US\$bn | Fiscal revenues > Notation |
| `\varphi` | Sector-fuel coverage | \% | Fiscal revenues > Notation |
| `revExi` | Revenues from existing excises and other taxes (text also `revEx_{ft}`) | Real 2021 US\$bn | Fiscal revenues > Notation |
| `cs` | Consumer-side subsidy | US\$/Gj | Fiscal revenues > Notation |
| `fao` | Fixed/ad val part/other | US\$/Gj | Fiscal revenues > Notation |
| `revVAT` | Revenues from VAT | Real 2021 US\$bn | Fiscal revenues > Notation |
| `cstPs` | Losses from producer-side subsidies | Real 2021 US\$bn | Fiscal revenues > Notation |
| `subDem` | Subsidized demand | Billion liters for oil, GJ for coal and natural gas and GWh for electricity | Fiscal revenues > Notation |
| `pusF` | Per-unit fossil fuels subsidies | US\$/liters for oil, US\$/GJ for coal and natural gas and US\$/GWh for electricity | Fiscal revenues > Notation |
| `cstRen` | Cost of renewable subsidies | Real 2021 US\$bn | Fiscal revenues > Notation |
| `ct_{ocft}` | Revenues/losses from price controls (eq writes `ctr_{ocft}`) *(text)* |  | Additional information |
| `pInt_{ocft}` | international price *(eq only)* |  | Revenues/losses from price controls |
| `pth_{ocft}` | pass-through of global energy price changes ("portion ... not passed-through" is `pth − 1`) *(eq only)* |  | Revenues/losses from price controls |
| `ddw` | efficiency (deadweight) costs (Harberger) |  | Efficiency costs in CPAT |

Social cost of carbon (Appendix E): NSCC discount rate `ρ` (2%/1%) and NSCC elasticity of marginal utility `μ` (1.5%/0.7%) appear only as plain-text Greek in the settings table; SCC target \$75 by 2030, 4%/yr real rise.

Validation regression ("Panel estimation of energy demand" > "Methodology"): `fc_{\text{it}}` fuel consumption, `y_{\text{it}}` GDP, `p_{\text{it}}` price, `\alpha_{i}` individual effects, `\beta_{1}`..`\beta_{3}`, `\epsilon_{\text{it}}`, time effect `\lambda_{t}`.

### 2.8 Multipliers / GDP (`04_Multipliers.qmd`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `h = 0,1,\ldots,H - 1` | horizon |  | Methodology for estimating dynamic multipliers using panel data |
| `y_{i,t}` | dependent variable: "100 times the log of real per-capita GDP in percent" |  | Methodology for estimating dynamic multipliers using panel data |
| `\alpha_{i,h}` | country fixed effects |  | Methodology for estimating dynamic multipliers using panel data |
| `\delta_{t,h}` | time fixed effects |  | Methodology for estimating dynamic multipliers using panel data |
| `s_{i,t}` | identified shock variable: "the cyclically adjusted tax revenue-GDP ratio in percent" |  | Methodology for estimating dynamic multipliers using panel data |
| `\beta_{h}` | cumulative multiplier ("by how many percent(age-points) output (employment) increases in $t + h$ relative to $t - 1$ if discrete policy increases tax revenues by 1% of GDP") |  | Methodology for estimating dynamic multipliers using panel data |
| `x_{i,t}` | vector of control variables |  | Methodology for estimating dynamic multipliers using panel data |
| `\gamma_{h}` | coefficients on controls (not described) |  | Methodology for estimating dynamic multipliers using panel data |
| `\epsilon_{t,i,h}` | error term (text writes `\varepsilon_{t,i,h}`) |  | Methodology for estimating dynamic multipliers using panel data |
| `\frac{T}{Y}` | tax revenue-GDP ratio |  | Cyclical adjustment of tax revenues and public spending |
| `Y^{*}` | trend GDP obtained from the HP filter of log GDP |  | Cyclical adjustment |
| `\eta_{\text{YT}}` | output gap elasticity of the tax revenues |  | Cyclical adjustment |

Note: the Multipliers chapter defines **no symbol** for the multiplier as used inside CPAT, nor any equation mapping recycled revenue (\% of GDP) × multiplier → change in real GDP `Y`. The only statements are prose: "Multipliers indicate by how many % GDP responds on impact and in every subsequent year up to a horizon of 10 years to an increase of a fiscal policy instrument by 1% of GDP" (Introduction) and "in this section tax multipliers are *not* taken as the negative" (Estimation results). Weights for combining pooled and subsample estimates are given only as tables (`Computation of country specific dynamic multipliers`); "the energy excise tax multipliers are approximated by the means of the EGT and EVT multipliers". Mitigation Appendix E: "Include endogenous GDP effects? Yes\*/No – Use fiscal multipliers to model effects on GDP, which increases projected energy demand ('rebound effect')"; multiplier sources Income-grp\*/Estimated/Manual (+ global); adjustment Base\*/High/Low = ±1 SD.

### 2.9 Distribution (`05_Distribution.qmd`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `\pi^{\text{dg}}` | "the budget share of expenditures on a given, category $g$ item by a household in decile $d$" |  | `{#sec-5_2_1}` |
| `\pi_{j}^{g}` | household budget share of household $j$ on category $g$ |  | `{#sec-5_2_1}` |
| `C_{j}^{g}` | "household $j$'s annual consumption on expenditure category $g$" (also written `C_{\text{gj}}`) | LCU | `{#sec-5_2_1}` |
| `C_{j}` | total household consumption (for budget shares: excl. imputed rent) | LCU | `{#sec-5_2_1}` |
| `popw` | per-capita population weight (= hhsize\*popw_hh) |  | `{#sec-5_2_1}`, tbl-5_2 |
| `cons\_ pc` | household per-capita consumption (`cons\_ pc = tot\_cons/hhsize`) | LCU | `{#sec-5_2_1}` |
| `\digamma^{\text{di}}` | "the weighted share of households (in percent) within decile d which have access to infrastructure category *i*" | \% | `{#sec-5_2_2}` |
| `\digamma_{j}^{i}` | binary access indicator for household j, category i | 0/1 | `{#sec-5_2_2}` |
| `p_{j}` | proportion of additional expenditures of individual j (text calls it *P*) | share of consumption | `{#sec-5_3_1}` |
| `p_{\text{fgj}}` | fuel-f, sector-g component of `p_{j}` |  | `{#sec-5_3_1}` |
| `\overline{e_{\text{fg}}}` | average energy intensities (USD/USD) of fuel *f* of consumption items from each sector *g* | USD/USD | `{#sec-5_3_1}` |
| `t_{\text{fg}}` | "the tax rate *t for fuel f in sector g, expressed as the price increase post- (p2) relative to pre-reform (p1)*"; from Mitigation, by country, year and fuel-sector pair (power, industry, residential) | USD<sub>p2</sub>/USD<sub>p1</sub> | `{#sec-5_3_1}` |
| `e_{f}` | fuels' carbon intensities, measured by emissions factors |  | `{#sec-5_3_1}` |
| `e_{g}` | household (sectoral) energy intensities, entries of the Leontief vector (also written `\overline{e_{g}}`) |  | `{#sec-5_3_1}` |
| `\left( I - A \right)^{- 1}` | Leontief inverse; $I$ identity, $A$ technical coefficients (GTAP-10) |  | `{#sec-5_3_1}` |
| `P_{M}^{y}` | economy-wide tax burden / total tax revenues estimated in the Mitigation Module for year y |  | `{#sec-5_3_2_1}` |
| `P_{D}^{y}` | same, in the Distribution Module, scaled to national accounts |  | `{#sec-5_3_2_1}` |
| `\theta_{c}` | final consumption expenditure to GDP ratio (WDI NE.CON.PRVT.ZS) |  | `{#sec-5_3_2_1}` |
| `p_{\text{Adj}}` | downward adjustment factor to the tax incidence on consumers |  | `{#sec-5_3_2_1}` |
| `{\epsilon_{\text{use}}}^{g}` | country-decile-specific price elasticity of demand for consumption category g (eq writes `\epsilon_{\text{use}}`) |  | `{#sec-5_3_2_2}` |
| `\gamma_{g}` | pass-through coefficients ($\gamma_{g} \leq 1$; 0.7–0.9, avg 0.8; 14 transport and industrial sectors) |  | `{#sec-5_3_2_3}` |
| `{t}_{\text{fg}}^{*}` | downward-adjusted energy price change |  | `{#sec-5_3_2_3}` |
| `T^{y}` | per capita transfer for the targeted population | LCU | `{#sec-5_4_1}` |
| `\text{pop}_{T}^{y}` | targeted population in year y (eq-5_10 writes `\text{pop}^T_y`) |  | `{#sec-5_4_1}` |
| `\theta_{\text{pop}}^{y}` | survey-to-national population scaling factor |  | `{#sec-5_4_1}` |
| `T_{d}^{y}` | average per capita transfer for decile d (eq writes `T_{d\ }^{y}`) |  | `{#sec-5_4_1}` |
| `p(T)` | targeted consumption percentile threshold (`C_{jT} \leq p(T) C_j`) |  | `{#sec-5_4_1}` |
| `{\mathrm{\Delta}A}_{a}^{y}` | proportion by which protection scheme *a* can be scaled up |  | `{#sec-5_4_2}` |
| `A_{a}^{y}` | inflation-adjusted total government spending on protection scheme *a* |  | `{#sec-5_4_2}` |
| `L_{\text{dcy}}` | total PIT liabilities of decile d, country c, year y | real 2021 LCU | `{#sec-5_4_3_1}` |
| `l_{\text{dcy}}` | per-capita PIT liabilities |  | `{#sec-5_4_3_1}` |
| `s_{\text{dc}}` | share of PIT liability of decile d (text also `s_{\text{dcy}}`) |  | `{#sec-5_4_3_1}` |
| `{AVG\_ PIT\_ GDP}_{c}` | 2010–2019 average PIT-to-GDP ratio |  | `{#sec-5_4_3_1}` |
| `\text{RGDP}_{\text{cy}}` | real GDP in constant 2021 LCU |  | `{#sec-5_4_3_1}` |
| `P_{\text{dcy}}` | total population of decile d |  | `{#sec-5_4_3_1}` |
| `r_{\text{cy}}` | ratio of all available CT revenues to the sum of all individuals |  | `{#sec-5_4_3_2}` |
| `f_{\text{cy}}` | LCU gain from CP revenue recycling per LCU of baseline PIT paid |  | `{#sec-5_4_3_2}` |
| `\mathbb{I}_{\left\lbrack d = exempt \right\rbrack}` | indicator: decile d selected for full PIT exemption |  | `{#sec-5_4_3_2}` |

### 2.10 Air pollution (`06_Air_pollution.qmd`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `A_{\text{ij}}` | source-receptor matrix coefficient (annual mean responses) | $\mu$g/m3 | Option 1 `{#sec-tmfasst}` |
| `E_{i}(x)` | emission rate (kg/yr) of precursor I at source x | kg/yr | Option 1 |
| `C_{j,\ base}\left( y \right)` | constant for pollutant $j$ and location $y$ |  | Option 1 |
| `n_{x}` | number of source regions (`n_{i}` number of precursors) |  | Option 1 |
| `UrbanIncFactor` | urban increment factor (also `urbIncfactor`, `urbanIncfactor`) |  | Option 1 |
| `\text{AF}_{s}` | Adjustment factor for sector $s$ |  | Option 2 `{#sec-apportinfo}` |
| `\text{ShareExterna}l_{s}` | % Contribution to ambient PM2.5 from sector $s$, according to user's input or to WHO database (FASST counterpart `\text{ShareFASS}T_{s}`) | \% | Option 2 |
| `E_{s,p,m}` | Emissions of sector $s$ and pollutant $p$ in month $m$ | Tg | Option 3 |
| `\beta_{s,p}` | emission coefficients (elastic net); derived `{\beta'}_{s,p}`, `{\beta''}_{s,p}` |  | Option 3 |
| `\gamma_{1}` | weather coefficients `\gamma_{1}`..`\gamma_{6}` on PPT, TMIN, TMAX, VPD, WS, WD |  | Option 3 |
| `\delta_{s}` | sector composite-index coefficients (derived `\delta_{s}^{'}`, `{\delta^{''}}_{s}`) |  | Option 3 |
| `\lambda_{p}` | pollutant composite-index coefficients |  | Option 3 |
| `\mu` | NOx×NH3 interaction coefficient (`\nu` SO2×NH3, `\xi` SO2×NOx, `\theta_{s}` sector×WS×WD) |  | Option 3 |
| `\phi_{m}` | Monthly fixed effects |  | Option 3 |
| `\varphi_{m}` | month weight (days/365) |  | Option 3 |
| `T_{p,m}` | composite index from the sum of total emissions of pollutant $p$ in month $m$ (also `T_{s,m}`, `T_{p}`, `T_{s}`, `T_{p,s}`) |  | Option 3 |
| `w_{p,m}` | share of emissions of pollutant $p$ in month $m$ |  | Option 3 |
| `\widehat{E_{s,p,m}}` | normalized emissions (OLS) |  | Option 3 > OLS |
| `iF` | Intake Fraction, inhaled grams of PM2.5 per ton (ppm) of emissions | ppm | Option 4 `{#sec-if}` |
| `P_{i}` | population residing in a region located at a distance $i$ from the emission source |  | Option 4 |
| `\text{BR}` | Average breathing rate | m3/day | Option 4 |
| `Q` | Emissions rate | tonne/day | Option 4 |
| `CM` | implied "concentration matrix" (change in concentration per 1 tonne/year) | µg/m3 per tonne/yr | Option 4 |
| `P_{s,p,t}` | perturbation compared to emissions in the baseline year (%) | \% | Option 5 `{#sec-machlearn}` |
| `C_{0}` | contribution of sources not modeled in CPAT (constant) | µg/m3 | Modeled and total ambient pollution |
| `\text{RR}` | Relative Risk |  | Definitions of key technical terms |
| `\text{Exp}_{\text{OAP}}` | Ambient PM2.5 exposure level | µg/m3 | Joint ambient and household |
| `\text{Exp}_{\text{HAP}}` | Excess exposure to PM2.5 for those who use solid fuel for cooking | µg/m3 | Joint ambient and household |
| `p_{\text{HAP}}` | proportion of the population using solid fuel for cooking (appendix writes `p_{H}`) |  | Joint ambient and household |
| `{PAF}_{\text{PM}}` | Population level PAF (also `\text{PA}F_{\text{OAP}}`, `\text{PA}F_{\text{HAP}}`) |  | Joint ambient and household |
| `TMREL` | theoretical minimum risk exposure level (PM2.5: 4.15 µg/m3; O3 ~U(29.1, 35.7) ppb) |  | Joint ambient and household; Ozone |
| `L_{s,a}` | standard loss function (years of life lost for a death at age a, sex s) | years | Health outcomes |
| `\text{DW}_{c,s,a}` | Disability weight |  | Health outcomes |
| `{\mathrm{\Delta}C}_{O3}` | change in ozone concentration (RR 1.06 per 10 ppb, 6mDMA8h) | ppb | Ozone air pollution |
| `\lambda_{\text{TMREL}}` | Mortality incidence proportion if pollution was a the TMREL level |  | `{#sec-quanthealtheff}` |
| `M_{0}` | Baseline mortality (`M_{1}` under policy) | deaths | `{#sec-quanthealtheff}` |
| `\text{WDL}_{\text{pollution}}` | working days lost due to pollution (β = 0.0046) | days | Working days lost |
| `W_{\text{ij}}` | expected value of GDP per worker for a person of age $j$ in state $i$ |  | Market output losses |
| `\alpha` | Labor's share of GDP (default 65%) — in this chapter |  | Market output losses |
| `\text{PV}_{\text{ij}}` | present discounted value of lost market and non-market output |  | Market output losses |
| `hp` | household production (not included) |  | Market output losses |
| `\text{HEAP}_{c,t}` | total health expenditure attributed to pollution |  | Health expenditure |
| `VSL_{c}` | value of statistical life (VSL_OECD,2005 = 3 million USD 2005 PPP; income elasticity `b` = 0.8 HIC, 1.2 others) |  | Value of the statistical life |
| `CI_{t}` | congestion index | \% | Travel time saved |
| `FreeFlowTT` | free-flow travel time per vehicle-km | min/vehkm | Travel time saved |

### 2.11 Road transport (`07_Road_Transport.qmd`)

| Symbol (LaTeX as in docs) | Meaning (docs wording) | Unit (docs) | Where defined/used |
|---|---|---|---|
| `\ln\left( Y_{\text{ct}} \right)` | natural logarithm of the outcome in country $c$ in year $t$ |  | Estimation equation |
| `\ln{(p_{\text{ct}})}` | natural logarithm of pump price for gasoline |  | Estimation equation |
| `X_{\text{ct}}` | vector of covariates including income per capita and population density |  | Estimation equation |
| `\mu_{c}` | country-specific effects (`\mu_{t}` year effects) |  | Estimation equation |
| `\widehat{\beta}` | estimate of the elasticity of the outcome wrt fuel prices |  | Estimation equation |
| `{\overline{x}}_{c}` | average of $x_{\text{ct}}$ over time; `T_{c}` number of years |  | Short-run and long-run estimators |
| `\beta'` | between (long-run) coefficient; `\beta''` within (short-run) |  | Short-run and long-run estimators |
| `v_{\text{ct}}^{1}` | additional variable influencing elasticity (general `v_{\text{ct}}^{k}`) |  | Country-specific elasticity estimates |
| `{\widehat{\beta}}_{c}` | country-specific elasticity |  | Country-specific elasticity estimates |
| `Y_{t}^{\text{baseline}}` | baseline (without policy) forecast of variable $Y$ |  | Baseline forecasts |
| `Y_{t}^{\text{simple}}` | "naïve" linear forecast based only on past observed values (text later writes `Y_{t}^{f}`) |  | Baseline forecasts |
| `\overline{g^{\text{GDP}}}` | expected GDP growth (geometric average growth over past years); `\overline{g^{\text{pop}}}` analogous |  | Baseline forecasts |
| `\eta_{\text{GDP}}` | elasticity of the outcome wrt GDP (`\eta_{\text{pop}}` wrt population) |  | Baseline forecasts |
| `\eta_{p}` | elasticity wrt fuel price |  | Policy forecast |
| `p^{\text{baseline}}` | baseline road fuel price (consumption-weighted gasoline/diesel); `p^{\text{policy}}` policy |  | Policy forecast |

## 3. Core equations, verbatim

No equation in `03_Mitigation.qmd` or `04_Multipliers.qmd` carries a Quarto `{#eq-...}` label; labels exist only in `05_Distribution.qmd`, `06_Air_pollution.qmd` and `07_Road_Transport.qmd`. For unlabelled equations the source line numbers are given.

Important structural facts (from the text):

- **No partial-adjustment / lagged-response model.** "For simplicity, we assume that all the effects take place over the course of one year" (Fuel Consumption Dynamics); "CPAT, for a while, had short- and long-term components to the price elasticity. We eliminated these" (Status of upgrades); "all elasticities are long-term elasticities" (Price elasticities). The only lags are (i) the year-on-year ratio form of the demand equation and (ii) engineer-model end-user power prices: "These prices respond to changes in weighted total generation cost, which is lagged by one year to avoid circularity issue" (Power demand); fuel costs in the engineer model default to "a moving average over a 5-year window".
- **No transport sub-model inside Mitigation**: transport fuel use follows the generic fuel equation (with biofuel split for road and jet fuel for domestic aviation). The Road Transport module is a separate post-processor (Section 5).
- **GDP feedback**: no equation is given anywhere in the docs (see 2.8).

### 3.1 Mitigation – prices, taxes, subsidies

**Retail price identity** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 598–598, "Fuel prices, taxes, and subsidies" > "Overview" `{#sec-PricesOVerview}`.  
Retail price = supply price + VAT + excise and all other taxes.

```tex
$p_{\text{cgft}} = sp_{\text{cgft}} + \text{va}t_{\text{cgft}} + \text{tx}o_{\text{cgft}}$
```

**Excise/other taxes, forecast composition (table)** — core. Inline in text/table (no label), `03_Mitigation.qmd`, Overview, `{#tbl-PriceForecastingSummary}`.  
Table @tbl-PriceForecastingSummary, row `txo`.

```tex
$txo = \text{fixtax} + \text{fixsub} + \text{flts} + \text{xcp} + \text{ncp}$
```

**Retail price, forecast composition (table)** — core. Inline in text/table (no label), `03_Mitigation.qmd`, Overview.  
Table @tbl-PriceForecastingSummary, row `p`.

```tex
$p = \text{sp} + \text{vat} + \text{txo}$
```

**Existing carbon price, one-step growth (main text)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 751–751, "Forecasted years: Construction of data on prices and taxes" `{#sec-PricesForecastedYears}`.  
Existing carbon price per energy unit = last year's existing carbon tax and ETS price grown at user rates δ.

```tex
$xcp_{cgft} = xct_{cgf,t - 1}*\left( 1 + \delta_{\text{CT}} \right) + xetsp_{cgf,t - 1}*\left( 1 + \delta_{\text{ETS}} \right)$
```

**New carbon price per energy unit (main text)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 757–757, `{#sec-PricesForecastedYears}`.  
National price per tCO2 × emission factor × sector-fuel coverage, for new carbon tax and new ETS. Also written in text: `$ncp_{cgft} = nct_{cgft} + netsp_{cgft}$`.

```tex
$ncp_{cgft} = NCT_{\text{ct}}*ef_{cgf}*\varphi_{\text{NCT},cgft} + NETSP_{ct}*ef_{cgf}*\varphi_{\text{NETS},cgft}$
```

**Aggregate (fuel-level) retail price** — adjustment/detail (reporting). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 779–779, "Price aggregation" `{#sec-PricesAggregation}`.  
Consumption-weighted average of sector-group retail prices.

```tex
$P_{cf,t} = \sum_g {\frac{F_{cgf,t}}{\sum_g F_{cgf,t}}*p_{cgf,t}}$
```

Appendix C (historical decomposition, `{#sec-Appendix_C_Prices}` > "Price components" > "Assumed pricing mechanism"):

**Retail = supply + total net taxes** — adjustment/detail (historical data construction). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 3991–3993, Appendix C > Assumed pricing mechanism.  
Holds for all scenarios.

```tex
$$
p_{cgf,t}=sp_{cgf,t} + ttx_{cgf,t}
$$
```

**Total net taxes (residual)** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4001–4003, Appendix C > Assumed pricing mechanism.  
ttx negative = net subsidy.

```tex
$$
ttx_{cgf,t} = p_{cgf,t} - sp_{cgf,t}
$$
```

**VAT payment (historical form)** — core (same form used in forecast). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4009–4011, Appendix C > Assumed pricing mechanism.  
VAT base (supply price + excise/other) × VAT rate; rate 0 for industry and power.

```tex
$$
vat_{c,f,g,t} = \left( sp_{c,f,g,t} + txo_{c,f,g,t} \right)*vatrate_{c,f,g,t}
$$
```

**Excise and other taxes (historical residual)** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4019–4021, Appendix C > Assumed pricing mechanism.  
Residual of retail price after supply price and VAT.

```tex
$$
txo_{cgf,t} = p_{cgf,t} - sp_{cgf,t} - vat_{cgf,t}
$$
```

Appendix C forecast ("Forecasted prices (after 2021)" > "Calculations: Modeling assumptions"; text: "For years starting from 2023"):

**Retail price (forecast)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4079–4081, Appendix C > Calculations.  


```tex
$$
p_{cgf,t} = sp_{cgf,t} + vat_{cgf,t} + txo_{cgf,t}
$$
```

**Supply price (forecast)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4085–4087, Appendix C > Calculations.  
Fixed + floating portion + outstanding producer-side subsidy.

```tex
$$
sp_{cgf,t} = fixsp_{cgf} + fltsp_{cgf,t} + ps_{cgf,t}
$$
```

**Fixed portion of supply price** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4093–4095, Appendix C > Calculations.  
Average over historical years 2018–2022.

```tex
$$
fixsp_{cgf} = \frac{1}{n_{t_0}} \sum_{t_0 = 2018}^{2022} fixsp_{cgf,t_0} 
$$
```

**Floating portion of supply price** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4098–4100, Appendix C > Calculations.  
Grows with international price gp.

```tex
$$
fltsp_{cgf,t} = fltsp_{cgf,t-1} \times \frac{gp_{cgf,t}}{gp_{cgf,t-1}}
$$
```

**Producer-side subsidy phase-out** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4103–4105, Appendix C > Calculations.  


```tex
$$
ps_{cgf,t} = ps_{cgf,t-1} \times \phi_{\text{PS}, t}
$$
```

**VAT payment (forecast)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4111–4113, Appendix C > Calculations.  


```tex
$$
vat_{cfg,t} = \left( sp_{cfg,t} + txo_{cfg,t} \right)*vatrate_{cfg,t}
$$
```

**Excise and other taxes (forecast)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4122–4127, Appendix C > Calculations.  
Sum of fixed tax, fixed subsidy, floating tax/subsidy, existing and new carbon taxes/ETS, new excise.

```tex
$$
\begin{align*}
    txo_{cgf,t} = fixtax_{cgf,t} \; + \; &fixsub_{cgf,t} \; + \; flts_{cgf,t} \; + \; xct_{cgf,t} \; + \; xetsp_{cgf,t} \; + \\
    &nct_{cgf,t} \; + \; netsp_{cgf,t} \; + \; nexc_{cgf,t}
\end{align*}
$$
```

**Fixed portion of taxes** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4134–4134, Appendix C > Calculations.  


```tex
$$fixtax_{cgf,t} = fixtax_{cgf,{t_0}}$$
```

**Fixed portion of subsidies with phase-out** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4138–4138, Appendix C > Calculations.  


```tex
$$fixsub_{cgf,t} = fixsub_{cgf,{t_0}} \times \phi_{\text{CS}, t}$$
```

**Floating portion of subsidy/tax with price-control phase-out** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4144–4146, Appendix C > Calculations.  


```tex
$$
flts_{cgf,t} = \left( \frac{\sum_{t_0 = 2018}^{2022} flts_{cgf,t_0}}{n_{t_0}} + \frac{\sum_{t_0 = 2018}^{2022} sp_{cgf,t_0}}{n_{t_0}} - sp_{cgf,t} \right) \times \left(1 - pcc \right) \times \phi_{\text{PC}_t}
$$
```

**Existing carbon price (compounded from base year)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4153–4160, Appendix C > Calculations.  
Base-year national price × ef × coverage × (1+δ)^(t−t0).

```tex
$$
\begin{align*}
xcp_{cgf,t} = \; &xct_{cgf,t} + xetsp_{cgf,t} \\
            = \; &xct_{cgf,t_0}*(1 + \delta_{CT})^{t-t0} \; + \; xetsp_{cgf,t_0}*(1+\delta_{ETS})^{t-t_0} \\
            = \; &XCT_{c,t_0}*ef_{cgf}*\varphi_{XCT,cgf,t_0}*(1 + \delta_{CT})^{t-t_0} \; + \\
              \; &XETSP_{c,t_0}*ef_{cgf}*\varphi_{XETS,cgf,t_0}*(1 + \delta_{ETS})^{t-t_0}
\end{align*}
$$
```

**New carbon price** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4166–4172, Appendix C > Calculations.  


```tex
$$
\begin{align*}
ncp_{cgf,t} = \; &nct_{cgf,t} \; + \; netsp_{cgf,t} \\
            = \; &NCT_{c,t}*ef_{cgf}*\varphi_{NCT,cgf,t} \; + \\
             &NETSP_{c,t}*ef_{cgf}*\varphi_{NETS,cgf,t}
\end{align*}
$$
```

**Direct carbon pricing (memo)** — adjustment/detail (memo account). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4184–4186, Appendix C > Calculations.  


```tex
$$
tcp^{DIR}_{cgf,t} = xcp_{cgf,t} + ncp_{cgf,t} 
$$
```

**Indirect carbon pricing (memo)** — adjustment/detail (memo account). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4190–4196, Appendix C > Calculations.  


```tex
$$
\begin{align}
tcp^{IND}_{cgf,t} \; = \; &fixtax_{cgf,t} \; + \; fixsub_{cgf,t} \; + \; flts_{cgf,t} \; + \; nexc_{cgf,t} \; + \; \theta^{PS}_{TCP} \; ps_{cgf,t} \; +  \\
& + \; \left(vatrate_{cfg,t} \; - \; \overline{vatrate}_{c,t}\right) \times \Big( sp_{cfg,t} \; + \; fixtax_{cgf,t} \; + \;  flts^{+}_{cgf,t} \; + \\
& \hspace{5.5cm} + \; xcp_{cgf,t} + ncp_{cgf,t}  \Big)_{g \; \in \; [\text{pow, ind}] \; , \; f \; \notin \; [\text{oil, bio}]} 
\end{align}
$$
```

**Total carbon price per energy unit (memo)** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4201–4205, Appendix C > Calculations.  


```tex
$$
\begin{align}
  tcp_{cgf,t} \; = \; &tcp^{DIR}_{cgf,t} \; + \; tcp^{IND}_{cgf,t}  \\
\end{align}
$$
```

**Fuel-level TCP (memo)** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4208–4210, Appendix C > Calculations.  
CO2-weighted average across sector groups.

```tex
$$
  TCP_{cf, t} \; = \; \frac{\sum_g TCP_{cgf,t} \; F_{cgf,t} \; ef_{cgf, t}}{\sum_g F_{cgf,t} \; ef_{cgf, t}}
$$
```

**National TCP (memo)** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4212–4214, Appendix C > Calculations.  


```tex
$$
TCP_{c, t} \; = \frac{\sum_f TCP_{cf, t} \left(\sum_g F_{cgf,t} \; ef_{cgf, t} \right)}{\sum_f \sum_g F_{cgf,t} \; ef_{cgf, t}}
$$
```

Power end-user prices are in 3.3. Exemption phase-out (text only): "the carbon pricing policy (new carbon tax or ETS) will increase by 1/n every year"; subsidy phase-out: "decrease linearly by 1/n every year" (Appendix C > User options).

### 3.2 Mitigation – energy demand (fuel use response)

**Fuel consumption dynamics (THE demand equation)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 825–825, "Fuel Consumption Dynamics" `{#sec-FuelConsumptionDynamics}`.  
Year-on-year fuel use ratio = autonomous efficiency term (with rebound) × Covid factor × GDP effect × price effect on usage × price effect on efficiency. Applies to every scenario o, country c, sector s, fuel f. Shadow prices of non-pricing policies enter only the efficiency term.

```tex
$\frac{F_{\text{ocsf},t}}{F_{\text{ocsf},t - 1}} = \left( \frac{1}{1 + \alpha_{\text{sf}}} \right)^{1 + \epsilon_{U,c\text{sf}}}\Psi_{\text{ct}}\left( \frac{Y_{c,t}}{Y_{c,t - 1}} \right)^{\epsilon_{Y,\text{csf}}}\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{U,\text{csf}}}\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{F,\text{csf}}\left( 1 + \epsilon_{U,\text{csf}} \right)}$
```

Named terms (verbatim, same section): GDP effect `\left( \frac{Y_{c,t}}{Y_{c,t - 1}} \right)^{\epsilon_{Y,\text{csf}}}`; price effect on usage `\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{U,\text{csf}}}`; price effect on energy efficiency `\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{F,\text{csf}}\left( 1 + \epsilon_{U,\text{csf}} \right)}`. "Both autonomous and price-driven efficiency components are subject to rebound effects by raising to the power of $\left( 1 + \epsilon_{U} \right)$, where $\epsilon_{U}$ is negative."

**Biomass leakage share (residential cooking)** — adjustment/detail (option). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 882–882, "Biomass substitution in the residential sector".  
Share of the % change in the most-used cooking fuel (f = nga, lpg, ker) that is transferred to biomass; ε_bio,f = 0.25 ("for a 10% price change in ... natural gas, 0.9% of natural gas consumption is shifted to biomass").

```tex
$\epsilon_{\text{bio},f}*\frac{\text{Ef}f_{\text{bio}}}{\text{Ef}f_{f}}$
```

**Rebound decomposition of the total price term** — adjustment/detail (derivation). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 978–978, "Rebound effect".  
"the rebound effect is defined as the product of the energy efficiency elasticity and the usage elasticity"; with ε_F = ε_U = −0.3 the rebound is 15.5%.

```tex
$\left( \frac{P_{t}}{P_{t - 1}} \right)^{\epsilon_{F} + \epsilon_{U} + \epsilon_{F}*\epsilon_{U}}$
```

Covid calibration (`{#sec-CalibrationCovid}`) is described only in prose (emissions-outturn calibration in 2020–21; "difference in recent three-year average GDP growth vs 2020 growth rate times 1.4"; −4.2% vs 2019 for 2021). Adjustment/detail.

### 3.3 Mitigation – power sector

#### 3.3.1 Generation costs and power prices (`{#sec-PowerPrices}`)

**Current variable cost (dispatch cost)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1197–1197, "Concept 1: Current variable costs".  
Variable OpEx + fuel cost (price / thermal efficiency) + implicit coal price. Text: fuel cost $\frac{ps_{\text{cft}}}{\nu_{\text{cf}}}$ (pre-tax incl. producer subsidies), 5-year moving average by default.

```tex
$vc_{\text{ocft}} = \text{vo}p_{\text{ocft}} + fc_{\text{ocft}} + ip_{\text{cft}} = \text{vo}p_{\text{ocft}} + \frac{p_{\text{ocft}}}{\nu_{\text{cf}}} + ip_{\text{cft}}$
```

**Levelized cost of a cost component (general)** — core (concept). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1218–1218, "Concept 2: Levelized costs of generation" > "General approach".  
Discounted sum of component-q costs / discounted generation.

```tex
$\text{LCO}E_{q} = \frac{PV_{q}}{\text{dem}} = \frac{\sum_{t = 0}^{N - 1}C_{q,t}e^{- \text{rt}}}{\sum_{t = 0}^{N - 1}g_{t}e^{- \text{rt}}}$
```

**Levelized total investment cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1253–1253, Concept 2 > General approach.  
Used in the investment logit; dfc defined in text as "$1 + \text{wac}c_{\text{cft}}^{t - t_{0}}$".

```tex
$\text{ti}c_{P,\text{cf}} = \frac{vc_{P,\text{cft}}*cf_{\text{cf}}*\text{df}c_{\text{cft}}}{cf_{\text{cf}}*\text{df}c_{\text{cft}}} + \text{fi}x_{\text{cft}}^{\text{fl}}$
```

**Forward-looking levelized fixed cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1257–1257, Concept 2 > General approach.  
CapEx and decommissioning annualised over discounted lifetime + storage + fixed OpEx + renewable subsidy + transmission.

```tex
$\text{fi}x_{\text{cft}}^{\text{fl}} = \frac{\text{ca}x_{\text{cft}}}{cf_{\text{cf}}*365*24*\text{dl}f_{\text{cft}}} + \frac{\text{dt}c_{\text{cft}}}{cf_{\text{cf}}*365*24*\text{dl}f_{\text{cft}}} + \text{st}o_{\text{cft}} + \text{op}f_{\text{cft}} + \text{pusRe}n_{\text{cft}} + tmc_{fct}$
```

**Post-policy total current cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1271–1271, Concept 2 > General approach.  
Text: "where $vc_{P,\text{cft}} = vc_{B,\text{cft}} + \text{nc}p_{\text{cft}}$".

```tex
$\text{LCO}E_{P,\text{cft}} = vc_{P,\text{cft}} + \text{fi}x_{\text{cft}}^{\text{fl}}$
```

**LCOE geometric-series simplification** — adjustment/detail (derivation). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1279, 1285, 1287, 1289, 1291, 1295, 1297, "LCOE methodology: Simplification".  
Closed form when costs grow at constant log rate τ after year n; for constant costs LCOE = C0/g0.

```tex
$\text{LCO}E_{q} = \frac{PV_{q}}{g} = \frac{\sum_{t = 0}^{N - 1}C_{q,t}e^{- \text{rt}}}{\sum_{t = 0}^{N - 1}g_{t}e^{- \text{rt}}}$
$\begin{matrix} \text{PVofCosts} & = \sum_{t = 0}^{n - 1}C_{t}e^{- \text{rt}} + \sum_{t = n}^{N - 1}C_{n}e^{- \text{rn}}\left( e^{\tau - r} \right)^{t - n} & & & \\ \end{matrix}$
$= \sum_{t = 0}^{n - 1}C_{t}e^{- \text{rt}} + C_{n}e^{- \text{rn}}\sum_{t = n}^{N - 1}\left( e^{\tau - r} \right)^{t - n}$
$= \sum_{t = 0}^{n - 1}C_{t}e^{- \text{rt}} + C_{n}e^{- \text{rn}}\sum_{t = 0}^{N - n - 1}\left( e^{\tau - r} \right)^{t}$
$= \sum_{t = 0}^{n - 1}C_{t}e^{- \text{rt}} + C_{n}e^{- \text{rn}}\frac{1 - \left( e^{\tau - r} \right)^{N - n}}{1 - \left( e^{\tau - r} \right)}$
$\text{PVofCosts} = C_{n}e^{- \text{rn}}\frac{1 - \left( e^{\tau - r} \right)^{N - n}}{1 - \left( e^{\tau - r} \right)} = C_{0}\frac{1 - e^{- \text{rN}}}{1 - e^{- r}}$
$\begin{matrix} \text{LCOE} & = \frac{\sum_{t = 0}^{N - 1}C_{t}e^{- \text{rt}}}{\sum_{t = 0}^{N - 1}g_{t}e^{- \text{rt}}} & = \frac{\sum_{t = 0}^{N - 1}C_{0}e^{\text{τt}}e^{- \text{rt}}}{\sum_{t = 0}^{N - 1}g_{t}e^{- \text{rt}}} & = \frac{\sum_{t = 0}^{N - 1}C_{0}\left( e^{\tau - r} \right)^{t}}{\sum_{t = 0}^{N - 1}g_{t}e^{- \text{rt}}} & = \frac{C_{0}\frac{1 - e^{- \text{rN}}}{1 - e^{- r}}}{g_{0}\frac{1 - e^{- \text{rN}}}{1 - e^{- r}}} & = \frac{C_{0}}{g_{0}} \\ \end{matrix}$
```

**Cost-recovery generation cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1308–1308, "Concept 3: Cost-recovery estimated total cost of generation".  


```tex
$\text{gn}c_{B,\text{cft}} = vc_{B,\text{cft}} + \text{fi}x_{\text{cft}}$
```

**Amortized fixed cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1314–1314, Concept 3.  


```tex
$\text{fi}x_{B,\text{cft}} = \text{ac}c_{\text{cft}} + \text{in}t_{\text{cft}} + \text{de}c_{\text{cft}} + \text{st}o_{\text{cft}} + \text{op}f_{\text{cft}}$
```

Components of amortized fixed cost (inline, Concept 3, verbatim):

- acc – yearly amortization of capital costs per kWh: `\frac{\text{ca}x_{\text{cft}}^{\text{av}}}{\text{cf}*365*24*\text{li}f_{f}}`
- weighted average CapEx update: `\text{ca}x_{\text{cf},t - 1}^{\text{av}}*\left( 1 - \Phi_{\text{inv}} \right) + \text{ca}x_{\text{cft}}*\Phi_{\text{inv}}`
- int – interest cost, straight-line amortization: `0.5*\frac{\text{ca}x_{\text{cft}}^{\text{av}}*\text{wac}c_{\text{cf}}}{cf_{\text{cf}}*365*24}`
- dec – yearly amortization of decommissioning costs (not discounted): `\frac{\text{dt}c_{B,\text{cft}}}{cf_{B,\text{cf}}*365*24*\text{li}f_{f}}`
- opf – fixed OpEx per kWh: `\frac{\text{tf}c_{\text{cft}}}{365*24*cf_{\text{cf}}}`

**Weighted average generation cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1340–1340, "Concept 4: End-user prices".  
Generation-share-weighted current (cost-recovery) generation cost, baseline, carbon tax excluded.

```tex
$\text{gn}c_{B,\text{ct}}^{\text{av}} = \sum_{f}^{}gns_{B,\text{cft}}*\text{gn}c_{B,\text{cft}}$
```

**Engineer-model supply power price** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1346–1346, Concept 4.  
g = Residential, Industrial; tmc = \$40/MWh residential, \$15/MWh industrial.

```tex
$sp_{B,\text{cg}}^{T} = \text{gn}c_{B,\text{ct}}^{\text{av}} + \text{tmc}$
```

**Markup calibrating to historical retail price** — core (calibration). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1354–1354, Concept 4.  
"when the markup is negative (i.e. retail prices are lower than modeled supply prices), the model captures a subsidy."

```tex
$mu_{B,\text{cgt}}^{T} = \text{gn}c_{B,\text{ct}}^{\text{av}} + \text{tmc} - \text{hr}p_{\text{cg}}.$
```

**End-user power price (policy)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1362–1362, Concept 4.  
Adds new carbon price, minus output-based rebate, plus power excise. Pass-through share (1/0.75/0.5/0.25/0) scales cost changes (text, Concept 4 and Appendix E).

```tex
$p_{P,\text{cgt}}^{T} = \text{gn}c_{B,\text{ct}}^{\text{av}} + \text{nc}p_{\text{cgt}} - \text{re}b_{P,\text{cgt}} + \text{pe}x_{P,\text{cgt}} + \text{tmc} + mu_{B,\text{cgt}}^{T}$
```

#### 3.3.2 Engineer model (`{#sec-EngineerModel}`)

**Power demand by sector** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1506–1506, "Power demand".  
Same form as the fuel equation with f = P; GDP elasticity written ε_G.

```tex
$\frac{E_{\text{ocsf},t}}{E_{\text{ocsf},t - 1}} = \left( \frac{1}{1 + \alpha_{\text{sf}}} \right)^{1 + \epsilon_{U,\text{sf}}}\Psi_{\text{ct}}\left( \frac{Y_{c,t}}{Y_{c,t - 1}} \right)^{\epsilon_{G,\text{csf}}}\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{U,\text{csf}}}\left( \frac{p_{\text{ocsf},t}}{p_{\text{ocsf},t - 1}} \right)^{\epsilon_{F,\text{csf}}\left( 1 + \epsilon_{U,\text{csf}} \right)}$
```

**Total generation requirement** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1518–1518, "Power demand".  
Demand grossed up by base-year shares of net exports, own use, transmission/statistical differences.

```tex
$g_{\text{oc},t} = \sum_{s}^{}E_{\text{ocs},t}*\left( 1 + \text{ne}t_{\text{oc},t_{0}} + \text{ei}u_{c,t_{0}} + \Delta_{c,t_{0}}^{\text{dif}} \right)$
```

**Multilogit share (generic)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1530–1530, "Power supply" `{#sec-PowerSupply}` > "Logit function".  
Share of investment (x = inv) or generation (x = gen) to type f by relative cost c; K default 2.

```tex
$\frac{x_{\text{ocft}}}{\sum_{f}^{}x_{\text{ocft}}} = \frac{e^{- K.c}}{\sum_{i}^{}e^{- K.c}}$
```

**Residual generation for coal + gas** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1544–1544, "Dispatch decision".  
Must-run renewables and nuclear (also biomass, oil per text) at fixed capacity factors.

```tex
$\text{reqge}n_{\text{oc},\text{COA} + \text{GAS},t} = g_{\text{oc},t} - \sum_{\text{fϵ}\left( \text{RE},\text{NUC} \right)}^{}cap_{f}*cf_{f}$
```

**Minimum coal generation** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1552–1552, "Dispatch decision".  
Gas at maximum capacity factor (default 90%); symmetric for gas.

```tex
$\text{minge}n_{\text{oc},\text{COA},t} = \text{reqge}n_{\text{oc},\text{COAL} + \text{GAS},t} - \text{ca}p_{\text{GAS}}*\text{maxC}f_{\text{GAS}}$
```

**Dispatch logit coal vs gas** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1556–1556, "Dispatch decision".  
H_f = vc / lowest vc between coal and gas.

```tex
$\lambda_{f} = \frac{e^{- K_{\text{dispatch}}.H_{f}}}{\sum_{f}^{}e^{- K_{\text{dispatch}}.H_{f}}}$
```

**Coal generation** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1562–1562, "Dispatch decision".  


```tex
$g_{\text{oc},\text{COA},t} = \text{minge}n_{\text{oc},\text{COA},t} + \lambda_{f}*\text{residualreqge}n_{\text{oc},\frac{\text{COA}}{\text{GAS}},t}$
```

**Generation mix with PPAs** — adjustment/detail (PPA option). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1568–1568, "Dispatch decision".  


```tex
$\gamma_{\text{ocf},t} = \left( 1 - \omega_{\text{oct}} \right)*{\widetilde{\gamma}}_{\text{ocf},t} + \omega_{\text{oct}}*\Omega*\left( \text{ca}p_{\text{ocft}}*CF_{\text{cft}} \right)$
```

**Capacity (stock) accounting** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1580–1580, "Retirement and capacity needed".  
Old capacity less retirements plus investment.

```tex
$g_{\text{ocft}} = g_{\text{ocf},t - 1} - \sum_{f}^{}ret_{ocf,t - 1} + inv_{ofc,t - 1}$
```

**Exponential retirement** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1584–1584, "Retirement and capacity needed".  
Coal uses plant-level scheduled retirement (Coal Plant Tracker) where available; hydro retirement default 0 (Appendix E).

```tex
$\text{re}t_{\text{ocft}} = \frac{1}{\text{lif}}*\text{ca}p_{\text{ocft}}$
```

**Cost-based early coal retirement share** — core (default on). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1596–1598, "Retirement and capacity needed".  
Multiplied by maximum coal retirement (80% of coal effective capacity); f ∈ {coal, solar, wind}.

```tex
$$
\text{re}p_{\text{oc},\text{coa},t} = 1 - \frac{e^{- K_{i}.H_{r,\text{COA}}}}{\sum_{f}^{}e^{- K_{i}.H_{r,f}}}
$$
```

**Investment allocation logit (round 1)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1620–1622, "Investment decision and non-VRE and VRE scale up limitations".  


```tex
$$
\frac{\text{iv}p_{\text{ocft}}}{\sum_{f}^{}{\text{iv}p_{\text{ocft}}}} = \zeta_{\text{cft}}*\frac{e^{- K_{i}.H_{i}}}{\sum_{i}^{}e^{- K_{i}.H_{i}}}
$$
```

**Maximum effective investment (scale-up cap)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1640–1642, Investment decision.  


```tex
$$
{\text{iv}_{\text{ocft}}^{\max} = g}_{\text{oc},t}*\zeta_{\text{cft}}*VRE_{\text{cft}}
$$
```

**Remaining unallocated investment** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1660–1662, Investment decision.  
Allocated in round 2 by least-cost merit order (prose).

```tex
$$
{iv_{\text{ocft}}^{\text{rem}} = \ iv}_{\text{ocft}}^{\max} - \min{(\text{iv}_{\text{ocft}}^{\max},\text{iv}_{\text{ocft}}^{\text{new}})}
$$
```

**Total new investment** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1670–1672, Investment decision.  


```tex
$$
iv^{\text{tot}} = \text{iv}_{\text{ocft}}^{\text{new}} + \ iv_{\text{ocft}}^{\text{rem}}
$$
```

**Coal-share calibration objective** — adjustment/detail (calibration 2019, 2020). Inline in text/table (no label), `03_Mitigation.qmd`, "Calibration and systems costs".  
Goal-seek on implicit coal price (positive only).

```tex
$\left( \text{co}a_{t}^{\text{est}} - \text{co}a_{t}^{\text{obs}} \right)^{2}$
```

**Short-term storage requirement** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1721–1723, "Storage decision" `{#sec-StorageDecision}` > "Short-term storage".  
Hours of storage per kW average generation (100% VRE → 9 h). Also appears inline at line 1719.

```tex
$$
\text{sst} = 9v^{2}
$$
```

**Marginal short-term storage** — core (as documented; see 4). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1729–1731, Short-term storage.  


```tex
$$
\frac{\text{dsst}}{\text{dv}} = 18v^{2}
$$
```

**Long-term storage requirement** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1747–1753, "Long-term storage".  
Zero below 75% VRE; 33% of LT storage cost allocated to VRE.

```tex
$$
\text{slt} =
\begin{cases}
    0 & \text{for } v \leq 0.75 \\
    \left(\frac{v-0.75}{1-0.75}\right)^2 & \text{for } v > 0.75 \\
\end{cases}
$$
```

**Marginal long-term storage** — core. Inline in text/table (no label), `03_Mitigation.qmd`, Long-term storage.  


```tex
$2*\frac{v - 0.75}{\left( 1 - 0.75 \right)^{2}}$
```

#### 3.3.3 Elasticity model (`{#sec-ElasticityModel}`)

**Total power demand (elasticity model)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1849–1851, "Total power demand".  
Economy-wide; half the Covid adjustment.

```tex
$$
\frac{E_{\text{oct}}}{E_{\text{oc},t - 1}} = \left( 1 + \alpha \right)^{- \left( 1 + \epsilon_{U} \right)}\left( 1 + 0.5*\Psi_{\text{ct}} \right)\left( \frac{p_{\text{cEt}}}{p_{\text{cE},t - 1}} \right)^{\epsilon_{U,\text{cE}}}\left( \frac{p_{\text{cEt}}}{p_{\text{cE},t - 1}} \right)^{\epsilon_{F,\text{cE}}}\left( \frac{Y_{\text{ct}}}{Y_{c,t - 1}} \right)^{\epsilon_{G,\text{cE}}}
$$
```

**Total generation** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1861–1863, "Total power supply".  


```tex
$$
g_{\text{oct}} = E_{\text{oct}}*\frac{g_{\text{oc},t_{0}}}{E_{\text{oc},t_{0}}}
$$
```

**Generation share update (documented form)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1871–1873, Total power supply.  


```tex
$$
\Phi_{\text{ocft}} = \Phi_{\text{ocf},t - 1}\left( \frac{\text{gn}c_{\text{ocft}}^{*}}{\text{gn}c_{\text{ocf},t - 1}^{*}} \right)^{\epsilon_{\widetilde{E}}} + \frac{\Phi_{\text{ocf},t - 1}\sum_{i \neq f}^{}\left\lbrack 1 - \frac{\text{gn}c_{\text{ocit}}^{*}}{\text{gn}c_{\text{oci},t - 1}^{*}} \right\rbrack^{\epsilon_{\widetilde{E}}}}{\sum_{j \neq f}^{}\Phi_{\text{ocj},t - 1}}
$$
```

**Generation share update with nuclear/hydro reallocation (as implemented)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1881–1883, Total power supply.  
Plus inline definitions below.

```tex
$$
\Phi_{\text{ocft}} = \Phi_{\text{ocf},t - 1}\left( \frac{\text{gn}c_{\text{ocft}}^{*}}{\text{gn}c_{\text{ocf},t - 1}^{*}} \right)^{\epsilon_{\widetilde{E}}} + \frac{\Phi_{\text{ocf},t - 1}\sum_{f \neq i}^{}\left\lbrack 1 - \iota_{\text{cft}} \right\rbrack^{\epsilon_{\widetilde{E}}}}{\sum_{f \neq i}^{}\Phi_{\text{ocf},t - 1}}*\delta^{\text{add}}
$$
```

```tex
$\iota_{\text{cft}} = \frac{\text{gn}c_{\text{ocft}}^{*}}{\text{gn}c_{\text{ocf},t - 1}^{*}}$ and $\delta_{\text{oct}}^{\text{add}} = \frac{\text{TotExces}s_{\text{oc},\text{NUC} + \text{HYD},t}}{\left( 1 - \Phi_{\text{oc},\text{HYD},t} - \Phi_{\text{oc},\text{NUC},t} \right)}$
```

**Fuel input to power generation** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1891–1893, Total power supply.  


```tex
$$
F_{\text{ocft}} = E_{\text{ocft}}*\left( \frac{1}{1 + \alpha_{f}} \right)^{t}\frac{F_{\text{ocf},0}}{E_{\text{ocf},0}}
$$
```

**Old IMF generation cost (elasticity model, 'Old' option)** — adjustment/detail (non-default). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4225–4225, Appendix C > "Power generation costs".  


```tex
$gnc_{ocft} = efc_{ocft} + nfc_{ocft} + rps_{o,cgft} + nct_{P,cgft}*\left( 1 - tex_{P,tcft} \right)$
```

**Base-year non-fuel cost** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 4232–4234, Appendix C > Power generation costs.  


```tex
$$
     nfc_{ocf,t_0} = \frac{efc_{ocf,t_0}}{(1-\gamma)}*\gamma
$$
```

#### 3.3.4 Power data preparation (`{#sec-PowerDataSources}`)

**Thermal efficiency from balances** — adjustment/detail (data). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1935–1937, "Data approach for the power prices and 'Engineer' power model".  
For coal, gas, oil, nuclear, biomass; =1 for solar, wind, hydro, other ren.; study value used if <10%.

```tex
$$
\nu_{\text{cf}} = \frac{g_{\text{cf},t_{0}}}{F_{\text{cEf},t_{0}}}
$$
```

**Capacity factor from data** — adjustment/detail (data). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 1949–1951, idem.  


```tex
$$
cf_{\text{cf}} = \frac{g_{\text{cf},t_{0}}}{\text{ca}p_{\text{cf},t_{0}}}
$$
```

**Learning curve** — core for CapEx projection (wind, solar from 2023). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2093–2093, "Estimation of the power sector characteristics" `{#sec-PowerCharacteristics}`.  


```tex
$\text{Cos}t_{t} = \text{Cos}t_{0}\left( \frac{\text{Ca}p_{t}}{\text{Ca}p_{0}} \right)^{\left( - \varepsilon \right)}$
```

**Learning rate** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2097–2097, idem.  


```tex
$\text{LR} = 1 - 2^{\varepsilon}$
```

Other data-prep inline formulas (verbatim): `$\text{CAPE}X_{2019} = 0.2 \times \text{CAPE}X_{2015} + 0.8 \times \text{CAPE}X_{2020}$`; overnight-cost adjustment `$\frac{\text{CapE}x_{\text{IRENA}}}{\left( 1 + \text{wacc} \right)_{\text{cons}}^{n}}$` ("Consistency across data sources").

### 3.4 Mitigation – emissions

**Total GHG = energy + non-energy** — core. Inline in text/table (no label), `03_Mitigation.qmd`, "Emissions" > "Overview".  


```tex
$em_{\text{oc},\text{GHG},t} = em_{\text{ocER},\text{GHG},t} + em_{\text{ocNER},\text{GHG},t}$
```

**Emission factor unit conversion** — adjustment/detail. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2278–2278, "Emission factors".  


```tex
$ef_{\text{cgf},\frac{\text{tC}O_{2}}{\text{ktoe}}} = ef_{\text{cgf},\frac{\text{tC}O_{2}}{\text{GJ}}}*41,868$
```

**Energy-related CO2 emissions** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2308–2308, "Energy-related emissions" > "Carbon dioxide".  
Base year scaled to UNFCCC inventory (multiplicative calibration factor, prose).

```tex
$em_{\text{ocEsfpt}} = F_{\text{ocEsft}}*ef_{\text{cEsfp}}$
```

**Total energy emissions** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2314–2314, idem.  


```tex
$em_{\text{ocpt}} = \sum_{s}^{}{\sum_{f}^{}e}m_{\text{ocsfpt}}$
```

**Methane from fossil fuel production** — core (methane). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2328–2330, "Methane ($CH_{4}$)".  


```tex
$$
em_{oc,oil/nga/coa,CH_{4},t} = prod_{oc,oil/nga/coa,t} * ef_{c,oil/nga/coa,CH_{4},After Abatment, t}
$$
```

**Methane abatement curve** — core (methane fee). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2344–2346, "Methane ($CH_{4}$)".  
Note: the closing `$$` line carries trailing prose in the source.

```tex
$$
red_{ocf, CH_{4}, t} = A * mf_{t}^{B}
$$where A and B are the inputs for the abatment curve.
```

**Energy N2O scaled to CO2** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2356–2358, "Nitrous oxide ... and Flourinated gases".  
F-gases energy: `$em_{\text{ocpt}} = 0$` for t > 2018.

```tex
$$
em_{oc,N_{2}O,t} = em_{oc,N_{2}O,\left( t - 1 \right)}*\frac{em_{\text{oc},CO_{2},t}}{em_{\text{oc},CO_{2},\left( t - 1 \right)}}
$$
```

**IPPU growth from industrial energy CO2** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2382–2388, "Industrial processes and product use".  


```tex
$$ 
\Delta em_{ocI,CO_{2},t + 1} =
\begin{cases}
    \max\left(0,\frac{em_{\text{ocEind},CO_{2},t + 1}}{em_{\text{ocEind},CO_{2},t}} - 1\right) & \text{for } t = 2019 \\
    \frac{em_{\text{ocEind},CO_{2},t + 1}}{em_{\text{ocEind},CO_{2},t}} - 1 & \text{for } t > 2019
\end{cases}
$$
```

**IPPU emissions all pollutants** — core. Inline in text/table (no label), `03_Mitigation.qmd`, Industrial processes and product use.  
For t > 2019.

```tex
$em_{\text{ocIpt}} = em_{\text{ocIp}\left( t - 1 \right)}*\left( 1 + \text{Δe}m_{\text{ocI},CO_{2},t} \right)$
```

**Agriculture (non-CH4)** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2408–2410, "Agriculture".  


```tex
$$
em_{\text{ocApt}} = \frac{em_{\text{ocAp},t - 1}}{\text{am}e_{A,t - 1}}(1 + Y_{\text{growth}})^{\epsilon_{Y}}*\left( 1 + lp_{\text{grow}} \right)^{\epsilon_{\text{lp}}}*\text{am}e_{\text{At}}
$$
```

**LULUCF CO2** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2432–2437, "Land use, land-use change and forestry".  


```tex
$$
em_{\text{ocLpt}} = \begin{cases}
em_{ocLp,t - 1} - \left\| em_{\text{ocLp},2019}\cdot\Delta em_{L,t} \right\| & \text{if }em_{ocLp,t - 1} < 0 \\
\frac{em_{ocLp,t - 1}}{ame_{cLp,t - 1}}\cdot ame_{cLpt} - \left\| em_{\text{ocL},2019}\cdot\Delta em_{L,t} \right\| & \text{if }em_{ocLp,t - 1} \geq 0 \\
\end{cases}
$$
```

**LULUCF CH4** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2445–2445, idem.  


```tex
$em_{\text{ocLpt}} = \frac{em_{\text{ocLp}\left( t - 1 \right)}}{\text{am}e_{B,L,t - 1}}*\text{am}e_{P,Lt} - \left| em_{\text{ocLp},2019}*\text{Δe}m_{L,t} \right|$
```

**LULUCF N2O** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2453–2453, idem.  


```tex
$em_{\text{ocLpt}} = \frac{em_{ocLp,t - 1}}{\text{am}e_{B,L,t - 1}}*\text{am}e_{P,Lt}*\left( 1 + lp_{\text{grow}} \right) - \left| em_{\text{ocLp},2019}*\text{Δe}m_{L,t} \right|$
```

**LULUCF F-gases** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2461–2461, idem.  


```tex
$em_{\text{ocLpt}} = \frac{em_{\text{ocLp},t - 1}}{\text{am}e_{B,Lp,t - 1}}*\text{am}e_{P,Lt}*\left( 1 + lp_{\text{grow}} \right)$
```

**Waste and Other** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2473–2473, "Waste and Others".  


```tex
$em_{\text{ocupt}} = \frac{em_{\text{ocup},t - 1}}{\text{am}e_{B,u,t - 1}}*\text{am}e_{P,ut}*\left( 1 + lp_{\text{grow},t} \right)^{\epsilon_{\text{lp}}}$
```

Agricultural and waste CH4 (prose only): production driven by GDP and population growth and the oil-producer-price change from the methane fee, × after-abatement EF × GWP of non-fossil methane.

### 3.5 Mitigation – fiscal revenues and welfare

**General revenue formula** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2521–2523, "Fiscal revenues" > "Overview".  


```tex
$$
rev_{ocfgt}=F_{ocfgt}*\varphi_{cgft}*ncp_{ocfgt}
$$
```

**Revenues from existing excises/other taxes** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2594–2601, "Total revenues raised by policy".  
Other energy use excluded.

```tex
$$
revExi_{ft} = \left\{
    \begin{array}{ll}
             (F_{ocft} - F_{oc,oen,ft})* (cs_{cft} + fao_{cft} + xct_{cft}) & \mbox{if } Existing ETS = EU ETS \\
             (F_{ocft} - F_{oc,oen,ft})* (cs_{cft} + fao_{cft} + xct_{cft} + xetsp_{cft}) & \mbox{if } Existing ETS \ne EU ETS
    \end{array}
\right.
$$
```

**Revenues from VAT** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2611–2613, idem.  


```tex
$$
revVAT_{ft} = (F_{ocft} - F_{oc,oen,ft}) * vat_{cft}
$$
```

**Producer-side subsidy cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2633–2635, idem.  
Oil: subsidized demand = global demand; coal/gas 50% global + 50% domestic; electricity domestic.

```tex
$$
cstPs_{ocft} = subDem_{ocft} * pusF_{ocft}
$$
```

**Renewable subsidy cost** — core. Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2647–2649, idem.  


```tex
$$
cstRen_{ocft} = pusRen_{ocft} * g_{ocft}
$$
```

**Revenues/losses from price controls** — adjustment/detail (memo, not in total). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2661–2663, "Revenues/losses from price controls".  


```tex
$$
ctr_{ocft} = (F_{ocft} - F_{oc,oen,ft}) * (pth_{ocft}-1) * (pInt_{ocft} - pInt_{ocf,t-1})
$$
```

**Efficiency (deadweight) cost** — core (welfare). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2701–2701, "Efficiency costs in CPAT".  
Harberger trapezoid: average of new and pre-existing tax × change in fuel use.

```tex
$ddw_{ft} = \frac{\left( nc_{ft} - xcp_{ft} \right)}{2}*(F_{P,ft} - F_{B,ft})$
```

Welfare aggregation (prose, "Monetized welfare benefits"): averted climate damages (national SCC × ΔCO2) + averted air-pollution mortality/morbidity (AP module) + averted road accidents + reduced congestion (Transport module) − efficiency costs; shown as % of GDP.

### 3.6 Mitigation – validation and energy balances (detail)

**Panel fuel-demand regression** — adjustment/detail (validation). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 2823–2823, "Panel estimation of energy demand" > "Methodology".  


```tex
$\begin{matrix} \text{ln\:f}c_{\text{it}} = \alpha_{i} + \beta_{1}\text{\:ln\:}y_{\text{it}} + \beta_{2}\text{\:ln\:}p_{\text{it}} + \beta_{3}\text{\:t} + \epsilon_{\text{it}} \\ \end{matrix},$
```

**TPES identity** — adjustment/detail (data). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 3774–3774, Appendix B > "CPAT energy sectors".  


```tex
$\text{TPE}S_{j} = \text{Productio}n_{j} + \text{Import}s_{j} - \text{Export}s_{j} + \text{STOCKCH}A_{j}$
```

**TFC identity** — adjustment/detail (data). Label: `(no label)`. Source: `03_Mitigation.qmd` lines 3778–3778, Appendix B.  


```tex
$\text{TF}C_{j} = \text{TPE}S_{j} + \text{TOTTRAN}F_{j} + \text{TRANSFE}R_{j} + \text{OWNUS}E_{j} + \text{DISTLOS}S_{j} + \text{STATDIF}F_{j}$
```

### 3.7 Multipliers / GDP feedback (`04_Multipliers.qmd`)

**Local-projection panel regression** — adjustment/detail (offline estimation of multipliers). Label: `(no label)`. Source: `04_Multipliers.qmd` lines 163–163, "Methodology for estimating dynamic multipliers using panel data".  
Cumulative multiplier β_h per horizon.

```tex
$y_{i,t + h} - y_{i,t - 1} = \alpha_{i,h} + \delta_{t,h} + \text{Δs}_{i,t}\beta_{h} + \Delta x_{i,t}\gamma_{h} + \epsilon_{t,i,h}$
```

**Cyclical adjustment of revenue ratio** — adjustment/detail (offline). Label: `(no label)`. Source: `04_Multipliers.qmd` lines 208–208, "Cyclical adjustment of tax revenues and public spending".  


```tex
$\frac{T^{*}}{Y^{*}} = \frac{T}{Y}\left( \frac{Y^{*}}{Y} \right)^{\eta_{\text{YT}} - 1}$
```

**Missing in docs:** the in-model GDP update (Y as function of revenue-recycling shares, instrument multipliers by horizon, and baseline WEO growth). A rebuild must take it from the Excel model, not the docs.

### 3.8 Distribution (`05_Distribution.qmd`)

**eq-5_1** — core (data prep). Label: `{#eq-5_1}`. Source: `05_Distribution.qmd` lines 271–271, heading "Household budget shares {#sec-5_2_1}".  
Household budget share; aggregated to decile π^{dg} (popw-weighted).

```tex
$$\pi_{j}^{g} = \frac{C_{j}^{g}}{C_{j}} = \frac{C_{j}^{g}}{\sum C_{j}^{g}}$$ {#eq-5_1}
```

**eq-5_2** — core. Label: `{#eq-5_2}`. Source: `05_Distribution.qmd` lines 378–378, heading "Tax incidence analysis {#sec-5_3_1}".  
Additional expenditure share of household j: Σ over fuel-sector pairs of energy intensity × price change × category consumption / total consumption (direct + indirect effect).

```tex
$$p_{j} = \sum_{\text{fg}}p_{\text{fgj}}  = \frac{\sum_{\text{fg}}{\overline{e_{\text{fg}}}\ *t_{\text{fg}}* C_{\text{gj}}}}{C_{j}} \;\; , f \in g$$ {#eq-5_2}
```

**eq-5_3** — core (IO). Label: `{#eq-5_3}`. Source: `05_Distribution.qmd` lines 412–412, heading "Tax incidence analysis {#sec-5_3_1}".  
Energy intensities of non-fuel sectors via Leontief inverse (domestic fuels only; GTAP-10).

```tex
$$e_{g} = f\left( I - A \right)^{- 1}, \; f \notin g$$ {#eq-5_3}
```

**eq-5_4** — core (option: mitigation-adjusted). Label: `{#eq-5_4}`. Source: `05_Distribution.qmd` lines 520–520, heading "Mitigation-adjusted tax incidence {#sec-5_3_2_1}".  
Total revenues implied by HBS consumption.

```tex
$$P_{D} = \sum_{j}{p_{j}*C_{j}}$$ {#eq-5_4}
```

**eq-5_5** — core (option). Label: `{#eq-5_5}`. Source: `05_Distribution.qmd` lines 530–530, heading "Mitigation-adjusted tax incidence {#sec-5_3_2_1}".  
Scaling to national accounts in year y.

```tex
$$P_{D}^{y} = P_{D}* \frac{\text{GDP}^{y}*\theta_{c}}{\sum C_{j}}$$ {#eq-5_5}
```

**eq-5_6** — adjustment/detail (option). Label: `{#eq-5_6}`. Source: `05_Distribution.qmd` lines 543–543, heading "Mitigation-adjusted tax incidence {#sec-5_3_2_1}".  
Mitigation-adjusted downward factor, applied homogeneously.

```tex
$$p_{\text{Adj}} = \frac{P_{D}^{y} - P_{M}^{y}}{P_{D}^{y}} \; , \;P_{M}^{y} < P_{D}^{y}$$ {#eq-5_6}
```

**eq-5_7** — adjustment/detail (option). Label: `{#eq-5_7}`. Source: `05_Distribution.qmd` lines 577–577, heading "Decile-specific price elasticities of demand {#sec-5_3_2_2}".  
Decile-specific price-elasticity adjustment of consumption.

```tex
$$C_{j}^{g}* \left( \frac{p_{t}}{p_{t - 1}} \right)^{\epsilon_{\text{use}}}$$ {#eq-5_7}
```

**eq-5_8** — adjustment/detail (option). Label: `{#eq-5_8}`. Source: `05_Distribution.qmd` lines 599–599, heading "Imperfect pass-through {#sec-5_3_2_3}".  
Imperfect pass-through.

```tex
$$t_{\text{fg}}^{*} = t_{\text{fg}}*\gamma_{g}$$ {#eq-5_8}
```

**eq-5_9** — core (recycling). Label: `{#eq-5_9}`. Source: `05_Distribution.qmd` lines 722–722, heading "Targeted and infrastructure-based transfers {#sec-5_4_1}".  
Per-capita targeted transfer.

```tex
$$T^{y} = \frac{P_{M}^{y}}{\text{pop}_{T}^{y}}$$ {#eq-5_9}
```

**eq-5_10** — core (recycling). Label: `{#eq-5_10}`. Source: `05_Distribution.qmd` lines 734–734, heading "Targeted and infrastructure-based transfers {#sec-5_4_1}".  
Targeted population scaled to national population.

```tex
$$\text{pop}^T_y = (\sum \text{popw}_{T})* \theta_{\text{pop}}^{y}$$ {#eq-5_10}
```

**eq-5_11** — core (recycling). Label: `{#eq-5_11}`. Source: `05_Distribution.qmd` lines 738–738, heading "Targeted and infrastructure-based transfers {#sec-5_4_1}".  


```tex
$$\theta_{\text{pop}}^{y} = \frac{\text{pop}^{y}}{\sum\text{popw}}$$ {#eq-5_11}
```

**eq-5_12** — core (recycling). Label: `{#eq-5_12}`. Source: `05_Distribution.qmd` lines 747–747, heading "Targeted and infrastructure-based transfers {#sec-5_4_1}".  
Decile average transfer.

```tex
$$T_{d\ }^{y} = \ T^{y}*\frac{\sum \text{pop}_{T}^{\text{dy}}}{\sum \text{pop}^{\text{dy}}}$$ {#eq-5_12}
```

**eq-5_13** — core (recycling – infrastructure). Label: `{#eq-5_13}`. Source: `05_Distribution.qmd` lines 787–787, heading "Targeted and infrastructure-based transfers {#sec-5_4_1}".  
Population without access receives transfer.

```tex
$$\text{pop}_{\text{Ti}}^{\text{dy}} = \sum_{d = 1}^{10}\text{pop}^{\text{dy}}*(1 - \digamma^{\text{di}})$$ {#eq-5_13}
```

**eq-5_14** — core (recycling – existing schemes). Label: `{#eq-5_14}`. Source: `05_Distribution.qmd` lines 812–812, heading "Transfers through existing social protection schemes {#sec-5_4_2}".  
Proportional scale-up of ASPIRE schemes (quintile → deciles).

```tex
$${\mathrm{\Delta}A}_{a}^{y} = \frac{P_{M}^{y}}{A_{a}^{y}}$$ {#eq-5_14}
```

**PIT liabilities (total and per capita)** — core (PIT recycling). Label: `(no label)`. Source: `05_Distribution.qmd` lines 914–915, `{#sec-5_4_3_1}` "Data Requirements and Setup".  


```tex
$L_{\text{dcy}} = \ s_{\text{dc}}*{AVG\_ PIT\_ GDP}_{c}*\text{RGDP}_{\text{cy}}$
and $l_{\text{dcy}} = \ L_{\text{dcy}}/P_{\text{dcy}}$
```

**PIT – Targeted Exemption gain** — core (PIT option). Label: `(no label)`. Source: `05_Distribution.qmd` lines 977–977, `{#sec-5_4_3_2}` "Calculations".  


```tex
$$g_{dcy\_ TE} = l_{\text{dcy}}\mathbb{I}_{\lbrack d = exempt\rbrack} \mathbb{I}_{\lbrack 0\  \leq remaining\ CT\ revenues\  \leq l_{\text{dcy}}\rbrack}$$
```

**PIT – Personal Allowance gain** — core (PIT option). Label: `(no label)`. Source: `05_Distribution.qmd` lines 1005–1005, `{#sec-5_4_3_2}`.  


```tex
$$g_{dcy\_ PE} = {min\{ l_{\text{dcy}},\ r}_{\text{cy}}\}$$
```

**PIT – Proportional Compensation gain** — core (PIT option). Label: `(no label)`. Source: `05_Distribution.qmd` lines 1030–1030, `{#sec-5_4_3_2}`.  


```tex
$$g_{dcy\_ PC} = \ l_{\text{dcy}}*f_{\text{cy}}$$
```

Welfare measure (prose): consumption effects are compensating-variation / Laspeyres upper bounds ("un-adjusted consumption effects should be interpreted as upper-bound estimates in terms of Laspeyres Variation"); results by decile as % of pre-reform consumption and per-capita absolute amounts, overall/urban/rural; net effect = transfers − consumption effect. Direct effect uses residential-sector fuel price changes; indirect via IO. Cooking-fuel rebate and emissions-based ('time-zero revenue', ~60% final-demand) scaling are prose-only options.

### 3.9 Air pollution (`06_Air_pollution.qmd`) – all labelled equations

**eq-gainsem** — core. Label: `{#eq-gainsem}`. Source: `06_Air_pollution.qmd` lines 271–271, heading "Emission factors from GAINS".  
Emissions = fuel consumption × EF (computed in Mitigation tab).

```tex
 $$Emissions = FuelConsumption*Emission\ Factors$$ {#eq-gainsem}
```

**eq-sourcerecep** — core (Option 1). Label: `{#eq-sourcerecep}`. Source: `06_Air_pollution.qmd` lines 468–468, heading "Option 1: TM5-FASST {#sec-tmfasst}".  
TM5-FASST SR coefficient; ΔE = 0.2 E_base.

```tex
$$A_{\text{ij}}\left\lbrack x,\ y \right\rbrack = \frac{\mathrm{\Delta}C_{j}(y)}{\mathrm{\Delta}E_{i}\left( x \right)}$$ {#eq-sourcerecep}
```

**eq-deltae** — core (Option 1). Label: `{#eq-deltae}`. Source: `06_Air_pollution.qmd` lines 488–488, heading "Option 1: TM5-FASST {#sec-tmfasst}".  
Concentration at receptor.

```tex
$$C_{j}\left( y \right) = C_{j,\ base}\left( y \right) + \sum_{k = 1}^{n_{x}}{\sum_{i = 1}^{n_{i}}{A_{\text{ij}}\left\lbrack x_{k},\ y \right\rbrack*\left\lbrack E_{i}\left( x_{k} \right) - E_{i,\ base}\left( x_{k} \right) \right\rbrack*UrbanIncFactor}}$$ {#eq-deltae}
```

**eq-downscale** — adjustment/detail. Label: `{#eq-downscale}`. Source: `06_Air_pollution.qmd` lines 522–522, heading "Option 1: TM5-FASST {#sec-tmfasst}".  
Population downscaling of regional coefficients.

```tex
$$A_{i,j,country} = A_{i,j,region}*\frac{\text{Population}_{\text{region}}}{\text{Population}_{\text{country}}}$$ {#eq-downscale}
```

**eq-modeled** — core (Option 1). Label: `{#eq-modeled}`. Source: `06_Air_pollution.qmd` lines 529–529, heading "Option 1: TM5-FASST {#sec-tmfasst}".  
Modeled contribution by sector.

```tex
$$\text{Modeled\ }i_{t,s} = \sum_{j}^{}{\sum_{s}^{}{A_{i,j}*Emissions_{j,s,t}}}$$ {#eq-modeled}
```

**eq-bcincfactor** — adjustment/detail. Label: `{#eq-bcincfactor}`. Source: `06_Air_pollution.qmd` lines 573–573, heading "From FASST spreadsheet to CPAT".  
FASST spreadsheet mechanics.

```tex
$$d_{BC,1} = delta_{BC,1}*urbIncfactor$$ {#eq-bcincfactor}
```

**eq-pomincfactor** — adjustment/detail. Label: `{#eq-pomincfactor}`. Source: `06_Air_pollution.qmd` lines 575–575, heading "From FASST spreadsheet to CPAT".  


```tex
$$d_{POM,2} = delta_{POM,1}*urbIncfactor$$ {#eq-pomincfactor}
```

**eq-so4agg** — adjustment/detail. Label: `{#eq-so4agg}`. Source: `06_Air_pollution.qmd` lines 579–579, heading "From FASST spreadsheet to CPAT".  


```tex
$$d_{SO4,1} = delta_{SO2 \rightarrow SO4,1} + delta_{NOx - > SO4,1} + delta_{NH3 - SO4,1}$$ {#eq-so4agg}
```

**eq-no3agg** — adjustment/detail. Label: `{#eq-no3agg}`. Source: `06_Air_pollution.qmd` lines 580–580, heading "From FASST spreadsheet to CPAT".  


```tex
$$d_{NO3,1} = delta_{SO2 - > NO3,1} + delta_{NOX - > NO3,1} + delta_{NH3 - > NO3,1}$$ {#eq-no3agg}
```

**eq-nh4agg** — adjustment/detail. Label: `{#eq-nh4agg}`. Source: `06_Air_pollution.qmd` lines 581–581, heading "From FASST spreadsheet to CPAT".  


```tex
$$d_{NH4,1} = delta_{SO2 - > NH4,1} + delta_{NOx - > NH4,1} + delta_{NH3 - > NH4,1}$$ {#eq-nh4agg}
```

**eq-opragg** — adjustment/detail. Label: `{#eq-opragg}`. Source: `06_Air_pollution.qmd` lines 582–582, heading "From FASST spreadsheet to CPAT".  


```tex
$$d_{OPrPM2.5,1} = delta_{OPrPM2.5 - > OPrPM2.5,1}$$ {#eq-opragg}
```

**eq-totdp** — adjustment/detail. Label: `{#eq-totdp}`. Source: `06_Air_pollution.qmd` lines 586–586, heading "From FASST spreadsheet to CPAT".  


```tex
$$\text{TOTdP}M_{1} = d_{BC,\ 1} + d_{POM,\ 1\ } + d_{SO4,1} + d_{NO3,1} + d_{NH4,1} + d_{OPrPM2.5,1}$$ {#eq-totdp}
```

**eq-afs** — core (Option 2). Label: `{#eq-afs}`. Source: `06_Air_pollution.qmd` lines 626–626, heading "Option 2: Source apportionment information {#sec-apportinfo}".  
Source-apportionment adjustment factor.

```tex
$$\text{AF}_{s} = \frac{\text{ShareFASST}_{s,to}}{\text{ShareExterna}l_{s}}$$ {#eq-afs}
```

**eq-modpm** — core (Option 2). Label: `{#eq-modpm}`. Source: `06_Air_pollution.qmd` lines 645–645, heading "Option 2: Source apportionment information {#sec-apportinfo}".  


```tex
$$\text{Modeled~PM}{2.5}_{t} = \sum_{p}^{}{\sum_{s}^{}{AF_{s}*\text{FASST}_{p,s}*Emissions_{p,s,t}}}$$ {#eq-modpm}
```

**eq-monthconc** — adjustment/detail (Option 3 estimation form). Label: `{#eq-monthconc}`. Source: `06_Air_pollution.qmd` lines 793–793, heading "Elastic net model".  


```tex
$$P{M2.5}_{m} = \alpha + \sum_{s,p}^{}{\beta_{s,p}*E_{s,p,m}} + \gamma_{1}*PPT_{m} + \gamma_{2}*TMIN_{m} + \gamma_{3}*TMAX_{m} + \gamma_{4}*\text{VPD}_{m} + \gamma_{5}*\text{WS}_{m} + \gamma_{6}*\text{WD}_{m} + \sum_{s}^{}{{\delta_{s}*T}_{s,m} + \sum_{p}^{}{\lambda_{p}*T_{p,m}}} + \mu*T_{nox,m}*T_{NH3,m} + \nu*T_{SO2,m}*T_{NH3,m} + \xi*T_{SO2,m}*T_{NOx,m} + {\sum_{s}^{}{{\theta_{s}*T_{s,m}*WS}_{m}*WD_{m}} + \phi}_{m} + \varepsilon_{m}$$ {#eq-monthconc}
```

**eq-pm** — adjustment/detail. Label: `{#eq-pm}`. Source: `06_Air_pollution.qmd` lines 840–840, heading "Elastic net model".  


```tex
$$PM2.5 = \sum_{m}^{}{\varphi_{m}*PM{2.5}_{m}}$$ {#eq-pm}
```

**eq-pm2** — adjustment/detail. Label: `{#eq-pm2}`. Source: `06_Air_pollution.qmd` lines 844–844, heading "Elastic net model".  


```tex
$$PM2.5 = \alpha + \sum_{s,p}^{}{\beta_{s,p}*\overline{E_{s,p}}} + \gamma_{1}*\overline{\text{PPT}} + \gamma_{2}*\overline{\text{TMIN}} + \gamma_{3}*\overline{\text{TMAX}} + \gamma_{4}*\overline{\text{VPD}} + \gamma_{5}*\overline{\text{WS}} + \gamma_{6}*\overline{\text{WD}} + \sum_{s}^{}{{\delta_{s}*T}_{s}*\sum_{m}^{}{\varphi_{m}*w_{s,m}} + \sum_{p}^{}{\lambda_{p}*T_{p}}}*\sum_{m}^{}{\varphi_{m}*w_{p,m}} + \mu*T_{\text{NOx}}*T_{NH3}*\sum_{m}^{}{\varphi_{m}*w_{NOx,m}*w_{NH3,m}} + \nu*T_{SO2}*T_{NH3}*\sum_{m}^{}{\varphi_{m}*w_{SO2,m}*w_{NH3,m}} + \xi*T_{SO2}*T_{\text{NOx}}*\sum_{m}^{}{\varphi_{m}*w_{SO2,m}*w_{NOx,m}} + \sum_{s}^{}{\theta_{s}*T_{s}*\sum_{m}^{}{\varphi_{m}*w_{s,m}*WS_{m}*WD_{m}}} + \overline{\phi} + \varepsilon_{m}$$ {#eq-pm2}
```

**eq-weather** — adjustment/detail. Label: `{#eq-weather}`. Source: `06_Air_pollution.qmd` lines 879–879, heading "Elastic net model".  


```tex
$${Weather = \gamma}_{1}*\overline{\text{PPT}} + \gamma_{2}*\overline{\text{TMIN}} + \gamma_{3}*\overline{\text{TMAX}} + \gamma_{4}*\overline{\text{VPD}} + \gamma_{5}*\overline{\text{WS}} + \gamma_{6}*\overline{\text{WD}}$$ {#eq-weather}
```

**eq-deltas** — adjustment/detail. Label: `{#eq-deltas}`. Source: `06_Air_pollution.qmd` lines 886–886, heading "Elastic net model".  


```tex
$$\delta_{s}^{'} = \delta_{s}*\sum_{m}^{}{\varphi_{m}*w_{s,m}}$${#eq-deltas}
```

**eq-lamdap** — adjustment/detail. Label: `{#eq-lamdap}`. Source: `06_Air_pollution.qmd` lines 887–887, heading "Elastic net model".  


```tex
$$\lambda_{p}^{'} = \lambda_{p}*\sum_{m}^{}{\varphi_{m}*w_{p,m}}$${#eq-lamdap}
```

**eq-mua** — adjustment/detail. Label: `{#eq-mua}`. Source: `06_Air_pollution.qmd` lines 888–888, heading "Elastic net model".  


```tex
$$\mu' = \mu*\sum_{m}^{}{\varphi_{m}*w_{NOx,m}*w_{NH3,m}}$${#eq-mua}
```

**eq-nua** — adjustment/detail. Label: `{#eq-nua}`. Source: `06_Air_pollution.qmd` lines 889–889, heading "Elastic net model".  


```tex
$$\nu' = \nu*\sum_{m}^{}{\varphi_{m}*w_{SO2,m}*w_{NH3,m}}$${#eq-nua}
```

**eq-xia** — adjustment/detail. Label: `{#eq-xia}`. Source: `06_Air_pollution.qmd` lines 890–890, heading "Elastic net model".  


```tex
$$\xi' = \xi*\sum_{m}^{}{\varphi_{m}*w_{SO2,m}*w_{NOx,m}}$${#eq-xia}
```

**eq-thetas** — adjustment/detail. Label: `{#eq-thetas}`. Source: `06_Air_pollution.qmd` lines 891–891, heading "Elastic net model".  


```tex
$${{\theta^{'}}_{s} = \theta}_{s}*\sum_{m}^{}{\varphi_{m}*w_{s,m}*WS_{m}*WD_{m}}$${#eq-thetas}
```

**eq-beta1** — adjustment/detail. Label: `{#eq-beta1}`. Source: `06_Air_pollution.qmd` lines 892–892, heading "Elastic net model".  


```tex
$${\beta'}_{s,p} = \beta_{s,p}/12$${#eq-beta1}
```

**eq-beta2** — adjustment/detail. Label: `{#eq-beta2}`. Source: `06_Air_pollution.qmd` lines 893–893, heading "Elastic net model".  


```tex
$${\beta''}_{s,p} = {(\beta'}_{s,p}{+ \lambda'}_{p})$${#eq-beta2}
```

**eq-pmbis** — core (Option 3). Label: `{#eq-pmbis}`. Source: `06_Air_pollution.qmd` lines 897–897, heading "Elastic net model".  
Annual PM2.5 used in CPAT.

```tex
$$PM2.5 = \alpha + Weather + \overline{\phi} + \sum_{s,p}^{}{\beta_{s,p}*\overline{E_{s,p}}} + \sum_{s}^{}{{{\delta'}_{s}*T}_{s} + \sum_{p}^{}{{\lambda'}_{p}*T_{p}}} + \mu'*T_{\text{NOx}}*T_{NH3} + \nu'*T_{SO2}*T_{NH3} + \xi'*T_{SO2}*T_{\text{NOx}} + \sum_{s}^{}{{\theta'}_{s}*T_{s}} + \varepsilon_{m}$${#eq-pmbis}
```

**eq-pms** — adjustment/detail. Label: `{#eq-pms}`. Source: `06_Air_pollution.qmd` lines 902–902, heading "Elastic net model".  


```tex
$$\text{PM}{2.5}_{s} = \sum_{p}^{}{{\beta'}_{s,p}*T_{p,s}} + {{\delta'}_{s}*T}_{s} + \sum_{p}^{}{{\lambda'}_{p}*T_{p,s}} + \mu'*T_{NOx,s}*T_{NH3,s} + \nu'*T_{SO2,s}*T_{NH3,s} + \xi'*T_{SO2,s}*T_{NOx,s} + {\theta'}_{s}*T_{s}$${#eq-pms}
```

**eq-pmsbis** — adjustment/detail. Label: `{#eq-pmsbis}`. Source: `06_Air_pollution.qmd` lines 907–907, heading "Elastic net model".  


```tex
$$\text{PM}{2.5}_{s} = \sum_{p}^{}{{(\beta'}_{s,p}{+ \lambda'}_{p})*T_{p,s}} + {({\delta^{'}}_{s} + {\theta^{'}}_{s})*T}_{s} + \mu'*T_{NOx,s}*T_{NH3,s} + \nu'*T_{SO2,s}*T_{NH3,s} + \xi'*T_{SO2,s}*T_{NOx,s}$${#eq-pmsbis}
```

**eq-pmsagain** — core (Option 3). Label: `{#eq-pmsagain}`. Source: `06_Air_pollution.qmd` lines 913–913, heading "Elastic net model".  
Sector contribution.

```tex
$$\text{PM}{2.5}_{s} = \sum_{p}^{}{{\beta''}_{s,p}*T_{p,s}} + {{\delta''}_{s}*T}_{s} + \mu'*T_{NOx,s}*T_{NH3,s} + \nu'*T_{SO2,s}*T_{NH3,s} + \xi'*T_{SO2,s}*T_{NOx,s}$${#eq-pmsagain}
```

**eq-term** — adjustment/detail. Label: `{#eq-term}`. Source: `06_Air_pollution.qmd` lines 925–925, heading "Elastic net model".  


```tex
$$\mu'*(T_{\text{NOx}}*T_{NH3} - \sum_{s}^{}{T_{NOx,s}*T_{NH3,s}}) + \nu'*{(T}_{SO2}*T_{NH3} - \sum_{s}^{}{T_{SO2,s}*T_{NH3,s}}) + \xi'*(T_{SO2}*T_{\text{NOx}} - \sum_{s}^{}{T_{SO2,s}*T_{NOx,s}})$${#eq-term}
```

**eq-pmm** — adjustment/detail (OLS shares). Label: `{#eq-pmm}`. Source: `06_Air_pollution.qmd` lines 935–935, heading "OLS model".  


```tex
$$P{M2.5}_{m} = \alpha + \sum_{s}^{}{\delta_{s}*\widehat{T_{s,m}}} + \gamma_{1}*PPT_{m} + \gamma_{2}*TMIN_{m} + \gamma_{3}*TMAX_{m} + \gamma_{4}*\text{VPD}_{m} + \gamma_{5}*\text{WS}_{m} + \gamma_{6}*\text{WD}_{m} + \varepsilon_{m}$${#eq-pmm}
```

**eq-espm** — adjustment/detail. Label: `{#eq-espm}`. Source: `06_Air_pollution.qmd` lines 948–948, heading "OLS model".  


```tex
$$\widehat{E_{s,p,m}} = \frac{E_{s,p,m} - \text{Min}_{s,p}}{\text{Max}_{s,p} - \text{Min}_{s,p}}$${#eq-espm}
```

**eq-tsm** — adjustment/detail. Label: `{#eq-tsm}`. Source: `06_Air_pollution.qmd` lines 962–962, heading "OLS model".  


```tex
$$\widehat{T_{s,m}} = \sum_{p}^{}\widehat{E_{s,p,m}}$${#eq-tsm}
```

**eq-if** — core (Option 4). Label: `{#eq-if}`. Source: `06_Air_pollution.qmd` lines 981–981, heading "Option 4: Intake fractions {#sec-if}".  
Intake fraction definition.

```tex
$$iF = \frac{\sum_{i = 1}^{N}{P_{i}*\mathrm{\Delta}C_{i}*BR}}{Q}$$ {#eq-if}
```

**eq-sumi** — core (Option 4). Label: `{#eq-sumi}`. Source: `06_Air_pollution.qmd` lines 998–998, heading "Option 4: Intake fractions {#sec-if}".  


```tex
$$\sum_{i = 1}^{N}{P_{i}*\mathrm{\Delta}C_{i}} = \frac{iF*Q}{\text{BR}}$${#eq-sumi}
```

**eq-ifsec** — adjustment/detail. Label: `{#eq-ifsec}`. Source: `06_Air_pollution.qmd` lines 1028–1028, heading "Intake fractions for ground level, low and high stack emission sources".  


```tex
$$\text{iF}_{\text{secondary\ pollutant}} = \frac{\text{iF}_{PM2.5,\ Apte}}{\text{iF}_{PM2.5,\ Humbert}}*\text{iF}_{\text{secondary\ Humbert}}\ $$ {#eq-ifsec}
```

**eq-ifhl** — adjustment/detail. Label: `{#eq-ifhl}`. Source: `06_Air_pollution.qmd` lines 1048–1048, heading "Intake fractions for ground level, low and high stack emission sources".  


```tex
$$\text{iF}_{high/low} = \text{iF}_{PM2.5,\ Fantke}*\frac{\text{iF}_{PM2.5,\ \ Humbert,\ high/low}}{\text{iF}_{PM2.5,\ Humbert,\ \ groundlevel}}$${#eq-ifhl}
```

**eq-ifeach** — adjustment/detail. Label: `{#eq-ifeach}`. Source: `06_Air_pollution.qmd` lines 1199–1199, heading "Intake fractions from power plants".  


```tex
$${iF}_{p,\ j,\ l} = \sum_{i = 1}^{4}{\beta_{i,j}*{P\text{op}}_{i,\ l} + \beta_{5,\ j}*{P\text{recipitation}}_{p}}$$ {#eq-ifeach}
```

**eq-cm** — core (Option 4). Label: `{#eq-cm}`. Source: `06_Air_pollution.qmd` lines 1237–1237, heading "Intake fractions from power plants".  
Concentration per tonne/yr.

```tex
$$CM = \frac{\Delta C\lbrack\frac{\text{μg}}{m3}\rbrack}{1\ \lbrack tonne/year\rbrack} = \frac{iF\ (ppm)}{\text{BR}\left( \frac{m3}{d} \right)*365\left( \frac{d}{\text{year}} \right)*Pop\ (capita)}*10^6$$ {#eq-cm}
```

**eq-pspt** — core (Option 5). Label: `{#eq-pspt}`. Source: `06_Air_pollution.qmd` lines 1256–1256, heading "Option 5: Machine learning {#sec-machlearn}".  


```tex
$$P_{s,p,t} = \ \left( \frac{\text{Emission}s_{s,p,t}}{\text{Emissions}_{s,p,t0}} - 1 \right)*100$$ {#eq-pspt}
```

**eq-cpspt** — core (Option 5). Label: `{#eq-cpspt}`. Source: `06_Air_pollution.qmd` lines 1262–1278, heading "Option 5: Machine learning {#sec-machlearn}".  
Piecewise-linear emulator.

```tex
$$
C\ (P_{s,p,t}) = 
\left\{\begin{matrix} \\\\
\text{if } P_{s,p,t} < -100, \ a_{-100} \\
\text{if } -100 \le P_{s,p,t} < -80,\ \ \ a_{- 100} + b_{- 100}*(P_{s,p,t} - ( - 100)) \\
\text{if } - 80 \leq P_{s,p,t} < - 60,\ \ \ a_{- 80} + b_{- 80}*(P_{s,p,t} - ( - 80)) \\
\text{if } - 60 \leq P_{s,p,t} < - 40,\ \ \ a_{- 60} + b_{- 60}*(P_{s,p,t} - ( - 60)) \\
\text{if } - 40 \leq P_{s,p,t} < - 20,\ \ \ a_{- 40} + b_{- 40}*(P_{s,p,t} - \left( - 40 \right)) \\
\text{if } - 20 \leq P_{s,p,t} < 0,\ \ \ a_{- 20} + b_{- 20}*(P_{s,p,t} - \left( - 20 \right)) \\
\text{if }\ 0 \leq P_{s,p,t} < 20,\ \ \ a_{0} + b_{0}*(P_{s,p,t} - 0) \\
\text{if }\ 20 \leq P_{s,p,t} < 40,\ \ \ a_{20} + b_{20}*(P_{s,p,t} - 20) \\
\text{if }\ 40 \leq P_{s,p,t} < 60,\ \ \ a_{40} + b_{40}*(P_{s,p,t} - 40) \\
\text{if }\ 60 \leq P_{s,p,t} < 80,\ \ \ a_{60} + b_{60}*(P_{s,p,t} - 60) \\
\text{if }\ 80 \leq P_{s,p,t} < 100,\ \ \ a_{80} + b_{80}*(P_{s,p,t} - 80) \\
\text{if }P_{s,p,t} > 100,\ \ \ a_{100} + b_{100}*(P_{s,p,t} - 100) \\
\end{matrix} \right.
$${#eq-cpspt}
```

**eq-cspto** — core (Option 5). Label: `{#eq-cspto}`. Source: `06_Air_pollution.qmd` lines 1285–1285, heading "Option 5: Machine learning {#sec-machlearn}".  


```tex
$$C_{s,p,t_0} = {- C}_{s,p,t}(P_{s,p,t} = - 100)$$ {#eq-cspto}
```

**eq-cspt2** — core (Option 5). Label: `{#eq-cspt2}`. Source: `06_Air_pollution.qmd` lines 1290–1290, heading "Option 5: Machine learning {#sec-machlearn}".  


```tex
$$C_{s,p,t} = C_{s,p,t}\left( P_{s,p,t} \right) - BaselineConcentration + C_{s,p,t_0}$$ {#eq-cspt2}
```

**eq-obsc** — core. Label: `{#eq-obsc}`. Source: `06_Air_pollution.qmd` lines 1321–1321, heading "Modeled and total ambient pollution".  
Calibrate unmodeled background C0 in base year.

```tex
$$\text{Observed}C_{t_0} = Modeled\ C_{t_0} + C_{0}$${#eq-obsc}
```

**eq-ambientc** — core. Label: `{#eq-ambientc}`. Source: `06_Air_pollution.qmd` lines 1326–1326, heading "Modeled and total ambient pollution".  


```tex
$$\text{Ambient}C_{t} = Modeled\ C_{t} + C_{0}$${#eq-ambientc}
```

**eq-rr** — adjustment/detail (definition). Label: `{#eq-rr}`. Source: `06_Air_pollution.qmd` lines 1412–1412, heading "Definitions of key technical terms".  


```tex
$$\text{RR} = \frac{y_{0}}{y_{c}}$${#eq-rr}
```

**eq-rroap** — core. Label: `{#eq-rroap}`. Source: `06_Air_pollution.qmd` lines 1542–1542, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$$\text{RR}_{\text{OAP}} = MRBRT(z = \text{Exp}_{\text{OAP}})/MRBRT(z = TMREL)$${#eq-rroap}
```

**eq-rrhap** — core. Label: `{#eq-rrhap}`. Source: `06_Air_pollution.qmd` lines 1547–1547, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$$\text{RR}_{\text{HAP}} = MRBRT(z = \text{Exp}_{\text{OAP}} + \text{Exp}_{\text{HAP}})/\ MRBRT(z = TMREL)$${#eq-rrhap}
```

**eq-rrpm** — core. Label: `{#eq-rrpm}`. Source: `06_Air_pollution.qmd` lines 1553–1553, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$$RR_{\text{PM}} = RR_{\text{OAP}}*\left( 1 - p_{\text{HAP}} \right) + RR_{\text{HAP}}*p_{\text{HAP}}$${#eq-rrpm}
```

**eq-pafpm** — core. Label: `{#eq-pafpm}`. Source: `06_Air_pollution.qmd` lines 1555–1555, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$${PAF}_{\text{PM}} = 1 - 1/RR_{\text{PM}}$${#eq-pafpm}
```

**eq-pafoap** — core. Label: `{#eq-pafoap}`. Source: `06_Air_pollution.qmd` lines 1560–1560, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$$\text{PA}F_{\text{OAP}} = \frac{\text{Exp}_{\text{OAP}}}{\text{Exp}_{\text{OAP}} + p_{\text{HAP}}*\text{Exp}_{\text{HAP}}}*\text{PAF}_{\text{PM}}$${#eq-pafoap}
```

**eq-pafhap** — core. Label: `{#eq-pafhap}`. Source: `06_Air_pollution.qmd` lines 1562–1562, heading "Joint ambient and household air pollution (@murray2020global)".  


```tex
$$\text{PA}F_{\text{HAP}} = \frac{{p_{\text{HAP}}*Exp}_{\text{HAP}}}{\text{Exp}_{\text{OAP}} + {p_{\text{HAP}}*Exp}_{\text{HAP}}}*\text{PAF}_{\text{PM}}$${#eq-pafhap}
```

**eq-daly** — core. Label: `{#eq-daly}`. Source: `06_Air_pollution.qmd` lines 1617–1617, heading "Health outcomes in CPAT {#sec-healthout}".  


```tex
$$\text{DALY}_{c,s,a,t} = \text{YLL}_{c,s,\ a,t} + \text{YLD}_{c,s,a,t}$${#eq-daly}
```

**eq-yll** — core. Label: `{#eq-yll}`. Source: `06_Air_pollution.qmd` lines 1623–1623, heading "Health outcomes in CPAT {#sec-healthout}".  


```tex
$$\text{YLL}_{c,s,\ a,t} = {\text{Number}\ \text{of}\ \text{deaths}}_{c,s,a,t}*L_{s,a}$${#eq-yll}
```

**eq-yld** — core. Label: `{#eq-yld}`. Source: `06_Air_pollution.qmd` lines 1633–1633, heading "Health outcomes in CPAT {#sec-healthout}".  


```tex
$$\text{YLD}_{c,s,a,t} = P_{c,s,a,t}*\text{DW}_{c,s,a}$${#eq-yld}
```

**eq-relrisk** — core (ozone). Label: `{#eq-relrisk}`. Source: `06_Air_pollution.qmd` lines 1655–1655, heading "Ozone air pollution".  


```tex
$$RR = e^{\beta*{\mathrm{\Delta}C}_{O3}}$${#eq-relrisk}
```

**eq-pafbis** — core (ozone). Label: `{#eq-pafbis}`. Source: `06_Air_pollution.qmd` lines 1657–1657, heading "Ozone air pollution".  


```tex
$$PAF = 1 - e^{- \beta*{\mathrm{\Delta}C}_{O3}}$${#eq-pafbis}
```

**eq-pafsum** — adjustment/detail. Label: `{#eq-pafsum}`. Source: `06_Air_pollution.qmd` lines 1671–1671, heading "Multiple risks factors".  


```tex
$$\text{PA}F_{1..i} = 1 - \prod_{i = 1}^{n}{(1 - PAF_{i})}$$ {#eq-pafsum}
```

**eq-pafmp** — adjustment/detail. Label: `{#eq-pafmp}`. Source: `06_Air_pollution.qmd` lines 1680–1680, heading "Multiple risks factors".  


```tex
$$\text{PA}F_{MP2.5 - O3 - COPD\ } = 1 - \left( 1 - PAF_{PM2.5} \right)*(1 - PAF_{O3})$$ {#eq-pafmp}
```

**eq-corr** — adjustment/detail. Label: `{#eq-corr}`. Source: `06_Air_pollution.qmd` lines 1688–1688, heading "Multiple risks factors".  


```tex
$$\text{Cor}r_{\text{factor}} = \frac{\text{PA}F_{MP2.5 - O3 - COPD\ }}{\text{PA}F_{PM2.5} + PAF_{O3}}$${#eq-corr}
```

**eq-prophh** — core (biomass leakage interface). Label: `{#eq-prophh}`. Source: `06_Air_pollution.qmd` lines 1785–1785, heading "Leakage to biomass".  


```tex
$$\text{ProportionHH}_{\text{carbon\ price}} = \text{ProportionHH}_{\text{baseline}}*(1 + Leakage*F_{\text{pro}p_{\text{HH}}})$${#eq-prophh}
```

**eq-prophhadj** — core. Label: `{#eq-prophhadj}`. Source: `06_Air_pollution.qmd` lines 1787–1787, heading "Leakage to biomass".  


```tex
$${F\_ prop\_ HH}_{\text{adjusted}} = \left( \frac{\text{MaxPropHH}}{\text{ProportionHH}_{\text{baseline}}} - 1 \right)*\frac{1}{\text{Leakage}}$${#eq-prophhadj}
```

**eq-prophhif** — core. Label: `{#eq-prophhif}`. Source: `06_Air_pollution.qmd` lines 1789–1792, heading "Leakage to biomass".  


```tex
$$F\_ prop\_ HH = \left\{ \begin{matrix}
\text{if }\text{ProportionHH}_{\text{carbon price}} > Max\ then{\ F\_ prop\_ HH}_{\text{adjusted}} \\
\text{else }\text{ProportionHH}_{\text{carbon price}} \\
\end{matrix} \right.\ $${#eq-prophhif}
```

**eq-logfunc** — adjustment/detail (post-neonatal). Label: `{#eq-logfunc}`. Source: `06_Air_pollution.qmd` lines 1802–1802, heading "Post neonatal mortality (@woodruff2006fine)".  


```tex
$$\left( 1 - \left( \frac{1}{\left( 1 - Incidence \right)*EXP\left( \beta*DeltaQ \right) + Incidence} \right) \right)*Incidence*POP$${#eq-logfunc}
```

**eq-rrappro** — adjustment/detail (depression). Label: `{#eq-rrappro}`. Source: `06_Air_pollution.qmd` lines 1819–1819, heading "Depressive disorders".  


```tex
$$RR \approx \text{OR}_{10}*\frac{{PM2.5}_{\text{current}} - {PM2.5}_{\text{counterfactual}}}{10}$${#eq-rrappro}
```

**eq-pafe** — core (working days lost). Label: `{#eq-pafe}`. Source: `06_Air_pollution.qmd` lines 1902–1902, heading "Working days lost".  


```tex
$$PAF = 1 - e^{- \beta*\mathrm{\Delta}C}$${#eq-pafe}
```

**eq-totnblost** — core. Label: `{#eq-totnblost}`. Source: `06_Air_pollution.qmd` lines 1904–1904, heading "Working days lost".  


```tex
$$\text{WDL}_{\text{pollution}} = \text{Pop}_{15\ to\ 64}*\text{Per\ person\ WDL}_{\text{baseline}}*(1 - e^{- \beta*C\ baseline})$${#eq-totnblost}
```

**eq-dailywage** — adjustment/detail. Label: `{#eq-dailywage}`. Source: `06_Air_pollution.qmd` lines 1913–1913, heading "Working days lost".  


```tex
$$Daily\ wage = \frac{GDP*\alpha}{N{^\circ}\ of\ persons\ employed}*\frac{1}{N{^\circ}\ of\ days}$${#eq-dailywage}
```

**eq-wij** — core (output losses). Label: `{#eq-wij}`. Source: `06_Air_pollution.qmd` lines 1932–1932, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$W_{\text{ij}} = \left( \frac{L_{\text{ij}}}{N_{\text{ij}}} \right)\left( \frac{\text{αY}_{i}}{L_{i}} \right)$${#eq-wij}
```

**eq-wpshare** — core. Label: `{#eq-wpshare}`. Source: `06_Air_pollution.qmd` lines 1954–1954, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$W_{p} = \left( \frac{L_{p}}{N_{p}} \right)\left( \frac{\text{αY}_{p}}{L_{p}} \right) = \ \frac{\text{αY}_{p}}{N_{p}}$${#eq-wpshare}
```

**eq-wif17** — adjustment/detail. Label: `{#eq-wif17}`. Source: `06_Air_pollution.qmd` lines 1962–1962, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$${W'}_{ij2017} = \left( \frac{L_{\text{ij}}}{N_{\text{ij}}} \right)\left( \frac{\text{αY}_{i}}{L_{i}} \right) + hp\left( 1 - \frac{L_{\text{ij}}}{N_{\text{ij}}} \right)\left( \frac{\text{αY}_{i}}{L_{i}} \right)$${#eq-wif17}
```

**eq-pvij** — core. Label: `{#eq-pvij}`. Source: `06_Air_pollution.qmd` lines 1970–1970, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$\text{PV}_{\text{ij}} = \sum_{a = j}^{84}\pi_{ij,t}\left\lbrack \left( \frac{L_{\text{it}}}{N_{\text{it}}} \right)\left( \frac{\text{αY}_{i}}{L_{i}} \right) + hp\left( 1 - \frac{L_{\text{it}}}{N_{\text{it}}} \right)\left( \frac{\text{αY}_{i}}{L_{i}} \right) \right\rbrack\left( \frac{1 + g}{1 + r} \right)^{t - j}$${#eq-pvij}
```

**eq-pvj** — core. Label: `{#eq-pvj}`. Source: `06_Air_pollution.qmd` lines 1990–1990, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$\text{PV}_{j} = W*\sum_{t = j}^{64}\pi_{j,t}*\left( \frac{1 + g}{1 + r} \right)^{t - j}$${#eq-pvj}
```

**eq-pvjw** — core. Label: `{#eq-pvjw}`. Source: `06_Air_pollution.qmd` lines 1994–1994, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$\text{PV}_{j}/W = \sum_{t = j}^{64}\pi_{j,t}*\left( \frac{1 + g}{1 + r} \right)^{t - j}$${#eq-pvjw}
```

**eq-totoutplost** — core. Label: `{#eq-totoutplost}`. Source: `06_Air_pollution.qmd` lines 1999–1999, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$TotalOutputLost = \sum_{j}^{}{\text{PV}_{\text{ij}}D_{\text{ij}}}$${#eq-totoutplost}
```

**eq-mij** — core. Label: `{#eq-mij}`. Source: `06_Air_pollution.qmd` lines 2012–2012, heading "Market output losses {#sec-marketoutputlosses}".  


```tex
$$M\text{ij}\  = \ \ Wij*\text{YLD}\text{ij}$${#eq-mij}
```

**eq-dprob** — adjustment/detail. Label: `{#eq-dprob}`. Source: `06_Air_pollution.qmd` lines 2038–2038, heading "CPAT operationalization".  


```tex
$$d_{25,29} = d_{25} + d_{26} + d_{27} + d_{28} + d_{29}$${#eq-dprob}
```

**eq-dsimple** — adjustment/detail. Label: `{#eq-dsimple}`. Source: `06_Air_pollution.qmd` lines 2045–2045, heading "CPAT operationalization".  


```tex
$$d_{25} = d_{26} = d_{27} = d_{28} = d_{29} = \frac{d_{25,29}}{5}$${#eq-dsimple}
```

**eq-survprob** — adjustment/detail. Label: `{#eq-survprob}`. Source: `06_Air_pollution.qmd` lines 2050–2050, heading "CPAT operationalization".  


```tex
$$\pi_{25,29} = \left( 1 - \frac{d_{25,29}}{5} \right) = \pi_{25} = \pi_{26} = \pi_{27} = \pi_{28} = \pi_{29}$${#eq-survprob}
```

**eq-pvw** — adjustment/detail. Label: `{#eq-pvw}`. Source: `06_Air_pollution.qmd` lines 2054–2054, heading "CPAT operationalization".  


```tex
$$\frac{\text{PV}_{25 - 29}}{W} = \pi_{25,29}*\sum_{k = 0}^{2}a^{k} + \pi_{25,34}*\sum_{k = 3}^{7}{a^{k} + \ldots + \pi_{25,64}*\sum_{k = 43}^{47}a^{k}}$${#eq-pvw}
```

**eq-sumk** — adjustment/detail. Label: `{#eq-sumk}`. Source: `06_Air_pollution.qmd` lines 2061–2061, heading "CPAT operationalization".  


```tex
$$\sum_{k = 0}^{n}{a^{k} = \frac{1 - a^{n + 1}}{1 - a}}$${#eq-sumk}
```

**eq-sumkm** — adjustment/detail. Label: `{#eq-sumkm}`. Source: `06_Air_pollution.qmd` lines 2066–2066, heading "CPAT operationalization".  


```tex
$$\sum_{k = m}^{n}{a^{k} = \sum_{k = 0}^{n}a^{k} - \sum_{k = 0}^{m}a^{k} = \frac{1 - a^{n + 1}}{1 - a} - \frac{1 - a^{m + 1}}{1 - a}}$${#eq-sumkm}
```

**eq-bod** — core (health expenditure). Label: `{#eq-bod}`. Source: `06_Air_pollution.qmd` lines 2083–2083, heading "Health expenditure".  


```tex
$$\% BoD_{d,c,t} = \frac{\text{DALY}s_{d,c,t}}{\text{TotalDALY}s_{c,t}}$${#eq-bod}
```

**eq-heap** — core. Label: `{#eq-heap}`. Source: `06_Air_pollution.qmd` lines 2088–2088, heading "Health expenditure".  


```tex
$$\text{HEAP}_{c,t} = \sum_{d}^{}{\% BoD_{d,c,t}*PAF_{d,t}*THE_{c,t}}$${#eq-heap}
```

**eq-vslc** — core (VSL). Label: `{#eq-vslc}`. Source: `06_Air_pollution.qmd` lines 2116–2116, heading "Value of the statistical life".  


```tex
$$VSL_{c} = VSL_{OECD,2005}*\left( \frac{Y_{c}}{Y_{OECD,2005}} \right)^{b}*\left( 1 + \%\mathrm{\Delta}P + \%\mathrm{\Delta}Y \right)^{b}$${#eq-vslc}
```

**eq-vsloecd** — core. Label: `{#eq-vsloecd}`. Source: `06_Air_pollution.qmd` lines 2135–2135, heading "Value of the statistical life".  


```tex
$$VSL_{OECD,\ t,2011PPP} = VSL_{OECD,2005}*\left( \frac{Y_{OECD,t}}{Y_{OECD,2005}} \right)^{0.8}*\left( 1 + \%\mathrm{\Delta}P_{2005,2011} \right)^{0.8}$${#eq-vsloecd}
```

**eq-vsloecdbis** — core. Label: `{#eq-vsloecdbis}`. Source: `06_Air_pollution.qmd` lines 2140–2140, heading "Value of the statistical life".  


```tex
$$VSL_{OECD,\ 2014} = VSL_{OECD,\ 2014}*\left( \frac{Y_{c,2014}}{Y_{OECD,2014}} \right)^{b}$${#eq-vsloecdbis}
```

**eq-vslct** — core. Label: `{#eq-vslct}`. Source: `06_Air_pollution.qmd` lines 2145–2145, heading "Value of the statistical life".  


```tex
$$VSL_{c,\ t} = VSL_{c,2014}*\left( \frac{Y_{c,t}}{Y_{c,\ 2014}} \right)^{b}$${#eq-vslct}
```

**eq-congvkm** — core (travel time, used by Transport). Label: `{#eq-congvkm}`. Source: `06_Air_pollution.qmd` lines 2253–2253, heading "Travel time saved".  


```tex
$$\text{CongestionT}T_{2019}\lbrack min/vehkm\rbrack = \frac{\text{AccumulatedTravelTim}e_{2019}\ \lbrack min\rbrack}{\text{TotalVeh}\text{KM}_{2019}\lbrack vehkm\rbrack}$${#eq-congvkm}
```

**eq-freeflow** — core. Label: `{#eq-freeflow}`. Source: `06_Air_pollution.qmd` lines 2262–2262, heading "Travel time saved".  


```tex
$$FreeFlowTT\lbrack\frac{\min}{\text{vehkm}}\rbrack = \frac{\text{CongestionT}T_{2019}\ \lbrack\frac{\min}{\text{vehkm}}\rbrack}{(1 + \frac{CI_{2019}}{100})}$${#eq-freeflow}
```

**eq-travtime** — core. Label: `{#eq-travtime}`. Source: `06_Air_pollution.qmd` lines 2276–2276, heading "Travel time saved".  


```tex
$$\text{Travel time}_{t} = \left( 1 + \frac{CI_{t}}{100} \right)*FreeFlowTT\left\lbrack \frac{\min}{\text{vehkm}} \right\rbrack*VehKm\ per\ capita\left\lbrack \frac{\text{vehkm}}{\text{year}} \right\rbrack*UrbanPopulation_{15 + ,t}$${#eq-travtime}
```

**eq-msum** — core (morbidity valuation). Label: `{#eq-msum}`. Source: `06_Air_pollution.qmd` lines 2310–2310, heading "Value of morbidity using years lived with disabilities (YLDs) {#sec-valuemorbidity}".  


```tex
$$M = \ \sum_{c = 1}^{n}{YLD_{c}*\frac{365}{DW_{c}}}$${#eq-msum}
```

**eq-cc** — core. Label: `{#eq-cc}`. Source: `06_Air_pollution.qmd` lines 2325–2325, heading "Value of morbidity using years lived with disabilities (YLDs) {#sec-valuemorbidity}".  


```tex
$$c_{c} = w*\frac{DW_{c}}{D}$${#eq-cc}
```

**eq-costmorbidity** — core. Label: `{#eq-costmorbidity}`. Source: `06_Air_pollution.qmd` lines 2333–2333, heading "Value of morbidity using years lived with disabilities (YLDs) {#sec-valuemorbidity}".  


```tex
$$Cost\ of\ Morbidity = \ \sum_{i = 1}^{n}{c_{c}*M}$${#eq-costmorbidity}
```

**eq-rractual** — core (RR interpolation). Label: `{#eq-rractual}`. Source: `06_Air_pollution.qmd` lines 2590–2590, heading "Relative Risk IER GBD 2019".  


```tex
$$\text{RR}_{\text{actual}} = \text{RR}_{\text{high}} - \frac{\text{RR}_{\text{high}} - \text{RR}_{\text{low}}}{\text{PM}_{\text{high}} - \text{PM}_{\text{low}}}*(\text{PM}_{\text{high}} - \text{PM}_{\text{actual}})$${#eq-rractual}
```

**eq-rrhap0** — core. Label: `{#eq-rrhap0}`. Source: `06_Air_pollution.qmd` lines 2601–2601, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  


```tex
$$\text{RR}_{\text{HAP}}^{0} = \frac{\lambda_{\text{HAP}}^{0}}{\lambda_{\text{TMREL}}}$${#eq-rrhap0}
```

**eq-rraop0** — core. Label: `{#eq-rraop0}`. Source: `06_Air_pollution.qmd` lines 2610–2610, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  


```tex
$$\text{RR}_{\text{OAP}}^{0} = \frac{\lambda_{\text{OAP}}^{0}}{\lambda_{\text{TMREL}}}$${#eq-rraop0}
```

**eq-mpop** — core. Label: `{#eq-mpop}`. Source: `06_Air_pollution.qmd` lines 2615–2615, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  


```tex
$$M_{0} = Population*p_{H}*\lambda_{\text{HAP}}^{0} + Population*{(1 - p}_{H})*\lambda_{\text{OAP}}^{0}$${#eq-mpop}
```

**eq-mpop0** — core. Label: `{#eq-mpop0}`. Source: `06_Air_pollution.qmd` lines 2619–2619, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  


```tex
$$M_{0} = Population*p_{H}*\text{RR}_{\text{HAP}}^{0}*\lambda_{\text{TMREL}} + Population*{(1 - p}_{H})*\text{RR}_{\text{OAP}}^{0}*\lambda_{\text{TMREL}}$${#eq-mpop0}
```

**eq-lambdasolve** — core. Label: `{#eq-lambdasolve}`. Source: `06_Air_pollution.qmd` lines 2625–2625, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  


```tex
$$\lambda_{\text{TMREL}} = \frac{M_{0}}{\text{Population}}*\left( \frac{1}{p_{H}*\text{RR}_{\text{HAP}}^{0} + {(1 - p}_{H})*\text{RR}_{\text{OAP}}^{0}} \right)$${#eq-lambdasolve}
```

**eq-deltamm** — core. Label: `{#eq-deltamm}`. Source: `06_Air_pollution.qmd` lines 2631–2633, heading "Quantification of health effects in CPAT {#sec-quanthealtheff}".  
Change in mortality, baseline vs policy.

```tex
$$
\mathrm{\Delta}M = M_{0}*\left\{ 1 - \left( \frac{p_{H}^{1}*\text{RR}_{\text{HAP}}^{1} + {(1 - p}_{H}^{1})*\text{RR}_{\text{OAP}}^{1}}{p_{H}^{0}*\text{RR}_{\text{HAP}}^{0} + {(1 - p}_{H}^{0})*\text{RR}_{\text{OAP}}^{0}} \right) \right\}
$${#eq-deltamm}
```

**eq-eftonktoe** — adjustment/detail (units). Label: `{#eq-eftonktoe}`. Source: `06_Air_pollution.qmd` lines 2668–2668, heading "Some unit conversions".  


```tex
$$\text{EF }\left\lbrack \frac{\text{ton}}{\text{ktoe}} \right\rbrack = EF\ \left\lbrack \frac{\text{kton}}{\text{PJ}} \right\rbrack*\frac{1\ PJ}{10^{6}\text{GJ}}*\frac{10^{3}\text{ton }}{1\ kton}*\frac{41868\ GJ}{1\ ktoe}$${#eq-eftonktoe}
```

**eq-convertktoevol** — adjustment/detail. Label: `{#eq-convertktoevol}`. Source: `06_Air_pollution.qmd` lines 2672–2672, heading "Some unit conversions".  


```tex
$$1\ ktoe = 1\ ktoe*\frac{1\ Kcal}{1*10^{- 10}\text{ktoe}}*\frac{1}{\text{CalVal}\left\lbrack \frac{\text{kcal}}{\text{kg}} \right\rbrack}*\frac{1}{\text{Dens}\left\lbrack \frac{\text{ton}}{m3} \right\rbrack}*\frac{1\ ton}{10^{3}\text{kg}}$${#eq-convertktoevol}
```

**eq-convertktoem3** — adjustment/detail. Label: `{#eq-convertktoem3}`. Source: `06_Air_pollution.qmd` lines 2676–2676, heading "Some unit conversions".  


```tex
$$Conv\_ ktoe\_ to\_ liter = \frac{1}{\text{CalVal}\left\lbrack \frac{\text{kcal}}{\text{kg}} \right\rbrack*Dens\left\lbrack \frac{\text{ton}}{m3} \right\rbrack}*10^{7}$${#eq-convertktoem3}
```

**eq-convertktoelit** — adjustment/detail. Label: `{#eq-convertktoelit}`. Source: `06_Air_pollution.qmd` lines 2681–2681, heading "Some unit conversions".  


```tex
$$Conv\_ ktoe\_ to\_ liter = \frac{1}{\text{CalVal}\left\lbrack \frac{\text{kcal}}{\text{kg}} \right\rbrack*Dens\left\lbrack \frac{\text{ton}}{m3} \right\rbrack}*10^{10}$${#eq-convertktoelit}
```

**eq-convertktontonlit** — adjustment/detail. Label: `{#eq-convertktontonlit}`. Source: `06_Air_pollution.qmd` lines 2687–2687, heading "Some unit conversions".  


```tex
$$\frac{1\ kton}{\text{PJ}}*\frac{1000\ ton}{1\ kton}*\ \text{CalVal}\left\lbrack \frac{\text{PJ}}{\text{ton}} \right\rbrack*dens\left\lbrack \frac{\text{ton}}{m3} \right\rbrack*\frac{1m3}{1000L}$${#eq-convertktontonlit}
```

**eq-convertktontonlitbis** — adjustment/detail. Label: `{#eq-convertktontonlitbis}`. Source: `06_Air_pollution.qmd` lines 2691–2691, heading "Some unit conversions".  


```tex
$$\frac{1\ kton}{\text{PJ}}*\frac{1000\ ton}{1\ kton}*\ \text{CalVal}\left\lbrack \frac{\text{Kcal}}{\text{kg}} \right\rbrack*1000\frac{\text{kg}}{\text{ton}}*dens\left\lbrack \frac{\text{ton}}{m3} \right\rbrack*\frac{1m3}{1000L}*\frac{1\ PJ}{2.39*10^{11}\text{Kcal}}$${#eq-convertktontonlitbis}
```

**eq-convertktoetoliter** — adjustment/detail. Label: `{#eq-convertktoetoliter}`. Source: `06_Air_pollution.qmd` lines 2695–2695, heading "Some unit conversions".  


```tex
$$1\ ktoe*\frac{1}{\text{CalVal}\left\lbrack \frac{\text{Kcal}}{\text{kg}} \right\rbrack}*\frac{1\ Kcal}{1*10^{- 10}\text{ktoe}}*\frac{1}{\text{dens}\left\lbrack \frac{\text{ton}}{m3} \right\rbrack*1000\frac{\text{kg}}{\text{ton}}*\frac{1m3}{1000\ liter}}$${#eq-convertktoetoliter}
```

Unlabelled in AP: hazard ratio `$$\text{HR} = \frac{H_{0}}{H_{c}}$$`, incidence/prevalence definitions, intake-fraction distance-band case list, attributable burden inline `$AB = PAF*Health\ Outcome$`, survival `\pi_{j} = \prod_{j}^{64}{(1 - \text{Prob\ of\ death}_{j})}` (tbl-parampdty).

### 3.10 Road transport (`07_Road_Transport.qmd`)

**eq-no1** — adjustment/detail (offline estimation). Label: `{#eq-no1}`. Source: `07_Road_Transport.qmd` lines 653–653, heading "Estimation equation".  
Log-log panel regression; β = elasticity.

```tex
$$\ln\left( Y_{\text{ct}} \right) = \alpha + \beta\ln\left( p_{\text{ct}} \right) + \gamma\ X_{\text{ct}} + \mu_{t} + \mu_{c} + \epsilon_{\text{ct}}$$ {#eq-no1}
```

**eq-no2** — adjustment/detail. Label: `{#eq-no2}`. Source: `07_Road_Transport.qmd` lines 677–677, heading "Short-run and long-run estimators".  


```tex
 $$y_{\text{ct}} = \alpha + \beta x_{\text{ct}} + \mu_{c} + \epsilon_{\text{ct}}$$  {#eq-no2}
```

**eq-no3** — adjustment/detail. Label: `{#eq-no3}`. Source: `07_Road_Transport.qmd` lines 685–685, heading "Short-run and long-run estimators".  


```tex
$$y_{\text{ct}} = \alpha + \beta'{\overline{x}}_{c} + \beta''(x_{\text{ct}} - {\overline{x}}_{c}) + \mu_{c} + \epsilon_{\text{ct}}$$ {#eq-no3}
```

**eq-no4** — adjustment/detail. Label: `{#eq-no4}`. Source: `07_Road_Transport.qmd` lines 702–702, heading "Short-run and long-run estimators".  
Between estimator → long-run.

```tex
$${\overline{y}}_{c} = \alpha + \beta'{\overline{x}}_{c} + \mu_{c} + {\overline{\epsilon}}_{c}$$ {#eq-no4}
```

**eq-no5** — adjustment/detail. Label: `{#eq-no5}`. Source: `07_Road_Transport.qmd` lines 711–711, heading "Short-run and long-run estimators".  
Within estimator → short-run.

```tex
$${y_{\text{ct}} - \overline{y}}_{c} = \beta''{(x_{\text{ct}} - \overline{x}}_{c}) + (\epsilon_{\text{ct}} - {\overline{\epsilon}}_{c})$$  {#eq-no5}
```

**eq-no6** — adjustment/detail. Label: `{#eq-no6}`. Source: `07_Road_Transport.qmd` lines 756–756, heading "Country-specific elasticity estimates".  
Interaction terms.

```tex
$$\ln\left( Y_{\text{ct}} \right) = \alpha + \beta_{0}\ln{(p_{\text{ct}})} + \beta_{1}v_{\text{ct}}^{1}\ln{(p_{\text{ct}})} + \beta_{2}v_{\text{ct}}^{2}\ln{(p_{\text{ct}})} + \gamma\ X_{\text{ct}} + \mu_{c} + \ \mu_{t} + \epsilon_{\text{ct}}$$ {#eq-no6}
```

**eq-no7** — core (parameter). Label: `{#eq-no7}`. Source: `07_Road_Transport.qmd` lines 763–763, heading "Country-specific elasticity estimates".  
Country-specific elasticity.

```tex
$${\widehat{\beta}}_{c} = {\widehat{\beta}}_{0} + {\widehat{\beta}}_{1}\overline{v_{c}^{1}} + {\widehat{\beta}}_{2}\overline{v_{c}^{2}}$$ {#eq-no7}
```

**eq-basefor** — core. Label: `{#eq-basefor}`. Source: `07_Road_Transport.qmd` lines 1389–1389, heading "Baseline forecasts".  
Baseline forecast of VKT/congestion/fatalities/road damage.

```tex
$$Y_{t}^{\text{baseline}} = \left( \frac{\text{GDP}_{t}}{\text{GDP}_{t - 1}} - \overline{g^{\text{GDP}}} \right)^{\eta_{\text{GDP}}}{\left( \frac{\text{pop}_{t}}{\text{pop}_{t - 1}} - \overline{g^{\text{pop}}} \right)^{\eta_{\text{pop}}}Y}_{t}^{\text{simple}}$$ {#eq-basefor}
```

**eq-policy** — core. Label: `{#eq-policy}`. Source: `07_Road_Transport.qmd` lines 1447–1447, heading "Policy forecast".  
Policy forecast via fuel-price ratio and elasticity.

```tex
$$Y_{t}^{\text{policy}} = \left( \frac{p^{\text{policy}}}{p^{\text{baseline}}} \right)^{\eta_{p}}Y_{t}^{\text{baseline}}$$ {#eq-policy}
```

## 4. Notation inconsistencies, clashes and apparent errors in the docs

### 4.1 Same letter, different meanings (cross- and within-module)

| Symbol | Meanings found (file > section) |
|---|---|
| `g` | sector grouping index (Mit. Dimensions); electricity generation, GWh (Mit. Power notation; `g_{\text{oc},t}`, `g_{t}`); growth rate in `C_{t} = C_{n}e^{g\left( t - n \right)}` (LCOE Simplification, while text says the rate is τ); the LCOE denominator "$g$ is the discounted power produced"; expenditure category / IO sector (Distribution); per-capita PIT gain `g_{dcy\_ TE}` (Distribution); growth rate of GDP per worker (AP output losses); `\overline{g^{\text{GDP}}}` (Road transport) |
| `G` subscript | `\epsilon_{G,\text{csf}}` / `\epsilon_{G,\text{cE}}` in both power-demand equations — never defined; the fuel equation uses `\epsilon_{Y}` |
| `E` | power demand quantity (Engineer & Elasticity models); sector index for electricity (`F_{\text{cEf},t_{0}}`, `p_{\text{cEt}}`); UNFCCC energy-related sector `u = E`; emission rate `E_{i}(x)` and emissions `E_{s,p,m}` (AP) |
| `P` / `p` | `p` retail price; `P` aggregate retail price (`P_{cf,t}`) and also `P_{t}` in the rebound term; `P` policy scenario subscript; `p` pollutant index; `P_{D}`, `P_{M}` revenues, `P` proportion of additional expenditure, `p_{j}`, `p(T)`, `P_{\text{dcy}}` population (Distribution); `P_{s,p,t}` perturbation, `P_{i}` population, `P_{c,s,a,t}` prevalence, `p` power plant / period, `p_{\text{HAP}}` (AP); `p_{\text{ct}}` pump price (Road) |
| `t` | year (all modules); `t_{\text{fg}}` tax rate/price-increase ratio (Distribution); age in survival sums `\pi_{j,t}` (AP) |
| `Y` | total real GDP (Mitigation); household final demand vector (Distribution sec-5_3_1); outcome `Y_{\text{ct}}` (Road); GDP `Y_{i}` and GDP per capita PPP `Y_{c}` (AP); `Y^{*}` trend GDP and `T/Y` (Multipliers) |
| `f` | fuel index; "each fossil fuel sector, *f* is a vector" in `e_{g} = f\left( I - A \right)^{- 1}` (Distribution); scalar `f_{\text{cy}}` (PIT) |
| `j` | household (Distribution); country (Mitigation Appendix B); bound fuel index (Elasticity model); component PM2.5/O3, pollutant, or age (AP) |
| `i` | bound fuel index and multilogit alternative (Mitigation); investment in `K_{i}`, `H_{i}`; infrastructure category (Distribution); country (Multipliers, Validation); precursor, distance band, state, risk factor (AP) |
| `c` | country; relative cost `c` in `e^{- K.c}` (Engineer logit); cause of death and disease (AP) |
| `s` | sector; sex (AP DALY); shock variable `s_{i,t}` (Multipliers); PIT share `s_{\text{dc}}` (Distribution) |
| `\gamma` | generation shares after PPAs (Engineer); non-fuel cost share (Appendix C old costs); pass-through `\gamma_{g}` (Distribution); control coefficients `\gamma_{h}` (Multipliers); weather coefficients `\gamma_{1..6}` (AP); covariate coefficients (Road) |
| `\Phi` / `\phi` / `\varphi` | `\Phi_{\text{inv}}` new-investment proportion vs `\Phi` production share (Elasticity model); `\phi_{\text{PS}}`, `\phi_{\text{CS}}`, `\phi_{\text{PC}}` phase-out factors vs `\varphi` policy coverage (prices, revenues) vs `\varphi = \frac{W}{Q_{I}}` thermal efficiency (power data; elsewhere `\nu`); AP: `\phi_{m}` monthly fixed effects and `\varphi_{m}` month weights |
| `\delta` | growth rates `\delta_{\text{CT}}`, `\delta_{\text{ETS}}`; `\delta^{\text{add}}` additional share (Elasticity model); time FE `\delta_{t,h}` (Multipliers); `\delta_{s}` (AP) |
| `\lambda` | dispatch share `\lambda_{f}`; time effect `\lambda_{t}` (Validation); `\lambda_{p}` (AP elastic net); `\lambda_{\text{TMREL}}` mortality rate (AP) |
| `\alpha` | autonomous efficiency improvement (Mitigation) vs fixed effects `\alpha_{i}`, `\alpha_{i,h}`; intercepts (Road, AP); labour share of GDP (AP) |
| `\epsilon` vs `\varepsilon` | `\epsilon` = elasticities in Mitigation/Distribution and error terms in Validation/Road; `\varepsilon` = learning-curve experience parameter (power data) and error term (AP, Multipliers text) while Multipliers equation writes `\epsilon_{t,i,h}`; `\text{fϵ}` used as set membership in the reqgen sum |
| `\eta` | elasticities in Road transport (`\eta_{p}`, `\eta_{\text{GDP}}`) and output-gap elasticity `\eta_{\text{YT}}` (Multipliers) — while Mitigation uses `\epsilon` for elasticities |
| `\mu`, `\nu`, `\theta` | `\mu` markup (`mu^{T}`), NSCC elasticity of marginal utility (Appendix E), FE `\mu_{c}`/`\mu_{t}` (Road), interaction coeff. (AP); `\nu` thermal efficiency vs interaction coeff. (AP); `\theta^{PS}_{TCP}` boolean, `\theta_{c}`, `\theta_{\text{pop}}^{y}` (Distribution), `\theta_{s}` (AP) |
| `K` | logit shape parameter, subscripted `K_{\text{dispatch}}`, `K_{i}`, and in text `K_{g}` |
| `A` | abatement-curve coefficient (`A * mf_{t}^{B}`), IO technical-coefficient matrix (Distribution), protection-scheme spending `A_{a}^{y}` (Distribution), SR coefficient `A_{\text{ij}}` (AP); `B` is both abatement exponent and baseline scenario |
| `T` | technoeconomic-model superscript; targeted transfer `T^{y}` and targeted subscript (Distribution); tax revenue `T` (Multipliers); composite emission index `T_{p,m}` (AP); `T_{c}` years per country (Road) |
| `oc` | index prefix scenario-country vs pollutant code `oc` = organic carbon (Appendix F) |
| `M` | baseline mortality `M_{0}`, annual disease days `M`, morbidity output loss `M\text{ij}` (AP); Mitigation-module subscript in `P_{M}^{y}` (Distribution) |
| `r` | discount rate in LCOE (`e^{- \text{rt}}`), discount rate (AP), `r_{\text{cy}}` revenue per person (Distribution) |

### 4.2 Index-order and index-set inconsistencies (Mitigation)

- Declared order `o c u g s f p t`, but many equations deviate: `rev_{ocfgt}`, `F_{ocfgt}`, `ncp_{ocfgt}` (fuel before group) next to `\varphi_{cgft}`; `vat_{cfg,t}` and `vatrate_{cfg,t}` vs `vat_{cgf,t}`; `vat_{c,f,g,t}` (comma-separated); `inv_{ofc,t - 1}`; `tmc_{fct}`; `tex_{P,tcft}`; `rps_{o,cgft}`.
- Sector index `s` vs group `g`: the fuel equation is written in `s` but the text says "$\epsilon_{Y}$ denotes the forward-looking real GDP-elasticity of fuel demand for fuel $f$ in sector $g$"; prices are defined on `g` (`p_{\text{cgft}}`) but the demand equation uses `p_{\text{ocsf},t}` (implicit mapping s→g).
- Inconsistent index sets inside one equation: fuel equation `\left( \frac{1}{1 + \alpha_{\text{sf}}} \right)^{1 + \epsilon_{U,c\text{sf}}}` vs engineer power demand `^{1 + \epsilon_{U,\text{sf}}}` (no c); `E_{\text{cgt}}` in text vs `E_{\text{ocsf},t}` in the equation.
- Scenario index sometimes dropped (`xcp_{cgft}`, `ncp_{cgft}`, `fix_{\text{cft}}`, `tic_{P,\text{cf}}` has no t though RHS does), sometimes as `B`/`P` subscript, sometimes inside `ame` (`\text{am}e_{B,L,t - 1}`, `\text{am}e_{P,Lt}`) while the LHS `em_{\text{ocLpt}}` carries generic `o`.
- Fuel codes: upper case `COA, NGA, OIL...` (footnote 10, equations `\text{COA}`, `\text{COAL}`, `\text{GAS}` for natural gas) vs lower case `coa, nga, ...` (Appendix F); electricity `ecy` (Mitigation Appendix F) vs `ely` (Distribution tbl-5_1, HBS); `f = P` for power in the power-demand section; Appendix F expanded biomass codes look swapped (`bgs` labelled biodiesel, `bdi` labelled biogasoline).
- Base year/time window: base year 2019 and historical price years 2019–2021 (Prices Overview) vs Appendix C averages over "historical years $t_0$ (2018-2022)", heading "Forecasted prices (after 2021)" vs text "For years starting from 2023"; horizon 2019–2035 vs "(2018-2035)" in the summary of methodology; `t_{0}` is also used as a summation index (`\sum_{t_0 = 2018}^{2022}`) and written `t0` in `(1 + \delta_{CT})^{t-t0}`.

### 4.3 Undefined, renamed or mismatched symbols (Mitigation)

- `\epsilon_{G}` undefined (see 4.1). `tex_{P,tcft}` undefined. `fug` and `gwp` listed in the Emissions notation table but used in no equation. `XCT`, `XETSP`, `\varphi_{XCT}`, `\varphi_{XETS}`, `ttx`, `vatrate`, `n_{t_0}`, `tcp`, `TCP`, `\theta^{PS}_{TCP}` appear in Appendix C equations but not in the Prices notation table.
- Coverage symbol: table `\varphi_{\text{NCT} / \text{ETS}}`, equations `\varphi_{\text{NCT},cgft}` and `\varphi_{\text{NETS},cgft}`.
- Variable OpEx: table `\text{opv}`, equation `\text{vo}p`. Implicit coal price: table `\text{ipc}`, equation `ip_{\text{cft}}`, text `\text{ip}c_{\text{cft}}`, calibration `\text{im}p_{c,\text{coa},t}`. Forward-looking fixed cost text names `\text{fro}` (for `opf`) and `\text{re}s_{\text{cft}}` (for `\text{pusRe}n`).
- Fuel cost in `vc`: text says $\frac{ps_{\text{cft}}}{\nu_{\text{cf}}}$ (pre-tax incl. producer subsidies) but the equation writes `\frac{p_{\text{ocft}}}{\nu_{\text{cf}}}` (retail price) and `ps` is elsewhere the producer subsidy itself.
- Supply-price table entry `sp_{T}` vs equations `sp_{B,\text{cg}}^{T}`; `mu^{T}` vs `\text{mu}`.
- Markup sign: `mu_{B,\text{cgt}}^{T} = \text{gn}c_{B,\text{ct}}^{\text{av}} + \text{tmc} - \text{hr}p_{\text{cg}}` is then *added* in `p_{P,\text{cgt}}^{T}`; to reproduce `\text{hrp}` in the base year the markup must be `\text{hrp} - \text{gnc}^{av} - \text{tmc}` (consistent with the text "when the markup is negative ... the model captures a subsidy").
- Levelized investment cost: `\text{df}c` defined as "$1 + \text{wac}c_{\text{cft}}^{t - t_{0}}$" (presumably `(1+wacc)^{-(t-t_0)}`); as written `tic = vc*cf*dfc/(cf*dfc) + fix^{fl}` cancels to `vc + fix^{fl}` (sums over t are presumably intended).
- Decommissioning: notation table unit US\$/kWh, text "$\text{dt}c_{\text{cft}}$ denotes the decommissioning and transmission costs in USD per kW"; `opf` unit US\$/kW in table, "USD per kWh" in text.
- LCOE denominators: "$\text{dem}$ is the discounted power produced" (Concept 2) vs "$g$ is the discounted power produced" (Simplification) for the same equation.
- Dispatch: `H_{f}` in the equation, `H_{g}` and `K_{g}` in the text; `\lambda_{f}` unit given as GWh but it is a proportion; `COAL` vs `COA`; `\text{residualreqge}n_{\text{oc},\frac{\text{COA}}{\text{GAS}},t}` (a fraction used as a label); multilogit LHS sums over `f`, RHS over `i`, with cost written `c` (no index).
- Capacity stock equation is written in generation `g_{\text{ocft}}` (GWh) with `\sum_{f}^{}ret_{ocf,t - 1}` summed over `f` on an f-specific LHS; `inv`/`ret` units MWh in the table though `\text{re}t_{\text{ocft}} = \frac{1}{\text{lif}}*\text{ca}p_{\text{ocft}}` is in capacity (MWy).
- PPA generation mix uses `CF_{\text{cft}}` (capital) where `cf` is meant; `\Omega` has no indices.
- `\zeta_{\text{cft}}` "New investments permitted": unit MWh in the table, "in percentage" in text.
- Storage: `\frac{\text{dsst}}{\text{dv}} = 18v^{2}` is not the derivative of `\text{sst} = 9v^{2}` (should be `18v`). Short-term kWh/kW ratio: "standard 4-hour ratio" vs "we use a low number (2 hours)" (Appendix E: 2 hours). Long-term marginal table (85%→2.5, 90%→5.0, 95%→7.5, 100%→10.0 MW) does not match the stated derivative `2*\frac{v - 0.75}{\left( 1 - 0.75 \right)^{2}}` (gives 3.2 at 85%, 8.0 at 100%).
- Elasticity-model share equation: the documented form sums `\sum_{i \neq f}` in the numerator and `\sum_{j \neq f}` in the denominator; the implemented form sums `\sum_{f \neq i}` in both (index roles swapped); `\iota_{\text{cft}}` drops `o` while defined from `o`-indexed costs; `\delta^{\text{add}}` appears unindexed in the equation but `\delta_{\text{oct}}^{\text{add}}` in its definition. The text explaining the cross term refers to "$\frac{\Phi_{\text{ocf},t - 1}}{\sum_{f \neq i}^{}\Phi_{\text{ocf},t - 1}}$".
- Power-sector fuel use `F_{\text{ocft}} = E_{\text{ocft}}*...` uses `E` (demand) with a fuel index, while the text says "The fuel use is equal to the electricity generated" (i.e. `g`); base year written `0` not `t_{0}`, exponent `t` (cumulative).
- Covid factor `\Psi`: multiplicative factor `\Psi_{\text{ct}}` in the fuel/engineer equations but additive rate in `\left( 1 + 0.5*\Psi_{\text{ct}} \right)` (elasticity model); unit listed as %.
- Rebound term uses `P_{t}` (aggregate price symbol) instead of `p`.
- Thermal efficiency also written `\varphi = \frac{W}{Q_{I}}` (power data) and computed as `\nu_{\text{cf}} = \frac{g_{\text{cf},t_{0}}}{F_{\text{cEf},t_{0}}}` (GWh over ktoe, unit conversion implicit) while the text cites `F_{\text{ocEf},t_{0}}`.
- Emissions: unit of `\text{em}` given as tCO2/GJ; IPPU text uses `\text{Δe}m_{ocP,CO_{2},t + 1}` (P) where the equation uses `\Delta em_{ocI,CO_{2},t + 1}` (I); LULUCF CO2 uses norm bars `\left\| \cdot \right\|` while CH4/N2O use `\left| \cdot \right|`, and drops `p` in `em_{\text{ocL},2019}`; agriculture uses `\text{am}e_{A,t - 1}` (no B/P) vs LULUCF `\text{am}e_{B,L,t - 1}`/`\text{am}e_{P,Lt}` and text `a\text{me}_{cLp,t}`; `Y_{\text{grow}}` (table) vs `Y_{\text{growth}}` (equation); `lp_{\text{grow},t}` vs `lp_{\text{grow}}`.
- Fiscal: `revEx_{ft}` (text) vs `revExi_{ft}` (eq.); `ct_{ocft}` (text) vs `ctr_{ocft}` (eq.); `ncp` unit US\$/ton of CO2 in the revenue table but US\$/Gj in the price table (the formula `F*\varphi*ncp` needs per-energy-unit).
- Welfare: `ddw_{ft} = \frac{\left( nc_{ft} - xcp_{ft} \right)}{2}*(F_{P,ft} - F_{B,ft})` uses `nc_{ft}` while the text writes `ncp_{ft}`; the text calls it "the average of new and pre-existing tax" but the formula is half their difference.
- Supply price: main text "sum of the fixed and floating portions of the supply price, minus any remaining producer subsidies" vs Appendix C `sp_{cgf,t} = fixsp_{cgf} + fltsp_{cgf,t} + ps_{cgf,t}` (plus).
- Existing carbon price: main text grows last year's `xct_{cgf,t - 1}` by one period of `(1+\delta)` while Appendix C compounds from `t_0`; ETS adjusted values written `XETSP_{c,t}` in text but notation table has only `NETSP`, `NCT`.
- VAT symbol family: `vat`, `VAT` ("where $VAT$ is the VAT payment per energy unit"), `vatrate`, `VATrate`.

### 4.4 Distribution, Multipliers, Air pollution, Road transport

- Distribution: `\pi^{\text{dg}}` (superscript order d,g) vs `\pi_{j}^{g}`; `C_{j}^{g}` vs `C_{\text{gj}}`; `e_{f}`, `e_{g}`, `\overline{e_{g}}`, `\overline{e_{\text{fg}}}` used for related intensities; eq-5_2 states "$f \in g$" while eq-5_3 states "$f \notin g$" and the text says direct effects are "for f=g, in @eq-5_3" (should reference eq-5_2); `\text{pop}^T_y` (eq-5_10) vs `\text{pop}_{T}^{y}` (eq-5_9); eq-5_13 sums `\sum_{d = 1}^{10}` on the RHS while the LHS is decile-specific; eq-5_7 uses `t` and plain `\epsilon_{\text{use}}` while the text has `{\epsilon_{\text{use}}}^{g}` and year index `y`; `t_{\text{fg}}` is called a "tax rate" but defined as a price ratio USD<sub>p2</sub>/USD<sub>p1</sub>; Personal Allowance scenario labelled `PE`; `s_{\text{dc}}` vs `s_{\text{dcy}}`; indicator bound written `l_{\text{dy}}` once; `P_{\text{dcy}}` (population) collides with `P_{D}`, `P_{M}` (revenues).
- Distribution vs Mitigation: Distribution uses `g` for consumption categories/IO sectors and only three price sectors (power, industry, residential), while Mitigation `g` is the sector grouping (residential, industry incl. services, transport, power); `j` (household) clashes with Mitigation's bound fuel index; `\gamma_{g}` (pass-through) clashes with engineer-model `\gamma`.
- Multipliers: no in-CPAT multiplier symbol or GDP equation; error term `\epsilon_{t,i,h}` in the equation vs `\varepsilon_{t,i,h}` in the text; `\alpha`, `\delta`, `\gamma` reused with meanings unrelated to Mitigation.
- Air pollution: in eq-deltae `k` is defined as "pollutant" but indexes source regions `x_{k}`; eq-modeled swaps the roles of `i` and `j` relative to eq-sourcerecep; eq-pomincfactor writes `d_{POM,2}` with `delta_{POM,1}`; eq-ifeach LHS `{iF}_{p,\ j,\ l}` but the where-list writes `{iF}_{p,\ j,\ c}`; `p_{\text{HAP}}` vs `p_{H}`; `\Pi_{ij,t}` vs `\pi_{ij,t}`; `W_{\text{ij}}` vs `Wij`; `\text{THE}_{c,t}` "for country $t$"; the urban factor appears as `UrbanIncFactor`, `urbIncfactor`, `urbanIncfactor`; eq-vsloecdbis has `VSL_{OECD,\ 2014}` on both sides; `\text{Cor}r_{\text{factor}}` (eq-corr) vs `\text{cor}r_{\text{fact}}` (text); travel-time valuation 50% of after-tax wage (AP) vs 80% (Road transport "Externality costs").
- Road transport: `Y_{t}^{\text{simple}}` vs `Y_{t}^{f}` for the naive forecast; eq-basefor subtracts the average growth `\overline{g^{\text{GDP}}}` from a gross growth ratio `\frac{\text{GDP}_{t}}{\text{GDP}_{t - 1}}` (dimensionally ambiguous: as written the base is ≈1 − g̅ + g, not 1 + g − g̅ unless g̅ is a net rate); elasticities are `\eta` here vs `\epsilon` in Mitigation; `\beta` is the elasticity in eq-no1.

## 5. Interfaces: what the Air-pollution and Road-transport modules take from Mitigation, and what they return

### 5.1 Air pollution (`06_Air_pollution.qmd`)

**Inputs from the Mitigation module / shared CPAT data:**

- Energy consumption by fuel, sector, year and scenario (`F_{\text{ocsf},t}`): "the air pollution tab receives as an input the energy consumption for the different sectors and fuels from the Mitigation tab" (Introduction); sectors re-aggregated per tbl-aggsec (power by coal/gas/other, road, residential/services/construction, industries, rail, domestic aviation LTO, food & forestry).
- Emissions of local pollutants (PM2.5, NOx, SO2, CO2, NMVOC, BC, OC, CH4, CO) — computed in the Mitigation tab with GAINS (ECLIPSE_V5a_CLE_base) EFs (time-varying or 2015-constant; 89 countries, else regional averages): "Emissions (of local and global pollutants) are calculated in the Mitigation tab"; review log: "Emissions of local pollutants were moved to the mitigation module". NH3 assumed constant.
- Biomass leakage (residential): "The demand for fuels, including the demand for biomass for cooking is calculated in the Mitigation tab" → `Leakage` in eq-prophh (default 50% to more households using solid fuels, 50% to more use within such households; 100% of indoor emissions reach ambient air).
- Year, baseline/policy scenario structure (baseline year 2019 for C0 calibration and ML perturbations).
- Macro data: GDP and GDP per capita projections (VSL transfer eq-vslct, labour-share output losses eq-wij), population projections, real interest rate / discount rate options, CPI.
- Emission factors per fuel/sector and calorific values/densities for per-litre externalities.

**Outputs (and where they flow back):**

- Ambient PM2.5 and O3 concentrations (population-weighted, baseline and policy) by one of 6 options; household exposure.
- Deaths, YLL, YLD, DALYs attributable to ambient + household PM2.5 and ozone (COPD), baseline vs policy; averted deaths with cessation lag (30% year 1, 50% years 2–5, 20% years 6–20; discount factors 0.906 at 3%, 0.798 at 8%).
- Monetised: VSL-valued averted mortality, morbidity cost (YLD-based), working days lost, market output losses (mortality, morbidity), health expenditure attributable (by payer). → Mitigation "Monetized welfare benefits" item 2: "Averted air pollution mortality/morbidity is taken from the Air Pollution module".
- Air pollution externality per unit of fuel (deaths/ktoe × VSL + morbidity; expressed US\$/ktoe, US\$/litre, US\$/GJ) → Mitigation "Energy externalities costs" component 2 ("Air pollution costs"), which with supply cost and VAT defines the 'efficient price' and the optional non-climate Pigouvian tax ("Add non-climate Pigouvian tax on top?", Appendix E) — i.e. a feedback into prices.
- Net warming effects of local pollutants via regional GWP100 coefficients (tbl-gwp) and CH4 GWP100 = 28.
- Shared valuation inputs used by Road transport: VSL ("adjusted for GDP growth and inflation (within the Air Pollution Module)"), average hourly after-tax wages, and the travel-time method (eq-congvkm, eq-freeflow, eq-travtime: "used in CPAT Transport tab").

### 5.2 Road transport (`07_Road_Transport.qmd`)

**Inputs from Mitigation / shared data:**

- Road fuel prices, baseline and policy: "The Road Transport Module takes as an input the road fuel price changes induced by the policy"; road fuel price = gasoline and diesel prices weighted by each fuel's share of total road fuel consumption in that scenario (baseline weights for baseline, policy weights for policy) → `p^{\text{baseline}}`, `p^{\text{policy}}`.
- Road fuel consumption by fuel and scenario (for the weights) and the change in motor fuel consumption (denominator of externality per litre: "Divide change in value by change in motor fuel consumption from CPAT Mitigation Module").
- GDP growth forecasts (IMF WEO) and population projections (WB) for eq-basefor; elasticities by country (`\eta_{p}` wrt price or tax, `\eta_{\text{GDP}}`, `\eta_{\text{pop}}`) from the Tran_Elas sheet (country-specific via eq-no7 or international default).
- VSL and after-tax wages from the Air Pollution module (valuation).

**Outputs:**

- Baseline and policy forecasts of VKT, urban congestion (TomTom index), road-accident fatalities and road damage (maintenance cost); policy impact = difference.
- Externality costs per litre of motor fuel for accidents (fatalities × VSL) and congestion (time lost × value of travel time; urban only) → Mitigation "Energy externalities costs" item 3 and "Monetized welfare benefits" items 3 ("Averted road accidents are taken from the transport module") and 4 ("Reduced congestion is taken from the transport module").
- Road damage is computed but **not** included in welfare (Mitigation footnote 37: "Resulting reduced road damage are currently not accounted for in welfare benefits"); Appendix E parameter "Congestion & road damage attributable to fuels: 0.01".
- No feedback into Mitigation quantities: "the VKT estimates in the CPAT Road Transport Module are not linked to the transport CO2 in the Mitigation Module".

### 5.3 (For completeness) Distribution and Multipliers interfaces

- Distribution ← Mitigation: fuel price changes `t_{\text{fg}}` "for each country, year and fuel-sector pair" (power, industry, residential; residential for direct effects), revenues `P_{M}^{y}` available for recycling (share chosen by user per scheme), expected GDP `\text{GDP}^{y}`, economy-wide emissions reductions (for the mitigation-adjusted option). Distribution → Mitigation: nothing ("this adjustment is carried out in the Distribution Module alone and does not alter revenue estimates in/from the Mitigation Module").
- Multipliers ↔ Mitigation: recycled revenues by instrument (EET, PIT, VAT, GIS, GCS, TRS) × multipliers (horizons up to 10 years) adjust baseline real GDP growth; the adjusted `Y` feeds back into energy demand through `\epsilon_{Y}` ("the change in GDP affects energy consumption and, therefore, the effective carbon tax revenues", Multipliers Introduction; Summary "Mitigation module"). Exact formula not documented.
