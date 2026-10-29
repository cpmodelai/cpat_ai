# data - every data file of the repository, and the scripts that convert them

All data live here (root `NORMS.md` section 8): the inputs of Coded CPAT, the data workbooks the Excel prototype links to, the dummy data in the legacy layout, the legacy extracts the MVP is built from, and the distribution data. Code reads them from here; nothing is copied into the project folders. Only dummy or public data are committed; real (proprietary) data stay outside the repository.

## Quick start

- **MVP data link (Windows):** in `CPAT-AI-Mitigation-MVP-v7.1.xlsm`, sheet ScenarioCompare, source table row "Dummy - local file", column Path or URL (blank = searched next to the workbook and in `<repo>/data/workbooks/`): `C:\<your repos>\CPAT-AI\data\workbooks\CPAT_Data_dummy_python.xlsx` (plain text). Then choose that source and click Update data tables. SharePoint: upload this file over the existing one, keeping the SharePoint file name.
- **Coded CPAT** reads `dummy/` by default (`coded/config.py`).
- **Paste into legacy CPAT:** `workbooks/CPAT_Data_dummy_cpat.xlsx` (Index sheet: the range of each sheet) or `legacy_dummy/`.
- **After changing `dummy/`:** from `data/`, run `python scripts/build_data_workbook.py`, then `python scripts/convert_data_workbook.py to-cpat`, then `pytest tests`.

## Layout

| Folder | Contents | Written by | Read by |
|---|---|---|---|
| `dummy/` | The Coded CPAT inputs, dummy version: 38 CSVs (fake values in the real formats; `HHSurvey`/`IO_GTAP`-type distribution tables are Egypt from the public legacy file) | by hand; `distn_*.csv` by `excel_ai/distribution/scripts/build_distribution_model_data.py` | Coded CPAT (`coded/config.py`: `DATA_PATH`, default `../data/dummy`; `real` reads `REAL_DATA_PATH`) |
| `workbooks/` | The data workbook of each version, in two formats: `CPAT_Data_dummy_python.xlsx` (Python format: one `c_` table per CSV, the `L_` tables, README, Index) and `CPAT_Data_dummy_cpat.xlsx` (CPAT format: the legacy data sheets at legacy cell addresses) | `scripts/build_data_workbook.py`, `scripts/convert_data_workbook.py` | the MVP's DataLinks (Power Query, `L_` tables); people pasting into legacy CPAT |
| `legacy_dummy/` | `CPAT_LegacyData_dummy.xlsx`, `_csv/`, `_ReadMe.md`: the four proprietary tables (EnergyCons, Prices_dom, HHSurvey, IO_GTAP) in the legacy layout | `scripts/export_to_legacy.py` | legacy CPAT (paste); checks |
| `mvp_legacy_extracts/` | The tables the mitigation MVP is built from: `legacy_<Tab>.csv` (verbatim from the legacy workbook), `legacy_<Tab>_cells.csv` (tabs kept at legacy addresses), derived tables, `mtinputs_465.csv` (every input row of legacy 465 MTInputs: name, legacy name, Name Manager; `extract_inputs.py`, v8.4), `source/` (country price files), `tracker_mapping.json` | the MVP's `extract_*_v<n>.py`, `update_prices_egypt_v<n>.py` | `excel_ai/mitigation/build_v<n>.py`, checks, reference models; `L_Balances` of the data workbook |
| `distribution/` | The distribution data pipeline, one workbook per stage: `data_bymodule`, `data_tabular`, `data_standardized` and the two `_regenerated` checks | `excel_ai/distribution/scripts/` (`run_all.py`) | the distribution workbook, `build_distribution_model_data.py` |
| `air_pollution/legacy_459/` | Nine public Air Pollution reference tables and source-dimensions manifest from legacy 459 NoPropData | `scripts/extract_air_pollution_legacy.py` (read-only source) | `excel_ai/air_pollution/build_workbook.py`; regression: `python -m pytest data/tests/test_extract_air_pollution_legacy.py -q` from the repository root |
| `scripts/` | The conversion scripts: `export_to_legacy.py` (+ `legacy_layouts.json`), `build_data_workbook.py`, `convert_data_workbook.py` (+ `cpat_layouts.json`) | - | - |
| `tests/` | pytest for the scripts: `pytest tests` from this folder (15 tests; about 2 minutes) | - | - |

The legacy workbook itself (`excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb`, and 459) stays in `excel_ai/legacy/workbooks/`: it is the read-only reference model, not data. The test fixtures of Coded CPAT stay in `coded/cpat_testing/model/data_expected/`.

## Scripts

Run from `data/`:

```bash
python scripts/build_data_workbook.py                      # dummy/ -> workbooks/CPAT_Data_dummy_python.xlsx
python scripts/convert_data_workbook.py to-cpat            # workbooks/..._python.xlsx -> workbooks/..._cpat.xlsx
python scripts/convert_data_workbook.py to-python          # workbooks/..._cpat.xlsx -> workbooks/..._python.xlsx
python scripts/convert_data_workbook.py to-cpat --in dummy --out x_cpat.xlsx                 # from a CSV folder
python scripts/convert_data_workbook.py to-python --in x_cpat.xlsx --out x_python.xlsx --csv-dir x_csv
python scripts/export_to_legacy.py --data dummy --out legacy_dummy/CPAT_LegacyData_dummy.xlsx --csv-dir legacy_dummy/CPAT_LegacyData_dummy_csv
python scripts/build_data_workbook.py --data /path/real --version real --out /path/CPAT_Data_real_python.xlsx   # real data: outside the repo
```

### Python format and CPAT format (`convert_data_workbook.py`)

- **Python format** (`CPAT_Data_<version>_python.xlsx`, `build_data_workbook.py`): README, Index (layout, size, country filter column, proposed licence class, MVP tab, MD5 of each source CSV), one `c_` table per CSV as it is, and the `L_` tables in the MVP layout (EnergyCons, Prices_dom, HHSurvey, IO_GTAP as `export_to_legacy.py` builds them; v7.1: WEO, GDPRatios, HH_Elast, UNPop through the CPAT-format converters of `convert_data_workbook.py`; Balances from `mvp_legacy_extracts/legacy_Balances.csv`). The MVP (v7.1) links nine tabs to them, copied by column name. Every table is an Excel table with a header in row 1 and, where it has a country column, a last column `FilterISO3`.
- **CPAT format** (`CPAT_Data_<version>_cpat.xlsx`): 17 legacy data sheets with the legacy names, header rows and cell positions (EnergyCons, Prices_dom, HHSurvey, IO_GTAP, WEO, WDI, UNPop, GDPRatios, GHGs, CH4Inputs, OilProductShares, EF_GHG, CalVal, Air_Data, HH_Elast, ASPIRE, WHOCooking), so a data block pastes onto the legacy sheet at the same address; `py_` sheets for the 21 tables whose legacy tab holds several tables (carried in the Python layout); `pyx_` sheets for the Python cells legacy has no place for; README and Index (data range, blank legacy columns, Python column order).
- **Round trip:** every `to-cpat` converts back in memory and stops on any difference. Python workbook -> CPAT -> Python is exact; CSV -> workbook keeps 16 significant digits (openpyxl), and a whole float comes back as an integer.
- **Codes:** WEO BCA_BP6, BCA_GDP_BP6, ENDA and PCPI_PCH are written as the legacy series BCA, BCA_NGDPD, XDC_USD.PA_RT and PCPIPCH (to be confirmed); WDI fills the second legacy block (header row 265).

### Legacy export (`export_to_legacy.py`)

The four proprietary input tables in the legacy layout, ready to paste into the legacy workbook:

| Coded CPAT file | Legacy sheet | Layout |
|---|---|---|
| `energy_consumption.csv` (country x sector rows, fuel columns) | `EnergyCons` | row 1 header, data from A2; one row per country x fuel, sector columns `elec` ... `neu`; key `egy.mit.enc.ele` |
| `prices_dom.csv` | `Prices_dom` | rows 1-8 header (fuel, sector, indicator, unit, code), data from A9; one row per country-year |
| `distn_hh_survey.csv` (long) | `HHSurvey` | row 1 header, data from A2; wide, one column per variable |
| `distn_io_gtap.csv` (long) | `IO_GTAP` | row 1 header, data from A2; wide, one column per GTAP sector |

- **Energy:** legacy Mitigation reads `EnergyCons` (rows 583-601) when the Dashboard switch `BalancesOrConsumption` is not "Balances". The IEA flow-level `Balances` sheet cannot be rebuilt from `energy_consumption.csv` (already aggregated to CPAT sectors). `ren` and `total_energy_use` are not exported (legacy computes them); coded `hea` is legacy `heat`; `wav` and `neu` are blank; `--energy-year` (default 2022) sets the Year column.
- **Prices:** 48 legacy columns are not in `prices_dom.csv` (source and reliability flags, `taxa`, `sub.or` overrides, production volumes, spot prices) and are left blank. `countrycode_weo` is the ISO code.
- **NoPropData file:** some lookups into the stripped sheets were shrunk to row 1 there (e.g. Mitigation `AA583`); widen them before pasting. The full workbook has them.
- **Precision:** the CSVs are read with `float_precision='round_trip'`, so every value equals the CSV text.
- **Layouts:** header rows from `legacy_layouts.json` (`--rebuild-layouts`, needs `pyxlsb`); `convert_data_workbook.py` keeps its own in `cpat_layouts.json`.

## Rules

- Only dummy data are committed. `CPAT_Data_*.xlsx` and `CPAT_LegacyData*.xlsx` are git-ignored except the dummy files; an export of real data (`--data` pointing at `REAL_DATA_PATH`) stays outside the repository.
- When `dummy/` changes, rebuild in the same task: `workbooks/` (both formats), `legacy_dummy/` (`NORMS.md` section 8), and run `pytest tests`.
- Every workbook a script writes passes `excel_ai/shared/excel_lint.py` (`NORMS.md` section 3g).
