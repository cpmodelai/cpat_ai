# v9.0 group R6R10: residential exempt split, producer subsidies, Manual inputs, electricity subsidies and power memos, road biofuels, aviation and navigation renewables, range anxiety (changes for the integrator)

Spec: `Equations_addendum.md` section E (R6-R10), notes section E. Built in `build.py` (Settings, Inputs_prices,
Inputs_power, Inputs_ela, Manual inputs notes, sections 1-3, 5b, 6b, 11, 14), `check_full.py` (in step where it
covers the rows), new script `ra_goalseek.py`, new data `data/range_anxiety_fit/range_anxiety_fit.csv`.
Includes the hand-off of the power agent (POW465): the price-chain residual of legacy rows 3607/3636 (R9.3a-b).

## 1. What is built

### R6 Residential initially-exempt demand (as legacy)
- R6.1 (I137): Settings C65 `CookFuel` = WHOCooking code, `"lpg"` if missing (legacy L1784 IFNA). `check_full` too.
- R6.3 (I136): Settings row 82 = the basket row (`<ISO>.distn.bsh.bkt.ove.mean.`&BasketQ: budget share x
  cons_pc_acrent x popw); C83 `ExemptCookShare` = spend of the exempt deciles / economy-wide spend of the basket, x D82
  (1 if the fuel is nga, lpg or ker, else 0).
- R6.7 (I138): `lkd` (LEAKCHANGE) on last year's not-exempt use: `INDEX(res ener, t-1) - lkx(t-1)`.
- lkxp, lkx, lkxa unchanged (R6.4-R6.6). Egypt: ExemptMostCook = No, so no change of results.

### R7 Producer subsidies with their price effect (as legacy)
- R7.1: `psu.<f>` after the last price year = last value x `psf.<f>` (PRODSUBUNIT gets the factor; legacy O2455 =
  $J2456 x O2213); the block row `psp` (unchanged code; it is the legacy "in which: producer-side subsidies" row, now
  phased) enters the supply cost (SUPPLYCOST unchanged), so E21-E23 and the price controls absorb (1 - pass-through).
  The addendum's new code `psb` is not added: `psp` is that row (no second copy).
- R7.3: rows removed: policy rows `psr.<f>`, block rows `ppsw`, subsector rows `psw` (codes gone: 320 = 288 psw +
  24 ppsw + 8 psr); `atp`, `rvt`, `rsr` (no psw VAT term), `pvatn` (SUM(pctx:ppcw)) adjusted; LAMBDAs PSREFORM,
  PSWEDGE removed. rpsu unchanged (R7.4).
- Electricity (sub-table G2 of section 3, rows per user group res/ind): `rpnv` (data price before VAT, held),
  `txg` (price gap before VAT - supply cost - manual excise), `txe` (tax/subsidy of the dataset; R9.1), `scl`,
  `psegap`, `psegs`, `psesh` (R7.5 allocation, fallbacks as legacy IFERROR), `pseu` (R7.6/R7.8 per kWh,
  MAX(PsElFloor, ...), then x `psf.ecy`), `pser` (R7.7 residual, USD m, memo), `rppre` adds pi x change in
  (pseu + csd + ores) x (1 + VAT) (R7.9, R9.3).
- New named constant `PsElFloor` = -0.3 USD/kWh (sheet Constants; legacy H3590:H3591; I146).
- Inputs_power: new columns `tx2021`..`tx2024` (Prices_dom `mit.txo.ecy.<g>` x CPI index, "" where blank), names
  `PwTx`, `PwTxYr`, `PwRp`, `PwRpYr`.

### R8 Manual inputs
- R8.1-R8.2 (I53/I139 replicated): table on Inputs_prices below the notes (rows MP_R0.. , names `MPU`, `MPUYr`,
  `MPUHdr`): one column per code of Manual inputs rows 60-146 (61 codes), Manual inputs row, flag (DomPrTax = Yes and
  a 2021 value), Prices_dom column; block M (manual values, 2021-2026), block U (manual where flagged, else Prices_dom;
  "" where blank). Every historical domestic price lookup reads U: Inputs_prices rpn/spn/txn/vrd/vrb, Inputs_power
  rp (and the new tx; VAT at LastHist), the policy rows `pros.<f>` (param D = column of MPU). New Settings rows
  85-89: C86 `ManPrOn` (DomPrTax), C87 `ElIncMan`, C88 `ElPrcMan`, C89 `ResBioSubst` (moved from the name on
  Elasticities!C131). Names `ManPrKey`, `ManPrVal`, `ManPrYr`.
- R8.3-R8.4: Inputs_ela new columns I:M (Manual inputs row, column, manual value with #N/A for blank (I140), source
  switch, elasticity used: MAX(.,0) income, MIN(.,0) usage/efficiency); `ElaSel` now reads column M. L101 fixed
  (services read column N).
- R8.5: `ResBioSubst` (Settings C89) = Manual inputs L319 when ElPrcMan = 1 (blank: #N/A), else Elasticities C131.
  L220 fixed: Manual inputs L319:L321 = `=Elasticities!G131..G133` (were C91:C93). Only the biomass / LPG value is
  used by the model (the prototype's leakage uses one sigma, as before); kerosene and gasoline/diesel cells placed.
- R8.6-R8.7 (I141; L135 fixed): section 14 block "Methane sources: intensity index" rows `ch4.int.<j>` =
  (1 - rate)^MAX(0, year - GHGYear) (LAMBDA INTDECLINE; rate Manual inputs J185 og/dg/bm, J186 cm, J187 liv/ric, J188
  wst); `ch4.em` and `ch4.emf` (METHSOURCE gets an `intensity` argument) multiply it. `check_full` in step.
- Manual inputs block notes (57-146, 183-200, 271-327) now say "Read".

### R9 Electricity consumer subsidy option and power cost memos
- R9.1 `txe`, R9.2 `csd` (CSELEC: tax x (pof.cs - 1) if tax < 0 and PowerSubsidyExemptInclude = Include, after the
  last price year), R9.3 into `rppre` (above).
- R9.3a-b (POW465 hand-off): `ores` = txg - txe - pseu up to the last price year; then held, a negative one x
  scl / scl(t-1) with `scl` = MIN(sc, sc of the last price year) (= legacy O3607 = J x MIN(sc, J3600)/J3600).
  `check_full` passes `txo_res`, `txo_ind` (dataset tax of LastHist x CPI) to `power_model_ref.engine`.
- R9.4-R9.13: sub-table E2 of section 3 (rows per type): `cur` (INVCOST(lfx, tvc, MinPost)), `sys` (SYSCOST),
  `pcbcap` (LEVCAPEX), `pcbom` (OMCOST), `pcbfu` (VARCOST: fixed fuel + fpp x kwh + xck), `pcbcp` (= ccp), `pcbrns`
  (= rns), `pcbchk` (parts - cur), single `pcbct` (cptraj x (scenario > 1); L222 fixed).
- New MTInputs reads (no new MTInputs rows: both are template rows): `PowerSubsidyExemptInclude` (row 138) and
  `SupplyCostDeltaSubsidy` (row 351), per scenario, as section-1 rows (list `R9_PARAMS`). `CostBreakdownYear` is not
  read (see deviations). CPATScenarios.bas MT_LAST unchanged.

### R10 Road biofuels, aviation and navigation renewables, range anxiety
- Section 5b, new heading and rows (after the range-anxiety fit): parameter rows `trp.bfe` (oil | transport
  elasticities and AEEI, I143), `trp.rne` (renewables | transport, I144), `trp.rn0` (EnergyCons `ren` of avi, nav,
  new read); `trbe.bgs`, `trbe.bdi` (BIOFOLLOW: follow elasticity-model gasoline / diesel, R10.1-R10.2), `trbe.aef`,
  `trbe.obf` (FUELUSE with the road biomass price and shadow price, oil elasticities, R10.3), `trbe.bio` (sum, R10.4);
  `trp.ren` (= tic of solar, R10.5), `trp.renaef`, `ener.avi.ren`, `ener.nav.ren` (FUELUSE, R10.6).
- `ener` of road biomass: ROADSWITCH's elasticity argument is `trbe.bio` (engineer branch unchanged, LD62).
- R10.7: the two renewables rows have variable `ener` (fuel ren), so section 11 totals by subsector and the grand
  total (SUMIFS over the sector sections) include them; the aviation / navigation subsector heading rows and the
  section-5 total add them explicitly; `ener.chk` adds them to the fuel side (no `ren` fuel row in 11).
- R10.8-R10.9: `ra_goalseek.py` (pattern of ets_goalseek.py): secant on the 2025 residual rows `raf.*` (scenario 1),
  each step a LibreOffice recalculation of a working copy with trial values in Transport3 H/N/T; result stored in
  `data/range_anxiety_fit/range_anxiety_fit.csv`; the builder (`ra_fit_apply`) writes the stored values over the
  country's Transport3 cells (bright yellow, data changed by assumption). A goal seek cannot be a formula (the start
  value is read from the base year, the residual is a 2025 result: a later-year read, and the root needs iteration).

## 2. Deviations from the addendum, and why
- `psb` not added: `psp` is the legacy block row of the producer subsidy and now carries the phase-out (R7.1). Wedge
  rows removed rather than kept at 0 (R7.3 allows either).
- Codes differ from the addendum where the addendum code would double count or clash: road biofuels are `trbe.rod.bgs/bdi/obf/bio`
  (not `ener.rod.*`: `ener` rows are summed by SUMIFS into the totals, and `ener.rod.bio` already holds the total);
  `atp.ren` is `trpren.tra.ren` (an `atp` row outside the price blocks); `ps.ecy.sh`, `ps.ecy`, `ps.ecy.res` are
  `psesh`, `pseu`, `pser`; `pcb.cap/om/fuel/cp/rns/chk/ct` are `pcbcap/pcbom/pcbfu/pcbcp/pcbrns/pcbchk/pcbct`;
  `pcb.sys` = `sys`, `pcb.tot` = `cur` (same row).
- E5 cost breakdown: yearly rows (one column per year) instead of a single-year table in CostBreakdownYear: a
  single-year column would read a later year from earlier columns (NORMS 3c: the year selection belongs to the output
  sheets); the CostBreakdownYear value is that year's column. `CostBreakdownYear` therefore not read.
- `scl` replaces the addendum's MIN(sc, sc_L)/sc_L (same value, shorter formulas: ores x scl/scl(t-1) telescopes to it).
- R9.1 fallback (SupplyCostDeltaSubsidy = Yes): price before VAT - supply cost - manual excise (`txg`); the addendum's
  ntx is the manual excise (legacy N3602), as `entx`.
- R7.5 uses the price before VAT (`rpnv` = data retail price / (1 + VAT)) in the gap, consistently with the residual
  (POW465 hand-off: J3607 on the price before VAT).
- Methane intensity starts declining after GHGYear (2024 for Egypt in the prototype data), legacy after 2023 (its own
  inventory year): one year less of decline in every year (2030: x0.9720 vs legacy x0.9674 for agriculture).
- Self-generated renewables base year read from EnergyCons (not the Balances option); Egypt 0.

## 3. Registered bugs said not reproduced in 465 (re-checked in 465 formulas)
- L46 (other road biofuels row): M5406 uses price row 5392, the shadow price in the efficiency term, `_eff_imp_oil_rod`
  and $M2199: not reproduced in 465; built as 465 (I143).
- L47: M5491, M5516 use (1+M2439) like every fuel row: not reproduced; built with the shock row.
- L48: M5568 has the income factor; not reproduced; prototype keeps it (lkx).
- L82: K2547 `=K$826`, O2547 `=$J2548*O2213`: not reproduced.
- L83: O3601 `=$J3601*O2213`, O3592 `=$N3592*O2213`: not reproduced; built as 465 (pseu, pser x psf.ecy).
- L84: O3606 `=IF(AND($J3606<0,PowerSubsidyExemptInclude="Include"),$J3606*O2214,$J3606)`: the phasing is correct in
  465 (only the MTInputs C138 unit text "Exempt/Include*" is stale); built as 465 (csd).
- L86, L100: `_manual_codes`, `_manual_prices` cover G59:N146; manual electricity prices and the producer subsidy are
  read in 465: not reproduced; built (MPU covers rows 60-146).
- Proposed register status for all eight: "Not reproduced in legacy 465" (source version to re-check).
- Bugs fixed here: L94 (R6.4, already), L101, L135, L220, L222. New issues replicated: I136-I146 (as listed in
  the notes section E); I142: E5 check column shows -(shadow price + rebate) when they are not 0.

## 4. LegacyDiff rows (by LD number)
- **LD19 Producer subsidies**: this model: "In the supply cost as legacy (v9.0, R7): per-unit subsidy psu (Prices_dom
  mit.pros, or Manual inputs) up to the last price year, then x the phase-out factor psf; block row psp in the supply
  cost, so the floating taxes and price controls absorb (1 - pass-through) of the phase-out (rows 2455-2708, 2213);
  fiscal line rpsu by fuel. Electricity: allocation by the pre-tax gap, per kWh floored at -0.3 $/kWh, residual memo,
  passed through in the price before policies (rows 3587-3592, 3601, 3630)". Reason: "As legacy (v9.0, R7; v6.2
  separate wedge reverted); L82, L83 not reproduced in 465; issues I49, I146". Effect: "None for Egypt (no producer
  subsidy data)". Type: **Same**.
- **LD32 Power: end-user prices**: this model: "Telescoped (S4) with every legacy component: price(t) = price(t-1) +
  pass-through x change in (supply cost + producer subsidy pseu + consumer subsidy phase-out csd + price-chain residual
  ores) x (1 + VAT) (v9.0, R7.9, R9.3)". Effect: "Egypt: the residential residual (-0.063 $/kWh at LastHist 2022)
  shrinks when the supply cost falls below its 2022 value: residential price up to +0.0008 $/kWh". Type: **Same**.
- **LD62 Road transport: biofuels**: elasticity road model now as legacy (rows 5403-5406, 5435): bioethanol and
  biodiesel follow the elasticity-model gasoline and diesel, other biofuels the fuel-use equation with oil elasticities
  and the biomass price (I143); type **Same**.
- **LD63 Road transport: range anxiety**: this model: "Goal seek on the prototype's model (ra_goalseek.py, scenario 1,
  2025, stored in data/range_anxiety_fit, written over the country's Transport3 cells)"; legacy: "Solver results for
  the legacy model (Transport3)"; effect: see section 6; type **Same** (method as legacy; I145).
- **LD67 Exemption phase-out**: add "v9.0 (R6): share over the economy-wide basket spend (I136), lpg if the WHOCooking
  code is missing (I137), leakage on the not-exempt use (I138)"; type **Same**.
- **LD68 Manual inputs tab**: add to the blocks read: manual domestic prices (G59:N146), manual elasticities
  (K279:N307, L319), methane intensity decline (J185:J188).
- New rows proposed: "Methane intensity decline" (legacy rows 6077-6079, 6103, 6159-6183 and 6203-6212 without the
  index for agriculture and waste (L135); this model: every source x (1 - rate)^(year - GHGYear); Same, bug L135
  fixed); "Power cost memos E4, E5, F1" (yearly rows instead of the CostBreakdownYear table; Same numbers in that
  year; L222 fixed); "Self-generated renewables in aviation and navigation" (Same; I144).

## 5. Register status changes
- I49: resolved as legacy (v9.0: phase-out in the supply cost; wedge rows removed).
- I53 / I139: replicated (manual rows switch on with a 2021 value; manual years 2021-2026).
- I61 (range anxiety fit off for the prototype): addressed by the goal seek (R10.8-R10.9).
- I135-I146: replicated as built (see section 1). L101, L135, L220, L222: fixed in the prototype.

## 6. Results (quick check) and Egypt comparison
(filled below)

## 7. Version-log sentence
"v9.0 (R6-R10): residential exempt split as legacy (basket denominator, lpg default, leakage on the not-exempt use);
producer subsidies in the supply cost as legacy and electricity producer subsidies (allocation, per kWh floor,
residual); electricity consumer-subsidy phase-out (PowerSubsidyExemptInclude) and the price-chain residual (rows
3607/3636); manual domestic prices, manual elasticities (L101, L220 fixed) and the methane intensity decline (L135
fixed) read from Manual inputs; power cost memos E4, E5, F1 (L222 fixed); road biofuels of the elasticity road model,
self-generated renewables of aviation and navigation; range anxiety fitted on the prototype (ra_goalseek.py)."

## 8. Caveats (CAVEATS.md)
- LastHist of the prototype is 2022 (Settings C10, decision 2026-10-15), legacy 465 uses 2024: the electricity tax and
  residual are those of 2022 (res txe +0.0021, ores -0.063 $/kWh; legacy 2024: -0.0551, -0.0205). Not changed here.
- Methane intensity: decline from GHGYear (2024), legacy from 2023.
- The deadweight cost of the methane fee (`mfc` rows, section 18) still uses the unabated base without the intensity
  index (as check_full); a small overstatement where the fee is on.
- Revenue: the electricity producer-subsidy phase-out raises the price before policies, so it enters the subsidy gap
  `rgap` as well as `rpsu` (addendum: "rgap as now"); a possible double count where pros.ecy is not 0 (Egypt 0).
- check_full: the exempt split (lkx) and the R10 rows are not re-computed (ExemptMostCook No, Egypt values 0); the
  electricity subsidies only through power_model_ref's txo inputs; the E2 memos not re-computed (to add).
