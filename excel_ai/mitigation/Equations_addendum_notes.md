# Builder notes for the equations addendum (v9.0)

Research notes behind [`Equations_addendum.md`](Equations_addendum.md): legacy 465 cell evidence for every new bug and issue, cell plans, the build.py hook points, missing inputs, typed Egypt values and cached legacy values for regression. Register codes are final (L173-L222, I101-I146, LD80). Legacy 465 Mitigation years: L = 2022 ... AE = 2041 (K = 2021).

## A. Reverts to legacy and R13

## REV notes (for the builder): reverts to legacy and R13

Legacy = CPAT 1.0pre_465_NoPropData (Mitigation; policy block = baseline row + 6316). Cached run: Egypt, scenario 2 =
carbon tax 0 -> 5 $/t real 2026-2040 (Linear*, 5.36 in 2041), GDPEndogenous Yes*, no fuel price reform, no feebates,
no methane fee.

### 1. Legacy bugs (cell plans, JSON in the style of legacy/bugfixes/data/fixes_other_mitigation_2.json)

| Id | Pri | Cells | Formula now -> intended | Egypt effect |
|---|---|---|---|---|
| L171 | Medium | Mitigation L167:AE180 | final `0` (option **No**) -> hold `$G+$J*(Target-Start)` | none (Linear*, no reform) |
| L173 | Low | L167:AE180 | Percentage `$K167*L167` -> `(1+$K167)*L167` (col L: hold) | none |
| L174 | Low | K2001:K2004 | `($J-$I)/($J$1977-$I$1977)` -> `IF($J$1977>$I$1977,...,0)` (#DIV/0! when start = target) | none |
| L175 | Low | G1988:G1989 | flag tests industry rates `$I$2004:$J$2004` while the rate reads row 2003 -> `$I$2003:$J$2003` | none |
| L172 | High | O747:O752, O755:O758, Q747:Q752 | `AVERAGE(INDEX(_prices_main,...))` -> `... * INDEX($K$725:$AE$725,MATCH(<year read>,$K$724:$AE$724,0))` | fixed supply cost: gas ind 8.534 -> 9.553 $/GJ, gas res 13.406 -> 14.719, gas pow 7.607 -> 8.570, coal ind 3.972 -> 4.212, oil 0.123 -> 0.140 $/l |

Option list of ExtendCarbonPriceBeyondOutro (checked): Dashboard L20 data validation `"No,Linear*,Percentage"`;
MTInputs F265 (name; E265 = Dashboard!$L$20, default `Linear*`); Mitigation C67 label "(No/Linear*/Percentage)". So
the "any other option" of L171 is exactly **No**. The carbon price (row 2248) under No adds 0 to last year (holds),
under Percentage adds $F$69 x last year: the reference for both fixes.

Cell plans:

```json
[
 {
  "id": "L171",
  "pri": "Medium",
  "title": "Fuel price reform drops to 0 after the target year unless the path continues (option No)",
  "where": "Mitigation L167:AE180 (fuel price reform paths, shared by both blocks)",
  "why": "ExtendCarbonPriceBeyondOutro has three options (Dashboard L20 validation list No, Linear*, Percentage; Mitigation C67). From the target year on, any option but Linear* and Percentage (i.e. No) returns 0: the reform price increase disappears in and after the target year, although No means 'do not continue to rise'. The carbon price with the same switch (row 2248) holds its level under No (adds 0 to last year's price).",
  "fixes": [
   {
    "cell": "L167",
    "now": "=IF(L$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(L$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(L$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*K167,0)))",
    "new": "=IF(L$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(L$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(L$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*K167,$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "fill": "L167:L180",
    "policy": "none (rows above 2173 are shared by both blocks)"
   },
   {
    "cell": "M167",
    "now": "=IF(M$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(M$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(M$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*L167,0)))",
    "new": "=IF(M$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(M$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(M$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*L167,$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "fill": "M167:AE180",
    "policy": "none (rows above 2173 are shared by both blocks)"
   }
  ],
  "ref": "Row 2248 (carbon price, same switch: No = hold the level). Hold level = the linear value at the target year ($G+$J*(target-start)) = the target price H when target > start (J = 0 otherwise, as the linear branch).",
  "effect": "None for Egypt (no fuel price reform; switch Linear*). With option No the reform keeps its target level instead of falling to 0 from the target year (prices, demand, revenue).",
  "note": "The test is t < target (strict), so the target year itself already takes the No/Percentage branch; with the fix the target year gets the hold level = the linear value, so the strict test no longer matters. Column L reads K (the rate column) as 'previous year' in the Percentage branch; see L173.",
  "status": "fix"
 },
 {
  "id": "L173",
  "pri": "Low",
  "title": "Fuel price reform 'Percentage' continuation multiplies by the growth rate, not by 1 + rate",
  "where": "Mitigation L167:AE180 (Percentage branch), rate K167:K180",
  "why": "K is the annual percentage increase ((H/G)^(1/n) - 1). After the target year the Percentage branch returns $K x last year's value, e.g. 5% of the price increase instead of 105%: the path collapses. The carbon price with the same switch adds $F$69 x last year to last year (row 2248). Column L (first year) reads K167, the rate itself, as last year's value.",
  "fixes": [
   {
    "cell": "L167",
    "now": "=IF(L$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(L$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(L$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*K167,$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "new": "=IF(L$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(L$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(L$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod),$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "fill": "L167:L180",
    "policy": "none (rows above 2173 are shared by both blocks)"
   },
   {
    "cell": "M167",
    "now": "=IF(M$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(M$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(M$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",$K167*L167,$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "new": "=IF(M$166<FuelPriceIncreaseStartYearMitMod,0,IF(OR(M$166<FuelPriceIncreaseTargetYearMitMod,ExtendCarbonPriceBeyondOutro=\"Linear*\"),$G167+$J167*(M$166-FuelPriceIncreaseStartYearMitMod),IF(ExtendCarbonPriceBeyondOutro=\"Percentage\",(1+$K167)*L167,$G167+$J167*(FuelPriceIncreaseTargetYearMitMod-FuelPriceIncreaseStartYearMitMod))))",
    "fill": "M167:AE180",
    "policy": "none (rows above 2173 are shared by both blocks)"
   }
  ],
  "ref": "Row 2248 (carbon price Percentage: K2248 + $F$69*K2248). 'now' is the formula after the L171 fix (apply L171 first).",
  "effect": "None for Egypt (no fuel price reform; Linear*). With Percentage, the reform path grows at the rate after the target year instead of falling to rate x price.",
  "note": "Column L only reaches the branch if the target year is 2022 or earlier; there it takes the hold level.",
  "status": "fix"
 },
 {
  "id": "L174",
  "pri": "Low",
  "title": "Feebate slope divides by (target year - start year): #DIV/0! when they are equal",
  "where": "Mitigation K2001:K2004 (and the paths L2001:AE2004 that read it)",
  "why": "The slope has no guard, unlike the fuel price reform slope (J167 = IF($E$164>$E$163, ..., 0)): a feebate that starts in its target year gives #DIV/0! in every year, and the error reaches prices, fuel use and revenue.",
  "fixes": [
   {
    "cell": "K2001",
    "now": "=($J2001-$I2001)/($J$1977-$I$1977)",
    "new": "=IF($J$1977>$I$1977,($J2001-$I2001)/($J$1977-$I$1977),0)",
    "fill": "K2001:K2004",
    "policy": "none (rows above 2173 are shared by both blocks)"
   }
  ],
  "ref": "Row 167 J (fuel price reform guard). With J1977 = I1977 the path then jumps to the target rate from the start year (L2001: t > target gives $J2001).",
  "effect": "None for Egypt (feebate years 2027/2035, rates 0).",
  "note": "",
  "status": "fix"
 },
 {
  "id": "L175",
  "pri": "Low",
  "title": "Feebates of food & forestry and services: on/off flag from the industry rates, rate from the residential rates",
  "where": "Mitigation G1988:G1989 (rates L1988:AE1989 read row 2003)",
  "why": "Rows 1988-1989 (group 'Commercial') take the residential feebate rate (L$2003, L2003) but their flag G tests the industry rates ($I$2004:$J$2004), so a residential-only feebate does not reach them and an industry-only feebate switches them on at the residential rate (0).",
  "fixes": [
   {
    "cell": "G1988",
    "now": "=IF(MAX($I$2004:$J$2004)>0,1,0)",
    "new": "=IF(MAX($I$2003:$J$2003)>0,1,0)",
    "fill": "G1988:G1989",
    "policy": "none (rows above 2173 are shared by both blocks)"
   }
  ],
  "ref": "Row 1987 (residential: flag and rate both row 2003). The prototype maps food and services to the residential feebate group (SUBSECTORS column 7).",
  "effect": "None for Egypt (no feebates).",
  "note": "Labels F1985/F1986 (tra.nav/tra.avi) are swapped; cosmetic.",
  "status": "fix"
 },
 {
  "id": "L172",
  "pri": "High",
  "title": "Margins and domestic production cost added in nominal USD to real prices",
  "where": "Mitigation O747:O752, O755:O758 (margins), Q747:Q752 (production cost); read by the fixed portion of supply costs J/K 2453, 2476, 2499, 2522, 2545, 2568, 2591, 2614, 2637, 2660, 2683, 2706 and the policy copies (+6316)",
  "why": "The supply costs and retail prices of the IMF dataset are converted to real USD of the results year with the CPI index row 725 (L773: ...*L$725), but the margin (mit.mar, read at 2024 for coal and gas, at FirstYearCalculations for oil products) and the domestic production cost (mit.coa/nga.prod.cost, FirstYearCalculations) are not: the fixed portion (margin + share produced domestically x cost) is nominal and the floating portion (sp - fixed - ps) absorbs the difference.",
  "fixes": [
   {
    "cell": "O747",
    "now": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & 2024, _prices_country_years,0),MATCH(O$745 & \".\" & $G747,_prices_codes,0)))",
    "new": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & 2024, _prices_country_years,0),MATCH(O$745 & \".\" & $G747,_prices_codes,0)))*INDEX($K$725:$AE$725,MATCH(2024,$K$724:$AE$724,0))",
    "fill": "O747:O752",
    "policy": "none (rows above 2173 are shared by both blocks)"
   },
   {
    "cell": "O755",
    "now": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(O$745 & \".\" & $G755,_prices_codes,0)))",
    "new": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(O$745 & \".\" & $G755,_prices_codes,0)))*INDEX($K$725:$AE$725,MATCH(FirstYearCalculations,$K$724:$AE$724,0))",
    "fill": "O755:O758",
    "policy": "none (rows above 2173 are shared by both blocks)"
   },
   {
    "cell": "Q747",
    "now": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(\"mit.coa.prod.cost\",_prices_codes,0)))",
    "new": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(\"mit.coa.prod.cost\",_prices_codes,0)))*INDEX($K$725:$AE$725,MATCH(FirstYearCalculations,$K$724:$AE$724,0))",
    "fill": "Q747:Q749",
    "policy": "none (rows above 2173 are shared by both blocks)"
   },
   {
    "cell": "Q750",
    "now": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(\"mit.nga.prod.cost\",_prices_codes,0)))",
    "new": "=AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(\"mit.nga.prod.cost\",_prices_codes,0)))*INDEX($K$725:$AE$725,MATCH(FirstYearCalculations,$K$724:$AE$724,0))",
    "fill": "Q750:Q752",
    "policy": "none (rows above 2173 are shared by both blocks)"
   }
  ],
  "ref": "Row 725 (CPI index, results year = 1, by year of row 724) and its use in L773:AE830. O759, O760 (typed 0) unchanged.",
  "effect": "Egypt fixed supply cost ($/GJ, $/l): coal pow 1.324 -> 1.404, res 7.944 -> 8.424, ind 3.972 -> 4.212; gas pow 7.607 -> 8.570, res 13.406 -> 14.719, ind 8.534 -> 9.553; gasoline/diesel/LPG/kerosene 0.123 -> 0.140. The historical pre-tax price is unchanged (data); the floating part falls by the same amount, so projected supply costs follow international prices less.",
  "note": "The year 2024 of the coal and gas margins is typed (issue I101, replicated); the conversion uses the CPI index of the year actually read.",
  "status": "fix"
 }
]```

### 2. Issues (replicate)

- **I101** Margin of coal and gas read at a typed year (O747:O752 `_Country_code & 2024`), while the oil-product
  margins (O755:O758), the production cost and the domestic-production share read FirstYearCalculations. Replicate
  (user decision R13): Inputs_prices column `mary` = 2024 for coal/gas, BaseYr otherwise (better: a Settings cell
  "MarginYear" = 2024, documented as legacy's typed year).
- **I102** Fuel price reform: the test is `t < target` (strict) and the Percentage rate K for a zero start price
  uses (H/(G+J))^(1/n) - 1 (growth from the first-year step). Replicate (with L171 the strict test has no effect).
- **I103** Feebates constant at the target rate after the target year whatever ExtendCarbonPriceBeyondOutro says
  (rows 2001-2004: `IF(t>J1977,$J,...)`). Replicate (user decision LD10).
- Known, not re-reported: L24 (GDP growth vs level; prototype E95 fixes it), L66 (additional efficiency group), I47
  (now reverted), I74 (methane calibration on data), L69 (lag row of the GDP block).

### 3. Unregistered prototype departure found (needs a decision; proposed: as legacy)

- **LD80 Production cost weight.** Legacy 465 fixed supply cost of coal and gas = margin + **share produced
  domestically** (P747:P752 = MAX(0,MIN(1,`mit.coa.prod` / `mit.nga.prod`)), Egypt gas 0.899) x production cost
  (rows 2454/2477/2500/2523/2546/2569, label "share dom prod"). The prototype (build.py 7092, check_full.py 765) and
  coded CPAT (`coded/cpat_model/mitigation/prices/prices.py` `__set_fixsp`) use the **bucketed pass-through** `pccb`
  (Egypt gas 0) instead. Egypt gas fixed cost: legacy 8.53 $/GJ nominal (ind), prototype about 2.6 real. Not in the
  register (no LD entry). REV.md R13.2-R13.3 adopt legacy (dsh); if the user prefers the coded rule, keep pccb.

### 4. Where it hooks in build.py

- **LD1**: line 174 `SUBSECTORS` row `('foo', ..., 'bld', 'srv', ...)` -> elasticity sector `'ind'`; update the comment
  (v0.11) and `ISSUES.md`/register LD1 -> "Aligned". Inputs columns `esec`, `eY`, `eU`, `eF`, `a` follow (Inputs sheet,
  build_inputs ~6960). `psec` (`ind`) and `AEG` (default 3, line 3240) already as legacy. Python reference:
  check_full.py elasticity sector of foo. Not covered by the decision (left as is): the shadow-price/feebate group of
  food (prototype feebate sector `res`, SUBSECTORS column 7; legacy uses `shp.*.ind` rows 2379/2382 and the industry
  regulation group row 2349 for food but the residential feebate rate row 1988).
- **LD10**: `pol_calc` branch `key.startswith('fpr.') or key.startswith('fb.')` (lines 9917-9922) and `path_formula`
  (9874): fpr -> new formula LD10.3 reading `{col}${R_POL["ExtendCarbonPriceBeyondOutro"]}` and the previous column
  of the same row (first year: no previous column, use the hold level); fb -> `call('PATH', ..., 'FALSE')` /
  `path_formula(..., linear_ext='"No"')` (flat after T1). New LAMBDA `FPRPATH` next to `PATH` (4583, 4859). Doc rows
  E24, E62 (Formulas), E2, E3 (Equations.md), docstring of `path_formula` ("the one default for all paths") and
  register LD10 -> "Aligned" (the ETS benchmark/cap parts of LD10 are not in this decision; keep). Inputs present:
  `fpr.yr0`/`fpr.yr1` (MT rows 140/141, `MT_ROWS_FIXED`), `fpr.s`/`fpr.f` (`_pol` ~597-600), `fb.*` (629),
  `ExtendCarbonPriceBeyondOutro` (`CP_PARAMS`, 391). Missing: none.
- **I47**: `fis.rev` (11566-11570): `ch4.revf` -> `ch4.rev`. Remove `CH4S_SRC` (328), `CH4S_STORE` (329), the GHG block
  "Methane fee in the fiscal space" (3279-3281), docs 4046-4057, `ch4.emf`/`ch4bs.chk`/`ch4.revf` branches
  (11298-11316), the BaselineCO2 rows dg/bm (6303, 12064, 12082, 12158) and `R_POL['ch4bs.*']`. Keep the v6.2
  P_FIRST/P_LAST fix (3143) and `ref_formula` ending at the column: these keep every reference exact-year. Test:
  full recalculation (LibreOffice/Excel) with a methane fee and GDPEndogenous = Yes, no circular-reference warning.
  Register I47 -> replicated.
- **L172 / LD16**: Inputs_prices (`IP_COLS` 497-510; values 7086-7092): add `mary` (2024 for coa/nga, else
  `Settings!$C$7`), `dsh` (=MAX(0,MIN(1,`mit.<fuel>.prod` at PDomBase)) for coa/nga, else 0), `cpim` (CPI index of
  `mary`, row IP_CPI), read `mar` at `mary` (row `MATCH(CtryCode&mary,PDomKey,0)`), and
  `fixsp = (mar*cpim + dsh*pcost*bcpi)/gj`. Python reference check_full.py 763-766. Register LD16 -> "Aligned, L172
  fixed". Prices_dom holds EGY2024 (`mit.mar.nga.ind` 1.946 = legacy O752).

### 5. LD41 detail (data vintage)

| Data | Prototype source now | 465 | Result |
|---|---|---|---|
| International price forecasts (Mitigation 633-695) | `extract_data.py extract_int_prices` from 456 -> prices_int.csv | same rows | identical (1008 cells; 465 has text 'NA' in 2041 for IEA oil, IEA/EIA gas, prototype blank) |
| US CPI, deflator (rows 455, 452) | 456 -> weo_us.csv | same | identical |
| Domestic prices (Prices_dom) | CPAT_PriceModule_Data_1.xlsx + update_prices_egypt | Prices_dom A9:EL1062 | identical for EGY (372/380 cells; only `mit.spot.coa/nga`, junk in 465); 465 adds EGY2025 |
| Balances (sheet Balances rows 13+) | `extract_legacy_tables.py` from 456 -> legacy_Balances.csv | changed | 161 cells differ; TFC 61,682 vs 67,089 ktoe; resident 12,470 vs 13,702; food diesel 875.272 vs 927.02 |
| Base-year fuel use (energy_use.csv) | Kernel v1.6 Data_Energy (= 456 rows 583-602) | Mitigation 583-602 (from Balances) | changes with Balances |
| EFs (rows 980-1009), elasticities | 456 | not checked | re-extract and diff |

Re-extraction: point `LEGACY` of extract_data.py, extract_legacy_tables.py, extract_ecp/ets/gdp/ghg/power/transport.py
to `CPAT 1.0pre_465_NoPropData.xlsb` (row numbers: check `legacy/bugfixes/data/rowmap_456_465.json`; rows 452-455,
633-695, 980-1009 unchanged for the items checked), rebuild energy_use.csv from 465 (rows 583-602 cached, or Balances
with legacy's mapping, which extract_legacy_tables already implements for EnergyCons), rerun the build and compare.

### 6. Egypt cached values (legacy 465) for regression

LD58 benchmark: compare `gdp.eff` with row 14592 and the fiscal space with 14336 (shares, not %); LD58's register text
(175 $/t, 2030 -0.07%, 2035 +0.34%, 2040 +1.22%) does **not** match 465 (5 $/t; 2030 -0.0035%, 2035 +0.029%, 2040
+0.080%): it seems to come from another vintage; update the register. Baseline GDP-effect rows 8265-8276 are 0.
Columns 2022 ... 2041.

| Row | Variable | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8567 | cptraj.2 carbon price ($/t real) | 0 | 0 | 0 | 0 | 0 | 0.357143 | 0.714286 | 1.07143 | 1.42857 | 1.78571 | 2.14286 | 2.5 | 2.85714 | 3.21429 | 3.57143 | 3.92857 | 4.28571 | 4.64286 | 5 | 5.35714 |
| 14212 | mf.new.usd.2 methane fee revenue (bn) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14328 | rev.new.usd.2 total revenue (bn) | -31.9708 | -26.6775 | -41.2289 | -40.3212 | -45.2162 | -42.4058 | -41.6236 | -41.6147 | -41.4239 | -40.3662 | -39.5433 | -39.0874 | -38.3114 | -37.3269 | -35.9831 | -34.3142 | -32.2801 | -29.8494 | -27.3908 | -26.9416 |
| 14335 | fiscal revenue %GDP, own | -0.0584506 | -0.0470057 | -0.0709432 | -0.0664622 | -0.0714993 | -0.0639662 | -0.0594932 | -0.0565261 | -0.0536683 | -0.0499081 | -0.0466801 | -0.0440779 | -0.0412913 | -0.0384699 | -0.0354801 | -0.0323868 | -0.0291783 | -0.025853 | -0.0227433 | -0.0214568 |
| 14334 | fiscal revenue %GDP, scenario 1 | -0.0584506 | -0.0470069 | -0.0709443 | -0.0664632 | -0.0715003 | -0.0642205 | -0.0600452 | -0.0573578 | -0.0547644 | -0.0512291 | -0.0482064 | -0.0458136 | -0.0432205 | -0.0405792 | -0.0377557 | -0.0348145 | -0.0317437 | -0.0285429 | -0.0255456 | -0.0243615 |
| 14336 | fiscal space (additional, %GDP) | 0 | 1.26122e-06 | 1.07346e-06 | 1.00446e-06 | 1.02312e-06 | 0.000254312 | 0.000552026 | 0.000831706 | 0.00109606 | 0.00132099 | 0.00152631 | 0.00173567 | 0.0019292 | 0.00210929 | 0.00227562 | 0.00242761 | 0.00256539 | 0.00268986 | 0.00280237 | 0.00290473 |
| 14340 | additional revenue (bn US$ real) | 0 | 0.000715788 | 0.000623843 | 0.000609384 | 0.000647023 | 0.168594 | 0.386217 | 0.612305 | 0.845995 | 1.06843 | 1.29295 | 1.53915 | 1.78997 | 2.04662 | 2.30788 | 2.57208 | 2.83811 | 3.10566 | 3.37502 | 3.64724 |
| 14341 | impulse (change in %GDP) | 0 | 1.26122e-06 | -1.58212e-07 | -2.38332e-08 | 5.95178e-08 | 0.000253336 | 0.000311052 | 0.000307099 | 0.000302767 | 0.00027502 | 0.000265041 | 0.000277632 | 0.000270327 | 0.000264507 | 0.000257609 | 0.000249357 | 0.000240469 | 0.000231729 | 0.000223661 | 0.000216795 |
| 14582 | gdp.exc.pct.2 | 0 | 0 | 0 | 0 | -2.20216e-08 | -9.37659e-05 | -0.000249386 | -0.000400114 | -0.000545717 | -0.000662825 | -0.000752779 | -0.000836396 | -0.000905965 | -0.000958351 | -0.000997292 | -0.00102596 | -0.00105102 | -0.00107445 | -0.00109605 | -0.00103591 |
| 14583 | gdp.pit.pct.2 | 0 | 0 | 0 | 0 | 4.46383e-09 | 1.90047e-05 | 4.23334e-05 | 6.46051e-05 | 8.33392e-05 | 9.85518e-05 | 0.000112903 | 0.000127586 | 0.000142684 | 0.000156935 | 0.000169638 | 0.000180938 | 0.000191482 | 0.000201537 | 0.000211318 | 0.000204554 |
| 14584 | gdp.cit.pct.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14586 | gdp.inv.pct.2 | 0 | 0 | 0 | 0 | 1.84505e-08 | 7.85538e-05 | 0.000180046 | 0.000278932 | 0.000365688 | 0.000444021 | 0.000524552 | 0.000619219 | 0.000721316 | 0.000840407 | 0.000968815 | 0.00110433 | 0.00123795 | 0.00136678 | 0.00149142 | 0.00154595 |
| 14587 | gdp.cur.pct.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14588 | gdp.tra.pct.2 | 0 | 0 | 0 | 0 | 1.90457e-09 | 8.10997e-06 | 2.36376e-05 | 4.28411e-05 | 6.13828e-05 | 7.81643e-05 | 9.33666e-05 | 0.000108384 | 0.000122967 | 0.000137823 | 0.000150379 | 0.000162025 | 0.000173227 | 0.000183924 | 0.000194316 | 0.000197473 |
| 14590 | net effect on GDP | 0 | 0 | 0 | 0 | 2.79734e-09 | 1.19026e-05 | -3.36883e-06 | -1.37359e-05 | -3.53064e-05 | -4.20874e-05 | -2.19574e-05 | 1.87933e-05 | 8.10009e-05 | 0.000176814 | 0.00029154 | 0.000421338 | 0.000551634 | 0.000677797 | 0.000801 | 0.000912075 |
| 14592 | gdp.cha.pct.2 effect on GDP | 0 | 0 | 0 | 0 | 2.79734e-09 | 1.19026e-05 | -3.36883e-06 | -1.37359e-05 | -3.53064e-05 | -4.20874e-05 | -2.19574e-05 | 1.87933e-05 | 8.10009e-05 | 0.000176814 | 0.00029154 | 0.000421338 | 0.000551634 | 0.000677797 | 0.000801 | 0.000912075 |
| 8758 | gdp.pre.lvl.2 (bn) | 546.971 | 567.539 | 581.153 | 606.679 | 632.401 | 662.941 | 699.636 | 736.204 | 771.85 | 808.812 | 847.114 | 886.779 | 927.831 | 970.29 | 1014.18 | 1059.51 | 1106.31 | 1154.58 | 1204.35 | 1255.62 |
| 8759 | gdp.pst.lvl.2 (bn) | 546.971 | 567.539 | 581.153 | 606.679 | 632.401 | 662.941 | 699.644 | 736.201 | 771.84 | 808.784 | 847.08 | 886.761 | 927.848 | 970.365 | 1014.35 | 1059.81 | 1106.75 | 1155.19 | 1205.13 | 1256.59 |
| 8761 | endogenous GDP change (t-1 effect) | 0 | 0 | 0 | 0 | 0 | 2.79734e-09 | 1.19026e-05 | -3.36883e-06 | -1.37359e-05 | -3.53064e-05 | -4.20874e-05 | -2.19574e-05 | 1.87933e-05 | 8.10009e-05 | 0.000176814 | 0.00029154 | 0.000421338 | 0.000551634 | 0.000677797 | 0.000801 |
| 8762 | gdp.pos.pct.2 growth | 0.0665135 | 0.0376028 | 0.023988 | 0.0439239 | 0.0423971 | 0.0482922 | 0.0553651 | 0.0522627 | 0.048405 | 0.0478521 | 0.0473139 | 0.0468026 | 0.0463119 | 0.0458427 | 0.0454071 | 0.0449904 | 0.0445888 | 0.0441877 | 0.0437825 | 0.0433743 |
| 5618 | ener.foo.tot.e.1 (ktoe) | 875.594 | 1065.07 | 1333.31 | 1360.75 | 1387.45 | 1418.46 | 1454.7 | 1489.27 | 1521.55 | 1553.94 | 1586.52 | 1619.31 | 1652.29 | 1685.45 | 1718.78 | 1752.29 | 1785.95 | 1819.77 | 1853.73 | 1887.84 |
| 11934 | ener.foo.tot.e.2 (ktoe) | 875.594 | 1065.07 | 1333.31 | 1360.75 | 1387.45 | 1412.79 | 1443.13 | 1471.56 | 1497.51 | 1523.34 | 1549.16 | 1574.98 | 1600.81 | 1626.66 | 1652.56 | 1678.51 | 1704.51 | 1730.58 | 1756.7 | 1782.86 |
| 5612 | ener.foo.die.e.1 | 875.272 | 1064.72 | 1332.9 | 1360.33 | 1387.01 | 1418.01 | 1454.23 | 1488.79 | 1521.05 | 1553.42 | 1585.99 | 1618.76 | 1651.72 | 1684.86 | 1718.18 | 1751.66 | 1785.31 | 1819.11 | 1853.05 | 1887.13 |
| 11928 | ener.foo.die.e.2 | 875.272 | 1064.72 | 1332.9 | 1360.33 | 1387.01 | 1412.34 | 1442.66 | 1471.08 | 1497.02 | 1522.83 | 1548.63 | 1574.43 | 1600.25 | 1626.09 | 1651.97 | 1677.9 | 1703.89 | 1729.93 | 1756.03 | 1782.18 |

Fixed portion of supply costs (legacy, constant 2022-2041, nominal as stored): coal pow 1.324, res 7.944, ind 3.972
(rows 2453/2476/2499); gas pow 7.60687, res 13.4059, ind 8.53387 (2522/2545/2568); gasoline/diesel/LPG/kerosene 0.123
(2591...). Fuel price reform rows 167-180 and feebates 2001-2004: all 0 (no policy).

## B. R1 inputs from air pollution and transport co-benefits; R2 social costs and benefits, full welfare

## R1R2 notes for the builder

Rows: l465.xlsb, by the sheets' year rows (Mitigation rows 112-206 and F10: K = 2021, L = 2022 … AE = 2041, checked on
rows 112, 16081, 17380, 17713; Transport I..AB = 2022..2041, row 321; Air pollution K..AC = 2022..2040, row 973).
The plans and build.py comments cite F10 rows from about 17600 on 15 rows lower (plan/build 17732 = l465 17717;
build "17636-17648" eff = l465 17621-17633; "17680-17713" SCC = l465 17665-17698). The plans' cached values are of
another run; the values below are the l465 cache (policy: small carbon tax from 2027; scenario 2).

### 1. Legacy bugs (proposed; none of these is in issues_register.py; plan IDs given where the plans proposed them)

| # | Cell(s) | Formula now | Intended | Egypt effect |
|---|---|---|---|---|
| L176 | Mit 17704 (`cc.code.oop.1`, label "damage/GJ") read by 17838, 17777, 17778, 17782 | L17704 = L$17698*$G17680, G17680 = L967*_conv_barrel_to_liter: **$/bbl**; L17838 = L17704 + L17753 ($/GJ); L17777 = -(L17704+L17748)*(…)*_conv_ktoe_to_gj/10^9 | climate cost per GJ: L17704/_conv_barrel_to_gj (6.12 GJ/bbl) | oop externality 2022 34.77 → 15.86 $/GJ; implicit oop subsidy 2022 11.19 → 5.11, 2030 28.78 → 11.01, 2041 42.65 → 16.26 bn; FFS oop rows 2030 0.301 → 0.151 bn |
| L177 | Mit 18090 (and 18102 = 18090) | =(L17740*L$16993/L$17003+L17743*L$16994/L$17003+L17748*L$16995/L$17003)*(_conv_ktoe_to_gwh/1000): $/GJ of fuel × generation share × 0.01163 (not GJ per kWh) | Σ_k cost_k × fuel use_k (GJ) / total generation (kWh) | 2022 0.01103 → 0.00882 $/kWh (-20%); R3 efficient electricity prices |
| L178 | Mit 17750, 17751 | L17750 = (L17738*L16911 + L17739*L16913 + L17740*L16914)/(…): industry cost weighted by power coal (16911), power cost by industry coal (16914); 17751 same for gas (16917 pow, 16920 ind) | L17738*L16914 + L17740*L16911 (and gas likewise) | coal other 2022 0.7475 → 2.374 $/GJ (no Egypt use); gas other 0.350 → 0.465 $/GJ (FFS nga.oth line, small) |
| L179 | Mit 17767, 17768, 17769, 17770, 17772 | 17767 (coal ind) Δ = L16911-L16850 (coal **power**); 17769 (coal pow) Δ = L16914-L16853 (coal **industry**); 17768 (coal res) Δ = L16912-L16851 (coal **transport**); 17770 (gas ind) Δ = L16917-L16856 (gas **power**); 17772 (gas pow) Δ = L16920-L16859 (gas **industry**) | each line its own sector: ind 16914-16853, res 16913-16852, pow 16911-16850; gas ind 16920-16859, pow 16917-16856 | the 5 lines 2030 0.0957 → 0.0989 bn, 2041 0.575 → 0.586 bn |
| L180 (plan T B-i) | Mit 17774 | =-(L17706+L17745+L17757+L17759)*(L16930-L16869)*_conv_ktoe_liter_gso/10^9 | _conv_ktoe_liter_die and + L17761 (road damage) | diesel road line 2030 0.0538 → 0.0658 bn |
| L181 | Mit 17897 | coal residential retail price =L17385 (gas industry price) | =L17386 | coal res explicit 2022 0.00103 → 0, implicit 0.00061 → 0.00040 bn |
| L182 | Mit 17906 | coal power retail price =L17386 (coal residential) | =L17388 | 0 (no coal power) |
| L183 | Mit 17866 | gas power externalities =L17679+L17743 (national SCC; every other line uses the global rows 17702-17709) | =L17703+L17743 | 0 while NSCC and GSCC sources agree (default Target) |
| L184 | Mit 17814 | LPG household share = IF(L17811>L17810,0,(L17810-MAX(L17811,L17807)))*L17812 (subsidy formula reading diesel rows and a blank row) = 0 | =L811 (0.99493) | LPG VAT 0 → 0.20 $/l; LPG implicit subsidy 2022 6.76 → 8.52, 2030 11.25 → 13.67, 2041 15.92 → 19.24 bn |
| L185 | Mit 17836 | oop household share =L820 (the oop **VAT rate** row) | household share of oop (no OilProductShares column: 0) | 0 |
| L186 | Mit 17831 | kerosene consumption L16879*_conv_ktoe_liter_die | _conv_ktoe_liter_ker (as 17629, 17776) | kerosene subsidy lines × conv_ker/conv_die (prototype: in PJ, no conversion) |
| L187 | Mit M17939:AE17943 | L17939 is the consumption-weighted supply cost, but M17939 =M16204 (diesel supply cost), M17943 =M17391 (gasoline retail), M17941 =SUM(M17939:M17940)*M$17787 | the L formulas copied right | electricity-other explicit 2030 0.228 → 0.044, implicit 0.069 → 0.004 bn |
| L188 | Mit 17950, 17951 | =L17948/K$16082 (GDP of the previous year: K16081 = 2021) | /L$16082 | explicit subsidy 2022 7.54% → 7.07% of GDP |
| L189 (plan AP B2) | Mit 17742 | ='Air pollution'!K4382 (deaths 15-64 per ktoe) | AP 4378 × 741 × time_factor × (1+1713) / 41868 | res. gas 2022 0.00148 → 0.0371 $/GJ |
| L190 (plan AP B3) | Mit 17746 | ='Air pollution'!$K$4314 (2022 for every year) | K$4314 relative | LPG 2030 0.675 → 0.689 $/l |
| L191 (plan AP B4) | Mit AB17738:AE17749 (=AA…), AD17717:AE17717 (=AC…) | unit costs held at 2037 from 2038; wel.air held at 2039 in 2040 | link AP to 2040 (AP has 2040); 2041 = 2040 (issue I112) | wel.air 2040 0.2856 → 0.3183 bn; diesel 2040 0.2887 → 0.3259 $/l |
| L192 (plan AP B12) | Mit 17739 | =IF(L16282/9127>0.1%,…) typed constant 9127 (≈ a year's residential total use) | residential coal / residential total of the year | 0 |
| I119 (was proposed as bug Lnew-R1R2-18; an issue: see R3) | Mit K124, K125 | =IFERROR(L18102,0), =IFERROR(L18090,0) in the 2021 column; L124:AE125 empty; L159 =L124*L$146, L160 =L125*L$146 | the formulas in L:AE | electricity Pigouvian tax always 0 (only with AddEfficientTaxes = Yes; for R3) |
| L193 (plan T B-b) | Transport 188, 223, 235 (+ policy rows) | #DIV/0! when a fuel has no class use (LPG), masked to 0 by IFERROR in 326-351 | 0 when the class use is 0 | 0 |

Not used by the equations, so not built: Transport I249 policy freight VKT reads the electricity fuel economy
(plan T B-a; only code `tranfre.vkt.2`). Pending user decisions from the transport plan (typed values here are as
legacy): B-c (value of time 80% of the after-tax wage, F44 0.7 unused: would scale `tran.con.km` by 0.8 or 0.56),
B-d (road damage per liter with the average diesel fuel economy: by the rule a bug, fix = freight km per road diesel
liter, about 2.3× lower `tran.rdm.cost.die`), B-e (earnings not deflated: `tran.con.km` × deflator ~1.124).
Plan AP B1 (adult incidence) is inside the typed v_PM and ĉ: if the user fixes it, the typed values must be
recomputed by a module run (they cannot be corrected by a factor).

### 2. Issues to replicate (proposed)

| # | Issue |
|---|---|
| I104 | Air-pollution unit costs are average damages (baseline deaths per µg/m3, plan AP I-b): Σ cost × Δuse = 0.322 bn in 2030 against legacy wel.air 0.057 bn (5.7×). Kept as legacy for social costs, subsidies, FFS and efficient prices; the welfare uses v_PM |
| I105 | wel.air linearised: v_PM is legacy wel.air / ΔPM2.5 of one policy run (2023-2026 from ΔC ≈ 1.5e-4 µg/m3, so noisy: 0.196-0.291); O3 deaths and YLD scale with PM2.5; household air pollution does not respond |
| I106 | Typed Egypt values: the AP and VSL options of the cached run (SourceAppSel = Manual-FASST in MTInputs F322 and Dashboard F429, VSL Transfer from Group, 3% discount, cessation lag Yes) are frozen; ScenarioDefinition rows 322-336 stay grey (inert). Other countries: the R1 issue of the plan |
| I107 | FFS lines value diesel in industry, power and "other" at the oil-product climate and AP costs; gasoline and diesel road lines take the transport sector; FFS uses the global SCC; FFS welfare is a separate measure, not in wel.usd |
| I108 | Electricity externalities blank in the subsidy block (implicit electricity subsidy = VAT gap only) |
| I109 | Subsidy-block VAT: the general rate (fuel-specific VAT rows 17790, 17802, 17813, 17824, 17835, 17855, 17892, 17929 read but unused), on the household share only; none on industry and power |
| I110 | Legacy computes subsidies (and the `.1` unit costs) for scenario 1 only; the prototype computes them in every group (group 1 = legacy) |
| I111 | Transport: I100 (engineer VKT whatever TrModel, cite); margins from scenario 1 (plan T I111); per-km costs scenario-independent, congestion not responding to policy (T I-b); welfare a rectangle, road damage only freight, 0.12 USD/km not deflated (T I-d, I-h) |
| I112 | AP horizon 2040: AP-derived typed values 2041 = 2040 (plan AP I-o) |

### 3. Where it hooks in build.py

- New section "17b. Inputs from air pollution and transport co-benefits": insert between section 17 and 18
  (`B_WEL = R_CPR['ecr'] + 2`, line ~3485; add a band, blocks with `layout_blocks`, a summary row, and an entry in
  `SECTION_GROUPS`). Typed rows (T1-T4) from a new data block (e.g. sheet Constants/Inputs_cob, source "legacy 465 AP
  row …, cached Egypt run"), year-indexed.
- Section 18 (`WEL_BLOCKS`, line 3468; `c18`, line ~11733): new blocks `cc.nat.*`, `cc.code.*`, `airpol.cost.ecy`,
  `airpol.cost.*.other`, `tot.ext.*`, `wel.air.usd`, `wel.rod.*`, `wel.air.pct`, `wel.rod.pct`, FFS (`env.ffs.*`,
  `wel.ffs`), subsidy blocks; change `fu == 'usd'` (wel.usd = wcli.nat + wel.air + wrod.* − eff.all − mfc.all) and
  the note at line ~11794 ("Air pollution and transport co-benefits come with their modules").
- Rename band headings: section 15 "15. Local air pollutants: outputs to the air pollution module"; section 5b
  (`B_TR`) "5b. Road transport: engineer model and outputs to the transport co-benefits module". No copies.
- Existing inputs: Settings 33-42 SCC (`scc.nat`, `scc.glo`), Inputs `gj`, `ef`, `osh` (Inputs_prices), VAT_WEO
  (Inputs_prices row IP_VATW), road elasticities `eldg`, `eldd`, `elfg`, `elfd` (trp.ela), 5b `trkmt`, `trkmf`,
  `trafg`, `trafo.*`, `trafe`, `trfcp.*`, `trfcf.*`, `trfcc`, `trfcep/f/c`, `ener`, `pe`, `gen`, electricity `dem`,
  `sc`, `rp`, `sp`, `atp`, section 15 `aps.<p>.<m>`, `gdp.usd`. Missing: the typed tables T1-T4 only. No new
  ScenarioDefinition input (AddEfficientTaxes, ExternalityAddVAT, ClimateEffTax are R3).

### 4. Typed values (T1-T4) and Egypt cached values for the regression test
Generated by `r12_extract.py` (scratchpad) from l465.xlsb. Rows marked "fixed" differ from the cached Mitigation rows
by the bug fix; the regression of the prototype against legacy must feed legacy quantities (VKT, ΔPM2.5, fuel use)
and apply the fixes listed above.
Check values: wel.air 2030 = 0.293071 × (42.2873 − 42.0933) = 0.056857; wrod.aci 2030 = 0.0059092 × (305.35 −
303.944) = 0.008309; wrod.con 2030 = 0.0083766 × 1.406 = 0.011779; wrod.dmg 2030 = 0.12 × (17.8425 − 17.7663) =
0.009145; acc gso 2022 = 0.0063295 × 13.393 × 0.5 × 1 = 0.042386 $/l.

#### T1. Air-pollution cost per unit of fuel, typed (`airpol.cost`), 2022-2040 from the AP sheet, 2041 = 2040

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| airpol.cost.coa.ind | AP 3924 ($/GJ) | 2.37614 | 1.92141 | 1.80008 | 1.64437 | 1.8678 | 1.91151 | 2.06488 | 2.20724 | 2.33711 | 2.37559 | 2.46342 | 2.55275 | 2.64456 | 2.73854 | 2.83477 | 2.93324 | 3.03382 | 3.13645 | 3.24135 | 3.24135 |
| airpol.cost.coa.res | AP 4351 ($/GJ; switch in the prototype) | 45.7535 | 37.1775 | 35.0004 | 32.1301 | 36.6762 | 37.7209 | 40.9509 | 43.9937 | 46.8173 | 47.8293 | 49.8501 | 51.9224 | 54.0666 | 56.2776 | 58.5581 | 60.9089 | 63.3285 | 65.8167 | 68.3698 | 68.3698 |
| airpol.cost.coa.pow | AP 3731 ($/GJ) | 0.748238 | 0.605947 | 0.568541 | 0.520151 | 0.591734 | 0.606517 | 0.656203 | 0.702545 | 0.745064 | 0.758543 | 0.787854 | 0.817753 | 0.848554 | 0.880164 | 0.912614 | 0.945906 | 0.980003 | 1.01489 | 1.05051 | 1.05051 |
| airpol.cost.nga.ind | AP 3998 ($/GJ) | 0.293984 | 0.238879 | 0.224891 | 0.206448 | 0.235658 | 0.24237 | 0.263124 | 0.282675 | 0.300817 | 0.307319 | 0.320303 | 0.333618 | 0.347395 | 0.361601 | 0.376253 | 0.391358 | 0.406904 | 0.422891 | 0.436798 | 0.436798 |
| airpol.cost.nga.pow | AP 3732 ($/GJ) | 0.559905 | 0.454017 | 0.426546 | 0.390754 | 0.445115 | 0.45684 | 0.494924 | 0.530586 | 0.563457 | 0.574428 | 0.597438 | 0.620961 | 0.645238 | 0.670202 | 0.69588 | 0.722277 | 0.749368 | 0.777148 | 0.799931 | 0.799931 |
| airpol.cost.gso.all | AP 3886 ($/l) | 0.060784 | 0.0488894 | 0.0455492 | 0.0413756 | 0.0467298 | 0.0475465 | 0.0510594 | 0.0542534 | 0.057097 | 0.057679 | 0.0594362 | 0.061199 | 0.062989 | 0.0647974 | 0.0666247 | 0.0684687 | 0.0703251 | 0.0721907 | 0.0747137 | 0.0747137 |
| airpol.cost.die.all | AP 3887 ($/l) | 0.217734 | 0.176876 | 0.166476 | 0.152784 | 0.174356 | 0.179276 | 0.194577 | 0.20898 | 0.222335 | 0.227082 | 0.236615 | 0.246387 | 0.256496 | 0.266915 | 0.277659 | 0.288731 | 0.300123 | 0.311834 | 0.325903 | 0.325903 |
| airpol.cost.lpg.all | AP 4314 ($/l; all years, L190 fixed) | 0.674992 | 0.548272 | 0.515978 | 0.473491 | 0.540289 | 0.555476 | 0.60282 | 0.647376 | 0.688673 | 0.703303 | 0.73275 | 0.762932 | 0.794148 | 0.826321 | 0.859491 | 0.893668 | 0.928829 | 0.964969 | 1.00203 | 1.00203 |
| airpol.cost.ker.all | AP 4313 ($/l) | 0.936977 | 0.759087 | 0.712505 | 0.652118 | 0.742155 | 0.760999 | 0.823669 | 0.882192 | 0.935962 | 0.953283 | 0.990526 | 1.02854 | 1.06773 | 1.10796 | 1.1493 | 1.19173 | 1.23521 | 1.27974 | 1.32522 | 1.32522 |
| airpol.cost.oop.pow | AP 3733 ($/GJ) | 5.85636 | 4.7286 | 4.4234 | 4.03467 | 4.5759 | 4.67575 | 5.04302 | 5.38217 | 5.68976 | 5.77409 | 5.97775 | 6.18428 | 6.39596 | 6.61202 | 6.83262 | 7.05768 | 7.28685 | 7.51995 | 7.75756 | 7.75756 |
| airpol.cost.oop.ind | AP 3961 ($/GJ) | 23.4271 | 18.9284 | 17.7188 | 16.1728 | 18.3551 | 18.7689 | 20.2576 | 21.6356 | 22.8889 | 23.2454 | 24.0834 | 24.9344 | 25.8078 | 26.7005 | 27.6131 | 28.5455 | 29.4964 | 30.465 | 31.4539 | 31.4539 |
| airpol.cost.nga.res | AP 4378 x 741 x time_factor x (1+1713) / 41868 ($/GJ; L189 fixed) | 0.0371033 | 0.0301487 | 0.0283832 | 0.0260555 | 0.0297422 | 0.0305894 | 0.0332087 | 0.0356762 | 0.0379659 | 0.0387866 | 0.0404254 | 0.0421059 | 0.0438447 | 0.0456377 | 0.047487 | 0.0493934 | 0.0513556 | 0.0533734 | 0.0554437 | 0.0554437 |

Legacy Mitigation rows 17738-17749 as cached (with bugs B2-B4), for comparison:

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17738 | Coal ind | 2.37614 | 1.92141 | 1.80008 | 1.64437 | 1.8678 | 1.91151 | 2.06488 | 2.20724 | 2.33711 | 2.37559 | 2.46342 | 2.55275 | 2.64456 | 2.73854 | 2.83477 | 2.93324 | 2.93324 | 2.93324 | 2.93324 | 2.93324 |
| 17739 | Coal res | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 17740 | Coal pow | 0.748238 | 0.605947 | 0.568541 | 0.520151 | 0.591734 | 0.606517 | 0.656203 | 0.702545 | 0.745064 | 0.758543 | 0.787854 | 0.817753 | 0.848554 | 0.880164 | 0.912614 | 0.945906 | 0.945906 | 0.945906 | 0.945906 | 0.945906 |
| 17741 | Natural gas ind | 0.293984 | 0.238879 | 0.224891 | 0.206448 | 0.235658 | 0.24237 | 0.263124 | 0.282675 | 0.300817 | 0.307319 | 0.320303 | 0.333618 | 0.347395 | 0.361601 | 0.376253 | 0.391358 | 0.391358 | 0.391358 | 0.391358 | 0.391358 |
| 17742 | Natural gas res | 0.00147795 | 0.00150796 | 0.00153134 | 0.00153261 | 0.001558 | 0.00156077 | 0.00157338 | 0.00158621 | 0.00159955 | 0.00161971 | 0.00164002 | 0.00165983 | 0.00167982 | 0.00169978 | 0.00171978 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 |
| 17743 | Natural gas pow | 0.559905 | 0.454017 | 0.426546 | 0.390754 | 0.445115 | 0.45684 | 0.494924 | 0.530586 | 0.563457 | 0.574428 | 0.597438 | 0.620961 | 0.645238 | 0.670202 | 0.69588 | 0.722277 | 0.722277 | 0.722277 | 0.722277 | 0.722277 |
| 17744 | Gasoline  | 0.060784 | 0.0488894 | 0.0455492 | 0.0413756 | 0.0467298 | 0.0475465 | 0.0510594 | 0.0542534 | 0.057097 | 0.057679 | 0.0594362 | 0.061199 | 0.062989 | 0.0647974 | 0.0666247 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 |
| 17745 | Diesel  | 0.217734 | 0.176876 | 0.166476 | 0.152784 | 0.174356 | 0.179276 | 0.194577 | 0.20898 | 0.222335 | 0.227082 | 0.236615 | 0.246387 | 0.256496 | 0.266915 | 0.277659 | 0.288731 | 0.288731 | 0.288731 | 0.288731 | 0.288731 |
| 17746 | LPG  | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 |
| 17747 | Kerosene  | 0.936977 | 0.759087 | 0.712505 | 0.652118 | 0.742155 | 0.760999 | 0.823669 | 0.882192 | 0.935962 | 0.953283 | 0.990526 | 1.02854 | 1.06773 | 1.10796 | 1.1493 | 1.19173 | 1.19173 | 1.19173 | 1.19173 | 1.19173 |
| 17748 | Other oil products pow | 5.85636 | 4.7286 | 4.4234 | 4.03467 | 4.5759 | 4.67575 | 5.04302 | 5.38217 | 5.68976 | 5.77409 | 5.97775 | 6.18428 | 6.39596 | 6.61202 | 6.83262 | 7.05768 | 7.05768 | 7.05768 | 7.05768 | 7.05768 |
| 17749 | Other oil products ind | 23.4271 | 18.9284 | 17.7188 | 16.1728 | 18.3551 | 18.7689 | 20.2576 | 21.6356 | 22.8889 | 23.2454 | 24.0834 | 24.9344 | 25.8078 | 26.7005 | 27.6131 | 28.5455 | 28.5455 | 28.5455 | 28.5455 | 28.5455 |
| 17750 | Coal - other other | 0.747496 | 0.605304 | 0.567961 | 0.519632 | 0.591143 | 0.605916 | 0.655559 | 0.701863 | 0.744346 | 0.757818 | 0.787107 | 0.816984 | 0.847762 | 0.879348 | 0.911774 | 0.945041 | 0.945041 | 0.945041 | 0.945041 | 0.945041 |
| 17751 | Natural gas - other other | 0.350146 | 0.279196 | 0.257287 | 0.235242 | 0.269447 | 0.278533 | 0.304331 | 0.328868 | 0.352306 | 0.361825 | 0.379236 | 0.395818 | 0.413429 | 0.431409 | 0.450013 | 0.46919 | 0.46919 | 0.46919 | 0.46919 | 0.46919 |
| 17752 | Other oil products and diesel - other other | 8.51612 | 6.82618 | 6.54943 | 6.40843 | 6.93924 | 7.30771 | 7.8316 | 8.30344 | 8.71725 | 8.95584 | 9.38619 | 9.82988 | 10.2884 | 10.7641 | 11.2561 | 11.765 | 11.765 | 11.765 | 11.765 | 11.765 |
| 17753 | Other oil products - average avg | 12.1706 | 9.72423 | 9.77033 | 9.27196 | 9.62708 | 9.89204 | 10.3229 | 10.6834 | 10.969 | 11.3591 | 12.0007 | 12.6683 | 13.3586 | 14.0817 | 14.8337 | 15.6158 | 15.9012 | 16.187 | 16.4739 | 16.7616 |

#### T2. Effective PM2.5 concentration coefficients `air.conc.coef` κ[m,p] (µg/m3 per t; AP F442:F522 x I974:I980, Manual-FASST as cached)

| Sector m | factor I | so2 | nox | pm2 | bc | pom | opm | voc |
|---|---|---|---|---|---|---|---|---|
| cpp | 1 | 2.051e-06 | 2e-07 | 0 | 5.5052e-05 | 5.4276e-05 | 5.5052e-05 | 0 |
| gpp | 57.804 | 0.000118556 | 1.15608e-05 | 0 | 0.00318223 | 0.00313737 | 0.00318223 | 0 |
| opp | 7.00187 | 1.43608e-05 | 1.40037e-06 | 0 | 0.000385467 | 0.000380033 | 0.000385467 | 0 |
| rod | 2.30598 | 4.72957e-06 | 4.61196e-07 | 0 | 0.000126949 | 0.000125159 | 0.000126949 | 0 |
| gro | 4.56734 | 9.36762e-06 | 9.13468e-07 | 0 | 0.000251441 | 0.000247897 | 0.000251441 | 0 |
| oth | 25.6111 | 5.25284e-05 | 5.12222e-06 | 0 | 0.00140994 | 0.00139007 | 0.00140994 | 0 |
| foo | 332.73 | 0.000682429 | 6.6546e-05 | 0 | 0.0183175 | 0.0180593 | 0.0183175 | 0 |

#### T3. Value of averted modelled ambient PM2.5 `air.vpm` (USD bn per µg/m3) = AP 3217 / (AP 981 - AP 1814); 2022 = 0; 2041 = 2040

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| air.vpm | typed | 0 | 0.290688 | 0.276304 | 0.196348 | 0.223911 | 0.23237 | 0.253805 | 0.274121 | 0.293071 | 0.299288 | 0.311904 | 0.324926 | 0.338351 | 0.352188 | 0.366428 | 0.381091 | 0.396147 | 0.411588 | 0.427404 | 0.427404 |
| (AP 981) | modelled PM2.5, scen 1 | 30.1723 | 28.5791 | 33.0267 | 36.5062 | 36.2478 | 38.5792 | 39.8333 | 41.0833 | 42.2873 | 42.655 | 43.0203 | 43.4602 | 43.8985 | 44.3493 | 44.8072 | 45.273 | 45.7457 | 46.225 | 46.7105 | 46.7105 |
| (AP 1814) | modelled PM2.5, scen 2 | 30.1723 | 28.5789 | 33.0265 | 36.5061 | 36.2477 | 38.5375 | 39.7429 | 40.9421 | 42.0933 | 42.4071 | 42.7183 | 43.1017 | 43.4825 | 43.8757 | 44.2765 | 44.6862 | 45.1045 | 45.5311 | 45.9659 | 45.9659 |
| (AP 3217) | wel.air legacy AP | 0 | 4.65067e-05 | 4.2525e-05 | 2.90915e-05 | 3.29443e-05 | 0.00970037 | 0.0229379 | 0.0387092 | 0.0568571 | 0.0741913 | 0.0942123 | 0.116503 | 0.140749 | 0.166789 | 0.194464 | 0.2236 | 0.254001 | 0.285577 | 0.318264 | 0.318264 |

#### T4. Transport external cost per vehicle-km, typed

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tran.acc.km | Transport 185 (USD/km) | 0.00632954 | 0.0049802 | 0.00460373 | 0.00419517 | 0.00473596 | 0.00485939 | 0.00524274 | 0.00559414 | 0.00590918 | 0.005954 | 0.0061273 | 0.00630436 | 0.00648515 | 0.00666962 | 0.00685774 | 0.00704945 | 0.00724651 | 0.00744909 | 0.00765733 | 0.00787139 |
| tran.con.km | Transport 220 (USD/km) | 0.00536868 | 0.00548468 | 0.00546949 | 0.00583626 | 0.00621345 | 0.00666956 | 0.00722952 | 0.00780289 | 0.00837663 | 0.00898573 | 0.00963183 | 0.0103166 | 0.0110416 | 0.0118087 | 0.0126195 | 0.0134757 | 0.0143841 | 0.0153472 | 0.0163671 | 0.0174454 |
| tran.rdm.km | Transport 232 (USD/freight km) | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

#### R. Legacy cached values for regression (scenario 2 = policy of the cached run)

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vkt.1 (T168) | Transport | 215.761 | 214.476 | 208.154 | 199.105 | 205.133 | 226.134 | 249.018 | 274.304 | 305.35 | 343.448 | 387 | 437.052 | 494.516 | 560.766 | 636.752 | 724.789 | 827.237 | 947.011 | 1086.79 | 1242.09 |
| vktf.1 (T169) | Transport | 11.7285 | 11.7281 | 11.3698 | 10.8613 | 11.9501 | 13.175 | 14.529 | 16.0265 | 17.8425 | 20.0473 | 22.5478 | 25.4043 | 28.5903 | 32.1684 | 36.188 | 40.7124 | 45.8085 | 51.5652 | 58.0877 | 65.4194 |
| vkt.2 (T248) | Transport | 215.761 | 214.476 | 208.154 | 199.105 | 205.133 | 225.856 | 248.417 | 273.334 | 303.944 | 341.522 | 384.466 | 433.809 | 490.449 | 555.747 | 630.638 | 717.411 | 818.397 | 936.465 | 1074.24 | 1227.22 |
| vktf.2 (T135) | Transport | 11.7285 | 11.7281 | 11.3698 | 10.8613 | 11.9501 | 13.1601 | 14.4967 | 15.9742 | 17.7663 | 19.9425 | 22.4098 | 25.2279 | 28.3692 | 31.8952 | 35.855 | 40.311 | 45.3292 | 50.9973 | 57.4194 | 64.6376 |
| tr.acc.gso.1 | Transport 322 | 0.0423861 | 0.0343589 | 0.0314842 | 0.0284638 | 0.0322049 | 0.0331571 | 0.0358265 | 0.0382694 | 0.0404957 | 0.0409011 | 0.0422092 | 0.0435663 | 0.0449834 | 0.0464629 | 0.0480066 | 0.0496133 | 0.0512967 | 0.0530592 | 0.0549027 | 0.0568334 |
| tr.acc.gso.2 | Transport 323 | 0.0423861 | 0.0343589 | 0.0314842 | 0.0284638 | 0.0322049 | 0.033157 | 0.0358291 | 0.0382781 | 0.0405138 | 0.0409309 | 0.0422544 | 0.04363 | 0.045069 | 0.0465738 | 0.0481465 | 0.0497858 | 0.0515057 | 0.0533086 | 0.0551969 | 0.0571767 |
| tr.acc.die.1 | Transport 324 | 0.013174 | 0.00968533 | 0.00870486 | 0.00792335 | 0.00867499 | 0.00894511 | 0.0097038 | 0.0104114 | 0.0110568 | 0.0111981 | 0.0115804 | 0.0119725 | 0.012382 | 0.0128028 | 0.0132336 | 0.0136781 | 0.014139 | 0.0146144 | 0.0151031 | 0.0155943 |
| tr.acc.die.2 | Transport 325 | 0.013174 | 0.00968533 | 0.00870486 | 0.00792335 | 0.00867499 | 0.00895126 | 0.00971831 | 0.0104365 | 0.0110947 | 0.0112488 | 0.0116465 | 0.0120561 | 0.0124854 | 0.0129285 | 0.013384 | 0.0138556 | 0.0143461 | 0.0148538 | 0.0153771 | 0.0159055 |
| tr.con.gso.1 | Transport 333 | 0.0359517 | 0.0378394 | 0.037405 | 0.0395984 | 0.0422519 | 0.0455084 | 0.0494033 | 0.0533794 | 0.0574052 | 0.0617276 | 0.0663509 | 0.0712926 | 0.0765889 | 0.0822635 | 0.0883408 | 0.0948407 | 0.101822 | 0.109317 | 0.117351 | 0.12596 |
| tr.con.gso.2 | Transport 334 | 0.0359517 | 0.0378394 | 0.037405 | 0.0395984 | 0.0422519 | 0.0455083 | 0.049407 | 0.0533915 | 0.0574308 | 0.0617726 | 0.0664219 | 0.0713969 | 0.0767347 | 0.08246 | 0.0885983 | 0.0951705 | 0.102237 | 0.109831 | 0.11798 | 0.126721 |
| tr.con.die.1 | Transport 335 | 0.0111741 | 0.0106664 | 0.0103419 | 0.0110228 | 0.0113813 | 0.0122772 | 0.0133812 | 0.0145222 | 0.0156738 | 0.0169001 | 0.0182038 | 0.0195919 | 0.0210816 | 0.0226677 | 0.0243522 | 0.026147 | 0.0280653 | 0.0301097 | 0.0322818 | 0.0345617 |
| tr.con.die.2 | Transport 336 | 0.0111741 | 0.0106664 | 0.0103419 | 0.0110228 | 0.0113813 | 0.0122857 | 0.0134012 | 0.0145572 | 0.0157274 | 0.0169765 | 0.0183077 | 0.0197287 | 0.0212577 | 0.0228903 | 0.0246289 | 0.0264864 | 0.0284765 | 0.0306029 | 0.0328677 | 0.0352513 |
| tr.rdm.die.1 | Transport 344 | 0.148468 | 0.140497 | 0.135773 | 0.134828 | 0.134486 | 0.135095 | 0.135797 | 0.136534 | 0.137298 | 0.138101 | 0.13894 | 0.139816 | 0.140735 | 0.141686 | 0.142667 | 0.143679 | 0.14472 | 0.145785 | 0.146872 | 0.147965 |
| tr.rdm.die.2 | Transport 345 | 0.148468 | 0.140497 | 0.135773 | 0.134828 | 0.134486 | 0.135207 | 0.13604 | 0.136923 | 0.137848 | 0.138827 | 0.139856 | 0.140934 | 0.142069 | 0.14325 | 0.144472 | 0.145738 | 0.147045 | 0.148387 | 0.149761 | 0.151151 |
| tr.acc.nga.1 | Transport 328 | 0.00044399 | 0.000404711 | 0.000427699 | 0.000363455 | 0.000410962 | 0.000428061 | 0.000470294 | 0.000509764 | 0.000550987 | 0.000563235 | 0.000589415 | 0.000603155 | 0.000621394 | 0.000638269 | 0.000655916 | 0.000673855 | 0.000692366 | 0.000711403 | 0.000730784 | 0.000750495 |
| tr.con.nga.1 | Transport 339 | 0.00037659 | 0.000445706 | 0.00050813 | 0.000505632 | 0.000539171 | 0.000587518 | 0.000648516 | 0.000711035 | 0.000781058 | 0.000850031 | 0.000926534 | 0.000987013 | 0.00105799 | 0.00113007 | 0.001207 | 0.00128814 | 0.00137432 | 0.00146569 | 0.00156201 | 0.00166332 |
| tr.acc.ecy.1 | Transport 330 | 1.0903e-06 | 1.79107e-06 | 2.1613e-06 | 2.32467e-06 | 3.97749e-06 | 6.74205e-06 | 1.22396e-05 | 2.2243e-05 | 4.159e-05 | 7.33803e-05 | 0.000127568 | 0.000209219 | 0.000328454 | 0.000495612 | 0.00071808 | 0.00100824 | 0.00138227 | 0.0018595 | 0.00245562 | 0.00313834 |
| tr.con.ecy.1 | Transport 341 | 9.24782e-07 | 1.9725e-06 | 2.56774e-06 | 3.23404e-06 | 5.21836e-06 | 9.25352e-06 | 1.68779e-05 | 3.10253e-05 | 5.89564e-05 | 0.000110745 | 0.000200531 | 0.00034237 | 0.000559228 | 0.000877491 | 0.0013214 | 0.00192735 | 0.00274376 | 0.00383109 | 0.00524874 | 0.00695551 |
| tr.rdm.ecy.1 | Transport 350 | 7.47238e-06 | 8.18192e-06 | 7.72461e-06 | 6.81302e-06 | 7.58318e-06 | 1.01835e-05 | 1.67135e-05 | 3.16625e-05 | 6.72231e-05 | 0.000146015 | 0.000310651 | 0.00062544 | 0.00108378 | 0.00170612 | 0.00251848 | 0.0035422 | 0.00480177 | 0.0063259 | 0.0081423 | 0.0101874 |
| M17714 | Avoided climate damages (global)  | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17715 | Total global welfare benefits  | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17716 | Averted climate damages (national) egy.mit.wel.cli.usd | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17717 | Averted air pollution mortality/morbidit egy.mit.wel.air.usd | 0 | 4.65067e-05 | 4.2525e-05 | 2.90915e-05 | 3.29443e-05 | 0.00970037 | 0.0229379 | 0.0387092 | 0.0568571 | 0.0741913 | 0.0942123 | 0.116503 | 0.140749 | 0.166789 | 0.194464 | 0.2236 | 0.254001 | 0.285577 | 0.285577 | 0.285577 |
| M17718 | Averted road accidents egy.mit.wel.rod.aci.usd | 0 | 0 | 0 | 0 | 1.51897e-09 | 0.00135188 | 0.00314791 | 0.00542962 | 0.00830923 | 0.0114704 | 0.0155271 | 0.020444 | 0.0263758 | 0.033477 | 0.0419311 | 0.0520088 | 0.0640633 | 0.0785583 | 0.0961178 | 0.117066 |
| M17719 | Reduced congestion egy.mit.wel.rod.con.usd | 0 | 0 | 0 | 0 | 1.99284e-09 | 0.00185546 | 0.00434084 | 0.00757341 | 0.0117789 | 0.0173111 | 0.0244079 | 0.0334549 | 0.0449075 | 0.0592718 | 0.0771609 | 0.09942 | 0.127163 | 0.161852 | 0.205446 | 0.259453 |
| M17720 | Reduced road damage egy.mit.wel.rod.dmg.usd | 0 | 0 | 0 | 0 | 1.98327e-10 | 0.00178905 | 0.00387103 | 0.00628408 | 0.0091453 | 0.0125725 | 0.016561 | 0.0211591 | 0.0265396 | 0.0327786 | 0.0399554 | 0.0481704 | 0.0575246 | 0.0681429 | 0.0801981 | 0.0938132 |
| M17721 | Efficiency costs egy.mit.wel.eco.dwl.usd | 0 | 0.000702906 | 0.000622611 | 0.000605192 | 0.00064773 | 0.0578384 | 0.164548 | 0.273614 | 0.386069 | 0.488786 | 0.589355 | 0.703693 | 0.820088 | 0.937329 | 1.0547 | 1.17048 | 1.2835 | 1.39323 | 1.4995 | 1.60134 |
| M17722 | Total national welfare benefits egy.mit.wel.tot.tot | -1.09609e-07 | 0.00107789 | 0.000993892 | 0.000963466 | 0.00102206 | 0.118189 | 0.311323 | 0.519672 | 0.745251 | 0.964925 | 1.19601 | 1.46073 | 1.74375 | 2.04462 | 2.36342 | 2.69902 | 3.05146 | 3.42233 | 3.78186 | 4.16199 |
| M17723 | Climate benefits egy.mit.wel.cli.pct | -2.00394e-10 | 5.7877e-07 | 5.65696e-07 | 5.42598e-07 | 5.39823e-07 | 6.88661e-05 | 0.000160766 | 0.000255448 | 0.000353815 | 0.000445832 | 0.000538233 | 0.000637676 | 0.00073838 | 0.000839927 | 0.000941856 | 0.00104326 | 0.00114363 | 0.00124284 | 0.00134099 | 0.00143733 |
| M17724 | Air pollution co-benefits egy.mit.wel.air.pct | 0 | 8.19446e-08 | 7.31736e-08 | 4.7952e-08 | 5.20941e-08 | 1.46323e-05 | 3.27855e-05 | 5.25795e-05 | 7.36634e-05 | 9.17287e-05 | 0.000111216 | 0.000131378 | 0.000151697 | 0.000171896 | 0.000191746 | 0.000211041 | 0.000229594 | 0.000247343 | 0.000237122 | 0.000227439 |
| M17725 | Transport co-benefits egy.mit.wel.rod.pct | 0 | 0 | 0 | 0 | 5.86675e-12 | 7.53671e-06 | 1.62367e-05 | 2.61981e-05 | 3.78745e-05 | 5.11294e-05 | 6.66923e-05 | 8.46411e-05 | 0.000105432 | 0.000129371 | 0.000156824 | 0.000188388 | 0.000224849 | 0.000267243 | 0.000316986 | 0.000374582 |
| M17726 | Efficiency costs egy.mit.wel.eco.dwl.pct | 0 | 1.23852e-06 | 1.07134e-06 | 9.97549e-07 | 1.02424e-06 | 8.72453e-05 | 0.00023519 | 0.000371655 | 0.000500186 | 0.000604326 | 0.000695722 | 0.000793538 | 0.000883876 | 0.000966029 | 0.00103995 | 0.00110474 | 0.00116017 | 0.0012067 | 0.00124507 | 0.00127534 |
| M17727 | Total national welfare benefits egy.mit.wel.tot.pct | -2.00394e-10 | 1.89923e-06 | 1.71021e-06 | 1.5881e-06 | 1.61616e-06 | 0.00017828 | 0.000444978 | 0.00070588 | 0.000965539 | 0.00119302 | 0.00141186 | 0.00164723 | 0.00187939 | 0.00210722 | 0.00233038 | 0.00254743 | 0.00275824 | 0.00296413 | 0.00314017 | 0.00331468 |
| M17763 | Total externalities - gasoline  | 0.139122 | 0.121088 | 0.114438 | 0.109438 | 0.121187 | 0.126212 | 0.136289 | 0.145902 | 0.154998 | 0.160308 | 0.167996 | 0.176058 | 0.184561 | 0.193524 | 0.202972 | 0.212923 | 0.221588 | 0.230845 | 0.240723 | 0.251262 |
| M17764 | Total externalities - diesel  | 0.39055 | 0.337726 | 0.321295 | 0.306558 | 0.328899 | 0.335593 | 0.353458 | 0.370448 | 0.386363 | 0.393281 | 0.40534 | 0.417768 | 0.430694 | 0.444072 | 0.457912 | 0.472235 | 0.475655 | 0.47924 | 0.482987 | 0.486852 |
| M17783 | Environmental benefits - Harberger trian egy.mit.env.ffs.cost.all.all.2 | -1.91944e-15 | 0.000398538 | 0.000396587 | 0.000394472 | 0.000411228 | 0.132697 | 0.298078 | 0.482806 | 0.686657 | 0.898863 | 1.12956 | 1.38398 | 1.6588 | 1.95308 | 2.26647 | 2.59807 | 2.92329 | 3.26135 | 3.61256 | 3.97617 |
| M17784 | Total national welfare benefits (FFS) egy.mit.wel.ffs.all.all.2 | -1.91944e-15 | 0.00110144 | 0.0010192 | 0.000999664 | 0.00105896 | 0.190535 | 0.462626 | 0.75642 | 1.07273 | 1.38765 | 1.71891 | 2.08767 | 2.47888 | 2.89041 | 3.32117 | 3.76855 | 4.2068 | 4.65458 | 5.11206 | 5.57752 |
| M17678 | Coal 0.09620266666666666 | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| M17679 | Natural gas 0.055799999999999995 | 3.05794 | 3.18026 | 3.30747 | 3.43976 | 3.57736 | 3.72045 | 3.86927 | 4.02404 | 4.185 | 4.3524 | 4.5265 | 4.70756 | 4.89586 | 5.09169 | 5.29536 | 5.50717 | 5.72746 | 5.95656 | 6.19482 | 6.44262 |
| M17680 | Non-road oil 0.41246307181497194 | 22.6037 | 23.5079 | 24.4482 | 25.4261 | 26.4431 | 27.5009 | 28.6009 | 29.7449 | 30.9347 | 32.1721 | 33.459 | 34.7974 | 36.1893 | 37.6368 | 39.1423 | 40.708 | 42.3363 | 44.0298 | 45.791 | 47.6226 |
| M17681 | Gasoline 0.0023557889897100003 | 0.129101 | 0.134265 | 0.139636 | 0.145222 | 0.15103 | 0.157072 | 0.163354 | 0.169889 | 0.176684 | 0.183752 | 0.191102 | 0.198746 | 0.206695 | 0.214963 | 0.223562 | 0.232504 | 0.241804 | 0.251477 | 0.261536 | 0.271997 |
| M17682 | Diesel 0.0026891510273550005 | 0.14737 | 0.153265 | 0.159396 | 0.165771 | 0.172402 | 0.179298 | 0.18647 | 0.193929 | 0.201686 | 0.209754 | 0.218144 | 0.22687 | 0.235944 | 0.245382 | 0.255198 | 0.265405 | 0.276022 | 0.287063 | 0.298545 | 0.310487 |
| M17683 | LPG 0.0017684866341836556 | 0.0969162 | 0.100793 | 0.104825 | 0.109018 | 0.113378 | 0.117913 | 0.12263 | 0.127535 | 0.132636 | 0.137942 | 0.14346 | 0.149198 | 0.155166 | 0.161373 | 0.167827 | 0.174541 | 0.181522 | 0.188783 | 0.196334 | 0.204188 |
| M17684 | Kerosene 0.0025734887129072754 | 0.141032 | 0.146673 | 0.15254 | 0.158642 | 0.164987 | 0.171587 | 0.17845 | 0.185588 | 0.193012 | 0.200732 | 0.208761 | 0.217112 | 0.225796 | 0.234828 | 0.244221 | 0.25399 | 0.26415 | 0.274716 | 0.285704 | 0.297133 |
| M17685 | Memo: LPG & kerosene 0.0021709876735454656 | 0.118974 | 0.123733 | 0.128682 | 0.13383 | 0.139183 | 0.14475 | 0.15054 | 0.156562 | 0.162824 | 0.169337 | 0.176111 | 0.183155 | 0.190481 | 0.1981 | 0.206024 | 0.214265 | 0.222836 | 0.231749 | 0.241019 | 0.25066 |
| M17702 | Coal egy.mit.cc.code.coa.1 | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| M17703 | Natural gas egy.mit.cc.code.nga.1 | 3.05794 | 3.18026 | 3.30747 | 3.43976 | 3.57736 | 3.72045 | 3.86927 | 4.02404 | 4.185 | 4.3524 | 4.5265 | 4.70756 | 4.89586 | 5.09169 | 5.29536 | 5.50717 | 5.72746 | 5.95656 | 6.19482 | 6.44262 |
| M17704 | Non-road oil egy.mit.cc.code.oop.1 | 22.6037 | 23.5079 | 24.4482 | 25.4261 | 26.4431 | 27.5009 | 28.6009 | 29.7449 | 30.9347 | 32.1721 | 33.459 | 34.7974 | 36.1893 | 37.6368 | 39.1423 | 40.708 | 42.3363 | 44.0298 | 45.791 | 47.6226 |
| M17705 | Gasoline egy.mit.cc.code.gso.1 | 0.129101 | 0.134265 | 0.139636 | 0.145222 | 0.15103 | 0.157072 | 0.163354 | 0.169889 | 0.176684 | 0.183752 | 0.191102 | 0.198746 | 0.206695 | 0.214963 | 0.223562 | 0.232504 | 0.241804 | 0.251477 | 0.261536 | 0.271997 |
| M17706 | Diesel egy.mit.cc.code.die.1 | 0.14737 | 0.153265 | 0.159396 | 0.165771 | 0.172402 | 0.179298 | 0.18647 | 0.193929 | 0.201686 | 0.209754 | 0.218144 | 0.22687 | 0.235944 | 0.245382 | 0.255198 | 0.265405 | 0.276022 | 0.287063 | 0.298545 | 0.310487 |
| M17707 | LPG egy.mit.cc.code.lpg.1 | 0.0969162 | 0.100793 | 0.104825 | 0.109018 | 0.113378 | 0.117913 | 0.12263 | 0.127535 | 0.132636 | 0.137942 | 0.14346 | 0.149198 | 0.155166 | 0.161373 | 0.167827 | 0.174541 | 0.181522 | 0.188783 | 0.196334 | 0.204188 |
| M17708 | Kerosene egy.mit.cc.code.ker.1 | 0.141032 | 0.146673 | 0.15254 | 0.158642 | 0.164987 | 0.171587 | 0.17845 | 0.185588 | 0.193012 | 0.200732 | 0.208761 | 0.217112 | 0.225796 | 0.234828 | 0.244221 | 0.25399 | 0.26415 | 0.274716 | 0.285704 | 0.297133 |
| M17709 | Memo: LPG & kerosene  | 0.118974 | 0.123733 | 0.128682 | 0.13383 | 0.139183 | 0.14475 | 0.15054 | 0.156562 | 0.162824 | 0.169337 | 0.176111 | 0.183155 | 0.190481 | 0.1981 | 0.206024 | 0.214265 | 0.222836 | 0.231749 | 0.241019 | 0.25066 |
| M17948 | Total - explicit subsidy egy.mit.expsub.con.all.all.1 | 38.6524 | 33.8739 | 48.5984 | 47.3255 | 53.0274 | 50.2822 | 50.0807 | 50.896 | 51.704 | 51.993 | 52.9246 | 54.4568 | 55.9072 | 57.4377 | 58.9891 | 60.5749 | 62.1915 | 63.8405 | 65.5266 | 67.2508 |
| M17949 | Total - implicit subsidy egy.mit.impsub.con.all.all.1 | 39.5492 | 38.4482 | 45.7499 | 50.1768 | 53.9035 | 58.8638 | 64.1037 | 69.6553 | 75.3597 | 78.34 | 81.7894 | 85.6999 | 89.7593 | 94.0532 | 98.5646 | 103.311 | 107.456 | 111.807 | 116.376 | 121.173 |
| M17950 | Total - explicit subsidy egy.mit.expsubgdp.con.all.all.1 | 0.0753665 | 0.0619299 | 0.0856301 | 0.0814339 | 0.087406 | 0.0795101 | 0.0755433 | 0.0727463 | 0.0702306 | 0.0673616 | 0.0654351 | 0.0642851 | 0.0630452 | 0.0619053 | 0.0607953 | 0.0597282 | 0.0586984 | 0.0577061 | 0.0567536 | 0.05584 |
| M17951 | Total - implicit subsidy egy.mit.impsubgdp.con.all.all.1 | 0.0771152 | 0.070293 | 0.080611 | 0.0863402 | 0.08885 | 0.09308 | 0.0966959 | 0.0995593 | 0.102363 | 0.101496 | 0.101123 | 0.101167 | 0.101219 | 0.101369 | 0.101583 | 0.101867 | 0.101421 | 0.101064 | 0.100795 | 0.100613 |
| M17795 | Gasoline - efficient price egy.mit.effprice.gso.all.1 | 1.40346 | 1.22331 | 1.16007 | 1.03764 | 1.1432 | 1.06711 | 1.06135 | 1.06746 | 1.07481 | 1.07724 | 1.09438 | 1.11228 | 1.13104 | 1.15068 | 1.17126 | 1.19279 | 1.21327 | 1.23485 | 1.25758 | 1.28152 |
| M17799 | Gasoline - implicit subsidy egy.mit.impsub.con.gso.all.1 | 3.90868 | 3.7092 | 4.56061 | 4.50405 | 4.97859 | 5.13654 | 5.50083 | 5.88523 | 6.26814 | 6.60646 | 7.01872 | 7.45567 | 7.91959 | 8.41199 | 8.93463 | 9.48913 | 10.0435 | 10.6327 | 11.259 | 11.9247 |
| M17798 | Gasoline - explicit subsidy egy.mit.expsub.con.gso.all.1 | 3.21727 | 3.72421 | 4.92732 | 3.77738 | 4.77202 | 3.93822 | 3.79011 | 3.75951 | 3.73151 | 3.68607 | 3.78005 | 3.87479 | 3.97028 | 4.06647 | 4.16332 | 4.26082 | 4.35891 | 4.45757 | 4.55675 | 4.65643 |
| M17807 | Diesel - efficient price egy.mit.effprice.die.all.1 | 1.6216 | 1.35177 | 1.26461 | 1.14524 | 1.25147 | 1.18514 | 1.18829 | 1.20175 | 1.21583 | 1.22035 | 1.24089 | 1.26213 | 1.28423 | 1.30715 | 1.33091 | 1.35555 | 1.36964 | 1.38433 | 1.39963 | 1.41551 |
| M17811 | Diesel - implicit subsidy egy.mit.impsub.con.die.all.1 | 9.31645 | 9.01531 | 10.6004 | 10.614 | 11.4809 | 12.0401 | 12.9415 | 13.8407 | 14.7222 | 15.407 | 16.2512 | 17.1365 | 18.0675 | 19.0449 | 20.0704 | 21.1465 | 21.9437 | 22.7736 | 23.6376 | 24.5355 |
| M17810 | Diesel - explicit subsidy egy.mit.expsub.con.die.all.1 | 11.3289 | 10.4186 | 11.5364 | 9.30951 | 11.2244 | 9.62694 | 9.35209 | 9.30335 | 9.26045 | 9.18647 | 9.37344 | 9.56101 | 9.74914 | 9.93775 | 10.1268 | 10.3162 | 10.5059 | 10.6959 | 10.886 | 11.0763 |
| M17818 | LPG - efficient price egy.mit.effprice.lpg.all.1 | 1.44263 | 1.35333 | 1.32277 | 1.25617 | 1.30973 | 1.26325 | 1.25393 | 1.25175 | 1.25067 | 1.24925 | 1.25477 | 1.26051 | 1.26648 | 1.27268 | 1.27914 | 1.28585 | 1.29283 | 1.30009 | 1.30764 | 1.3155 |
| M17822 | LPG - implicit subsidy egy.mit.impsub.con.lpg.all.1 | 6.76132 | 7.64019 | 9.25849 | 9.53787 | 9.81617 | 10.1393 | 10.5174 | 10.8883 | 11.2459 | 11.6126 | 11.9898 | 12.3777 | 12.777 | 13.1878 | 13.6108 | 14.0463 | 14.4948 | 14.9568 | 15.4329 | 15.9236 |
| M17821 | LPG - explicit subsidy egy.mit.expsub.con.lpg.all.1 | 4.34153 | 4.68789 | 5.40129 | 4.67324 | 5.39564 | 4.88897 | 4.85619 | 4.90072 | 4.94356 | 4.9754 | 5.10236 | 5.23079 | 5.36069 | 5.49201 | 5.62473 | 5.75883 | 5.89427 | 6.03103 | 6.16907 | 6.30836 |
| M17829 | Kerosene - efficient price egy.mit.effprice.ker.all.1 | 1.96285 | 1.69205 | 1.6414 | 1.4831 | 1.65498 | 1.60898 | 1.66227 | 1.72142 | 1.77712 | 1.79393 | 1.84168 | 1.89057 | 1.94105 | 1.99301 | 2.04651 | 2.10155 | 2.11227 | 2.12341 | 2.135 | 2.14705 |
| M17833 | Kerosene - implicit subsidy egy.mit.impsub.con.ker.all.1 | 0.873751 | 0.783249 | 0.857381 | 0.823746 | 0.946203 | 0.998446 | 1.10844 | 1.21797 | 1.32421 | 1.39225 | 1.48753 | 1.58777 | 1.69366 | 1.80525 | 1.9228 | 2.04653 | 2.11463 | 2.18455 | 2.25634 | 2.33006 |
| M17832 | Kerosene - explicit subsidy egy.mit.expsub.con.ker.all.1 | 0.273674 | 0.346931 | 0.403888 | 0.326421 | 0.398659 | 0.343246 | 0.336391 | 0.337589 | 0.338691 | 0.338534 | 0.348362 | 0.358306 | 0.368359 | 0.37852 | 0.388784 | 0.399148 | 0.409608 | 0.42016 | 0.4308 | 0.441524 |
| M17840 | Other oil products - efficient price egy.mit.effprice.oop.all.1 | 53.8099 | 48.7663 | 49.187 | 47.1432 | 50.2691 | 49.7733 | 50.8039 | 52.0562 | 53.311 | 54.699 | 56.6274 | 58.6333 | 60.7155 | 62.8862 | 65.1437 | 67.4915 | 69.4052 | 71.3845 | 73.4326 | 75.5519 |
| M17844 | Other oil products - implicit subsidy egy.mit.impsub.con.oop.all.1 | 11.1933 | 10.272 | 11.205 | 14.4747 | 15.8555 | 19.2434 | 22.1569 | 25.3324 | 28.7793 | 29.7052 | 30.832 | 32.0139 | 33.2904 | 34.6178 | 36.0182 | 37.4909 | 38.69 | 39.9496 | 41.269 | 42.6511 |
| M17843 | Other oil products - explicit subsidy egy.mit.expsub.con.oop.all.1 | 4.38892 | 3.47327 | 3.66144 | 4.16917 | 4.91512 | 5.10992 | 5.36737 | 5.75022 | 6.15118 | 5.94817 | 5.91192 | 5.87911 | 5.85662 | 5.83455 | 5.81667 | 5.80213 | 5.79094 | 5.78293 | 5.77741 | 5.77437 |
| M17849 | Natural gas, industry - efficient price egy.mit.effprice.nga.ind.1 | 15.6125 | 13.6107 | 13.1019 | 13.2926 | 13.6418 | 13.5743 | 13.4883 | 13.5716 | 13.7249 | 13.8842 | 14.0713 | 14.2656 | 14.4677 | 14.6777 | 14.8961 | 15.123 | 15.3433 | 15.5724 | 15.8106 | 16.0584 |
| M17853 | Natural gas, industry - implicit subsidy egy.mit.impsub.con.nga.ind.1 | 1.55451 | 1.36055 | 1.54745 | 1.66045 | 1.80162 | 1.95316 | 2.13787 | 2.33057 | 2.52884 | 2.73442 | 2.95885 | 3.19964 | 3.45794 | 3.73483 | 4.0315 | 4.34918 | 4.67731 | 5.02792 | 5.40242 | 5.80225 |
| M17852 | Natural gas, industry - explicit subsidy egy.mit.expsub.con.nga.ind.1 | 3.21129 | 2.06184 | 1.96371 | 2.07628 | 2.24044 | 2.22999 | 2.20851 | 2.26087 | 2.3407 | 2.42794 | 2.52581 | 2.62605 | 2.72866 | 2.83364 | 2.94098 | 3.05068 | 3.16272 | 3.2771 | 3.39381 | 3.51282 |
| M17859 | Natural gas, residential - efficient pri egy.mit.effprice.nga.res.1 | 22.7498 | 20.7356 | 20.1737 | 20.4074 | 20.7613 | 20.6898 | 20.5834 | 20.6616 | 20.8172 | 20.9922 | 21.1907 | 21.3971 | 21.6118 | 21.8351 | 22.0673 | 22.3088 | 22.5599 | 22.8211 | 23.0927 | 23.3752 |
| M17863 | Natural gas, residential - implicit subs egy.mit.impsub.con.nga.res.1 | 0.470812 | 0.474449 | 0.655656 | 0.678735 | 0.704019 | 0.725364 | 0.748582 | 0.774768 | 0.802255 | 0.83099 | 0.861114 | 0.892444 | 0.925031 | 0.958924 | 0.994179 | 1.03085 | 1.06899 | 1.10867 | 1.14995 | 1.19288 |
| M17862 | Natural gas, residential - explicit subs egy.mit.expsub.con.nga.res.1 | 0.986375 | 0.97724 | 1.36608 | 1.38419 | 1.41318 | 1.40096 | 1.3868 | 1.38918 | 1.39714 | 1.40608 | 1.41649 | 1.42672 | 1.43678 | 1.44665 | 1.45634 | 1.46585 | 1.47518 | 1.48432 | 1.49328 | 1.50206 |
| M17868 | Natural gas, power - efficient price egy.mit.effprice.nga.pow.1 | 15.1054 | 13.0234 | 12.5008 | 12.6833 | 13.0795 | 12.9911 | 12.8917 | 12.9802 | 13.1451 | 13.3071 | 13.5042 | 13.7088 | 13.9214 | 14.1422 | 14.3715 | 14.6097 | 14.83 | 15.0591 | 15.2974 | 15.5452 |
| M17872 | Natural gas, power - implicit subsidy egy.mit.impsub.con.nga.pow.1 | 4.45989 | 4.19791 | 5.20653 | 5.87333 | 6.21787 | 6.43908 | 6.69361 | 6.96632 | 7.15548 | 7.40417 | 7.65093 | 8.17434 | 8.64247 | 9.17624 | 9.73257 | 10.3234 | 10.902 | 11.5146 | 12.168 | 12.8656 |
| M17871 | Natural gas, power - explicit subsidy egy.mit.expsub.con.nga.pow.1 | 10.7292 | 7.82627 | 8.52293 | 9.5041 | 9.89726 | 9.49446 | 9.00811 | 8.82721 | 8.65321 | 8.60515 | 8.54988 | 8.78406 | 8.93083 | 9.11904 | 9.30166 | 9.48902 | 9.67866 | 9.87181 | 10.0727 | 10.2818 |
| M17877 | Natural gas, other - efficient price egy.mit.effprice.nga.other.1 | 15.5838 | 13.5568 | 13.083 | 13.2344 | 13.6177 | 13.5395 | 13.4491 | 13.5408 | 13.7113 | 13.8773 | 14.0771 | 14.2714 | 14.4775 | 14.6902 | 14.9116 | 15.1418 | 15.3588 | 15.5847 | 15.8196 | 16.064 |
| M17881 | Natural gas, other - implicit subsidy egy.mit.impsub.con.nga.other.1 | 0.0756736 | 0.0794192 | 0.112844 | 0.117701 | 0.125227 | 0.132291 | 0.14088 | 0.149679 | 0.158603 | 0.167329 | 0.176833 | 0.186791 | 0.197268 | 0.208274 | 0.219838 | 0.231984 | 0.243893 | 0.256389 | 0.269499 | 0.283252 |
| M17886 | Coal, industry - efficient price egy.mit.effprice.coa.ind.1 | 18.7686 | 16.0151 | 15.0793 | 14.2925 | 15.2265 | 15.6237 | 15.983 | 16.3379 | 16.6872 | 16.9582 | 17.3462 | 17.7477 | 18.1641 | 18.5957 | 19.0431 | 19.5067 | 19.8865 | 20.2815 | 20.6923 | 21.1195 |
| M17890 | Coal, industry - implicit subsidy egy.mit.impsub.con.coa.ind.1 | 0.504315 | 0.464312 | 0.56342 | 0.620434 | 0.645241 | 0.67697 | 0.730578 | 0.78544 | 0.841067 | 0.891108 | 0.944255 | 1.00008 | 1.0588 | 1.12051 | 1.18535 | 1.25345 | 1.31448 | 1.37847 | 1.44555 | 1.51589 |
| M17896 | Coal, residential - efficient price egy.mit.effprice.coa.res.1 | 29.199 | 21.9015 | 21.2434 | 20.148 | 21.1652 | 21.6149 | 21.8275 | 22.0461 | 22.2708 | 22.5113 | 22.8535 | 23.2093 | 23.5794 | 23.9643 | 24.3646 | 24.7809 | 25.2139 | 25.6642 | 26.1325 | 26.6195 |
| M17900 | Coal, residential - implicit subsidy egy.mit.impsub.con.coa.res.1 | 0.000607511 | 0.000560478 | 0.000652095 | 0.000704119 | 0.000718173 | 0.000745733 | 0.000781215 | 0.000817926 | 0.000855733 | 0.00089528 | 0.000934277 | 0.000975001 | 0.00101753 | 0.00106193 | 0.0011083 | 0.00115671 | 0.00120726 | 0.00126003 | 0.00131513 | 0.00137264 |
| M17933 | Electricity, residential - efficient pri egy.mit.effprice.ecy.res.1 | 0.0676265 | 0.0582941 | 0.114847 | 0.113334 | 0.113053 | 0.113379 | 0.113204 | 0.113332 | 0.113444 | 0.113886 | 0.112639 | 0.111645 | 0.110653 | 0.109742 | 0.108886 | 0.108084 | 0.107329 | 0.106614 | 0.105933 | 0.10527 |
| M17937 | Electricity, residential - implicit subs egy.mit.impsub.con.ecy.res.1 | 0.428632 | 0.393429 | 1.12105 | 1.21372 | 1.26389 | 1.31495 | 1.3616 | 1.41594 | 1.46355 | 1.51646 | 1.54287 | 1.59566 | 1.64607 | 1.69869 | 1.75194 | 1.80621 | 1.86135 | 1.91732 | 1.97415 | 2.0316 |
| M17942 | Electricity, other - efficient price egy.mit.effprice.ecy.other.1 | 0.0652756 | 0.974528 | 0.887347 | 0.761395 | 0.848931 | 0.758162 | 0.73319 | 0.720603 | 0.709594 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 |
| M17946 | Electricity, other - implicit subsidy egy.mit.impsub.con.ecy.other.1 | 0.00131064 | 0.0576379 | 0.0604121 | 0.0574365 | 0.0675396 | 0.0634581 | 0.0647574 | 0.0671286 | 0.0692251 | 0.0712154 | 0.0742852 | 0.0783984 | 0.0825416 | 0.0868557 | 0.091289 | 0.0958556 | 0.100552 | 0.105381 | 0.110347 | 0.115452 |
| M17945 | Electricity, other - explicit subsidy egy.mit.expsub.con.ecy.other.1 | 0 | 0.213999 | 0.24574 | 0.204419 | 0.265335 | 0.22488 | 0.221546 | 0.225295 | 0.228264 | 0.230132 | 0.240052 | 0.253344 | 0.266733 | 0.280674 | 0.295 | 0.309757 | 0.324934 | 0.340539 | 0.356586 | 0.373082 |
| M17767 | Coal egy.mit.env.ffs.cost.coa.ind.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17768 | Coal egy.mit.env.ffs.cost.coa.res.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17769 | Coal egy.mit.env.ffs.cost.coa.pow.2 | 0 | 0 | 0 | 0 | 0 | 0.00161038 | 0.00346075 | 0.0055767 | 0.00797306 | 0.0106425 | 0.0134925 | 0.0166129 | 0.0200142 | 0.0237053 | 0.0276887 | 0.0319714 | 0.036446 | 0.0412173 | 0.0463012 | 0.0517133 |
| M17770 | Natural gas egy.mit.env.ffs.cost.nga.ind.2 | 0 | 0.000352379 | 0.000350738 | 0.000348738 | 0.000363835 | 0.000386344 | 0.0169197 | 0.0355313 | 0.056724 | 0.0709429 | 0.0851966 | 0.105365 | 0.126405 | 0.148383 | 0.171378 | 0.194736 | 0.217553 | 0.240037 | 0.262073 | 0.283542 |
| M17771 | Natural gas egy.mit.env.ffs.cost.nga.res.2 | 0 | 0 | 0 | 0 | 0 | 0.00258705 | 0.00544889 | 0.0086022 | 0.0120573 | 0.0158422 | 0.0199781 | 0.0244851 | 0.029385 | 0.0347004 | 0.0404529 | 0.0466673 | 0.0533701 | 0.0605921 | 0.0683662 | 0.0759277 |
| M17772 | Natural gas egy.mit.env.ffs.cost.nga.pow.2 | 0 | 0 | 0 | 0 | 0 | 0.0060286 | 0.0131521 | 0.0214851 | 0.031048 | 0.0418641 | 0.0542648 | 0.0682441 | 0.0838827 | 0.101245 | 0.120339 | 0.141199 | 0.163172 | 0.18686 | 0.212355 | 0.239745 |
| M17773 | Gasoline - road egy.mit.env.ffs.cost.gso.rd.2 | 0 | 0 | 0 | 0 | 0 | 0.00553241 | 0.0120234 | 0.0195528 | 0.0280988 | 0.0374073 | 0.0480582 | 0.0598939 | 0.0729452 | 0.0872198 | 0.102659 | 0.119235 | 0.136383 | 0.154573 | 0.173852 | 0.19426 |
| M17774 | Diesel - road egy.mit.env.ffs.cost.die.rd.2 | 0 | 0 | 0 | 0 | 0 | 0.0106631 | 0.0231629 | 0.0375675 | 0.0537804 | 0.0706863 | 0.0900538 | 0.111324 | 0.134548 | 0.159722 | 0.186769 | 0.215659 | 0.241817 | 0.268874 | 0.296863 | 0.325794 |
| M17775 | LPG egy.mit.env.ffs.cost.lpg.all.2 | 0 | 0 | 0 | 0 | 0 | 0.0439046 | 0.0905267 | 0.139897 | 0.191746 | 0.246424 | 0.303949 | 0.364238 | 0.427237 | 0.492874 | 0.560971 | 0.631439 | 0.704208 | 0.779312 | 0.856829 | 0.936825 |
| M17776 | Kerosene egy.mit.env.ffs.cost.ker.all.2 | 0 | 0 | 0 | 0 | 0 | 2.25861e-05 | 4.10669e-05 | 7.54114e-05 | 0.00012384 | 0.000193948 | 0.000281572 | 0.000358182 | 0.000397522 | 0.000365667 | 0.000205568 | -0.000132006 | -0.000679666 | -0.00145034 | -0.0024578 | -0.00371819 |
| M17777 | Other oil products and diesel  egy.mit.env.ffs.cost.oop.pow.2 | 0 | 4.61587e-05 | 4.58485e-05 | 4.57343e-05 | 4.73927e-05 | 4.87325e-05 | 5.08874e-05 | 5.34643e-05 | 5.652e-05 | 0.00434 | 0.00571721 | 0.00663922 | 0.00843054 | 0.0100239 | 0.0116184 | 0.0132224 | 0.0147143 | 0.0161452 | 0.0174586 | 0.0186723 |
| M17778 | Other oil products and diesel  egy.mit.env.ffs.cost.oop.ind.2 | -1.75279e-15 | 0 | 0 | 0 | 0 | 0.0542925 | 0.11697 | 0.188308 | 0.267943 | 0.3514 | 0.445922 | 0.549258 | 0.661624 | 0.783044 | 0.913207 | 1.05197 | 1.18328 | 1.31993 | 1.46208 | 1.60983 |
| M17779 | Coal - other egy.mit.env.ffs.cost.coa.other.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17780 | Natural gas - other egy.mit.env.ffs.cost.nga.other.2 | 0 | 0 | 0 | 0 | 0 | 0.000748702 | 0.00160081 | 0.00256269 | 0.00363746 | 0.00482373 | 0.00614826 | 0.00761168 | 0.00922557 | 0.0109986 | 0.0129402 | 0.0150607 | 0.0173162 | 0.0197624 | 0.0224128 | 0.0250169 |
| M17781 | Gasoline - other egy.mit.env.ffs.cost.gso.other.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17782 | Diesel and other oil products  egy.mit.env.ffs.cost.die.other.2 | -1.66641e-16 | 1.9853e-16 | -1.29101e-16 | -3.03055e-16 | 2.1848e-16 | 0.0068719 | 0.0147214 | 0.0235951 | 0.0334679 | 0.0442966 | 0.056494 | 0.0699471 | 0.0847022 | 0.1008 | 0.11824 | 0.137043 | 0.155717 | 0.175496 | 0.196429 | 0.218568 |
| M18090 | Air pollution costs egy.mit.airpol.cost.ecy.ind.2 | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |
| M18102 | Air pollution costs egy.mit.airpol.cost.ecy.res.2 | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |

## C. R3 Pigouvian taxes; R4 CBAM process emissions

## R3-R4 notes for the builder (Pigouvian taxes, efficient prices, CBAM process emissions)

Legacy 465, sheet Mitigation unless stated. Years by the year row: L = 2022 ... AE = 2041 (row 1 and 204 headers; K = 2021).
Tools used: lx.py / dec465.py; a formula grep over the whole sheet (scratchpad eq/r3r4/grepf.py) to find every consumer.

### 1. Legacy bugs (proposed; not replicated)

| # | Cells | Formula now | Formula intended | Egypt effect |
|---|---|---|---|---|
| L194 | L123:AE123 (feeds L158, ntx oop row 215, policy 9012) | `=IFERROR(L17748,0)` = 'Air pollution'!K3733, **US$ per GJ**, in a row labelled $/barrel and added to the climate damage in $/bbl (L142) | `=IFERROR(L17748,0)*_conv_barrel_to_gj` (6.12 GJ/bbl) | 0 by default (AddEfficientTaxes No*). With Yes: oop Pigouvian 2030 36.62 -> 65.77 $/bbl (AP 5.69 $/GJ -> 34.82 $/bbl) |
| L195 | L146:N146 (2022-2024) | `=IF(L204>=CPIntro,1,0)` (no phase-in) | O146's `=IF(L204>=CPIntro,MIN((L204-CPIntro+1)/$E$145,1),0)` | 0 (CPIntro 2026) |
| L196 | O146:AE146 | `MIN((t-CPIntro+1)/$E$145,1)`: #DIV/0! when AddEfficientTaxesPhaseInYears = 0, propagating into ntx (rows 205-215, 8782-9012) | full tax from CPIntro: divide by MAX($E$145,1) | 0 (5 years) |
| L197 | L1905 (and M1905:AE1909 empty); duplicate codes H5996:H6000 = H6007:H6011 | L1905 is **text** `'=@INDEX(L$2170:L$14547,$J1905)'` (range also 3 rows off); J1905 = MATCH of `egy.mit.cpe.ind.mch.1` finds 5996 (fuel CO2 rows) before 6007 (process rows) | `=INDEX(L$2173:L$14755,$J1905)` filled L1905:AE1909; unique codes (fuel rows e.g. `cfe.*`, process rows `cpe.*`) so 1905-1909 read 6007-6011; same for policy 1939-1943 (G codes only, no formulas) | 0 (CBAM off) |
| L198 | L1918:AE1918 | `=SUM(L1905:L1908)` (cement 1909 left out) | `=SUM(L1905:L1909)` | 0 |
| L199 | K5869:AE5871 (policy +6,316) | typed 0 in L:AE; K holds text '=L2727' (now Nuclear fuel cost), '=L2322', '=L2346' | carbon tax rate of the scenario ($/t, E1), auctioned ETS price (row 1876 / L2322), total shadow price (L2346) | 0: all CBAM prices, reductions and revenue are 0 |
| L200 | L5974:AE5981; M5981:AE5981 | `=L5952*(EXP(-($E5974)*(L5872))-1)`: price = row 5872 "Revenues Fund" (typed 0); M5981 `EXP(-(F5981)*...)`, N5981 `G5981` (relative drift) | price `($F5921*L5869+$G5921*L5870)` as rows 5985-5992; `$E5981` | 0 |
| L201 | L6014:AE6021 | `=L5963*(L5869*F5921+L5870*G5921)`: pre-policy process emissions x the **fuel** inclusion (sector coverage, ignores CBAMProc) | `=(L5963+L5985)*(L5869*F5932+L5870*G5932)` (post-policy, process inclusion) | 0 |
| L202 | M5996:AE6000; L6012:AE6012 | M:AE typed constants (equal to the process rows 6007-6011) while L sums fuel CO2 (5952..+5974..); 6012 empty | L formula filled right; `=SUM(L6007:L6011)` | 0 (not read) |
| L203 | L18096:AE18096, L18108:AE18108; L18152:L18157; INDEX ranges $L:$AD in 18128-18156 | #DIV/0! (CO2e of electricity taxes over a blank climate cost); the residential electricity column copies industry (`=K18152`), check row L18157 tests the gas rows; YearFuelPrices = 2041 gives #N/A | IFERROR(...,"n.a."); `=INDEX($L18101:$AE18101,...)` etc.; ranges to AE | display only |

Already known, cited (not re-reported): Air_pollution.md B2 (17742 <- AP K4382 deaths, not $), B3 (17746 `$K$4314` LPG fixed at 2022), B4 (AP links flat after 2037; visible in rows 113-123), B12 (17739 typed 9127), B13 (codes 17744, 17748-17749); register L113 (exact "Yes" tests; F200 tests `="Yes"`, consistent with its dropdown "Yes,No*"); I-f, I-h of Transport_cobenefits.md.

### 2. Issues to replicate (proposed)

- I113 Netting: with AddEfficientTaxes on, the whole new excise of the block (reform + manual excise + Pigouvian) becomes `MIN(R, MAX(0, R - SUM(existing fixed tax, fixed subsidy, floating part, existing carbon tax, existing ETS)))` (rows 8782-9012 O:AE): a top-up over existing taxes, never below 0 and never above R; subsidies do not raise it above R. The new carbon tax and new ETS are not netted, so with ClimateEffTax = Yes* and a carbon tax the climate damage is charged twice (row 81 calls the option "non-climate Pigouvian taxes").
- I114 Phase-in anchored on CPIntro (carbon tax start), linear over AddEfficientTaxesPhaseInYears; computed in every scenario, applied only in policy scenarios ($C>1); ntx rows typed 0 for 2022-2024.
- I115 Vintages: Pigouvian tax uses baseline externalities (transport mf.1, air pollution .1); efficient prices use transport mf.2 and air pollution .1.
- I116 Climate damage = national SCC (NSCC) x generic EF (IIASA average across 2-3 sectors, base-year column L, not the calibrated EF[f,s], not inventory-adjusted); CO2-equivalent rows multiply by the global SCC (17959) and divide by the national damage.
- I117 Other oil products: one Pigouvian for all oop using the oil **power-plant** air-pollution cost (row 123 "Power"); industrial oop cost (17749, 23.4 $/GJ in 2022) unused.
- I118 Road damage only for diesel (row 132 and 17967 empty: "No road damage externalities for gasoline").
- I119 Electricity Pigouvian = 0: rows 124-125 hold a formula only in K (2021) (`=IFERROR(L18102,0)`), L:AE blank, so L159:AE160 = 0. Filling them would tax power-plant air pollution twice (already in the coal/gas/oil-for-power Pigouvian, rows 148, 151, 158). Replicate 0; K124:K125 are dead cells. Owned here: this is the R1R2 group's bug candidate I119 (was proposed as bug Lnew-R1R2-18; an issue: see R3) ("electricity Pigouvian always 0"); checked: true (L159:AE160 = 0 in the cached run), but classified as an issue, not a bug, because the intended fill (L124 = L18102, L125 = L18090) double counts power-plant air pollution already in rows 148/151/158 and enters the price through the power model. Decision for the user: keep 0 (proposed), or fix and drop the AP term of coa.pow, nga.pow and the power share of oop. I119 (was proposed as bug Lnew-R1R2-18; an issue: see R3) should be retired in favour of this item.
- I120 Efficient prices: potential VAT only on consumer fuels (oil products, residential coal, gas, electricity); typed 0 for industry and power; general VAT rate of 2022 for all years (`$E$17956 = L726`, label "2018"); supply cost of scenario 1, retail price of the live scenario; computed for the live scenario only; no oop, no biomass.
- I121 Electricity air-pollution cost per kWh (18090) = generation-share-weighted fuel cost ($/GJ of fuel) x `_conv_ktoe_to_gwh/1000` = 0.01163 GJ/kWh, i.e. a fixed 31% thermal efficiency; baseline generation mix in every scenario.
- I122 Exact switch texts (F144 "Yes*", F200 "Yes", F17955 "No", I2203 "Yes*") match their dropdowns; the prototype uses LEFT(x,3)="Yes" (L113 rule). I2202:I2203 (code for VAT optimal taxation) are dead.
- I123 CBAM block: Egypt only (typed 2024 production and prices; `IF(_Country_code="EGY",...)`), master switch Dashboard G20 (Manual inputs row 22), switch of the live scenario read by both blocks (shared rows 1832-1836); abatement uses the auctioned ETS price; product fuel CO2 (E^f) is also in the energy model (memo rows only); no output read anywhere (decision D-R4).

### 3. Where it hooks into build.py

- Section 1 (policies): new rows next to `fpr.<c>` (`_pol(f'fpr.{pc}', ...)`, build.py ~604; formula in the section-1 builder ~9917): `pig.phi`, `pigx.<c>`, `ntxg.<c>` per PRICE_FUELS (bio and ecy: 0). Inputs via `MT_NAMES` (AddEfficientTaxes, ClimateEffTax, AddEfficientTaxesPhaseInYears, CPIntro).
- Price block (section 2, per price fuel, next to `pcsw`/`ppcw`): `xpre.<c>` and `ntxb.<c>` (no fuel-use weights: avoids the circularity a pxcd-based netting would create through ener).
- `calc_formula` var 'ntx' (build.py ~9233): read `ntxb` instead of `fpr/gj`, keep x exf. `rex`, `rnew`, `rvt`, `atp` follow unchanged.
- Power `ccp` (~9615): `fpr` of coa.pow / nga.pow / oop.all -> `ntxb x gj`.
- Efficient prices: a new memo section after welfare (reads `scc.nat`/`scc.glo` of R_WEL, the R1 section, `sp`, `rpn`, `txo`, `ener`, power `gen`). Generic EF ē_c from Inputs_ef (EF_SEL rows) averaged as R3.2.
- CBAM: a new section (data table for Pr_p, g_p, P_p typed from legacy F5898:G5905, G5910:G5917; EFs and σ from Manual inputs rows 30-37, 40-47, already placed by MI_BLOCKS (18, 47) - mark it read). MI_BLOCKS note to update.

Inputs: all six names exist in ScenarioDefinition (template rows 117-121, 212, 216-218, 282: CBAMProcMch/Irn/Nfm/Mac/Cem, AddEfficientTaxesPhaseInYears, ClimateEffTax, AddEfficientTaxes, ExternalityAddVAT, YearFuelPrices); none is read by build.py today. Missing: CBAM master switch (Dashboard G20 / Manual inputs H21:L21 -> row 22; the CBAMProc defaults already fold it in), CBAM production, growth and product prices (typed in legacy Mitigation, not on Manual inputs), the fossil manual excise (Manual inputs 150-160, AdditionalExcise; not built, R8).

### 4. Egypt cached values (legacy 465, scenario 2 = carbon tax; AddEfficientTaxes No*, ClimateEffTax Yes*, CPIntro 2026, CBAM off)

ntx rows 8782-9012 = 0 in all years (switch off, no reform). Pigouvian per unit (rows 148-158) are computed regardless of the switch:

| Row | Label | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 113 | Power | 0.748238 | 0.605947 | 0.568541 | 0.520151 | 0.591734 | 0.606517 | 0.656203 | 0.702545 | 0.745064 | 0.758543 | 0.787854 | 0.817753 | 0.848554 | 0.880164 | 0.912614 | 0.945906 | 0.945906 | 0.945906 | 0.945906 | 0.945906 |
| 115 | Industry | 2.37614 | 1.92141 | 1.80008 | 1.64437 | 1.8678 | 1.91151 | 2.06488 | 2.20724 | 2.33711 | 2.37559 | 2.46342 | 2.55275 | 2.64456 | 2.73854 | 2.83477 | 2.93324 | 2.93324 | 2.93324 | 2.93324 | 2.93324 |
| 116 | Power | 0.559905 | 0.454017 | 0.426546 | 0.390754 | 0.445115 | 0.45684 | 0.494924 | 0.530586 | 0.563457 | 0.574428 | 0.597438 | 0.620961 | 0.645238 | 0.670202 | 0.69588 | 0.722277 | 0.722277 | 0.722277 | 0.722277 | 0.722277 |
| 117 | Residential | 0.00147795 | 0.00150796 | 0.00153134 | 0.00153261 | 0.001558 | 0.00156077 | 0.00157338 | 0.00158621 | 0.00159955 | 0.00161971 | 0.00164002 | 0.00165983 | 0.00167982 | 0.00169978 | 0.00171978 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 |
| 118 | Industry | 0.293984 | 0.238879 | 0.224891 | 0.206448 | 0.235658 | 0.24237 | 0.263124 | 0.282675 | 0.300817 | 0.307319 | 0.320303 | 0.333618 | 0.347395 | 0.361601 | 0.376253 | 0.391358 | 0.391358 | 0.391358 | 0.391358 | 0.391358 |
| 119 | All | 0.060784 | 0.0488894 | 0.0455492 | 0.0413756 | 0.0467298 | 0.0475465 | 0.0510594 | 0.0542534 | 0.057097 | 0.057679 | 0.0594362 | 0.061199 | 0.062989 | 0.0647974 | 0.0666247 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 |
| 120 | All | 0.217734 | 0.176876 | 0.166476 | 0.152784 | 0.174356 | 0.179276 | 0.194577 | 0.20898 | 0.222335 | 0.227082 | 0.236615 | 0.246387 | 0.256496 | 0.266915 | 0.277659 | 0.288731 | 0.288731 | 0.288731 | 0.288731 | 0.288731 |
| 121 | All | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 |
| 122 | All | 0.936977 | 0.759087 | 0.712505 | 0.652118 | 0.742155 | 0.760999 | 0.823669 | 0.882192 | 0.935962 | 0.953283 | 0.990526 | 1.02854 | 1.06773 | 1.10796 | 1.1493 | 1.19173 | 1.19173 | 1.19173 | 1.19173 | 1.19173 |
| 123 | Power | 5.85636 | 4.7286 | 4.4234 | 4.03467 | 4.5759 | 4.67575 | 5.04302 | 5.38217 | 5.68976 | 5.77409 | 5.97775 | 6.18428 | 6.39596 | 6.61202 | 6.83262 | 7.05768 | 7.05768 | 7.05768 | 7.05768 | 7.05768 |
| 128 | Road accidents - gasoline | 0.0423861 | 0.0343589 | 0.0314842 | 0.0284638 | 0.0322049 | 0.0331571 | 0.0358265 | 0.0382694 | 0.0404957 | 0.0409011 | 0.0422092 | 0.0435663 | 0.0449834 | 0.0464629 | 0.0480066 | 0.0496133 | 0.0512967 | 0.0530592 | 0.0549027 | 0.0568334 |
| 129 | Road accidents - diesel | 0.013174 | 0.00968533 | 0.00870486 | 0.00792335 | 0.00867499 | 0.00894511 | 0.0097038 | 0.0104114 | 0.0110568 | 0.0111981 | 0.0115804 | 0.0119725 | 0.012382 | 0.0128028 | 0.0132336 | 0.0136781 | 0.014139 | 0.0146144 | 0.0151031 | 0.0155943 |
| 130 | Congestion - gasoline | 0.0359517 | 0.0378394 | 0.037405 | 0.0395984 | 0.0422519 | 0.0455084 | 0.0494033 | 0.0533794 | 0.0574052 | 0.0617276 | 0.0663509 | 0.0712926 | 0.0765889 | 0.0822635 | 0.0883408 | 0.0948407 | 0.101822 | 0.109317 | 0.117351 | 0.12596 |
| 131 | Congestion - diesel | 0.0111741 | 0.0106664 | 0.0103419 | 0.0110228 | 0.0113813 | 0.0122772 | 0.0133812 | 0.0145222 | 0.0156738 | 0.0169001 | 0.0182038 | 0.0195919 | 0.0210816 | 0.0226677 | 0.0243522 | 0.026147 | 0.0280653 | 0.0301097 | 0.0322818 | 0.0345617 |
| 133 | Road damage - diesel | 0.148468 | 0.140497 | 0.135773 | 0.134828 | 0.134486 | 0.135095 | 0.135797 | 0.136534 | 0.137298 | 0.138101 | 0.13894 | 0.139816 | 0.140735 | 0.141686 | 0.142667 | 0.143679 | 0.14472 | 0.145785 | 0.146872 | 0.147965 |
| 136 | Coal | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| 137 | Natural gas | 3.05794 | 3.18026 | 3.30747 | 3.43976 | 3.57736 | 3.72045 | 3.86927 | 4.02404 | 4.185 | 4.3524 | 4.5265 | 4.70756 | 4.89586 | 5.09169 | 5.29536 | 5.50717 | 5.72746 | 5.95656 | 6.19482 | 6.44262 |
| 138 | Gasoline | 0.129101 | 0.134265 | 0.139636 | 0.145222 | 0.15103 | 0.157072 | 0.163354 | 0.169889 | 0.176684 | 0.183752 | 0.191102 | 0.198746 | 0.206695 | 0.214963 | 0.223562 | 0.232504 | 0.241804 | 0.251477 | 0.261536 | 0.271997 |
| 139 | Diesel | 0.14737 | 0.153265 | 0.159396 | 0.165771 | 0.172402 | 0.179298 | 0.18647 | 0.193929 | 0.201686 | 0.209754 | 0.218144 | 0.22687 | 0.235944 | 0.245382 | 0.255198 | 0.265405 | 0.276022 | 0.287063 | 0.298545 | 0.310487 |
| 140 | LPG | 0.0969162 | 0.100793 | 0.104825 | 0.109018 | 0.113378 | 0.117913 | 0.12263 | 0.127535 | 0.132636 | 0.137942 | 0.14346 | 0.149198 | 0.155166 | 0.161373 | 0.167827 | 0.174541 | 0.181522 | 0.188783 | 0.196334 | 0.204188 |
| 141 | Kerosene | 0.141032 | 0.146673 | 0.15254 | 0.158642 | 0.164987 | 0.171587 | 0.17845 | 0.185588 | 0.193012 | 0.200732 | 0.208761 | 0.217112 | 0.225796 | 0.234828 | 0.244221 | 0.25399 | 0.26415 | 0.274716 | 0.285704 | 0.297133 |
| 142 | Non-road oil | 22.6037 | 23.5079 | 24.4482 | 25.4261 | 26.4431 | 27.5009 | 28.6009 | 29.7449 | 30.9347 | 32.1721 | 33.459 | 34.7974 | 36.1893 | 37.6368 | 39.1423 | 40.708 | 42.3363 | 44.0298 | 45.791 | 47.6226 |
| 146 | None | 0 | 0 | 0 | 0 | 0.2 | 0.4 | 0.6 | 0.8 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 148 | Power | 0 | 0 | 0 | 0 | 1.35186 | 2.80832 | 4.39624 | 6.11219 | 7.96026 | 8.26235 | 8.59181 | 8.93387 | 9.28932 | 9.65856 | 10.0421 | 10.4406 | 10.8204 | 11.2154 | 11.6262 | 12.0534 |
| 149 | Residential | 0 | 0 | 0 | 0 | 1.23352 | 2.56571 | 4.00251 | 5.55015 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| 150 | Industry | 0 | 0 | 0 | 0 | 1.60708 | 3.33032 | 5.24144 | 7.31594 | 9.55231 | 9.8794 | 10.2674 | 10.6689 | 11.0853 | 11.5169 | 11.9643 | 12.428 | 12.8077 | 13.2027 | 13.6135 | 14.0407 |
| 151 | Power | 0 | 0 | 0 | 0 | 0.804494 | 1.67092 | 2.61851 | 3.6437 | 4.74846 | 4.92683 | 5.12393 | 5.32852 | 5.5411 | 5.76189 | 5.99124 | 6.22945 | 6.44974 | 6.67884 | 6.9171 | 7.16489 |
| 152 | Residential | 0 | 0 | 0 | 0 | 0.715783 | 1.4888 | 2.3225 | 3.2205 | 4.1866 | 4.35402 | 4.52814 | 4.70922 | 4.89754 | 5.09339 | 5.29708 | 5.50891 | 5.7292 | 5.9583 | 6.19656 | 6.44436 |
| 153 | Industry | 0 | 0 | 0 | 0 | 0.762603 | 1.58513 | 2.47943 | 3.44537 | 4.48582 | 4.65972 | 4.8468 | 5.04117 | 5.24325 | 5.45329 | 5.67161 | 5.89853 | 6.11882 | 6.34792 | 6.58618 | 6.83397 |
| 154 | All | 0 | 0 | 0 | 0 | 0.0544434 | 0.113313 | 0.179786 | 0.252633 | 0.331682 | 0.344059 | 0.359098 | 0.374804 | 0.391257 | 0.408487 | 0.426534 | 0.445427 | 0.463392 | 0.482321 | 0.502258 | 0.523259 |
| 155 | All | 0 | 0 | 0 | 0 | 0.10026 | 0.205957 | 0.323957 | 0.451502 | 0.58805 | 0.603035 | 0.623484 | 0.644638 | 0.666638 | 0.689454 | 0.713109 | 0.73764 | 0.751677 | 0.766303 | 0.781532 | 0.797338 |
| 156 | All | 0 | 0 | 0 | 0 | 0.157674 | 0.317162 | 0.478573 | 0.642022 | 0.807629 | 0.812934 | 0.818452 | 0.82419 | 0.830158 | 0.836365 | 0.84282 | 0.849533 | 0.856514 | 0.863775 | 0.871327 | 0.87918 |
| 157 | All | 0 | 0 | 0 | 0 | 0.181428 | 0.373034 | 0.601271 | 0.854224 | 1.12897 | 1.15402 | 1.19929 | 1.24565 | 1.29352 | 1.34279 | 1.39352 | 1.44572 | 1.45588 | 1.46644 | 1.47743 | 1.48886 |
| 158 | Power | 0 | 0 | 0 | 0 | 6.20381 | 12.8706 | 20.1864 | 28.1017 | 36.6245 | 37.9462 | 39.4368 | 40.9816 | 42.5852 | 44.2489 | 45.9749 | 47.7657 | 49.394 | 51.0874 | 52.8486 | 54.6803 |

Efficient prices and Pigouvian reference values (scenario 2):

| Row | Label | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17962 | Gasoline - efficient price | 1.40346 | 1.22331 | 1.16007 | 1.03764 | 1.1432 | 1.06711 | 1.06136 | 1.06748 | 1.07486 | 1.07732 | 1.09451 | 1.11248 | 1.1313 | 1.15103 | 1.17171 | 1.19337 | 1.21399 | 1.23572 | 1.25863 | 1.28278 |
| 17969 | Potential VAT (assuming general rate) | 0.172355 | 0.150231 | 0.142464 | 0.127429 | 0.140393 | 0.131048 | 0.130342 | 0.131094 | 0.132001 | 0.132303 | 0.134414 | 0.13662 | 0.138932 | 0.141355 | 0.143894 | 0.146554 | 0.149086 | 0.151756 | 0.154569 | 0.157535 |
| 17974 | Pigouvian tax | 0.268223 | 0.255353 | 0.254074 | 0.254659 | 0.272217 | 0.283283 | 0.29965 | 0.315812 | 0.331726 | 0.344134 | 0.359214 | 0.374972 | 0.391488 | 0.408795 | 0.426931 | 0.445929 | 0.464016 | 0.483085 | 0.503181 | 0.524363 |
| 17976 | Pigouvian tax CO2 equivalent | 113.857 | 108.394 | 107.851 | 108.099 | 115.552 | 120.25 | 127.197 | 134.058 | 140.813 | 146.08 | 152.481 | 159.17 | 166.181 | 173.528 | 181.226 | 189.291 | 196.968 | 205.063 | 213.594 | 222.585 |
| 17977 | Diesel - efficient price | 1.84052 | 1.53426 | 1.43533 | 1.29985 | 1.42041 | 1.34528 | 1.34903 | 1.3645 | 1.3807 | 1.38607 | 1.40964 | 1.43405 | 1.45944 | 1.48579 | 1.51312 | 1.54148 | 1.5579 | 1.57502 | 1.59286 | 1.61137 |
| 17989 | Pigouvian tax | 0.537921 | 0.490991 | 0.480691 | 0.472329 | 0.501301 | 0.515019 | 0.540206 | 0.564826 | 0.588691 | 0.603888 | 0.624569 | 0.645976 | 0.668252 | 0.691366 | 0.715342 | 0.740216 | 0.75462 | 0.769637 | 0.785281 | 0.801526 |
| 17991 | Pigouvian tax CO2 equivalent | 200.034 | 182.582 | 178.752 | 175.642 | 186.416 | 191.517 | 200.883 | 210.039 | 218.913 | 224.565 | 232.255 | 240.216 | 248.499 | 257.095 | 266.01 | 275.26 | 280.616 | 286.201 | 292.018 | 298.059 |
| 17992 | LPG - efficient price | 1.6446 | 1.54279 | 1.50796 | 1.43203 | 1.49309 | 1.4401 | 1.42947 | 1.427 | 1.42576 | 1.42415 | 1.43044 | 1.43698 | 1.44378 | 1.45086 | 1.45822 | 1.46587 | 1.47383 | 1.48211 | 1.49071 | 1.49967 |
| 18001 | Pigouvian tax | 0.771908 | 0.775785 | 0.779817 | 0.78401 | 0.78837 | 0.792905 | 0.797622 | 0.802527 | 0.807629 | 0.812934 | 0.818452 | 0.82419 | 0.830158 | 0.836365 | 0.84282 | 0.849533 | 0.856514 | 0.863775 | 0.871327 | 0.87918 |
| 18003 | Pigouvian tax CO2 equivalent | 436.48 | 438.672 | 440.951 | 443.322 | 445.788 | 448.353 | 451.02 | 453.793 | 456.678 | 459.678 | 462.798 | 466.043 | 469.417 | 472.927 | 476.577 | 480.373 | 484.32 | 488.426 | 492.696 | 497.137 |
| 18004 | Kerosene - efficient price | 2.12185 | 1.82912 | 1.77437 | 1.60324 | 1.78904 | 1.73932 | 1.79693 | 1.86087 | 1.92108 | 1.93925 | 1.99086 | 2.04372 | 2.09829 | 2.15446 | 2.21228 | 2.27179 | 2.28337 | 2.29542 | 2.30795 | 2.32097 |
| 18013 | Pigouvian tax | 1.07801 | 0.90576 | 0.865045 | 0.81076 | 0.907142 | 0.932585 | 1.00212 | 1.06778 | 1.12897 | 1.15402 | 1.19929 | 1.24565 | 1.29352 | 1.34279 | 1.39352 | 1.44572 | 1.45588 | 1.46644 | 1.47743 | 1.48886 |
| 18015 | Pigouvian tax CO2 equivalent | 418.89 | 351.958 | 336.137 | 315.043 | 352.495 | 362.382 | 389.401 | 414.916 | 438.694 | 448.424 | 466.016 | 484.033 | 502.634 | 521.779 | 541.49 | 561.773 | 565.721 | 569.827 | 574.097 | 578.537 |
| 18016 | Coal in industry - efficient price | 18.7686 | 16.0151 | 15.0793 | 14.2925 | 15.2265 | 15.6237 | 15.983 | 16.3379 | 16.6872 | 16.9582 | 17.3462 | 17.7477 | 18.1641 | 18.5957 | 19.0431 | 19.5067 | 19.8865 | 20.2815 | 20.6923 | 21.1195 |
| 18025 | Pigouvian tax | 7.64822 | 7.40437 | 7.50236 | 7.57474 | 8.03539 | 8.3258 | 8.73574 | 9.14493 | 9.55231 | 9.8794 | 10.2674 | 10.6689 | 11.0853 | 11.5169 | 11.9643 | 12.428 | 12.8077 | 13.2027 | 13.6135 | 14.0407 |
| 18027 | Pigouvian tax CO2 equivalent | 79.5011 | 76.9663 | 77.9849 | 78.7373 | 83.5256 | 86.5444 | 90.8056 | 95.059 | 99.2937 | 102.694 | 106.727 | 110.9 | 115.229 | 119.715 | 124.366 | 129.185 | 133.133 | 137.239 | 141.509 | 145.949 |
| 18028 | Coal in residential - efficient price | 29.199 | 21.9015 | 21.2434 | 20.148 | 21.1652 | 21.6149 | 21.8275 | 22.0461 | 22.2708 | 22.5113 | 22.8535 | 23.2093 | 23.5794 | 23.9643 | 24.3646 | 24.7809 | 25.2139 | 25.6642 | 26.1325 | 26.6195 |
| 18037 | Pigouvian tax | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| 18040 | Coal in power - efficient price | 19.3211 | 12.7486 | 12.1829 | 11.269 | 12.1803 | 12.5777 | 12.8196 | 13.0636 | 13.3097 | 13.5404 | 13.8698 | 14.2119 | 14.5674 | 14.9366 | 15.3202 | 15.7187 | 16.0984 | 16.4934 | 16.9042 | 17.3314 |
| 18049 | Pigouvian tax | 6.02031 | 6.08891 | 6.27082 | 6.45052 | 6.75932 | 7.0208 | 7.32706 | 7.64024 | 7.96026 | 8.26235 | 8.59181 | 8.93387 | 9.28932 | 9.65856 | 10.0421 | 10.4406 | 10.8204 | 11.2154 | 11.6262 | 12.0534 |
| 18052 | Natural gas in industry - efficient price | 15.6125 | 13.6107 | 13.1019 | 13.2926 | 13.6418 | 13.5743 | 13.4883 | 13.5716 | 13.7249 | 13.8842 | 14.0713 | 14.2656 | 14.4677 | 14.6777 | 14.8961 | 15.123 | 15.3433 | 15.5724 | 15.8106 | 16.0584 |
| 18061 | Pigouvian tax | 3.35192 | 3.41914 | 3.53236 | 3.64621 | 3.81301 | 3.96282 | 4.13239 | 4.30671 | 4.48582 | 4.65972 | 4.8468 | 5.04117 | 5.24325 | 5.45329 | 5.67161 | 5.89853 | 6.11882 | 6.34792 | 6.58618 | 6.83397 |
| 18064 | Natural gas in residential - efficient price | 22.7498 | 20.7356 | 20.1737 | 20.4074 | 20.7613 | 20.6898 | 20.5834 | 20.6616 | 20.8172 | 20.9922 | 21.1907 | 21.3971 | 21.6118 | 21.8351 | 22.0673 | 22.3088 | 22.5599 | 22.8211 | 23.0927 | 23.3752 |
| 18073 | Pigouvian tax | 3.05942 | 3.18176 | 3.309 | 3.4413 | 3.57891 | 3.72201 | 3.87084 | 4.02562 | 4.1866 | 4.35402 | 4.52814 | 4.70922 | 4.89754 | 5.09339 | 5.29708 | 5.50891 | 5.7292 | 5.9583 | 6.19656 | 6.44436 |
| 18076 | Natural gas in power - efficient price | 15.1054 | 13.0234 | 12.5008 | 12.6833 | 13.0795 | 12.9911 | 12.8917 | 12.9802 | 13.1451 | 13.3071 | 13.5042 | 13.7088 | 13.9214 | 14.1422 | 14.3715 | 14.6097 | 14.83 | 15.0591 | 15.2974 | 15.5452 |
| 18085 | Pigouvian tax | 3.61784 | 3.63427 | 3.73401 | 3.83052 | 4.02247 | 4.17729 | 4.36419 | 4.55462 | 4.74846 | 4.92683 | 5.12393 | 5.32852 | 5.5411 | 5.76189 | 5.99124 | 6.22945 | 6.44974 | 6.67884 | 6.9171 | 7.16489 |
| 18088 | Electricity in industry - efficient price | 0.0746921 | 0.0710401 | 0.114839 | 0.112735 | 0.113787 | 0.114724 | 0.115697 | 0.116977 | 0.118263 | 0.118258 | 0.116755 | 0.115443 | 0.114149 | 0.11296 | 0.111846 | 0.110806 | 0.109473 | 0.108222 | 0.107042 | 0.105914 |
| 18090 | Air pollution costs | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |
| 18097 | Pigouvian tax | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |
| 18100 | Electricity in residential - efficient price | 0.0802058 | 0.0683401 | 0.123663 | 0.121571 | 0.122828 | 0.123831 | 0.124975 | 0.126408 | 0.127852 | 0.127756 | 0.126296 | 0.125003 | 0.123728 | 0.122558 | 0.121462 | 0.120439 | 0.119073 | 0.117792 | 0.116586 | 0.115435 |
| 18109 | Pigouvian tax | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |
| 18117 | Pigouvian tax CO2 equivalent | 128.173 | 130.578 | 130.993 | 129.411 | 135.391 | 139.556 | 145.527 | 151.39 | 157.493 | 162.107 | 167.684 | 172.531 | 177.855 | 183.254 | 188.882 | 194.714 | 199.312 | 204.104 | 209.084 | 214.256 |
| 18118 | Pigouvian tax CO2 equivalent | 128.173 | 130.58 | 130.995 | 129.413 | 135.392 | 139.458 | 145.397 | 151.235 | 157.322 | 161.888 | 167.416 | 172.223 | 177.51 | 182.869 | 188.457 | 194.247 | 198.796 | 203.536 | 208.46 | 213.572 |
| 18122 | Air pollution Pigouvian tax CO2 equivalent | 56.5493 | 56.723 | 55.3553 | 52.0628 | 55.1643 | 56.2826 | 58.891 | 61.3063 | 63.7816 | 64.8399 | 66.6181 | 67.7496 | 69.1198 | 70.4284 | 71.7842 | 73.1637 | 73.1161 | 73.0623 | 72.9938 | 72.9103 |
| 18123 | Air pollution Pigouvian tax CO2 equivalent | 56.5493 | 56.7247 | 55.3566 | 52.064 | 55.1655 | 56.1958 | 58.767 | 61.1494 | 63.599 | 64.6065 | 66.3339 | 67.4215 | 68.7493 | 70.0135 | 71.3251 | 72.6588 | 72.5589 | 72.4502 | 72.3242 | 72.179 |

CBAM pre-policy emissions (Mt; everything downstream = 0):

| Row | Label | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5960 | Total Emissions | 20.9262 | 21.6212 | 22.3402 | 23.084 | 23.8536 | 24.6498 | 25.4737 | 26.3261 | 27.2082 | 28.121 | 29.0656 | 30.0432 | 31.0549 | 32.102 | 33.1858 | 34.3075 | 35.4687 | 36.6706 | 37.9148 | 39.2028 |
| 5971 | Total Emissions | 26.0903 | 26.9619 | 27.863 | 28.7946 | 29.7578 | 30.7537 | 31.7834 | 32.8481 | 33.949 | 35.0874 | 36.2644 | 37.4816 | 38.7403 | 40.042 | 41.388 | 42.7801 | 44.2198 | 45.7087 | 47.2487 | 48.8414 |

## D. R5 green public investment; R11 current account; R12 GVA and emissions intensity

## Notes for the builder: R5, R11, R12

Columns of legacy 465 Mitigation: K = 2021, L = 2022 (FirstYearCalculations) ... AE = 2041 (rows 2178, 6194, 8017).
The brief's "K = 2022" does not hold on Mitigation. Scenario 2 copy of a scenario-1 row r is row r + 6316.

### Legacy bugs found (proposed)

| Id | Cell(s) | Formula now | Formula intended | Effect on Egypt |
|---|---|---|---|---|
| L204 | Mitigation K6239 (and K12555) | `=K6238*K$6234` (cash transfers) | `=K6238*K6232` (public capital investment, as L:AD) | None: column K = 2021, K8024 = 0. Out of the prototype horizon. |
| L205 | K6243:AD6243; K12559:AD12559 | `=K8029` / `=K14345` (row 8029 = "Change in population") | `=K8020` / `=K14336` (fiscal revenues raised, % GDP, additional) | Scen. 2 shows population growth (0.0149 in 2022 ... 0.04) as net revenue % GDP; intended 0 ... 0.0028 (2040). |
| L206 | K6244:AD6244; K12560:AD12560 | `=K6243*K$6234` / `=K12559*K$6234` (cash transfer share, and the scen.-1 block) | `=K6243*K6232` / `=K12559*K12548` | Share 0.2 used instead of 0.5 (EXPTransfers vs EXPCapex). |
| L207 | K6245:AD6245; K12561:AD12561 | `=$D$6222*K6244` (Net Zero End Year, 2060) | `=$D6220*K6244` / `=$D12536*K12560` (green proportion 0.5, as row 6240) | Scen. 2 cached 2040: 16.48 (1648 % of GDP); intended 0.0007 (0.07 %). |
| L208 | K6249:AD6249; K12565:AD12565 | `=IF(K6248>=$D6219,$H$6229,0)` (H6229 blank) | `=IF(K6248>=$D6219,$H$6227,0)` / `$H$12543` | 0 instead of 0.0086 from 2026 (dead-end row). |
| L209 | L6256:AD6256; L12572:AD12572 | `=IF(L6248<$D$6223,1,K6256-$D$6225)` (D6223 = increment 0.029; D6225 blank) | `=IF(L6248<$D6221,1,K6256-$D6223)` (start year; increment); scen. 2: `$D12537`, `$D12539` | φ = 0 every year (should be 1 to 2025, then −1/34 a year): NZ path, reduction and abatement all 0. |
| L210 | P6250:AD6250; P12566:AD12566 | `=$H$6252*(1-P6256)` (H6252 blank) | `=$H$6250*(1-P6256)` / `=$H$12566*(1-P12572)` | 0 instead of 0.0088 (2026) ... 0.132 (2040). |
| L211 | P6251:AD6251, L6261:AD6261; P12567:AD12567, L12577:AD12577 | `=P6250*$D$6226`, `=L6260*$D$6226` (D6226 = header text "Mitigation ($2020 bn)") | `=P6250*$D6224`, `=L6260*$D6224` (public part 0.5; H6251 = H6261 = D6224 show the intent); scen. 2 `$D12540` | #VALUE! in rows 6251, 6261, 6265, 6266 (and 12567, 12577, 12581, 12582). |
| L212 | L6255:AD6255; L12571:AD12571 | `=L$7628` (row 7628 blank, between the section-16 band 7627 and its info rows) | `=L$7626` (Total GHGs exc LULUCF, `ghg.tot.1`; scenario 1 in both blocks = BAU) | BAU emissions 0 instead of 400.9 (2022) ... 715.4 Mt (2040). Row 7626 is the only total in reach (rows inserted above shifted the reference); prototype: `ghg.ref`. |
| L213 | L12580:AD12580 (scen. 2) | `=SUM($K$6247:L12561)` (rows 6247-12561, thousands of rows) | `=SUM($K12561:L12561)`; scen. 1 `=SUM($K6245:L$6247)` works only because 6246-6247 are blank, intended `=SUM($K6245:L6245)` | #VALUE! (scen. 2). |
| L214 | Mitigation L18195:AE18195 | `=L18191+L18192+L18193` | `=L18191+L18192+L18193+L18194` (coal, as 18188 = SUM(18184:18187)) | Coal effect left out of the % GDP total (2041: 0.0037 pp; coal use change −102.5 ktoe). |
| L215 | Mitigation L18172:AE18172 | `=L18171*_conv_ktoe_to_gj*L709/10^9*$H741` (L709 in $/MMBtu) | `...*L733/...` ($/GJ real, as row 741) | Gas effect 5.5 % too large (1.055 GJ per MMBtu). Prototype `xnim` uses the section-2 supply price in $/GJ: not replicated already. |
| L216 | Mitigation H18756 | `=L18731/(SUMIF(..,"ftr",..)*(1+$J$15705))*10^6` (L18731 = total industrial indirect CO2) | `=L18730/(...)*10^6` (fuel transformation's own) | ftr indirect intensity 453.32 → 216.35; total 820.06 → 583.10 tCO2/$m (MTOutputs M134, chart). |
| L217 | Mitigation H18762, H18763 | `=L18638` (srv row reads food CO2), `=L18639` (foo row reads services CO2) | H18762 `=L18639`, H18763 `=L18638` (as G18747 = L18638 for food) | Emissions share srv 0.0415 → 0, foo 0 → 0.0415 (MTOutputs L143, L135, and O135-O143). |
| L218 | MTOutputs L141 | `=ROUND(Mitigation!J18767,2)` (intensity) | `=ROUND(Mitigation!I18767,2)` (emissions share, as L134:L143) | Machinery emissions share 48.78 → 0; cumulative O141:O143 49.74, 49.74, 49.78 → 1.00, 1.00, 1.00. |
| L219 | Mitigation J18747, J18748 (check column) | `=L18733/...`, `=L18734/...` (a label row and a year row) | no foo/srv rows in 18735-18742: check against I18747 itself, or drop | Check column only; not built. |

L50 (known): the cell plan to redo. In 465 the pre-policy current account (18182, 18191, 18198) looks up `egy.bca_bp6`
and `egy.bca_gdp_bp6` in WEO_codes, but the WEO sheet now uses `EGY.BCA.A` and `EGY.BCA_NGDPD.A` (rows 843-844): MATCH
gives #N/A (J18182, J18191, J18198), stored as #NAME? through `_xlfn.IFNA`. Fix: codes `bca.a`, `bca_ngdpd.a`. The
"column lag" of L50 is row 18200 (`=SUM(K741:K743)`: trade balance of t−1), already not replicated by 16b (`xtb`). The
"sign" is a label issue: rows 741-743 and 18200-18204 are trade balances (exports − imports), labelled "net imports";
the arithmetic (18203 = 18200 − ΔNI) is right.

L128 (known) does not reproduce in the .xlsb: K6238 `=K8024`, same column and year (row 6237 L = 2022 = row 8017 L).
Proposed: close it as "not reproduced" (like L123), after a check of the cell plan source.

### Issues to replicate

| Id | Issue | Replicate |
|---|---|---|
| I124 | Cumulative need H6250 `=H6227*(2060-2025)`: 35 years hard-coded, while the phase-out spans D6222 − D6221 = 34 years and reaches 0 in 2059 | as legacy (35; Λ step 1/34) |
| I125 | Section 10 stops at 2040 (K:AD, as the revenue allocation rows 2178-2184); 2041 blank | as legacy (2041 blank) |
| I126 | Green public investment is report only: it changes neither emissions nor GDP; its five parameters are typed in Mitigation D6219-D6224, not MTInputs | as legacy; constants on Settings, labelled legacy hard-coded |
| I127 | Countries outside the CCDR list (ETS+LTS rows 261-302, 42 rows) get #N/A in D6218 and every row of section 10 | as legacy (Egypt is in the list); IFERROR is a departure |
| I128 | CGI sums annual GDP shares of different years against a cumulative ratio of discounted CCDR GDP; net revenue includes base erosion (rev.new.usd, I41) | as legacy |
| I129 | % of GDP effects divide by GDP implied by CA/CA% (row 18192); fails when the current account is 0 | as legacy |
| I130 | Current-prices row 18198 has no hold rule: 0 for 2032-2040 (blank WEO cells), AE = AD; the USD row 18182 tests the % row (J18191) for non-zero | as legacy |
| I131 | GVA shares floored at 1 % for the chart (L18747:L18756, sum 1.0032) and passed to MTOutputs | as legacy |
| I132 | "GVA" is the GTAP OUTPUT column (gross output), so intensities are per USD of output; IO year 2014 inflated by the fixed 2014 CPI index $G$15631; label "thousands US$" but values are USD m | as legacy (typed values) |
| I133 | Cumulative table: emissions = direct only (H18762:H18771), next to total intensities; MTOutputs codes repeat (`emin.cem` in rows 124 and 138) and construction is `cst` (132) and `con` (140) | as legacy |
| I134 | Mapping column R sends GTAP `coa` (coal mining) to foo, `oil` (crude extraction) to ftr, `nga` to pow | as legacy (typed GVA) |

### Where it hooks in build.py

- **R5**: a new sub-block of section 16 (after `fis.*`, near `R_GDPS_AFTER`, line ~3424) or its own band. Reads
  `R_GDPS['fis.rev']`, `R_GDPS['fis.ref']`, `R_GDPS['fis.sp']` (GDP_BLOCKS, line 3389), the input row `EXPCapex`
  (GDP_PARAMS, line 370; MTInputs row 199 exists) with the CPIntro gate used by `fis.impp` (I43), `R_GHG['ghg.ref']`,
  and ETS+LTS!A261:A302 / H261:H302 (legacy_cells tab, line 5812; csv has rows 258-302). Missing inputs: the five
  constants D6219-D6224 (Settings: GreenInvStart 2026, GreenShare 0.5, NZStart 2026, NZEnd 2060, PublicInvPart 0.5).
- **R11**: EXT_BLOCKS (line 3443) and `c16b` (line 11649): new rows after `xnim.pct`; read `xnim.g.oil/nga/coa` and
  `infl` (US CPI index, ι). Typed rows `bca`, `bca.gdp`, `bca.n` (Egypt values below), in the typed-Egypt-data
  section with R1. Replace the note at line 11681 ("until WEO current-account data are added").
- **R12**: a base-year block (one column, t₀) e.g. in section 13b next to `co2.grid` (line 4020); reads `co2.sec.<s>`
  (EMI_ROWS, line 3220), `dem` of each subsector (power section, line 4390), `co2.grid`, θ_g (Settings). Typed `gva.<s>`.
  MTOutputs (build_mtoutputs, line 8614) is by year; the emin rows are a static table (two blocks, MTOutputs legacy
  rows 123-143).

### Typed data

**R11** (WEO sheet of 465, rows 843-844, last data year 2031; held flat after 2031 by legacy's IFNA/previous rule):

| Year | CA0 USD bn nominal (EGY.BCA.A) | ca0 % of GDP (EGY.BCA_NGDPD.A) | CAn current prices (row 18198) |
|---|---|---|---|
| 2022 | -16.5513 | -3.48279 | -16.5513 |
| 2023 | -4.7105 | -1.196082 | -4.7105 |
| 2024 | -20.8066 | -5.43104 | -20.8066 |
| 2025 | -15.4246 | -4.230086 | -15.4246 |
| 2026 | -17.834583 | -4.151002 | -17.834583 |
| 2027 | -20.950561 | -4.583618 | -20.950561 |
| 2028 | -19.674211 | -3.869298 | -19.674211 |
| 2029 | -19.613478 | -3.501898 | -19.613478 |
| 2030 | -19.398187 | -3.17492 | -19.398187 |
| 2031-2041 | -17.756772 | -2.667806 | 2031: -17.756772; 2032-2041: 0 |

Cached legacy values 2022-2041 of rows 18182-18198: all #NAME?/#N/A (bug L50). The values above are what legacy
computes with the codes fixed.

**R12** (legacy K18747:K18756, base year 2022, USD bn of 2026):

| foo | srv | mch | irn | nfm | mac | cem | omn | cst | ftr | total |
|---|---|---|---|---|---|---|---|---|---|---|
| 263.98475 | 374.72957 | 32.67380 | 6.97331 | 12.09939 | 53.47002 | 25.81484 | 125.57658 | 66.67669 | 69.38984 | 1031.38879 |

(= GTAP OUTPUT 2014 by CPAT sector, USD m, x 1.4053307 (US CPI 2026/2014) x 1.4995617 (WEO GDP 2022 / GTAP GDP) / 1000.)

### Egypt values for the regression test

**R5**, scenario 2, intended (bugs fixed; prototype inputs as legacy: EXPCapex 50 from CPIntro 2026):

| Year | ΔR USD bn | GI USD bn | fs | GI% | φ | E_B Mt | ER Mt | PReq | CGI | π | ERg Mt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2022 | 0 | 0 | 0 | 0 | 1 | 400.94 | 0 | - | 0 | - | - |
| 2026 | 0.000647 | 0.000162 | 1.02e-6 | 2.56e-7 | 0.9706 | 497.57 | -14.63 | 0.004408 | 2.56e-7 | 5.8e-5 | -0.0004 |
| 2030 | 0.8460 | 0.2115 | 0.001096 | 0.000274 | 0.8529 | 556.75 | -81.88 | 0.02204 | 0.000684 | 0.0310 | -1.270 |
| 2035 | 2.0466 | 0.5117 | 0.002109 | 0.000527 | 0.7059 | 627.08 | -184.4 | 0.04408 | 0.002839 | 0.0644 | -5.939 |
| 2040 | 3.3750 | 0.8438 | 0.002802 | 0.000701 | 0.5588 | 715.37 | -315.6 | 0.06612 | 0.006029 | 0.0912 | -14.39 |

m = 0.0085643 (29.7 / 3467.8765), Ncum = 0.29975. Full series 2022-2040: appendix "R5 and R11 series" below. Legacy cached
scen. 2: 12554-12556 as intended (USD rows are right); 12559 population growth; 12561 16.48 in 2040; 12565-12573,
12576 zero; 12567, 12577, 12580-12582 #VALUE!. Note ΔR and fs here are legacy's (rev.new, scen. 2 − scen. 1); the
prototype's fis.rev also counts I47 methane fee.

**R11** (legacy fuel effects 18185-18187, intended totals): 2030: CAr -17.798, ΔCA oil 0.2008, gas 0.0268, coal
0.0053, CA1 -17.565 USD bn, ca1 -3.1334 %; 2041: CAr -15.944, CA1 -14.962, ca1 -2.5036 %. ι(2022) = 1.13682,
ι(2031+) = 0.897896. Prototype ΔCA differs (xnim: supply prices, share on oil; L49).

**R12** (base year 2022, tCO2 per USD m; legacy cached / intended where a bug changes it):

| Sector | direct | indirect | total | GVA share | emissions share |
|---|---|---|---|---|---|
| foo | 9.78 | 21.23 | 31.01 | 0.26 | 0 → 0.0415 |
| srv | 0 | 46.09 | 46.09 | 0.36 | 0.0415 → 0 |
| mch | 0 | 54.95 | 54.95 | 0.03 | 0 |
| irn | 635.90 | 492.60 | 1128.51 | 0.01 | 0.0713 |
| nfm | 0 | 2.34 | 2.34 | 0.01 | 0 |
| mac | 0 | 48.78 | 48.78 | 0.05 | 0 |
| cem | 377.96 | 205.55 | 583.50 | 0.03 | 0.1568 |
| omn | 159.22 | 26.04 | 185.25 | 0.12 | 0.3214 |
| cst | 0 | 0 | 0 | 0.06 | 0 |
| ftr | 366.74 | 453.32 → 216.35 | 820.06 → 583.10 | 0.07 | 0.4090 |

Cumulative (ftr, foo, mch, omn, cem, irn, cst, mac, nfm, srv), intended: GVA 0.067, 0.323, 0.355, 0.477, 0.502,
0.512, 0.576, 0.628, 0.640, 1.003; emissions 0.409, 0.451, 0.451, 0.772, 0.929, 1.000, 1.000, 1.000, 1.000, 1.000.
Inputs at t₀: grid intensity 0.39386 MtCO2/TWh (82.215 Mt / 208.74 TWh), θ_g/1000 = 0.01163 TWh per ktoe, direct CO2
(Mt) foo 2.582, irn 4.434, cem 9.757, omn 19.994, ftr 25.448, others 0.

## E. R6-R10

## R6-R10: notes for the builder

Years are read from each sheet's own year row (Mitigation K = 2021, L = 2022 ... AE = 2041; rows 765-829 and
3594 ff. likewise K = 2021). Scenario 2 copies of the Mitigation rows: +6316 (e.g. 3509 -> 9825, 6203 -> 12519).

### 1. New legacy bugs (proposed)

| Id | Cell(s) | Formula now | Formula intended | Effect on Egypt |
|---|---|---|---|---|
| L220 | Manual inputs L319:L321 (feed Elasticities F131:F133, then C131:C133 when ElPrcMainSrc = Manual) | `=Elasticities!C91`, `C92`, `C93` (usage elasticities of services biomass, renewables, electricity: -0.4, -0.7, -0.5) | the cross-price defaults `=Elasticities!G131`, `G132`, `G133` (simple values, 0.25) | None by default (ElPrcMainSrc = Simple*). With Manual: the biomass/LPG substitution elasticity of the leakage (C131 -> _ResLpgKerBioSubstElasticity, E5572) turns -0.4, reversing leakage |
| L221 | Elasticities H29, H30, H37, H38, H45, H46 (standard deviation used by the Low / High adjustment) | `=H149`, `=H150`, `=H151`, `=H152`, `=H163`, `=H164` | `=H145`, `=H146`, `=H153`, `=H154`, `=H161`, `=H162` (own fuel) | None (equal values within a sector; only with ElastIncAdjustment Low/High). Extends known L116 (H53, H54), whose text "every other row reads its own" is wrong |
| L222 | Mitigation T9825 (E5 cost breakdown, scenario-2 block); header P9824 | `=IF(B$2173="Baseline",0,INDEX(L9400:AE9400,...))`; `P9824 =B$2173` | `=IF(B$8489="Baseline",0,...)` (own block's scenario name); P9824 a fixed label "Carbon price" | Policy scenario 2030: carbon-tax memo 0 instead of 1.4286 $/tCO2 (L9400 row = cptraj); header shows "Baseline" in both blocks |

### 2. Registered bugs not reproduced in 465 (cell evidence; please re-check their source version)

- **L48**: M5568:M5570 contain the income factor (`(1+M2446)^(_el_inc_nga_res*M2433)`); M5546:M5547 already test
  `LEFT(AlwaysExemptResLPGKer,3)="Yes"`. Nothing to fix; R6 keeps the income factor.
- **L82**: K2547 `=K$826` (gas), projection O2547 `=$J2548*O2213` (J2548 holds N2547). Correct.
- **L83**: O3601 `=$J3601*O2213`, O3630 `=$J3630*O2213`, O3592 `=$N3592*O2213`: base x factor of the year. Correct.
- **L84**: O3606 / O3635 `=IF(AND($J3606<0,PowerSubsidyExemptInclude="Include"),$J3606*O2214,$J3606)`: consumer factor
  2214; Dashboard L54 list is `"DoNotPhaseOut*,Include"`, so "Include" works. Only the MTInputs C138 unit text
  "Exempt/Include*" is stale (cosmetic).
- **L86, L100**: names `_manual_codes = 'Manual inputs'!$G$59:$G$146`, `_manual_prices = $G$59:$N$146`; I828
  `=MATCH($G828,_manual_codes,0)` = 88 (row 146). Manual electricity prices and producer subsidy are read in 465.
- **L46**: M5406 uses price row 5392 (= biomass block 2720/2721 x road coverage), shadow `M2388*M2404` inside the
  efficiency term, AEEI `_eff_imp_oil_rod`, α+ `$M2199` (road). Only the oil elasticities remain (issue I143).
- **L47**: M5491 and M5516 use `(1+M2439)` (the shock row of every fuel row). Correct.
- **L92**: already marked not reproduced in the register. **L94** stands (rows 5568-5570 `MIN(M2258/ExemptPhaseoutPeriod,1)`,
  row 2258 = years since CPIntro, no switch) and is fixed by R6.4. **L101** confirmed (Elasticities F51:F58 read column M).
  **L135** confirmed (indices 6159, 6171, 6183 computed, rows 6203, 6206, 6212 do not multiply them).

### 3. Issues to replicate (new)

- **I135** Initially exempt demand mutes the usage response to every price change, not only to the new
  policy: rows 5568-5570 raise the after-tax price ratio to εU·phase, phase = 0 before the phase-out, in every
  scenario including scenario 1 (baseline world-price moves too). The prototype already does this (lkx); keep.
- **I136** Exempt share denominator = economy-wide spend from the basket row (K1793 = bsh_bkt x total
  consumption), not the sum of deciles. With mean budget shares the ten decile parts do not sum to 1 (Egypt LPG: Σ
  deciles / basket = 0.822). Egypt, 4 deciles, LPG: legacy 27.26 %, prototype now 33.16 % (Σ deciles). Change C83.
- **I137** Most-used cooking fuel defaults to "lpg" when the WHOCooking code is missing (L1784
  `IFNA(...,"lpg")`); prototype C65 gives "". Change C65 (affects leakage too).
- **I138** Leakage to biomass is computed on the not-exempt use only (5577 = -L5564 x share ...).
- **I139** (I53 known) Manual price rows switch on only with a 2021 value; manual years 2021-2026 only.
- **I140** A blank manual elasticity gives "no data" and an error in the elasticity (Elasticities F column):
  replicate as #N/A plus a check, not a silent fallback.
- **I141** Methane intensity decline: biomass and downstream gas use the oil-and-gas rate J185 (rows 6078,
  6079); coal J186 = 0; agriculture J187 = 0.4719 %/y; waste J188 = 0.5 %/y. Decline from 2024 (index 1 in 2023).
- **I142** E5 cost breakdown has no shadow-price (D6) column and ignores the MinPostSubsidyPowerPrice floor;
  checksum S shows the gap (0 for Egypt in both scenarios). Keep the checksum.
- **I143** Road other biofuels (elasticity model) use oil elasticities and oil AEEI with the biomass price.
- **I144** Self-generated renewables are priced at the solar levelised investment cost (row 3468), carry no
  new policy (nce typed 0) and no shadow price, with the transport ("rod") renewables elasticities.
- **I145** Range anxiety may be negative; a negative start value is then held (rows 4354-4356
  `IF(N<0,N,...)`); the fit uses one year (Transport3 A1 = 2025); freight residual scaled x 10 (no effect on the root);
  missing country -> average of the stored table.
- **I146** Electricity producer subsidy per kWh floored at -0.3 $/kWh (H3590:H3591); the part above the floor
  is a residual (3592) outside prices; allocation by the pre-tax gap x consumption (3588).

### 4. Where it hooks in (build.py)

- **R6**: `_layout_lk` (line ~3040): `lkd` base -> `ener(t-1) - lkx(t-1)` (LEAKCHANGE gets a second argument);
  Settings C83 denominator -> basket row `CtryCode&".distn.bsh.bkt.ove.mean.9999"` (b x cons_pc_acrent x popw);
  Settings C65 fallback `"lpg"`. PHASEIN/XPATH/XADJ unchanged. LegacyDiff 67: status Same after the build;
  Equations.md last section: replace "Σ deciles" wording.
- **R7**: `price_formula` 'sp' (line ~9350, LAMBDA SUPPLYCOST): use `psp*psf` (new block row psb) in place of `psp`
  now and last year; `ppsw` -> 0 (or memo), `pvatn` parts and `rsr` (drop `psw x VAT`); LegacyDiff LD19 text is stale
  (says "no price effect"; v6.1-6.2 built it): set to "Same" after R7. Power section G: new rows ps.ecy.sh, ps.ecy,
  ps.ecy.res; `rppre` gets the Δps term; Inputs_power must read `mit.txo.ecy.res/ind` (Prices_dom) by year.
- **R8**: Inputs_prices `dom()` helper (line ~7068) -> wrap with the manual override (Manual inputs I:N by code G,
  year row 59); Inputs_power `dom()` (line ~7953) likewise for ecy; policy `pros` (PRODSUB). Inputs_ela (line ~7495):
  IF(src = Manual, Manual inputs K:N by key, country value) with MAX/MIN clamps. Section 14 `ch4.em`: x `ch4.int`.
  MI_BLOCKS notes for blocks 57-146, 183-200 and 271-327 -> "Read".
- **R9**: section 3 block G: `csd` row; MTInputs row PowerSubsidyExemptInclude (new); block E: rows cur, sys, and a
  memo table pcb.* (types x 8 columns) for CostBreakdownYear.
- **R10**: elasticity road block (section 5 road): rows bgs, bdi, obf; bio = their sum (BIOSPLIT remains for the
  engineer branch); new fuel row `ren` in avi and nav (not a FUELS member: a sector-local row added to the totals);
  range-anxiety goal seek: a macro / Python script like `ets_goalseek.py` writing RAPas/RAFre/RACyc for the country.

### 5. Inputs: present / missing

- Present in ScenarioDefinition (names.tsv), not read: DomPrTax, ElIncMainSrc, ElPrcMainSrc, CostBreakdownYear
  (legacy MTInputs 342, default 2030), SupplyCostDeltaSubsidy, ElastIncAdjustment. Read: ExemptMostCook,
  ExemptCookDeciles, ExemptPhaseout, YearPha, ExemptPhaseoutPeriod, BiomassLeakage, TrModel, producer-subsidy rows.
- Missing: PowerSubsidyExemptInclude (legacy MTInputs 138, options DoNotPhaseOut* / Include, default DoNotPhaseOut*);
  RngAnxietySource and PassAnxiety, FreightAnxiety, MotorAnxiety (+ Decline) (Dashboard G548:Q549, L61) are needed only
  if the Dashboard source is offered; the goal seek writes the stored table instead.
- Data: Prices_dom `mit.txo.ecy.*` (check the corrected Egypt block, issue I99, has it), EnergyCons `ren` of avi, nav
  (Egypt 0).

### 6. Egypt cached values (465) for regression

- R6: ExemptMostCook = No -> exempt rows 0; residential totals unchanged (L5557 = 3107.45 ktoe LPG 2022, M = 3427.70
  2023). With Yes, 4 deciles: share s (legacy formula) LPG 0.2726, nga 0.1829, ker 0.1207; Egypt m* = lpg.
- R7: Prices_dom pros all 0 for Egypt (rows 825-829 = 0; 3587 = 0) -> no change. Electricity txo 2024 (J3606, J3635):
  -0.05514 $/kWh real 2026, both groups.
- R8: DomPrTax = No, sources Simple*: no change. Methane, scenario 1, Mt CH4 (cached / with L135 fixed):
  livestock 2030 0.46972 / 0.45442, 2041 0.69387 / 0.63723; rice 2030 0.27508 / 0.26612, 2041 0.40635 / 0.37319;
  waste 2030 1.48266 / 1.43154, 2041 2.26054 / 2.06551. Indices 6159 (agr) 2041 = 0.91838, 6183 (waste) 2041 = 0.91372;
  oil and gas EF 6077: 2023 0.61951, 2041 0.59222 t CH4/ktoe (already declining in legacy).
- R9: E5 breakdown 2030, scenario 1 (L capital, M O&M, N fuel, O system, P carbon, R total, $/kWh): coal 0.04857,
  0.01580, 0.05710, 0.01694, 0, 0.13841; gas 0.04669, 0.01408, 0.01978, 0.01415, 0, 0.09471; oil 0.12870, 0.02521,
  0.02797, 0.04600, 0, 0.22789; nuclear 0.05513, 0.02233, 0.004, 0.01353, 0, 0.09499; wind 0.04088, 0.01131, 0,
  0.02737, 0, 0.07955; solar 0.03524, 0.00417, 0, 0.02991, 0, 0.06931; hydro 0.07195, 0.01067, 0, 0.03089, 0, 0.11351;
  other ren 0.06805, 0.01520, 0, 0.02433, 0, 0.10758; biomass 0.03970, 0.01965, 0.20619, 0.00819, 0, 0.27373.
  Scenario 2: carbon column coal 0.00141 (total 0.13982), gas 0.00059 (0.09530), oil 0.00120 (fuel 0.02738, total
  0.22849); others as scenario 1 but system wind 0.02743, solar 0.02998, other ren 0.02440. Checksums 0. Carbon-tax
  memo T: 0 (bug L222; intended 1.4286).
- R10: road biofuels and renewables 0 in Egypt (all ener.*.ren = 0). Range anxiety stored (Transport3 row 3):
  passenger 78,639.34, freight 440,798.51, 2-3 wheelers 1,107.65 $/vehicle. Legacy's own 2025 fit with these values:
  passenger calculated 0.2134 % vs actual 0.1458 %; freight 0.0176 % vs 0.0100 %; 2-3 wheelers 2.726 % vs 3.000 %
  (Mitigation 18967-18972 O). Prototype (I61): passenger 0.09 % vs 0.15 %.

## Appendix: R1-R2 extracted values

##### T1. Air-pollution cost per unit of fuel, typed (`airpol.cost`), 2022-2040 from the AP sheet, 2041 = 2040

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| airpol.cost.coa.ind | AP 3924 ($/GJ) | 2.37614 | 1.92141 | 1.80008 | 1.64437 | 1.8678 | 1.91151 | 2.06488 | 2.20724 | 2.33711 | 2.37559 | 2.46342 | 2.55275 | 2.64456 | 2.73854 | 2.83477 | 2.93324 | 3.03382 | 3.13645 | 3.24135 | 3.24135 |
| airpol.cost.coa.res | AP 4351 ($/GJ; switch in the prototype) | 45.7535 | 37.1775 | 35.0004 | 32.1301 | 36.6762 | 37.7209 | 40.9509 | 43.9937 | 46.8173 | 47.8293 | 49.8501 | 51.9224 | 54.0666 | 56.2776 | 58.5581 | 60.9089 | 63.3285 | 65.8167 | 68.3698 | 68.3698 |
| airpol.cost.coa.pow | AP 3731 ($/GJ) | 0.748238 | 0.605947 | 0.568541 | 0.520151 | 0.591734 | 0.606517 | 0.656203 | 0.702545 | 0.745064 | 0.758543 | 0.787854 | 0.817753 | 0.848554 | 0.880164 | 0.912614 | 0.945906 | 0.980003 | 1.01489 | 1.05051 | 1.05051 |
| airpol.cost.nga.ind | AP 3998 ($/GJ) | 0.293984 | 0.238879 | 0.224891 | 0.206448 | 0.235658 | 0.24237 | 0.263124 | 0.282675 | 0.300817 | 0.307319 | 0.320303 | 0.333618 | 0.347395 | 0.361601 | 0.376253 | 0.391358 | 0.406904 | 0.422891 | 0.436798 | 0.436798 |
| airpol.cost.nga.pow | AP 3732 ($/GJ) | 0.559905 | 0.454017 | 0.426546 | 0.390754 | 0.445115 | 0.45684 | 0.494924 | 0.530586 | 0.563457 | 0.574428 | 0.597438 | 0.620961 | 0.645238 | 0.670202 | 0.69588 | 0.722277 | 0.749368 | 0.777148 | 0.799931 | 0.799931 |
| airpol.cost.gso.all | AP 3886 ($/l) | 0.060784 | 0.0488894 | 0.0455492 | 0.0413756 | 0.0467298 | 0.0475465 | 0.0510594 | 0.0542534 | 0.057097 | 0.057679 | 0.0594362 | 0.061199 | 0.062989 | 0.0647974 | 0.0666247 | 0.0684687 | 0.0703251 | 0.0721907 | 0.0747137 | 0.0747137 |
| airpol.cost.die.all | AP 3887 ($/l) | 0.217734 | 0.176876 | 0.166476 | 0.152784 | 0.174356 | 0.179276 | 0.194577 | 0.20898 | 0.222335 | 0.227082 | 0.236615 | 0.246387 | 0.256496 | 0.266915 | 0.277659 | 0.288731 | 0.300123 | 0.311834 | 0.325903 | 0.325903 |
| airpol.cost.lpg.all | AP 4314 ($/l; all years, L190 fixed) | 0.674992 | 0.548272 | 0.515978 | 0.473491 | 0.540289 | 0.555476 | 0.60282 | 0.647376 | 0.688673 | 0.703303 | 0.73275 | 0.762932 | 0.794148 | 0.826321 | 0.859491 | 0.893668 | 0.928829 | 0.964969 | 1.00203 | 1.00203 |
| airpol.cost.ker.all | AP 4313 ($/l) | 0.936977 | 0.759087 | 0.712505 | 0.652118 | 0.742155 | 0.760999 | 0.823669 | 0.882192 | 0.935962 | 0.953283 | 0.990526 | 1.02854 | 1.06773 | 1.10796 | 1.1493 | 1.19173 | 1.23521 | 1.27974 | 1.32522 | 1.32522 |
| airpol.cost.oop.pow | AP 3733 ($/GJ) | 5.85636 | 4.7286 | 4.4234 | 4.03467 | 4.5759 | 4.67575 | 5.04302 | 5.38217 | 5.68976 | 5.77409 | 5.97775 | 6.18428 | 6.39596 | 6.61202 | 6.83262 | 7.05768 | 7.28685 | 7.51995 | 7.75756 | 7.75756 |
| airpol.cost.oop.ind | AP 3961 ($/GJ) | 23.4271 | 18.9284 | 17.7188 | 16.1728 | 18.3551 | 18.7689 | 20.2576 | 21.6356 | 22.8889 | 23.2454 | 24.0834 | 24.9344 | 25.8078 | 26.7005 | 27.6131 | 28.5455 | 29.4964 | 30.465 | 31.4539 | 31.4539 |
| airpol.cost.nga.res | AP 4378 x 741 x time_factor x (1+1713) / 41868 ($/GJ; L189 fixed) | 0.0371033 | 0.0301487 | 0.0283832 | 0.0260555 | 0.0297422 | 0.0305894 | 0.0332087 | 0.0356762 | 0.0379659 | 0.0387866 | 0.0404254 | 0.0421059 | 0.0438447 | 0.0456377 | 0.047487 | 0.0493934 | 0.0513556 | 0.0533734 | 0.0554437 | 0.0554437 |

Legacy Mitigation rows 17738-17749 as cached (with bugs B2-B4), for comparison:

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17738 | Coal ind | 2.37614 | 1.92141 | 1.80008 | 1.64437 | 1.8678 | 1.91151 | 2.06488 | 2.20724 | 2.33711 | 2.37559 | 2.46342 | 2.55275 | 2.64456 | 2.73854 | 2.83477 | 2.93324 | 2.93324 | 2.93324 | 2.93324 | 2.93324 |
| 17739 | Coal res | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 17740 | Coal pow | 0.748238 | 0.605947 | 0.568541 | 0.520151 | 0.591734 | 0.606517 | 0.656203 | 0.702545 | 0.745064 | 0.758543 | 0.787854 | 0.817753 | 0.848554 | 0.880164 | 0.912614 | 0.945906 | 0.945906 | 0.945906 | 0.945906 | 0.945906 |
| 17741 | Natural gas ind | 0.293984 | 0.238879 | 0.224891 | 0.206448 | 0.235658 | 0.24237 | 0.263124 | 0.282675 | 0.300817 | 0.307319 | 0.320303 | 0.333618 | 0.347395 | 0.361601 | 0.376253 | 0.391358 | 0.391358 | 0.391358 | 0.391358 | 0.391358 |
| 17742 | Natural gas res | 0.00147795 | 0.00150796 | 0.00153134 | 0.00153261 | 0.001558 | 0.00156077 | 0.00157338 | 0.00158621 | 0.00159955 | 0.00161971 | 0.00164002 | 0.00165983 | 0.00167982 | 0.00169978 | 0.00171978 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 | 0.00173982 |
| 17743 | Natural gas pow | 0.559905 | 0.454017 | 0.426546 | 0.390754 | 0.445115 | 0.45684 | 0.494924 | 0.530586 | 0.563457 | 0.574428 | 0.597438 | 0.620961 | 0.645238 | 0.670202 | 0.69588 | 0.722277 | 0.722277 | 0.722277 | 0.722277 | 0.722277 |
| 17744 | Gasoline  | 0.060784 | 0.0488894 | 0.0455492 | 0.0413756 | 0.0467298 | 0.0475465 | 0.0510594 | 0.0542534 | 0.057097 | 0.057679 | 0.0594362 | 0.061199 | 0.062989 | 0.0647974 | 0.0666247 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 | 0.0684687 |
| 17745 | Diesel  | 0.217734 | 0.176876 | 0.166476 | 0.152784 | 0.174356 | 0.179276 | 0.194577 | 0.20898 | 0.222335 | 0.227082 | 0.236615 | 0.246387 | 0.256496 | 0.266915 | 0.277659 | 0.288731 | 0.288731 | 0.288731 | 0.288731 | 0.288731 |
| 17746 | LPG  | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 | 0.674992 |
| 17747 | Kerosene  | 0.936977 | 0.759087 | 0.712505 | 0.652118 | 0.742155 | 0.760999 | 0.823669 | 0.882192 | 0.935962 | 0.953283 | 0.990526 | 1.02854 | 1.06773 | 1.10796 | 1.1493 | 1.19173 | 1.19173 | 1.19173 | 1.19173 | 1.19173 |
| 17748 | Other oil products pow | 5.85636 | 4.7286 | 4.4234 | 4.03467 | 4.5759 | 4.67575 | 5.04302 | 5.38217 | 5.68976 | 5.77409 | 5.97775 | 6.18428 | 6.39596 | 6.61202 | 6.83262 | 7.05768 | 7.05768 | 7.05768 | 7.05768 | 7.05768 |
| 17749 | Other oil products ind | 23.4271 | 18.9284 | 17.7188 | 16.1728 | 18.3551 | 18.7689 | 20.2576 | 21.6356 | 22.8889 | 23.2454 | 24.0834 | 24.9344 | 25.8078 | 26.7005 | 27.6131 | 28.5455 | 28.5455 | 28.5455 | 28.5455 | 28.5455 |
| 17750 | Coal - other other | 0.747496 | 0.605304 | 0.567961 | 0.519632 | 0.591143 | 0.605916 | 0.655559 | 0.701863 | 0.744346 | 0.757818 | 0.787107 | 0.816984 | 0.847762 | 0.879348 | 0.911774 | 0.945041 | 0.945041 | 0.945041 | 0.945041 | 0.945041 |
| 17751 | Natural gas - other other | 0.350146 | 0.279196 | 0.257287 | 0.235242 | 0.269447 | 0.278533 | 0.304331 | 0.328868 | 0.352306 | 0.361825 | 0.379236 | 0.395818 | 0.413429 | 0.431409 | 0.450013 | 0.46919 | 0.46919 | 0.46919 | 0.46919 | 0.46919 |
| 17752 | Other oil products and diesel - other other | 8.51612 | 6.82618 | 6.54943 | 6.40843 | 6.93924 | 7.30771 | 7.8316 | 8.30344 | 8.71725 | 8.95584 | 9.38619 | 9.82988 | 10.2884 | 10.7641 | 11.2561 | 11.765 | 11.765 | 11.765 | 11.765 | 11.765 |
| 17753 | Other oil products - average avg | 12.1706 | 9.72423 | 9.77033 | 9.27196 | 9.62708 | 9.89204 | 10.3229 | 10.6834 | 10.969 | 11.3591 | 12.0007 | 12.6683 | 13.3586 | 14.0817 | 14.8337 | 15.6158 | 15.9012 | 16.187 | 16.4739 | 16.7616 |

##### T2. Effective PM2.5 concentration coefficients `air.conc.coef` κ[m,p] (µg/m3 per t; AP F442:F522 x I974:I980, Manual-FASST as cached)

| Sector m | factor I | so2 | nox | pm2 | bc | pom | opm | voc |
|---|---|---|---|---|---|---|---|---|
| cpp | 1 | 2.051e-06 | 2e-07 | 0 | 5.5052e-05 | 5.4276e-05 | 5.5052e-05 | 0 |
| gpp | 57.804 | 0.000118556 | 1.15608e-05 | 0 | 0.00318223 | 0.00313737 | 0.00318223 | 0 |
| opp | 7.00187 | 1.43608e-05 | 1.40037e-06 | 0 | 0.000385467 | 0.000380033 | 0.000385467 | 0 |
| rod | 2.30598 | 4.72957e-06 | 4.61196e-07 | 0 | 0.000126949 | 0.000125159 | 0.000126949 | 0 |
| gro | 4.56734 | 9.36762e-06 | 9.13468e-07 | 0 | 0.000251441 | 0.000247897 | 0.000251441 | 0 |
| oth | 25.6111 | 5.25284e-05 | 5.12222e-06 | 0 | 0.00140994 | 0.00139007 | 0.00140994 | 0 |
| foo | 332.73 | 0.000682429 | 6.6546e-05 | 0 | 0.0183175 | 0.0180593 | 0.0183175 | 0 |

##### T3. Value of averted modelled ambient PM2.5 `air.vpm` (USD bn per µg/m3) = AP 3217 / (AP 981 - AP 1814); 2022 = 0; 2041 = 2040

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| air.vpm | typed | 0 | 0.290688 | 0.276304 | 0.196348 | 0.223911 | 0.23237 | 0.253805 | 0.274121 | 0.293071 | 0.299288 | 0.311904 | 0.324926 | 0.338351 | 0.352188 | 0.366428 | 0.381091 | 0.396147 | 0.411588 | 0.427404 | 0.427404 |
| (AP 981) | modelled PM2.5, scen 1 | 30.1723 | 28.5791 | 33.0267 | 36.5062 | 36.2478 | 38.5792 | 39.8333 | 41.0833 | 42.2873 | 42.655 | 43.0203 | 43.4602 | 43.8985 | 44.3493 | 44.8072 | 45.273 | 45.7457 | 46.225 | 46.7105 | 46.7105 |
| (AP 1814) | modelled PM2.5, scen 2 | 30.1723 | 28.5789 | 33.0265 | 36.5061 | 36.2477 | 38.5375 | 39.7429 | 40.9421 | 42.0933 | 42.4071 | 42.7183 | 43.1017 | 43.4825 | 43.8757 | 44.2765 | 44.6862 | 45.1045 | 45.5311 | 45.9659 | 45.9659 |
| (AP 3217) | wel.air legacy AP | 0 | 4.65067e-05 | 4.2525e-05 | 2.90915e-05 | 3.29443e-05 | 0.00970037 | 0.0229379 | 0.0387092 | 0.0568571 | 0.0741913 | 0.0942123 | 0.116503 | 0.140749 | 0.166789 | 0.194464 | 0.2236 | 0.254001 | 0.285577 | 0.318264 | 0.318264 |

##### T4. Transport external cost per vehicle-km, typed

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tran.acc.km | Transport 185 (USD/km) | 0.00632954 | 0.0049802 | 0.00460373 | 0.00419517 | 0.00473596 | 0.00485939 | 0.00524274 | 0.00559414 | 0.00590918 | 0.005954 | 0.0061273 | 0.00630436 | 0.00648515 | 0.00666962 | 0.00685774 | 0.00704945 | 0.00724651 | 0.00744909 | 0.00765733 | 0.00787139 |
| tran.con.km | Transport 220 (USD/km) | 0.00536868 | 0.00548468 | 0.00546949 | 0.00583626 | 0.00621345 | 0.00666956 | 0.00722952 | 0.00780289 | 0.00837663 | 0.00898573 | 0.00963183 | 0.0103166 | 0.0110416 | 0.0118087 | 0.0126195 | 0.0134757 | 0.0143841 | 0.0153472 | 0.0163671 | 0.0174454 |
| tran.rdm.km | Transport 232 (USD/freight km) | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

##### R. Legacy cached values for regression (scenario 2 = policy of the cached run)

| Code | Source | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2038 | 2039 | 2040 | 2041 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vkt.1 (T168) | Transport | 215.761 | 214.476 | 208.154 | 199.105 | 205.133 | 226.134 | 249.018 | 274.304 | 305.35 | 343.448 | 387 | 437.052 | 494.516 | 560.766 | 636.752 | 724.789 | 827.237 | 947.011 | 1086.79 | 1242.09 |
| vktf.1 (T169) | Transport | 11.7285 | 11.7281 | 11.3698 | 10.8613 | 11.9501 | 13.175 | 14.529 | 16.0265 | 17.8425 | 20.0473 | 22.5478 | 25.4043 | 28.5903 | 32.1684 | 36.188 | 40.7124 | 45.8085 | 51.5652 | 58.0877 | 65.4194 |
| vkt.2 (T248) | Transport | 215.761 | 214.476 | 208.154 | 199.105 | 205.133 | 225.856 | 248.417 | 273.334 | 303.944 | 341.522 | 384.466 | 433.809 | 490.449 | 555.747 | 630.638 | 717.411 | 818.397 | 936.465 | 1074.24 | 1227.22 |
| vktf.2 (T135) | Transport | 11.7285 | 11.7281 | 11.3698 | 10.8613 | 11.9501 | 13.1601 | 14.4967 | 15.9742 | 17.7663 | 19.9425 | 22.4098 | 25.2279 | 28.3692 | 31.8952 | 35.855 | 40.311 | 45.3292 | 50.9973 | 57.4194 | 64.6376 |
| tr.acc.gso.1 | Transport 322 | 0.0423861 | 0.0343589 | 0.0314842 | 0.0284638 | 0.0322049 | 0.0331571 | 0.0358265 | 0.0382694 | 0.0404957 | 0.0409011 | 0.0422092 | 0.0435663 | 0.0449834 | 0.0464629 | 0.0480066 | 0.0496133 | 0.0512967 | 0.0530592 | 0.0549027 | 0.0568334 |
| tr.acc.gso.2 | Transport 323 | 0.0423861 | 0.0343589 | 0.0314842 | 0.0284638 | 0.0322049 | 0.033157 | 0.0358291 | 0.0382781 | 0.0405138 | 0.0409309 | 0.0422544 | 0.04363 | 0.045069 | 0.0465738 | 0.0481465 | 0.0497858 | 0.0515057 | 0.0533086 | 0.0551969 | 0.0571767 |
| tr.acc.die.1 | Transport 324 | 0.013174 | 0.00968533 | 0.00870486 | 0.00792335 | 0.00867499 | 0.00894511 | 0.0097038 | 0.0104114 | 0.0110568 | 0.0111981 | 0.0115804 | 0.0119725 | 0.012382 | 0.0128028 | 0.0132336 | 0.0136781 | 0.014139 | 0.0146144 | 0.0151031 | 0.0155943 |
| tr.acc.die.2 | Transport 325 | 0.013174 | 0.00968533 | 0.00870486 | 0.00792335 | 0.00867499 | 0.00895126 | 0.00971831 | 0.0104365 | 0.0110947 | 0.0112488 | 0.0116465 | 0.0120561 | 0.0124854 | 0.0129285 | 0.013384 | 0.0138556 | 0.0143461 | 0.0148538 | 0.0153771 | 0.0159055 |
| tr.con.gso.1 | Transport 333 | 0.0359517 | 0.0378394 | 0.037405 | 0.0395984 | 0.0422519 | 0.0455084 | 0.0494033 | 0.0533794 | 0.0574052 | 0.0617276 | 0.0663509 | 0.0712926 | 0.0765889 | 0.0822635 | 0.0883408 | 0.0948407 | 0.101822 | 0.109317 | 0.117351 | 0.12596 |
| tr.con.gso.2 | Transport 334 | 0.0359517 | 0.0378394 | 0.037405 | 0.0395984 | 0.0422519 | 0.0455083 | 0.049407 | 0.0533915 | 0.0574308 | 0.0617726 | 0.0664219 | 0.0713969 | 0.0767347 | 0.08246 | 0.0885983 | 0.0951705 | 0.102237 | 0.109831 | 0.11798 | 0.126721 |
| tr.con.die.1 | Transport 335 | 0.0111741 | 0.0106664 | 0.0103419 | 0.0110228 | 0.0113813 | 0.0122772 | 0.0133812 | 0.0145222 | 0.0156738 | 0.0169001 | 0.0182038 | 0.0195919 | 0.0210816 | 0.0226677 | 0.0243522 | 0.026147 | 0.0280653 | 0.0301097 | 0.0322818 | 0.0345617 |
| tr.con.die.2 | Transport 336 | 0.0111741 | 0.0106664 | 0.0103419 | 0.0110228 | 0.0113813 | 0.0122857 | 0.0134012 | 0.0145572 | 0.0157274 | 0.0169765 | 0.0183077 | 0.0197287 | 0.0212577 | 0.0228903 | 0.0246289 | 0.0264864 | 0.0284765 | 0.0306029 | 0.0328677 | 0.0352513 |
| tr.rdm.die.1 | Transport 344 | 0.148468 | 0.140497 | 0.135773 | 0.134828 | 0.134486 | 0.135095 | 0.135797 | 0.136534 | 0.137298 | 0.138101 | 0.13894 | 0.139816 | 0.140735 | 0.141686 | 0.142667 | 0.143679 | 0.14472 | 0.145785 | 0.146872 | 0.147965 |
| tr.rdm.die.2 | Transport 345 | 0.148468 | 0.140497 | 0.135773 | 0.134828 | 0.134486 | 0.135207 | 0.13604 | 0.136923 | 0.137848 | 0.138827 | 0.139856 | 0.140934 | 0.142069 | 0.14325 | 0.144472 | 0.145738 | 0.147045 | 0.148387 | 0.149761 | 0.151151 |
| tr.acc.nga.1 | Transport 328 | 0.00044399 | 0.000404711 | 0.000427699 | 0.000363455 | 0.000410962 | 0.000428061 | 0.000470294 | 0.000509764 | 0.000550987 | 0.000563235 | 0.000589415 | 0.000603155 | 0.000621394 | 0.000638269 | 0.000655916 | 0.000673855 | 0.000692366 | 0.000711403 | 0.000730784 | 0.000750495 |
| tr.con.nga.1 | Transport 339 | 0.00037659 | 0.000445706 | 0.00050813 | 0.000505632 | 0.000539171 | 0.000587518 | 0.000648516 | 0.000711035 | 0.000781058 | 0.000850031 | 0.000926534 | 0.000987013 | 0.00105799 | 0.00113007 | 0.001207 | 0.00128814 | 0.00137432 | 0.00146569 | 0.00156201 | 0.00166332 |
| tr.acc.ecy.1 | Transport 330 | 1.0903e-06 | 1.79107e-06 | 2.1613e-06 | 2.32467e-06 | 3.97749e-06 | 6.74205e-06 | 1.22396e-05 | 2.2243e-05 | 4.159e-05 | 7.33803e-05 | 0.000127568 | 0.000209219 | 0.000328454 | 0.000495612 | 0.00071808 | 0.00100824 | 0.00138227 | 0.0018595 | 0.00245562 | 0.00313834 |
| tr.con.ecy.1 | Transport 341 | 9.24782e-07 | 1.9725e-06 | 2.56774e-06 | 3.23404e-06 | 5.21836e-06 | 9.25352e-06 | 1.68779e-05 | 3.10253e-05 | 5.89564e-05 | 0.000110745 | 0.000200531 | 0.00034237 | 0.000559228 | 0.000877491 | 0.0013214 | 0.00192735 | 0.00274376 | 0.00383109 | 0.00524874 | 0.00695551 |
| tr.rdm.ecy.1 | Transport 350 | 7.47238e-06 | 8.18192e-06 | 7.72461e-06 | 6.81302e-06 | 7.58318e-06 | 1.01835e-05 | 1.67135e-05 | 3.16625e-05 | 6.72231e-05 | 0.000146015 | 0.000310651 | 0.00062544 | 0.00108378 | 0.00170612 | 0.00251848 | 0.0035422 | 0.00480177 | 0.0063259 | 0.0081423 | 0.0101874 |
| M17714 | Avoided climate damages (global)  | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17715 | Total global welfare benefits  | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17716 | Averted climate damages (national) egy.mit.wel.cli.usd | -1.09609e-07 | 0.000328474 | 0.000328756 | 0.000329183 | 0.000341384 | 0.0456541 | 0.112477 | 0.188062 | 0.273092 | 0.360594 | 0.455945 | 0.565478 | 0.685092 | 0.814973 | 0.955208 | 1.10534 | 1.2652 | 1.43496 | 1.61502 | 1.80474 |
| M17717 | Averted air pollution mortality/morbidit egy.mit.wel.air.usd | 0 | 4.65067e-05 | 4.2525e-05 | 2.90915e-05 | 3.29443e-05 | 0.00970037 | 0.0229379 | 0.0387092 | 0.0568571 | 0.0741913 | 0.0942123 | 0.116503 | 0.140749 | 0.166789 | 0.194464 | 0.2236 | 0.254001 | 0.285577 | 0.285577 | 0.285577 |
| M17718 | Averted road accidents egy.mit.wel.rod.aci.usd | 0 | 0 | 0 | 0 | 1.51897e-09 | 0.00135188 | 0.00314791 | 0.00542962 | 0.00830923 | 0.0114704 | 0.0155271 | 0.020444 | 0.0263758 | 0.033477 | 0.0419311 | 0.0520088 | 0.0640633 | 0.0785583 | 0.0961178 | 0.117066 |
| M17719 | Reduced congestion egy.mit.wel.rod.con.usd | 0 | 0 | 0 | 0 | 1.99284e-09 | 0.00185546 | 0.00434084 | 0.00757341 | 0.0117789 | 0.0173111 | 0.0244079 | 0.0334549 | 0.0449075 | 0.0592718 | 0.0771609 | 0.09942 | 0.127163 | 0.161852 | 0.205446 | 0.259453 |
| M17720 | Reduced road damage egy.mit.wel.rod.dmg.usd | 0 | 0 | 0 | 0 | 1.98327e-10 | 0.00178905 | 0.00387103 | 0.00628408 | 0.0091453 | 0.0125725 | 0.016561 | 0.0211591 | 0.0265396 | 0.0327786 | 0.0399554 | 0.0481704 | 0.0575246 | 0.0681429 | 0.0801981 | 0.0938132 |
| M17721 | Efficiency costs egy.mit.wel.eco.dwl.usd | 0 | 0.000702906 | 0.000622611 | 0.000605192 | 0.00064773 | 0.0578384 | 0.164548 | 0.273614 | 0.386069 | 0.488786 | 0.589355 | 0.703693 | 0.820088 | 0.937329 | 1.0547 | 1.17048 | 1.2835 | 1.39323 | 1.4995 | 1.60134 |
| M17722 | Total national welfare benefits egy.mit.wel.tot.tot | -1.09609e-07 | 0.00107789 | 0.000993892 | 0.000963466 | 0.00102206 | 0.118189 | 0.311323 | 0.519672 | 0.745251 | 0.964925 | 1.19601 | 1.46073 | 1.74375 | 2.04462 | 2.36342 | 2.69902 | 3.05146 | 3.42233 | 3.78186 | 4.16199 |
| M17723 | Climate benefits egy.mit.wel.cli.pct | -2.00394e-10 | 5.7877e-07 | 5.65696e-07 | 5.42598e-07 | 5.39823e-07 | 6.88661e-05 | 0.000160766 | 0.000255448 | 0.000353815 | 0.000445832 | 0.000538233 | 0.000637676 | 0.00073838 | 0.000839927 | 0.000941856 | 0.00104326 | 0.00114363 | 0.00124284 | 0.00134099 | 0.00143733 |
| M17724 | Air pollution co-benefits egy.mit.wel.air.pct | 0 | 8.19446e-08 | 7.31736e-08 | 4.7952e-08 | 5.20941e-08 | 1.46323e-05 | 3.27855e-05 | 5.25795e-05 | 7.36634e-05 | 9.17287e-05 | 0.000111216 | 0.000131378 | 0.000151697 | 0.000171896 | 0.000191746 | 0.000211041 | 0.000229594 | 0.000247343 | 0.000237122 | 0.000227439 |
| M17725 | Transport co-benefits egy.mit.wel.rod.pct | 0 | 0 | 0 | 0 | 5.86675e-12 | 7.53671e-06 | 1.62367e-05 | 2.61981e-05 | 3.78745e-05 | 5.11294e-05 | 6.66923e-05 | 8.46411e-05 | 0.000105432 | 0.000129371 | 0.000156824 | 0.000188388 | 0.000224849 | 0.000267243 | 0.000316986 | 0.000374582 |
| M17726 | Efficiency costs egy.mit.wel.eco.dwl.pct | 0 | 1.23852e-06 | 1.07134e-06 | 9.97549e-07 | 1.02424e-06 | 8.72453e-05 | 0.00023519 | 0.000371655 | 0.000500186 | 0.000604326 | 0.000695722 | 0.000793538 | 0.000883876 | 0.000966029 | 0.00103995 | 0.00110474 | 0.00116017 | 0.0012067 | 0.00124507 | 0.00127534 |
| M17727 | Total national welfare benefits egy.mit.wel.tot.pct | -2.00394e-10 | 1.89923e-06 | 1.71021e-06 | 1.5881e-06 | 1.61616e-06 | 0.00017828 | 0.000444978 | 0.00070588 | 0.000965539 | 0.00119302 | 0.00141186 | 0.00164723 | 0.00187939 | 0.00210722 | 0.00233038 | 0.00254743 | 0.00275824 | 0.00296413 | 0.00314017 | 0.00331468 |
| M17763 | Total externalities - gasoline  | 0.139122 | 0.121088 | 0.114438 | 0.109438 | 0.121187 | 0.126212 | 0.136289 | 0.145902 | 0.154998 | 0.160308 | 0.167996 | 0.176058 | 0.184561 | 0.193524 | 0.202972 | 0.212923 | 0.221588 | 0.230845 | 0.240723 | 0.251262 |
| M17764 | Total externalities - diesel  | 0.39055 | 0.337726 | 0.321295 | 0.306558 | 0.328899 | 0.335593 | 0.353458 | 0.370448 | 0.386363 | 0.393281 | 0.40534 | 0.417768 | 0.430694 | 0.444072 | 0.457912 | 0.472235 | 0.475655 | 0.47924 | 0.482987 | 0.486852 |
| M17783 | Environmental benefits - Harberger trian egy.mit.env.ffs.cost.all.all.2 | -1.91944e-15 | 0.000398538 | 0.000396587 | 0.000394472 | 0.000411228 | 0.132697 | 0.298078 | 0.482806 | 0.686657 | 0.898863 | 1.12956 | 1.38398 | 1.6588 | 1.95308 | 2.26647 | 2.59807 | 2.92329 | 3.26135 | 3.61256 | 3.97617 |
| M17784 | Total national welfare benefits (FFS) egy.mit.wel.ffs.all.all.2 | -1.91944e-15 | 0.00110144 | 0.0010192 | 0.000999664 | 0.00105896 | 0.190535 | 0.462626 | 0.75642 | 1.07273 | 1.38765 | 1.71891 | 2.08767 | 2.47888 | 2.89041 | 3.32117 | 3.76855 | 4.2068 | 4.65458 | 5.11206 | 5.57752 |
| M17678 | Coal 0.09620266666666666 | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| M17679 | Natural gas 0.055799999999999995 | 3.05794 | 3.18026 | 3.30747 | 3.43976 | 3.57736 | 3.72045 | 3.86927 | 4.02404 | 4.185 | 4.3524 | 4.5265 | 4.70756 | 4.89586 | 5.09169 | 5.29536 | 5.50717 | 5.72746 | 5.95656 | 6.19482 | 6.44262 |
| M17680 | Non-road oil 0.41246307181497194 | 22.6037 | 23.5079 | 24.4482 | 25.4261 | 26.4431 | 27.5009 | 28.6009 | 29.7449 | 30.9347 | 32.1721 | 33.459 | 34.7974 | 36.1893 | 37.6368 | 39.1423 | 40.708 | 42.3363 | 44.0298 | 45.791 | 47.6226 |
| M17681 | Gasoline 0.0023557889897100003 | 0.129101 | 0.134265 | 0.139636 | 0.145222 | 0.15103 | 0.157072 | 0.163354 | 0.169889 | 0.176684 | 0.183752 | 0.191102 | 0.198746 | 0.206695 | 0.214963 | 0.223562 | 0.232504 | 0.241804 | 0.251477 | 0.261536 | 0.271997 |
| M17682 | Diesel 0.0026891510273550005 | 0.14737 | 0.153265 | 0.159396 | 0.165771 | 0.172402 | 0.179298 | 0.18647 | 0.193929 | 0.201686 | 0.209754 | 0.218144 | 0.22687 | 0.235944 | 0.245382 | 0.255198 | 0.265405 | 0.276022 | 0.287063 | 0.298545 | 0.310487 |
| M17683 | LPG 0.0017684866341836556 | 0.0969162 | 0.100793 | 0.104825 | 0.109018 | 0.113378 | 0.117913 | 0.12263 | 0.127535 | 0.132636 | 0.137942 | 0.14346 | 0.149198 | 0.155166 | 0.161373 | 0.167827 | 0.174541 | 0.181522 | 0.188783 | 0.196334 | 0.204188 |
| M17684 | Kerosene 0.0025734887129072754 | 0.141032 | 0.146673 | 0.15254 | 0.158642 | 0.164987 | 0.171587 | 0.17845 | 0.185588 | 0.193012 | 0.200732 | 0.208761 | 0.217112 | 0.225796 | 0.234828 | 0.244221 | 0.25399 | 0.26415 | 0.274716 | 0.285704 | 0.297133 |
| M17685 | Memo: LPG & kerosene 0.0021709876735454656 | 0.118974 | 0.123733 | 0.128682 | 0.13383 | 0.139183 | 0.14475 | 0.15054 | 0.156562 | 0.162824 | 0.169337 | 0.176111 | 0.183155 | 0.190481 | 0.1981 | 0.206024 | 0.214265 | 0.222836 | 0.231749 | 0.241019 | 0.25066 |
| M17702 | Coal egy.mit.cc.code.coa.1 | 5.27208 | 5.48296 | 5.70228 | 5.93037 | 6.16758 | 6.41429 | 6.67086 | 6.93769 | 7.2152 | 7.50381 | 7.80396 | 8.11612 | 8.44076 | 8.77839 | 9.12953 | 9.49471 | 9.8745 | 10.2695 | 10.6803 | 11.1075 |
| M17703 | Natural gas egy.mit.cc.code.nga.1 | 3.05794 | 3.18026 | 3.30747 | 3.43976 | 3.57736 | 3.72045 | 3.86927 | 4.02404 | 4.185 | 4.3524 | 4.5265 | 4.70756 | 4.89586 | 5.09169 | 5.29536 | 5.50717 | 5.72746 | 5.95656 | 6.19482 | 6.44262 |
| M17704 | Non-road oil egy.mit.cc.code.oop.1 | 22.6037 | 23.5079 | 24.4482 | 25.4261 | 26.4431 | 27.5009 | 28.6009 | 29.7449 | 30.9347 | 32.1721 | 33.459 | 34.7974 | 36.1893 | 37.6368 | 39.1423 | 40.708 | 42.3363 | 44.0298 | 45.791 | 47.6226 |
| M17705 | Gasoline egy.mit.cc.code.gso.1 | 0.129101 | 0.134265 | 0.139636 | 0.145222 | 0.15103 | 0.157072 | 0.163354 | 0.169889 | 0.176684 | 0.183752 | 0.191102 | 0.198746 | 0.206695 | 0.214963 | 0.223562 | 0.232504 | 0.241804 | 0.251477 | 0.261536 | 0.271997 |
| M17706 | Diesel egy.mit.cc.code.die.1 | 0.14737 | 0.153265 | 0.159396 | 0.165771 | 0.172402 | 0.179298 | 0.18647 | 0.193929 | 0.201686 | 0.209754 | 0.218144 | 0.22687 | 0.235944 | 0.245382 | 0.255198 | 0.265405 | 0.276022 | 0.287063 | 0.298545 | 0.310487 |
| M17707 | LPG egy.mit.cc.code.lpg.1 | 0.0969162 | 0.100793 | 0.104825 | 0.109018 | 0.113378 | 0.117913 | 0.12263 | 0.127535 | 0.132636 | 0.137942 | 0.14346 | 0.149198 | 0.155166 | 0.161373 | 0.167827 | 0.174541 | 0.181522 | 0.188783 | 0.196334 | 0.204188 |
| M17708 | Kerosene egy.mit.cc.code.ker.1 | 0.141032 | 0.146673 | 0.15254 | 0.158642 | 0.164987 | 0.171587 | 0.17845 | 0.185588 | 0.193012 | 0.200732 | 0.208761 | 0.217112 | 0.225796 | 0.234828 | 0.244221 | 0.25399 | 0.26415 | 0.274716 | 0.285704 | 0.297133 |
| M17709 | Memo: LPG & kerosene  | 0.118974 | 0.123733 | 0.128682 | 0.13383 | 0.139183 | 0.14475 | 0.15054 | 0.156562 | 0.162824 | 0.169337 | 0.176111 | 0.183155 | 0.190481 | 0.1981 | 0.206024 | 0.214265 | 0.222836 | 0.231749 | 0.241019 | 0.25066 |
| M17948 | Total - explicit subsidy egy.mit.expsub.con.all.all.1 | 38.6524 | 33.8739 | 48.5984 | 47.3255 | 53.0274 | 50.2822 | 50.0807 | 50.896 | 51.704 | 51.993 | 52.9246 | 54.4568 | 55.9072 | 57.4377 | 58.9891 | 60.5749 | 62.1915 | 63.8405 | 65.5266 | 67.2508 |
| M17949 | Total - implicit subsidy egy.mit.impsub.con.all.all.1 | 39.5492 | 38.4482 | 45.7499 | 50.1768 | 53.9035 | 58.8638 | 64.1037 | 69.6553 | 75.3597 | 78.34 | 81.7894 | 85.6999 | 89.7593 | 94.0532 | 98.5646 | 103.311 | 107.456 | 111.807 | 116.376 | 121.173 |
| M17950 | Total - explicit subsidy egy.mit.expsubgdp.con.all.all.1 | 0.0753665 | 0.0619299 | 0.0856301 | 0.0814339 | 0.087406 | 0.0795101 | 0.0755433 | 0.0727463 | 0.0702306 | 0.0673616 | 0.0654351 | 0.0642851 | 0.0630452 | 0.0619053 | 0.0607953 | 0.0597282 | 0.0586984 | 0.0577061 | 0.0567536 | 0.05584 |
| M17951 | Total - implicit subsidy egy.mit.impsubgdp.con.all.all.1 | 0.0771152 | 0.070293 | 0.080611 | 0.0863402 | 0.08885 | 0.09308 | 0.0966959 | 0.0995593 | 0.102363 | 0.101496 | 0.101123 | 0.101167 | 0.101219 | 0.101369 | 0.101583 | 0.101867 | 0.101421 | 0.101064 | 0.100795 | 0.100613 |
| M17795 | Gasoline - efficient price egy.mit.effprice.gso.all.1 | 1.40346 | 1.22331 | 1.16007 | 1.03764 | 1.1432 | 1.06711 | 1.06135 | 1.06746 | 1.07481 | 1.07724 | 1.09438 | 1.11228 | 1.13104 | 1.15068 | 1.17126 | 1.19279 | 1.21327 | 1.23485 | 1.25758 | 1.28152 |
| M17799 | Gasoline - implicit subsidy egy.mit.impsub.con.gso.all.1 | 3.90868 | 3.7092 | 4.56061 | 4.50405 | 4.97859 | 5.13654 | 5.50083 | 5.88523 | 6.26814 | 6.60646 | 7.01872 | 7.45567 | 7.91959 | 8.41199 | 8.93463 | 9.48913 | 10.0435 | 10.6327 | 11.259 | 11.9247 |
| M17798 | Gasoline - explicit subsidy egy.mit.expsub.con.gso.all.1 | 3.21727 | 3.72421 | 4.92732 | 3.77738 | 4.77202 | 3.93822 | 3.79011 | 3.75951 | 3.73151 | 3.68607 | 3.78005 | 3.87479 | 3.97028 | 4.06647 | 4.16332 | 4.26082 | 4.35891 | 4.45757 | 4.55675 | 4.65643 |
| M17807 | Diesel - efficient price egy.mit.effprice.die.all.1 | 1.6216 | 1.35177 | 1.26461 | 1.14524 | 1.25147 | 1.18514 | 1.18829 | 1.20175 | 1.21583 | 1.22035 | 1.24089 | 1.26213 | 1.28423 | 1.30715 | 1.33091 | 1.35555 | 1.36964 | 1.38433 | 1.39963 | 1.41551 |
| M17811 | Diesel - implicit subsidy egy.mit.impsub.con.die.all.1 | 9.31645 | 9.01531 | 10.6004 | 10.614 | 11.4809 | 12.0401 | 12.9415 | 13.8407 | 14.7222 | 15.407 | 16.2512 | 17.1365 | 18.0675 | 19.0449 | 20.0704 | 21.1465 | 21.9437 | 22.7736 | 23.6376 | 24.5355 |
| M17810 | Diesel - explicit subsidy egy.mit.expsub.con.die.all.1 | 11.3289 | 10.4186 | 11.5364 | 9.30951 | 11.2244 | 9.62694 | 9.35209 | 9.30335 | 9.26045 | 9.18647 | 9.37344 | 9.56101 | 9.74914 | 9.93775 | 10.1268 | 10.3162 | 10.5059 | 10.6959 | 10.886 | 11.0763 |
| M17818 | LPG - efficient price egy.mit.effprice.lpg.all.1 | 1.44263 | 1.35333 | 1.32277 | 1.25617 | 1.30973 | 1.26325 | 1.25393 | 1.25175 | 1.25067 | 1.24925 | 1.25477 | 1.26051 | 1.26648 | 1.27268 | 1.27914 | 1.28585 | 1.29283 | 1.30009 | 1.30764 | 1.3155 |
| M17822 | LPG - implicit subsidy egy.mit.impsub.con.lpg.all.1 | 6.76132 | 7.64019 | 9.25849 | 9.53787 | 9.81617 | 10.1393 | 10.5174 | 10.8883 | 11.2459 | 11.6126 | 11.9898 | 12.3777 | 12.777 | 13.1878 | 13.6108 | 14.0463 | 14.4948 | 14.9568 | 15.4329 | 15.9236 |
| M17821 | LPG - explicit subsidy egy.mit.expsub.con.lpg.all.1 | 4.34153 | 4.68789 | 5.40129 | 4.67324 | 5.39564 | 4.88897 | 4.85619 | 4.90072 | 4.94356 | 4.9754 | 5.10236 | 5.23079 | 5.36069 | 5.49201 | 5.62473 | 5.75883 | 5.89427 | 6.03103 | 6.16907 | 6.30836 |
| M17829 | Kerosene - efficient price egy.mit.effprice.ker.all.1 | 1.96285 | 1.69205 | 1.6414 | 1.4831 | 1.65498 | 1.60898 | 1.66227 | 1.72142 | 1.77712 | 1.79393 | 1.84168 | 1.89057 | 1.94105 | 1.99301 | 2.04651 | 2.10155 | 2.11227 | 2.12341 | 2.135 | 2.14705 |
| M17833 | Kerosene - implicit subsidy egy.mit.impsub.con.ker.all.1 | 0.873751 | 0.783249 | 0.857381 | 0.823746 | 0.946203 | 0.998446 | 1.10844 | 1.21797 | 1.32421 | 1.39225 | 1.48753 | 1.58777 | 1.69366 | 1.80525 | 1.9228 | 2.04653 | 2.11463 | 2.18455 | 2.25634 | 2.33006 |
| M17832 | Kerosene - explicit subsidy egy.mit.expsub.con.ker.all.1 | 0.273674 | 0.346931 | 0.403888 | 0.326421 | 0.398659 | 0.343246 | 0.336391 | 0.337589 | 0.338691 | 0.338534 | 0.348362 | 0.358306 | 0.368359 | 0.37852 | 0.388784 | 0.399148 | 0.409608 | 0.42016 | 0.4308 | 0.441524 |
| M17840 | Other oil products - efficient price egy.mit.effprice.oop.all.1 | 53.8099 | 48.7663 | 49.187 | 47.1432 | 50.2691 | 49.7733 | 50.8039 | 52.0562 | 53.311 | 54.699 | 56.6274 | 58.6333 | 60.7155 | 62.8862 | 65.1437 | 67.4915 | 69.4052 | 71.3845 | 73.4326 | 75.5519 |
| M17844 | Other oil products - implicit subsidy egy.mit.impsub.con.oop.all.1 | 11.1933 | 10.272 | 11.205 | 14.4747 | 15.8555 | 19.2434 | 22.1569 | 25.3324 | 28.7793 | 29.7052 | 30.832 | 32.0139 | 33.2904 | 34.6178 | 36.0182 | 37.4909 | 38.69 | 39.9496 | 41.269 | 42.6511 |
| M17843 | Other oil products - explicit subsidy egy.mit.expsub.con.oop.all.1 | 4.38892 | 3.47327 | 3.66144 | 4.16917 | 4.91512 | 5.10992 | 5.36737 | 5.75022 | 6.15118 | 5.94817 | 5.91192 | 5.87911 | 5.85662 | 5.83455 | 5.81667 | 5.80213 | 5.79094 | 5.78293 | 5.77741 | 5.77437 |
| M17849 | Natural gas, industry - efficient price egy.mit.effprice.nga.ind.1 | 15.6125 | 13.6107 | 13.1019 | 13.2926 | 13.6418 | 13.5743 | 13.4883 | 13.5716 | 13.7249 | 13.8842 | 14.0713 | 14.2656 | 14.4677 | 14.6777 | 14.8961 | 15.123 | 15.3433 | 15.5724 | 15.8106 | 16.0584 |
| M17853 | Natural gas, industry - implicit subsidy egy.mit.impsub.con.nga.ind.1 | 1.55451 | 1.36055 | 1.54745 | 1.66045 | 1.80162 | 1.95316 | 2.13787 | 2.33057 | 2.52884 | 2.73442 | 2.95885 | 3.19964 | 3.45794 | 3.73483 | 4.0315 | 4.34918 | 4.67731 | 5.02792 | 5.40242 | 5.80225 |
| M17852 | Natural gas, industry - explicit subsidy egy.mit.expsub.con.nga.ind.1 | 3.21129 | 2.06184 | 1.96371 | 2.07628 | 2.24044 | 2.22999 | 2.20851 | 2.26087 | 2.3407 | 2.42794 | 2.52581 | 2.62605 | 2.72866 | 2.83364 | 2.94098 | 3.05068 | 3.16272 | 3.2771 | 3.39381 | 3.51282 |
| M17859 | Natural gas, residential - efficient pri egy.mit.effprice.nga.res.1 | 22.7498 | 20.7356 | 20.1737 | 20.4074 | 20.7613 | 20.6898 | 20.5834 | 20.6616 | 20.8172 | 20.9922 | 21.1907 | 21.3971 | 21.6118 | 21.8351 | 22.0673 | 22.3088 | 22.5599 | 22.8211 | 23.0927 | 23.3752 |
| M17863 | Natural gas, residential - implicit subs egy.mit.impsub.con.nga.res.1 | 0.470812 | 0.474449 | 0.655656 | 0.678735 | 0.704019 | 0.725364 | 0.748582 | 0.774768 | 0.802255 | 0.83099 | 0.861114 | 0.892444 | 0.925031 | 0.958924 | 0.994179 | 1.03085 | 1.06899 | 1.10867 | 1.14995 | 1.19288 |
| M17862 | Natural gas, residential - explicit subs egy.mit.expsub.con.nga.res.1 | 0.986375 | 0.97724 | 1.36608 | 1.38419 | 1.41318 | 1.40096 | 1.3868 | 1.38918 | 1.39714 | 1.40608 | 1.41649 | 1.42672 | 1.43678 | 1.44665 | 1.45634 | 1.46585 | 1.47518 | 1.48432 | 1.49328 | 1.50206 |
| M17868 | Natural gas, power - efficient price egy.mit.effprice.nga.pow.1 | 15.1054 | 13.0234 | 12.5008 | 12.6833 | 13.0795 | 12.9911 | 12.8917 | 12.9802 | 13.1451 | 13.3071 | 13.5042 | 13.7088 | 13.9214 | 14.1422 | 14.3715 | 14.6097 | 14.83 | 15.0591 | 15.2974 | 15.5452 |
| M17872 | Natural gas, power - implicit subsidy egy.mit.impsub.con.nga.pow.1 | 4.45989 | 4.19791 | 5.20653 | 5.87333 | 6.21787 | 6.43908 | 6.69361 | 6.96632 | 7.15548 | 7.40417 | 7.65093 | 8.17434 | 8.64247 | 9.17624 | 9.73257 | 10.3234 | 10.902 | 11.5146 | 12.168 | 12.8656 |
| M17871 | Natural gas, power - explicit subsidy egy.mit.expsub.con.nga.pow.1 | 10.7292 | 7.82627 | 8.52293 | 9.5041 | 9.89726 | 9.49446 | 9.00811 | 8.82721 | 8.65321 | 8.60515 | 8.54988 | 8.78406 | 8.93083 | 9.11904 | 9.30166 | 9.48902 | 9.67866 | 9.87181 | 10.0727 | 10.2818 |
| M17877 | Natural gas, other - efficient price egy.mit.effprice.nga.other.1 | 15.5838 | 13.5568 | 13.083 | 13.2344 | 13.6177 | 13.5395 | 13.4491 | 13.5408 | 13.7113 | 13.8773 | 14.0771 | 14.2714 | 14.4775 | 14.6902 | 14.9116 | 15.1418 | 15.3588 | 15.5847 | 15.8196 | 16.064 |
| M17881 | Natural gas, other - implicit subsidy egy.mit.impsub.con.nga.other.1 | 0.0756736 | 0.0794192 | 0.112844 | 0.117701 | 0.125227 | 0.132291 | 0.14088 | 0.149679 | 0.158603 | 0.167329 | 0.176833 | 0.186791 | 0.197268 | 0.208274 | 0.219838 | 0.231984 | 0.243893 | 0.256389 | 0.269499 | 0.283252 |
| M17886 | Coal, industry - efficient price egy.mit.effprice.coa.ind.1 | 18.7686 | 16.0151 | 15.0793 | 14.2925 | 15.2265 | 15.6237 | 15.983 | 16.3379 | 16.6872 | 16.9582 | 17.3462 | 17.7477 | 18.1641 | 18.5957 | 19.0431 | 19.5067 | 19.8865 | 20.2815 | 20.6923 | 21.1195 |
| M17890 | Coal, industry - implicit subsidy egy.mit.impsub.con.coa.ind.1 | 0.504315 | 0.464312 | 0.56342 | 0.620434 | 0.645241 | 0.67697 | 0.730578 | 0.78544 | 0.841067 | 0.891108 | 0.944255 | 1.00008 | 1.0588 | 1.12051 | 1.18535 | 1.25345 | 1.31448 | 1.37847 | 1.44555 | 1.51589 |
| M17896 | Coal, residential - efficient price egy.mit.effprice.coa.res.1 | 29.199 | 21.9015 | 21.2434 | 20.148 | 21.1652 | 21.6149 | 21.8275 | 22.0461 | 22.2708 | 22.5113 | 22.8535 | 23.2093 | 23.5794 | 23.9643 | 24.3646 | 24.7809 | 25.2139 | 25.6642 | 26.1325 | 26.6195 |
| M17900 | Coal, residential - implicit subsidy egy.mit.impsub.con.coa.res.1 | 0.000607511 | 0.000560478 | 0.000652095 | 0.000704119 | 0.000718173 | 0.000745733 | 0.000781215 | 0.000817926 | 0.000855733 | 0.00089528 | 0.000934277 | 0.000975001 | 0.00101753 | 0.00106193 | 0.0011083 | 0.00115671 | 0.00120726 | 0.00126003 | 0.00131513 | 0.00137264 |
| M17933 | Electricity, residential - efficient pri egy.mit.effprice.ecy.res.1 | 0.0676265 | 0.0582941 | 0.114847 | 0.113334 | 0.113053 | 0.113379 | 0.113204 | 0.113332 | 0.113444 | 0.113886 | 0.112639 | 0.111645 | 0.110653 | 0.109742 | 0.108886 | 0.108084 | 0.107329 | 0.106614 | 0.105933 | 0.10527 |
| M17937 | Electricity, residential - implicit subs egy.mit.impsub.con.ecy.res.1 | 0.428632 | 0.393429 | 1.12105 | 1.21372 | 1.26389 | 1.31495 | 1.3616 | 1.41594 | 1.46355 | 1.51646 | 1.54287 | 1.59566 | 1.64607 | 1.69869 | 1.75194 | 1.80621 | 1.86135 | 1.91732 | 1.97415 | 2.0316 |
| M17942 | Electricity, other - efficient price egy.mit.effprice.ecy.other.1 | 0.0652756 | 0.974528 | 0.887347 | 0.761395 | 0.848931 | 0.758162 | 0.73319 | 0.720603 | 0.709594 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 | 0.697635 |
| M17946 | Electricity, other - implicit subsidy egy.mit.impsub.con.ecy.other.1 | 0.00131064 | 0.0576379 | 0.0604121 | 0.0574365 | 0.0675396 | 0.0634581 | 0.0647574 | 0.0671286 | 0.0692251 | 0.0712154 | 0.0742852 | 0.0783984 | 0.0825416 | 0.0868557 | 0.091289 | 0.0958556 | 0.100552 | 0.105381 | 0.110347 | 0.115452 |
| M17945 | Electricity, other - explicit subsidy egy.mit.expsub.con.ecy.other.1 | 0 | 0.213999 | 0.24574 | 0.204419 | 0.265335 | 0.22488 | 0.221546 | 0.225295 | 0.228264 | 0.230132 | 0.240052 | 0.253344 | 0.266733 | 0.280674 | 0.295 | 0.309757 | 0.324934 | 0.340539 | 0.356586 | 0.373082 |
| M17767 | Coal egy.mit.env.ffs.cost.coa.ind.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17768 | Coal egy.mit.env.ffs.cost.coa.res.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17769 | Coal egy.mit.env.ffs.cost.coa.pow.2 | 0 | 0 | 0 | 0 | 0 | 0.00161038 | 0.00346075 | 0.0055767 | 0.00797306 | 0.0106425 | 0.0134925 | 0.0166129 | 0.0200142 | 0.0237053 | 0.0276887 | 0.0319714 | 0.036446 | 0.0412173 | 0.0463012 | 0.0517133 |
| M17770 | Natural gas egy.mit.env.ffs.cost.nga.ind.2 | 0 | 0.000352379 | 0.000350738 | 0.000348738 | 0.000363835 | 0.000386344 | 0.0169197 | 0.0355313 | 0.056724 | 0.0709429 | 0.0851966 | 0.105365 | 0.126405 | 0.148383 | 0.171378 | 0.194736 | 0.217553 | 0.240037 | 0.262073 | 0.283542 |
| M17771 | Natural gas egy.mit.env.ffs.cost.nga.res.2 | 0 | 0 | 0 | 0 | 0 | 0.00258705 | 0.00544889 | 0.0086022 | 0.0120573 | 0.0158422 | 0.0199781 | 0.0244851 | 0.029385 | 0.0347004 | 0.0404529 | 0.0466673 | 0.0533701 | 0.0605921 | 0.0683662 | 0.0759277 |
| M17772 | Natural gas egy.mit.env.ffs.cost.nga.pow.2 | 0 | 0 | 0 | 0 | 0 | 0.0060286 | 0.0131521 | 0.0214851 | 0.031048 | 0.0418641 | 0.0542648 | 0.0682441 | 0.0838827 | 0.101245 | 0.120339 | 0.141199 | 0.163172 | 0.18686 | 0.212355 | 0.239745 |
| M17773 | Gasoline - road egy.mit.env.ffs.cost.gso.rd.2 | 0 | 0 | 0 | 0 | 0 | 0.00553241 | 0.0120234 | 0.0195528 | 0.0280988 | 0.0374073 | 0.0480582 | 0.0598939 | 0.0729452 | 0.0872198 | 0.102659 | 0.119235 | 0.136383 | 0.154573 | 0.173852 | 0.19426 |
| M17774 | Diesel - road egy.mit.env.ffs.cost.die.rd.2 | 0 | 0 | 0 | 0 | 0 | 0.0106631 | 0.0231629 | 0.0375675 | 0.0537804 | 0.0706863 | 0.0900538 | 0.111324 | 0.134548 | 0.159722 | 0.186769 | 0.215659 | 0.241817 | 0.268874 | 0.296863 | 0.325794 |
| M17775 | LPG egy.mit.env.ffs.cost.lpg.all.2 | 0 | 0 | 0 | 0 | 0 | 0.0439046 | 0.0905267 | 0.139897 | 0.191746 | 0.246424 | 0.303949 | 0.364238 | 0.427237 | 0.492874 | 0.560971 | 0.631439 | 0.704208 | 0.779312 | 0.856829 | 0.936825 |
| M17776 | Kerosene egy.mit.env.ffs.cost.ker.all.2 | 0 | 0 | 0 | 0 | 0 | 2.25861e-05 | 4.10669e-05 | 7.54114e-05 | 0.00012384 | 0.000193948 | 0.000281572 | 0.000358182 | 0.000397522 | 0.000365667 | 0.000205568 | -0.000132006 | -0.000679666 | -0.00145034 | -0.0024578 | -0.00371819 |
| M17777 | Other oil products and diesel  egy.mit.env.ffs.cost.oop.pow.2 | 0 | 4.61587e-05 | 4.58485e-05 | 4.57343e-05 | 4.73927e-05 | 4.87325e-05 | 5.08874e-05 | 5.34643e-05 | 5.652e-05 | 0.00434 | 0.00571721 | 0.00663922 | 0.00843054 | 0.0100239 | 0.0116184 | 0.0132224 | 0.0147143 | 0.0161452 | 0.0174586 | 0.0186723 |
| M17778 | Other oil products and diesel  egy.mit.env.ffs.cost.oop.ind.2 | -1.75279e-15 | 0 | 0 | 0 | 0 | 0.0542925 | 0.11697 | 0.188308 | 0.267943 | 0.3514 | 0.445922 | 0.549258 | 0.661624 | 0.783044 | 0.913207 | 1.05197 | 1.18328 | 1.31993 | 1.46208 | 1.60983 |
| M17779 | Coal - other egy.mit.env.ffs.cost.coa.other.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17780 | Natural gas - other egy.mit.env.ffs.cost.nga.other.2 | 0 | 0 | 0 | 0 | 0 | 0.000748702 | 0.00160081 | 0.00256269 | 0.00363746 | 0.00482373 | 0.00614826 | 0.00761168 | 0.00922557 | 0.0109986 | 0.0129402 | 0.0150607 | 0.0173162 | 0.0197624 | 0.0224128 | 0.0250169 |
| M17781 | Gasoline - other egy.mit.env.ffs.cost.gso.other.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M17782 | Diesel and other oil products  egy.mit.env.ffs.cost.die.other.2 | -1.66641e-16 | 1.9853e-16 | -1.29101e-16 | -3.03055e-16 | 2.1848e-16 | 0.0068719 | 0.0147214 | 0.0235951 | 0.0334679 | 0.0442966 | 0.056494 | 0.0699471 | 0.0847022 | 0.1008 | 0.11824 | 0.137043 | 0.155717 | 0.175496 | 0.196429 | 0.218568 |
| M18090 | Air pollution costs egy.mit.airpol.cost.ecy.ind.2 | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |
| M18102 | Air pollution costs egy.mit.airpol.cost.ecy.res.2 | 0.0110344 | 0.0088123 | 0.00773269 | 0.00722611 | 0.00857438 | 0.00916779 | 0.010325 | 0.0114702 | 0.0126387 | 0.0121664 | 0.0119797 | 0.0117174 | 0.0114698 | 0.0112426 | 0.0110322 | 0.0108376 | 0.0103017 | 0.00980513 | 0.00934449 | 0.00891681 |

## Appendix: R5 and R11 series (legacy 465, Egypt)

```
R5 intended scen2: t | dR usd bn | PI | GI | dR%GDP | PI% | GI% | need | Req | PubReq | E_BAU | phi | E_NZ | ER | ERpub | CumGI | pi | ERgi
2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 400.9 | 1 | 400.9 | 0 | 0 | 0 | - | -
2023 | 0.0007158 | 0 | 0 | 1.261e-06 | 0 | 0 | 0 | - | - | 412.3 | 1 | 412.3 | 0 | 0 | 0 | - | -
2024 | 0.0006238 | 0 | 0 | 1.073e-06 | 0 | 0 | 0 | - | - | 463.6 | 1 | 463.6 | 0 | 0 | 0 | - | -
2025 | 0.0006094 | 0 | 0 | 1.004e-06 | 0 | 0 | 0 | - | - | 489.8 | 1 | 489.8 | 0 | 0 | 0 | - | -
2026 | 0.000647 | 0.0003235 | 0.0001618 | 1.023e-06 | 5.116e-07 | 2.558e-07 | 0.008564 | 0.008816 | 0.004408 | 497.6 | 0.9706 | 482.9 | -14.63 | -7.317 | 2.558e-07 | 5.803e-05 | -0.0004246
2027 | 0.1686 | 0.0843 | 0.04215 | 0.0002543 | 0.0001272 | 6.358e-05 | 0.008564 | 0.01763 | 0.008816 | 513.3 | 0.9412 | 483.2 | -30.2 | -15.1 | 6.383e-05 | 0.007241 | -0.1093
2028 | 0.3862 | 0.1931 | 0.09655 | 0.000552 | 0.000276 | 0.000138 | 0.008564 | 0.02645 | 0.01322 | 528.1 | 0.9118 | 481.5 | -46.6 | -23.3 | 0.0002018 | 0.01526 | -0.3556
2029 | 0.6123 | 0.3062 | 0.1531 | 0.0008317 | 0.0004159 | 0.0002079 | 0.008564 | 0.03526 | 0.01763 | 543 | 0.8824 | 479.1 | -63.89 | -31.94 | 0.0004098 | 0.02324 | -0.7423
2030 | 0.846 | 0.423 | 0.2115 | 0.001096 | 0.000548 | 0.000274 | 0.008564 | 0.04408 | 0.02204 | 556.8 | 0.8529 | 474.9 | -81.88 | -40.94 | 0.0006838 | 0.03102 | -1.27
2031 | 1.068 | 0.5342 | 0.2671 | 0.001321 | 0.0006605 | 0.0003302 | 0.008564 | 0.0529 | 0.02645 | 567.2 | 0.8235 | 467.1 | -100.1 | -50.05 | 0.001014 | 0.03834 | -1.919
2032 | 1.293 | 0.6465 | 0.3232 | 0.001526 | 0.0007632 | 0.0003816 | 0.008564 | 0.06171 | 0.03086 | 579.1 | 0.7941 | 459.9 | -119.2 | -59.61 | 0.001396 | 0.04523 | -2.696
2033 | 1.539 | 0.7696 | 0.3848 | 0.001736 | 0.0008678 | 0.0004339 | 0.008564 | 0.07053 | 0.03526 | 595.1 | 0.7647 | 455.1 | -140 | -70.01 | 0.00183 | 0.05188 | -3.632
2034 | 1.79 | 0.895 | 0.4475 | 0.001929 | 0.0009646 | 0.0004823 | 0.008564 | 0.07935 | 0.03967 | 610.7 | 0.7353 | 449 | -161.7 | -80.83 | 0.002312 | 0.05827 | -4.71
2035 | 2.047 | 1.023 | 0.5117 | 0.002109 | 0.001055 | 0.0005273 | 0.008564 | 0.08816 | 0.04408 | 627.1 | 0.7059 | 442.6 | -184.4 | -92.22 | 0.002839 | 0.06441 | -5.939
2036 | 2.308 | 1.154 | 0.577 | 0.002276 | 0.001138 | 0.0005689 | 0.008564 | 0.09698 | 0.04849 | 643.8 | 0.6765 | 435.5 | -208.3 | -104.1 | 0.003408 | 0.07028 | -7.32
2037 | 2.572 | 1.286 | 0.643 | 0.002428 | 0.001214 | 0.0006069 | 0.008564 | 0.1058 | 0.0529 | 661 | 0.6471 | 427.7 | -233.3 | -116.6 | 0.004015 | 0.0759 | -8.854
2038 | 2.838 | 1.419 | 0.7095 | 0.002565 | 0.001283 | 0.0006413 | 0.008564 | 0.1146 | 0.05731 | 678.6 | 0.6176 | 419.2 | -259.5 | -129.7 | 0.004656 | 0.08125 | -10.54
2039 | 3.106 | 1.553 | 0.7764 | 0.00269 | 0.001345 | 0.0006725 | 0.008564 | 0.1234 | 0.06171 | 696.8 | 0.5882 | 409.9 | -286.9 | -143.4 | 0.005329 | 0.08635 | -12.39
2040 | 3.375 | 1.688 | 0.8438 | 0.002802 | 0.001401 | 0.0007006 | 0.008564 | 0.1322 | 0.06612 | 715.4 | 0.5588 | 399.8 | -315.6 | -157.8 | 0.006029 | 0.09119 | -14.39
R5 legacy cached scen2 rows 12554-12566,12571-12580 (L..AD)
12554 ['0', '0.0007158', '0.0006238', '0.0006094', '0.000647', '0.1686', '0.3862', '0.6123', '0.846', '1.068', '1.293', '1.539', '1.79', '2.047', '2.308', '2.572', '2.838', '3.106', '3.375']
12555 ['0', '0', '0', '0', '0.0003235', '0.0843', '0.1931', '0.3062', '0.423', '0.5342', '0.6465', '0.7696', '0.895', '1.023', '1.154', '1.286', '1.419', '1.553', '1.688']
12556 ['0', '0', '0', '0', '0.0001618', '0.04215', '0.09655', '0.1531', '0.2115', '0.2671', '0.3232', '0.3848', '0.4475', '0.5117', '0.577', '0.643', '0.7095', '0.7764', '0.8438']
12559 ['0.01491', '0.01469', '0.01544', '0.01331', '0.0122', '0.02', '0.02', '0.02', '0.02', '0.03', '0.04', '0.04', '0.04', '0.04', '0.04', '0.04', '0.04', '0.04', '0.04']
12560 ['0', '0', '0', '0', '0.002439', '0.004', '0.004', '0.004', '0.004', '0.006', '0.008', '0.008', '0.008', '0.008', '0.008', '0.008', '0.008', '0.008', '0.008']
12561 ['0', '0', '0', '0', '5.024', '8.24', '8.24', '8.24', '8.24', '12.36', '16.48', '16.48', '16.48', '16.48', '16.48', '16.48', '16.48', '16.48', '16.48']
12565 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12566 ['-', '-', '-', '-', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12567 ['-', '-', '-', '-', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf']
12571 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12572 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12573 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12576 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
12577 ['0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf']
12580 ['0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf']
12581 ['-', '-', '-', '-', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf']
12582 ['-', '-', '-', '-', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf', '0xf']
R11: t | iota(456) | CA0 nom | CA0% | CAr | oil(18185) | gas(18186) | coal(18187) | CA1 USD | Yhat | CA1% intended (incl coal)
2022 | 1.13682 | -16.5513 | -3.48279 | -18.8158 | 0 | 0 | 0 | -18.8158 | 5.40251 | -3.48279
2023 | 1.09176 | -4.7105 | -1.19608 | -5.14274 | 2.38374e-05 | 0.000210909 | 0 | -5.14251 | 4.29966 | -1.19603
2024 | 1.06046 | -20.8066 | -5.43104 | -22.0645 | 2.1934e-05 | 0.000170941 | 0 | -22.0643 | 4.06266 | -5.43099
2025 | 1.03228 | -15.4246 | -4.23009 | -15.9225 | 1.78271e-05 | 0.000176867 | 0 | -15.9223 | 3.76411 | -4.23003
2026 | 1 | -17.8346 | -4.151 | -17.8346 | 2.0018e-05 | 0.000205383 | 0 | -17.8344 | 4.29645 | -4.15095
2027 | 0.979036 | -20.9506 | -4.58362 | -20.5113 | 0.0509863 | 0.00434028 | 0.00127896 | -20.4547 | 4.47492 | -4.57097
2028 | 0.958114 | -19.6742 | -3.8693 | -18.8501 | 0.100083 | 0.012161 | 0.00259352 | -18.7353 | 4.87172 | -3.84573
2029 | 0.9376 | -19.6135 | -3.5019 | -18.3896 | 0.150338 | 0.01907 | 0.00394145 | -18.2162 | 5.25132 | -3.46889
2030 | 0.917508 | -19.3982 | -3.17492 | -17.798 | 0.200766 | 0.0268043 | 0.00531096 | -17.5651 | 5.60581 | -3.13338
2031 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.25205 | 0.0325827 | 0.00670878 | -15.6524 | 5.97635 | -2.61906
2032 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.308728 | 0.038839 | 0.00817919 | -15.588 | 5.97635 | -2.60828
2033 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.366956 | 0.0463757 | 0.00968514 | -15.5207 | 5.97635 | -2.59702
2034 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.426789 | 0.0539347 | 0.0112216 | -15.4518 | 5.97635 | -2.58549
2035 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.487641 | 0.0615131 | 0.0127829 | -15.3818 | 5.97635 | -2.57378
2036 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.549058 | 0.0690964 | 0.0143605 | -15.3112 | 5.97635 | -2.56197
2037 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.610707 | 0.0765354 | 0.0159488 | -15.2405 | 5.97635 | -2.55014
2038 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.672271 | 0.0837577 | 0.0175428 | -15.1702 | 5.97635 | -2.53837
2039 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.733631 | 0.0907289 | 0.0191406 | -15.1002 | 5.97635 | -2.52667
2040 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.794721 | 0.0974457 | 0.0207417 | -15.0308 | 5.97635 | -2.51505
2041 | 0.897896 | -17.7568 | -2.66781 | -15.9437 | 0.855475 | 0.103719 | 0.0223451 | -14.9622 | 5.97635 | -2.50357
coal change 18177: ['0', '0', '0', '0', '0', '-5.482', '-11.29', '-17.44', '-23.94', '-30.78', '-37.53', '-44.44', '-51.49', '-58.65', '-65.89', '-73.18', '-80.49', '-87.82', '-95.17', '-102.5']
```
