# Data interface of Coded CPAT and Excel-AI

**For the data person.** What the models read from a database: which files, in which layout, with which keys, and what the full (proprietary) database must contain. It is a code interface, not a user interface: it says what the loaders of Coded CPAT (`coded/cpat_model/data/`) and the builder of Excel-AI (`excel_ai/mitigation/build.py`) expect to find. Written 2026-10-29 (Coded CPAT plan, task 2.1; design decision D6).

The file-by-file list is [`interface_manifest.csv`](interface_manifest.csv): one row per file with its group, layout, legacy tab and version, keys, country-key convention, years, what the full database needs, proprietary status and notes. The manifest is the source; this page explains it. A test of Coded CPAT checks that its loaders read only the files the manifest lists.

## 1. The decisions behind it

- **Same data, same layout, both models.** Coded CPAT reads exactly the files Excel-AI is built from, in the same layout: the legacy CPAT tables as they are in the legacy workbook (`CPAT 1.0pre_465`), with legacy column headers, codes and country keys. Nothing is reshaped into a second format, so the two models cannot read different numbers. (A tidy Python layout may come later, with a converter; it is not part of this interface.)
- **CSV files in the current `data/` folders** (D6). No new database format.
- **A database is a folder** holding the files of the manifest under the same names. There are two:

| Database | Where | Contents |
|---|---|---|
| `full` | The private data repository, never this one | Every file of the manifest, every country, including the four proprietary tables |
| `dummy` | This repository | The same files; the four proprietary tables (and the files derived from them) with dummy values |

Today the folder [`mvp_legacy_extracts/`](mvp_legacy_extracts/) is the database Excel-AI is built from: the public legacy tables plus the Egypt rows of the proprietary tables that the public legacy file (`NoPropData`) contains. It is the starting point of both databases (section 6).

- **Selecting a database** (Coded CPAT, `coded/.env`): `DATA_ENVIRONMENT=full` with `FULL_DATA_PATH` pointing at the folder in the private repository, or `DATA_ENVIRONMENT=dummy` (today's names `real` and `REAL_DATA_PATH` are renamed in task 2.6). Systematic comparisons use `full` where it is available, `dummy` otherwise; every model in a comparison reads the same database.

## 2. The four proprietary tables

| Table | File | Legacy tab | Derived files (also proprietary) |
|---|---|---|---|
| Energy balances | `legacy_Balances.csv` | Balances | `legacy_EnergyCons.csv`; range-anxiety fit (fitted on a run that used them) |
| Domestic prices | `prices_dom.csv` | Prices_dom | `prices_dom_changes.csv`, `prices_dom_header.csv` (layout only) |
| GTAP input-output | `legacy_IO_GTAP.csv` | IO_GTAP | - |
| Household survey | `legacy_HHSurvey.csv` | HHSurvey | - |

Rules: the full versions live only in the private repository; never commit them, nor anything computed from them (root `NORMS.md` section 8). The checks of Excel-AI also keep cached legacy runs (`legacy_*_reference.csv`, `legacy_cached_baseline.csv`, `energy_use.csv`, `energy_balance.csv`): they are derived from proprietary data too, and are not part of the model interface.

## 3. Layouts

Every file is UTF-8 CSV, comma-separated, one header line, `.` as decimal point, no thousands separators, blank for missing. Numbers keep full precision (the loaders parse them exactly; do not round). Two layouts:

| Layout | Files | Form |
|---|---|---|
| **Table** | `legacy_<Tab>.csv` and the other tables | The legacy table as it is: the legacy header row, then one row per record. Column names, codes and their case exactly as legacy (for example `country_code`, `SERIES_CODE`, `egy.mit.enc.coa`) |
| **Cells** | `legacy_<Tab>_cells.csv` | A legacy tab that holds several tables at fixed addresses, kept at those addresses: columns `row,col,value`, 1-based legacy row and column numbers, one line per non-empty cell, values as typed (text or number) |

**Country keys are as legacy, and legacy is not uniform** (the manifest gives each file's convention): mostly ISO3 upper case (`EGY`); ISO3 lower case in `legacy_IO_GTAP.csv`, `legacy_EF_PM.csv`, `legacy_EF_GHG.csv`, `legacy_ETS+LTS_cells.csv` and inside codes; country names in `legacy_Transport3_cells.csv` and the Prices_int country assumptions; the ISO3 of `legacy_GoalSeekCoal.csv` sits in a column named `Region`. Keep each file's convention: the models replicate legacy's lookups. Regional and world rows (World Bank regions, `world`) stay where legacy has them (EF_PM, EF_GHG, WEO, GDPRatios, UNPop).

**Years** are columns where legacy has them as columns (WEO 2000-2040, UNPop 2019-2050, GDPRatios 1960-2023, Transport2 2022-2040) and a column `year` otherwise.

## 4. The files, by group

| Group | Files | What the full database needs |
|---|---|---|
| **A. Country tables** (23) | `legacy_Balances`, `legacy_EnergyCons`, `prices_dom` (+ `prices_dom_header`, `prices_dom_changes`), `legacy_HHSurvey`, `legacy_IO_GTAP`, `legacy_HH_Elast`, `legacy_ASPIRE`, `legacy_WHOCooking`, `legacy_GDPRatios`, `legacy_WEO`, `legacy_UNPop`, `legacy_SCC`, `legacy_CH4Inputs`, `legacy_GoalSeekCoal`, `legacy_NDCs`, `legacy_GHGHist`, `legacy_EF_PM`, `legacy_EF_GHG`, `legacy_OilProductShares`, `legacy_Transport1`, `legacy_Transport2` | Every country (and region where legacy has regions), the legacy columns |
| **B. Legacy tabs at their addresses** (10) | `legacy_Countries_cells`, `legacy_Elasticities_cells`, `legacy_Prices_int_cells`, `legacy_Power_cells`, `legacy_CoC_cells`, `legacy_GHGs_cells`, `legacy_ECP_cells`, `legacy_ETS+LTS_cells`, `legacy_Multipliers_cells`, `legacy_Transport3_cells` | The whole legacy tab from row 3 (these already hold every country) |
| **C. Global parameters** (8) | `transport_params`, `transport_paths`, `fuel_units`, `distn_catmap`, `distn_programs`, `distn_gtapmap`, `distn_passthrough`, `../range_anxiety_fit/range_anxiety_fit` | Unchanged (not country data), except the range-anxiety fit (one row per fitted country) |

Not part of the interface (Coded CPAT will hold these in its code or inputs, so the data person need not maintain them): the files Excel-AI reads only for row structure or labels (`elasticities.csv`, `multipliers.csv`, `ghg_inventory.csv`, `legacy_GHGs.csv`, `power_paths.csv`, `power_params.csv`, `power_demand.csv`, `population.csv`), the few values typed from Egypt runs (`gdp_level.csv`: the manual SCC path, which belongs to the advanced inputs; `power_tech.csv`: four constants per generation type), the code tables (`code_renames_v0_7_2.csv`, `codes_crosswalk_v0_7_1.csv`, `mtinputs_465.csv`), and the files read only by checks or by nothing (`excel_ai/mitigation/check_full.py` and the reference models). The air-pollution tables (`air_pollution/legacy_459/`) are read by the air-pollution standalone, not yet by these models.

## 5. Input files (new: `data/inputs/`)

The model's input files sit beside the data (D5, D6):

| File | Form |
|---|---|
| `inputs/scenarios_<name>.csv` | A scenario set: one row per MTInputs row (the legacy 465 rows 8-413 in order, from `mvp_legacy_extracts/mtinputs_465.csv`, then the Excel-AI additions, `ModelForm` last), columns `row`, `NameOfParameter`, `unit`, then one column per scenario (scenario 1 = baseline). Two header lines above the rows give each scenario's name and its countries (ISO3, or `all`). Values in legacy units (percentages as whole numbers where legacy does, I85). Excel-AI's `ScenarioDefinition` columns paste into it |
| `inputs/advanced_<name>.xlsx` | Advanced inputs: tab `ManualInputs` (the legacy Manual inputs tab in the cells layout; default `mvp_legacy_extracts/legacy_ManualInputs_cells.csv`), tabs `Settings` and `Constants` (Excel-AI defaults) |

Scenario files with proprietary values stay in the private repository like the data.

## 6. Open points for the data person

1. **`prices_dom.csv` holds 220 countries of real-looking prices (2021-2024), committed to this repository** since v0.7.2. They come from the earlier price-module prototype (`excel_ai/standalone_initial_prototypes/CPAT_PriceModule_Data_1.xlsx`), not from legacy. Domestic prices are one of the four proprietary tables: confirm whether these values may be in the repository; if not, they need replacing by dummy values and removing from the history (the user decides).
2. **Prices_dom layout.** The models read the 99 columns of the price-module layout (codes `mit.<variable>.<fuel>.<sector>`); legacy Prices_dom has 142 columns and 8 header rows. The full database should deliver at least these 99 columns under these codes (extra columns are ignored).
3. **Cut to Egypt in the repository although legacy 465 has every country:** `legacy_IO_GTAP.csv` (proprietary), `legacy_ASPIRE.csv`, `legacy_WHOCooking.csv` (public). The full database needs every country; ASPIRE and WHOCooking can come back whole into this repository (set `EGYPT_ONLY` in `excel_ai/mitigation/extract_legacy_tables.py`).
4. **Legacy versions differ:** HHSurvey and HH_Elast come from legacy 456, everything else from 465 (air pollution: 459). Deliver the 465 versions where they exist.
5. **The dummy database is not complete yet.** Dummy versions of EnergyCons, Prices_dom, HHSurvey and IO_GTAP exist in the legacy layout (`legacy_dummy/CPAT_LegacyData_dummy_csv/`), but not of Balances, which Excel-AI reads (`BalancesOrConsumption` = Balances); and the dummy Prices_dom is in the 142-column legacy layout. Assembling `dummy` (the public files of `mvp_legacy_extracts/` plus dummy proprietary tables) is a Coded CPAT task (`coded/TODO.md`, 2.6).
6. **Files with no writer script** (made by hand once): `legacy_GoalSeekCoal.csv`, `distn_gtapmap.csv`, `distn_passthrough.csv`. Their sources are in the manifest.
7. **`transport_paths.csv`** comes from Egypt's legacy run (BEV stock fuel economy, charging cost per port); whether legacy makes these country-specific is not yet checked.
8. **Module values typed in the builder, not in a data file.** The air-pollution and transport co-benefit values that Excel-AI's tabs `FromAirPollution` and `FromTransportCB` carry (value of averted PM2.5, concentration coefficients, costs per vehicle-km; Egypt from the legacy 465 run, 0 elsewhere) are typed in `excel_ai/mitigation/build.py`. They move to a data file of group C when the placeholder modules are built (`coded/TODO.md`, 2.10), and the manifest gains its row then.
