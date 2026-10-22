# Legacy CPAT power-input chains: spec for a formula re-implementation

Source: `CPAT 1.0pre_456_NoPropData.xlsb` (cached run: Egypt, EGY, baseline). Items: every column of `data/power_tech.csv`, every key of `data/power_paths.csv` and `data/power_params.csv`, as copied by `excel_ai/mitigation/extract_power_v4_5.py`.

**Cross-check result:** I recomputed every copied cell from the cached Mitigation values (the `v_Mitigation` dump) and compared it with the three CSVs: **0 mismatches** (relative tolerance 1e-12). This covers all 9 techs × 17 traced tech columns, all 37 path rows × 20 years, and all 22 params.


**v4.10: the legacy bugs this spec documents are fixed in the prototype's data step (user rule: bugs are never replicated).**
The chains below describe legacy as it is. The prototype departs from them in five places (register L52-L56): Rule-C for
every type (L52, section 1.1); the actual capacity factor from installed capacity of the base year over Power F:AC,
inside the CFOverride bounds (L53, section 1.2); hydro investment from the base year only above a 50% hydro share
(L54, section 2.15); country rows looked up in the country block, Power rows 112-294 (L55); default WACC for countries
without CoC risk data (L56, section 6).
---

## 0. Conventions and caveats (read first)

* **Year columns on Mitigation:** K = 2021, **L = 2022** (= `FirstYearCalculations`), M = 2023 … AE = 2041. Row 1 holds the year headers (`L1 = FirstYearCalculations`, `K1 = L1-1`).
* **Tech row order** in every Mitigation engineer-model table: coa, nga, oil/oop, nuc, wnd, sol, hyd, ore, bio (row offset 0..8). Tables A2, A4, A7 and A14/A15 use the code `oil` (column B). Tables A16, B*, D* and later use `oop`. The Power tab and the CoC tab use `oil`.
* **Defined names:** use the workbook-level names (sheet index −1 in `names.tsv`). The sheet-index-17 copies (index 17 = sheet **ECP**) point one row higher in ScenarioDefinition, for example `CFOverrideIfAbove` → F376 instead of F377. They do not apply to Mitigation formulas. pyxlsb2 decoding of the xlsb confirms this: `FirstYearCalculations` → `ScenarioDefinition!$F$232`.
* **ScenarioDefinition column F = Dashboard.** Every setting has the form `ScenarioDefinition!F<r> = IF(ScenarioDefinition!$C$5, D<r>, IF(ScenarioDefinition!$F$16="Default", IF(I<r>="Y", E<r>, G<r>), E<r>))`, with `C5 = FALSE` ("MT is active") and `F16 = "Manual*"`. So F = E = a Dashboard cell (`ScenarioDefinition!E<r> = Dashboard!<cell>`). The settings table in section 7 lists every Dashboard cell used.
* **XLOOKUP caveat in the `f_` dumps:** the LibreOffice conversion **drops the first argument of every `_xlfn.XLOOKUP`**. Example: the dump shows `XLOOKUP(CoC!$B$202:$B$390,CoC!$D$202:$D$390,0.075)`. The true formula, decoded from the xlsb tokens with pyxlsb2, is `XLOOKUP(G2988, CoC!$B$202:$B$390, CoC!$D$202:$D$390, 0.075)`. Section 1.4 gives the corrected formulas, which the cached values confirm.
* **Scenario index:** `Mitigation!C2173` = 1 in the baseline block (rows 2954–4300), from `INDEX($N$224:$AC$224, MATCH(B2173,$N$223:$AC$223,0))`. The carbon-tax copy of the engineer model sits at rows +6331 (row 9285 onwards) with C-index > 1.
* **Country identity:** `_Countryname = ScenarioDefinition!F8 = Dashboard!E2` ("Egypt"). `_Country_code = Dashboard!D644 = VLOOKUP(_Countryname, Countries!$C$6:$D$227, 2, FALSE)` ("EGY"). Formulas use `LOWER(_Country_code)` ("egy") for the Power codes. MATCH and XLOOKUP are case-insensitive, so "egy" also matches "EGY".
* **Constants:** `_conv_ktoe_to_gwh = Mitigation!E1033 = 11.63` (typed value). `_conv_gwh_to_mwy = Mitigation!E1044 = 1000/(365*24)`. `_conv_ktoe_to_mwy = Mitigation!E1034 = E1033*E1044 = 1.32762557…`. `_conv_kWh_to_GJ = Mitigation!E1045 = 0.0036`.

---

## 1. Shared building blocks

### 1.1 A2 "Main Parameters": Power technoeconomic lookup (Mitigation rows 2976–2985)

Row r = 2977 + i, with tech code `B<r>` ∈ {coa, nga, oil, nuc, wnd, sol, hyd, ore, bio}.

| Cell | Formula (names restored) | Meaning |
|---|---|---|
| E<r> | `="wld.mpp."&B<r>` | world code |
| G<r> | `=LOWER(_Country_code)&".mpp."&B<r>` | country code, e.g. `egy.mpp.coa` |
| L<r> | `=IFERROR(MATCH(E<r>,Power!$A$25:$A$356,0),0)` | world index |
| K<r> | `=IFERROR(MATCH(G<r>,Power!$A$25:$A$356,0),L<r>)` | country index, falls back to world |
| M<r> | `=L<r>` | "3rd helper", = world |
| N<r> (CapacityFactor) | `=IF(INDEX(Power!E$25:E$355,$K)>0, INDEX(..,$K), IF(INDEX(..,$L)>0, INDEX(..,$L), INDEX(..,$M)))` | **country if > 0, else world** (all 9 techs) |
| O<r> (CapEx $/kW) | same pattern on `Power!F$25:F$356` | country if > 0, else world (all techs) |
| P..T, rows 2977–2980 (coa, nga, oil, nuc) | same "> 0" pattern on Power!G (Efficiency.NCV), H (OpexFixed $/kW/y), I (OpexVariable $/kWh), J (WACC), K (TotalLifetime) | country if > 0, else world |
| P..T, rows 2981–2985 (wnd, sol, hyd, ore, bio) | `=IFERROR(IF(ISERROR(INDEX(Power!G$25:G$356,$K)), INDEX(..,$K), IF(ISERROR(INDEX(..,$L)), INDEX(..,$L), INDEX(..,$M))),0)` | **bug:** inverted ISERROR logic, so the result is always the **world** value (M); country data is ignored |

* The index is relative to Power row 25: Power row = 24 + index. MATCH searches `Power!A25:A356`, which spans the world, regional, country, ctf and dtc blocks. **The regional block is never looked up deliberately.**
* Egypt indices: coa 4 (row 28), nga **142 (row 166, `egy.mpp.nga`)**, oil 6 (row 30), nuc 7 (31), wnd 9 (33), sol **206 (row 230, `egy.mpp.sol`)**, hyd 8 (32), ore 11 (35), bio 12 (36). The world rows are 28–36, in the order coa nga oil nuc hyd wnd sol ore bio.
* Egypt results:

| Column | coa | nga | oil | nuc | wnd | sol | hyd | ore | bio |
|---|---|---|---|---|---|---|---|---|---|
| N (CF) | .535 | .566 | .134 | .934 | .3 | .18 | .43229 | .75120 | .68577 |
| O (capex) | 2000 | **1304.195** (country) | 1345.38 | 4000 | 1300 | **1222.683** (country) | 3300 | 3500 | 2000 |
| P (eff.) | .34354 | **.594** (country) | .37660 | .38 | 0 | 0 | 0 | .38142 | .25275 |
| Q (opex fix) | 60 | **32.05** (country) | 23.525 | 150 | 40 | **15** (world; country H230 = 11.831 ignored) | 50 | 100 | 100 |
| R (opex var) | .003 | **.004** | .00517 | .004 | 0 | 0 | .001 | 0 | .003 |
| S (WACC) | .08039 | .07710 | .07757 | .07397 | .06877 | .07478 | .08295 | .09869 | .07106 |
| T (life) | 30 | 30 | 35 | 50 | 30 | 25 | 50 | 30 | 30 |

  For nga, the country row 166 has blank E, J and K, so those fall back to world row 29. The S column (Power J) is not used under the current WACC setting (section 1.4).

### 1.2 A1 / A4: energy-balance block (country data from Balances)

1. **Mitigation rows 503–520** (fuels `C503:C520` = ecy coa nga oop gso die ker lpg jfu wnd sol hyd ore nuc bio bgs bdi obf; flows `E501:W501` = imports production exports stockcha worldav worldnav tes · statdiff transfer ownuse distloss tottranf power tfc · eloutput info_agrc):
   `X<r> = INDEX(_balances, MATCH($C$501&X$501, _bal_countries&_bal_flows, 0), MATCH($C<r>, _bal_fuels, 0))`.
   This is an array MATCH on a concatenated key. `_balances = Balances!A13:Z4044`, `_bal_countries = Balances!A13:A4044`, `_bal_flows = Balances!E13:E4044`, `_bal_fuels = Balances!A13:Z13`, and `C501 = _Country_code`.
   **The year is not part of the key**, so the Balances tab must hold a single year per country (this file has EGY 2022 only, rows 14–50).
2. **Rows 584–597** (C584:C597 = coa nga oop gso die ker lpg jfu wnd sol hyd ore nuc bio). With `C578 = (BalancesOrConsumption="Balances")` = TRUE:
   * `E<r> = IF($C$578, V<r−80>, …EnergyCons…)`: power output, GWh (flow `eloutput`).
   * `F<r> = IF($C$578, −S<r−80>, …)`: fuel input, ktoe (minus flow `power`).
   * Example: `E584 = V504`, `F584 = −S504`.
3. **A1 rows 2959–2973:**
   * `L<r> = $F$<584+k>` (input ktoe) and `M<r> = $E$<584+k>` (output GWh), for k = 0..13.
   * Row 2973 "All oil products" (code `oil`): `L2973 = SUM(L2961:L2966)`, `M2973 = SUM(M2961:M2966)` (oop gso die ker lpg jfu).
4. **A4 rows 2999–3007** (`B` = coa nga oil nuc wnd sol hyd ore bio):

| Cell | Formula |
|---|---|
| K | `=MATCH(B,$B2959:$B2973,0)` (oil → row 2973) |
| L (primary energy MWy) | `=INDEX(L2959:L2973,$K,0)*_conv_ktoe_to_mwy` |
| M (power output MWy) | `=INDEX(M2959:M2973,$K,0)*_conv_gwh_to_mwy` |
| N (capacity actual MW) | `=INDEX(Power!$F$358:$Y$1635, MATCH(LOWER(_Country_code)&"."&B, Power!$C$358:$C$1635,0), MATCH(FirstYearCalculations, Power!$F$357:$Y$357,0))` → **#N/A** (bug: 2022 sits in column AB, outside F:Y = 2000–2019) |
| O (eff. actual) | `=M/L` (#DIV/0! when there is no input) |
| P (eff. studies) | coa, nga, oil, nuc, bio: `=P<A2 row>`; wnd, sol, hyd, ore: typed constant **1.0** |
| Q (CF actual) | `=IFERROR(M/N,0)` → 0 (N is #N/A) |
| R (CF studies) | `=N<A2 row>` |
| S (min CF) | wnd, sol: `CFOverrideIfBelowWndSol` (ScenarioDefinition!F375 = Dashboard!G196 = 0.1); others: `CFOverrideIfBelowFosOth` (F376 = G197 = 0.01) |
| T (max CF) | `CFOverrideIfAbove` (F377 = G198 = 1) |
| **V (eff. used)** | `=IFERROR(IF(O<MinimumThermalEfficiency,P,O),P)`, with MinimumThermalEfficiency = ScenarioDefinition!F380 = Dashboard!G194 = 0.1 |
| **W (CF used)** | `=IFERROR(IF(AND(Q<T,Q>S),Q,R),R)` → always R, because Q = 0 |
| X | `=1/W` |
| **Y (capacity used, MW)** | `=M*X` |

### 1.3 A7: capex time factors (rows 3036–3046)

* `L3036 = FirstYearCalculations`.
* `L3037 = MATCH(L3036, CapexTimeFactorYearRange, 0)`, where `CapexTimeFactorYearRange = Power!F302:BD302` (2000..2050). So 2022 → 23 → Power column AB.
* Row r = 3038 + i:
  * `E = "wld.ctf."&scen&"."&B`. scen = `"med"` (typed) for coa, nga, oil, nuc. For wnd, sol, hyd, ore, bio, scen = `IF(RenewableCostDeclineRate="Low","low",IF(RenewableCostDeclineRate="Medium*","med",IF(RenewableCostDeclineRate="High","hgh","vhg")))`, with `RenewableCostDeclineRate` = ScenarioDefinition!F367 = Dashboard!G52 = "Medium*".
  * `F = LOWER(_Country_code)&"."&scen&".ctf."&B` (`egy.med.ctf.coa`). The segment order differs from the world codes and the Power tab has no country ctf rows, so this **never matches**.
  * `I = IFERROR(MATCH(E,Power!$A$25:$A$356,0),0)`, `J = IFERROR(MATCH(F,Power!$A$25:$A$356,0),I)`.
  * `L..AE = INDEX(Power!F$25:$BE$597, $J, L$3037)`.
* Egypt indices → Power rows: coa 283 → 307, nga 288 → 312, oil 290 → 314, nuc 289 → 313, wnd 296 → 320, sol 295 → 319, hyd 285 → 309, ore 292 → 316 (the code `wld.ctf.med.ore` also appears at row 318; the first match wins), bio 280 → 304.

### 1.4 A3: WACC (rows 2987–2996; coa … bio = rows 2988–2996)

| Cell | Formula (first XLOOKUP argument restored) | Egypt |
|---|---|---|
| G | `=LOWER(_Country_code)` | egy |
| AA | `=INDEX(Countries!$H$6:$H$227, MATCH(_Countryname, Countries!$C$6:$C$227,0),1)`, income code (Countries!H = IF(G="Low income","LIC",…,"HIC")) | LMIC (Countries row 65) |
| AC | typed tech code: coa nga oil nuc wnd sol hyd ore bio | |
| AB ("Tech") | `=IFERROR(XLOOKUP(G, CoC!$B$202:$B$390, CoC!$D$202:$D$390, 0.075), 0.075) + XLOOKUP(AC, CoC!$X$203:$X$211, XLOOKUP(AA, CoC!$Y$202:$AB$202, CoC!$Y$203:$AB$211))` | .0994764 + tech adjustment |
| I ("Country*") | `=IFERROR(XLOOKUP(G, CoC!$B$202:$B$390, CoC!$D$202:$D$390, 0.075), 0.075) + XLOOKUP(AA, CoC!$Y$202:$AB$202, CoC!$Y$205:$AB$205)` (coal adjustment, row 205, applied to all techs) | .124126 |
| Q | `=S<A2 row>` (Power J) | |
| R | `=IF(WACCSource="User", WACCUserGlobal, IF(WACCSource="Income*", IncomeDepWACC, Q))`. `IncomeDepWACC = Mitigation!S82 = INDEX(Power!$N$20:$N$23, MATCH(S81, Power!$M$20:$M$23,0))` | |
| S, T, U, V, W | `S = IF(L="Yes",M,R)`; `T = IF(C2173>1, N, "No*")`; `U = IF(T="Delta",O,0)`; `V = IF(T="Override",P,"")`; `W = MinimumWACC` (ScenarioDefinition F348 = Dashboard Q193 = 0.01) | |
| **X (Final WACC)** | `=IF(D_WACCSource="Country*", I, IF(D_WACCSource="Tech", AB, MAX(IF(T="Override",V,S+U),W)))`, with `D_WACCSource = Dashboard!Q191` = **"Tech"** (`WACCSource` = ScenarioDefinition!F365 is the same cell) | = AB |
| Y | `=1/(1+X)` | |

* Only CoC column **D (2022)** is used: WACC is constant over time.
* CoC tech-adjustment table (X203:X211 × Y..AB = HIC/UMIC/LMIC/LIC), LMIC column AA: bio .03215 (row 203), nga .02465 (204), coa .02465 (205), ore .04425 (206), hyd .02725 (207), sol .02935 (208), oil .02465 (209), nuc .02725 (210), wnd .02935 (211).
* `CoC!D253` (EGY) = 0.09947642998297449.

### 1.5 A5 / A6: discounted lifetime (used by dlf_ren and cel)

`G3026+i = (1-$Y<2988+i>^$G<3012+i>)/(1-$Y<2988+i>)`, where `G3012+i = T<2977+i>` (lifetime). This is the sum over k = 0..n−1 of (1+wacc)^−k. Egypt: wnd G3030 = 8.531278484, sol G3031 = 8.338794967.

---

## 2. PowerTech items (power_tech.csv)

Notation: i = tech offset (coa 0 … bio 8). "Rule-C" means "country Power row if > 0, else world". "Rule-W" means "world row only" (the bug in section 1.1).

### 2.1 cax0_usd_per_kw: capital cost at time factor 1

1. **Copied:** `Mitigation!H(3181+i) / Mitigation!L(3038+i)`.
2. **Chain:**
   * `H3181 = L3099` (B2, "assumed capex for existing capital stock").
   * `L3099 = $O2977*L3038` (A13: capex × time factor).
   * So **cax0 = O(2977+i)**, the A2 CapEx (Power!F, Rule-C for all techs).
3. **Country-specific:** yes, via the Power country row `iso.mpp.<t>` (Egypt: nga row 166, sol row 230). Otherwise global (world rows 28–36).
4. **Egypt:** coa 2000, nga 1304.195, oop 1345.3800, nuc 4000, wnd 1300, sol 1222.683, hyd 3300, ore 3500, bio 2000. Matches the CSV.

### 2.2 life_years

1. **Copied:** `Mitigation!T(2977+i)` (A2 TotalLifetime).
2. **Chain:** Power!K lookup. coa, nga, oil, nuc use Rule-C. **wnd, sol, hyd, ore, bio use Rule-W (bug)**.
3. **Country-specific:** coa..nuc only, when the country row has K (Egypt's rows have none). Otherwise global.
4. **Egypt:** 30, 30, 35, 50, 30, 25, 50, 30, 30. Matches the CSV.

### 2.3 efficiency

1. **Copied:** `Mitigation!L(3061+i)` (A9; `L3061 = V2999`, M.. = L).
2. **Chain:** `V = IFERROR(IF(O<MinimumThermalEfficiency, P, O), P)`.
   * O = actual efficiency = Balances eloutput (GWh × 1000/8760) / (−Balances power (ktoe) × 11.63 × 1000/8760). For `oil`, the fuel sums oop + gso + die + ker + lpg + jfu.
   * Fallback P = A2 P (Power!G: Rule-C for coa..nuc; Rule-W for bio), or the constant 1.0 for wnd, sol, hyd, ore.
   * MinimumThermalEfficiency = Dashboard!G194 = 0.1.
3. **Country-specific:** yes (Balances). The fallback is the Power G column.
4. **Egypt:** coa .343545 (no input → P = world G28), nga .4749917 (Balances: 175355.62 GWh / 31743.44 ktoe), oop .3214695, nuc .38 (P), wnd 1.0038548, sol 1.0261872, hyd .9374616, ore 1.0 (P), bio .2527459 (P). Matches the CSV.

### 2.4 capacity_factor

1. **Copied:** `Mitigation!L(3049+i)` (A8; `L3049 = W2999`, later years = L).
2. **Chain:** `W = IFERROR(IF(AND(Q<T,Q>S),Q,R),R)`. Q is always 0 because of the installed-capacity lookup bug (section 1.2). So **CF = R = A2 N = Power!E, Rule-C (all techs)**. The bounds S and T (CFOverride*) never act.
3. **Country-specific:** only through a country E value (Egypt's rows have none). Effectively global for Egypt.
4. **Egypt:** .535, .566, .134, .934, .3, .18, .4322928214, .7512024819, .6857673941. Matches the CSV.

### 2.5 wacc

1. **Copied:** `Mitigation!H(3203+i)` (B4 "Final WACC"; `H3203 = X2988` … `H3211 = X2996`).
2. **Chain:** section 1.4. With D_WACCSource = "Tech":
   `wacc = IFERROR(XLOOKUP(iso, CoC!B202:B390, CoC!D202:D390, 0.075), 0.075) + XLOOKUP(tech, CoC!X203:X211, XLOOKUP(income, CoC!Y202:AB202, CoC!Y203:AB211))`.
   The income code comes from Countries!H6:H227 by country name (Countries!C6:C227).
3. **Country-specific:** yes (CoC country WACC 2022 plus the income-group tech adjustment).
4. **Egypt:** coa/nga/oop .12412642998, nuc/hyd .12672642998, wnd/sol .12882642998, ore .14372642998, bio .13162642998. Matches the CSV.

### 2.6 dtc_usd_per_kw: decommissioning cost

1. **Copied:** `Mitigation!L(3110+i)` (A14).
2. **Chain:** `L3110 = INDEX(Power!$E$25:$E$355, $K3110)*$O2977`, with `K3110 = IFERROR(MATCH("wld.dtc."&B3110, Power!$A$25:$A$356,0),0)` (rows 346–354). In words: world decommissioning share × A2 capex.
3. **Country-specific:** only via capex (O). The share is global.
4. **Egypt:** 100, 13.04195, 33.0210467, 532.133695, 39, 73.36098, 660, 253.788727, 145.02213. Matches the CSV.

### 2.7 tcx_usd_per_kw: transmission capex (legacy label: "not used in the model at all")

1. **Copied:** `Mitigation!L(3121+i)` (A15).
2. **Chain:** `L3121 = INDEX(Power!$F$25:$F$355, $K3110)*$O2977`. It reuses A14's helper K3110 instead of its own K3121 (same value). In words: world transmission share (Power F346:F354) × capex.
3. **Country-specific:** via capex only.
4. **Egypt:** 597.474101, 382.180237, 447.878551, 449.426341, 405.468607, 335.334508, 756.528401, 347.657362, 267.624027. Matches the CSV.

### 2.8 opf_usd_per_kwh: fixed O&M per kWh

1. **Copied:** `Mitigation!L(3132+i)` (A16).
2. **Chain:** `L3132 = $Q2977/(365*24*L3049)`, that is Power!H (opex fixed $/kW/y; Rule-C for coa..nuc, **Rule-W for wnd..bio**) / (8760 × CF used).
3. **Country-specific:** via H (coa..nuc country rows) and CF. For Egypt: nga uses country H166 = 32.05. **sol uses world 15, not country 11.831 (bug).**
4. **Egypt:** .0128024581, .0064640915, .0200410618, .0183332844, .0152207002, .0095129376, .0132034637, .0151963357, .0166463515. Matches the CSV.

### 2.9 vop_usd_per_kwh: variable O&M

1. **Copied:** `Mitigation!L(3339+i)` (D1).
2. **Chain:** `L3339 = $R2977` (Power!I; Rule-C for coa..nuc, Rule-W for wnd..bio). The H column code `egy.mit.vro.pow.<t>.t.1` is a label only.
3. **Country-specific:** coa..nuc via the country row (Egypt nga = .004 from row 166, world .002).
4. **Egypt:** .003, .004, .00517, .004, 0, 0, .001, 0, .003. Matches the CSV.

### 2.10 fuel_fixed_usd_per_kwh (nuclear only; 0 for the others by script)

1. **Copied:** `Mitigation!L3353` (D2, nuclear row). The script writes 0 for the other techs (their D2 rows are fuel prices, handled through price_code).
2. **Chain:** `L3353 = K2727` (**column shift:** the 2022 cell takes the 2021 value; `M3353 = L2727`). `K2727 = K$710`, and `Mitigation!K710:AE710` hold the **typed constant 0.004** ("Uranium Fuel Cost", $/kWhe). Power!G22 = 0.004 is the documented source but is not linked.
3. **Country-specific:** no (global constant).
4. **Egypt:** nuc 0.004, others 0. Matches the CSV.

### 2.11 cap0_mw: base-year effective capacity

1. **Copied:** `Mitigation!Y<A4 row>` (A4, rows 2999–3007 matched by code; oop → `oil` row 3001).
2. **Chain:** `Y = M*(1/W)`, that is gen0 / CF used.
3. **Country-specific:** yes (Balances).
4. **Egypt:** 0, 35367.0761395, 15765.4362799, 0, 2387.25143731, 3326.62425071, 3879.79648188, 0, 0. Matches the CSV.

### 2.12 gen0_mwy: base-year generation

1. **Copied:** `Mitigation!M<A4 row>`.
2. **Chain:** `M = INDEX(M2959:M2973,K,0)*_conv_gwh_to_mwy`, where M2959.. = E584.. = Balances flow `eloutput` (GWh) for the fuel. oil = sum of oop..jfu.
3. **Country-specific:** yes (Balances).
4. **Egypt:** 0, 20017.765095, 2112.5684615, 0, 716.17543119, 598.79236513, 1677.2081677, 0, 0. Matches the CSV.

### 2.13 retire_rate

1. **Copied:** `Mitigation!J(4011+i)` (K6).
2. **Chain:**
   * `J = 1/I`, with `I(4011+i) = T(2977+i)` (lifetime).
   * Hydro: `J4017 = IF(HydroDoesntRetire="Yes",0,1/I4017)`, where HydroDoesntRetire = ScenarioDefinition F350 = Dashboard V198 = "Yes".
3. **Country-specific:** only via lifetime (coa..nuc country K). Effectively global.
4. **Egypt:** 1/30, 1/30, 1/35, 1/50, 1/30, 1/25, 0, 1/30, 1/30. Matches the CSV.

### 2.14 invest_permitted

1. **Copied:** `Mitigation!G(4061+i)` (L3).
2. **Chain:**
   * `G = IF(E="If Present*", F, E)`.
   * `E = ScenarioDefinition!F$397..F$405` (NewInvCoa..NewInvBio = Dashboard U51:U59). Egypt: "If Present*" except wnd and sol = "Yes".
   * `F = IF(OR(_Country_code="WAV",_Country_code="WMR"),"Yes", IF(L(3932+i)/L3941>0.001,"Yes","No"))`, where `L3932+i = Y(A4)` is cap0 and `L3941 = SUM(L3932:L3940)`.
3. **Country-specific:** yes (capacity share from Balances), unless the Dashboard overrides it.
4. **Egypt:** No, Yes, Yes, No, Yes, Yes, Yes, No, No. Matches the CSV.

### 2.15 invest_start

1. **Copied:** `Mitigation!H(4061+i)`.
2. **Chain:**
   * `H = NewInv<Tech>Year`, that is ScenarioDefinition F407..F415 = Dashboard V51:V59 (2022, 2022, 2022, 2030, 2022, 2022, 2030, 2030, 2022).
   * **Hydro bug:** `H4067 = IF($L$3827>50%, FirstYearCalculations, NewInvHydYear)`. L3827 is the year header of table I5 (2022), so the test is always true and hydro always starts in FirstYearCalculations (2022) instead of 2030. Probably intended: the hydro generation share L3846.
3. **Country-specific:** no (Dashboard).
4. **Egypt:** 2022, 2022, 2022, 2030, 2022, 2022, **2022**, 2030, 2022. Matches the CSV, including the hydro bug.

### 2.16 scaleup_rate

1. **Copied:** `Mitigation!G(4130+i)`.
2. **Chain:**
   * coa, nga, hyd: `MaxNonVREAsPCOfTotalGen` (ScenarioDefinition F359 = Dashboard Q194 = 0.05).
   * oop, nuc, ore, bio: `MaxNonNucOreBioAsPCOfTotalGen` (F360 = Q195 = 0.02).
   * wnd, sol: `VREMaxPercentagePointofTotalGen = Mitigation!S91 = INDEX(S85:S90, MATCH($O91, O85:O90, 0))`, where `O91 = ScenarioDefinition!F362` (MaxScaleUpRateCategory = Dashboard G53 = "CtryDefault*"). The options:
     * "CtryDefault*" → `S85 = INDEX(Power!$C$2349:$C$2570, MATCH(LOWER(_Country_code), Power!$B$2349:$B$2570, 0))`
     * Low → Power!J20 (.01); Medium → J21 (.02); High → J22 (.03); Vhigh → J23 (.04)
     * UserDefined → MaxWindSolarScaleup (F361 = Dashboard Q196 = .05)
3. **Country-specific:** wnd and sol under CtryDefault* (Power B2349:C2570; EGY row 2408 = 0.02). The others are global.
4. **Egypt:** .05, .05, .02, .02, .02, .02, .05, .02, .02. Matches the CSV.

### 2.17 planned_retirement (coal; "No" for the others by script)

1. **Copied:** `Mitigation!J3991` (K5 "Use Data?").
2. **Chain:**
   * `J3991 = INDEX(Power!$F$1750:$F$1857, Mitigation!I3992)`, with `I3992 = MATCH(_Country_code, Power!$D$1750:$D$1878, 0)` = 25 → Power row 1774 (EGY).
   * `Power!F1750.. = IF(AVERAGE(Z:AJ)<0.1,"No","Yes")` over the 5-year-averaged retirements.
   * Use: `L3991 = IFERROR(IF(OR(ISNA(INDEX(Power!$D$1749:$BD$1878,$I3992,L3990)), $J3991="No"),"DoNotUse","UseData"),"DoNotUse")`. The ISNA probe is offset by one row and three columns (bug, harmless).
3. **Country-specific:** yes (Power planned-retirement block).
4. **Egypt:** No (all 9). Matches the CSV.

### 2.18 Script constants (no legacy chain)

* `code` and `name`: labels.
* `price_code` (coa.pow, nga.pow, oop.all, bio.all): the section-2 fuel price rows that D2 uses.
* `vre` (wnd, sol, ore = 1) and `vre_share`: legacy C3 and rows 3851 / 3907 use these sets.
* `dispatch` (coa, nga = cg).
* `rns_usd_per_kwh = 0`. The nearest legacy analogue is RenewableSubsidyBL = ScenarioDefinition F354 = Dashboard L55 = 0.
* `source`.

---

## 3. PowerPaths items (power_paths.csv; years 2022–2041 = Mitigation L..AE)

### 3.1 tcf|<t>: capex time factor

1. **Copied:** `Mitigation!L..AE(3038+i)` (A7).
2. **Chain:** section 1.3, that is `INDEX(Power!F$25:$BE$597, MATCH("wld.ctf."&scen&"."&t, Power!$A$25:$A$356,0), MATCH(year, Power!$F$302:$BD$302,0))`.
3. **Country-specific:** no (world rows only). It depends on the Dashboard G52 scenario for the renewables.
4. **Egypt:** coa, nga, oop, nuc, hyd, ore, bio are 1.0 every year. wnd (Power row 320): 1.05 (2022), 1.0, .993, … .909 (2041). sol (row 319): 1.05, 1.0, .955, … .533. Matches the CSV.

### 3.2 cbat, cint, obat: battery capex, interface capex, battery opex

1. **Copied:** `Mitigation!L..AE 3887 / 3888 / 3891` (J2).
2. **Chain:**
   * `L3882 = MATCH(L3881, Power!$F$1883:$BD$1883)`. This is an **approximate** match (no third argument; the years are sorted ascending). L3881 = FirstYearCalculations + k.
   * `L3887 = INDEX(Power!$F$1899:$BD$1899,1,L3882)` (Battery Capex $/kWh).
   * `L3888 = INDEX(Power!$F$1903:$BD$1903,1,L3882)` (Batteryinterface Capex $/kW).
   * `L3891 = INDEX(Power!$F$1900:$BD$1900,1,L3882)` (Battery OpexFix $/kWh/y).
   * Power rows 1899–1911 are themselves formulas: € rows 1884–1895 converted to $ (2021 EUR→USD factor Power!D1897 = 1.18).
3. **Country-specific:** no.
4. **Egypt:** cbat 300.61444 (2022) … ; cint 150.30722 … ; obat 9.47422 … . Matches the CSV.

### 3.3 cel: electrolyser cost per marginal unit (LT storage)

1. **Copied:** `Mitigation!L3900 + L3901 + L3902` (per year).
2. **Chain:**
   * `L3900 = L3897/L3885`, where `L3897 = INDEX(Power!$F$1907:$BD$1907,1,L3882) + L3896` (electrolyser capex). Here `L3896 = L3895*L3894`, `L3895 = INDEX(Power!$F$1911:$BD$1911,1,L3882)` (storage tank $/kWh), and `L3894 = $E3879 = StorageHoursForLTStorage` (ScenarioDefinition F395 = Dashboard V196 = 1000).
   * `L3885 = L3883*365*24`, with `L3883 = AVERAGE($G3030:$G3031)` (dlf_ren, section 1.5).
   * `L3901 = L3898/L3884`, with `L3898 = INDEX(Power!$F$1908:$BD$1908,…)` (opex fixed) and `L3884 = 8760`.
   * `L3902 = L3899 = INDEX(Power!$F$1909:$BD$1909,…)` (variable opex).
3. **Country-specific:** **yes**, through dlf_ren (the country WACC of wnd and sol, plus their lifetimes). The Power costs are global.
4. **Egypt:** 0.0698625848 (2022), 0.0675552617, … . Matches the CSV.

### 3.4 incf: income-dependent factor on GDP elasticities

1. **Copied:** `Mitigation!L..AE2433`.
2. **Chain:**
   * `L2433 = IF($E2425, L2432/$G2432, 1)`. `E2425 = IF(D2425="Yes*",1,0)`, with `D2425 = IncElAdj` (ScenarioDefinition F262 = Dashboard L24 = "Yes*"). `G2432 = 0.74` (typed).
   * `L2432 = MAX(0, 0.012019x⁴ − 0.365464x³ + 4.011846x² − 18.722243x + 31.59949 + 0.16)`, with `x = L2431 = MIN(10, LN(L2429))`.
   * GDP per capita, `$ per capita`:
     * 2022: `L2429 = L2442/L2428*10^3` (not lagged).
     * Later years: `M2429 = L2443/L2428*10^3` (previous year's post-policy GDP / previous year's population).
   * `L2443 (GDP post) = K2442*(1+L2446)`. `L2446 = L2444 + L2445`, where L2444 = row 480 = row 463 × F287 and L2445 = endogenous change K8288 (0 in the baseline). `L2442 (GDP pre) = L$465`.
   * Row 465 (USD bn, ResultsYear constant prices):
     * J and K (2020–2021): `= CHOOSE($E$460, J423, J423, J443)` = row 422 × row 467. Row 422 = WEO NGDP (LCU bn, row 424) / WEO XDC_USD.PA_RT (row 432). Row 467 = CHOOSE(H467, row 453, row 418); with DfSelection "World" this is row 453 = USA NGDP_D(ResultsYear) / USA NGDP_D(y).
     * From L: `= K465*(1+L463)`, with `L463 = CHOOSE($E$460, L420, 'Manual inputs'!J231, L441)`. E460 = MATCH(GDPScenario "WEO*", {"WEO","Manual","SSPs"}, 0) = 1.
   * Row 420 = WEO NGDP_RPCH/100 up to the WEO last year (2031), extrapolated after that. `F287 = CHOOSE(MATCH(GdpAdj,{"Low","Base","High"},0), 50%, 100%, 150%)` = 1, with GdpAdj = Dashboard V20 = "Base*" (the * acts as a wildcard).
   * Row 428 population = WEO LP.A (millions), extrapolated `prev*(1+growth)`.
   * WEO lookups: `INDEX(WEO!$C$9:$AU$3333, MATCH(iso&"."&code, WEO!$D$9:$D$3333, 0), MATCH(year, WEO!$C$9:$AU$9, 0))`.
3. **Country-specific:** yes (WEO GDP and population).
4. **Egypt:** 1.0271517247 (2022), 1.0271517247 (2023), 1.0205698359, … , 0.9460252655 (2041). Matches the CSV.

### 3.5 shock: exogenous shock on energy consumption

1. **Copied:** `Mitigation!L..AE2439` (`= L$483` …).
2. **Chain:**
   * Row 483: L (2022) is empty (0). M483 = E478 (2023) and N483 = F478 (2024). O483 onwards are empty (0).
   * `E478 = IF(M479=FirstYearCalculations+1, IFERROR(INDEX(GHGs!$G$1202:$G$1388, MATCH(_Country_code, GHGs!$B$1202:$B$1388,0)),"0%"), 0)`. The test is always true. The fallback is the text "0%".
   * `F478 = IF(N479=FirstYearCalculations+2, IFERROR(INDEX(GHGs!$H$1202:$H$1388, …),0%),0)`.
   * GHGs!G1202:H1388 are typed calibration values, with key `GHGs!B` = ISO (B = INDEX(Countries!D, MATCH(name D, Countries!C))). Egypt is row 1224: G = −0.2081330830, H = 0.0923714286.
3. **Country-specific:** yes (GHGs).
4. **Egypt:** 0, −0.20813308302, 0.09237142857, then 0 to 2041. Matches the CSV.

### 3.6 pret|<t>: planned retirement, nameplate MW

1. **Legacy:** coal only, `Mitigation!L..3992`. The script writes zeros for all techs. `L3992 = IF(L3991="DoNotUse", L3932*$J4011, INDEX(Power!$G$1750:$BD$1878, $I3992, L3990))`, with `L3990 = MATCH(L3989, Power!$G$1749:$BD$1749, 0)` (2022 → 22 → column AB).
2. **Data:** the Power averaged block 1750–1857 (5-year centred mean of the raw block 1639–1746: `H1750 = AVERAGE(F1639:J1639)` …). When the data are not used, legacy row 3992 holds the exponential retirement (capacity × rate), which is **not** the planned-retirement series.
3. **Country-specific:** yes (coal only).
4. **Egypt:** the data row (Power 1774) is all 0. The legacy row 3992 is 0 because coal capacity = 0. The CSV holds 0 everywhere, which is consistent.

---

## 4. PowerParams items (power_params.csv)

| Key | Copied cell | Chain to data | Country? | Egypt (CSV = legacy) |
|---|---|---|---|---|
| tmc\|res | Mitigation!L3599 | `=ResidentialTransmissionCost` = **Power!G20** | no | 0.04 |
| tmc\|ind | Mitigation!L3628 | `=IndustrialTransmissionCost` = **Power!G21** | no | 0.015 |
| pass | Mitigation!L3596 | `=$J3596`; `J3596 = PowerSectorPriceChangePassOn` = ScenarioDefinition F343 = **Dashboard!L51** | no | 1.0 |
| gen_per_cons | Mitigation!I3723 | `=1+SUM(I3719:I3722)`; telescopes to **L3748/L3741** = generation (ktoe) / final power demand (ktoe), see below | yes (Balances) | 1.2211686765 |
| dlf_ren | Mitigation!L3883 | `=AVERAGE($G3030:$G3031)` (section 1.5: wnd and sol annuity sums with country WACC) | yes (CoC) | 8.4350367257 |
| st_alloc | Mitigation!E3871 | `=ScenarioDefinition!F$388` (AllocateSTStorageToVRE) = **Dashboard!V190** | no | 1.0 |
| st_marg_hours | Mitigation!E3873 | `=2*E3872`; `E3872 = ScenarioDefinition!F$389` (TotalHoursStorageFor100pcVRE) = **Dashboard!V191** (9) | no | 18 |
| st_ratio | Mitigation!E3874 | `=ScenarioDefinition!F$390` (StorageToInterfaceRatioSTStorage) = **Dashboard!V192** | no | 2 |
| lt_start | Mitigation!E3877 | `=StartingPointWhenLTStorageIsNeeded` = ScenarioDefinition F393 = **Dashboard!V194** | no | 0.75 |
| lt_alloc | Mitigation!E3876 | `=ScenarioDefinition!F$392` (AllocateLTStorageToVRE) = **Dashboard!V193** | no | 0.33 |
| sh_nxp | Mitigation!I3719 | `=IF(L3741=0,0,L3742/L3741)`; `L3742 = F3719 = −SUM($E$503,$G$503)` = −(imports + exports) of Balances `ecy` | yes | 0.0092445306 |
| sh_tsd | Mitigation!I3720 | `=L3743/L3741`; `L3743 = F3720 = −SUM($N$503,$O$503,$Q$503)` = −(statdiff + transfer + distloss), ecy | yes | 0.1899579758 |
| sh_eou | Mitigation!I3721 | `=L3744/L3741`; `L3744 = F3721 = −$P$503` = −ownuse, ecy | yes | 0.0381940028 |
| sh_add | Mitigation!I3722 | `=L3745/L3741`; `L3745 = L3748 − SUM(L3741:L3744)` (residual) | yes | −0.0162278327 |
| extra_eff | Mitigation!M3719 | `=M2198`; `M2198 = ScenarioDefinition!$F$242` (AdditionalEfficiencyPower) = **Dashboard!L134** | no | 0 |
| maxcf_cg | Mitigation!L3783 | `=MaximumCoalCF` = ScenarioDefinition F372 = **Dashboard!G192**. Gas has its own `L3784 = MaximumGasCF` (F373 = G193, also 0.9); the CSV keeps one value | no | 0.9 |
| k_dispatch | Mitigation!M3720 | `=kDispatch` = ScenarioDefinition F346 = **Dashboard!G190** | no | 2 |
| k_invest | Mitigation!M3721 | `=kInvestment` = ScenarioDefinition F347 = **Dashboard!Q190** | no | 2 |
| min_cost | Mitigation!K3463 | `=MinPostSubsidyPowerPrice` = ScenarioDefinition F351 = **Dashboard!L192** | no | 0.01 |
| early_max | Mitigation!J3975 | **typed constant 0.8** (not linked to MaxCostBasedEarlyRetirement) | no | 0.8 |
| early_factor | Mitigation!F3993 | `=IF(C2173=1, IF(EarlyRetirementInBaseline="Yes", MaxCostBasedEarlyRetirement, 0%), MaxCostBasedEarlyRetirement)`; F379 = **Dashboard!Q52** ("Yes"), F378 = **Dashboard!Q51** (0.8) | no | 0.8 |
| ktoe_gwh | (script constant) | legacy `_conv_ktoe_to_gwh` = Mitigation!E1033 = 11.63 (typed) | no | 11.63 |

**gen_per_cons and sh_* details (base year L = 2022):**

* **L3741, total final power demand (ktoe):** `=SUM(L3725:L3739)`, with `L37xx = E37xx`.
  * `D3725:E3738 = TRANSPOSE(_Power_Use_Formatted)`, where `_Power_Use_Formatted = Mitigation!G582:T583`.
  * `E3739 = $V$583`.
  * `G583..T583 = IF($C$578, E531..R531, …)` and `V583 = T531`.
  * Row 531 = Balances `ecy` (C503) for the flows in `E529:R529, T529`: road, rail, domesair, domesnav, resident, food_forest, services, mining_chemicals, ironstl, nonferrmet, machinery, cement, other_manufact, construc, plus ononspec. Excluded: U583 (fuel transformation / own use) and nonenuse.
  * Egypt: 15495.7198104.
* **L3748, actual generation (ktoe):** `=L3751/_conv_ktoe_to_gwh`; `L3751 = L3754/_conv_gwh_to_mwy`; `L3754 = L3813 = SUM(L3804:L3812)`; `L3804+i = M(A4 row)` (gen0). In short: Σ gen0 (MWy) × 8.76 / 11.63. Egypt: 18922.8876526.
* `I3722 = (L3748 − L3741 − L3742 − L3743 − L3744)/L3741`, so `I3723 = L3748/L3741` exactly.
* The `BalancesOrConsumption="Consumption"` branch (ScenarioDefinition F234 = Dashboard G136; Egypt = "Balances") would take the shares from `J3719:J3721 = $H$573:$H$575` instead.

---

## 5. Legacy **Power** tab layout (copy at the same cell addresses)

Values are typed except where noted. Code keys are always in **column A** (lower-case); a copy of old data sits to the right (columns Q/R..AA, "OLD DATA"; not used). All lookups that A2, A7 and A14 make use `MATCH(code, Power!$A$25:$A$356, 0)` with `INDEX(Power!<col>$25:<col>$356, idx)`, so rows 25–356 must keep their exact positions, **including the regional block and the order of duplicates**.

| Block | Rows | Title / header | Key column and code pattern | Value columns | Used by |
|---|---|---|---|---|---|
| Year header | 1 | F1:BD1 = 2000..2050 | — | — | — |
| Overview | 2–14 | text (A data section, C method, K unit, N level, P source) | — | — | — |
| Misc. parameters | 15–23 | title A15, A16 "Global level", header row 19 (B Quantity, D Sector, E Source, F Unit, G Value) | rows 20–23 by position | G20 res T&D 0.04 (`ResidentialTransmissionCost`); G21 ind T&D 0.015 (`IndustrialTransmissionCost`); G22 nuclear fuel 0.004 (not linked); G23 `=ROUND(AVERAGE(#REF!),2)` (broken, unused) | tmc\|res, tmc\|ind |
| RE scale-up categories | 19–23 | I19 header; I20:I23 = Low, Medium*, High, Vhigh | position | J20:J23 = .01 .02 .03 .04 | scaleup (wnd, sol) if category ≠ CtryDefault |
| WACC by income | 18–23 | M18 "WACC Assumptions (user set)", M19/N19 header | M20:M23 = HIC, UMIC, LMIC, LIC | N20:N23 = .075 .1 .125 .15 | `IncomeDepWACC` (Mitigation!S82), only if WACCSource="Income*" |
| mpp world | 25–39 | title A25, A26 "Global level", **header row 27**: B Item Code, C CPAT World Code, D Tech, E CapacityFactor, F CapEx.USD_kW, G Efficiency.NCV, H OpexFixed.USD_kW_y, I OpexVariable.USD_kWh, J WACC, K TotalLifetime, L Construction | A28:A39 `wld.mpp.<t>`, t = coa nga oil nuc hyd wnd sol ore bio eys bat bat-int (rows 28..39) | E..L | A2 (L, M indices) |
| mpp regional | 40–109 | A40 "Regional level", header row 41 (C CPAT Region Code; E..J as above) | A42:A109 `<reg>.mpp.<t>`, reg ∈ {nac, chn, eas, ecs, jpn, kor, lcn, mea, sas, ssf} (name `reg_mpp` = A41:BD109) | E..J | not deliberately; **shadows** the country codes chn, jpn and kor (bug) |
| mpp country | 110–294 | A110 "Country level", header row 111 (C CPAT Country Code; J "WACC (Not used)", K "TotalLifetime (Not used)") | A112:A294 `<iso3>.mpp.<t>` (63 countries; name `mpp_cntr` = A112:BD299). Egypt: A166 `egy.mpp.nga`, A230 `egy.mpp.sol` | E..K (sparse; a blank or 0 means "use world") | A2 (K index) |
| Capex time factor (ctf) | 300–330 | A300 title, row 301 "Global level", **header row 302**: B Item Code, C world, D Scenarios, E tech, **F302:BD302 = 2000..2050** (`CapexTimeFactorYearRange`) | A303:A330 `=C&"."&B&"."&D&"."&E` → `wld.ctf.<scen>.<t>`, scen ∈ {low, med, hgh, vhg, oldlow, oldmed, oldhgh, oldvhg}; `wld.ctf.med.ore` is duplicated (316, 318). Name `reg_ctf` = A302:BE343 | F..BD by year (index 2020 = 1) | A7 (tcf) |
| Yearly change sol/wnd | 331–340 | helper (D category, E tech, F hist avg, G.. formulas) | — | — | feeds the ctf rows |
| Decommissioning & transmission (dtc) | 344–354 | A344 title, **header row 345**: B Item Code, C world, D tech, E Decommissioning costs (share of capex), F Transmission costs (share of capex) | A346:A354 `wld.dtc.<t>`, t = coa nga oil nuc wnd sol hyd ore bio; E353:E354 `=AVERAGE(E346:E352)` | E, F | A14 (dtc), A15 (tcx) |
| Installed capacity | 355–1635 | A355 title, **header row 357**: B "ic", C Code, D CountryCode, E FuelType, **F357:AC357 = 2000..2023** | **column C** `<iso3>.<t>`, t = coa nga oil nuc wnd sol hyd ore bio (9 rows per country; Egypt C691:C699). Name `instcap_cntr` = A358:BD1635 | F..AC MW | A4 col N (broken: range F:Y) |
| Planned retirement, raw (coal) | 1636–1746 | A1636 title, A1637 source, **header row 1638**: D CountryCode, E CountryName, F1638:AT1638 = 2000..2040 | **column D** ISO3 upper-case (Egypt D1663). Name `cpp_retir` = A1639:BD1746 | F..AT MW/y | feeds the averaged block |
| Planned retirement, averaged | 1748–1857 | A1748 title, **header row 1749**: D CountryCode, E CountryName, **F DataAvailable**, G1749:AT1749 = 2001..2040 | **column D** ISO3 (Egypt D1774). All formulas: `D=D1639`, `F=IF(AVERAGE(Z:AJ)<0.1,"No","Yes")`, `H1750=AVERAGE(F1639:J1639)` … (G typed 0). Name `avg_data_cntr` = A1750:BD1857 | F flag; G..AT MW/y | K5 (planned_retirement, pret) |
| Battery storage | 1882–1911 | A1882 title; **row 1883 years F:BD** (`Z1883 = 2020` typed, the rest ±1 formulas); rows 1884–1895 € values (C tech, D item, E unit); D1896 2015 EUR→USD 1.085, D1897 2021 EUR→USD 1.18; row 1898 years; rows 1899–1911 $ values (formulas) | by **position**: 1899 Battery Capex $/kWh, 1900 Battery OpexFix, 1901 OpexVar, 1902 Lifetime, 1903 Batteryinterface Capex $/kW, 1904–1906 its OpexFix, OpexVar, Lifetime, 1907 WaterElectrolysis Capex, 1908 OpexFix, 1909 VariableOpex, 1910 Lifetime, 1911 StorageTank Capex $/kWh | F..BD by year | J2 (cbat, cint, obat, cel) |
| Max/avg RE growth | 1917–2335 | header row 1921: A Code, B CountryCode, C FuelType, D AveGrowthMW, E MaxGrowthMW, F TotalCap, G..J rates; H1919 = `MinimumGrowthRateRenewables` | A `=B&"."&C` → `<iso>.<sol\|wnd>`; `wld.sol` and `wld.wnd` at 2334–2335 (names `_AvGrowthRate_World_*`). Name `max_avg_cap_inc` = A1921:BD2335 | D..J | engineer-model scale-up (not one of these items) |
| VRE max invest (gen share add) | 2343–2570 | A2343, A2344 titles; header row 2348: A Economy, B Code (ISO3 upper), C historical country max RE scale-up rate | **column B** ISO3 (Egypt row 2408) | C (0.02 default; CHN and IND 0.03) | scaleup_rate wnd/sol (CtryDefault*) |
| sol_wind by carbon-price band | 2572–4792 | header row 2572: A Code, B CountryCode, C FuelType, D CarbonPriceLevel, E2572:Z2572 = 2019..2040 | A `=LOWER(B)&"."&C&"."&D` → `<iso>.<sol\|wnd>.<band>`. Name `sol_wind` = A2573:BD4792 | E..Z | Mitigation L4126:L4127 (dead code for these items) |
| Previous WACC | 4795–4985 | A4796 Country, B Region, C Default WACC | name | C | unused |

---

## 6. Legacy **CoC** tab, WACC block used by A3 (copy rows 200–390 at the same addresses)

* **Title:** A200 ">>> Real WACC". **Header row 201:** A Country, B Country_Code, C S&P, **D201:V201 = 2022..2040**, X201 "Tech Adjustment".
* **Rows 202–390** (189 countries, alphabetical): A name, **B ISO3 upper-case (lookup key)**, C rating (or "Not Found").
  * **D..V**: real WACC by year. The model uses only **D (2022)**. Egypt is row **253**: D253 = 0.09947642998297449.
  * These are `LET` formulas (the WACC calculator): `rf + β·(ERP_US + CRP)` weighted by the equity share, plus `(rf + default spread + lender margin)·(1−tax)·(1−equity share)`.
    * rf = `XLOOKUP(year, A24:A34, C24:C34)` (real risk-free rate).
    * β, CRP, default spread, tax, equity weight and lender margin = `XLOOKUP(code, B41:B197, H/F/D/G/I/J41:197, <row 172>)`.
    * ERP_US = E192.
  * Countries missing from the fixed data (65 rows, C = "Not Found") get **row 172 (Sri Lanka)** parameters through the if_not_found argument (for example AFG = LKA = 0.177883…).
  * From M (2031) onwards the values repeat the previous year. Copy D202:V390 as values, or copy the calculator rows 18–197 as well.
* **Tech adjustment table:**
  * X202 "(CPAT) Tech", Y202:AB202 = HIC, UMIC, LMIC, LIC (income keys).
  * X203:X211 = bio, nga, coa, ore, hyd, sol, oil, nuc, wnd (tech keys).
  * **Y203:AB211** = additive adjustments (typed). Example LMIC column AA: .03215 .02465 .02465 .04425 .02725 .02935 .02465 .02725 .02935.
* **Lookups used:** country `XLOOKUP(LOWER(iso), CoC!$B$202:$B$390, CoC!$D$202:$D$390, 0.075)` (0.075 when the country is missing). Tech adjustment `XLOOKUP(tech, CoC!$X$203:$X$211, XLOOKUP(income, CoC!$Y$202:$AB$202, CoC!$Y$203:$AB$211))`. The "Country*" option uses `CoC!$Y$205:$AB$205` (coal row) for every tech.
* **Calculator inputs, if the formulas are wanted:** rows 22–36 time data (A year, B nominal yield, C real rf = `EXP(LN(1+B)−LN(1+$F$24))−1`, D US deflator, F24 = `(D31/D24)^(1/7)−1`); rows 40–197 fixed data (A country, B code, C region/income, D default spread, E ERP, F CRP, G tax, H β, I equity weight, J lender margin; some B/C/H/I cells are `=#N/A`).

---

## 7. Other data tabs and settings touched

* **Balances** (copy as is): A13:Z13 header (country_code, country, year, measure, flow_code, ecy, coa, nga, oop, gso, die, ker, lpg, jfu, wnd, sol, hyd, ore, nuc, bio, hea, totren, bgs, bdi, obf, total). Data rows 14..4044, keyed by **A (ISO3) & E (flow_code)**; one year per country. Units: ktoe, except `eloutput` (gwh).
  * Flows used: imports, exports, statdiff, transfer, ownuse, distloss, power, eloutput, and the 15 demand flows of section 4.
* **Countries:** C6:C227 name, D6:D227 ISO3, F region, G WB income group, **H6:H227 income code** (formula from G), N GHG region, P euro flag.
* **GHGs:** rows 1201–1388. B ISO3 (formula), G1201 = FirstYear+1 (2023), H1201 = 2024. **G1202:H1388 typed shocks.**
* **WEO:** row 9 header (A last year, B ISO, C dataset, D series code `ISO.INDICATOR`, E country, F indicator, G9:… = 2000..). Data rows 10..3333. Used for incf: LP.A, NGDP.A, NGDP_D.A, NGDP_R.A, NGDP_RPCH.A, XDC_USD.PA_RT.A, plus usa.NGDP_D.A.
* **Mitigation constants used:** K710:AE710 (uranium 0.004), E1033 (11.63), E1044, E1045, J3975 (0.8), G2432 (0.74), A4 P3003:P3006 (1.0).

**Dashboard settings in the chains** (all through ScenarioDefinition!F = ScenarioDefinition!E = Dashboard; cached values):

| Name (ScenarioDefinition row) | Dashboard cell | Value |
|---|---|---|
| _Countryname (F8) | E2 | Egypt |
| _Country_code | D644 (formula `VLOOKUP(_Countryname, Countries!$C$6:$D$227,2,FALSE)`) | EGY |
| FirstYearCalculations (F232) | G134 | 2022 |
| BalancesOrConsumption (F234) | G136 | Balances |
| AdditionalEfficiencyPower (F242) | L134 | 0 |
| GdpAdj (F259) | V20 | Base* |
| IncElAdj (F262) | L24 | Yes* |
| GDPScenario (F222) | Q20 | WEO* |
| ResultsYear (F233) | G135 | 2026 |
| DfSelection (F296) | G142 | World |
| PowerSectorPriceChangePassOn (F343) | L51 | 1 |
| kDispatch (F346), kInvestment (F347) | G190, Q190 | 2, 2 |
| MinimumWACC (F348) | Q193 | 0.01 |
| HydroDoesntRetire (F350) | V198 | Yes |
| MinPostSubsidyPowerPrice (F351) | L192 | 0.01 |
| RenewableSubsidyBL (F354) | L55 | 0 |
| MaxNonVREAsPCOfTotalGen (F359), MaxNonNucOreBioAsPCOfTotalGen (F360), MaxWindSolarScaleup (F361) | Q194, Q195, Q196 | .05, .02, .05 |
| MaxScaleUpRateCategory (F362) | G53 | CtryDefault* |
| WACCSource (F365) / D_WACCSource | Q191 | Tech |
| WACCUserGlobal (F366) | Q192 | 0.075 |
| RenewableCostDeclineRate (F367) | G52 | Medium* |
| MaximumCoalCF (F372), MaximumGasCF (F373) | G192, G193 | .9, .9 |
| CFOverrideIfBelowWndSol (F375), …FosOth (F376), CFOverrideIfAbove (F377) | G196, G197, G198 | .1, .01, 1 |
| MaxCostBasedEarlyRetirement (F378), EarlyRetirementInBaseline (F379) | Q51, Q52 | 0.8, Yes |
| MinimumThermalEfficiency (F380) | G194 | 0.1 |
| AllocateSTStorageToVRE (F388), TotalHoursStorageFor100pcVRE (F389), StorageToInterfaceRatioSTStorage (F390) | V190, V191, V192 | 1, 9, 2 |
| AllocateLTStorageToVRE (F392), StartingPointWhenLTStorageIsNeeded (F393), LongTermStorageFor100pcVRE (F394), StorageHoursForLTStorage (F395) | V193, V194, V195, V196 | .33, .75, 1, 1000 |
| NewInvCoa..NewInvBio (F397:F405) | U51:U59 | If Present* (wnd, sol: Yes) |
| NewInvCoaYear..NewInvBioYear (F407:F415) | V51:V59 | 2022 2022 2022 2030 2022 2022 2030 2030 2022 |

---

## 8. Legacy bugs and oddities in these chains

1. **A2 rows 2981–2985 (wnd, sol, hyd, ore, bio), columns P..T:** the `IF(ISERROR(INDEX(K)),INDEX(K),IF(ISERROR(INDEX(L)),INDEX(L),INDEX(M)))` logic is inverted, so the result is always the world value. Country efficiency, fixed opex, variable opex, WACC and lifetime for these techs are ignored. Egypt: solar fixed opex uses 15 instead of the country 11.831, which changes opf|sol.
2. **A4 column N (installed capacity):** the column range `Power!$F$357:$Y$357` (2000–2019) does not contain FirstYearCalculations (2022, column AB), so N = #N/A. Actual capacity factors are never used; CF = study values, and the CFOverride bounds are dead.
3. **Hydro investment start (H4067):** `IF($L$3827>50%, …)` tests a year header (2022 > 0.5), so hydro always starts in the first year (2022 instead of NewInvHydYear = 2030).
4. **Regional/country code shadowing:** MATCH over `Power!A25:A356` finds the regional rows (42–109) first for `chn.mpp.*`, `jpn.mpp.*` and `kor.mpp.*`. For China, Japan and Korea, region data replace country data (18 codes).
5. **A7 country ctf code** `iso.med.ctf.t` uses a different segment order from the world code `wld.ctf.med.t`, and there are no country/regional ctf rows, so the country branch is dead.
6. **D2 nuclear fuel:** `L3353 = K2727` (shifted one column: 2022 takes the 2021 value). The value is the typed constant Mitigation!K710:AE710 = 0.004, not Power!G22. No numeric effect.
7. **A15 (tcx)** uses A14's helper `$K3110` instead of `$K3121` (same value). A15 is labelled "not used in the model at all".
8. **K5 planned-retirement probe:** `INDEX(Power!$D$1749:$BD$1878,$I3992,L3990)` is offset by one row and three columns from the data range `G1750:BD1878`; the flag J3991 uses `F1750:F1857` while the MATCH uses `D1750:D1878`. Harmless today.
9. **CoC:** countries without fixed data silently get Sri Lanka's parameters (row 172) as the XLOOKUP if_not_found. Countries absent from CoC rows 202–390 get 0.075 + the tech adjustment.
10. **WACC is time-invariant:** only CoC column D (2022) is used, although D:V hold 2022–2040.
11. **"Country\*" WACC option** applies the coal adjustment (CoC row 205) to every tech.
12. **early_max (J3975 = 0.8) is typed** and not linked to MaxCostBasedEarlyRetirement (0.8 today). The label says "80%".
13. **Power!G23** `=ROUND(AVERAGE(#REF!),2)` is broken (unused).
14. **shock:** the IFERROR fallback in E478 is the text `"0%"`; the IF test `M479=FirstYearCalculations+1` is always true.
15. **incf:** the 2022 GDP per capita uses the current year (`L2429 = L2442/L2428`) while later years are lagged. Post-policy GDP `L2443 = K2442*(1+L2446)` rebases on the previous **pre-policy** level, so endogenous GDP changes do not accumulate (zero in the baseline).
16. **Balances lookup ignores the year column.** Only one year per country is allowed in the Balances tab.
17. **A2 N column range** `Power!E$25:E$355`, while the other columns use `:356`. No effect.

---

## 9. Summary table

Notation: `iso` = LOWER(country code); `idxC(t)` = `IFERROR(MATCH(iso&".mpp."&t, Power!$A$25:$A$356,0), idxW(t))`; `idxW(t)` = `MATCH("wld.mpp."&t, Power!$A$25:$A$356,0)`; `PC(col,t)` = `IF(INDEX(Power!col$25:col$356,idxC)>0, INDEX(..,idxC), INDEX(..,idxW))`; `PW(col,t)` = `INDEX(Power!col$25:col$356, idxW)`; `P*(col,t)` = PC for coa, nga, oil, nuc and PW for wnd, sol, hyd, ore, bio (legacy bug replicated); `BAL(flow,fuel)` = `INDEX(Balances!$A$13:$Z$4044, MATCH(ISO&flow, Balances!$A$13:$A$4044&Balances!$E$13:$E$4044,0), MATCH(fuel, Balances!$A$13:$Z$13,0))`.

| Item | Data source | Country-specific? | Formula sketch |
|---|---|---|---|
| cax0_usd_per_kw | Power F (mpp) | yes (country mpp row, else world) | `PC("F",t)` |
| life_years | Power K | coa..nuc only (if country K) | `P*("K",t)` |
| efficiency | Balances, fallback Power G | yes | `IFERROR(IF(g/i<MinTE, P, g/i), P)`; g = BAL("eloutput",f)·1000/8760, i = −BAL("power",f)·11.63·1000/8760 (oil = Σ oop..jfu); P = P*("G",t) for coa, nga, oil, nuc, bio and 1.0 for wnd, sol, hyd, ore |
| capacity_factor | Power E | only via a country E | `PC("E",t)` (actual-CF branch dead) |
| wacc | CoC D202:D390 + Y203:AB211, Countries H | yes | `IFERROR(XLOOKUP(iso,CoC!$B$202:$B$390,CoC!$D$202:$D$390,0.075),0.075)+XLOOKUP(t,CoC!$X$203:$X$211,XLOOKUP(inc,CoC!$Y$202:$AB$202,CoC!$Y$203:$AB$211))` |
| dtc_usd_per_kw | Power E346:E354 × capex | via capex | `INDEX(Power!$E$25:$E$355,MATCH("wld.dtc."&t,Power!$A$25:$A$356,0))*cax0` |
| tcx_usd_per_kw | Power F346:F354 × capex | via capex | same with column F |
| opf_usd_per_kwh | Power H, CF | via H (coa..nuc) and CF | `P*("H",t)/(8760*CF)` |
| vop_usd_per_kwh | Power I | coa..nuc | `P*("I",t)` |
| fuel_fixed_usd_per_kwh | Mitigation K710 (typed) | no | nuc: 0.004; others 0 |
| rns_usd_per_kwh | script | no | 0 |
| cap0_mw | Balances, CF | yes | `gen0/CF` |
| gen0_mwy | Balances eloutput | yes | `BAL("eloutput",f)*1000/8760` |
| retire_rate | lifetime | effectively no | `1/life`; hyd `IF(HydroDoesntRetire="Yes",0,1/life)` |
| invest_permitted | Dashboard U51:U59, cap0 shares | yes | `IF(set="If Present*",IF(cap0/SUM(cap0)>0.001,"Yes","No"),set)` |
| invest_start | Dashboard V51:V59 | no | `NewInv<T>Year`; hyd = FirstYearCalculations (bug) |
| scaleup_rate | Dashboard Q194/Q195/G53, Power B2349:C2570 | wnd/sol (CtryDefault*) | coa, nga, hyd: Q194; oil, nuc, ore, bio: Q195; wnd, sol: `INDEX(Power!$C$2349:$C$2570,MATCH(iso,Power!$B$2349:$B$2570,0))` (or J20:J23 / Q196 per G53) |
| planned_retirement | Power F1750:F1857 | yes (coal) | coa: `INDEX(Power!$F$1750:$F$1857,MATCH(ISO,Power!$D$1750:$D$1878,0))`; others "No" |
| price_code, vre, vre_share, dispatch, code, name | script | no | constants |
| tcf\|t (path) | Power ctf F303:BD330 | no | `INDEX(Power!$F$25:$BE$597,MATCH("wld.ctf."&scen&"."&t,Power!$A$25:$A$356,0),MATCH(y,Power!$F$302:$BD$302,0))` |
| cbat / cint / obat | Power 1899 / 1903 / 1900 | no | `INDEX(Power!$F$1899:$BD$1899,1,MATCH(y,Power!$F$1883:$BD$1883))` etc. |
| cel | Power 1907, 1908, 1909, 1911; dlf | yes (via WACC) | `(P1907(y)+P1911(y)*StorageHoursForLTStorage)/(dlf*8760)+P1908(y)/8760+P1909(y)` |
| incf | WEO (GDP, population) | yes | `IF(IncElAdj="Yes*",MAX(0,poly(MIN(10,LN(gdppc))))/0.74,1)`; gdppc = USD GDP (row 465 chain) / population, lagged one year from 2023 |
| shock | GHGs G1202:H1388 | yes | 2023: `IFERROR(INDEX(GHGs!$G$1202:$G$1388,MATCH(ISO,GHGs!$B$1202:$B$1388,0)),0)`; 2024: column H; else 0 |
| pret\|t | Power G1750:BD1878 (coal) | yes | coa: `INDEX(Power!$G$1750:$BD$1878,MATCH(ISO,Power!$D$1750:$D$1878,0),MATCH(y,Power!$G$1749:$BD$1749,0))` when used; others 0 |
| tmc\|res, tmc\|ind | Power G20, G21 | no | `=Power!G20`, `=Power!G21` |
| pass | Dashboard L51 | no | setting |
| gen_per_cons | Balances | yes | `(SUM(gen0)*8.76/11.63)/SUM(BAL(demand flows,"ecy"))` |
| dlf_ren | CoC (WACC), lifetimes | yes | `AVERAGE over t∈{wnd,sol} of (1-(1/(1+wacc_t))^life_t)/(1-1/(1+wacc_t))` |
| st_alloc, st_ratio, lt_alloc, lt_start | Dashboard V190, V192, V193, V194 | no | settings |
| st_marg_hours | Dashboard V191 | no | `2*V191` |
| sh_nxp | Balances ecy | yes | `-(BAL("imports","ecy")+BAL("exports","ecy"))/D` |
| sh_tsd | Balances ecy | yes | `-(BAL("statdiff")+BAL("transfer")+BAL("distloss"))/D` |
| sh_eou | Balances ecy | yes | `-BAL("ownuse","ecy")/D` |
| sh_add | Balances | yes | `gen_per_cons-1-sh_nxp-sh_tsd-sh_eou` |
| extra_eff | Dashboard L134 | no | setting |
| maxcf_cg | Dashboard G192 (gas G193) | no | setting |
| k_dispatch, k_invest | Dashboard G190, Q190 | no | settings |
| min_cost | Dashboard L192 | no | setting |
| early_max | Mitigation J3975 (typed) | no | 0.8 |
| early_factor | Dashboard Q51, Q52 | no | `IF(baseline,IF(Q52="Yes",Q51,0),Q51)` |
| ktoe_gwh | constant | no | 11.63 |

(D = total final power demand, ktoe = Σ Balances `ecy` over road, rail, domesair, domesnav, resident, food_forest, services, mining_chemicals, ironstl, nonferrmet, machinery, cement, other_manufact, construc, ononspec.)
