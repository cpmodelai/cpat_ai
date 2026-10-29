# air pollution module (legacy sheet Air pollution and its 9 data tabs)

Status: planned, not built (user 2026-10-19: data tabs in the prototype workbook). Decisions for the user in section 7 (the key one: legacy bug B1, adult-disease incidence applied to the 25+ population, which roughly halves the adult burden; by the replication rule a bug is fixed, but the fix about doubles wel.air for Egypt and interacts with the optional Adjust-to-GBD factor). Research below: legacy structure, data tabs, settings, cached Egypt values, bugs and issues, prototype mapping, step plan.

## 1. Legacy `Air pollution` sheet

**Geometry.** Rows 1-4,780, columns A-AR. A-J are descriptors and helpers (C variable, D pollutant/area, E unit, F note, G input code, H output code, I-J MATCH helpers). The years run from **K = 2022 to AC = 2040**, with a few rows to AD = 2041. Mitigation L (2022) maps to AP K.
- The sheet holds **one baseline block and one policy block**. The policy block is the scenario in Dashboard!D647 `ScenarioNum` (= 2), with H891 = 1 and H1724 = 2.
- Codes are `egy.air.<metric>.<pollutant>.<risk>.<age>.<area>.<scen>`.
- About **62,200 formula cells**, 16,700 of them array formulas, mostly `INDEX/MATCH` helpers.

| Block | Rows | Formula cells / rows | What it computes |
|---|---|---|---|
| A | 1-8 | 21 / 2 | Title, years |
| B1 settings | 26-103 | small | Options read from ScenarioDefinition and Dashboard (section 3), and typed parameters: β WDL 0.0046 (Ostro), TMREL WDL 0; β O3 0.005827, TMREL O3 32.4 ppb; β depression 0.009713, counterfactual 25 µg/m3; TMREL GBD 4.15; median OECD VSL; working days 20; labour share 0.65; max solid-fuel share 0.99; leakage 0.5; cessation lag Yes; TCRE 0.4; GBD adjustment No. Disability weights for 6 diseases with wage factor = DW / 0.4 (rows 96-103). VSL base table by income group (rows 45-51, typed, 2022 PPP: LMI 1.1 mln USD with GDP per capita 13,580) |
| B2 hand-off copies | 105-361 | ~3,950 | Copies of Mitigation E3 (15827-16078): power and residential fuel use (e.1 / e.2), food shares, emissions of 10 pollutants × 8 sectors in t/yr for baseline (149-249) and policy (251-353), CO2 and GWP100 (357-361) |
| B3 exposure and population | 363-436 | | Observed PM2.5 OAP urban, rural and all, O3, HAP level (GBD). HAP level and share-exposed paths are quadratics a·t²+b·t+c (ExposureCoefs), capped at the base year. Urban share (WB). Population by 16 age groups = UNPop total × GBD base-year age structure (fixed). Neonatal population |
| B4 emissions to concentrations | 437-522 | 162 array | Coefficients in µg/m3 per t from ConcMat for 7 sectors × 9 pollutants, PM2.5 (column F) and O3 (column G), by the method selected (TM5-FASST is per pollutant only; the other methods are per sector) |
| B5 RR and adjustment tables | 524-542 | typed | GBD 2021 RR grid: 21 concentration points (2000 … 0) × ihd, str, lun, cop, dme, lri, lbw, ptb. GBD adjustment factors (ExposureCoefs `fact.dth`, `fact.dly`) |
| B6 incidence | 544-700 | | Base-year incidence per 10^5 by metric (dth, YLL, YLD) × disease × age (GBD). Baseline deaths, YLL and YLD by disease and age. λ_TMREL = incidence / (p_H·RR_hop + (1-p_H)·RR_oap) at base-year RR (rows 672-700, named `lambda_tmrel` W672:Y701). O3 and depression λ |
| B7 VSL | 702-749 | | WEO and deflators. VSL options: GNI×100, GNI×160, transfer from group (PPP, then USD), manual. Selected VSL in row 741. Cessation lag 30% / 4×12.5% / 15×1.33%, discounted, factor 0.906 (`time_factor` K749) |
| B8 productivity, WDL, health spending | 751-889 | | Discount-rate options (3). Survival probabilities (Air_Data). PV of forgone output by age (ILO output growth). Working days lost per person (Air_Data). Daily earnings (ILO). Health spending (IHME) × DALY share of 6 causes → cost per DALY. Spending shares (gov, private, OOP, DAH) |
| **C baseline** | **891-1723** | 12,109 / 605 rows | The chain below, scenario 1 |
| **D policy** | **1724-2556** | 12,108 / 606 rows | An exact copy of C, offset by 833 rows (checked cell by cell; only cosmetic differences) |
| E | 2557-2563 | 79 | For Transport: VSL, urban population 15+, daily earnings |
| F results and charts | 2564-3578 | 13,536 / 825 rows | Cross-scenario tables (baseline vs `ScenarioNum`, looked up by code over C:D): average EF charts, sector shares, averted deaths by risk, sector, age and area, lag distribution (display), COPD multi-risk-corrected averted deaths, **valuation (3203-3217)**, WDL and wages, GDP loss (forgone output), health-spending savings, per-µg/m3 metrics (3301-3318), implied concentration matrices for all 7 methods (3321-3378) |
| F unit externalities | 3579-4583 | 12,034 / 803 rows | Intake fractions inside and outside the country (IF PP). Per fuel and sector: EF (t/ktoe, Mitigation 1052-1663) × concentration coefficient → µg/m3 per ktoe; × deaths per µg/m3 (baseline) → deaths, YLL, YLD and WDL per ktoe; × VSL × time_factor × (1 + morbidity/mortality ratio) → $/ktoe, then $/GJ or $/litre. Blocks: power coal, gas, oil; road gasoline, diesel, LPG, gas; per litre; manufacturing and all industries × coal, oop, gas, LPG, kerosene, biomass; kerosene and LPG all sectors; residential coal, gas, kerosene, biomass, LPG. Summaries 4501-4583 (inside, outside, cross-border) |
| G notes | 4584-4616 | 0 | Equations |
| H export | 4617-4780 | 3,925 | Per-ktoe metrics copied for export; VSL; lag factor |

**The chain of block C, per year and scenario** (rows of C; D = C + 833):

| Step | Rows | Formula |
|---|---|---|
| Modelled PM2.5 by sector | 895-981 | Σ over so2, nox, pm2, bc, pom, opm, voc of emissions (t) × coefficient. With Manual-FASST, a sector factor = Manual inputs F247:F253 share × observed / modelled |
| Modelled O3 by sector | 983-1050 | Σ over nox, so2, voc, ch4 of emissions × O3 coefficient |
| Household (HAP) change | 1053-1082 | Δ = (res coal + bio)/(baseline) - 1. Share exposed p_H × (1 + Δ × ApLeakHh), capped. HAP level × (1 + Δ) |
| Total concentrations | 1084-1118 | Co = observed(2022) - modelled(2022), constant. Ambient = modelled + Co (urban, rural, all). O3 likewise. OAP+HAP = ambient + HAP |
| RR | 1120-1287 | Linear interpolation in the RR grid at ambient (OAP) and at ambient+HAP (hop), urban and rural × 6 diseases + neonatal (lbw/ptb). O3: exp(β·max(C-TMREL,0)) for COPD 25-64 and 65+. Depression: max(1, exp(β(C-25))) |
| Exposed population | 1289-1311 | pop(age) × p_H (or 1-p_H) × urban/rural share, for all, 25-64, 65+, neonatal |
| Burden, OAP not exposed to HAP | 1313-1378 | pop × (RR-1) × λ × 10^-5 × GBD factor (deaths, YLL, YLD; urban and rural × 7 diseases) |
| Burden, OAP exposed to HAP | 1380-1450 | Same with RR_hop × share OAP (ambient / (ambient + HAP)) |
| Total OAP | 1452-1484 | Deaths, YLL, YLD, DALYs; split by age with the base-year age shares of rows 634-666 |
| Burden, HAP | 1486-1594 | RR_hop × share HAP. Summary by age |
| COPD multi-risk | 1596-1606 | PAF_PM, PAF_O3, joint PAF → adjustment = COPD share × (1 - correction) |
| Depression YLD | 1608-1622 | |
| O3 COPD | 1624-1656 | Deaths, YLL, YLD, DALYs |
| Health spending | 1658-1661 | (OAP + HAP DALYs) × cost per DALY |
| Costs | 1663-1713 | WDL = (1 - e^(-β(C - TMREL))) × days lost × urban/rural share. Value = WDL × daily earnings. YLD → disease days via average disability weight; value = days × earnings × wage factor. Deaths × VSL × time_factor as a share of GDP. Morbidity/mortality ratio (1713) |
| Temperature | 1715-1722 | (CO2 + GWP_t - (CO2 + GWP_2022)) × TCRE × 10^-6 |

**What it reads from legacy Mitigation:**
- 223-224: scenario names.
- 413-467: WEO block, US and world deflators. 426: PPP GDP per capita.
- 504-517: food flows (display only).
- 1051-1663: pollutant EFs `egy.air.ef.<sec>.<fuel>.<pol>` in t/ktoe by year.
- 15827-16078: hand-off E3 (GDP, power and residential fuel use, emissions 10 × 8 × 2 scenarios, CO2, GWP, revenue).
- Directly from data tabs: UNPop, Countries G and X, WEO_upd, Glossary, Transport (I417 accidents, for a chart).

**What it sends back:**

| To | Cells | Content |
|---|---|---|
| Mitigation F10 welfare | 17732 ← 3217; 17739 = 17732 / GDP | `egy.mit.wel.air.usd`, `.pct`: value of averted mortality and morbidity (USD bn), included in wel.tot (17737) |
| Mitigation F10f externality unit costs | 17753 ← 3924, 17754 ← 4351 (zero if residential coal < 0.1% of 9127), 17755 ← 3731, 17756 ← 3998, 17757 ← **4382 (bug)**, 17758 ← 3732, 17759 ← 3886, 17760 ← 3887, 17761 ← **$K$4314**, 17762 ← 4313, 17763 ← 3733, 17764 ← 3961; derived 17765-17768 | `mit.airpol.cost.<fuel>.<sec>.1` in $/GJ or $/litre. They feed explicit and implicit subsidies (17782-17966), efficient prices and Pigouvian taxes (17977-18138), electricity (18105) |
| LiveOutputs | 811-876 | `air.con.pm2.oap.urb/rur.1/2`, `air.con.pm2.mod.all.1`, `obs.all.1`, `who_guidelines`, `air.cad.{ao3,apm25,hpm25,net}`, `air.ada.{2464,65,u24}`, `air.av.{yll,yld}`, `air.mort`, `air.ext.{pp.coa,pp.gas,pp.oil,ind.coa,ind.gas,ind.oil,tra.gso,tra.die}`, `air.gdp.loss(.ch)`, `air.sav.the.{gov,ppr,opo,das}`, `dth.ktoe.{pow.coa,pow.nga,pow.opp,rod.gso,rod.die,ind.coa,ind.oop,ind.nga,res.nga}.1`, `air.conc.pm2.{cpp..foo,tot}.1/.2` |
| LiveOutputs, through Mitigation | 838-847, 900, 906, 275-424 | `mit.airpol.cost.*.1`, `mit.wel.air.usd/pct`; `mit.airpol.cost.*.2` and `mit.app.*` (Pigouvian air-pollution part) |
| Dashboard | 438-622 | Air-pollution panel: 32 chart titles read AP F rows. **44 of 448 charts** read the AP sheet |

---

## 2. Data tabs (group `DATA_AIR_POLL->`)

All tabs are **all-country** in the public NoPropData file, and Egypt is present in each.

| Tab | Size (rows × cols) | Layout | Key | What the module uses |
|---|---|---|---|---|
| WB | 649 × 25 | Header row 4 (years 2021-2041 in E:Y); 3 stacked series | `urb.pop-iso` (5-204, 200 ctys), `FR.INR.RINR-iso` (205-468), `gni.iso` (469-649, constant 2015 US$) | Urban share by year; GNI per capita (GNI×100/160 VSL options; extended at its CAGR); real interest rate (discount option, broken: bug B8) |
| GBD | 21,227 × 6 | Header row 4 (Code, Country, Series, Atrib1, Atrib2, Value); 8 stacked segments read with fixed row ranges | Lowercase `iso.air.…` / `ISO.pop.dtr.<age>` / `ISO.pm2.hap.prop.<area>` | Ambient PM2.5 by area (5-562), age structure (563-4687), incidence of dth, YLL and YLD by disease × age (4688-19195), DALY shares (19196-20413), O3 (20414-20609), HAP share exposed (20610-21031), HAP level (21032-21227). 8 duplicate keys (STP, LCA); about 105 cells for Egypt |
| IHME | 987 × 24 | Header row 3; 2 sub-tables | `iso.air.the` (4-207, years 2021-2040, thousand 2022 USD), `ISO.air.sh.<gov/priv/poc/dah>` (208-987, value in E) | Total health spending, financing shares |
| ILO | 603 × 11 | Header row 3 (2018-2023) | `Earnings-<unit>-iso` (4-424), `gou-iso` (425-603) | Monthly earnings (USD; 2021 PPP, local currency for display); output growth per worker |
| ExposureCoefs | 841 × 5 | 3 stacked tables with own headings (rows 3, 205, 403) | `iso.air.lev.hap`, `iso.air.sha.hap` (x², x, c), `iso.air.fact.dth/dly` (O3, OAP, HAP) | HAP level and share paths; GBD adjustment factors |
| IF PP | 1,781 × 7 | Header row 3 | `iso.air.cm.<pol>.<cpp/gpp/opp>.<ins/out>` | Intake fractions of power plants inside and outside the country (option "Intake fractions" and the cross-border display). 18 duplicate keys |
| ConcMat | 31,201 × 6 | **Header row 2**, data from row 3; no single key | Type (pm/ozone), Method (10 methods), Country, APSector (blank for TM5-FASST), Pollutant, coef | Source-receptor coefficients (µg/m3 or ppb per t). 206 countries; Egypt 203 rows. 79 duplicate keys (MDA and others) |
| Air_Data | 3,154 × 6 | Header row 3 | `Work_absence-iso`, `Prob_death-<age>-ISO` (223-2887), `Lab_sh-ISO`, `den/ncv.<fuel>.<iso/all>` (3004-3154) | Days lost per person, probability of death by age (PV of output), labour share, fuel density and NCV (per litre). `den.lpg.all` appears twice (0.56, 0.525): the first is used |
| Air_meta | 82 × 5 | Header row 2 | Codes, sources, disease codes | Metadata only |

The **typed tables in the AP sheet itself** must also go to the prototype (Constants or Inputs_air), with their legacy source:
- RR grid (rows 525-537, 9 × 21);
- VSL group table (45-51);
- parameters (57-103: β, TMREL, disability weights, D = 0.4, TCRE, OECD VSL);
- cessation-lag shares (745);
- WHO guideline 5 µg/m3 (2752).

---

## 3. Settings that drive it

| ScenarioDefinition row | Name | Options | Egypt (F) | Used? |
|---|---|---|---|---|
| 322 | `SourceAppSel` (PM2.5 emissions → concentrations) | TM5-FASST, Manual-FASST, Local study-FASST, Elastic net, Intake fractions, Machine learning, Machine learning no pixel, Machine learning DACCIWA, Avg. iF and LS FASST* | Local study-FASST (default G: Avg. iF and LS FASST*) | Yes. The coefficients read **Dashboard F429 (`D_SourceAppSel`)**, not ScenarioDefinition (bug B5) |
| 323 | `SourceAppO3` | TM5-FASST, Machine learning | TM5-FASST | Yes (the same: `D_SourceAppO3`) |
| 324 | `EFSel` | Average… | Average | **Displayed only** (inert) |
| 325 | `BiomassLeakage` | Yes/No | No | **Displayed only**. Leakage 0.5 (`ApLeakHh`) is always applied |
| 326 | `BiomassNormal` | Yes/No | No | Displayed only in AP (it is used in Mitigation) |
| 327 | `VSLMethod` | Transfer from Group, Transfer from OECD, GNI*100, GNI*160, Manual (rows 734-738) | Transfer from Group (ScenarioDefinition default column G: **Transfer from OECD**) | Yes. "Transfer from OECD" has no row in 734-738 → #N/A in all valuation (OECD median VSL G76 unused), so ScenarioDefinition Default mode breaks the module |
| 328 | `VSLManual` | number | 500,000 | When Manual |
| 329-330 | `VslElSource`, `VslEl` | | #REF! | Dead |
| 331-332 | `DiscSel`, `DiscRate` | Real interest rate, 3% (Robinson 2019), Manual | 3% | Yes (`discount_rate` K757) |
| 334-338 | `WorkDays`, `ApLabSh`, `ApMaxSs`, `ApLeakHh`, `ApCessLag` | | 20, 0.65, 0.99, 0.5, Yes | Yes. Legacy MTInputs E reads the AP sheet cells G80-G88, which are typed |
| AP G92 | `_gbd_fact` (adjust to GBD results) | Yes/No | No | Yes (factors 541-542) |
| AP G36 | Use PPP or USD to transfer VSL | typed "USD" | USD | Yes (C741) |
| Manual inputs 243-254 | Source apportionment shares (Manual-FASST) | cpp .10, gpp .03, opp .05, rod .13, gro .14, oth .15, foo .05, residual .35 | | Only with Manual-FASST. Already present in prototype sheet Manual inputs |
| ScenarioDefinition 218 | `ExternalityAddVAT` | | | F10h VAT on externalities (later step) |

Global, not per scenario (one ScenarioDefinition F value). The prototype ScenarioDefinition already holds rows 321-338 (legacy structure), currently grey.

---

## 4. Cached Egypt values for testing (B = baseline, P = policy, $50 carbon tax by 2030)

| Legacy row | Item | 2022 | 2025 | 2030 | 2035 | 2040 |
|---|---|---|---|---|---|---|
| 741 | VSL selected (const 2026 USD) | 387,400 | 256,800 | 361,700 | 408,200 | 467,900 |
| 749 | Cessation-lag factor | 0.9061 | | | | |
| 1713 | Morbidity/mortality ratio | 0.04107 | 0.06484 | 0.05437 | 0.05634 | 0.05687 |
| 981 | Modelled ambient PM2.5 B (µg/m3) | 16.50 | 16.56 | 16.80 | 17.15 | 17.62 |
| 1110 / 1111 / 1118 | Ambient PM2.5 B urban / rural / all | 55.68 / 40.59 / 54.86 | 55.74 / 40.65 / 54.92 | 55.98 / 40.89 / 55.16 | 56.32 / 41.24 / 55.51 | 56.79 / 41.70 / 55.97 |
| 1112 / 1113 | O3 B (ppb) / HAP urban | 52.30 / 92.4 | 51.84 | 52.36 | 52.85 | 53.32 / 92.4 |
| 1814 / 1951 | Modelled / ambient all P | 16.50 / 54.86 | 16.56 / 54.92 | 14.45 / 52.81 | 12.67 / 51.03 | 11.59 / 49.95 |
| 1455 / 2288 | OAP deaths B / P | 62,960 / 62,960 | 66,830 / 66,820 | 72,260 / 69,620 | 78,100 / 72,750 | 84,400 / 76,770 |
| 1512 / 2345 | HAP deaths B / P | 79.8 / 79.8 | 84.4 / 84.4 | 90.5 / 91.7 | 96.5 / 99.0 | 102.4 / 106.1 |
| 1633 / 2466 | O3 deaths B / P | 1,229 / 1,229 | 1,270 / 1,270 | 1,403 / 1,334 | 1,541 / 1,396 | 1,684 / 1,474 |
| 1457 / 1459 / 1461 | OAP YLL / YLD / DALY B | 1.822e6 / 117.6k / 1.939e6 | | 2.090e6 / 134.5k / 2.225e6 | | 2.440e6 / 155.6k / 2.595e6 |
| 1622 | Depression YLD B | 155,300 | 166,500 | 180,200 | 190,400 | 202,600 |
| 1606 | COPD multi-risk adjustment B | 0.003195 | 0.003145 | 0.003226 | 0.003312 | 0.003404 |
| 1661 | AP health spending B (USD m) | 1,498 | 1,604 | 1,970 | 2,332 | 2,745 |
| 1669 / 1672 | WDL B (days) / value (USD m) | 4.899e7 / 414 | 5.203e7 / 461 | 5.635e7 / 591 | 6.106e7 / 752 | 6.619e7 / 949 |
| 3056 | Total baseline AP mortality | 64,271 | 68,180 | 73,750 | 79,740 | 86,190 |
| 3147 / 3148 | Averted deaths O3 / PM2.5 (multi-risk adjusted) | 0 / 0 | 0.58 / 3.66 | 68.4 / 2,614 | 143 / 5,306 | 208 / 7,564 |
| 3159 | Cumulative averted deaths, net | 0 | 7.4 | 6,996 | 29,070 | 63,720 |
| 3207 / 3201 | Value of averted mortality (USD bn) / of averted YLD (USD m) | 0 / 0 | 0.00099 / 0.032 | 0.879 / 26.5 | 2.016 / 63.5 | 3.295 / 105.9 |
| **3217 = Mit 17732** | **wel.air, USD bn** | 0 | 0.00102 | **0.9056** | 2.079 | 3.401 (Mit 17732: 3.123, bug B4) |
| 3210 | Value of baseline AP mortality (USD bn) | 22.56 | 15.86 | 24.17 | 29.49 | 36.54 |
| 3277 / 3278 | Baseline GDP loss / change (USD bn) | 1.014 / 0 | 1.132 | 1.448 / -0.0087 | 1.836 | 2.304 / -0.0346 |
| 3286 | Health-spending savings (USD m) | 0 | 0.085 | 68.1 | 151.4 | 235.2 |
| 3308 | Deaths per µg/m3 (B) | 1,148 | 1,217 | 1,310 | 1,407 | 1,508 |
| 3732 / 3733 | Ext. gas / oil power plants $/GJ | 0.376 / 12.69 | 0.269 / 8.95 | 0.399 / 13.01 | 0.480 / 15.27 | 0.579 / 18.13 |
| 3886 / 3887 | Ext. gasoline / diesel $/l | 0.0305 / 0.109 | 0.0212 / 0.0783 | 0.0302 / 0.1175 | 0.0346 / 0.1425 | 0.0404 / 0.176 |
| 3924 / 3961 / 3998 | Ext. industry coal / oop / gas $/GJ | 0.907 / 8.94 / 0.112 | 0.643 / 6.32 / 0.081 | 0.941 / 9.22 / 0.121 | 1.114 / 10.86 / 0.147 | 1.334 / 12.94 / 0.180 |
| 4313 / 4314 | Ext. kerosene / LPG $/l | 0.719 / 1.244 | 0.517 / 0.894 | 0.776 / 1.342 | 0.943 / 1.630 | 1.159 / 2.004 |
| Mit 17739 / 17737 | wel.air % GDP / total national welfare (USD bn) | 0 / 0 | 1.7e-6 / 0.124 | 0.00117 / 9.67 | 0.00214 / 19.39 | 0.00259 / 29.37 |
| Mit 18137 / 18138 | AP Pigouvian CO2-equivalent, all fuels, B / P ($/t) | 67.2 / 67.2 | 61.3 / 61.6 | 67.7 / 64.0 | 72.4 / 66.5 | 75.0 / 68.9 |

Input values for Egypt:
- **Emissions:** legacy AP inputs (t, 2022): NOx 785.0k, SO2 285.8k, BC 30.2k, POM 46.4k, OPM 12.6k, VOC 368k, CH4 1.936M, CO 2.44M, PM2.5 89.2k, OC 35.7k. prototype section 15 is higher (NOx 886 kt, PM2.5 95.6 kt) because it fixes L22, L23, L58 and L59.
- **Exposure:** observed OAP urban 55.68, rural 40.59, all 54.86; O3 52.3; HAP 92.4; p_H 0.001194.
- **Population and economy:** population 111.7 m (urban 42.97%); PPP GDP per capita 19,060; LMI VSL group 1.1 m / 13,580.
- **Labour and health spending:** daily earnings $8.458; labour share 0.41; days lost 3.703; health spending 25.4 bn USD (2026 prices).

---

## 5. Legacy bugs found (proposed L items) and issues to replicate (I items)

### Bugs (do not replicate)

| # | Cells | What | Proposed fix | Egypt effect |
|---|---|---|---|---|
| **B1** (needs your confirmation) | λ rows 672-683 (column P/Q/R picks age "all" = I547:I552) used with population 25+ (K1304+K1305 …) in 1318-1327, 1340-1349, 1362-1371, 1390-1399, 1412-1421, 1434-1443, 1496-1505, 1518-1527, 1540-1549, + policy block | COPD, lung cancer, diabetes, stroke and IHD burden: the all-ages incidence (diluted by under-25 zeros) is applied to the 25+ population. All-ages/25+ rate ratio is 0.474 for every disease (column R "Above 25 (for sense check)" exists, unused) | Use the 25+ rate (R547:R570) for these diseases | About ×2.1 on adult-disease burden. OAP deaths 2022 ~63k → ~122k (estimate); wel.air about ×2. Note: ExposureCoefs `fact.dth` OAP for Egypt = 1.97, so the optional "Adjust to GBD" factor seems to compensate this gap. With the fix, that option would double-correct |
| B2 | Mit 17757 ← AP K4382 | Residential gas air-pollution cost ($/GJ) reads "deaths 15-64 per ktoe". The residential gas block has no monetary rows | Add the $/ktoe and $/GJ rows (deaths/ktoe × VSL × time_factor × (1 + ratio) / GJ) | 2022: 0.00048 → ~0.0121 $/GJ |
| B3 | Mit 17761 = `'Air pollution'!$K$4314` | LPG cost fixed at 2022 for all years (kerosene 17762 uses `K$4313`) | Relative column | 2030: 1.244 → 1.342 $/l |
| B4 | Mit 17732 (L:AC), 17753-17764 (L:AA), then `=previous`; AP stops at 2040 (AC) | Links are truncated: 2040-41 (wel.air) and 2038-41 (unit costs) are carried flat | Compute 2022-2041 on the AP sheet; link every year | 2040 wel.air 3.123 → 3.401 |
| B5 | 442-522 F/G, 974-980, 1807-1813 (`D_SourceAppSel`, `D_SourceAppO3`) | Concentration coefficients follow the **Dashboard** cell, while labels and `source_app_aux` follow ScenarioDefinition F (used for calculation) | Read ScenarioDefinition only | 0 (same option) |
| B6 | 442-522 and 3323-3378 array MATCHes | ConcMat ranges of different length (B$3:B$39555 vs $43279). The O3 non-FASST branch uses `D$2:D$4122` (offset 1 row, 4,121 rows) | Keyed exact lookup on the whole table | O3 "Machine learning" gives 0 for all sectors today. Latent for PM2.5 beyond row 39,555 |
| B7 | 1072-1073, 1076-1077 | When the new solid-fuel share is >1, the "final share" becomes (max/share - 1)/Δ, a factor, not a share. Urban uses K1059 and rural K1060 (adjusted max) | Cap at ApMaxSs (and the adjusted max for both areas) | 0 (edge case) |
| B8 | K754 | Real-interest-rate discount option: INDEX over one column with a year column index → #REF! | INDEX over E:X | Only with that option |
| B9 | K3877 | Road gas deaths/litre uses the LPG deaths/ktoe (K3820), not K3851 | K3851 | Not output |
| B10 | 3249, 3297 | Dead `#REF!` (avoided GDP loss % GDP; health spending per µg share) | Rebuild with GDP / leave out | Display |
| B11 | 4577, 4581 | Cross-border deaths #DIV/0 when coal-plant iF inside = 0 | IFERROR / skip | Display |
| B12 | Mit 17754 `IF(L16297/9127>0.1%, …)` | Typed Egypt-specific total-energy constant (9127) in the residential-coal switch | The year's total final energy use (Mitigation section 11). Denominator to confirm | 0 for Egypt |
| B13 | Mit 17759, 17763, 17764, 17767, 17768 | Wrong or duplicate output codes (`airpol.cost.gso` built from C17760; four rows `airpol.cost.oop.1`) | Unique codes | 0 |
| B14 | 327 option "Transfer from OECD" | No matching row in 734-738 → #N/A in all valuation | Build the OECD transfer from G76 (`_vsl_oecd`) or remove the option. **Decision** | Only with that option |

Cosmetic, not built: row 432 J:AC (later-year population drift, unused); K2171-2172 (policy LRI YLL reads baseline RR in 2022 only); V2298 stray cell; D/E label offsets 1067-1069.

### Issues (replicate as legacy, register as I)

| # | What |
|---|---|
| I-a | Source-receptor model is linear (emissions × coefficient). The non-modelled part Co = observed(2022) - modelled(2022) is held constant. TM5-FASST coefficients are per pollutant, not per sector |
| I-b | Unit damages use **average** deaths per µg/m3 (total OAP deaths / total PM2.5, `(K2762-0)`: the TMREL is not subtracted although the IF tests it), from the **baseline** for all scenarios |
| I-c | VSL transfer: income elasticity 1 on PPP GDP per capita; group base values typed (2022 PPP); PPP→USD by the current ratio, so Egypt's VSL falls 387k → 257k (2022-25) with the devaluation |
| I-d | Manual VSL grows with current (nominal) PPP GDP per capita, with no deflator and no PPP→USD step. **Possible bug: decision** |
| I-e | Population projected with fixed base-year GBD age structure. Incidence rates fixed at base year. λ_TMREL from base-year RR |
| I-f | RR by linear interpolation in the GBD 2021 grid. O3 (Turner 2016) and depression (Braithwaite 2019) log-linear |
| I-g | HAP: level scales with residential coal+biomass; share exposed with leakage 0.5. Inert switches `EFSel`, `BiomassLeakage`, `BiomassNormal`, `VslEl*`, elastic-net adjustment (G30/H30) |
| I-h | Valuation = averted deaths (multi-risk-adjusted, contemporaneous) × VSL × cessation-lag PV factor + value of averted YLD. WDL value, GDP loss and health-spending savings are computed but not in wel.air. The lag-distribution table is display only |
| I-i | Morbidity: YLD → days via average disability weight; × daily earnings × wage factor (DW/0.4) |
| I-j | Shares of GDP use baseline real GDP for all scenarios |
| I-k | Industry unit costs: Mitigation 17753/17764 use the "manufacturing" EF block (3889-4035); LiveOutputs `air.ext.ind.*` use "all industries" (4037-4255, simple average of non-zero subsector factors). Same for Egypt |
| I-l | LPG and kerosene costs per litre from all-sector average EFs with "ground-level other" coefficients |
| I-m | Temperature change against 2022 emissions, not cumulative (display) |
| I-n | Data quirks: duplicate keys (GBD 8, IF PP 18, ConcMat 79, Air_Data 3), the first match is used. `den.lpg.all` 0.56 vs 0.525 |
| I-o | Legacy horizon 2040 (Mitigation 2041 flat). Superseded by B4 if fixed |

---

## 6. Mapping onto the prototype

**Inputs already in the prototype:**

| Legacy input | prototype source |
|---|---|
| Emissions 10 pollutants × 7 sectors + all, t (E3 15859-16065) | Section 15 `aps.<pol>.<sec>` (kt; ×tPerKt). Same layout and pollutant order (v0.3.12) |
| Residential coal + biomass use (15837-15857) | Section 6 residential fuel-use rows (ener coa, bio) |
| Baseline real GDP 2026 USD (15827) | `gdp.usd` of scenario 1 through a `.ref` row |
| CO2 energy and GWP100 (16069-16073) | Section 13 CO2 total, `apf.all` (only for the temperature display) |
| Deflators (Mit 452, 467), PPP GDP per capita (426), NGDPD | `defl` row; Inputs_macro / WEO tab (codes `EGY.PPPPC.A`, `EGY.NGDPD.A` present) |
| EF t/ktoe by sector/fuel/pollutant/year (Mit 1052-1663) | Inputs columns `ap0_<pol>` / `ap1_<pol>` (+ Inputs_power) × `ap.w`. This needs explicit rows for the ~30 fuel-sector pairs of the unit-cost blocks |
| UNPop, Countries (income group G, VSL group X) | prototype tabs UNPop, Countries |
| Manual inputs 243-254 | prototype Manual inputs (legacy addresses; F254 formula already there) |

**New:**
1. **Data tabs** under `DATA_AIR_POLL->>`, in legacy order, after DATA_OUTPUT: WB, GBD, IHME, ILO, ExposureCoefs, IF PP, ConcMat, Air_Data, Air_meta. Legacy tables unchanged (NORMS 1.5).
   - Single tables at A4. ConcMat's header moves from row 2 to row 3, which is harmless because lookups are keyed.
   - Stacked tabs (GBD, WB, IHME, ILO, ExposureCoefs, Air_Data) at legacy addresses from row 3 (rule 2b).
   - Keys to the right: ConcMat `type|method|cty|sector|pol`; GBD lookups by code over the whole column, with no positional segments.
   - Named ranges sized with margin (ConcMat 60k, GBD 40k).
2. **Inputs_air data step** (NORMS 1.5-2c, formulas keyed on CtryCode):
   - GBD exposures, age structure, incidence (3 metrics × 7 diseases × 6 ages), DALY shares;
   - ExposureCoefs, ConcMat coefficients of the selected method (7 sectors × 8 pollutants × PM/O3), IF PP;
   - WB urban share and GNI by year; IHME spending and shares; ILO earnings and output growth; Air_Data;
   - typed legacy constants (RR grid, VSL groups, β/TMREL, disability weights, lag shares, WHO 5): Constants/Inputs_air with source "legacy AP row …".
3. **Sheet `Air pollution`** (legacy name, NORMS 1.4), a time-series module sheet with **exactly Mitigation's group geometry** (NORMS 3c-4): code column + 2022-2041 + spacer, groups 1-7, group 3 = LAMBDA test group, rows 1-12 header and scenario rows, `.ref` via `ref_formula`. One group = legacy block C for that scenario; reads Mitigation group *n* by code (NORMS 3c-6). Scenario-invariant series (population by age, urban share, VSL path, lag, PV of output, earnings, health spending) as rows in every group (identical), or in Inputs_air.

   | Sections | Rows (est.) |
   |---|---|
   | Prep series | ~60 |
   | Concentrations (PM by sector, O3, HAP, totals) | ~70 |
   | RR (OAP, hop, O3, depression) | ~60 |
   | Exposed population | ~20 |
   | Burden OAP/HAP/O3/depression with summaries | ~170 |
   | Multi-risk, health spending, WDL, YLD value, deaths value | ~40 |
   | Averted vs scenario 1 (`.ref`) and valuation `ap.val` → wel.air | ~30 |
   | Unit externalities per fuel-sector ($/ktoe, $/GJ, $/l; from scenario 1 per I-b) | ~120 |
   | Total | **~570 rows × 7 groups** (legacy C+F-unit ≈ 1,400 formula rows) |
4. **Section 18 feedback:**
   - add `wel.air` (USD bn) and `wel.air.pct` to the welfare summary; `wel.usd` = climate + air - efficiency - methane fee (legacy 17737 also sums transport co-benefits, still 0);
   - new sub-block **18b** "Air-pollution costs per unit of fuel" `airpol.cost.<fuel>.<sec>` (16 rows, legacy 17753-17768) reading the AP sheet.
   - Later and separate: F10f-h subsidies, efficient prices, Pigouvian taxes (need transport externalities).
5. **LiveOutputs:** legacy codes of rows 811-876, 838-860, 900, 906 (66 `air.*` / `dth.ktoe.*` codes + 10 `mit.airpol.cost.*.1` + 2 `wel.air`). Cumulative and age tables (cad.*, ada.*) are computed in LiveOutputs from the levels (NORMS 3c-2).
6. **ScenarioDefinition** rows 322-338 coloured green where used (322, 323, 327, 328, 331, 332, 334-338). Inert rows stay grey with a note (I-g). Manual inputs 247-254 noted as read.
7. **Python reference `airpollution_ref_v<n>.py`.** One group plus its scenario-1 reference, with the same chain as the sheet. A `legacy_bugs=True/False` switch: True must reproduce section 4 to print precision from the legacy cached inputs (AP rows 149-361 cached emissions, Inputs_air values); False lists the deltas of B1-B4, B7. Extract `extract_airpol_v<n>.py` → `data/mvp_legacy_extracts/legacy_<tab>.csv`, `data/mvp_legacy_extracts/legacy_ap_reference.csv`.
8. **Tests:**
   - quick check: AP group 2 vs the reference fed with the sheet's own inputs (to 1e-9); geometry equality with Mitigation; no error values; unique codes; legacy_compare rows for the section 4 items;
   - paste test: groups 4-7 on both sheets;
   - LAMBDA test group: AP LAMBDAs;
   - all-country: clone EGY rows of the 9 tabs as XEG, rewriting country codes embedded in keys in all cases (`egy.air.*`, `EGY.pm2.hap.prop.*`, `urb.pop-egy`, `Earnings-…-egy`, `Prob_death-<age>-EGY`, `Lab_sh-EGY`);
   - option sweep: 9 PM methods, 2 O3 methods, 4 VSL methods, 3 discount options, lag on/off, GBD factor yes, Manual-FASST.

---

## 7. Proposed plan

| Step | Content | Size |
|---|---|---|
| 0 | Your decisions (below); register L124+ (B1-B14), I69+ (I-a…I-o); LegacyDiff rows | S |
| 1 | `extract_airpol`: 9 tabs → CSV; AP typed constants; legacy cached reference (inputs and outputs, both blocks, LiveOutputs, Mit 17732-17768) | M |
| 2 | `airpollution_ref` (full chain, unit costs, valuation) reproducing legacy Egypt exactly with `legacy_bugs=True`; delta table with fixes | L |
| 3 | Data tabs and divider in the build (legacy layout, names, key columns), plus all-country clone rules | M |
| 4 | Inputs_air data step and constants (country selection, method selection, typed tables) | M |
| 5 | AP sheet skeleton with Mitigation geometry: header rows, groups, `.ref`; concentrations, HAP, totals, RR | L |
| 6 | Burden chain (exposed population; OAP not exposed / exposed; HAP; O3; depression; multi-risk; age splits) | L |
| 7 | Valuation and productivity rows; averted vs scenario 1; `ap.val` | M |
| 8 | Unit externalities per fuel-sector (EF rows from Inputs ap0/ap1 × ap.w, coefficients, per GJ / litre) | M |
| 9 | Section 18: `wel.air`, `wel.air.pct`, `wel.usd`; sub-block 18b `airpol.cost` | S-M |
| 10 | LAMBDAs for every AP calculated row; LAMBDA test group; spacer test | M-L |
| 11 | LiveOutputs AP section (legacy codes), ScenarioCompare; 2-4 charts (PM2.5 urban/rural, averted deaths, value) | M |
| 12 | Checks: quick-check reference comparison, geometry, paste, all-country, option sweep; full check entry | M |
| 13 | Docs: `AirPollutionModule_Method_v<n>.md`, Equations/Formulas, Replicated/NotReplicated lists, CAVEATS, TODO, version log | M |
| (14) | Optional later: F10f-h subsidies, efficient prices, Pigouvian (with transport externalities) | L |

Natural version split: steps 1-4 (data), 5-8 (sheet), 9-13 (feedback, outputs, checks).

**Decisions needed:**
1. **B1** (adult-disease incidence): fix as a bug (OAP deaths about ×1.9, wel.air about ×2) or keep as an issue. If fixed, what happens to the `_gbd_fact` option (factor 1.97 would double-correct)?
2. Unit damages from scenario 1 for every scenario (legacy, I-b; recommended) or each scenario's own.
3. Horizon: compute 2041 on the AP sheet (recommended; fixes B4).
4. Scope of the results/chart area F: LiveOutputs codes plus a few charts (recommended), or also the intake-fraction cross-border tables, per-µg metrics and the 44 legacy charts.
5. F10f-h (subsidies, efficient prices, Pigouvian taxes) now with transport externalities missing, or later (recommended later).
6. AP settings global (as legacy; recommended) or per scenario in ScenarioDefinition.
7. Inert switches (BiomassLeakage, EFSel, BiomassNormal, VslEl, elastic net): keep inert (issue) or implement BiomassLeakage = No → leakage 0.
8. Manual VSL units (I-d) and the "Transfer from OECD" option (B14): bug fixes or issues.
9. B12 denominator for the residential-coal switch (total final energy of the year?).
10. Sheet name `Air pollution` (legacy; quoted in formulas) vs `AirPollution`.
11. Accept that prototype AP results differ from legacy because section 15 emissions already include L22, L23, L58 and L59 (testing through the Python reference on both inputs).

