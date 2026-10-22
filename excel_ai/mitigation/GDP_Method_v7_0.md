# GDP effects: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`. Decisions: `Old/GDP_Plan_v3_6.md`.

The model estimates how spending the revenue gained by the policies changes GDP. The change feeds back into GDP growth, which drives fuel use, power demand and the non-energy GHG drivers. The method follows legacy CPAT section 17, with legacy bug L24 fixed.

## 1. Inputs (Egypt defaults)

- Revenue use, % of revenue (ScenarioDefinition): labour tax cuts 30, corporate tax cuts 0, public investment 50, current spending 0, targeted transfers 20.
- Multiplier source (ScenarioDefinition row 226): Global, income group, Estimated or Manual; Egypt: income group (LMIC). Range Base/Low/High (row 263): Base. Start year for GDP calculations (row 236, GDPStartYear): 2025. Endogenous GDP effects: Yes.
- Fiscal multipliers by group, instrument and lag 0-19 (sheet Multipliers, from the legacy sheet: MFMod medians). Low and high are the median minus and plus one standard deviation. Lags 12-19 hold the lag-11 value, as in legacy. v4.15 (LD56): "Estimated" takes the country's table of the legacy Multipliers tab (rows 210-1620, exact match of the country code; the income group where the country is missing, and for CIT and WAGE, whose legacy tables are empty or wrong: bug L76); "Manual" takes sheet Manual inputs J261:U268 (legacy addresses, lags 0-11, blank = 0). Low and high add -/+ the income group's standard deviation to these too, as legacy (issue I44). Any other source text means the income group.
- Baseline real GDP (sheet WEO): 547 USD bn in 2022.

## 2. Method

1. **Fiscal space** (v4.15, LD55): total revenue of the scenario (existing taxes net of subsidies plus new policies, power included: rnet + rnew, v4.16 + subsidy reform rsr and producer subsidies rpsu, as legacy's rev.new.usd = row 8026, the total of all instruments) minus that of scenario 1, as a share of GDP. Lower fuel use also lowers the cost of existing subsidies (base erosion), and that counts. Scenario 1 has no GDP effect.
2. **Impulse** (v4.15, as legacy row 14356): the change of that revenue gain in USD over this year's GDP, 0 before GDPStartYear (issues I41, I42). Each impulse starts a cohort that acts for 20 years (lags 0-19), lag 0 in the impulse year (legacy applies lag 1 there: bug L68).
3. **Effect of each use**: its share x the sum of impulse x multiplier over the lags. The revenue itself counts as an energy-tax increase (instrument `exc`, share -1). The uses map to labour tax (`pit`), corporate tax (`cit`), public investment (`capt`), current spending (`gnfs`) and transfers (`trns`).
4. **GDP effect**: the sum over uses (0 if endogenous effects are off): the change of the GDP level against the baseline, as a share of GDP.
5. **Feedback**: the GDP level is 1 + last year's GDP effect, and growth follows from the baseline growth and the change in that level. The one-year lag avoids a circular reference (revenue depends on fuel use, which depends on growth). Legacy instead adds the effect to the growth rate every year, so a steady effect compounds (L24).

## 2b. Timing rule (stated v6.2, issue I72; user 2026-10-20)

**Revenue of year t changes GDP only from year t+1.** `gdp.lvl`(t+1) = 1 + `gdp.eff`(t), and GDP growth after the feedback reads that level (as legacy row 8776, which reads the previous column). Three consequences, kept as rules:

1. The fiscal space of year t reads revenue of year t only (no later year, no whole-row lookup).
2. A same-year GDP effect never reaches same-year demand: the impulse of year t counts at lag 0 in `gdp.eff`(t), which acts on GDP from t+1.
3. Every other block must not read a later year (NORMS, circular references). With this lag, no revenue line can then close a circular reference, whatever it reads (fuel use, power, methane).

The quick check tests the reads of later years; a change that breaks the lag must restate this rule and pass the full recalculation (Err:522).

## 3. Results for Egypt (scenario 2 of the shipped file)

| | 2027 | 2030 | 2035 | 2040 |
|---|---|---|---|---|
| Fiscal space (share of GDP) | 0.74% | 0.75% | 0.65% | 0.57% |
| GDP effect (level) | 0.00% | -0.02% | 0.17% | 0.39% |

Fiscal space jumps to about 0.75% of GDP when the policies start (v4.15: total revenue; v4.14, new-policy revenue only: 0.55% in 2030). The revenue first lowers GDP: the excise multiplier peaks two years after the impulse. From the early 2030s public investment and transfers outweigh it, and GDP ends about 0.4% above the baseline. The effect raises fuel use a little through the income elasticities.

## 4. Choices and differences with legacy (sheet LegacyDiff)

- **L24 fixed**: the effect raises the GDP level, not the growth rate every year.
- **Revenue** (v4.15): total revenue, as legacy (the v3.1 reading "new-policy revenue only" misread legacy's code rev.new.usd, which is the total). v6.2: the methane fee revenue is included as legacy, on the stored scenario-1 activity of downstream gas and biomass use (`ch4.revf`, issue I47: no vulnerability to circular references; none for Egypt). v4.16: fis.rev adds its parts (rnet + rnew + rsr + rpsu); the v4.15 form rtot - rmf still referenced the methane fee and LibreOffice reported a circular reference (Err:522) on a full recalculation (found by the paste test's batch emulation).
- **Impulse and start year** (v4.15): as legacy (I41, I42). Not replicated: legacy sets the revenue-use shares to 0 before CPIntro, so earlier impulses count only as an excise drag (I43, tiny for Egypt).
- **Legacy bugs fixed**: L68 (lag 1 in the impulse year), L69 (first cohort's excise drag lost), L76 (Estimated multipliers).
- **Scenario-1 lookups stop at the current year**, which avoids a circular reference with the GDP feedback. Values are unchanged.
- **Legacy benchmark**: the NoPropData file strips the baseline GDP-effect rows to 0, but the policy rows 14584-14607 hold the cached values of its carbon-tax run (GDP effect 2030 -0.07%, 2035 +0.34%, 2040 +1.22%; its carbon price rises to about 175 $/t in 2041, so it is not the MVP scenario). The check compares the workbook with an independent Python recomputation that iterates the whole model on the growth path until it converges (growth depends only on earlier years).

## 5. Memo rows (v5.7; legacy F4 rows 16163-16201)

- gdpg.<use>: contribution of each revenue use to real GDP growth: (1 + baseline growth) x (fis.eff(t-1) - fis.eff(t-2))
  / gdp.lvl(t-1) when GDPEndogenous = Yes; gdpg.all, from gdp.eff, equals gdp.pos.pct - gdp.base (the channels sum to
  it). Legacy rows 16166-16175 add the effects to growth every year (L24), so its channel values are not comparable.
- gdpy: year of the reform, N = year - GDPStartYear + 1; the growth effect of reform year N (legacy rows 16183-16194)
  is gdpg.all in the column where gdpy = N. (v6.0: a row shifted to later columns read forward through the GDP chain
  and made a circular reference.)
- gdp.chg.usd: real GDP after the feedback - baseline real GDP (legacy rows 16199-16201).
