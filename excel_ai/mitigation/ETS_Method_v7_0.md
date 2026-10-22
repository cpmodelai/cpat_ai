# New ETS: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`.

How the MVP models a new emissions trading system. Background on the legacy algorithm and the design choice: `ETS_Legacy_Algorithm_v7_0.md` and `Old/ETS_Cap_Design_Options_v3_6.md`.

## 1. Inputs

| Input | Notes |
|---|---|
| Apply new ETS; start and target year (ScenarioDefinition) | |
| Cap: change against baseline covered emissions at start and target; continuation (ScenarioDefinition) | `Constant` keeps the cap level after the target year; any other value keeps the relative change |
| Price override switch (ScenarioDefinition) | `Yes`: the permit price comes from an override row of prices |
| Volatility, impact of volatility, carbon tax policy risk (ScenarioDefinition) | Labels Medium / High / Low / Zero; values from legacy ETS+LTS |
| Sector coverage (ScenarioDefinition) | 17 ETS sectors: power plus the 16 subsectors |
| Benchmarks by sector group (power, transport, residential/buildings, industry) | Share of a sector's emission intensity allocated free = 1 - the auctioned proportion of ScenarioDefinition rows 90-91 (start, target year) of the scenario, the same for every group, as legacy (v4.15, issue I21). Default 1.0: nothing auctioned, the legacy default. After the target year the target share is held (legacy drops it to 0 unless the continuation is Constant: bug L78). Benchmarks by sector come later. |
| Semi-elasticities by ETS sector | Legacy ETS+LTS table by country and sector group (power, transport, residential, industry; food and services use industry), sheet ETSSemi, looked up by the country code (v3.3; legacy Mitigation rows 1815-1831); used only by the fast estimate |
| Baseline CO2 by ETS sector | Scenario-1 CO2 by ETS sector, stored as data and refreshed by the build (with a check) |
| Effectiveness of output-based allocation; convergence exponent | 0.5 and 0.5 (legacy hardcodes) |

## 2. Price

- A covered sector counts once the ETS applies.
- Benchmarks run linearly from the start to the target year, flat afterwards. The output-based rebating (OBR) share of a sector = its group's benchmark, bounded to 0-1.
- Volatility adjustment = (1 + carbon tax policy risk x impact) / (1 + ETS volatility x impact). At Medium: (1 + 0.2 x 0.5) / (1 + 0.42 x 0.5) = 1/1.1.
- Cap = baseline covered emissions x (1 + change), with the change linear from the start to the target year (after it, per the continuation input).
- Effective semi-elasticity = baseline-weighted average over covered sectors of semi-elasticity x (1 − (1 − OBR effectiveness) x OBR share); OBR effectiveness is a setting (Settings C14, legacy value 0.5).
- Fast estimate = LN(cap / baseline covered) / (effective semi-elasticity x volatility adjustment) when the cap is below the baseline; else 0.
- Permit price = the override prices if the override switch is Yes (a blank year takes the carbon price path), else the fast estimate; 0 before the ETS applies.
- Tax-equivalent price = permit price x volatility adjustment; revenue factor = 1 / volatility adjustment.

## 3. Effect on fuel use and revenue

The ETS replaces the carbon tax in covered sectors. The tax-equivalent price splits by the OBR share:

- **Price wedge (auctioned part)** = tax-equivalent price x EF x coverage x (1 − OBR share). It enters the after-tax fuel price, so usage and efficiency both respond, as for a carbon tax.
- **Shadow price (OBR part)** = tax-equivalent price x EF x coverage x OBR share, added to the feebate shadow price. It acts only on the efficiency margin of fuel use, as feebates do.

New-policy revenue includes the price wedge x the revenue factor: the permit price on the auctioned part of covered emissions. The OBR part raises no revenue.

## 4. Meeting the cap

The fast estimate uses one semi-elasticity, so the full model does not hit the cap exactly. The model reports CO2 by ETS sector, covered emissions, the cap, the gap (covered / cap − 1) and a proposed price p x (LN(cap/baseline) / LN(covered/baseline)) ^ 0.5. To meet the cap, either:

- paste the proposed prices into the override row (with the override switch on) and repeat; or
- run the goal seek: the macro `SolveETSLive` (live scenario; `RunAllScenarios` runs it for every definition with a new ETS and no override), or `python ets_goalseek_v7_0.py WORKBOOK.xlsx <scenario>`, which writes the prices to `ets_override_s<scenario>.csv` for pasting into the override row. Both iterate with legacy's damped log-space step (mixing, smoothing, adaptive step) and stop when the worst yearly gap |covered / cap − 1| is below the maximum error, or after the maximum number of iterations.

The goal-seek settings are on sheet `Manual inputs` at their legacy addresses, as legacy (one value for all scenarios):

| Cell | Name | Setting | Value | Legacy default |
|---|---|---|---|---|
| E10 | ETSMaxIterations | Maximum number of iterations | 20 | 30 |
| E11 | ETSStartFreshContinue | StartFresh: start from the fast estimate (ets.est); Continue: start from the override row if it holds prices | Continue | Continue |
| E12 | ETSErrorTolerance | Maximum error: the worst yearly \|covered / cap − 1\| | 0.005 | 0.001 |

The values are those the goal seek has always used here; the legacy defaults are given for reference (the legacy error is measured on its own convergence criterion). A cell that is not a positive number falls back to 20 iterations and 0.005.

## 5. Limits

- Power is covered like any other sector: the power model gives its emissions, and the ETS cost enters its generation cost.
- Benchmarks are relative to current emission intensity, and output is proxied by fuel use. Free allocation therefore moves with emissions, and the OBR share equals the benchmark.
- The volatility adjustment scales behaviour (the tax-equivalent price), not the permit price. VAT on new policies is levied on the tax-equivalent ETS cost.
- No banking, borrowing, price floors or ceilings, and no CBAM process emissions.
