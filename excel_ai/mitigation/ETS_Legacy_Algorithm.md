# Legacy ETS algorithm and a benchmark-based design for the prototype

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

Background note on the legacy algorithm and the design choice behind the prototype's ETS; the prototype method is in `ETS_Method.md`.

Source: `CPAT 1.0pre_456_NoPropData.xlsb`, sheet Mitigation rows 1797–1969 and 2244–2425, sheet Manual inputs O15:AB15, and VBA Module1 (`OverrideETSFast`, `SolveFast`). Row numbers are legacy rows. Formulas not stored in the dump are inferred from the row labels and cached values and marked *(inferred)*.

## 1. Legacy inputs

| Rows | Item |
|---|---|
| 1800–1809 | Apply ETS; cap change at start and target (% vs baseline); cap continuation; start and target years; auction proportion at start and target; continuation; override switch |
| 1811–1813 | Risk premium inputs: price volatility 0.42, impact 0.5, policy risk 0.2 |
| 1815–1836 | Sector table: included flag, baseline emissions, semi-elasticity of emissions to the carbon price (power −0.00279, transport −0.00283, residential −0.00386, industry −0.00549, CBAM −0.001 per $/t), generic proportions |
| 1843 | Relative price of auctioned ETS vs tax for the same emissions target: 1.1 |
| 1846–1847 | Relative effectiveness, hardcoded: auctioning **1.0**, output-based allocation (OBA/OBR) **0.5** |

Allocation is one **time path of the auctioned share** *a* (rows 1863–1864; OBA share 1 − *a*), the same for every covered sector.

## 2. Legacy fast estimate (no iteration)

1. **Covered semi-elasticity** (row 1845): coverage-weighted average of the sector semi-elasticities, ε = −0.00288 in the cached run. The all-sector average used for the carbon tax (row 1844) is −0.00371.
2. **Reduction left for the ETS** (rows 1858–1860): the reduction needed by the cap minus that of other policies, counted as an effective carbon price × ε_tax (row 1859, e.g. $50/t × −0.00371 = −18.6%).
3. **Effectiveness of the allocation mix** (row 1866): e = a × 1.0 + (1 − a) × 0.5.
4. **Adjusted semi-elasticity** (row 1867): ε_adj = ε × e. With full OBA, −0.00288 × 0.5 = −0.00144, matching the cached value.
5. **Estimated price** (row 1868, `QuickEstimateOfETSPrices`): p ≈ (reduction left for the ETS) / ε_adj *(inferred: linear semi-elasticity form)*.

This closed-form estimate ignores the full fuel-demand model, where the response comes from prices × elasticities by fuel and subsector, not from one semi-elasticity.

## 3. Legacy override and goal seek (VBA)

- Row 1872 reads override prices from Manual inputs O15:AB15 (`OverrideOfETSPrices`); row 1873 uses them when the override switch is on.
- The full model computes covered emissions with the ETS (rows 1888–1953) and compares the actual reduction with the cap (rows 1956–1963: actual, cap, difference, ratio, error per year; max error in J1963).
- The workbook proposes a corrected price per year (`PricesAdjustedByErrorFactor`): p × (target log-reduction / actual log-reduction)^0.5 (convergence factor 0.5, row 1966).
- `OverrideETSFast` switches the ETS and the override on and calls `SolveFast`, a damped fixed-point iteration in log space:
  1. If StartFresh, seed the override row from the quick estimate.
  2. Step p ← p × (r/p)^α, with r the workbook's proposal.
  3. Anderson-style mixing: 0.7 new + 0.3 previous iterate.
  4. Smoothing: 5% weight on a centred 3-year moving average.
  5. Negative or invalid values keep the old price.
  6. Write back, recalculate, take the worst-year error over all 14 years. (The named `WorstYearlyETSError` averages only 9 years, so the macro bypasses it.)
  7. Halve α if the error got worse (minimum 0.0625); multiply it by 1.2 if the error more than halved (maximum 1).
  8. Stop when the worst error < `ETSErrorTolerance` or after `ETSMaxIterations`.
- The cached run has override prices of about $22–28/t for 2028–2038, with jumps (1.5 in 2027, 13.8 in 2040) and a max error of 0.33. It had not converged; the cap rows are 0 in the cached state.

## 4. Legacy split of the price (the same in both parts)

| Part | Legacy rows | What it does |
|---|---|---|
| Auctioned | 1875–1879, 2252 (`egy.mit.etstraj`) | p × a enters fuel prices as a **price wedge**, like a carbon tax: fuel switching, efficiency and usage all respond. It raises revenue. |
| OBA / OBR | 1881–1885, 2343–2349 ("Feebate plus non-auctioned ETS"), 2402–2419 | p × (1 − a) enters as a **shadow price on the efficiency margin only**, like a feebate: no pass-through to consumer prices, no revenue. |

The legacy note on rows 1875–1885 says "Arguably this should be an exp/ln function TBC": the split is linear in p. This is also why OBA effectiveness is 0.5: only the efficiency share of the response is triggered, about half of the total with the default elasticities.

## 5. prototype design: benchmarks instead of one auction share

The legacy auctioned proportion is replaced by **benchmarks per covered subsector**. Everything after the split stays as in section 4.

- **Inputs** per subsector: the covered flag and a benchmark path *b*(t), a share of the subsector's base-year emission intensity (e.g. 0.9 → free allocation at 90% of base-year intensity; a declining path tightens it).
- **Shares**: free allocation FA = b × base-year intensity × output, with output proxied by baseline fuel use (the prototype has no output variable). OBR share s = MIN(FA / covered emissions, 1); auctioned share a = 1 − s. To first order s ≈ b (intensity unchanged). Using actual covered emissions would be circular through fuel use, so the recommendation is scenario-1 (baseline) covered emissions, as in option A of `ETS_Cap_Design_Options_v6_4.md`; s is then a data-driven input.
- **Then as legacy**: effectiveness e = a + 0.5 × s per subsector; the auctioned part p × a is a price wedge (revenue = p × (covered emissions − FA)); the OBR part p × s joins the sector shadow price (the feebate channel); the fast estimate p = (reduction left for the ETS) / (ε × e), with ε and e weighted by covered baseline emissions.
- **Override**: an offline goal seek (a Python script with the same damped log-space step) writes a row of prices to paste. No VBA and no circular reference.

Without benchmarks the ETS is fully effective (permit price = carbon price path × coverage, as effective as a carbon tax, per an earlier user decision), and the auction share only affects revenue. With benchmarks, the OBR part moves from the price wedge to the shadow price, so emissions fall less for the same p and revenue falls. A benchmark of 0 (full auctioning) reproduces the fully effective case exactly.

## 6. Open points

1. The fast estimate uses legacy's sector semi-elasticities. The prototype could derive them from its own elasticities (one-off calibration run) to keep them consistent.
2. Legacy's linear split (p × a) vs a log form (legacy's own TBC note).
3. Legacy's relative price 1.1 (auctioned ETS vs tax) and the risk-premium inputs (rows 1811–1813) are not used by the fast estimate as cached. Check their role before carrying them over.
4. The CBAM sector semi-elasticity (−0.001) is not modelled in the prototype.
