# Plan: separating the Global Fiscal Indicators dashboard from its database

For `new-ai-tools/TaxMacroFiscalDashboard/`. Companion of the CPAT plan
(`CPAT-AI/excel_ai/mitigation/Plans_v7_0.md` (section DataSeparation_Plan)); same design, adapted. Plan only.

## 1. The situation is different from CPAT

- The dashboard is already separated **in the build**: `build_global_indicators.py` (or `.R`) writes the panel
  `build/output/global_data_long.csv`, and `build_dashboard.py` turns it into the workbook. Only the panel and
  `config/indicators.csv` are shared.
- The workbook is small: `Global_fiscal_indicators_v1.2.xlsx` is 0.9 MB (Data_wide 217 x 135, Data_long 10,183 rows,
  latest value per indicator).
- It **needs every country**: Scores rescales each indicator 1-10 across the 217 countries, and coverage counts all
  of them. Filtering the cross-section to one country would break the scores.

So size is not the problem today. Separation helps with two other things: (i) refreshing data without rebuilding the
workbook, and (ii) adding the full time series (`global_long_all_years.csv`, 113,730 rows, 13 MB) without bloating
the tool.

## 2. The design

1. **Keep the cross-section embedded** (Data_wide, Scores, Data_long, Spec, Sources). It is small and every score
   depends on all countries.
2. **Publish the database** as files next to the tool, written by `build_global_indicators.py`:
   ```
   GFI_Data_<version>/
     manifest.csv                 file, rows, md5, vintage, licence
     global_data_long.csv         the cross-section (as now)
     by_country/<ISO3>.csv        the all-years series of one country (from global_long_all_years.csv)
   ```
3. **Add a "Country series" sheet** that shows the history of the selected country (Dashboard!C4) for every
   indicator, filled from `by_country/<ISO3>.csv`. Pre-split, one country is about 500 rows (13 MB / 217), so a load
   reads tens of kilobytes: well under a second.
4. **Loader: Power Query here, not a macro.** The dashboard is an `.xlsx` (no macros) built on Windows with `.bat`
   files, so Power Query is the natural fit. openpyxl cannot create queries; add them in a Windows post-step
   `3_add_queries.bat` -> `add_queries.py` using Excel COM (`Workbook.Queries.Add` and a table on the sheet linked to
   the query). The query reads the folder path and the country from two named cells. Each user sets the workbook
   privacy level to "Ignore" once (Data > Get Data > Query Options > Current Workbook > Privacy), or the cell-plus-file
   combination raises the firewall error. Refresh: Data > Refresh All.
5. **Refreshing the cross-section without a rebuild (optional, later):** Data_wide could also become a query over
   `global_data_wide.csv`; Scores would then recalculate from it. Only worth it if data updates are more frequent than
   tool releases.

## 3. (a) WB and IMF team members

Sync the team folder holding `GFI_Data_<version>/` with OneDrive; point the `DataFolder` cell at it once. Updating the
data = re-running `1_build_database.bat` and copying the output to the folder; everyone gets it on the next refresh.

## 4. (b) Other users

- The repository `cpmodel/new-ai-tools` is public, so the public part of the database can be served from it (or from
  a GitHub release): the query reads `https://raw.githubusercontent.com/.../by_country/<ISO3>.csv`. Pre-split files
  mean only the country's rows travel. Before publishing, add a `licence` column to `config/sources.csv` and check
  each source's terms (WEO, WoRLD, WDI and IDS are open; check the others, such as the CPAT fossil-fuel subsidy data
  and any World Bank internal extracts).
- Users without network or Power Query get the workbook as now (cross-section embedded) plus, if wanted, a
  one-country export of the series.

## 5. Speed

The same rules as CPAT: a fixed cost of a fraction of a second per query, plus the file size read. With one
pre-split file per country the series sheet refreshes in about a second from a synced folder, a few seconds from a
URL. The cross-section, if ever moved to a query, is a 0.1-1.4 MB CSV: about a second. Scores and the Dashboard
recalculate in well under a second at this size.

## 6. Steps for the next version (v1.3)

1. `build_global_indicators.py` (and the R twin): also write `by_country/<ISO3>.csv` and `manifest.csv`.
2. `build_dashboard.py`: add the Country series sheet with its headers, named cells `DataFolder` and `CountryCode`
   (= Dashboard!C4), and a note on the README sheet.
3. `add_queries.py` + `3_add_queries.bat` (Windows, Excel COM): add the query and its table.
4. Test on Windows: pick three countries, refresh, compare with `global_long_all_years.csv`.
5. VersionNotes row; previous workbook to `Archive/`.
