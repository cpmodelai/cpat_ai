# Power engineer model: legacy 456 -> 465 (v9.0, group POW465)

The prototype's power engineer model (Mitigation section 3; Python reference `excel_ai/mitigation/power_model_ref.py`)
was written from legacy 456 with the legacy bugs fixed. LD41 moved the data extracts to legacy 465, and 465 changed
about 100 formulas of the engineer model. This note lists those changes, what they mean for the prototype, and the
reference test on 465.

User rule (2026-10-29): the CPAT team's power-model changes in 465 are bug fixes. The prototype follows 465. A change is
recorded as a caveat only where it does not do what it means to (cell evidence below).

## 1. How the changes were found

- Every formula of Mitigation rows 2950-4300 was decoded from both `.xlsb` files (the `dec.py` decoder pointed at 456, and
  `dec465.py`) and compared cell by cell. 111 rows (1,107 cells) differ.
- The policy copy (456 rows 9285-10631, 465 rows 9270-10616) was compared after mapping the 456 row numbers in each
  formula with `legacy/bugfixes/data/rowmap_456_465.json`. It changes in the same rows as the baseline. The only other
  differences are references written with an explicit `Mitigation!` prefix, which the map leaves alone, so they are
  not real changes.
- Rows 2170-2949, which the engine reads (carbon prices, regulations, switches), were also compared. Their changes
  belong to other modules: L65, L80, L87 and L93 in rows 2251-2288 and 2371-2394. They are not in this list.

## 2. Change list (465 cells; the policy copy is +6316)

| Rows (465) | 456 | 465 | Register code |
|---|---|---|---|
| K2977:K2985 | `MATCH(G,Power!$A$25:$A$356,0)` (whole Power tab) | `MATCH(G,Power!$A$112:$A$294,0)+87` (country block only) | L55 |
| P2981:T2985 | renewables: `IF(ISERROR(country),country,...)`, so they take the world value | `IF(country>0,country,...)` as the other types | L52 |
| N2999:N3007 | installed capacity read from `Power!$F:$Y` (no 2022 column, so the actual CF is never used) | `Power!$F:$AC` | L53 |
| I3042:I3046 | missing capex-decline series -> 0 | fallback `ctf.old<scen>`, then `wld.ctf.med.` | L109 |
| L3150:AF3150 | `RenewableSubsidyHydro="Yes"` | `LEFT(...,3)="Yes"` (AF added) | L113 |
| L3155:AE3157 | fuel price for power `AVERAGE(t-2 .. t+2)` | `AVERAGE(t-4 .. t)` from 2022 (`$L` while t < 2026) | L126 (caveat 1) |
| L3398:AE3400 | D6 shadow price = feebate only | + `$F2403*IF($D2369,L2375*$I...,0)` (regulations) | L88 |
| M3409:AE3409 | rebate `=-M3408` (per kWh consumed) | `=-M3407` (per kWh generated) | L9 |
| O3592, O3601, O3630 | `N3592*N2213` (compounds, lags a year) | `$N3592*O2213`, `$J3601*O2213`, `$J3630*O2213` | L83 |
| O3606, O3635 | consumer subsidy phased with factor row 2216 | row 2214 (consumer factor) | L84 |
| L3660 | manual excise revenue counts the whole excise | `(ntx - ntx of the last historical year) x pass-through`, after the last historical year | L111 |
| L3663 | rebate revenue includes VAT | `L3615/(1+L3611)` | L110 |
| M3691, M3697, M3703, M3709 | efficiency exponent `$F3677` (efficiency elasticity), increment `$M3719` | `$F3676` (usage elasticity), `$M2198` | L2, L95 |
| M3692, M3698, M3704, M3710 | `($F3675/$M3686)*M3686*M2433` (income factor twice) | `$F3675*M2433` | L3 |
| M3719 | `=M2198` | cleared | L95 (caveat 2) |
| M3676, M3690 | empty | `=M2433`, `=+$M2198` (memo cells, read by nothing) | L3, L95 (no effect) |
| N3731:AE3731 | services grow with the industry multiple (`N3707`) | `N3713` (services) | L1 |
| L3773, L3779 | `MAX(...,$G4291*L3752)` (stray reference) | `MAX(...,0)` | L11 |
| L3911 | long-term storage x `$E3876` twice | once | L4 |
| M3973 | `=L4004` (nameplate retirements) | `SUM(L4012:L4019)` (effective) | L7 |
| L4011 | `SUM(L4009:L4010)` (not capped) | `L3994*$W2999` | L8 |
| M4024 | `=L4030` (last year's plan) | `=M3753` (actual effective capacity) | L10 |
| L4027 | `=L3752` (this year's demand) | `L3752*IFERROR(L3752/K3752,1)` (next year's) | L67 |
| L4045, L4046 | cheapest type incl. types not permitted | `AGGREGATE(15,6,cost/(permit=1),1)`, else MIN | L6 |
| H4067 | `$L$3827>50%` | `$M3005/SUM($M2999:$M3007)>50%` (hydro share of base-year generation) | L54 |
| L4110:AE4118 | logit investment on `L4028` | on `L4108` (need net of manual investment) | L118 |
| L4273 | total nameplate investment is 0 | `SUM(L4264:L4272)` | L12 |
| L4276:AE4284 | capex at factor 1 (`$O2977`) | capex of the year (`L3099`) | L5 |
| E3871-E3878, E4061-E4069, F3636, F4097-F4118, F4264-F4272 | `MTInputs!F$388` ... | 2 rows higher (465 removed two MTInputs rows) | none: same inputs |

Every change matches a register bug, so no new code (Lnew-POW-n) is needed. The register check of these mappings was
not repeated here (deferred, see the changes file).

## 3. Caveats (a 465 fix that is incomplete)

1. **L126, biomass not fixed.** 465 `L3163:AE3163` (and the policy copy, row 9479) still read
   `=IF(UseSpotFuelPricesInEngineerModel="Yes",L3080,AVERAGE(J3080:N3080))`. This is the centred t-2 .. t+2 window, which
   reads later years. Coal, gas and oil (rows 3155-3157) use the trailing window. The prototype uses the trailing window
   for every fuel (intended formula, unchanged). For Egypt this has no effect, because the biomass price is flat after 2026.
2. **L95, partly fixed (already registered as a caveat).** `M3719` is cleared, but `P2823:AE2823` (total power demand,
   outside the engineer rows) still read `$M3719`, which is now empty.

## 4. What changed in the prototype

- **Engine formulas: nothing to change.** The prototype already implements every fix above, in the same form as 465:
  - L1-L12, L67: the engine runs with all of `power_model_ref.FIXES`.
  - L52-L55, L109: the data step.
  - L126: the trailing t-4 .. t average from the base year, which is exactly 465's coal, gas and oil formula.
  - L83, L84, L88, L110, L111, L113, L118: built in v5.4-v6.2.

  The prototype's data step (`power_model_ref.mvp_data`, as `check_full.power_data`) gives the same values as the 465
  cached A4 data (`power_tech.csv`) for all 9 types and 12 columns: capacity factors, efficiencies, cap0, gen0,
  investment start (hydro 2030), WACC and scale-up rates. The capex time factors of wind and solar differ only in
  2039-2040, because the prototype reads the Power tab and legacy's stored values are stale there (issue I94, still
  present in 465).
- **Labels:** the `fpp` row and the `POWFUELPRICE` description no longer say "centred t-2 .. t+2". They now describe the
  trailing window (`build.py`).
- **Not built (hand-off), the price-chain residual.** Legacy rows 3607 and 3636 ("Additional Over(+) or Under(-)
  estimated Costs") hold the residual `J` of the last historical year. When `J < 0`, the residual scales with the supply
  cost once that cost falls below its last-historical value:
  `O3607 = $J3607 - IF($J3607<0, MIN(0, O3600-$J3600), 0)*ABS($J3607/$J3600)`, that is `J x MIN(sc, sc_L)/sc_L`.
  - This formula is the same in 456 and 465. In 456 Egypt's `J` was positive (+0.067), so the prototype's telescoped
    price (simplification S4, "held components cancel") gave the same numbers.
  - The 465 data split the 2024 gap into a consumer subsidy (`J3606` = -0.0551 $/kWh) and a negative residual
    (`J3607` = -0.0205). The residential price before policy is therefore higher than the telescoped one, by
    +0.00027 $/kWh in 2025 (0.044272 against 0.044002).
  - The residual needs the consumer tax/subsidy of the last price year, `txe`. That is the parallel group's R9 (rows
    3604-3606), which also edits the same `rppre` formula. So it is specified for the integrator in
    `excel_ai/mitigation/v90_POW465_changes.md` and not built here.

## 5. Reference test (power_model_ref.py)

- `extract_power.py` now also writes the cached rows `sc_ind` (3629), `txo_res`/`txo_ind` (3606, 3635) and
  `ores_res`/`ores_ind` (3607, 3636) to `legacy_engineer_reference.csv`. These are 10 new rows; every other extract is
  byte-identical after the re-run.
- `power_model_ref.engine` adds the residual of section 4 when `txo_*` is given.
- `legacy_test` now runs with `ALL_FIXES`, because 465 contains them all.
- **Result.** `legacy_test('base')` and `legacy_test('ctax')` reproduce all 211 cached rows of both 465 runs (2022-2040):
  - base: max relative difference 1.7e-12 (second|wnd 2031);
  - ctax: max relative difference 9.2e-13 (second|nga 2032).

  Without the fixes the test fails (second|nga off by a factor of 525), as expected.
- `check_full.check_power_method` uses this test (now with the 465 fixes). Its per-fix effect table is still measured
  against 456's unfixed method.
