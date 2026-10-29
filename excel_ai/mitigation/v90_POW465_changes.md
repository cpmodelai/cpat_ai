# v9.0 group POW465: power engineer model aligned with legacy 465 (changes for the integrator)

Full note: `excel_ai/plans/Power_465.md`.

## Summary
- About 100 formulas of the 465 engineer model changed (111 rows; the policy copy changes the same rows). They are
  all CPAT-team fixes of registered bugs: L1-L12, L52-L55, L67, L83, L84, L88, L95, L109-L111, L113, L118 and L126.
  The MTInputs references moved 2 rows (no change in meaning).
- The prototype already had every one of these fixes in the same form, so **no engine formula changed**. Only the
  `fpp` label and the `POWFUELPRICE` description were corrected (they still said centred t-2 .. t+2).
- `power_model_ref.legacy_test` reproduces both cached 465 runs (base 1.7e-12, ctax 9.2e-13) with ALL_FIXES and the
  price-chain residual (below).

## Deferred (user, 2026-10-29)
- The detailed power checks (`check_full` power sections) and the cell-by-cell check of the code mapping against
  `issues_register.py` / `check465/legacy465_check.json` are deferred. The mapping in Power_465.md section 2 is from the
  formulas, not from re-reading each register cell plan.

## Register / tracker updates
- **L126:** fixed in 465 with a caveat. Coal, gas and oil (L3155:AE3157) use the trailing t-4 .. t window, as the
  prototype. Biomass L3163:AE3163 (policy row 9479) is still `AVERAGE(J3080:N3080)`, the centred window that reads
  later years. Status in legacy 465: "Fixed with caveat (biomass row 3163 not changed)". The prototype is unchanged:
  it applies the trailing window to every fuel.
- **L95:** the caveat is confirmed: P2823:AE2823 still read the cleared `$M3719`.
- No new bug codes (no Lnew-POW-n).

## LegacyDiff rows
- **'Power: fuel prices'** (`LEGACY_DIFFS`): the prototype column still says "centred average ... t-2 .. t+2". It
  should read: "Trailing average of the price before new policies over t-4 .. t from 2022 (row fpp; L126 fixed, as
  legacy 465 rows 3155-3157); Settings SpotPow for spot prices". Legacy column: "465: t-4 .. t from 2022 for coal, gas,
  oil; biomass still t-2 .. t+2". Verdict: Same (biomass: bug L126 caveat).
- **'Power: end-user prices'** (simplification S4, "same numbers as legacy"): no longer true with the 465 data (see
  the hand-off below). Until R9.3b is built: "Differs where the residual of the last historical year is negative
  (Egypt 465 residential: legacy price +0.00027 $/kWh in 2025)".

## Hand-off: price-chain residual (to build with R9, same rows)
Legacy rows 3607 and 3636 (unchanged from 456, newly active with the 465 data):
`O3607 = $J3607 - IF($J3607<0, MIN(0, O3600-$J3600), 0)*ABS($J3607/$J3600)`.
- `J3607 = N3575 - N3600 - N3602 - N3606 - N3601`: the price before VAT, less the supply cost, the manual excise, the
  consumer tax/subsidy and the producer subsidy, in the last historical year.
- Proposed (u in {res, ind}, L = last historical year):
  - R9.3a residual: `ores_u(L) = rppre_u(L)/(1+v_u) - sc_u(L) - ntx_u(L) - txe_u(L) - ps_u(L)`.
  - R9.3b projection: `ores_u(t) = ores_u(L) x MIN(sc_u(t), sc_u(L)) / sc_u(L)` if `ores_u(L) < 0`, else `ores_u(L)`.
  - In `rppre` (E49 with R9.3): `+ pi x (ores_u(t) - ores_u(t-1)) x (1 + v_u)`.
- The Python version is in `power_model_ref.engine` (inputs `txo_res`, `txo_ind`; outputs `ores_*`). `check_full`
  should pass `txo_*` (the R9 `txe`) once the sheet has it.
- Egypt 465 values: J3607 = -0.020467, J3600 = 0.121210, O3607 2025 = -0.020197 $/kWh. J3636 = +0.010896, so the
  industry residual is held.

## Data / extract
- `extract_power.py` writes 10 more rows to `data/mvp_legacy_extracts/legacy_engineer_reference.csv`: `sc_ind` (3629),
  `txo_res`/`txo_ind` (3606, 3635) and `ores_res`/`ores_ind` (3607, 3636), base and ctax. The other extracts are
  byte-identical after the re-run. (This touches `data/mvp_legacy_extracts/` after the LD41 merge: only added rows.)

## Version-log sentence
"v9.0 (POW465): the 465 engineer-model changes are the CPAT team's fixes of L1-L12, L52-L55, L67, L83, L84, L88, L95,
L109-L111, L113, L118 and L126, all already in the prototype; the power reference reproduces both cached 465 runs to
2e-12; L126 caveat (465 biomass row 3163 still centred)."

## Caveats (CAVEATS.md)
- The price-chain residual (rows 3607/3636) is not in the sheet yet (hand-off above). Until then the residential
  price after 2024 differs from legacy 465 by up to about 0.0003 $/kWh.
- The capex time factors of wind and solar in 2039-2040 still differ from legacy's stored values (I94, unchanged in
  465).

## Output codes
No formula of the engine changed, so the quick check should show no output-code changes from this group (labels
only).
