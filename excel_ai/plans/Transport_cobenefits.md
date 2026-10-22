# transport externalities (accidents, congestion, road damage)

Status: planned, not built (user 2026-10-19: after plan 1 and before or after plan 2, as the user decides). Decisions D1-D9 in section 7 are for the user; D1 (source of vehicle-km: legacy engineer model, elasticity-consistent, or switch with TrModel) is the key one. Research below: legacy map, data, settings, cached Egypt values, bugs and issues, prototype mapping, step plan.

## 1. Where legacy computes it

### 1.1 Map

| Where | Rows | What |
|---|---|---|
| Transport, A. Description | 1-24 | Text box only |
| Transport, B. Key assumptions | F28:F47 | Literal parameters: F30 `_tran_scenario` = "price"; F40 `_tran_years_SRLR` = 5; F41 0.57 multi-vehicle share of 4-wheeler deaths; F42 0.25 external share of multi-vehicle accident cost; F43 0.5 external share of road maintenance; F44 0.7 external share of congestion time (**unused**); F45 4 marginal/average congestion; F46 0.12 USD/km global road damage; F47 "Yes" (use F46) |
| Transport, B. Elasticities | 51-87 | Tran_Elast lookups (SR, LR, default) for congestion all, weekday and peak. Only `e_congestion_gdp` (H64 = 0.459) and `e_congestion_pop` (H65 = 1.140) feed results. The SR-LR dynamic elasticity (rows 63, 76, 87, 196, 276) feeds only the chart helper row 394 |
| Transport, B. Country data | 91-98 | Transport1 by country and year (array INDEX/MATCH): fatalities (91), maintenance spending (92), congestion avg and peak (93, 94), occupancy (95, unused), tax wedge (D96, first year), free-flow urban speed (D97), share of deaths that are 2-4 wheeler occupants (D98) |
| Transport, B. Macro | 102-108 | GDP growth from Mitigation 16166 (baseline), also used in the policy block; policy GDP 16173 unused. Population from UNPop (104), growth (105). Urban pop (106, unused). Hourly earnings = `'Air pollution'!K855`/8 (107). VSL = `'Air pollution'!K741` (108). Air pollution ends in 2040; 2041 is extrapolated as AA*AA/Z |
| Transport, B. Inputs from Mitigation | 112-157 | Block E of Mitigation, rows 15724-15823: engineer fuel economy by fuel, freight and total VKT (baseline 112-118, policy 130-136); fuel shares 120-128 and 138-146; driving and efficiency margins 148-157 |
| Transport, C. Baseline block (D159 = 1) | 162-237 | VKT, accidents, congestion, travel time, road damage, per-unit $/l |
| Transport, D. Policy block (D239 = ScenarioNum) | 242-317 | Same rows, +80 |
| Transport, E. Results for Mitigation | 321-351 | Per-unit $/l by fuel, `mf.1` and `mf.2`, by code lookup (IFERROR -> 0) |
| | 354-370 | Welfare: levels, changes 356, 360, 364, travel-time value 368-370 |
| Transport, F. Results for charts | 372-457 | Titles, $/l in YearDistn (H394:H398), VKT (404-406), deaths (414-418), congestion (426-435), travel time (442-444), road damage (450-452) |
| Transport | 459-728 | Historical scatter (Tran_Scatter, country list) |
| Mitigation | 128-133 | $/l (`=Transport!I322` ...), feeding Pigouvian tax rows 154-155 (ScenarioDefinition `AddEfficientTaxes`, default No) |
| Mitigation | 15724-15823 | Block E: transport inputs to the sheet (by output code from the engineer block and the switched energy totals) |
| Mitigation | 17733-17735 | Welfare `wel.rod.aci/con/dmg.usd` (= Transport I356, I360, I364). 17737 sum; 17740 `wel.rod.pct`; chart rows 17745-17749 |
| Mitigation | 17771-17779 | Social cost by externality: transport $/l (`tran.acc/con/rdm.cost.gso/die.1`), totals incl. climate (17720-17721) and air pollution (17759-17760) |
| Mitigation | 17788-17789 | FFS "environmental benefits, Harberger" for road gasoline and diesel: ($/l climate + air + accidents + congestion) x change in transport fuel (not in the welfare total; not exported) |
| Mitigation | 17804-17826 | Subsidies: externalities in implicit subsidies (17808, 17820 include transport $/l, baseline `mf.1`) |
| Mitigation | 17977-18006 | Efficient prices by component, scenario 2 (`mf.2`): accident (17980, 17995), congestion (17981, 17996), road damage (17997); Pigouvian tax 17989, 18004 |
| LiveOutputs | 885-897, 899-909, 273-299, 1224+ | Transport effects, welfare, efficient prices, subsidies (section 1.6) |
| Dashboard | 561-604 | 4 x 4 transport charts (section 1.6) |

### 1.2 Equations (one scenario s; baseline s = 1)

**Accidents**
- Deaths: `D_s(2022)` = Transport1 fatalities; then `D_s(t) = D_s(t-1) x VKT_s(t)/VKT_s(t-1)`. The 2023-2025 data are not used.
- External deaths: `Dx = D x sh4 x 0.57 x 0.25 + D x (1 - sh4)`, with sh4 = 0.62 (D98).
- Fatal cost: `Dx x VSL / 1e9` (USD bn).
- Non-fatal cost = fatal cost x `0.049 x (Dx/D)^-2.56` (literal; 0.3416 for Egypt).
- `ACC_s` = fatal + non-fatal. Per km: `a = ACC/VKT`. It is identical in both scenarios (deaths scale with VKT), so `a(t) = a(2022) x VSL(t)/VSL(2022)`.

**Congestion**
- Average congestion `c(t)`: data 2022-2024 (row 197 is filled only I:K), then `c(t-1) x (1+g)^0.459 x (1+n)^1.140`. Here g is **baseline** GDP growth and n population growth, the same in both scenarios.
- Speed = free-flow speed / (1 + c/100).
- Delay hours = VKT/speed - VKT/free-flow speed.
- Value: `hours x wage_h x (1 - tax wedge)`. The note says "80% of after tax wages", but the formula has no 0.8 (see section 5).
- `CON_s = 4 x value`. Per km `k = CON/VKT` does not depend on VKT or the scenario.

**Road damage**
- `RDM_s = 0.12 x freightVKT_s` (F47 = "Yes").
- The country option (F47 = "No") uses maintenance spending x 0.5 / freight VKT, with data 2022-2024 then scaled by freight VKT.

**Per liter of fuel f** (gso, die, lpg, nga; ecy per kWh)
- `e_f = (cost per km) x FE_f x dm_f/(dm_f+em_f) x shT_f`.
  - FE_f: engineer average fuel economy of the stock.
  - dm and em: driving and efficiency elasticities. For diesel, LPG, gas and electricity they are weighted by engineer passenger/freight fuel use (Mitigation 15736-15745).
  - shT_f: road share of total use of fuel f (switched model).
- Road damage, diesel: `0.12 x FE_die x dm/(dm+em) x shFreight_die x shT_die`.
- Computed per scenario. The baseline (`mf.1`) feeds Mitigation 128-133, 17771-17776 and subsidies; the policy (`mf.2`) feeds efficient prices 17977+.

**Welfare (bn USD, + = gain)**
- `wel.rod.aci = ACC_1 - ACC_s = a x (VKT_1 - VKT_s)`
- `wel.rod.con = k x (VKT_1 - VKT_s)`
- `wel.rod.dmg = 0.12 x (frVKT_1 - frVKT_s)`

Checked against the cache: 2031 0.005817 x 30.58 = 0.1779; 0.008986 x 30.58 = 0.2747; 0.12 x (20.62 - 19.03) = 0.1916.

**Monetisation against the change in fuel use**
- The legacy welfare does not use the $/l values. It uses the engineer change in VKT directly.
- $/l x change in fuel appears only in:
  - the FFS rows 17788-17789: transport fuel ktoe change x liters per ktoe;
  - implicit subsidies: $/l x consumption;
  - efficient prices: $/l as price components.

### 1.3 What depends on the parked engineer model (section 5b) and what does not

| Input | Source in legacy | Engineer-dependent? |
|---|---|---|
| Total VKT path, baseline and policy (rows 118, 136) | 5b distance (legacy 5336; prototype `trkmt`) | **Yes**: the denominator of deaths per km, delay hours, and the **policy change in VKT (all welfare)** |
| Freight VKT (117, 135) | 5b (5334; prototype `trkm` fre) | **Yes**: road damage level and change |
| Average fuel economy by fuel (112-116, 130-134) | 5b (5356-5373; prototype `trafg`, `trafo`, `trafe`) | **Yes**: every $/l value |
| Diesel/LPG/gas/electricity passenger-freight split (15727-15735) | 5b fuel use by class (prototype `trfcp`, `trfcf`, `trfcc`, `trfce`) | **Yes**: margin weights and the freight share of diesel |
| Road share of total fuel (15759-15781) | Switched model (`ener`) | No (follows TrModel) |
| Elasticities dm, em | `_el_dem_*_rod`, `_el_eff_*_rod` (prototype Elasticities, section 5 parameters) | No |
| VSL, wages, congestion, fatalities, speed, tax wedge, population, baseline GDP growth | Air pollution, Transport1, UNPop, Mitigation | No |

- prototype 5b is computed in every scenario whatever TrModel is, so legacy can be replicated today. But the default welfare would then depend on a model the user parked (I28, I61).
- An elasticity-consistent alternative (section 7, option B) needs from 5b only base-year (data-calibrated) quantities, or nothing at all if FE comes from Transport1.

---

## 2. Data tabs

| Legacy tab | Used for | In prototype? | Action |
|---|---|---|---|
| Transport1 | Fatalities, maintenance spending, share of deaths 2-4 wheeler occupants, total and peak congestion, urban travel speed, tax wedge (occupancy unused) | **Yes** (legacy table, `TrKey`, `TrYr`, `TrVal`); the columns are present (cols 16-21, 87-95 of `legacy_Transport1.csv`) | Only new lookups (`Inputs` block or section-18b data rows) |
| Tran_Elast (221 x 54, `_tran_elasticities`, `_tran_elastcountries`, `_tran_elastnames`) | `e_congestion_gdp`, `e_congestion_pop` (results); SR/LR elasticities (charts only) | **No** | New legacy table under `DATA_TRAN->>` (NORMS 1.5: unchanged, keys right); small |
| Tran_Scatter (124 x 23) | Historical scatter charts only | No | Skip (decision D7) |
| Notes | Text (econometrics of Tran_Elast) | No | Not needed; cite in method note |
| Air pollution (module sheet) | VSL (741: options 734-738), daily earnings (855), deflator to ResultsYear (718), PPP ratio (714 from WEO PPPPC/NGDPD) | No (prototype section 15 has emissions only, no health/VSL) | Rebuild VSL and earnings rows (they are also the future air-pollution health module's inputs) |
| ILO (603 rows; key `Earnings-<unit>-<iso>`, years 2018-2023) | Monthly earnings (USD) / `WorkDays` (ScenarioDefinition 334 = 20) | **No** | New legacy table (DATA_OTHER or with the air-pollution tabs) |
| Countries col X "VSL country grouping" | VSL group | **Yes** (`legacy_Countries_cells.csv` col 24) | Lookup only |
| Air pollution D45:E51 (group VSL in mln 2022 PPP USD and GDPpc 2022 PPP: OECD 7.1/56224, EU 8.4/58043, USA 8.5/77178, HIC 7.9/62989, UMIC/LMIC/LIC 1.1/13576) | VSL transfer | No | New small parameter table (TransportParams or a VSL parameter block) |
| WEO PPPPC, NGDPD; UNPop; population; deflator | VSL, earnings growth | **Yes** | Reuse |
| Air_Data (labour share), WB (GNI) | Earnings fallback when no ILO data; VSL options GNI x 100 / x 160 | No | Only if those options are replicated (D3) |

---

## 3. Settings that drive it

| Setting | Where | Options | Egypt default (legacy) |
|---|---|---|---|
| TrModel | ScenarioDefinition 340 | Elasticity / Engineer | Elasticity (the Transport sheet ignores it) |
| VSLMethod | ScenarioDefinition 327 | GNI*100, GNI*160, Transfer from Group (+ "PPP"/"USD" from Air pollution G36), Manual | "Transfer from Group" (G36 = USD), i.e. "Transfer from Group, USD"; the G (Defaults) column says "Transfer from OECD" |
| VSLManual | ScenarioDefinition 328 | number (constant ResultsYear PPP USD) | 500,000 |
| VslElSource, VslEl | ScenarioDefinition 329-330 | | **#REF!** in the legacy file; VSL income elasticity is hard-wired to 1 in Air pollution 736 |
| WorkDays | ScenarioDefinition 334 | days/month | 20 |
| ApLabSh | ScenarioDefinition 335 (Air pollution G82) | earnings fallback | 0.65 |
| YearDistn | ScenarioDefinition 304 | | 2030 (chart "externality per liter" H394:H398) |
| AddEfficientTaxes, ClimateEffTax, AddEfficientTaxesPhaseInYears, ExternalityAddVAT, YearFuelPrices | ScenarioDefinition 217, 216, 212, 218, 282 | | No*, Yes*, 5, Yes*, 2025: consumers of the $/l (Pigouvian tax, efficient prices); not in the prototype |
| Transport sheet literals | Transport F30, F40-F47 | | price, 5, 0.57, 0.25, 0.5, 0.7 (unused), 4, 0.12, Yes |
| Literals inside formulas | Transport 181, 107 | | 0.049, -2.56; 8 hours/day |
| Elasticities | `_el_dem_gso_rod` -0.4, `_el_eff_gso_rod` -0.4; diesel mix -0.340 (both) | | Elasticities tab |

Nothing for transport externalities is on 'Manual inputs'.

---

## 4. Cached Egypt values (for tests)

Static inputs:
- Transport1 2022: fatalities 5,610.47; maintenance 213.38 (2023: 314.96; 2024: 323.10); congestion 9.37 / 47.42; free-flow speed 59.05 km/h; tax wedge 0.20; share of deaths that are 2-4 wheeler occupants 0.62.
- Elasticities: e_congestion_gdp 0.45901, e_congestion_pop 1.14045.
- Daily earnings 2022: 8.4584 USD (ILO 169.168/20).
- VSL 2022: 387,389.73.
- H394:H398 (2030): accidents gso 0.03955, die 0.01163; congestion gso 0.05739, die 0.01687; road damage die 0.14839.

| Cell | Item | 2022 | 2025 | 2027 | 2030 | 2031 | 2035 | 2041 |
|---|---|---|---|---|---|---|---|---|
| T108 | VSL (constant 2026 USD) | 387,390 | 256,759 | 297,411 | 361,662 | 364,405 | 408,204 | 481,756 |
| T107 | Hourly earnings (USD) | 1.057 | 1.107 | 1.175 | 1.311 | 1.355 | 1.54 | 1.851 |
| T168/T248 | VKT all vehicles, base / policy (bn km) | 220.8 / 220.8 | 203.8 / 203.8 | 231.7 / 226.5 | 314 / 290.9 | 353.7 / 323.2 | 580.1 / 507.4 | 1,270 / 1,066 |
| T169/T135 | Freight VKT base / policy (bn km) | 12.01 / 12.01 | 11.12 / 11.12 | 13.5 / 13.23 | 18.32 / 17.11 | 20.62 / 19.03 | 33.16 / 29.45 | 66.96 / 57.49 |
| T173/T253 | Road deaths base / policy | 5,610 / 5,610 | 5,177 / 5,177 | 5,885 / 5,755 | 7,976 / 7,390 | 8,987 / 8,210 | 14,738 / 12,890 | 32,253 / 27,089 |
| T417 | Cumulative averted deaths | 0 | 0 | 129.9 | 1,405 | 2,182 | 7,788 | 29,076 |
| T200 | Congestion, average (%; both scenarios) | 9.37 | 9.728 | 10.47 | 11.79 | 12.24 | 14.15 | 17.39 |
| T210 | Congestion, peak (%) | 47.42 | 49.23 | 53 | 59.66 | 61.92 | 71.61 | 88.03 |
| T185 | Accident external cost per km (USD; both) | 0.006184 | 0.004099 | 0.004748 | 0.005773 | 0.005817 | 0.006516 | 0.00769 |
| T220 | Congestion external cost per km (USD; both) | 0.005369 | 0.005836 | 0.00667 | 0.008377 | 0.008986 | 0.01181 | 0.01745 |
| T184/T264 | Accident external cost base / policy (bn) | 1.366 / 1.366 | 0.8353 / 0.8353 | 1.1 / 1.076 | 1.813 / 1.679 | 2.058 / 1.88 | 3.78 / 3.306 | 9.763 / 8.2 |
| T219/T299 | Congestion external cost base / policy (bn) | 1.186 / 1.186 | 1.189 / 1.189 | 1.545 / 1.511 | 2.63 / 2.437 | 3.179 / 2.904 | 6.85 / 5.991 | 22.15 / 18.6 |
| T233/T313 | Road damage base / policy (bn) | 1.441 / 1.441 | 1.335 / 1.335 | 1.62 / 1.587 | 2.199 / 2.053 | 2.475 / 2.283 | 3.979 / 3.533 | 8.036 / 6.899 |
| T322/T323 | Accidents, gasoline $/l base / policy | 0.04142 / 0.04142 | 0.02781 / 0.02781 | 0.03239 / 0.03239 | 0.03955 / 0.03988 | 0.03995 / 0.04049 | 0.04537 / 0.04733 | 0.05551 / 0.06129 |
| T324/T325 | Accidents, diesel $/l base / policy | 0.0126 / 0.0126 | 0.008334 / 0.008334 | 0.009408 / 0.009507 | 0.01163 / 0.01221 | 0.01178 / 0.01255 | 0.01359 / 0.01552 | 0.01676 / 0.02145 |
| T333/T334 | Congestion, gasoline $/l base / policy | 0.03596 / 0.03596 | 0.0396 / 0.0396 | 0.04551 / 0.0455 | 0.05739 / 0.05787 | 0.0617 / 0.06254 | 0.08223 / 0.08577 | 0.1259 / 0.139 |
| T335/T336 | Congestion, diesel $/l base / policy | 0.01094 / 0.01094 | 0.01187 / 0.01187 | 0.01322 / 0.01335 | 0.01687 / 0.01771 | 0.0182 / 0.01939 | 0.02463 / 0.02813 | 0.03801 / 0.04866 |
| T344/T345 | Road damage, diesel $/l base / policy | 0.146 / 0.146 | 0.1457 / 0.1457 | 0.146 / 0.1479 | 0.1484 / 0.1572 | 0.1493 / 0.1608 | 0.1533 / 0.1774 | 0.1604 / 0.2078 |
| M17733 (T356) | Welfare: averted accidents (bn) `wel.rod.aci.usd` | 0 | 0 | 0.02427 | 0.1332 | 0.1779 | 0.4739 | 1.563 |
| M17734 (T360) | Welfare: reduced congestion (bn) `wel.rod.con.usd` | 0 | 0 | 0.03409 | 0.1933 | 0.2747 | 0.8589 | 3.546 |
| M17735 (T364) | Welfare: reduced road damage (bn) `wel.rod.dmg.usd` | 0 | 0 | 0.03242 | 0.1454 | 0.1916 | 0.446 | 1.137 |
| M17740 | Transport co-benefits, share of GDP (`wel.rod.pct`) | 0 | 0 | 0.0001369 | 0.0006114 | 0.0007965 | 0.001833 | 0.004975 |
| M17737 | Total national welfare (bn, legacy sum) | -6.9e-06 | 0.1242 | 2.56 | 9.67 | 11.58 | 19.39 | 31.51 |
| M17778 | Total externalities gasoline $/l (incl. climate, air pollution) | 0.1078 | 0.08863 | 0.1026 | 0.1271 | 0.1322 | 0.1622 | 0.2181 |
| M17779 | Total externalities diesel $/l | 0.2786 | 0.2443 | 0.2616 | 0.2944 | 0.2995 | 0.334 | 0.37 |
| M17810/M17822 | Efficient price gso / die (subsidy block, base) | 1.167 / 1.178 | 1.021 / 1.031 | 1.048 / 1.06 | 1.051 / 1.077 | 1.054 / 1.081 | 1.124 / 1.152 | 1.255 / 1.253 |

Use in tests:
- The engineer inputs of the cache (Transport rows 112-157) are in `data/mvp_legacy_extracts/legacy_transport_reference.csv` (legacy rows 5333-5373) and in `transport_model_ref.legacy_test(run, fix=frozenset())`.
- A Python reference fed with those inputs should reproduce every row above to rounding.
- The prototype 5b has the fixes L25-L41, so prototype values match legacy only in the base year and in the scenario-independent per-km costs.

---

## 5. Legacy bugs (proposed L items, next free L124+) and issues to replicate (I69+)

### 5.1 Bugs

**B-a. Policy freight VKT points at the electricity fuel economy (survey B16).**
- Cells: Transport I249:AB249 `=IF($D239=1,I$117,I$134)`; label C249 = "Road electricity - fuel economy"; latent in I169 (`I$134` branch).
- Effect: row 309 country-specific maintenance extrapolation (only when F47 = "No") and code `tranfre.vkt.2`. None on the default welfare: rows 311 and 313 read 135 directly.
- Fix: the scenario's freight VKT.

**B-b. #DIV/0! where a fuel has no road use (survey B16).**
- Cells: Transport 188, 223, 235, 268, 303, 315: `SUM(margins)=0` for LPG gives #DIV/0!. It is masked to 0 by IFERROR in 326-351, but a total would break.
- Effect: none for Egypt.
- Fix: 0 when the margins sum to 0 or road use is 0.

**B-c. Value of time: label says 80% of the after-tax wage, formula uses 100%; F44 is a dead input. Candidate, confirm.**
- Cells: Transport 218/298: D218 note "80% of after tax wages", formula `wage_h x hours x (1 - wedge)` with no 0.8. F44 = 0.7 ("portion of travel time lost in congestion that is an externality") is never used.
- Effect: congestion costs and welfare x0.8 (x0.56 if F44 also applies), i.e. -20% (-44%).
- Options: replicate (and register as an issue), or fix.

**B-d. Road damage per liter of diesel uses the wrong fuel economy. Candidate, confirm.**
- Cells: Transport 234/314: `0.12 x FE_die(avg, passenger+freight; 6.3 km/l) x dm share x shFreight x shT`. The cost is per **freight** km, so the km per liter must be freight km per freight liter (about 1.8 km/l in Transport1), or freight km / road diesel liters.
- Effect: Egypt 2031 legacy 0.149 $/l against about 0.065 $/l with freight km per road diesel liter (20.6 bn km / 12.1 bn l = 1.71 km/l), so road damage per liter is about 2.3x too high. It flows into total externalities, implicit subsidies and efficient prices; the welfare levels are unaffected.

**B-e. Daily earnings not deflated to ResultsYear USD. Candidate.**
- Cells: Air pollution K850 (= ILO 2022 USD), labelled "constant 2026 $USD"; later years grown with real GDP per capita. The VSL is deflated (K718).
- Effect: congestion costs about 11% low (deflator 1.124).

**B-f. VSL elasticity inputs are #REF!.**
- Cells: ScenarioDefinition F329:F330 (VslElSource, VslEl). The income elasticity is hard-wired to 1 in Air pollution 736.
- Effect: none on values; dead inputs.
- Fix: drop, or wire up later with the air-pollution module.

**B-g. Accident chart row uses the full VSL with the wrong sign.**
- Cells: Transport I418: `-VSL x averted deaths` (all deaths, full VSL, opposite sign), titled "Change in externality cost from road accidents" (Dashboard R577). LiveOutputs and welfare use 356 (external share).
- Effect: chart only.
- Fix: `= ACC_1 - ACC_s`.

**B-h. LiveOutputs export gaps and mislabels.**
- Road-damage welfare (17735, `wel.rod.dmg.usd`) is not exported (rows 901-903).
- E885/886 codes `tran.vmt.*` while the sheet codes are `tran.vkt.*`.
- H887 'vmt' for deaths.
- D903:D909 take the unit of the row above (E17734 for 17736, ...).
- Fix in the prototype LiveOutputs.

**B-i. FFS diesel row: wrong conversion factor and road damage left out. Only if the FFS block is rebuilt.**
- Cells: Mitigation 17789: diesel converted with `_conv_ktoe_liter_gso`, and road damage 17776 omitted. The block is not in the welfare total and not exported.
- Same class as the section-18 note "diesel and kerosene converted with the wrong factors".

**B-j. Unit and scenario labels (cosmetic).**
- Transport 370, 442-444: "Million" but values are USD bn.
- 264-265: "baseline" in the policy block.
- Mitigation 15771-15775: "baseline" on policy rows.

### 5.2 Design issues to replicate (I items, unless the user decides otherwise)

| # | Issue |
|---|---|
| I-a | Externalities use **engineer** VKT, fuel economy and class splits even when TrModel = Elasticity (survey B16), so welfare is inconsistent with the fuel use actually modelled. Egypt: engineer VKT -8.6% in 2031 (-16% in 2041) against switched road gasoline -12.9% and diesel -14.3% (-27% and -29% in 2041). The legacy note D168 says "simplified approach for now = change in fuel consumption". **This is decision D1** |
| I-b | Deaths scale 1:1 with VKT from the 2022 data (2023-2025 data unused). Congestion level does not respond to the policy: the elasticities are computed but unused, and the policy block uses baseline GDP growth. Congestion cost moves only with VKT |
| I-c | Congestion data used only for 2022-2024 (row 197 filled I:K), then grown with the GDP and population elasticities (Egypt 9.4% to 17.4% by 2041) |
| I-d | Literals: 0.049 x ratio^-2.56 (non-fatal), 0.57, 0.25, 0.5, 4, 0.12 USD/km (not deflated, constant), 8 h/day; tax wedge and free-flow speed of the first year only. Make them parameters (TransportParams) |
| I-e | Per liter: the all-vehicle average $/km is applied to every fuel. The driving share uses baseline margins; the diesel margins are weighted by engineer passenger/freight use. $/l is per liter of **all** use of the fuel (x road share) |
| I-f | The baseline $/l (`mf.1`) feeds Pigouvian taxes and implicit subsidies; the scenario $/l (`mf.2`) feeds efficient prices |
| I-g | VSL "Transfer from Group, USD": group VSL x (PPP GDPpc_t / group GDPpc) x deflator / (PPP/market ratio)_t. It is volatile with the exchange rate (Egypt 387k -> 257k over 2022-2025). Air pollution stops in 2040; 2041 is extrapolated geometrically |
| I-h | Welfare = change in the level of external costs (rectangle), not a triangle; 2-3 wheelers are in total VKT; road damage only for freight; country maintenance option unused by default |

---

## 6. Mapping onto the prototype

### 6.1 Inputs already available
- Road and total fuel use by fuel, per scenario: `ener` road rows, section 5 and totals.
- Elasticities `εU` (usage) and `εF` (efficiency) of road fuels: section 4 parameters; legacy `_el_dem`/`_el_eff`.
- 5b engineer rows per scenario: `trkm` (pas, fre, cyc), `trkmt`, `trfcp`, `trfcf`, `trfcc`, `trfce`, `trafg`, `trafo` (die, lpg, nga; fix B22), `trafe`.
- GDP growth `gdp` (baseline via `.ref`), population `pop`, `pop.g`, deflator `defl`.
- WEO PPPPC and NGDPD; Countries col X; Transport1 (`TrKey`, `TrVal`); liters per ktoe constants; `wel.usd` (section 18).

### 6.2 New
1. **Data**: Tran_Elast (legacy table, DATA_TRAN); ILO (legacy table); VSL group table and Transport literals as TransportParams keys (`tex.*`).
2. **Inputs block**, `Inputs_tex` (NORMS 1.5 rule 2c): Transport1 lookups (2022-2025), the two congestion elasticities, the group VSL parameters.
3. **Mitigation section 18, new lettered sub-block "18b Welfare and externalities, road transport"**. About 45 rows per scenario group; NORMS 3c.4 allows a module sheet instead, see D2. Proposed codes:

| Code | Content |
|---|---|
| `vsl` | VSL, constant ResultsYear USD |
| `wageh` | Hourly earnings |
| `tex.vkt`, `tex.vktf` | Total and freight VKT, per D1 |
| `tex.fe.<f>` | Fuel economy by fuel |
| `tex.dsh.<f>` | Driving share dm/(dm+em) |
| `tex.rsh.<f>`, `tex.fsh.die` | Road share of fuel use, freight share of diesel |
| `tex.dth`, `tex.dthx` | Deaths, external deaths |
| `tex.acc` | Accident external cost, USD bn |
| `tex.acckm` | Accident cost per km |
| `tex.cng`, `tex.cngp` | Congestion average and peak, % |
| `tex.spd`, `tex.hrs` | Speed, delay hours |
| `tex.con`, `tex.conkm` | Congestion external cost, per km |
| `tex.rdm` | Road damage, USD bn |
| `tex.acc.<f>`, `tex.con.<f>`, `tex.rdm.die` | $/l (gso, die; lpg, nga, ecy per D5) |
| `wrod.aci`, `wrod.con`, `wrod.dmg` | Welfare = `.ref` level - level (3c rule 2: differences that feed `wel` are scenario rows) |
| `wrod.all` | Sum of the three |

   Then `wel.usd = wcli.nat - eff - mfc + wrod.all`; new `wel.rod` (% of GDP); legacy chart order cli, air (later), rod, eff.
4. **LiveOutputs** (legacy codes, scenario appended):
   - `mit.wel.rod.aci.usd`, `mit.wel.rod.con.usd`, `mit.wel.rod.dmg.usd` (fixing B-h), `mit.wel.rod.pct`;
   - `tran.acc.cost.gso/die.1`, `tran.con.cost.gso/die.1`, `tran.rdm.cost.die.1` (from scenario 1 rows), with the `.2` series as efficient-price components later;
   - `tran.vkt.*` (fixing the `vmt` codes), `tran.deaths.*`, `tran.acc.avd.cum.*`, `tran.congestionP.*`.
5. **Charts**: VKT, deaths and averted deaths, congestion (all, peak), road damage, externality per liter in YearDistn (D7).
6. **Python reference**: `transport_ext_ref_v6_4.py`.
   - Pure functions for section 1.2.
   - `legacy_test()` feeds the cached legacy inputs (Transport rows 91-157 from the xlsb or the reference CSVs) and must reproduce rows 162-370 and Mitigation 17733-17740 for every year (switch `FIXES` off).
   - `ALL_FIXES` for the prototype.
7. **Checks** in `check_full.py`:
   - recompute 18b in every group from workbook values (`check_results_memos` style);
   - `wrod` = 0 in scenario 1;
   - per-km costs equal across groups (I-b);
   - `wel.usd` identity;
   - paste test (`check_paste`) for groups 4-7;
   - all-country clone (`check_allcountry`) with the Tran_Elast and ILO rows;
   - LAMBDA test group, if 18b rows get LAMBDAs (e.g. `EXTPERL` for $/l).
8. **Docs and register**: `ResultsSections_Method` section 18b; `Transport_vs_Legacy` (B16 resolved or kept); L items B-a..B-j, I items I-a..I-h, LegacyDiff rows; remove "transport co-benefits" from the Q42 "not as rows" list.

---

## 7. Proposed plan

| Step | Content | Size |
|---|---|---|
| 0 | User decisions D1-D9 (below); register L and I items | small |
| 1 | Python reference `transport_ext_ref_v6_4.py`: equations of 1.2, legacy mode reproducing the cache (all rows, 2022-2041, both blocks) and the fix switches; effect sizes of each candidate fix (B-c, B-d, B-e) and of option A vs B for Egypt | medium |
| 2 | Data: Tran_Elast and ILO legacy tables (extract script, `DATA_TRAN`/`DATA_OTHER`, names, keys right, all-country capacity), VSL group table and literals into TransportParams; `Inputs_tex` lookups | medium |
| 3 | VSL and hourly-earnings rows (Transfer from Group USD/PPP + Manual, per D3), WorkDays, deflator, PPP ratio from WEO; 2041 rule | medium |
| 4 | 18b physical rows: deaths, accident cost, congestion path, delay hours, congestion cost, road damage; per-km costs | medium |
| 5 | VKT, fuel-economy and share inputs per D1 (A: read 5b `trkmt`, `trkm`, `trafg`, `trafo`, `trfc*`; B: per-liter x change in road fuel with a base-year FE; C: switch) and the $/l rows | medium |
| 6 | Welfare rows `wrod.*`, `wel.usd`/`wel.rod` update, summary memo; LiveOutputs codes; Charts | small-medium |
| 7 | Checks (recompute, scenario-1 zero, paste, all-country, LAMBDA group if any); build and quick check; compare with the cache (base year exact; legacy-mode reference) | medium |
| 8 | Docs: ResultsSections 18b, Transport_vs_Legacy, Replicated/NotReplicated, LegacyDiff, CAVEATS, TODO | small |

The efficient prices, implicit and explicit subsidies, the Pigouvian tax and the FFS block are **not** in this plan. They also need the air-pollution $/l (legacy Air pollution module, not in the prototype). Step 5 delivers the transport $/l rows those blocks will read later.

### Decisions for the user

**D1. VKT source (the key decision).**
- (A) **Legacy**: read engineer 5b VKT, fuel economy and splits in every scenario, whatever TrModel is. This replicates the cache's mechanics; register I-a. The default welfare then depends on the parked engineer model (I28, I61).
- (B) **Elasticity-consistent**: welfare = Σ_f $/l (road liter, driving share, no road-share factor) x change in road fuel f, with FE from the 5b base year or Transport1. Egypt 2031: accidents 0.083, congestion 0.128, road damage 0.40 (0.18 with B-d fixed), against legacy 0.178 / 0.275 / 0.192. This is a departure and needs a U/I entry.
- (C) Follow TrModel: A under Engineer, B under Elasticity. NORMS default is A; C is the likely best compromise.

**D2. Placement.** Sub-block 18b on Mitigation (recommended, about 45 rows) or a module sheet with Mitigation's group geometry (NORMS 3c.4).

**D3. VSL options.** Default plus Manual only, or all five (GNI x 100 and x 160 need WB GNI data). The earnings fallback (Air_Data labour share) is needed only for countries without ILO data.

**D4. Bug candidates.**
- Fix: B-a, B-b, B-g, B-h, B-j (clear bugs).
- Confirm: B-c (0.8 VOT and F44), B-d (road-damage fuel economy), B-e (earnings deflator).
- B-f and B-i go to the air-pollution module work later.

**D5. Fuels for $/l.** Gasoline and diesel only (what legacy Mitigation reads and exports), or also LPG, gas and electricity (computed in legacy, unused).

**D6. Scope.** Confirm that efficient prices, subsidies, the Pigouvian tax and the FFS rows wait for the air-pollution health module; the transport $/l rows are delivered now.

**D7. Charts.** Which Dashboard charts to port (VKT, fatalities, congestion, travel time, road damage, $/l in YearDistn); skip the Tran_Scatter historical plots (recommended).

**D8. Tran_Elast.** Import the whole legacy table (NORMS 1.5, recommended) or only the two congestion elasticities.

**D9. Literals.** Transport literals (F41-F47, 0.049/-2.56, 8 h) become TransportParams keys, not ScenarioDefinition rows (NORMS 4: no new ScenarioDefinition functionality).

