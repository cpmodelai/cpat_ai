# Macro, revenues and results

## GDP effects: method

Equations: `Equations.md`; workbook formulas: `Formulas.md`. Decisions: `Old/GDP_Plan_v3_6.md`.

The model estimates how spending the revenue gained by the policies changes GDP. The change feeds back into GDP growth, which drives fuel use, power demand and the non-energy GHG drivers. The method follows legacy CPAT section 17, with legacy bug L24 fixed.

### 1. Inputs (Egypt defaults)

- Revenue use, % of revenue (ScenarioDefinition): labour tax cuts 30, corporate tax cuts 0, public investment 50, current spending 0, targeted transfers 20.
- Multiplier source (ScenarioDefinition row 226): Global, income group, Estimated or Manual; Egypt: income group (LMIC). Range Base/Low/High (row 263): Base. Start year for GDP calculations (row 236, GDPStartYear): 2025. Endogenous GDP effects: Yes.
- Fiscal multipliers by group, instrument and lag 0-19 (sheet Multipliers, from the legacy sheet: MFMod medians). Low and high are the median minus and plus one standard deviation. Lags 12-19 hold the lag-11 value, as in legacy. v0.4.15 (LD56): "Estimated" takes the country's table of the legacy Multipliers tab (rows 210-1620, exact match of the country code; the income group where the country is missing, and for CIT and WAGE, whose legacy tables are empty or wrong: bug L76); "Manual" takes sheet Manual inputs J261:U268 (legacy addresses, lags 0-11, blank = 0). Low and high add -/+ the income group's standard deviation to these too, as legacy (issue I44). Any other source text means the income group.
- Baseline real GDP (sheet WEO): 547 USD bn in 2022.

### 2. Method

1. **Fiscal space** (v0.4.15, LD55): total revenue of the scenario (existing taxes net of subsidies plus new policies, power included: rnet + rnew, v0.4.16 + subsidy reform rsr and producer subsidies rpsu, as legacy's rev.new.usd = row 8026, the total of all instruments) minus that of scenario 1, as a share of GDP. Lower fuel use also lowers the cost of existing subsidies (base erosion), and that counts. Scenario 1 has no GDP effect.
2. **Impulse** (v0.4.15, as legacy row 14356): the change of that revenue gain in USD over this year's GDP, 0 before GDPStartYear (issues I41, I42). Each impulse starts a cohort that acts for 20 years (lags 0-19), lag 0 in the impulse year (legacy applies lag 1 there: bug L68).
3. **Effect of each use**: its share x the sum of impulse x multiplier over the lags. The revenue itself counts as an energy-tax increase (instrument `exc`, share -1). The uses map to labour tax (`pit`), corporate tax (`cit`), public investment (`capt`), current spending (`gnfs`) and transfers (`trns`).
4. **GDP effect**: the sum over uses (0 if endogenous effects are off): the change of the GDP level against the baseline, as a share of GDP.
5. **Feedback**: the GDP level is 1 + last year's GDP effect, and growth follows from the baseline growth and the change in that level. The one-year lag avoids a circular reference (revenue depends on fuel use, which depends on growth). Legacy instead adds the effect to the growth rate every year, so a steady effect compounds (L24).

### 2b. Timing rule (stated v0.6.2, issue I72; user 2026-10-20)

**Revenue of year t changes GDP only from year t+1.** `gdp.lvl`(t+1) = 1 + `gdp.eff`(t), and GDP growth after the feedback reads that level (as legacy row 8776, which reads the previous column). Three consequences, kept as rules:

1. The fiscal space of year t reads revenue of year t only (no later year, no whole-row lookup).
2. A same-year GDP effect never reaches same-year demand: the impulse of year t counts at lag 0 in `gdp.eff`(t), which acts on GDP from t+1.
3. Every other block must not read a later year (NORMS, circular references). With this lag, no revenue line can then close a circular reference, whatever it reads (fuel use, power, methane).

The quick check tests the reads of later years; a change that breaks the lag must restate this rule and pass the full recalculation (Err:522).

### 3. Results for Egypt (scenario 2 of the shipped file)

| | 2027 | 2030 | 2035 | 2040 |
|---|---|---|---|---|
| Fiscal space (share of GDP) | 0.74% | 0.75% | 0.65% | 0.57% |
| GDP effect (level) | 0.00% | -0.02% | 0.17% | 0.39% |

Fiscal space jumps to about 0.75% of GDP when the policies start (v0.4.15: total revenue; v0.4.14, new-policy revenue only: 0.55% in 2030). The revenue first lowers GDP: the excise multiplier peaks two years after the impulse. From the early 2030s public investment and transfers outweigh it, and GDP ends about 0.4% above the baseline. The effect raises fuel use a little through the income elasticities.

### 4. Choices and differences with legacy (sheet LegacyDiff)

- **L24 fixed**: the effect raises the GDP level, not the growth rate every year.
- **Revenue** (v0.4.15): total revenue, as legacy (the v0.3.1 reading "new-policy revenue only" misread legacy's code rev.new.usd, which is the total). v0.6.2: the methane fee revenue is included as legacy, on the stored scenario-1 activity of downstream gas and biomass use (`ch4.revf`, issue I47: no vulnerability to circular references; none for Egypt). v0.4.16: fis.rev adds its parts (rnet + rnew + rsr + rpsu); the v0.4.15 form rtot - rmf still referenced the methane fee and LibreOffice reported a circular reference (Err:522) on a full recalculation (found by the paste test's batch emulation).
- **Impulse and start year** (v0.4.15): as legacy (I41, I42). Not replicated: legacy sets the revenue-use shares to 0 before CPIntro, so earlier impulses count only as an excise drag (I43, tiny for Egypt).
- **Legacy bugs fixed**: L68 (lag 1 in the impulse year), L69 (first cohort's excise drag lost), L76 (Estimated multipliers).
- **Scenario-1 lookups stop at the current year**, which avoids a circular reference with the GDP feedback. Values are unchanged.
- **Legacy benchmark**: the NoPropData file strips the baseline GDP-effect rows to 0, but the policy rows 14584-14607 hold the cached values of its carbon-tax run (GDP effect 2030 -0.07%, 2035 +0.34%, 2040 +1.22%; its carbon price rises to about 175 $/t in 2041, so it is not the prototype scenario). The check compares the workbook with an independent Python recomputation that iterates the whole model on the growth path until it converges (growth depends only on earlier years).

### 5. Memo rows (v0.5.7; legacy F4 rows 16163-16201)

- gdpg.<use>: contribution of each revenue use to real GDP growth: (1 + baseline growth) x (fis.eff(t-1) - fis.eff(t-2))
  / gdp.lvl(t-1) when GDPEndogenous = Yes; gdpg.all, from gdp.eff, equals gdp.pos.pct - gdp.base (the channels sum to
  it). Legacy rows 16166-16175 add the effects to growth every year (L24), so its channel values are not comparable.
- gdpy: year of the reform, N = year - GDPStartYear + 1; the growth effect of reform year N (legacy rows 16183-16194)
  is gdpg.all in the column where gdpy = N. (v0.6.0: a row shifted to later columns read forward through the GDP chain
  and made a circular reference.)
- gdp.chg.usd: real GDP after the feedback - baseline real GDP (legacy rows 16199-16201).


## Results sections of

This note covers the results that came over from legacy's post-processing (blocks E, F and G) into the scenario sections. The rules are in `excel_ai/core/NORMS.md` 3c and the plan in `Old/Plan_v3_9_to_v3_17.md`. Each later version adds its sub-block here. Every row is recomputed in Python by `check_full.py` (`check_results_memos`) in every scenario group.

### 0. Layout: summary rows

Every section ends with its summary row, the only row shown when the sheet opens rolled up; the sub-blocks below (11b, 12d, 13b, 14b, 16b) sit inside their section, before its notes and summary. Energy use (11), revenue (12), CO2 (13) and GHGs (14) have a second summary row: the change against scenario 1 (`echg.all`, `rtot.chg`, `co2.chg`, `ghg.chg`). Section 2 ends with `rpe` (average retail energy price, all energy, = `pav.uv` of all energy), section 17 with the effective carbon rate `ecr`, section 18 with the national welfare gain `wel.usd`.

### 1. Header rows (section 0)

| Row | Code | Content | Source |
|---|---|---|---|
| 11 | `gdp.usd` | Real GDP, baseline, USD bn (moved up from section 16; the code is unchanged) | Sheet WEO, legacy Mitigation row 465 |
| 12 | `gdp.lcu` | Real GDP, baseline, local currency bn | Sheet WEO, legacy Mitigation row 464 |
| 13 | `xr` | Exchange rate implied by real GDP: local currency per USD (`gdp.lcu / gdp.usd`) | Constant in real terms: 14.34 EGP per USD for Egypt |

Row 14 is real GDP growth after the GDP feedback (`gdp.pos.pct`), the summary row of section 0; rows 1-5 (years, title, band 0, scenario name, scenario number) are frozen. Every % of GDP row (12d, 16) uses `gdp.usd`. It is data, so not circular (Q24).

**Not built: nominal GDP (WEO `NGDP`, `NGDPD`).** The legacy file holds no nominal series: its rows 470-472 are empty in the NoPropData file. Nominal GDP waits until WEO data are added to the data step (TODO). This is a decision taken during the run, to confirm.

### 2. 12d Fiscal reports (v0.3.13; legacy section 16 info rows, F9)

**Revenue by fuel, net of subsidies (USD m real).** Each fuel covers existing taxes, subsidies and new-policy revenue:
- `rfu.<fuel>`: `rtx + rsub + rnew` of the fuel over all subsectors. The formula is `SUMPRODUCT(SUMIFS(..., SecVar, {"rtx","rsub","rnew"}, SecFuel, fuel))`.
- `rfu.ecy`: electricity, i.e. VAT, the subsidy gap and VAT on the policy cost passed through (`rvat + rgap + rnvat`, section 3 G).
- `rfg.<type>`: fuels burnt in power generation (coal, gas, oil, biomass): `prtx + prxc + prsub + prnew` of the type (section 3 M; Q28).
- `rfu.chk`: `ABS(sum of the rows - rnet.all - rnew.all)`. It is 0, because the rows split the section 12 totals exactly. The methane fee (`rmf`) is not a fuel revenue.

**12e. Total revenue by policy (v0.4.15, LD37; legacy rows 8016-8027, USD m real).** The legacy split of total revenue by instrument:
- `rpol.ct` new carbon tax = `SUMPRODUCT(covct, ctr)` over the coverage sectors (covered CO2 x the sector's carbon tax rate; power included); `rpol.ets` auctioned ETS = `SUMPRODUCT(co2.sec, etr) x ets.rf`; of which power: `rpol.ctp`, `rpol.etp`.
- `rpol.exc` new excise (fuel price reform) = the per-pair rows `rex` (fuel use x PJ/ktoe x `ntx`) + power `prnew` - `ctp` - `etp`.
- `rpol.vat` VAT = the per-pair rows `rvt` (fuel use x PJ/ktoe x (vat + (xcpd + nce) x VAT rate)) + electricity VAT (`rvat`, `rnvat`).
- `rpol.psu` producer subsidies = the electricity subsidy gap (`rgap`, legacy E for electricity; oil, coal and gas producer subsidies follow with LD19).
- `rpol.exi` existing taxes and subsidies = `rnet + rnew` - the rows above (fuel use x (excise + change in existing carbon pricing) + consumer subsidies + power fuel taxes and subsidies).
- `rpol.ren` renewable subsidies and `rpol.trs` transport revenues: 0 (not modelled; issue I46); `rpol.mf` methane fee = `rmf`; `rpol.tot` = their sum = `rtot` (check row `rpol.chk`).
Egypt, carbon tax scenario, 2030: carbon tax 4.2 bn USD (power 1.8), existing taxes and subsidies -10.3 bn, electricity subsidy gap -10.0 bn, total -16.1 bn. Legacy bugs L70-L73 and L75 do not arise (each pair takes its own rates, uses and coverage).

**Revenue against GDP and base erosion.**
- `rbe`: base erosion, i.e. `rnet - rnet of scenario 1` in the same year. This is the change in existing taxes net of subsidies when a policy changes fuel use (Q25: policy fuel use x baseline tax rates, against baseline revenue). Egypt, carbon tax scenario, 2030: about +1.5 bn USD. Fuel use falls, so subsidies (negative) shrink more than existing taxes.
- `rpct.<x>`: shares of baseline real GDP, via `GDPSHARE` in the LAMBDA column. They cover:
  - total revenue;
  - existing taxes net of subsidies;
  - subsidies;
  - new-policy revenue;
  - change in total revenue against scenario 1;
  - base erosion.

  Egypt 2022: total revenue -8.6% of GDP, because consumer subsidies exceed taxes.

MTOutputs rows: `rpct.all.tot`, `.chg`, `.sub`, `.be`; `rbe.all.all`.

**Not built (TODO; decisions taken during the run, to confirm):**
- **Producer subsidies (Q26).** There are no data for Egypt, and NORMS 3c bars zero placeholders.
- **Revenue lost to price controls (Q29).** Legacy holds only pass-through coefficients (rows 746-760, 2216-2220), not a revenue row.
- **Fuel expenditures.** These are the spending rows of the section 2 memo (`pav.sp`, v0.3.10), so they are not repeated here.
- **Vehicle revenues of the road engineer model in 12b (Q27).** Planned for later.

### 3. 11b Energy consumption: change against scenario 1 (v0.3.14; legacy F7)

`echg` rows give the change against scenario 1 in the same year, in ktoe. The levels come from section 11:
- by fuel, from the fuel rows (power generation fuels included);
- by sector group, from the sector totals of sections 5-8;
- power generation fuel use;
- the total.

The change is read through helper row 10 (`INDEX(scenario 1 .. this column, position of scenario 1's year)`).

`epct` rows give the % change: `echg / (level - echg)`, and 0 when scenario 1 is 0.

Not as rows: the energy-balance matrix (legacy G; Q30). It is a rearrangement of section 11 and goes to an output sheet later.

### 4. 13b CO2 change, grid emission intensity, Kaya identity (v0.3.14; legacy F13, row 6582, F14)

**CO2 change.** `cchg` gives the change of CO2 from fuel combustion against scenario 1, by fuel and by sector group, power included (MtCO2).

**Grid intensity.** `co2.grid` = CO2 of power generation x Million / (total generation in MWy x `HoursYr`), in tCO2 per MWh. Egypt: 0.41 in 2022 (legacy 0.38) and 0.33 in 2030.

**Kaya identity (legacy rows 18877-18893), as legacy (v0.3.18):**
- **GDP:** baseline real GDP (the header row), in every scenario.
- **CO2:** total CO2 including industrial processes (`ghg.g.co2`).
- **Energy:** total primary energy supply, `kaya.tpes` (legacy row 18880). It is the fuel use of section 11 (fuels burnt in power plants included, biomass included), plus primary electricity: the energy input `pe` of nuclear, wind, solar, hydro and other renewables in section 3. The input is generation divided by the type's efficiency (physical energy content method: nuclear at 38%, renewables at about 1). Egypt 2022: 89,471 ktoe = legacy 89,471. Energy intensity 163.57 ktoe per USD bn = legacy.

  v0.3.14-v0.3.17 used fuel use only (2.6% lower in 2022). This was corrected at the user's request (2026-10-16). Legacy's broken "simplified Kaya" row (18931, -97%) is a different row and is not used.

`kaya.*` levels:

| Row | Content | Unit |
|---|---|---|
| `kaya.pop` | Population | mn |
| `kaya.gpc` | GDP per capita | thousand USD |
| `kaya.tpes` | Total primary energy supply | ktoe |
| `kaya.ei` | Energy intensity | ktoe per USD bn |
| `kaya.ci` | Carbon intensity | ktCO2 per ktoe |

`kidx.*` indices against the base year of scenario 1: population, GDP, GDP per capita, energy intensity, carbon intensity, CO2. `kidx.chk` is the product of the four factors and equals the CO2 index exactly.

Egypt 2030:
- baseline: CO2 x1.17, with energy intensity 0.81 and carbon intensity 1.03;
- carbon tax: energy intensity 0.74, CO2 x1.10.

The efficiencies of wind (1.004), solar (1.026) and hydro (0.937) are legacy's power data, kept (issue I93).

Population is the prototype's UN series: 111.7 mn in 2022, against legacy's 103.6 mn (legacy bug L20, fixed). GDP per capita is therefore lower than in legacy, and the identity still holds.

LAMBDA `SAFEDIV` (amount / activity, 0 when the activity is 0) is used in the LAMBDA column.

### 5. 14b GHG change and energy GHGs including forcing (v0.3.14; legacy F12)

**GHG change.** `gchg` gives the change against scenario 1 by inventory category (energy, industrial processes, agriculture, LULUCF, waste, other) and by gas (Mt CO2e).

**Broad sectors.** Legacy's "GHG by broad sector" (rows 18229-18243) is the inventory categories, which section 14 already has. No allocation of CH4 and N2O to sectors is needed (Q32).

**Energy GHGs with forcing.** `ghg.enrp` = energy GHGs + the forcing of the local pollutants (`apf.all`, section 15): legacy "Total GHGs and PM", rows 18310 and 18321.

**Later:** the NDC comparison (Q33; needs the NDC table).

### 6. Section 17 Carbon pricing (v0.3.15; legacy F3, F5d-e)

**Implicit carbon price by fuel (`cpi.<fuel>`, USD per tCO2).** Revenue net of subsidies of the fuel, divided by its CO2:
- revenue: existing taxes + subsidies + new policies, final use (`rfu`) and power generation (`rfg`);
- CO2: from section 13.

This is legacy's "total carbon price" by fuel (F5d), which divides the tax-and-subsidy wedge per GJ by the emission factor. `cpi.all` is the same over the fossil fuels.

Biomass is left out (Q34): it has no CO2, and legacy gives `#DIV/0!`. Egypt 2022: gas -151, diesel -249, LPG -280, all fossil fuels -179 USD per tCO2 (subsidies). A carbon tax of 20 USD raises every fuel by about 20.

**Effective carbon rate (`ecr`, legacy row 16662).** `(rnet + rnew) / energy CO2`, as legacy, so VAT, the electricity subsidy gap and electricity VAT count (issue I36: the OECD rate counts carbon taxes, excises and permit prices only). Egypt 2022: -207 USD per tCO2 (legacy -122; the price data differ).

**Effective carbon tax (`cpeff`, legacy row 16137).** Carbon price x the share of energy CO2 it covers.

**Coverage.**
- `covct.<sector>`: CO2 covered by the new carbon tax in each of the 17 coverage sectors. It is the CO2 of the fuels whose switch is on (`fc` rows), counted only where the sector's carbon-tax rate is above 0. A sector in a non-complementary ETS has none. Power uses the CO2 of coal, gas and oil generation.
- `cov.ct.<group>`, `cov.ct.all`: shares of national energy CO2 (legacy rows 16152-16157). Egypt, carbon tax scenario, 2030: 99.8% (legacy 98.8%), of which power 41%.
- `cov.ets`: ETS coverage share (from `co2.ets`).
- `cov.all`: their sum.

The `cpi`, `ecr`, `cpeff` and coverage-share rows call `SAFEDIV` / `SCALEBY` in the LAMBDA column.

MTOutputs: `cpi.all.all`, `ecr.all.all`, `cpeff.all.all`, `cov.all.all.all`.

### 7. 16b External balance (v0.3.16; legacy F11, data rows 741-743)

Section 16 is renamed "GDP effects and external balance" (Q39).

**Data.** Legacy Mitigation rows 741-743 give the energy trade balance (exports - imports, USD bn real) of gas, oil products and coal, with their share traded: gas 0.19, oil products 0.47, coal 1.0. They are extracted by `extract_gdp` into sheet WEO (`EGY|tb_<group>`, `EGY|ts_<group>`).

**Change in net imports (`xnim`, USD bn real; Q37).** By fossil fuel: change in use (11b, `echg`) x PJ per ktoe x supply price (section 2, `sp`, $/GJ) x the share traded of the fuel's group (column D) / MperBn. Prices used:
- coal and gas: the industry supply price;
- jet fuel: kerosene;
- other fuels: their own `.all` price code.

The rows are summed by group (oil, gas, coal) and in total. Egypt, carbon tax 20 USD, 2030: -1.2 bn USD (oil -0.93).

Legacy leaves the share out for oil (bug L49, fixed), so its oil effect is about twice as large.

**Trade balance.**
- `xtb.<group>`, `xtb.all`: the baseline energy trade balance (data). Egypt 2022: -6.7 bn USD.
- `xtbp`: the scenario's balance, `xtb.all - xnim.all`.
- `xtb.pct`, `xnim.pct`: shares of baseline real GDP (`SAFEDIV`).

Legacy's balance-of-payments panel (rows 18195-18219) is not replicated (bug L50):
- its pre-policy current account is `#NAME?`;
- its rows lag one column, so it shows the 2021 balance (-5.85) in 2022;
- the sign of its policy net imports looks reversed.

The current-account level (WEO `BCA`, Q38) waits for WEO data in the data step.

MTOutputs: `xnim.all.all`, `xtbp.all.all`, `xtb.pct.all.all`.

### 8. Section 18 Welfare and externalities, climate part (v0.3.17; legacy F10, rows 17392-17742)

**Settings (rows 32-42; legacy rows 17671-17677).** Defaults as legacy:

| Setting | Default |
|---|---|
| Target-consistent price `SCCTgt` | 75 USD per tCO2 real |
| Its year `SCCTgtYr` | 2030 |
| Real growth `SCCGr` | 4% a year |
| National and global SCC source (`NSCCSrc`, `GSCCSrc`) | Target. The choices are Target, Ricke, Manual, EPA |
| Ricke et al. (2018) settings | pure rate of time preference 2, elasticity 1p5 |
| US EPA SCC in the base year | 62 |

**SCC options (Q40; legacy rows 17680-17713).** Egypt 2022 values are given.

| Option | Formula | Egypt 2022 |
|---|---|---|
| `scc.tgt` | SCCTgt x (1 + SCCGr)^(year - SCCTgtYr) | 54.8 |
| `scc.rkn` | Ricke national value (new data sheet `SCC`, key `egy.2.1p5`) x (1 + SCCGr)^(year - base year) | 6.87 |
| `scc.rkg` | Ricke global value (`wld.2.1p5`), same growth | 462 |
| `scc.man` | manual path: 'Manual inputs' row 237 (v0.5.2, L103 fixed; legacy reads the path typed on Mitigation row 17683) | 50.0 in 2025, +4% a year |
| `scc.epa` | US EPA value, same growth | 62 |
| `scc.nat`, `scc.glo` | the selected options (CHOOSE) | |

All equal legacy.

**Climate damages.**
- `dmg`: SCC x GHG excl. LULUCF (section 14), USD bn. Egypt 2022: 22.9 bn, against legacy's 22.0, because the inventories differ slightly.
- `wcli`: damages of scenario 1 - damages of the scenario, i.e. the damages avoided (national, global).

**Efficiency (deadweight) costs of energy (Q41; legacy rows 17636-17648).** For each fuel, power generation fuels included, and electricity:
- tax wedge `wdg` = revenue net of subsidies per unit of use (USD m per ktoe; 12d rows / section 11 use; electricity: `rfu.ecy` / electricity demand);
- cost `eff` = -(wedge + wedge of scenario 1) / 2 x change in use / MperBn (LAMBDA TRAPEZOID).

This is legacy's trapezoid: Harberger triangle + rectangle. With subsidies (negative wedges), a fall in use is a gain. Egypt, carbon tax 20 USD, 2031: -1.25 bn USD (gain), mostly electricity and diesel.

Legacy bugs not replicated:
- the LPG pre-existing tax row is empty (the LPG average tax is halved);
- diesel and kerosene are converted with the wrong factors;
- the coal row is offset;
- non-road oil is `#N/A`.

**Efficiency costs of the methane fee (Q43; legacy rows 17628-17634, "integral").** For each methane source:
- `mfp`: the fee per t CH4 used on the abatement curve, capped where abatement reaches 1 (MFEEPRICE);
- `mfc`: the area under the abatement curve, a x fee^b, i.e. unabated emissions x abated share x price x b / (1 + b) / Million (MFEECOST).

The fee is 0 in the shipped scenarios. A test with a fee of 50 USD per tCO2e agrees with the Python recomputation.

**Welfare summary (national; legacy rows 17727-17742).**
- `wel.usd` = avoided national damages - efficiency costs of energy - methane-fee costs;
- `wel.pct`, `wel.cli`, `wel.eff`: shares of baseline real GDP.

Egypt, carbon tax 20 USD, 2031: +3.2 bn USD (0.39% of GDP).

**Not as rows (Q42, NORMS 3c):** the air-pollution and transport co-benefits, externalities per unit, explicit and implicit subsidies, efficient prices. They come with their modules.

MTOutputs: `scc.all.nat`, `wcli.all.nat`, `eff.all.all`, `mfc.all.all`, `wel.all.usd`, `wel.all.pct`.


## Multiple scenarios: definitions, batch run, stored results, comparison

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

The model calculates a few scenarios at a time: the baseline and the live policy scenario (and any scenario group added by copy-paste). Since 1.2.0 the macros and the stored results are in the **Master workbook** (`excel_ai/active_workbooks/CPAT-AI-Master_UserGuide.xlsm`; the mitigation workbook has no macros). Its batch run copies each scenario definition into the live scenario of the activated mitigation workbook, calculates it and stores its results as values, which are compared afterwards. This follows legacy CPAT, where a macro copies each scenario column into the column used for calculation and stores the outputs.

### 1. Where things are

| Place | What it holds |
|---|---|
| ScenarioDefinition, column J (scenario 1) | The **baseline**. |
| ScenarioDefinition, column K (scenario 2) | The **live policy scenario**. The batch run overwrites it with each definition and restores it at the end. |
| ScenarioDefinition, columns L onwards | **Scenario definitions**, one full column each: short name (row 2, the legend in the charts), Run? (Yes/No), number, name, then the inputs. Red cells differ from the template. To add one, copy the last definition one column to the right and edit it. |
| Mitigation | Scenario groups: 1 = the baseline (plain formulas), 2 = the live scenario (every calculated cell calls its named LAMBDA). More live scenarios: copy group 2 to the right and set its scenario number. |
| MTOutputs | The key results of every scenario group **side by side**, in the columns of Mitigation's groups (room for four): columns A:J code stem, module, legacy code, indicator, unit, Mitigation row; row 5 the scenario number of each group; rows as legacy MTOutputs, then the outputs legacy does not list, by topic. Each cell is Mitigation's cell of its row in the same column. |
| FromMaster | What the Master wrote here (values): activation, the data source of the linked tables, the rows loaded. |
| Master: StoredScenarios | Results as **values only**: MTOutputs' rows at the same row numbers, ten slots (slot 1 the baseline), each with its scenario ID, name and when and from which file it was stored. |
| Master: CompareStored | The stored scenarios against the first slot (the baseline), for a chosen year. |
| Master: VBA module CPATMaster | Every macro (source `excel_ai/master/CPATMaster.bas`). |

### 2. Shipped definitions

| No. | Name | Inputs changed from the template |
|---|---|---|
| 3 | Carbon price $20/tCO2 from 2027 | The live scenario's settings |
| 4 | Package A: carbon tax to $50 by 2030 + feebates (transport, industry) | Carbon tax $10 (2027) to $50 (2030). Feebates 2027-2030: transport $10 → $50, industry $5 → $25. Feebate coverage adds road, mining & chemicals, and iron & steel |
| 5 | Package B: ETS on power and industry + carbon tax $25 elsewhere | Carbon tax $25 from 2027. New ETS from 2027: cap −5% (2027) to −20% (2035) of baseline covered emissions, constant afterwards. Template ETS coverage (power, mining & chemicals, iron & steel, non-ferrous metals, cement), default benchmarks and volatility |
| 6 | Carbon price $50/tCO2 from 2027 | The carbon price of definition 3 at $50 |

Paths continue after their target year as set in the model: the carbon price follows its ScenarioDefinition switch, and feebates continue linearly.

### 2b. Main scenario choice and regulations as shadow prices (v0.4.16, LD9)

ScenarioDefinition row 13 (`ScenarioSelected`, " - Carbon tax" in every shipped scenario) picks a row of the legacy scenario table (legacy Mitigation rows 222-262, columns N:AC; sheet Mapping, block "Main scenarios"): whether the scenario prices carbon explicitly (legacy row 259), its efficiency adjustment (ScenarioDefinition rows 247-251) and the sectors its shadow price covers (rows 240-257).

- Explicit scenarios (carbon tax, total carbon price, coal excise, road fuel tax, electricity emissions tax and excise): the carbon price path of ScenarioDefinition rows 18-21 is the carbon tax (`cpx` = `cptraj`), as before.
- Shadow-pricing scenarios (feebates, power supply feebates, energy efficiency regulations, power feebate, vehicle fuel economy, residential and industrial efficiency regulations; and "Baseline"): no explicit carbon tax (`cpx` = 0); the carbon price path becomes a shadow price on the efficiency margin, `reg.<sector>` = `cp.shd` x the scenario's adjustment (energy efficiency 247, vehicle fuel economy 248, residential 249, industrial 250, feebates 251; Egypt 0.7, feebates 1) x 1 if the scenario covers the sector. It enters `shpx` (with the feebate part, now x row 251, and the ETS benchmark part), so fuel use responds through efficiency only, and power through `shk` (legacy bugs L87, L88 fixed: legacy's regulation share is 0 and never reaches power).
- The road vehicle feebate of the engineer road model adds `reg.rod` (the road regulation shadow price) instead of the carbon price, which is in the fuel price already (prototype bug M13).
- A text that is not in the table counts as explicit pricing (as the shipped " - Carbon tax").

### 2b. Main scenario choice and regulations as shadow prices (v0.4.16, LD9)

ScenarioDefinition row 13 (`ScenarioSelected`, " - Carbon tax" in every shipped scenario) picks a row of the legacy scenario table (legacy Mitigation rows 222-262, columns N:AC; sheet Mapping, block "Main scenarios"): whether the scenario prices carbon explicitly (legacy row 259), its efficiency adjustment (ScenarioDefinition rows 247-251) and the sectors its shadow price covers (rows 240-257).

- Explicit scenarios (carbon tax, total carbon price, coal excise, road fuel tax, electricity emissions tax and excise): the carbon price path of ScenarioDefinition rows 18-21 is the carbon tax (`cpx` = `cptraj`), as before.
- Shadow-pricing scenarios (feebates, power supply feebates, energy efficiency regulations, power feebate, vehicle fuel economy, residential and industrial efficiency regulations; and "Baseline"): no explicit carbon tax (`cpx` = 0); the carbon price path becomes a shadow price on the efficiency margin, `reg.<sector>` = `cp.shd` x the scenario's adjustment (energy efficiency 247, vehicle fuel economy 248, residential 249, industrial 250, feebates 251; Egypt 0.7, feebates 1) x 1 if the scenario covers the sector. It enters `shpx` (with the feebate part, now x row 251, and the ETS benchmark part), so fuel use responds through efficiency only, and power through `shk` (legacy bugs L87, L88 fixed: legacy's regulation share is 0 and never reaches power).
- The road vehicle feebate of the engineer road model adds `reg.rod` (the road regulation shadow price) instead of the carbon price, which is in the fuel price already (prototype bug M13).
- A text that is not in the table counts as explicit pricing (as the shipped " - Carbon tax").

### 3. Macros (in the Master)

Buttons on the Master's tab `UserGuide` (green); also Alt+F8.

- **ActivateAll / ActivateMitigation / ActivateDistribution / ActivateAirPollution**: open the module's latest `.xlsx` (the local repository copy, else its GitHub link), copy the 2035 column across to 2041 on the sheets listed in the module table (Mitigation and MTOutputs), write `FromMaster`, recalculate fully (twice) and save `<Name>_latest.xlsb` next to the Master. The workbook stays open.
- **RunStoredScenarios** (button Run stored scenarios): stores the baseline if none is stored yet. Then, for every definition with Run? = Yes, it copies the definition's inputs and name into the live column K of the activated mitigation workbook, recalculates, runs the ETS goal seek if the definition applies a new ETS without "Override ETS price" = Yes, and stores the live scenario's MTOutputs group as values under the definition's number (replacing that ID's slot, else the next free one). At the end it restores the live column; the mitigation workbook is not saved.
- **StoreLiveScenarios**: stores every scenario group of MTOutputs as it stands (after a recalculation) in the next free slots.
- **ClearStoredScenarios**: empties every slot but the first (the baseline), after a confirmation.
- **UpdateDataTables**: refreshes the linked data tabs of the activated mitigation workbook from the source chosen on the Master's tab `Settings` (Power Query; the rows of the country, or every country), writes the choice on `FromMaster` and saves it.
- **UpdateDistributionFromMitigation**: copies section 19a (`ExportDistn`) of the activated mitigation workbook into `FromMitigation` of the activated distribution workbook, by code (it stops if the rows do not match), recalculates and saves it.

The ETS goal seek is legacy's damped log-space iteration, as in `ets_goalseek.py`. It starts from the override prices, or from the fast estimate if there are none. Each step is p × (proposed price / p) ^ alpha, mixed 0.3 with the previous iterate, with 5% smoothing. Alpha halves when the error grows (minimum 0.0625) and rises ×1.2 when the error more than halves (maximum 1). It stops when the worst |covered / cap − 1| is below 0.5%, or after 20 iterations.

### 4. First run in Excel

The Master and its VBA were built without Excel; the build checks that the VBA compiles in LibreOffice, and the checks emulate the activation in Python (identical to the full build, every formula). Activation of Mitigation has passed its first run in Excel (2026-10-31: the activated workbook equals the release values to 2035). The other macros are still to be run in Excel (`excel_ai/core/USER_TASKS.md` 17-18):

1. If the Master was downloaded, unblock it first (file Properties > Unblock), or Excel opens it with macros disabled.
2. Open it, choose Enable Content, and run Debug > Compile VBAProject (Alt+F11).
3. Activate the modules, then try Update data tables, Update Distribution from Mitigation, Store live scenarios and Run stored scenarios; report anything odd, with a screenshot.

### 5. Comparing and keeping results

- **Live** (in the mitigation workbook): Outputs (was MTOutputs) holds every live scenario group side by side; the dashboard tab ScenarioCompare was deleted in 1.2.2 (user 2026-10-31): the Master compares.
- **Key table.** Energy CO2 emissions, GHG emissions excluding LULUCF, revenue as a share of GDP, the GDP effect of the revenue use and the net welfare effect: level, difference from the baseline, and % difference for the two emission levels.
- **Time series.** Four tables (default: energy CO2, GHGs, revenue, GDP effect), scenarios down and years across, each with its line chart beside it. The title of each table is a dropdown of the indicator list: every MTOutputs indicator except the price and Kaya indices.
- **Stored** (in the Master): StoredScenarios keeps up to ten scenarios as values, so results of other runs (another country, another version) can sit side by side, as long as the rows are those of the same MTOutputs version (the store macros check the code stems). CompareStored compares them with slot 1.

### 6. Limits

- The batch run calculates one policy scenario at a time, through the live column K. Further scenario groups of Mitigation (copies of group 2) show on Outputs, and Store live scenarios stores them.
- MTOutputs defines what is stored: its rows, each code once. To store more, add rows to MTOutputs first (in the builder).
