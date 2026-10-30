# LD41: prototype data extracts moved from legacy 456 to legacy 465

User decision LD41 (2026-10-29): the data extracts of the prototype come from `CPAT 1.0pre_465_NoPropData.xlsb`
instead of `CPAT 1.0pre_456_NoPropData.xlsb`. Both files are read-only, in `excel_ai/legacy/workbooks/`. This note
lists what the move changed in `data_old/mvp_legacy_extracts/*.csv`. The prototype has not been rebuilt (`build.py` was not run or changed).

## 1. What was done

- **Extractors moved to 465.** `extract_data.py`, `extract_legacy_tables.py`, `extract_ecp.py`, `extract_ets.py`,
  `extract_gdp.py`, `extract_ghg.py`, `extract_power.py` and `extract_transport.py` now read 465.
  `extract_inputs.py` already read 465. Each docstring has a v0.8.5 (LD41) note.
- **Row numbers.** The Mitigation rows were mapped with `excel_ai/legacy/fixes/data/rowmap_456_465.json`. Rows
  1-5666 are the same in both files, so only rows below 5666 move:

  | Extractor | 456 rows | 465 rows |
  |---|---|---|
  | `extract_power.py` (carbon-tax copy of the engineer model) | 9285+ (offset 6331) | 9270+ (offset 6316) |
  | `extract_transport.py` (`OFF`, policy block) | +6331 | +6316 |
  | `extract_gdp.py` (manual SCC path) | 17683 | 17668 |

  The labels and codes in columns B-E agree under the map; the only text differences are in column G. The
  year columns are the same in both files: K = 2021, L = 2022, AE = 2041, AI = 2045.
- **Other sheets were compared cell by cell.** Countries, ECP, CH4Inputs, UNPop, OilProductShares, Prices_int,
  ETS+LTS, WEO, EF_GHG, SCC, GDPRatios, Transport1, Transport2, Multipliers and Power are identical. Manual inputs,
  Elasticities, GHGs, CoC and Transport3 have a few value changes on the same layout. Balances has 161 value changes on
  the same layout. Every assertion in the extractors (labels, table ids) still passes.
- **energy_use.csv and weo.csv no longer come from the kernel file.** Until v0.8.4 they came from
  `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, a copy of 456 Mitigation rows 583-601 and 2446. They now come from legacy
  465 directly (new function `extract_data.extract_base_year`, cached values):
  - **energy_use.csv:** Mitigation rows **583-601**. Each row is a fuel, with the code in column C: coa 584, nga 585,
    oop 586, gso 587, die 588, ker 589, lpg 590, jfu 591, bio 597. Each column is a subsector, with the code in row
    581: E elec ... G rod, H ral, I avi, J nav, K res, L foo, M srv, N mch, O irn, P nfm, Q mac, R cem, S omn, T cst,
    U ftr, V oen. Units are ktoe, Egypt, base year 2022.
  - **weo.csv:** Mitigation row **2446** (`Post-policy GDP growth`, `egy.mit.gdp.pos.pct.1`), columns K-AI.
  - The 456 values were checked first: all 144 cells of the old `energy_use.csv` equal 456 rows 583-601 exactly.
- **Two exceptions in `extract_legacy_tables.py`:**
  - **Still read from 456:** `HHSurvey` and `HH_Elast`. The 465 NoPropData file holds only their header rows.
  - **Kept to Egypt's rows:** `EF_PM`, `IO_GTAP`, `ASPIRE` and `WHOCooking`. 465 holds them for all countries; 456
    held Egypt only. The constant `EGYPT_ONLY` sets which rows are kept, so the prototype tables keep their size; with
    `EGYPT_ONLY = {}` the extractor writes all countries. `extract_ghg.py` keeps Egypt's EF_PM rows in the same way.
- **Not re-run:** `extract_data.extract_prices` and `update_prices_egypt`. Their source,
  the domestic price source file, is not in the repository, and they read
  no legacy data. `prices_dom*.csv` are unchanged. The Egypt domestic prices were already known to be identical in
  456 and 465.
- **Line endings.** `extract_ecp.py` and `extract_power.py` now write LF line ends, as the committed files have.
  Before, re-running them only flipped CRLF/LF.
- **`extra_eff` in power_params.csv.** 465 removed the input row "Additional Efficiency" (456 M3719 = 0). The
  extractor now writes 0.

## 2. Diff per csv (456 -> 465)

The two files were compared cell by cell. Numbers within a relative difference of 1e-9 count as equal. Changes only
to `source`, `legacy_row` or `legacy_cell` columns are not counted here. Every listed file was rebuilt.

### Identical (48 of 66 files; 47 byte for byte, `weo` in value)

- `extract_legacy_tables.py`: `legacy_HHSurvey`, `legacy_HH_Elast` (from 456), `legacy_ASPIRE`, `legacy_WHOCooking` (Egypt rows),
  `legacy_GDPRatios`, `legacy_SCC`, `legacy_UNPop`, `legacy_CH4Inputs`, `legacy_GHGs`, `legacy_Transport1`,
  `legacy_Transport2`, `legacy_EF_GHG`, `legacy_OilProductShares`, `legacy_WEO_NGDP_D`, `legacy_WEO`,
  `legacy_Countries_cells`, `legacy_ETS+LTS_cells`, `legacy_Multipliers_cells`, `legacy_Prices_int_cells`,
  `legacy_ECP_cells`, `legacy_Transport3_cells`, `legacy_Power_cells`, `legacy_NDCs`, `legacy_GHGHist`.
- `extract_data.py`: `prices_int`, `weo_us`, `price_assumptions`, `countries`, `elasticities`, `ef_co2` (EF rows
  980-1011), `fuel_units`. `weo` is also identical: only its `source` text changed; 2025 is 0.043923870000000004
  instead of 0.04392387.
- `ecp`, `ets_semi`, `multipliers`, `scc`, `ghg_inventory`, `ch4_inputs`, `population`, `gwp_pollutants`,
  `gains_region`, `power_paths`.
- Transport: `transport_data`, `transport_data_sources`, `vehicle_prices`, `range_anxiety`, `transport_params`,
  `transport_paths`.

In particular, the IIASA CO2 EFs (rows 980-1011), the elasticities (Elasticities rows 143-282), the international
price forecasts and the US CPI/deflator are the same in 465.

### Changed

| csv | cells changed | largest changes (Egypt) | verdict |
|---|---|---|---|
| `energy_use` | 26 of 144 | ftr/nga 7,454.0 -> 6,903.7 (-7.4%); omn/die 3,819.2 -> 3,531.6 (-7.5%); ftr/lpg 2,465.8 -> 2,264.6 (-8.2%); rod/die 10,207.6 -> 10,010.6 (-1.9%); rod/gso 7,577.3 -> 7,404.3 (-2.3%); foo/die 927.0 -> 875.3 (-5.6%); avi/jfu 706.9 -> 652.3 (-7.7%); res/lpg 3,182.3 -> 3,107.5; res/nga 2,035.5 -> 1,921.2. Total of the 144 cells 50,452.8 -> 48,337.8 ktoe (-4.2%) | changed (data vintage: Balances) |
| `legacy_Balances` | 161 | eloutput total 218,984.8 -> 208,739.7; eloutput nga 175,355.6 -> 165,384.5; tes total 109,428.5 -> 101,398.5; tfc total 67,088.6 -> 61,682.4; tfc ecy 15,974.8 -> 14,536.4 (-9.0%) | changed (data vintage) |
| `legacy_EnergyCons` (from Balances) | 52 | nga elec 175,355.6 -> 165,384.5; nga pow 31,743.4 -> 29,443.7; ele pow -19,492.3 -> -17,948.4; ele cem 1,270.6 -> 1,158.4 (-8.8%) | changed (data vintage) |
| `energy_balance` (rows 503-509) | 33 | nga production 58,241.6 -> 55,271.7; oop tpes 37,023.7 -> 34,291.2; nga tpes 53,647.0 -> 52,488.5; nga own use -7,454.0 -> -6,903.7 | changed (data vintage) |
| `power_demand` (rows 3725-3739) | 10 of 15 | res 6,382.1 -> 5,907.9 ktoe; srv 4,021.5 -> 3,770.8; cem 1,270.6 -> 1,158.4 (-8.8%); omn 773.8 -> 713.8 | changed (data vintage) |
| `power_tech` | 24 (+9 source) | nga cap0 35,367 -> 52,020 MW, capacity factor 0.566 -> 0.363; sol cap0 3,327 -> 1,724 MW, CF 0.18 -> 0.324; wnd cap0 2,387 -> 1,643 MW, CF 0.30 -> 0.404; hyd cap0 3,880 -> 2,832 MW, invest_start 2022 -> 2030; opf nga 0.0065 -> 0.0101 $/kWh | changed (data vintage, and a legacy formula change: plant data A4 are now read from Power rows 112-294) |
| `power_params` | 5 values | sh_add -0.0162 -> ~0; gen_per_cons 1.2212 -> 1.2347; sh_tsd 0.1900 -> 0.1867; sh_eou 0.0382 -> 0.0387; sh_nxp 0.00924 -> 0.00926 (extra_eff stays 0, see 1) | changed (data vintage) |
| `gdp_level` | 105 | Energy trade balance, rows 741-743: tb_nga 2022 2.992 -> 3.201 USD bn (+7%); tb_oil 2022 -8.260 -> -8.038; tb_coa 2022 -1.436 -> -1.383. Share traded: nga 0.189 -> 0.195, oil 0.471 -> 0.469. GDP usd/lcu and manual SCC unchanged | changed (data vintage) |
| `legacy_IO_GTAP` (Egypt) | 645 numbers (+59 cells where 0 is now blank) | every series lower by 0-17%: output total 608,362 -> 548,072 (-9.9%); totd ofd 24,085 -> 20,107 (-16.5%); output cns 37,477 -> 31,640; year label still 2014 | changed (data vintage: GTAP) |
| `legacy_EF_PM`, `ef_nonco2` | +2 rows | 456 cut Egypt's table after 227 rows (a "." row); 465 adds cst/lpg bc 0.00507 and cst/lpg ch4 0.08 kt/PJ. The other 227 rows are identical | changed (completed table) |
| `legacy_ManualInputs_cells` | 30 | electricity price elasticity rows 298 and 307 (K-N): 0 -> -0.5; rows 315-316 (renewables, electricity): -0.5 -> -0.75; goal-seek flags in rows 11, 53, 54 (TRUE/FALSE) | changed (legacy defaults) |
| `legacy_Elasticities_cells` | 16 (8 cells gone) | column F, electricity rows 69-127: 0 -> -0.5; G112-G119 (industry) emptied. These are not the blocks `elasticities.csv` reads (rows 143-282 identical) | changed (legacy defaults) |
| `legacy_GHGs_cells` | 6 | rows 1196-1198 (energy CO2 2022-2024 check block): 2023 172.5 -> 207.2 Mt, difference -0.355 -> -0.225 | changed (cached results) |
| `legacy_CoC_cells` | +9 cells | new row 198 "Default (Uses Sri Lanka)" | changed (new default row) |
| `legacy_power_reference` | 1,018 | B2 caxav sol 2026 1,235.6 -> 1,200.2; B1 phi oop 2024 0.003 -> 0.197 | changed (cached results of 465) |
| `legacy_engineer_reference` | 5,010 (base 2,459, ctax 2,551) | cap nga ctax 2041 26,382 -> 74,116 MW; usd oop ctax 2029 75 -> 6,777 | changed (cached results of 465; different policy, see 3) |
| `legacy_transport_reference` | 19,438 (base 8,779, pol 10,659; +962 `legacy_row` cells, the policy offset) | r4655 pol 2041 228,598 -> 162,248; in txo_gso base 2030 -0.004 -> -0.276 | changed (cached results of 465; different policy, see 3) |

## 3. Points for the prototype build

1. **The policy run cached in 465 differs from 456.** The 465 Dashboard has a carbon tax of US$5 (Dashboard I6 = 5,
   I7 = 2040); 456 had US$50. The policy columns of `legacy_engineer_reference.csv` (run `ctax`) and
   `legacy_transport_reference.csv` (run `pol`) are therefore a US$5 run. Any check that compares the prototype's
   US$50 run with these columns needs the 465 settings.
2. **Transport method test passes on 465.** `transport_model_ref.legacy_test` reproduces the cached values of both
   465 runs to 1e-14 (base and pol).
3. **Power method test fails on 465.** `power_model_ref.legacy_test` matched 456 to 4e-13 but does not reproduce 465:
   'second|nga' is off by a factor of 550, and cap, gen, pe and dem differ by 2-70%. This is not a data error: 465
   changed about 100 formulas of the engineer power model (rows 2954-4300). Some examples:
   - A4 plant data: `MATCH(..., Power!A112:A294)+87`.
   - Capex time factor fallbacks: `ctf.old`, `wld.ctf.med.`.
   - L3155-L3157: the fuel price is a running average `AVERAGE($L:L)`, not a 5-year window.
   - L3398-L3400: the variable cost includes the carbon price.
   - L3660, L3663: the revenue terms.
   - L3773: the reserve requirement is dropped.
   - F3636: now reads `MTInputs!F351`.
   - Rows 4011, 4061-4118 and 4264-4284.

   The prototype's power engine (and `power_model_ref.py`) follows the 456 formulas. Before the power reference is
   used again, these changes have to be classified as bugs, issues or decisions.
4. **ISSUES.md and the register still describe the old route.** The LD41 text in `ISSUES.md`, the register and
   `Formulas.md` still says "energy use via kernel v1.6". It comes from `build.py` line 8251, which was not changed
   by this task. It should read "energy use from legacy 465 Mitigation rows 583-601" at the next build.
5. **legacy_cached_baseline.csv still comes from 456.** It is written by `legacy_compare.py`, which was not in the
   list of extractors and still reads 456.
