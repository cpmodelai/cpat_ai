# Engineer road transport model: data and Python reference (v3.5, phases 1-2)

Source: legacy CPAT `legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (cached values, read with pyxlsb), Mitigation key inputs 15 (rows 2017-2171) and section 5 (rows 4302-5378, policy copy at +6331), as mapped in `Transport_Legacy_Survey_v7_0.md`. Plan and decisions: `Transport_Plan_v7_0.md` section 3 (approved: Elasticity default, all bugs fixed with legacy switches in the reference, legacy parameter values by default, range anxiety from Transport3, two calibration steps kept).

Scripts:
- `extract_transport_v7_0.py` writes the data files below from the xlsb alone. The country of the legacy run is read once from Dashboard D644 (`_Country_code`, EGY). Multi-country sheets keep all countries.
- `transport_model_ref_v7_0.py` is the Python reference: `engine(inp, years, fix)`, `legacy_inputs(run)` (run `base` or `pol`), `legacy_test(run, fix=frozenset())`, `effects_md(run)`. Running it prints the legacy test and the fix tables below.

## 1. Data files (`data/`)

| File | Content | Legacy source |
|---|---|---|
| `transport_data.csv` | 220 countries x 59 numeric variables, 2022-2025 (iso, country, variable, years) | Transport1 |
| `transport_data_sources.csv` | the `... - source` text columns, same layout | Transport1 |
| `vehicle_prices.csv` | ICEV and EV prices (passenger, freight, 2-3 wheeler), 220 countries, 2022-2040 | Transport2 |
| `range_anxiety.csv` | stored range anxiety per country ($/vehicle: passenger, freight, cycle), and the 2025 actual and calculated EV shares the solver fitted; 194 countries | Transport3 rows 5-226 |
| `transport_params.csv` | key, value, unit, description, legacy cell, use. Policies and parameters of the side tables (Mitigation 4304-4332, the Dashboard cell in the description), Dashboard options (TrModel, range-anxiety source, Q551, Q556, freight-share and 2-3 wheeler hump parameters), formula literals (Gompertz -5.897, gas /26, PHEV x9, insurance x0.5, station life /15, BEV distance caps 1.2/1/1, own and cross elasticities, policy factors x1, data years 2024/2022 hardcoded in the Dashboard), the Transport3 average (fallback), and the methodology-note alternatives (`note|...`, use = note, not used by default) | Dashboard 61-98, 540-559; Mitigation side tables |
| `transport_paths.csv` | BEV fuel economy of new vehicles (passenger, freight, 2-3 wheeler), BEV fuel economy light/freight/cycle (used in data years), charging cost per port, 2022-2041 | Manual inputs 375-377; Mitigation 2051, 2095, 2122, 2170 (v5.2: the workbook reads the BEV fuel economy of new vehicles from sheet Manual inputs J375:AC377, the same values; the CSV rows stay the reference input) |
| `legacy_transport_reference.csv` | cached legacy values, runs `base` and `pol`: every numeric row 4334-5378 (`r<row>`, baseline numbering; `legacy_row` gives the actual row), rows 2034-2171 (`r<row>`), side-table scalars (`c<cell>`: calibration tables 5170-5173, E/I/J5325-5331, H/I/J4787 and 4903, G5177/G5231/G5273, emission factors, VAT and customs cells, K4329, J2169, the 2017-2031 share/ktoe/liter block), and the inputs from the rest of Mitigation (`in|...`: retail prices 2589, 2590, 2594, 2596, 2612, 2618, 2635, 2641, 2543, 2566, 2572; power prices 3617, 3646; GDP growth 2446 incl. 2021; row 2455; carbon price 2375; feebate coverage 2404; population 428; GDP per capita 444; price block 789, 793, 797, 802, 805; scenario number; elasticities; conversions; emission factors; energy balance road column; VAT N726; power WACC average; range anxiety) | Mitigation |

Country-specific Dashboard cells (VAT on vehicles = Mitigation N726; customs = Transport1 duties of 2024; import shares = Transport1 2022; 2-3 wheeler imports = passenger) are not stored as parameters: the engine derives them from the data and the inputs (`customs_year`, `import_year`).

## 2. Equations (legacy behaviour; rows are the baseline block)

Years: data columns 2022-2025 (legacy L-O) take Transport1 values where legacy has `IF(ISNUMBER(data), data, model)`; projections from 2026.

- **Key inputs 15 (2017-2171).** Base-year road fuel by vehicle type = Transport1 shares x energy balance (gasoline + biogasoline, diesel + biodiesel, LPG, gas). Passenger/light blends by the ownership share s = own_pass/(own_pass + own_light) (2038): fuel economies 2041-2047 (LPG and CNG light scaled by FE_fuel/FE_gasoline), BEV 2052, distance 2060, EV shares 2069, 2083, 2088. Vehicle shares 2078-2081 use the 2022 VKT split in every data year (`$L2072`). Freight VKT per vehicle 2117 = diesel freight VKT / vehicles (2022), then scaled by the passenger distance ratio (2023-2025). BEV distance uplift 2056 = min(1.2, (p_BEV/p_ICE per km)^el_dem). Freight share of ownership 2168 and 2-3 wheeler hump 2169 = 2·J·H·y/(y²+H²) after the data years.
- **Stock (4740-4779, 4876-4895, 4956-4975).** Opening = data x new/used split, else last closing. Retirement = min(average opening of the last min(life, t) years / life, opening); lives: passenger new 7, used 13 (20-7), freight 10, 2-3 wheeler 7. Closing = after retirement + purchases (+ data-year adjustment).
- **Charging and range anxiety (4334-4356).** BEV stock (mln) 4340; stations 4347 = previous x (BEV stock ratio)^0.3 x (cost-after-subsidy ratio)^-0.67; mark-up 4350 = max(0.02, 0.3·(0.5 - EV fleet share)/0.5)·0.2; EV electricity price = last year's power price + mark-up (4351 residential, 4352 industrial); range anxiety 2022-2024 = Transport3 value, then RA_t = max(RA_t-1·(1-decline)·(stations ratio)^-0.5, 0).
- **New fuel economy (4358-4448).** Data years: stock FE x 1.05. Projections: FE_t = FE_t-1 · ((p+feebate)_t/(p+feebate)_t-1)^|el_eff| · (1+aei) (passenger uses `_el_eff_gso_rod` for all fuels, freight `_el_eff_die_rod`). Fuel weights = last year's ownership shares (4360, 4413). Used FE = trailing 7-year average of new FE (4401); used intensity = intensity 6 years earlier (4402). Feebate per liter = (feebate rate + carbon price x coverage) x EF, policy runs only.
- **Distance for the TCO (4450-4505).** Distance tax ramp (4451, 4479, 4497). VKT_t = VKT_t-1 · (cost ratio if Q551 = Yes)^el_dem · (1+lagged GDP growth)^inc_el; freight clamped to [50,000, 120,000] km; used vehicles scaled by (FE_new/FE_used)^el_dem.
- **TCO (4507-4736).** Discounted km = -PV(r, years, VKT); r (4531) linear in GDP per capita from 15% (1,000 USD) to 5% (50,000 USD); freight at the average power WACC (K4329). Price after policies = price·(1+customs·import share)·(1+ad valorem)·(1+VAT) + feebate (+ subsidy for BEVs). First-year depreciation 30%, annuity of the rest over life-1 years, discounted salvage; insurance = P·ins/r·(1-(1+r)^-(own+1))·0.5 + maintenance·km; fuel = price/FE·km + distance tax·km; BEVs add range anxiety (used: scaled by the used/new price ratio). TCO per km = TCO / discounted km. Per-fuel ICE TCO 4551-4555 (PHEV with BEV depreciation and range anxiety), 4658-4660.
- **Demand and choice (4781-5007).** Demand_t = 0.09·Sat·exp(-5.897·exp(-0.23·GDPpc/1000))·J + 0.91·demand_t-1, clamped to [-0%, +7.5%] (2-3 wheelers: hump, [-10%, +7.5%]); J = max(1, actual/expected) at 2024. Additions = demand - stock after retirement, split new/used by the used share. EV share = exp(-k·TCO_EV/avg)/(Σ), k = 3/2/4, average weighted by last year's ICE share; data years use the actual share. ICE fuel split: s_i,t = s_i,t-1·(TCO_i ratio)^-1.265·(weighted other ratios)^0.5725, renormalised to 1 - EV share; ownership shares s_own,t = s_own,t-1·(L-1)/L + sales/L (L = 13.57 passenger, 10 freight).
- **Stock fuel economy, distance and fuel use (5009-5303).** Closing FE = new·share_new + opening·(1-share_new), share_new = 1/(7·s_used + 20·(1-s_used)) passenger, 1/10 freight, 1/7 2-3 wheeler; BEV stock FE likewise with the BEV new/used turnover. VKT per vehicle_t = VKT_t-1·(cost per km ratio)^el_dem·(GDP per capita ratio)^inc_el; base year = data x step-1 factor. Fuel = vehicles·VKT/FE (PHEV gasoline and electricity split by 2049).
- **Calibration step 1 (5170-5173).** Q_f = energy balance_f / bottom-up_f (bottom-up x (1+bus share)); distance factors U/V/W = fuel-share-weighted Q (passenger 2.668, freight 1.703, 2-3 wheeler 3.301 for Egypt).
- **Buses (5305-5318).** Base-year bus fuel x (Σ 5310:5313)/(Σ 5310:5314 base) (see B6).
- **Calibration step 2 and results (5320-5378).** ktoe_f = bln liter / liters per ktoe x E_f, E_f = energy balance / calculated in 2022 (gasoline 1.234, diesel 0.858, gas 1.142); electricity E = 1 unless Q556 = Yes. Distance outputs x E (gasoline factor for passenger and 2-3 wheelers, diesel for freight); average fuel economy by fuel; vehicles.

## 3. Legacy match

`legacy_test(run)` drives the engine from the cached legacy inputs (`legacy_inputs`) with `fix = frozenset()` and compares every cached numeric row 4334-5378, the key-input rows 2034-2171 (934 year rows in all) and 157 side-table scalars, 2022-2041 (relative difference to max(1e-6, |legacy|)).

| Run | Series compared | Max relative difference | Where |
|---|---:|---:|---|
| base (Baseline, C2173 = 1) | 1,091 | 3.8e-14 | r5222 (PHEV electricity), 2037 |
| pol (Carbon tax, C8504 = 2) | 1,091 | 1.6e-14 | r4817 (used BEV choice), 2025 |

No residual: the differences are floating-point rounding. The range-anxiety start values from `range_anxiety.csv` equal the cached N4354:N4356 exactly (asserted).

## 4. Fixes

`FIXES` in the reference (each a switch; `ALL_FIXES` is the corrected model). B4 is a parameter choice treated as a fix (allow a decline of up to 10% a year, the legacy 2-3 wheeler value). Survey bugs not in the list: B5 (large calibration factors: a data issue, reported), B11 (intended lags), B12 (literals: now parameters), B13 (row 2171 unused), B14 (open question 1), B15-B17 (unused inputs, externality sheet, layout).

| Fix | Legacy rows | What is fixed |
|---|---|---|
| B1 | 4451, 4720 | `$C2227>1` (text "res" > 1 is TRUE) puts the passenger distance tax and 2-3 wheeler EV subsidy in the baseline: scenario number > 1 |
| B2 | 4487 AB:AE, 4501 | freight and 2-3 wheeler income growth = row 2455 (coal subsidies) from 2038: lagged GDP growth |
| B3 | H:J4787, H:J4903 | ownership calibration max(1, actual/expected) at 2024: actual/expected both ways at the last data year in the data (2025) |
| B3b | $N2168, J2169 | freight-share cap and 2-3 wheeler peak at 2024: last data year |
| B4 | T4328, U4328 | ownership cannot fall: maximum decrease 10% a year |
| B6 | 5310-5314, 5318 | bus scaling from LPG, gas and PHEV distance and BEV vehicles, and bus electricity from liters + kWh: passenger fuel use by fuel (ktoe) and passenger electricity; base bus energy in ktoe |
| B6b | O5171:O5173 | bus share grossed up as x(1+share): /(1-share) |
| B7 | G4376-G4378, G4419-G4421 | stale EF names (diesel and LPG industry, residential gas): road EFs |
| B8 | M5261, M5295, M5232, M4646 | BEV freight distance with the 2-3 wheeler income elasticity; BEV 2-3 wheeler distance with the cost ratio twice and no income term; LPG freight base row; freight ICE depreciation switching to the passenger rate from 2023 |
| B8w | K4329 | freight discounted at the average power WACC: consumer discount rate (4531) |
| B9 | 4850 L:O | negative PHEV sales share: (EV - BEV passenger share) x passenger share, ICE shares scaled to the rest |
| B10 | 4343 | charging subsidy ramp runs before the start year and is not capped: 0 before, linear to the target level, then constant |
| B19 (new) | 4573 | new BEV maintenance uses the ICEV rate (J4327): EV rate (J4328) |
| B20 (new) | 4598 | used ICEV depreciation annuity over 6 years (J4322-1), used BEV over 12 (J4323-1): 12 for both |
| B21 (new) | 5267 | freight distance output omits LPG and LNG trucks |
| B22 (new) | 5368, 5373 | gas fuel economy weights freight by LPG freight fuel (5244 for 5245); EV fuel economy fallback tests diesel (5326) |

### Effects, Egypt (cells 2030 / 2035 / 2041; % change, EV shares in percentage points)

Baseline:

| Series | Legacy 2030 | All fixes 2030 | Legacy 2035 | All fixes 2035 | Legacy 2041 | All fixes 2041 |
|---|---:|---:|---:|---:|---:|---:|
| Gasoline ktoe | 10,157 | 8,219 | 16,286 | 11,181 | 25,754 | 14,590 |
| Diesel ktoe | 14,282 | 10,977 | 22,912 | 14,553 | 36,357 | 18,352 |
| LPG ktoe | 0 | 0 | 0 | 0 | 0 | 0 |
| Gas ktoe | 738 | 586 | 1,199 | 798 | 1,926 | 1,039 |
| Electricity ktoe | 126 | 22 | 1,471 | 290 | 8,065 | 1,753 |
| EV sales share passenger | 5.0% | 1.0% | 21.2% | 9.3% | 41.0% | 27.7% |
| EV sales share freight | 3.2% | 1.7% | 22.2% | 15.6% | 36.6% | 31.1% |
| EV sales share 2-3 wheeler | 18.8% | 16.0% | 46.2% | 41.5% | 61.6% | 56.7% |
| Vehicles passenger mln | 8.93 | 7.11 | 15.98 | 10.11 | 32.30 | 15.31 |
| Vehicles freight mln | 1.58 | 1.17 | 2.81 | 1.63 | 5.55 | 2.38 |
| Vehicles 2-3 wheeler mln | 0.53 | 0.50 | 0.65 | 0.61 | 0.81 | 0.77 |

| Fix | Gasoline | Diesel | Gas | Electricity | EV share pass (pp) | EV share freight (pp) | EV share 2-3w (pp) | Vehicles pass | Vehicles freight | Vehicles 2-3w |
|---|---|---|---|---|---|---|---|---|---|---|
| B1, B4, B7, B10, B21, B22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B2 | 0 / 0 / 0 | 0 / 0 / -0.03 | 0 | 0 / 0 / +0.06 | 0 | 0 / 0 / +0.23 | 0 / 0 / -0.61 | 0 | 0 / 0 / +0.03 | 0 |
| B3 | -19.4 / -33.9 / -48.1 | -23.2 / -37.9 / -52.1 | -19.7 / -34.2 / -48.3 | -42.8 / -52.4 / -61.8 | -0.8 / -2.6 / -4.6 | -0.5 / -2.6 / -3.4 | -1.0 / -2.0 / -2.6 | -20.1 / -36.0 / -51.9 | -25.9 / -41.9 / -57.0 | 0 |
| B3b | -0.1 / 0 / 0 | 0 / +0.1 / +0.1 | 0 / +0.1 / +0.1 | -1.8 / -0.6 / -0.2 | -0.1 / -0.1 / 0 | -0.1 / -0.1 / 0 | -0.1 / 0 / 0 | 0 | 0 | -6.1 / -6.1 / -6.1 |
| B6 | 0 | -0.2 / -0.3 / -0.4 | -1.7 / -2.8 / -4.4 | -18.1 / -16.8 / -16.6 | 0 | 0 | 0 | 0 | 0 | 0 |
| B6b | 0 | 0 | 0 | -0.3 / -0.3 / -0.3 | 0 | 0 | 0 | 0 | 0 | 0 |
| B8 | 0 / 0 / 0 | 0 / -0.2 / -0.4 | 0 | +2.7 / +4.0 / +4.1 | 0 | +0.2 / +0.7 / +0.7 | 0 | 0 | 0 / +0.1 / +0.1 | 0 |
| B8w | 0 | 0 / +0.2 / +0.3 | 0 | -1.6 / -1.0 / -0.4 | 0 | -0.3 / -0.5 / -0.2 | 0 | 0 | 0 | 0 |
| B9 | 0 / 0 / -0.1 | +0.1 / +0.1 / +0.3 | +0.7 / +1.7 / +3.4 | +0.5 / +0.2 / +0.1 | 0 | 0 | 0 | 0 | 0 | 0 |
| B19 | 0 / -0.1 / -0.7 | 0 / -0.1 / -0.3 | 0 / -0.1 / -0.7 | +0.2 / +1.2 / +2.3 | 0 / +0.5 / +1.3 | 0 / 0 / +0.1 | 0 / 0 / +0.1 | 0 / +0.1 / +0.2 | 0 | 0 |
| B20 | +0.7 / +5.1 / +10.5 | +0.4 / +3.1 / +6.1 | +0.7 / +5.0 / +10.4 | -66.9 / -50.7 / -31.5 | -3.8 / -10.0 / -9.6 | -1.0 / -3.5 / -2.0 | -2.1 / -2.6 / -1.5 | -0.6 / -1.6 / -2.2 | -0.1 / -0.3 / -0.2 | 0 |
| All | -19.1 / -31.4 / -43.4 | -23.1 / -36.5 / -49.5 | -20.6 / -33.5 / -46.1 | -82.9 / -80.3 / -78.3 | -4.0 / -11.9 / -13.4 | -1.5 / -6.6 / -5.5 | -2.9 / -4.7 / -4.9 | -20.4 / -36.7 / -52.6 | -26.0 / -42.1 / -57.1 | -6.1 / -6.1 / -6.1 |

Policy (carbon tax):

| Series | Legacy 2030 | All fixes 2030 | Legacy 2035 | All fixes 2035 | Legacy 2041 | All fixes 2041 |
|---|---:|---:|---:|---:|---:|---:|
| Gasoline ktoe | 9,362 | 7,584 | 13,486 | 9,309 | 18,931 | 10,727 |
| Diesel ktoe | 12,881 | 9,937 | 18,068 | 11,581 | 24,689 | 12,494 |
| LPG ktoe | 0 | 0 | 0 | 0 | 0 | 0 |
| Gas ktoe | 605 | 498 | 822 | 572 | 1,134 | 622 |
| Electricity ktoe | 147 | 26 | 1,608 | 358 | 7,965 | 1,868 |
| EV sales share passenger | 6.0% | 1.4% | 23.3% | 11.6% | 43.2% | 30.7% |
| EV sales share freight | 4.6% | 2.6% | 28.1% | 21.8% | 43.6% | 38.7% |
| EV sales share 2-3 wheeler | 19.6% | 16.6% | 47.4% | 43.0% | 62.8% | 58.1% |
| Vehicles passenger mln | 8.94 | 7.11 | 16.04 | 10.14 | 32.48 | 15.37 |
| Vehicles freight mln | 1.58 | 1.17 | 2.83 | 1.64 | 5.60 | 2.40 |
| Vehicles 2-3 wheeler mln | 0.53 | 0.50 | 0.65 | 0.61 | 0.81 | 0.77 |

The per-fix changes in the policy run are within ±1 point of the baseline ones (full table: `python transport_model_ref_v7_0.py`). Notable: B3 -19/-34/-48% gasoline, B20 -4.4/-9.6/-8.9 pp passenger EV share, all fixes -19/-31/-43% gasoline and -23/-36/-49% diesel.

Reading: B3 (two-sided ownership calibration) removes most of the legacy growth: Egypt's ownership was 55 per 1,000 in 2025 against a Gompertz level of 152, so J = 0.36 instead of 1, and passenger ownership reaches 82 per 1,000 in 2041 instead of 173. B4 has no effect in Egypt because ownership still rises after B3. B20 is the largest choice-side fix: legacy front-loads the used ICEV depreciation, which raises used ICEV TCO and the used EV share. B1, B7, B10, B21 and B22 matter only when the policies or fuels are non-zero (all zero in both Egypt runs; the carbon tax does not enter the feebate because the road feebate coverage, row 2404, is 0).

## 5. Open questions (decided 2026-10-14)

User: "Go with suggestions and always try to match existing except where there are bugs". Decisions: (1) B14 kept as legacy; (2) B20 as implemented (12 years for both); (3) stored range anxiety, mismatch reported, re-solve later; (4) 10% kept; (5) PHEVs carry no range anxiety (new fix B23); (6) data years kept as legacy; (7) factors reported in the workbook; (8) B6 as implemented. All bugs and decisions against legacy: `Transport_vs_Legacy_v7_0.md`.


1. **B14 freight distance.** The TCO uses Transport1 `average vkt freight` (48,630 km, clamped to at least 50,000 km, which binds in every projection year), while fuel use uses 8,091 km (derived from fuel shares) x 1.70. Which freight VKT is right, and should the clamp stay? Not fixed.
2. **B20 direction.** The fix uses the used ownership period (13 years) for the used ICEV depreciation annuity, as legacy does for used BEVs and for the used insurance; confirm.
3. **Range anxiety after the fixes.** Transport3 values were solved in another vintage: in this file the calculated 2025 passenger EV share is 0.35% against 0.15% actual (Transport3 records 0.24%). With all fixes it is 0.09% (B20). The stored values should be re-solved for the corrected model (goal seek, later).
4. **B4 value.** 10% (legacy 2-3 wheeler value) is a placeholder; no effect for Egypt.
5. **PHEV TCO** includes the full BEV range anxiety (about 100,000 $/vehicle), so PHEV sales vanish; keep?
6. **Data years.** VAT on vehicles is the 2024 VAT rate, customs the 2024 duties, import shares 2022, bus electricity the 2024 EV stock share (parameters `customs_year`, `import_year`, `bus_ele_year`). Use the last data year instead?
7. **Calibration factors** (passenger distance x2.67, then gasoline x1.23): Transport1 ownership x distance / fuel economy explains only 30-60% of Egypt's road fuel. Report them in the workbook; review the data.
8. **Bus electricity (B6).** The fix scales bus electricity with passenger electricity relative to base passenger energy; an explicit bus EV share may be preferable.

## 6. Corrections to the survey

- Transport1 holds 220 countries (880 rows of 4 years), not 221; Transport3 has stored values for 194 countries.
- B4: the 2026 jump (P4787 = 59.25 against O = 55.12) is the 7.5% growth cap binding (55.12 x 1.075), not a closing-stock mismatch.
- B2 also hits 2-3 wheelers (4501 = 4487). For freight it has no effect on the TCO distance because the 50,000 km minimum binds; the effect shows only through 2-3 wheelers and BEV freight from 2038.
- B6 also mixes units in bus electricity (5318 adds bln liters of diesel, LPG and gas to bln kWh).
- B3: with the data to 2025, actual/expected is 55.1/152.1 = 0.36 (the survey's 57.8/138.9 is the 2024 column used by legacy).
- Not in the survey: B19 (new BEV maintenance at the ICEV rate), B20 (used ICEV/BEV depreciation periods differ), B21 (freight VKT output omits LPG/LNG), B22 (gas fuel-economy weights use LPG freight; EV fallback tests diesel); the BEV freight feebate (4637) uses ICEV discounted km (same values); vehicle shares 2078-2081 use the 2022 VKT split in every data year; the Transport3 calibration does not hold in this file (open question 3).
