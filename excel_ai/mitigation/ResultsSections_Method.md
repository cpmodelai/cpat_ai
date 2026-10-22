# Results sections of CPAT-AI-Mitigation-Prototype v6.4

This note covers the results that came over from legacy's post-processing (blocks E, F and G) into the scenario sections. The rules are in `../NORMS.md` 3c and the plan in `Old/Plan_v3_9_to_v3_17.md`. Each later version adds its sub-block here. Every row is recomputed in Python by `check_full.py` (`check_results_memos`) in every scenario group.

## 0. Layout: summary rows

Every section ends with its summary row, the only row shown when the sheet opens rolled up; the sub-blocks below (11b, 12d, 13b, 14b, 16b) sit inside their section, before its notes and summary. Energy use (11), revenue (12), CO2 (13) and GHGs (14) have a second summary row: the change against scenario 1 (`echg.all`, `rtot.chg`, `co2.chg`, `ghg.chg`). Section 2 ends with `rpe` (average retail energy price, all energy, = `pav.uv` of all energy), section 17 with the effective carbon rate `ecr`, section 18 with the national welfare gain `wel.usd`.

## 1. Header rows (section 0)

| Row | Code | Content | Source |
|---|---|---|---|
| 11 | `gdp.usd` | Real GDP, baseline, USD bn (moved up from section 16; the code is unchanged) | Sheet WEO, legacy Mitigation row 465 |
| 12 | `gdp.lcu` | Real GDP, baseline, local currency bn | Sheet WEO, legacy Mitigation row 464 |
| 13 | `xr` | Exchange rate implied by real GDP: local currency per USD (`gdp.lcu / gdp.usd`) | Constant in real terms: 14.34 EGP per USD for Egypt |

Row 14 is real GDP growth after the GDP feedback (`gdp.pos.pct`), the summary row of section 0; rows 1-5 (years, title, band 0, scenario name, scenario number) are frozen. Every % of GDP row (12d, 16) uses `gdp.usd`. It is data, so not circular (Q24).

**Not built: nominal GDP (WEO `NGDP`, `NGDPD`).** The legacy file holds no nominal series: its rows 470-472 are empty in the NoPropData file. Nominal GDP waits until WEO data are added to the data step (TODO). This is a decision taken during the run, to confirm.

## 2. 12d Fiscal reports (v3.13; legacy section 16 info rows, F9)

**Revenue by fuel, net of subsidies (USD m real).** Each fuel covers existing taxes, subsidies and new-policy revenue:
- `rfu.<fuel>`: `rtx + rsub + rnew` of the fuel over all subsectors. The formula is `SUMPRODUCT(SUMIFS(..., SecVar, {"rtx","rsub","rnew"}, SecFuel, fuel))`.
- `rfu.ecy`: electricity, i.e. VAT, the subsidy gap and VAT on the policy cost passed through (`rvat + rgap + rnvat`, section 3 G).
- `rfg.<type>`: fuels burnt in power generation (coal, gas, oil, biomass): `prtx + prxc + prsub + prnew` of the type (section 3 M; Q28).
- `rfu.chk`: `ABS(sum of the rows - rnet.all - rnew.all)`. It is 0, because the rows split the section 12 totals exactly. The methane fee (`rmf`) is not a fuel revenue.

**12e. Total revenue by policy (v4.15, LD37; legacy rows 8016-8027, USD m real).** The legacy split of total revenue by instrument:
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

LiveOutputs rows: `rpct.all.tot`, `.chg`, `.sub`, `.be`; `rbe.all.all`.

**Not built (TODO; decisions taken during the run, to confirm):**
- **Producer subsidies (Q26).** There are no data for Egypt, and NORMS 3c bars zero placeholders.
- **Revenue lost to price controls (Q29).** Legacy holds only pass-through coefficients (rows 746-760, 2216-2220), not a revenue row.
- **Fuel expenditures.** These are the spending rows of the section 2 memo (`pav.sp`, v3.10), so they are not repeated here.
- **Vehicle revenues of the road engineer model in 12b (Q27).** Planned for later.

## 3. 11b Energy consumption: change against scenario 1 (v3.14; legacy F7)

`echg` rows give the change against scenario 1 in the same year, in ktoe. The levels come from section 11:
- by fuel, from the fuel rows (power generation fuels included);
- by sector group, from the sector totals of sections 5-8;
- power generation fuel use;
- the total.

The change is read through helper row 10 (`INDEX(scenario 1 .. this column, position of scenario 1's year)`).

`epct` rows give the % change: `echg / (level - echg)`, and 0 when scenario 1 is 0.

Not as rows: the energy-balance matrix (legacy G; Q30). It is a rearrangement of section 11 and goes to an output sheet later.

## 4. 13b CO2 change, grid emission intensity, Kaya identity (v3.14; legacy F13, row 6582, F14)

**CO2 change.** `cchg` gives the change of CO2 from fuel combustion against scenario 1, by fuel and by sector group, power included (MtCO2).

**Grid intensity.** `co2.grid` = CO2 of power generation x Million / (total generation in MWy x `HoursYr`), in tCO2 per MWh. Egypt: 0.41 in 2022 (legacy 0.38) and 0.33 in 2030.

**Kaya identity (legacy rows 18877-18893), as legacy (v3.18):**
- **GDP:** baseline real GDP (the header row), in every scenario.
- **CO2:** total CO2 including industrial processes (`ghg.g.co2`).
- **Energy:** total primary energy supply, `kaya.tpes` (legacy row 18880). It is the fuel use of section 11 (fuels burnt in power plants included, biomass included), plus primary electricity: the energy input `pe` of nuclear, wind, solar, hydro and other renewables in section 3. The input is generation divided by the type's efficiency (physical energy content method: nuclear at 38%, renewables at about 1). Egypt 2022: 89,471 ktoe = legacy 89,471. Energy intensity 163.57 ktoe per USD bn = legacy.

  v3.14-v3.17 used fuel use only (2.6% lower in 2022). This was corrected at the user's request (2026-10-16). Legacy's broken "simplified Kaya" row (18931, -97%) is a different row and is not used.

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

The efficiencies of wind (1.004), solar (1.026) and hydro (0.937) are legacy's power data, kept (issue I37).

Population is the prototype's UN series: 111.7 mn in 2022, against legacy's 103.6 mn (legacy bug L20, fixed). GDP per capita is therefore lower than in legacy, and the identity still holds.

LAMBDA `SAFEDIV` (amount / activity, 0 when the activity is 0) is used in the LAMBDA column.

## 5. 14b GHG change and energy GHGs including forcing (v3.14; legacy F12)

**GHG change.** `gchg` gives the change against scenario 1 by inventory category (energy, industrial processes, agriculture, LULUCF, waste, other) and by gas (Mt CO2e).

**Broad sectors.** Legacy's "GHG by broad sector" (rows 18229-18243) is the inventory categories, which section 14 already has. No allocation of CH4 and N2O to sectors is needed (Q32).

**Energy GHGs with forcing.** `ghg.enrp` = energy GHGs + the forcing of the local pollutants (`apf.all`, section 15): legacy "Total GHGs and PM", rows 18310 and 18321.

**Later:** the NDC comparison (Q33; needs the NDC table).

## 6. Section 17 Carbon pricing (v3.15; legacy F3, F5d-e)

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

LiveOutputs: `cpi.all.all`, `ecr.all.all`, `cpeff.all.all`, `cov.all.all.all`.

## 7. 16b External balance (v3.16; legacy F11, data rows 741-743)

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

LiveOutputs: `xnim.all.all`, `xtbp.all.all`, `xtb.pct.all.all`.

## 8. Section 18 Welfare and externalities, climate part (v3.17; legacy F10, rows 17392-17742)

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
| `scc.man` | manual path: 'Manual inputs' row 237 (v5.2, L103 fixed; legacy reads the path typed on Mitigation row 17683) | 50.0 in 2025, +4% a year |
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

LiveOutputs: `scc.all.nat`, `wcli.all.nat`, `eff.all.all`, `mfc.all.all`, `wel.all.usd`, `wel.all.pct`.
