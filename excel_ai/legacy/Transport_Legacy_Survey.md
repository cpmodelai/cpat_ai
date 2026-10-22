# Legacy CPAT road transport (engineer) model: survey (for CPAT-AI-Mitigation-Prototype v4.7)

Source: `legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb`/xlsx (formulas) and `.xlsb` (cached values, Egypt run). Read-only survey, 2026-10-14.

## 0. How to read the formulas (important)

The xlsx was converted from the xlsb and **lost every defined name**: all name references show as `#NAME?` in openpyxl, and all 1,898 `<definedName>` entries in `xl/workbook.xml` are empty. I recovered them by parsing the xlsb binary directly:

- `names.py` parses the BrtName records in `xl/workbook.bin`: name to target range. Output: `names.tsv`.
- `fnames2.py` parses the BIFF12 formula token streams (rgce) in the sheet `.bin` parts, including shared (BrtShrFmla, 427) and array (BrtArrFmla, 426) formulas. It lists the ptgName references for each cell (`cellnames.json`).
- The `#NAME?` placeholders are then replaced in order with `{name}`. The resolved dumps are `f_Mitigation.txt`, `f_Transport.txt`, `f_Transport3.txt` and `f_MTInputs.txt`, with cached values in `v_*.txt`. About 39,800 Mitigation cells are resolved; 6 are left unresolved, all outside transport.
- The parsers are kept as `tools/xlsb_names.py`, `tools/xlsb_fnames2.py`, `tools/xlsb_grid.py` and `tools/xlsb_rc.py` (survey helpers, not maintained). The dumps were scratch output and are regenerated in phase 1 of `Transport_Plan.md`.

Formulas below use the recovered names in `{braces}`.

Key names for transport:

| Name | Target | Egypt value |
|---|---|---|
| `TrModel` | MTInputs!F340 (from Dashboard!G61) | **"Elasticity"** (default column G = "Engineer") |
| `RngAnxietySource` | Dashboard!L61 | "Solver" (so it uses the Transport3 calibration) |
| `PassAnxiety` / `FreightAnxiety` / `MotorAnxiety` | Dashboard!G548 / L548 / Q548 | 10,000 $/vehicle (used only if the source is "Dashboard") |
| `PassAnxietyDecline` etc. | Dashboard!G549 / L549 / Q549 | 0 |
| `_el_dem_gso_rod`, `_el_dem_die_rod` | Mitigation!K330 / K331 | -0.4 / -0.3 (Elasticities!C64 / C65) |
| `_el_eff_gso_rod`, `_el_eff_die_rod` | Mitigation elasticity block | -0.4 / (diesel value) |
| `_eff_imp_oil_rod` | autonomous efficiency improvement, road oil | (Mitigation) |
| `FirstYearCalculations` | MTInputs!F232 | 2022 |
| `_Country_code` | Dashboard!D644 | EGY |
| `_EnergyConsumptionBaseYear` | Mitigation!F583:W602 | base-year energy balance |
| `_conv_ktoe_liter_gso` etc. | Mitigation!O949 and neighbours | liters per ktoe (1.198e6 for gasoline) |
| `_ef_co2_*_lit` | Mitigation!O980:O1012 | tCO2 per liter; the names are mislabelled (see the bugs section) |

## 1. Sheets that hold transport

| Sheet | Size (rows x cols) | Role |
|---|---|---|
| **Mitigation** | 19,227 x 35 | The engineer model itself (section 5 of each scenario block), its input block (key inputs section 15), the elasticity road model, the switch, and the hand-off to the Transport and Air pollution sheets |
| Transport1 | 881 x 98 | Data only (no formulas). One row per country x year, 221 countries, years 2022-2025. Column A is the country, B the iso3, C the year; row 1 holds the variable codes that Mitigation column B matches on |
| Transport2 | 4,181 x 9 | Data only. Vehicle purchase prices (`ev_price_*` and `icev_price_*` for cycle, freight and passenger) by iso3 x year, 2022-2040 |
| Transport3 | 204 x 72 (live area A1:U226) | Range-anxiety calibration. Row 4 is the live goal-seek row (it pulls Mitigation rows 18982-18987); rows 5-226 are stored per-country solver results (Actual, Calculation, 2030, 2035, Difference, Range anxiety for passenger H, freight N and 2-3 wheeler T). Row 3 = INDEX by `_Countryname` (falls back to the average) |
| **Transport** | 728 x 36 | A *different* module: road-transport **externalities** (accidents, congestion, travel time, road damage), years I(2022)..AB(2041). It reads the engineer VKT and fuel economy and writes efficient-price components and welfare back to Mitigation |
| Tran_Elast | 221 x 54 | Country elasticities for VKT, deaths, damage and congestion (short and long run, price and tax) for the Transport (externalities) sheet (`_tran_elasticities`) |
| Tran_Scatter | 5 x 23 | Data for the historical scatter charts |
| Notes | 124 x 9 | Text: "Notes on the transport model". This documents the externality econometrics, not the engineer model |
| Dashboard | rows 60-98 and 540-558 | All engineer-model policy and parameter inputs (they bypass MTInputs) |
| Manual inputs | rows 373-377 | Fuel economy of new BEVs (hardcoded paths) |
| MTInputs | row 340 (`TrModel`); rows 52-64 (feebate rates); 243 (`AdditionalEfficiencyRoadVehicle`); 248 (`SPPEffAdjVehicleFuelEconomy`) | The only transport switch in MTInputs is row 340. The engineer-specific inputs are not in MTInputs |

There is no `TransportDataRequest` sheet, although the methodology note mentions one.

### Mitigation layout

Year columns: K = 2021 helper, L = 2022 (base) through AE = 2041. Text columns: B = fuel or code, C = sector, D = description, F = unit, G/H = codes. The parameter tables in section 5 use the columns J..AD as a side table (see 3.1).

Scenario blocks: block C (baseline) runs rows 2173-8503 (`C2173` = scenario number 1). Block D (policy, `B8504={_PolicyScenarioPolicy}`) runs rows 8504-14769 and is a full copy at **offset +6,331** (for example, transport section 5 starts at row 10633 and the switch rows are 11760-11771). Block E (14770+) holds results for other modules; block F (16081+) holds the reports.

### "Key inputs 15", Mitigation rows 2015-2171 (`A2015=15`, "Transportation")

This block appears **once** (above the scenario blocks), with data for L..O (2022-2025) only. Note the layout quirk in rows 2017-2031: column L = share, M = ktoe, N = bln liter (these are not years). C holds the liters-per-ktoe factor.

| Rows | Content |
|---|---|
| 2017-2031 | Base-year split of road fuel use by vehicle type. The shares come from Transport1 (`share of gasoline for passenger`, `... for cycle`, diesel passenger/bus/freight, LPG passenger/bus/freight, natural gas passenger/bus/freight); "light" = 1 - sum. The shares multiply the energy balance (`$G$587+$G$598` gasoline, `$G$588+$G$599` diesel, `$G$590` LPG, `$G$585` gas). Egypt: gasoline 60.5% passenger, 0.5% 2-3 wheeler, 38.9% light; diesel 56.0% passenger, 4.9% bus, 39.1% freight; gas 62.3% passenger, 37.7% bus |
| 2033-2089 | Passenger and light: fuel economy (Transport1); passenger share of passenger/light (2038); blended fuel economies (2041-2052, e.g. `=L2040*L$2038+L$2034*(1-L$2038)`); BEV-light fuel economy **hardcoded** in row 2051 (1.397 rising to 2.76 km/kWh); price per km (2054-2055); BEV VKT uplift (`MIN($H2056=1.2,(pBEV/pICE)^{_el_dem_gso_rod})`); VKT for the purchase calculation (2058-2061); EV purchase and stock shares (2063-2068); VKT by fuel = fuel economy x liters (2072-2076); vehicle shares (2078-2083); vehicles per 1,000 people (2086-2087); BEV purchase share (2088); `Data available` (2089 = 2025) |
| 2091-2118 | Freight: fuel economy; BEV freight fuel economy **hardcoded** in row 2095 (0.714 rising to 1.63 km/kWh); VKT; BEV shares; ownership; price per km; VKT per vehicle (row 2117 is *derived*, 8,091 km, while Transport1 `average vkt freight` = 48,630 km is used in the purchase calculation) |
| 2120-2137 | 2-3 wheelers: fuel economy; BEV fuel economy **hardcoded** in row 2122; ownership; VKT |
| 2139-2143 | Buses: base fuel use for diesel/LPG/gas from 2021/2025/2029. Electricity = `N2064*SUM(...)` |
| 2146-2147 | Emissions-intensity adjustment for gasoline and diesel (`G587/(G587+G598)`, i.e. the biofuel share) |
| 2150-2166 | Used-vehicle share; purchase prices (Transport2, with IFERROR carry-forward, so these extend to 2041); import duties; import shares; charging stations; ownership saturation point (Transport1) |
| 2167-2171 | GDP per capita (row 444); freight-to-passenger ownership ratio (row 2168, a declining linear function of income between Dashboard V553/V554); 2-3 wheeler ownership hump `2*J*H*y/(y^2+H^2)` with H = 7,000 USD (row 2169); **charging-station cost $/port hardcoded** (row 2170: 237,010 falling to 111,740); "Change in vehicle ownership" (row 2171) |

All data lookups have the form `INDEX(Transport1!$A$1:$CZ$1000, MATCH({_Country_code}&L$2033, Transport1!B&C, 0), MATCH($B20xx, Transport1!$A$1:$CZ$1, 0))`, so **column B of Mitigation holds the Transport1 variable code**.

### Section 5 "Transport sector - Baseline", Mitigation rows 4302-5537 (policy copy 10633-11868)

| Rows | Block |
|---|---|
| 4303-4332 | **Policy and parameter side tables** (columns G..AD, all `=Dashboard!...`). Feebate (J/K/L = passenger/freight/2-3 wheeler: year, $/t, pivot type, pivot, pivot change); distance tax (P/Q/R: start year, $/km, target year, $/km); VAT/customs (V/W/X: baseline and policy VAT, baseline and policy customs, year, import share); EV subsidies (AB/AC/AD: year, $/vehicle, annual change); ad-valorem purchase tax (J/K/L 4315-4319); charging-station subsidy (P4315-P4318); vehicle parameters (J/K/L 4322-4332: ownership years 7, useful life 20/10/7, first-year depreciation 30%, insurance 1.5%, maintenance $/km for ICE and EV, income elasticity of driving J4330 = 0.1, K = 0.1, L = -0.4; new-versus-average efficiency gap 5%; k-parameter 3/2/4); freight discount rate `K4329=AVERAGE(I2988:I2996)` (power WACCs); charging parameters P4322-P4328; ownership T/U/V 4322-4330 (adjustment speed 0.09, Gompertz coefficient -0.23, max growth 7.5%, max decline 0 (2-3 wheelers 10%), own-price elasticity -1.265 and cross-price elasticity 0.5725 (hardcoded `AVERAGE(...)` literals)); discount-rate income schedule Z4322-Z4325 (15% at <=1,000 to 5% at >=50,000 USD) |
| 4334-4356 | Charging stations, EV charging mark-up, EV electricity price, range anxiety |
| 4358-4407 | Fuel economy, passenger/light (new and used), feebate per liter, emissions intensity |
| 4409-4435 | Fuel economy, freight |
| 4437-4448 | Fuel economy, 2-3 wheelers |
| 4450-4476 | Distance driven, passenger (distance tax, cost per km, VKT of new and used vehicles) |
| 4478-4494 | Distance driven, freight |
| 4496-4505 | Distance driven, 2-3 wheelers |
| 4507-4582 | Lifetime cost (TCO), passenger new: ICEV 4523-4555, BEV 4557-4582 |
| 4584-4624 | TCO, passenger used |
| 4626-4681 | TCO, freight new |
| 4683-4736 | TCO, 2-3 wheelers new |
| 4738-4872 | Vehicle composition, passenger: stock accounting, Gompertz demand, logit EV choice, ICE fuel split, vehicles in millions |
| 4874-4952 | Vehicle composition, freight |
| 4954-5007 | Vehicle composition, 2-3 wheelers |
| 5009-5167 | "Fuel economy and reconciliation with energy balances": stock-average fuel economy (opening/closing), cost per km, **uncalibrated** VKT per vehicle and fuel use |
| 5169-5173 | **Calibration step 1**: bottom-up versus energy-balance ratios per fuel, giving the VKT scale factors U/V/W5170 |
| 5175-5303 | "Fuel use and distance driven", passenger / freight / 2-3 wheelers, **calibrated** (VKT per vehicle x factor) |
| 5305-5318 | Public transport (buses) |
| 5320-5351 | **Calibration step 2** (factors E5325-E5331) and final fuel use by fuel in ktoe (5325-5331); VKT (5333-5336); fuel use by vehicle type x fuel (5339-5351) |
| 5353-5378 | "Results for the rest of CPAT": average fuel economy by fuel (5356/5360/5364/5368/5373); vehicles (5375-5378) |
| 5380-5410 | **Road transportation, elasticity approach** (the standard CPAT fuel-use equation) |
| 5412-5442 | Road, used in calculations: **the switch** |
| 5445-5517 | Rail, aviation and navigation (elasticity approach only) |
| 5520-5537 | Total transport |

## 2. Road fuel use, the switch, and the links in both directions

### The switch (Mitigation rows 5428-5440; policy copy 11759-11771)

```
M5429 (nga)  =IFERROR(IF({TrModel} = "Engineer", M5328, M5397), M5397)
M5430 (gso)  =IFERROR(IF({TrModel} = "Engineer", M5325, M5398), M5398)
M5431 (die)  =IFERROR(IF({TrModel} = "Engineer", M5326, M5399), M5399)
M5432 (lpg)  =IFERROR(IF({TrModel} = "Engineer", M5327, M5400), M5400)
M5440 (power demand memo) =IFERROR(IF({TrModel} = "Engineer", M5331, M5408), M5408)
M5436-5438 biofuels: engineer -> L5436*M5430/L5430 (scaled with the fossil fuel); else the elasticity row
coa, ker, oop, ren: always elasticity (M5428=M5396, etc.)
L-column (2022) = energy balance in both branches.
```

`TrModel` = MTInputs!F340 = `IF(MTAct, D340, IF(Defaults, IF(I340="Y", E340, G340), E340))`, with E340 = Dashboard!$G$61. **In the Egypt run TrModel = "Elasticity"**, so the legacy Egypt road fuel use is the elasticity model. The engineer block is still calculated (cached values are non-zero) and it still feeds the Transport externality sheet (see below).

The elasticity road model (rows 5396-5402) is the standard CPAT equation, for example for gasoline:

```
M5398 = L5398*((1+M2446)^({_el_inc_gso_rod}*M2433))*(1+M2439)*((M5384/L5384)^{_el_dem_gso_rod})
        *((((M5384+M2383*M2404)/(L5384+L2383*L2404))^({_el_eff_gso_rod}))/(1+{_eff_imp_oil_rod}+$M2199))^(1+{_el_dem_gso_rod})
```

Here 5382-5393 are post-tax prices (`L2605+L2606*L2271`), 2383 is the shadow price, 2404 the feebate share, and 2439 the exogenous shock.

### Engineer final fuel use (rows 5321-5331)

```
L5321 gso bln l = L5195 + L5279                 (passenger + 2-3 wheelers)
L5322 die       = L5196 + L5243 + L5315         (passenger + freight + bus)
L5323 lpg       = L5197 + L5244 + L5316
L5324 nga       = L5198 + L5245 + L5317
L5325 gso ktoe  = L5321 / $G5325 * 10^9 * $E5325      G = {_conv_ktoe_liter_gso}
E5325 = IF(OR(I5325=0,J5325=0),1,J5325/I5325)          I = L5321/G*1e9 (calculated base year), J = INDEX({_EnergyConsumptionBaseYear},...)
L5330 ele bln kWh = SUM(L5318, L5299, L5265, L5223);  L5331 = L5330*1000/$G5331*$E5331
E5331 = IF(OR(I=0,J=0,Dashboard!$Q$556="No"),1,J/I)   (electricity reconciliation is optional)
```

### Inputs from the rest of Mitigation into the engineer model

- **Fuel prices** (post-tax, scenario-specific, so the carbon tax, fuel reform and existing taxes all pass through):
  - Gasoline passenger: `L2589` (retail).
  - Diesel passenger: `L2612`.
  - LPG: `L2635`.
  - CNG: `L2543/26` (residential gas $/GJ divided by 26).
  - Freight: diesel `L2612-L2618` (net of VAT), LPG `L2635-L2641`, LNG `(L2566-L2572)/26` (industrial gas, net of VAT).
  - 2-3 wheelers: `(L2590+L2596)*(1+L2594)`.
- **Electricity**: residential `L3617` and industrial `L3646` power prices, **lagged one year** (`M4351 = L3617 + M4350`, with the note "previous year to avoid circular reference").
- **Carbon price into the feebate**: `L4374 = (IF(year>=$J4304,$J4305,0) + L2375*L2404)*($C2173>1)`. Here 2375 is the general carbon price and 2404 the road feebate coverage.
- **Macro**: GDP growth `2446` (lagged), population `428`, GDP per capita `444`.
- **Elasticities**: `_el_dem_gso_rod` and `_el_dem_die_rod` (VKT), `_el_eff_gso_rod` and `_el_eff_die_rod` (new fuel economy), `_eff_imp_oil_rod` (autonomous efficiency).
- **Emission factors**: `_ef_co2_*_lit` times the 2146/2147 adjustments (G4375-G4379, G4419-G4421, G4441).
- **Base-year energy balance**: `_EnergyConsumptionBaseYear` (rows 583-602), via the 5170 and 5325 calibrations.

### Outputs from the engineer model to the rest of the workbook

- Road energy (rows 5428-5440, switched) feeds Total transport (5521-5537), emissions (6611+), revenues and so on.
- Road electricity: `M3725 = IFERROR(M5440, L3725*M3695)`, i.e. power-sector demand.
- **Even under "Elasticity"**, block E rows 15720-15823 pull the engineer outputs by output code: fuel use by vehicle type (from 5339-5351), average fuel economy by fuel (from 5356-5373), and VKT by passenger/freight/2-3 wheeler/all (5333-5336). These feed the **Transport** externality sheet (`Transport!C112:E146`), mixed with the *switched* energy totals (15759-15781).
- The Transport sheet returns to Mitigation:
  - Rows 128-133: externality $/liter by fuel (`=Transport!I322` etc.).
  - Rows 17733-17735: welfare (`=Transport!I356`, `I360`, `I364`).
  - Rows 17771-17776 and 17980-17997: efficient-price components.
- Rows 18981-18987 ("Share of EV sales", calculated and actual) feed Transport3 row 4 for the range-anxiety solver.

## 3. Engineer model equations (as implemented)

Vehicle classes:
- **Passenger/light** (LDV = cars + light commercial, blended by the ownership share in row 2038), new and used.
- **Freight** (HDV), new only.
- **2-3 wheelers**, new only.
- **Buses**: no stock model.

Powertrains:
- Passenger: gasoline, diesel, LPG, CNG, PHEV, BEV.
- Freight: diesel, LPG, LNG, BEV.
- 2-3 wheelers: gasoline, BEV.

The model is yearly. Data years 2022-2025 (columns L-O) are set from Transport1; projections run from 2026 (column P) and use `IF(ISNUMBER(data), data, model)`.

### 3.1 Charging, electricity price and range anxiety (rows 4334-4356)

- BEV stock (mln) = sum of the BEV stocks per capita (rows 4763, 4771, 4888, 4968) x population / 1000 (row 4340).
- Charging stations: data for 2022-2025, then `P4347 = O4347*(BEVstock_t/BEVstock_t-1)^0.3*(cost_t/cost_t-1)^-0.67`, where cost = $/port after the subsidy in row 4344.
- Charging mark-up: `L4350 = MAX($P4324=0.02, $P4323=0.3*($P4325=0.5 - EVfleetshare)/(1-0.5)) * $P4326=0.2` $/kWh.
- EV electricity price: `M4351 = L3617(prev yr resid) + M4350` (passenger and 2-3 wheelers); `M4352 = L3646 + M4350` (freight).
- Range anxiety ($/vehicle): L = M = N = `IF(RngAnxietySource="Dashboard", PassAnxiety, Transport3!$H$3)`. Then `O+ = MAX(N*(1-decline)*(stations_t/stations_t-1)^$P4327(-0.5), 0)`. Egypt: passenger 78,639, freight 440,799, 2-3 wheelers 1,108 $/vehicle (Transport3 row 60).

### 3.2 Fuel economy of new vehicles (rows 4358-4448)

- Data years: `L4386 = L$2041*(1+$J4331)`, i.e. the stock fuel economy +5% (new versus average).
- Projections: `P4386 = O4386 * P4380^ABS({_el_eff_gso_rod}) * (1+{_eff_imp_oil_rod})`, where `P4380 = (p_t+feebate_t)/(p_t-1+feebate_t-1)` (row 4380 = change in cost per liter, fuel price plus feebate per liter). This is a price-responsive efficiency with the elasticity's absolute value, plus autonomous improvement. The same applies to freight (`{_el_eff_die_rod}`) and 2-3 wheelers.
- BEV new fuel economy: `'Manual inputs'!J375:AC377` (hardcoded, +1-2% a year).
- The ICE passenger mix uses the previous year's ownership shares (`P4360 = O4861`).
- Used-vehicle fuel economy: `L4401 = AVERAGE(OFFSET(L4391,,,,-MIN(col#, J4322=7)))`, the trailing 7-year average of the new fuel economy. The used emissions intensity is the value 7 years earlier (`OFFSET`).
- Emissions intensity: `G4375/L4386*1e6` (g/km).
- Stock fuel economy (rows 5017-5035, 5096-5106, 5147-5149): closing = new x share_new + opening x (1-share_new). Here share_new = `1/(s_used*7+20*(1-s_used))` for passenger (row 4831), `1/10` for freight and `1/7` for 2-3 wheelers. Data overrides through 2025.

### 3.3 Driving (VKT) (rows 4450-4505 for purchase decisions; rows 5009-5303 for fuel use)

- Distance tax: linear from the start year to the target year (`L4451`).
- Cost per km = fuel price / fuel economy + distance tax.
- **VKT per new vehicle (TCO input)**: `P4465 = O4465 * IF(Dashboard!Q551="No",1,costchange)^{_el_dem_gso_rod} * (1+GDPgrowth_lag)^$J4330`. With the Egypt setting "No", the TCO VKT ignores prices. Freight is clamped to [50,000, 120,000] km (U4325:U4326). Used vehicles: `L4475 = L4470*(FEnew/FEused)^{_el_dem_gso_rod}`.
- **VKT per vehicle for fuel use** (calibrated): `P5177 = O5177 * P5041^{_el_dem_gso_rod} * P5064^$J4330`, where P5041 = change in stock-average cost per km and P5064 = GDP per capita ratio. In data years `L5177 = L5176 (Transport1 avg vkt) * $G5177`, with G5177 = U5170 = **2.668** (passenger), G5231 = V5170 = **1.703** (freight) and G5273 = W5170 = **3.301** (2-3 wheelers).
- Fuel use by fuel = vehicles (mln) x VKT / stock fuel economy. Examples: `L5195 = L5189/L5019 + L5193/L5035` (gasoline incl. PHEV); BEV kWh = VKT/stock km per kWh; PHEV electricity = `VKT/kmkWh*(1-share_gso)`.

### 3.4 Total cost of ownership (rows 4507-4736)

The structure is the same for each class (ICEV and BEV; passenger new and used; freight; 2-3 wheelers):

- **Discounted lifetime km**: `PV(r, years, VKT)*-1`. The ownership period is 7 years for a new passenger vehicle, 13 for used, 10 for freight, 7 for 2-3 wheelers.
- **Discount rate** `L4531`: linear in GDP per capita between 15% (at <=1,000) and 5% (at >=50,000). Freight uses `$K4329` = the average power WACC.
- **Purchase price after policies**:
  - ICEV: `price*(1+customs*importshare)*(1+adval)*(1+VAT) + feebate`.
  - BEV: the same, with the policy customs/VAT/ad-valorem rates after their switch years, + subsidy + feebate.
- **Feebate ($/vehicle)**: `(gCO2/km - pivot)*rate/1e6*discounted km`, with BEV at 0 g/km. Pivot (row 4517): "Average" means `avg_t^2/avg_t-1`; otherwise manual, with an annual decline.
- **Depreciation and salvage**:
  - First-year depreciation: 30%.
  - Then an annuity of `(P-dep1)/(life-1)` over `life-1` years.
  - Salvage: `-P*((life-own)/life*(1-dep1))/(1+r)^own`.
  - Used price: `price*(1-(dep1+(own-1)/(life-1)*(1-dep1)))` grossed up by taxes.
- **Insurance and maintenance**: `P*ins/r*(1-(1+r)^-(own+1))*0.5 + maint$/km*discounted km`.
- **Fuel**: price / fuel economy x discounted km, + distance tax x km.
- **BEV extra**: range anxiety (lump sum). For used BEVs it is scaled by the used/new price ratio.
- **TCO per km** = TCO / discounted km (rows 4549, 4582, 4608, 4624, 4656, 4681, 4714, 4736).
- **Per-fuel ICE TCO** (rows 4551-4555, 4658-4660) is used for the ICE fuel split. PHEV TCO uses the BEV depreciation and range anxiety.

### 3.5 New-vehicle choice (rows 4796-4833, 4907-4927, 4983-5003)

- Logit-type ("k-parameter") share between ICEV and BEV:

  ```
  k_ICE = EXP(-k * TCO_ICE/km / avgTCO)*1000;   k_EV = EXP(-k * TCO_EV/km / avgTCO)*1000
  share_EV = k_EV/(k_ICE+k_EV)
  ```

  avgTCO = TCO weighted by the *lagged* ICE share. k = 3 (passenger), 2 (freight), 4 (2-3 wheelers).
- Passenger has separate new (4800-4803) and used (4814-4817) choices. The combined share is `shrcalc = used*s_used + new*(1-s_used)` (row 4827).
- Data years override with the actual purchase shares (`IF(ISNUMBER(L4805),...)`, rows 4806, 4819). Row 4828 (`shract`) = actual if > 0, else calculated.
- **ICE fuel split** (rows 4846-4850, 4936-4938): constant-elasticity on the TCO change, `share_i,t = share_i,t-1 * (TCO_i ratio)^-1.265 * (weighted other-TCO ratio)^0.5725`. Then renormalised to (1-EV share) (rows 4851-4855). Ownership shares are a moving average: `own_t = own_t-1*(L-1)/L + sales_t/L`, with L = weighted ownership years 13.57 (rows 4856-4865).

### 3.6 Stock dynamics (rows 4738-4790; 4874-4905; 4954-4981)

Stocks are per 1,000 people, split into ICEV and BEV, and for passengers also into new-bought and used-bought sub-stocks:

- `opening_t = closing_t-1`. In data years the opening is the data value times the new/used split.
- **Scrappage** = `MIN(AVERAGE(OFFSET(opening, last min(life, col#) years))/life, opening)`, i.e. linear retirement of 1/life of the trailing-average stock. The life is 7 for the new-owned passenger stock and 13 for used (J4324-J4322); 10 for freight; 7 for 2-3 wheelers.
- Closing = after scrappage + purchases (+ a data-year "adjustment" plug, rows 4749, 4757, 4768, 4776).
- **Total demand** (row 4786):

  ```
  T4322=0.09 * Sat_pass * EXP(-5.897*EXP(GDPpc * T4323(-0.23)/1000)) * $J4787 + (1-0.09)*demand_t-1
  ```

  This is a Gompertz curve with partial adjustment. The constant -5.897 is hardcoded. Sat_pass = `Transport1 ownership saturation point*(1 - freight share)`; J4787 = `MAX(1, actual/expected)`.
- Demand is clamped to growth of [-0%, +7.5%] a year (row 4787).
- Freight: the same Gompertz with Sat x freight share (row 4899).
- 2-3 wheelers: the ownership hump from row 2169, clamped to [-10%, +7.5%].
- Additions = demand - stock after scrappage; split new/used by `s_used`; then by technology using the choice shares (rows 4823-4826).

### 3.7 Buses (rows 5305-5318)

- Base-year bus fuel (rows 2140-2143) is scaled by a ratio of passenger quantities, which is mis-referenced (see bug B6).
- Electric buses: base fossil bus energy x electricity share.

### 3.8 Calibration

1. **Step 1** (row 5170): bottom-up fuel use from data (ownership x VKT_data / fuel economy) is compared with the energy balance per fuel. The ratios are Q5170:Q5173 (Egypt: gasoline 3.30, diesel 1.70, LPG 1, gas 3.87). They are aggregated into vehicle-class VKT scale factors by fuel-use shares (U/V/W5170 = 2.67 / 1.70 / 3.30). **All VKT per vehicle is multiplied by these factors**, so the Egypt calibrated passenger VKT is about 26,400 km per vehicle instead of the data's 9,900.
2. **Step 2** (E5325-E5328): the remaining fuel-specific residual is applied to total fuel use by fuel (Egypt: gasoline 1.234, diesel 0.858, gas 1.142). The same factor also multiplies the VKT outputs (5333-5335) and the vehicle-type fuel use (5339-5351).
3. **Range anxiety**: an external Solver/VBA goal seek makes the calculated EV sales share in 2025 match the actual. The results are stored in Transport3 (Egypt row 60). The match is not exact: the passenger difference G60 = 0.0009 against an actual of 0.0015.
4. **Vehicle ownership**: `J4787 = MAX(1, actual/expected)`, which is only an upward calibration (see bug B3).

### 3.9 Response to prices and income

- **Fuel prices** act through four channels:
  - VKT (`_el_dem_*` on cost per km).
  - New fuel economy (`|_el_eff_*|` on price per liter incl. feebate).
  - TCO, which shifts EV shares and the ICE fuel mix.
  - Electricity price (lagged), through BEV TCO and VKT.
- **Income** acts through:
  - The Gompertz ownership target (partial adjustment 0.09).
  - VKT income elasticity: 0.1 for passenger and freight, -0.4 for 2-3 wheelers.
  - The discount rate.
  - The 2-3 wheeler hump.
  - The freight share.
- **Policies represented**:
  - Carbon tax, fuel taxes and fuel price reform: via the retail prices in rows 2589 etc.
  - Feebates (rate per tCO2 + pivot): both as a $/vehicle purchase adjustment and as a per-liter wedge in the fuel-economy response.
  - Carbon price (`L2375*L2404`): enters the feebate rate.
  - Distance-based tax ($/km, ramped).
  - EV purchase subsidy (ramped).
  - Ad-valorem purchase tax for ICEV and BEV.
  - VAT and customs changes for BEVs.
  - Charging-station subsidy.
- **Not represented**: a fuel-economy standard (only as a shadow price via MTInputs 248, and only in the elasticity model); mode shift; congestion feedback.

## 4. Data inputs and Egypt availability

| Input | Location | Egypt in NoPropData? |
|---|---|---|
| Fuel shares by vehicle type, fuel economy (all classes), ownership (passenger, light, freight, cycle), EV/BEV purchase and stock shares, VKT (passenger, light, freight, cycle), used share, import duties, import shares, charging stations, saturation point, tax wedge, occupancy, congestion, speed, road maintenance, fatalities | Transport1 rows 238-241 (EGY, 2022-2025) | **Yes, all populated** (LPG freight and gas freight shares = 0; BEV cycle 2022 = 0). Examples: ownership passenger 52.6 and light 7.18 per 1,000; fuel economy gasoline 13.6, diesel 13.7, light 6.96, diesel freight 1.83 km/l; VKT passenger 9,024, light 16,285, freight 48,630, cycle 4,088 km; EV purchase share 0.03% → 0.14%; used share 50.6%; customs ICE 60.9% / BEV 43.3% |
| Vehicle purchase prices | Transport2 rows 1123-1141 (EGY, 2022-2040) | **Yes**. ICEV passenger 13,709 → 24,666; BEV passenger 28,609 → 21,181; freight ICE 70,753 vs BEV 298,464; cycle 1,498 vs 3,701 |
| Range-anxiety calibration | Transport3 row 60 (Egypt) | **Yes**: 78,639 / 440,799 / 1,108 |
| BEV fuel economy of new vehicles | Manual inputs J375:AC377 (global hardcoded) | Yes (5.33, 0.714, 24.2 km/kWh in 2022) |
| BEV-light, BEV-freight and BEV-cycle fuel economy paths; charging-station $/port | Mitigation rows 2051, 2095, 2122, 2170 (hardcoded) | Yes (global) |
| Policy and parameter settings | Dashboard rows 61-98, 542-558 | Yes (all policies 0 in the Egypt file) |
| Energy balance road fuel use 2022 | Mitigation F583:W602 | gso 7,577.3, die 10,207.6, nga 541.7 ktoe, LPG 0, electricity 0 |
| Retail prices, power prices, GDP, population | Mitigation rows 2589..2641, 3617/3646, 444/428/2446 | Yes (computed) |
| Elasticities | Elasticities sheet via Mitigation K299-K334 | Yes |

**Conclusion: a complete working Egypt dataset can be extracted from the NoPropData file.** It consists of Transport1 EGY rows, Transport2 EGY rows, Transport3 row 60, the Dashboard parameters, the Manual inputs rows 375-377 and the hardcoded Mitigation rows 2051/2095/2122/2170. The cached xlsb values give a full reference run of the engineer model for both scenarios, even though Egypt uses "Elasticity". Caveat from earlier work: the NoPropData price block differs from the proprietary price vintage.

Cached Egypt results (ktoe):

| Year | Gasoline: engineer | Gasoline: elasticity (used) | Diesel: engineer | Diesel: elasticity (used) |
|---|---|---|---|---|
| 2022 | 7,577 | 7,577 | 10,208 | 10,208 |
| 2025 | 6,911 | 6,995 | 9,302 | 9,452 |
| 2030 | 10,157 | 8,022 | 14,282 | 10,532 |
| 2035 | 16,286 | 9,079 | 22,912 | 11,604 |
| 2041 | 25,754 | 10,396 | 36,357 | 12,889 |

Other Egypt engineer results:
- The engineer baseline more than doubles by 2035, driven by the Gompertz ownership catch-up (stock 55 → 106 per 1,000 by 2035, at the 7.5% a year cap).
- EV share of new passenger sales: 0.15% (2025) → 21% (2035) → 41% (2041).
- Road electricity: 2 → 1,471 ktoe (2035).
- Policy scenario (carbon tax): gasoline 2035 13,486 (engineer) versus 7,220 (elasticity).

## 5. Bugs and oddities

**B1. `($C2227 > 1)` instead of `($C2173 > 1)`**: rows 4451 (passenger distance tax) and 4720 (2-3 wheeler EV subsidy). C2227 is the text "res", and text > number is TRUE in Excel, so these policies are also active in the baseline. (The value is 0 in Egypt.)

**B2. Freight income growth switches row**: row 4487 is `=L4463` up to AA, then `=AB2455` from AB (2038) onwards. Row 2455 is "coal producer-side subsidies", so freight VKT income growth is zero from 2038.

**B3. Ownership calibration only upwards**: `J4787 = MAX(1, actual/expected)` (also J4903). For Egypt, actual 57.8 is below the Gompertz 138.9, so there is no downward scaling and the stock is pulled up 7.5% a year. The "Actual" in I4787 uses column **N (2024)** although data run to 2025 (O). The same N-column hardcoding appears in H4787, `$N2168` (freight-share cap) and J2169.

**B4. Ownership cannot fall**: the max annual decrease T4328 = 0, so the 2023-2025 decline in the data is followed by flat or rising demand. (P4787 = 59.25 versus O = 55.12: a jump in the first projection year, because the closing stock O4750+O4758 ≠ the demand base.)

**B5. Huge VKT calibration factors**: VKT per vehicle is scaled by 2.67 (passenger), 1.70 (freight) and 3.30 (2-3 wheelers), so passenger VKT is about 26,400 km per vehicle. The Transport1 ownership × VKT × fuel economy data explain only about 30-60% of Egypt's road fuel use. Step 2 then rescales again (1.23 gasoline, 0.86 diesel). The VKT output (5333 ff.) is multiplied by the *gasoline* factor for passenger and 2-3 wheelers, and by the diesel factor for freight.

**B6. Bus block off by one row / wrong rows**:

```
L5310 = L5191*$E5310/1e3   (label "Gasoline fuel use", but 5191 = LPG VKT)
L5311 = L5192 ...          (label "Diesel", but 5192 = gas VKT)
L5312 = L5193 ...          (PHEV VKT)
L5313 = L5194              (blank row)
L5314 = L5219 * ...        (BEV vehicles, mln; not kWh)
```

Bus fuel (5315-5318) is then scaled by these meaningless ratios. The bus-share gross-up in 5170 `(1+M)` should be `1/(1-M)`.

**B7. Mislabelled emission-factor names**: G4376/G4419 use `_ef_co2_ker_ind_lit`, G4377/G4420 use `_ef_co2_jet_avi_lit`, and G4378/G4421 use `_ef_co2_die_pow_lit/26`. These names point to O1004 (diesel industry), O1005 (LPG industry) and O995 (gas per GJ). The values are plausible (2.68 / 1.77 kg/l), but the names are stale and fragile, and industry rather than road EFs are used.

**B8. Inconsistent elasticities and drivers**:
- `M5261` (BEV freight VKT) uses `$L4330` (2-3 wheeler income elasticity, -0.4) instead of `$K4330`.
- `M5295` (BEV 2-3 wheeler VKT) uses `M5292^el * M5292^$L4330`: the cost ratio twice, and no GDP term.
- `M5232` uses `L5126` while its siblings use `L5230`.
- Freight depreciation `M4646` switches from `$K4329` (column L) to `M4531` (passenger discount rate, M+).
- Freight PV uses `$K4329` = the average **power-sector WACC** (I2988:I2996) as the consumer discount rate.

**B9. PHEV sales share is negative**: `L4850 = L4845 - L4805` subtracts the blended passenger/light BEV share from the passenger-only PHEV+BEV share. The light BEV share of 0.66% exceeds the passenger EV share of 0.03%, giving -0.07%. PHEV TCO (4555) includes the BEV range anxiety (so about 100k $).

**B10. Charging-station subsidy inputs are mislabelled and ramp incorrectly**: Dashboard rows 95-98 are labelled start year/start level/target year/target level, but the formula (4343) uses G97 as the start year, G95 as the start level, G96 as the target level and G98 as the target year. The ramp also starts accumulating before the start year and is not capped at the target year (only `MIN(1,...)`).

**B11. Lags and timing**:
- The EV electricity price is the previous year's power price (an intended circularity workaround).
- 2055 uses `K789` (2021) against L-year gasoline.
- The feebate lags (4407, 4435, 4448 "lagged") use the previous year's intensities.
- The ICE mix in 4360 uses the previous year's ownership.

**B12. Hardcoded literals**:
- -5.897 (Gompertz); /26 (gas to liter); ×9 (kWh to l-gasoline-equivalent, PHEV); 0.5 halving in the insurance annuity; /15 (row 4348, station life).
- Own- and cross-price elasticities `AVERAGE(-1.72,-1.27,-1.08,-0.99)` and `AVERAGE(0.71,0.43,0.51,0.64)`.
- BEV fuel economy paths (2051, 2095, 2122, Manual inputs 375-377); charging $/port (2170).
- BEV-light fuel economy of 1.4 km/kWh is implausibly low (it drags the blended passenger/light value to 5.33).

**B13. 2171 "Change in vehicle ownership"**: the numerator includes M2037 but the denominator omits L2037. The row is unused.

**B14. Freight VKT inconsistency**: the TCO uses Transport1 `average vkt freight` = 48,630 km (clamped to ≥ 50,000), while the fuel-use VKT is the derived 8,091 km × 1.70. Row 2117 M+ scales freight VKT by the *passenger* VKT ratio.

**B15. Unused inputs**:
- U4324 ("difference between discounted and average VKT").
- Rows 4380-4384 are used for fuel economy, but rows 4457-4461 (cost per km change) are used only when Dashboard!Q551 = "Yes".
- The `Data available` row 2089 = 2025 is not used to locate the last data column (N is hardcoded).

**B16. Transport (externalities) sheet**:
- Freight VKT in the policy block, `Transport!I249 = IF($D239=1, I$117, I$134)`, points at row 134 (electricity fuel economy, policy) instead of 135 (freight VKT, policy). Rows 169 and 249 should reference 117/135.
- The sheet always uses **engineer** VKT and fuel economy, even when TrModel = "Elasticity", so the welfare and externality results are inconsistent with the fuel use actually used.
- The LPG rows give #DIV/0! for Egypt (zero LPG road use).

**B17. Text "years" hardwired in the input block**: rows 2017-2031 use the L/M/N columns as Share/ktoe/bln liter rather than years, which breaks the year-column convention. Data lookups exist only for L-O (2022-2025); 2026+ rely on `ISNUMBER` blanks.

**B18. Methodology note versus implementation** (`tm.md`, from the Transportation_methodology.docx):
- The note says ICEV prices rise with income and discount rates run from 10% to 30%. The implementation takes prices from Transport2 and uses discount rates of 5-15%.
- The note says VKT income elasticity is 0.05 and driving elasticities are -0.3/-0.2. The implementation uses 0.1/-0.4 and `_el_dem` (-0.4/-0.3).
- The note says maintenance varies with wages. In the implementation it is a fixed $/km.

## 6. Existing repository material

- `coded` (Python CPAT) has **no transport engineer module**. Transport appears only as sector codes (`rod`, `ral`, `avi`, `nav`), the externality codes `acc`/`con`/`rdm`, the scenario name `VEHICLE_FUEL_ECONOMY` in `constants.py`, and the elasticity-based road fuel use in `components/energy_consumption/ec.py` (the same equation as Mitigation 5396-5402, with notes on legacy bugs for road biofuels).
- `excel_ai/plans/TODO.md` item 6 lists "transport detail (section 5, key inputs 15, sheets Transport1-Transport3)" as later work.
- `CAVEATS.md` v0.13/v0.14 notes that the legacy transport trajectory (falling in 2024, then rising steeply) differs from the prototype. This is consistent with the legacy run using the *elasticity* model with the exogenous shock in row 2439 (-20.8% in 2023), not the engineer model.
- The mitigation v3.4 docs mention transport only at sector level (`legacy_comparison_v6_4.md`, `LegacyBugFixes.md` L22 on navigation).
- The methodology note "Methodology for Modelling the Road Transportation Sector" is `data/source/Transportation_methodology.docx`.
