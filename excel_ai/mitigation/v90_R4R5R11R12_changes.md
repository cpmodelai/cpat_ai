# v9.0 changes of group R4R5R11R12 (for the integrator)

Scope after the user's change (2026-10-29): **only R11 is built**. R4, R5 and R12 are deferred to a later prompt,
because the legacy WIP is not linked up.

## Deferred (status)

| Item | Status |
|---|---|
| R4 CBAM process emissions | Design only, no code. Plan recorded in the commit message on branch `wip-r4-r5-r12` (17b memo block; prices = ctr + etr; switches CBAMProc<S>; Egypt goods typed in Constants; all rows memo, D-R4 not applied because no legacy row reads them). |
| R5 Green public investment | Design only, no code. Plan on `wip-r4-r5-r12` (16c after 16b; five constants + GreenNeedYrs 35 in NAMED_CONSTANTS; CCDR ratio from ETS+LTS rows 261-302; closed-form phi). |
| R12 Emissions intensity of industrial output | Design only, no code. Plan on `wip-r4-r5-r12` (13b block; GVA typed EGY; ftr electricity = demtot x (sh_tsd + sh_eou), legacy row 10071; var `co2.idr`, not `co2.ind`, which would clash with the code co2.ind.all). |

## R11 built (Equations_addendum R11.1-R11.9)

**Where.** Section 16b, a third sub-block after the energy trade balance: rows `bca`, `bca.gdp`, `bca.r`,
`bca.d.{oil,nga,coa}`, `bca.p`, `bca.y`, `bca.dp.{oil,nga,coa}`, `bca.pp`, `bca.n` (codes `egy.mit.bca.all.all.<n>`,
`egy.mit.bca.d.all.oil.<n>`, ...). Typed values on Inputs (block Inputs_macro), rows keyed `EGY|bca`, `EGY|bca_gdp`,
`EGY|bca_n`, years 2022-2041, bright yellow (F_CHANGED, FONT_CHANGED); read through WEOVal/WEOKey/WEOYear with
`CtryCode&"|bca"`, so another country reads 0. The fuel effect reuses `xnim.g.<g>` (L215, the gas unit bug, is not
replicated: xnim prices are USD/GJ). bca.dp calls SAFEDIV in the LAMBDA group (added to EXT_LAM). The 16b note no longer
says "until WEO current-account data are added". `check_full.py` 16b check extended to the bca rows.

**Departure, small:** `bca.y` and `bca.dp` give 0 where the % of GDP is 0 (a country without data); legacy would give
#DIV/0! (I129 otherwise replicated: GDP implied by CA / CA%).

**Register (for issues_register / LegacyDiff):**
- L50: status -> fixed in the prototype (v9.0): stale WEO codes; the corrected values typed for Egypt (EGY.BCA.A,
  EGY.BCA_NGDPD.A; held at 2031 by legacy's own rule). Column-lag part: already not replicated by 16b (`xtb`).
- L214: new legacy bug, fixed (coal left out of row 18195).
- L215: new legacy bug, not replicated (gas import bill x $/MMBtu; prototype `xnim` in $/GJ).
- L49: already fixed (share traded also on oil) - now also feeds the current account.
- I129 (replicated: % effects over the GDP implied by CA and CA%), I130 (replicated: bca.n 0 after 2031).
- Data issue (new, area Data, Extremely high per NORMS 0): current account typed for Egypt only; other countries 0.

**LegacyDiff row (new):** Area: External balance (current account). Legacy CPAT: rows 18180-18198, all #NAME?/#N/A
(stale WEO codes, L50); 18195 leaves coal out (L214); gas bill x $/MMBtu (L215). This model: typed WEO values for
Egypt (held at 2031), change = - xnim by fuel group, % of GDP over the implied GDP, coal included. Effect: legacy shows
errors; the prototype shows the current account. Codes: L50, L214, L215, I129, I130.

**Version-log sentence:** R11: current account (section 16b) from typed Egypt WEO values (EGY.BCA.A, EGY.BCA_NGDPD.A;
L50 fixed) and the change in net energy imports by fuel group (L214, L215 fixed); no existing output changes.

**Caveats:** Egypt only (typed); the current-prices memo (bca.n) is 0 after 2031 as legacy (I130); the % of GDP effect
divides by the GDP implied by the current account (I129), not by the model's GDP.

**New Settings/MTInputs inputs:** none. MT_LAST unchanged.

## Quick check and comparison with legacy

- Quick build: no exception, no lint error. Quick check: **PASS** (no error values; copy-paste, code protocol C1/C5/C7/C10
  OK). Output codes vs v8.4: 26 new codes from R11 (13 rows x 2 groups); no existing code changed by R11 (the rows are
  appended at the end of 16b and of Inputs_macro; the other changes in the regression come from the base commit).
- Egypt, pre-policy rows equal legacy (intended, L50 fixed): bca.r 2022 -18.8158, 2026 -17.8346, 2030 -17.7980,
  2031-2041 -15.9437; bca.y 5.4025 (2022), 5.6058 (2030), 5.9763 (2031+); bca.n 0 from 2032.
- Policy effects differ, as expected: the prototype's live scenario is not legacy's 0 -> 5 USD/t carbon tax, and xnim
  uses section-2 supply prices and the share traded also on oil (L49). Scenario 2, 2030: bca.d oil 0.903, gas 0.305,
  coal 0.084, bca.p -16.506, bca.pp -2.944 % (legacy: 0.201, 0.027, 0.005, -17.565, -3.133 %); 2041: bca.p -14.395,
  bca.pp -2.409 % (legacy -14.962, -2.504 %).
