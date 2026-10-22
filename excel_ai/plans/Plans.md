# Plans (CPAT-AI-Mitigation-Prototype v6.5)

Every plan for work not built yet, in one note. Each section is a former plan note, unchanged apart from its headings; its former file name is in the section title, so a reference by that name finds it. Built work is described in the method notes, not here.

1. [Plan: separating the Excel tool from its database (CPAT-AI-Mitigation-Prototype)](#1-plan-separating-the-excel-tool-from-its-database-cpat-ai-mitigation-mvp-dataseparation_plan) (former `DataSeparation_Plan_v6_4.md`; section 8: v6.5, the linked tables)
2. [Remaining switches and inputs to append at the bottom of ScenarioDefinition: plan (built in v5.6, except the scenario rows)](#2-remaining-switches-and-inputs-to-append-at-the-bottom-of-mtinputs-plan-built-in-v56-except-the-scenario-rows-mtinputs_appendix_plan) (former `MTInputs_Appendix_Plan_v6_4.md`)
3. [Power engineer model: features to add (plan, 2026-10-18; decisions recorded)](#3-power-engineer-model-features-to-add-plan-2026-10-18-decisions-recorded-powerfeatures_plan) (former `PowerFeatures_Plan_v6_4.md`)
4. [CPAT policy taxonomy, extended to cover every FTT policy (plan, 2026-10-20; decisions open)](#4-cpat-policy-taxonomy-extended-to-cover-every-ftt-policy-plan-2026-10-20-decisions-open-policytaxonomy_plan) (former `PolicyTaxonomy_Plan_v6_4.md`)
5. [Plan 2: air pollution module (legacy sheet Air pollution and its 9 data tabs)](#5-plan-2-air-pollution-module-legacy-sheet-air-pollution-and-its-9-data-tabs-plan_airpollution) (former `Plan_AirPollution_v6_4.md`)
6. [Plan 3: transport externalities (accidents, congestion, road damage)](#6-plan-3-transport-externalities-accidents-congestion-road-damage-plan_transportexternalities) (former `Plan_TransportExternalities_v6_4.md`)
7. [Plan 1: everything else (user request 2026-10-19; status at v6.1, 2026-10-20)](#7-plan-1-everything-else-user-request-2026-10-19-status-at-v61-2026-10-20-plan_rest) (former `Plan_Rest_v6_4.md`)
8. [Data request](#8-data-request-datarequest) (former `DataRequest_v6_4.md`)

## 1. Plan: separating the Excel tool from its database (CPAT-AI-Mitigation-Prototype) (DataSeparation_Plan)

User request (2026-10-20): a simple way to keep the global data out of the Excel tools, so that each tool holds only
what it needs: (a) for WB and IMF CPAT team members, (b) for other users. Is it quick for Excel to pull data from an
outside source, filtered by country? Is there a time cost per table? Consider it for the next version. A version for
the Global Fiscal Indicators dashboard (`new-ai-tools/TaxMacroFiscalDashboard`) is a separate note
(`DataSeparation_Plan_Dashboard.md`, to go in that repo).

Status: plan only. Nothing is built. The timings below are typical figures, not measurements; step 1 measures them on
a WB/IMF laptop before anything else is built.

**Update (user 2026-10-20, second request): section 7 supersedes sections 2-6 where they differ.** All the data go
into one workbook per data version (the dummy one is built: `data/workbooks/CPAT_Data_dummy_python.xlsx`); the
prototype keeps Egypt embedded and refreshes only a few big or possibly proprietary tables, by **Power Query**,
from a URL chosen by a data-version selector; and a simple dashboard goes on ScenarioCompare (built in v6.4: section 7.6).

Versions: this plan targets **v6.5**. v6.4 (2026-10-20) made ScenarioCompare the dashboard and changed no data tab, so sections 1-5 and 7.1-7.5 hold for v6.4 as written (the v6.2 sizes of section 1 are unchanged within 0.1 MB).

### 1. Where the size is today (v6.2, measured)

`CPAT-AI-Mitigation-Prototype-v6.2.xlsm` is 12.8 MB:

| Part | Zipped size | Notes |
|---|---|---|
| Mitigation sheet (the model) | 5.3 MB | stays in the tool |
| Other model sheets (Distribution, Inputs, LiveOutputs, StoredOutputs, LambdaTest, ...) | 1.3 MB | stays |
| Data tabs | about 6 MB | WEO 1.2, Power 0.8, Transport1 0.7, GHGs 0.5, Transport2 0.5, GDPRatios 0.4, Prices_dom 0.4, HH_Elast 0.4, the rest small |

Most data tabs already hold **all countries** (WEO, Transport1-2, GDPRatios, HH_Elast, CH4Inputs, Prices_dom, GHGs,
UNPop, NDCs: 190-266 countries each), of which the model uses one. The proprietary tabs (Balances, HHSurvey, IO_GTAP,
EF_PM, ASPIRE, WHOCooking) hold **Egypt only**, because the public legacy file has nothing else. With the full
proprietary data for every country they would grow about 200 times, and the tool would pass 50-100 MB. That, more
than today's size, is the reason to separate.

Filtered to one country, the data tabs shrink from about 6 MB to well under 1 MB, and the tool to about 7 MB.

### 2. The design (same for every user)

**One database, one country in the tool.**

1. **The database** is a folder of plain CSV files, one per data tab, with the same columns and codes as the tab
   (the copy-in rules of `DataTabs.md` and NORMS 1.5 do not change):
   ```
   CPAT_Data_<release>/
     manifest.csv          tab, file, type (L / A), licence (public / restricted), source, vintage, rows, md5
     global/               tables the model reads across countries (EF_GHG, SCC, Prices_int, Elasticities, ...)
     by_country/EGY/       one file per country tab, holding that country's rows only
     by_country/KEN/ ...
   ```
   Pre-splitting by country is the main speed trick: Excel then reads a few kilobytes per table instead of reading
   the whole global file to keep one country (section 4). The folder is written by one script from the files the
   build already uses (`data/mvp_legacy_extracts/legacy_<Tab>.csv`), so there is one source of truth.
2. **The tool** keeps the data tabs, their names and their layouts, so every formula, named range and check stays as
   it is. The tabs are simply filled for one country. The all-country test (`check_allcountry.py`) already shows
   the model gives the same results whatever other rows sit in the tables; a one-country fill is the easy case.
3. **The loader** is a macro, `LoadCountryData`, on a button on Inputs, next to the country selection. It reads
   `DataFolder` and the country code from two named cells, turns calculation off, writes each table in one block
   (L tabs at A4, A tabs at their legacy addresses from row 3), turns calculation back on and recalculates once. It
   writes the manifest line of every table it loaded (vintage, md5, rows) to a small log block on Settings, so every
   run records exactly which data it used.

**Why a macro rather than Power Query.** Power Query is the standard Excel route and works, but for this tool it has
three drawbacks: (i) it writes tables, not cells at fixed addresses, so the ten tabs kept at legacy addresses (Power,
GHGs, ECP, Elasticities, ...) do not fit; (ii) openpyxl cannot create queries, so the Linux build could not make them
(a Windows COM step would be needed); (iii) combining a cell value (the country) with a file triggers Power Query's
privacy "firewall" error unless each user changes a privacy setting. The prototype is already a macro workbook built with
an injected `.bas`, so a loader fits the existing build. For the `_noMacros` variants, Power Query remains the option
(section 5, b3).

**Two variants of every release.**
- `..._Linked.xlsm`: the model with empty data tabs (or one default country) and the loader. For the team.
- `..._<ISO3>.xlsm` / `.xlsx`: the model with one country filled in, as today. For anyone without the database:
  works offline, in LibreOffice, with no macros. This is what the build makes now, so nothing is lost.

### 3. (a) WB and IMF CPAT team members

- **Where the database lives:** a Teams/SharePoint folder restricted to the CPAT team (the proprietary tables, IEA
  balances, GTAP, household surveys, may only go to licensed users). Each member syncs it with OneDrive ("Add
  shortcut to My files" or "Sync"), so Excel reads a local folder: fast, works offline once synced, and no Excel
  sign-in prompts. Direct SharePoint URLs also work but add network time per file and authentication issues; avoid.
- **Path:** the synced path differs by user (`C:\Users\<name>\OneDrive - WBG\...` vs IMF tenants). The loader finds
  it from the `OneDrive`/`OneDriveCommercial` environment variables plus a relative path, else asks once with a folder
  picker and stores it in `DataFolder`.
- **Use:** open the tool, pick the country, click **Load country data**, wait (section 4), run as usual. Switching
  country is the same click; no file copies, no pasting.
- **Updates:** the data owner (one person) replaces files in the folder and bumps `vintage` in the manifest. Everyone
  gets them on the next load; the Settings log shows which vintage a result used. Old releases stay in their own
  `CPAT_Data_<release>/` folder, so old results remain reproducible.
- **Saving a country file:** after a load, Save As gives a self-contained one-country workbook to send to a country
  team. It is the `_<ISO3>` variant, made by hand.

### 4. Is it quick? The time per table

Yes, for one country it is quick. A load has four costs:

| Cost | Size | How to keep it small |
|---|---|---|
| Fixed per table: open the file, parse, write | about 0.1-0.5 s per table | fewer, pre-split files; screen updating and events off |
| Reading the source | proportional to file size: a few MB of CSV is under a second locally; xlsx sources are several times slower to parse; network/SharePoint adds about 0.5-2 s per file | CSV rather than xlsx; pre-split by country, so only the country's rows are read; synced local folder |
| Writing rows to the sheet | negligible for one country (a few hundred rows a tab) | write one array per table, never cell by cell |
| Recalculating the model | probably the largest single cost, the same as any full recalculation of v6.2 today | calculation off during the load, one recalculation at the end |

So yes, there is a cost per table, but it is small: with about 25 country tables and pre-split files, expect roughly
**5-15 seconds** of loading plus one recalculation. Without pre-splitting (each table filtered from its global file)
expect 20-60 seconds, and more from xlsx sources or over the network. Power Query is in the same range; its fixed cost
per query is a little higher.

What would make it slow: reading the global files and filtering in Excel, xlsx sources, SharePoint URLs instead of a
synced folder, recalculation left on during the load (one recalculation per table), or writing cell by cell.

### 5. (b) Other users (country teams, partners, the public)

Licensing decides the route: the public database (WEO, UN population, GHGs, NDCs, emission factors, ...) can be
published; the proprietary tables cannot.

1. **Download a country pack (recommended, simplest).** For each release, publish the `_<ISO3>` workbooks (one per
   country, public data filled, proprietary tabs marked "supply your own") and a zip of the public database. Users
   need nothing else: no network, no settings, works in LibreOffice. Those with their own proprietary data paste it
   in under the existing copy-in rules (`DataTabs.md`); the paste checks flag what is missing.
2. **Linked to a public folder.** The `_Linked` tool with the public database unzipped anywhere; the loader works the
   same. Missing restricted files leave those tabs as they are, with a warning naming them.
3. **Power Query from a public URL (for the `.xlsx` variants, later).** Host the public `by_country/` CSVs at a stable
   URL (a public GitHub repository or the WB/IMF data sites) and give a template query per tab that reads
   `<url>/by_country/<ISO3>/<Tab>.csv`. Because the files are pre-split, only the country's rows travel over the
   network, which keeps it fast. Users must set the workbook's privacy level to "Ignore", and Mac support for web
   sources is limited; hence later, and only if asked for.

### 6. Building it into the next version (v6.5)

Proposed steps. Steps 1 and 6 need Windows Excel (the user); the rest builds on Linux as now.

1. **Benchmark first (user, about 15 minutes).** A small test macro loads three tables (WEO, Transport1, GDPRatios)
   for Egypt from (i) the global CSVs, filtered, and (ii) pre-split files, from a synced folder and a SharePoint URL,
   and reports the seconds for each. This settles the speed question with real numbers before anything else is built.
2. **Database export:** `export_database_v6_5.py` writes `CPAT_Data_v6_5/` (global, by_country, manifest with
   licence, vintage and md5) from `data/mvp_legacy_extracts/legacy_*.csv` and the other data sources of the build.
3. **Loader:** `LoadCountryData` in the macro module (`CPATScenarios.bas`), with `DataFolder`, the country code,
   the load log on Settings, and a check that every manifest table arrived with the expected column headers (so a
   reshaped source cannot shift columns silently).
4. **Variants:** `make_variants.py` adds `_Linked` (data tabs emptied to their header rows) next to today's
   one-country variants.
5. **Checks:** the quick check loads Egypt from the database into `_Linked` and requires every output identical to
   the embedded build (max abs diff 0); `check_allcountry.py` runs on the exported database.
6. **Team trial (user):** two or three team members load two countries each from the synced folder.

Open points for the user:
- which tables are restricted (licence column), and who owns the SharePoint folder and the updates;
- whether the A tabs that are global (Power, GHGs, Elasticities, ECP, ...) should also move to the database in v6.5,
  or stay embedded until the L tabs are proven (they are about 2 MB);
- whether the public country packs are wanted for every country or on request.

### 7. Update (user 2026-10-20): one data workbook, a few linked tables, Power Query, a version selector

User decisions: all the data go into one xlsx per data version; only certain tables of the prototype link to the
online version (the biggest and the possibly proprietary ones); a selector picks the data version (dummy, real,
real except the proprietary tables, which are dummy); the prototype must still work out of the box with one country
(Egypt) loaded; a simple dashboard on ScenarioCompare. The data workbook is built; the dashboard is built in v6.4 (section
7.6); the rest is for v6.5.

#### 7.1 The data workbook (built)

`data/workbooks/CPAT_Data_dummy_python.xlsx` (9 MB), written by `data/scripts/build_data_workbook.py`
from `data/dummy/` (fake, non-proprietary data in the real formats):

- **README** and **Index** (one row per table: sheet, source file, layout, rows, columns, country filter column,
  number of countries, proposed licence class, the prototype tab it feeds, MD5 of the source CSV, header changes).
- **38 `c_` tables**, one per CSV, the file as it is (144,000 rows in all). Their layout is the Coded CPAT one.
- **4 `L_` tables** in the prototype layout, ready to load: `L_EnergyCons`, `L_Prices_dom`, `L_HHSurvey`, `L_IO_GTAP`
  (built as `export_to_legacy.py` does; identical, cell for cell, to `CPAT_LegacyData_dummy_csv/`). The header is
  the legacy code row, which is header row 3 of the prototype tab.
- Every table is an Excel table (header row 1) named as its sheet, and has a last column **FilterISO3** where it has a
  country column, so every query filters the same way and then drops that column.
- Checked: every cell equals its CSV (numbers to 1e-14), and the file opens in LibreOffice.

The other versions are built by the same script, with the same table names and columns, so that a query works on
any of them: `--data data/<version> --version <version>` for the versions kept in `data/`, and
the real version on the restricted OneDrive/SharePoint site only (never in the repository; `.gitignore` covers
`CPAT_Data_*.xlsx` except the dummy). The licence classes in the Index are proposals (from the tables legacy strips
in its NoPropData file) for the CPAT team to confirm.

**Gaps for the linked tables.** Only the four `L_` tables exist in the prototype layout. WEO, GDPRatios, HH_Elast and GHGs
have dummy data in the Coded CPAT layout only (`c_weo`, ...), to be converted to `L_` tables; Balances and
Transport1-2 have no dummy data at all (Balances cannot be rebuilt from `energy_consumption.csv`, which is already
aggregated to CPAT sectors).

#### 7.2 The method: Power Query, from a SharePoint/OneDrive URL

Yes, Power Query (Data > Get Data), and yes, please send a SharePoint URL: it goes into the version table below,
and you test the refresh, since this session cannot reach it.

- **Which URL.** Open the file in Excel desktop from SharePoint, then File > Info > Copy path, and delete any
  trailing `?web=1`. It looks like `https://<tenant>.sharepoint.com/sites/<site>/Shared Documents/<folder>/CPAT_Data_real.xlsx`
  (OneDrive: `https://<tenant>-my.sharepoint.com/personal/<user>/Documents/...`). A "Share" link does not work.
- **The query for one table** (the prototype tab's header list keeps the columns in the prototype's order, so a reshaped source
  cannot shift them):
  ```
  let
      Url     = Excel.CurrentWorkbook(){[Name="DataUrl"]}[Content]{0}[Column1],
      Country = Excel.CurrentWorkbook(){[Name="CountryCode"]}[Content]{0}[Column1],
      Book    = Excel.Workbook(Web.Contents(Url), true, true),
      T       = Book{[Item="L_HHSurvey", Kind="Table"]}[Data],
      Rows    = Table.SelectRows(T, each [FilterISO3] = Country),
      Out     = Table.RemoveColumns(Rows, {"FilterISO3"})
  in
      Out
  ```
  Its result is the Excel table on the prototype tab (header row 3, data from A4, where the Egypt rows sit now).
- **First refresh, once per user:** sign in with "Organizational account"; set Data > Get Data > Query Options >
  Current Workbook > Privacy to "Ignore the privacy levels" (else combining the cells with the file raises the
  firewall error).
- **WB and IMF are different tenants.** IMF staff reach a WB SharePoint site as guests (and the reverse): the site
  owner shares the folder with their accounts, and the first refresh may need them to sign in with the guest
  identity. Test with one person from each institution before rolling out.
- **How the queries get into the workbook.** The prototype is built with openpyxl, which cannot create queries. The build
  writes the query text into a small table (sheet DataLinks: table, prototype tab, M code), and a macro `SetupDataLinks`
  creates the queries in Excel (`Workbook.Queries.Add`) on first use. The `.xlsx` variants get the queries by hand,
  or not at all.
- **Speed with a single workbook.** Each query downloads the whole file (9 MB dummy; the real one may be larger)
  and Excel does not reliably share one download between queries, so the cost per table is now dominated by the
  download: perhaps 2-5 s per table from SharePoint. With five to eight linked tables, expect 20-40 s. If that is
  too slow, the same script writes a small companion file holding only the linked tables, or one CSV per linked
  table (then each query reads only what it needs). The benchmark (section 6, step 1) should time all three.
- **LibreOffice** has no Power Query; the checks keep running on the embedded Egypt data, so nothing changes there.

#### 7.3 The version selector

On Settings (or Inputs, next to the country): `DataVersion`, a dropdown, with a small table of versions and URLs:

| DataVersion | Source | Who |
|---|---|---|
| Embedded (default) | the Egypt rows shipped in the workbook; no refresh | everyone, out of the box |
| Dummy | `CPAT_Data_dummy_python.xlsx` (repository or a public copy) | everyone; testing, training |
| Real public, dummy proprietary | `CPAT_Data_dummy-proprietary.xlsx` | anyone without the licences |
| Real | `CPAT_Data_real.xlsx` on the restricted SharePoint site | WB/IMF CPAT team only |

`DataUrl` is a lookup of `DataVersion` in this table. The **Load data** button refreshes the linked queries (with
calculation off, then one recalculation) unless the version is Embedded. The cell next to the selector shows the
version and the time of the last refresh, and StoredOutputs records it with every stored scenario run, so a result
says which data it used. The "real public, dummy proprietary" version is assembled by the script from the real
public tables and the dummy proprietary ones (the licence classes decide which is which).

#### 7.4 Out of the box: Egypt embedded

The shipped workbook keeps every data tab as now, with Egypt (the linked tabs filled with Egypt rows only), and
DataVersion = Embedded. It opens and calculates with no network, no sign-in, no Power Query, in Excel or LibreOffice.
The quick check confirms the identity (Egypt embedded = Egypt loaded from a database version that holds the same
Egypt rows; max abs diff 0). Choosing Dummy and loading Egypt gives dummy results, by design.

#### 7.5 Which tables link (proposal)

The biggest and the possibly proprietary L tabs, in two steps:
1. Now available in the data workbook: EnergyCons, Prices_dom, HHSurvey, IO_GTAP.
2. After their `L_` tables are added to the data workbook: WEO, GDPRatios, HH_Elast, GHGs, Balances (real data only
   until a dummy exists), Transport1 and Transport2 (no dummy yet).

The tabs at legacy addresses (Power, ECP, Elasticities, ...) and the small tables stay embedded.

#### 7.6 The dashboard on ScenarioCompare (built in v6.4; additions for v6.5)

Built in v6.4 (`build.py`, `Scenarios_Method.md` section 5), with openpyxl charts, so it also works in
LibreOffice:
- every macro button, top right;
- the year selector (C4) and up to 8 scenario slots besides the baseline (row 6); the slots fill themselves with the
  stored IDs in order, and a typed ID overrides a slot;
- the comparison for the year (levels, differences and % differences vs the baseline);
- eight line charts over every model year (CO2, GHGs, fuel use, carbon price, net revenue, GDP effect, residential
  electricity price, VRE share), baseline dashed, from a chart-data block at the bottom of the tab.

Still to add with the data separation (v6.5):
- the country, the data version and the refresh time in the heading, so a screenshot is self-describing (they come
  with the selector of 7.3 and the version stamp in StoredOutputs);
- a row of headline tiles for the selected year: CO2 emissions (Mt and % vs baseline), revenue (% GDP), GDP effect,
  the average fuel price change, and the burden on the bottom and top deciles;
- a chart of the burden by decile. RunAllScenarios does not store decile results today (StoredOutputs holds the
  LiveOutputs rows only), so the distribution rows must be added to the stored block first.

#### 7.7 Steps for v6.5

1. User: send the SharePoint URL (and the IMF guest test); run the benchmark.
2. Data workbook: `L_` tables for WEO, GDPRatios, HH_Elast, GHGs; the companion file of the linked tables; the
   dummy-proprietary build.
3. prototype: Excel tables on the linked tabs; DataLinks sheet and `SetupDataLinks`; the selector and the Load data button;
   the version stamp in StoredOutputs.
4. ScenarioCompare dashboard additions (7.6): data version and refresh time in the heading, headline tiles, the
   burden by decile (after the decile rows are stored).
5. Checks: embedded = loaded (Egypt), the all-country check on the data workbook, the quick check.

### 8. v6.5 (2026-10-20): the first linked table (Balances) and the plan for the rest (DataLinks)

User request (2026-10-20): connect the big data tables so that CPAT holds one country only; three places for the
data (local, repository, shared drive); the Excel data workbook in every case; a dropdown of sources; one button to
update every linked table; Egypt out of the box; lighter and faster; build fast, with few tests. Second message: an
prototype with one table (Balances), and a plan for the rest.

#### 8.1 Built in v6.5 (prototype, one table)

- **Sheet DataLinks** (after Settings): dropdown `DataSource` (C4) over the source table (rows 10-12: name, kind
  `none` / `file` / `web`, path or URL), the country (= Settings C4), the last update (`DataLastUpdate`), and the
  table of linked tabs `DataLinkTable` (prototype tab, data-workbook table, header cell, columns, status). One row today:
  Balances <- `L_Balances`, header A3, 26 columns (the key column AA stays a formula outside the query table).
- **Sources:** `Embedded (shipped data, no update)` (default: the workbook works as before, no network);
  `Dummy - local file` (blank path = `data/workbooks/CPAT_Data_dummy_python.xlsx` found next to the workbook, one,
  two or three folders up; else a file picker); `Dummy - SharePoint` (the Share link the user gave).
- **Macro `UpdateDataTables`** (button on DataLinks G1 and on ScenarioCompare): writes the Power Query text of each
  linked tab with the path/URL and the country as literals (so no privacy-firewall error and no privacy setting),
  creates query `q_<tab>` and its table at the header cell on first use (the shipped rows are cleared), refreshes,
  writes rows and time to the status column; calculation is manual during the update, then one full recalculation.
  A Share link gets `download=1` appended; if SharePoint still refuses it, paste the direct path (Excel desktop:
  File > Info > Copy path) into DataLinks D12.
- **Macros `CalculationOn` / `CalculationOff`**; button "Calculation on (recalculate)" on ScenarioCompare.
- **Data workbook:** `build_data_workbook.py` adds `L_Balances` (Egypt rows of the prototype's own Balances table, as
  there is no Coded CPAT dummy balance; so a refresh from the dummy workbook gives the shipped results).
  `CPAT_Data_dummy.xlsx` was back in `coded/data/` (43 tables). **Since 2026-10-20 (all data in the root
  `data/`, root `NORMS.md` section 8) it is `data/workbooks/CPAT_Data_dummy_python.xlsx`**; the macro source
  (`CPATScenarios.bas`) searches `data/workbooks/` for that name, but the shipped v6.5 workbook still looks
  for `CPAT_Data_dummy.xlsx` until it is rebuilt: type the full path in DataLinks meanwhile. The SharePoint copy must
  be replaced by this file (keep the SharePoint file name, so the link stays), or the refresh finds no `L_Balances`.
- Not tested: Power Query cannot run on Linux. The build ran and the lint passed; the first refresh is the user's test
  (8.4).

#### 8.2 The tables to link, in order

| Step | prototype tab | Zipped size in v6.4 | Data-workbook table | Work |
|---|---|---|---|---|
| done | Balances | 0.10 MB | `L_Balances` | v6.5 |
| 1 | Prices_dom | 0.40 MB | `L_Prices_dom` (exists) | one `DATA_LINKS` row; header row 3 has the legacy codes; check the build's highlight of changed cells |
| 1 | HHSurvey | 0.10 MB | `L_HHSurvey` (exists) | one row |
| 1 | IO_GTAP | 0.01 MB | `L_IO_GTAP` (exists) | one row |
| 1 | EnergyCons | small | `L_EnergyCons` (exists) | one row (read only when BalancesOrConsumption is not Balances) |
| 2 | WEO | 1.19 MB | `L_WEO` (to add) | all-country public legacy table: the prototype's `data/mvp_legacy_extracts/legacy_WEO.csv` goes into the data workbook as Balances did; the prototype ships the Egypt rows only |
| 2 | Transport1, Transport2 | 0.66 + 0.49 MB | `L_Transport1`, `L_Transport2` | same (from `data/mvp_legacy_extracts/legacy_Transport*.csv`; no dummy needed) |
| 2 | GDPRatios, HH_Elast | 0.41 + 0.36 MB | `L_GDPRatios`, `L_HH_Elast` | same |
| 2 | CH4Inputs, UNPop, NDCs | 0.15 + 0.06 + 0.05 MB | `L_` tables | same; check each key formula column stays right of the query table |
| later | GHGs, Power, Elasticities, ECP, Multipliers | 0.5 + 0.8 + ... | none | these keep the legacy tab at its legacy addresses (several tables per tab), which a query table cannot fill; leave embedded, or give each its own one-table tab first |

Step 1 is four rows in `DATA_LINKS` and the four proprietary tables are then all linked. Step 2 is what makes the
tool light: the all-country tabs shrink to one country (about 3.5 MB less zipped). The "real" data workbook is the
same build pointed at the real CSVs; the proprietary `L_` tables come from the real files.

#### 8.3 Lighter and faster out of the box

1. **Two scenario groups, not three.** Mitigation (5.3 MB zipped) holds group 1 (baseline, plain formulas), group 2
   (policy, plain) and group 3 (a LAMBDA copy of group 2, a test). Make group 2 the policy group with the LAMBDAs and
   drop group 3 and the LambdaTest sheet: about a third of Mitigation (some 1.8 MB) and of the recalculation time.
   Change: `lambda_test_group` writes the LAMBDA calls into group 2 instead of a copy; `LAMBDA_GROUP` and the checks
   that read group 3 follow; the `_noLambdas` variant still expands them. More scenarios remain possible: copy group
   2 to the right (the paste test does this) or run the definitions with RunAllScenarios.
2. **One country in the all-country tabs** (8.2 step 2): about 3.5 MB.
3. **Calculation manual by default:** `wb.calculation.calcMode = 'manual'` with `fullCalcOnLoad` kept, so the file
   calculates once on open and then only on F9 or the "Calculation on" button; the dashboard says so in its heading.
   Risk: users read stale results after an edit; hence the heading note and the button. Excel takes the mode from the
   first workbook opened in the session.
4. Expected: about 12.8 MB -> about 7 MB, and a recalculation about a third faster.

#### 8.4 First test in Excel (user, 5 minutes)

1. Replace the SharePoint file by the new `data/workbooks/CPAT_Data_dummy_python.xlsx` (keep the SharePoint file name).
2. Open `CPAT-AI-Mitigation-Prototype-v7.1.xlsm`, enable macros; ScenarioCompare, Data source = `Dummy - local file`;
   Update data tables. Expect (v7.1, nine linked tabs): the status table at the top of `Cover` lists each tab with its
   rows; Balances 37 Egypt rows (the shipped ones); no error values (`check_links.py`: the nine links on the
   dummy data leave the model without errors; the results change, as the dummy values are fake).
3. Data source = `Dummy - SharePoint`; Update. If asked, sign in with Organizational account. If it fails, paste the
   Copy-path URL into the source table and retry. Note the seconds the message reports (the benchmark of section 6,
   step 1).

#### 8.4b v7.1: the links built (was Balances only)

| prototype tab | Data-workbook table | Header cell | Rows | Built from |
|---|---|---|---|---|
| Balances | L_Balances | A3 | country | `mvp_legacy_extracts/legacy_Balances.csv` |
| EnergyCons | L_EnergyCons | A3 | country | `energy_consumption.csv` (export_to_legacy) |
| Prices_dom | L_Prices_dom | A5 (code row) | country | `prices_dom.csv` (export_to_legacy; 142 legacy columns, the prototype takes its 99 by name) |
| HHSurvey | L_HHSurvey | A3 | country | `distn_hh_survey.csv` |
| IO_GTAP | L_IO_GTAP | A3 | country | `distn_io_gtap.csv` |
| HH_Elast | L_HH_Elast | A3 | country | `distn_hh_elast.csv` (CPAT-format converter) |
| WEO | L_WEO | A3 | all (US CPI, other countries) | `weo.csv` (CPAT-format converter) |
| GDPRatios | L_GDPRatios | A3 | all (regional fallbacks) | `distn_gdp_ratios.csv` (CPAT-format converter) |
| UNPop | L_UNPop | B3 | all | `un_pop.csv` (CPAT-format converter) |

Not linked yet (their prototype layout is not the legacy table of a converter): GHGs, EF_GHG, CH4Inputs, Elasticities,
Prices_int, OilProductShares, Transport1-2. The macro copies through a staging sheet by column name (`RefreshLink`):
a data workbook with the columns in another order, or extra columns, works; an prototype column missing in the table is
reported and left blank.

#### 8.5 The three places, and the real data

| Source row (DataLinks) | Kind | Status |
|---|---|---|
| Dummy - local file | file | built |
| Dummy - SharePoint | web | built (URL to confirm, 8.4) |
| Dummy - repository | web | to add when the repository URL is known: a raw GitHub URL works only for a public repository (a private one needs a token in the query); a local clone is the local-file row |
| Real public, dummy proprietary - local / repository / SharePoint | file / web | when that data workbook exists |
| Real - SharePoint | web | team only; never in the repository |

Adding a source is one row in `DATA_SOURCES` (build) or in the DataLinks table (by hand); the macro needs no change.

#### 8.6 Fast rebuild

The build already reuses its LibreOffice results when the model is unchanged (`.buildcache`), and `QUICK=1` writes
an unchecked `_quick.xlsx` in well under a minute. For this work: run `python build.py` only (no quick check,
no variants, no documents) until step 2 is done; the full checks (quick check, all-country check, embedded =
loaded) once at the end.

## 2. Remaining switches and inputs to append at the bottom of ScenarioDefinition: plan (built in v5.6, except the scenario rows) (MTInputs_Appendix_Plan)

**Status (v5.6):** blocks A (road parameters from TransportParams), B (TransmissionCostShare, read in the levelised cost), C (Settings C10, C14, C15, C19, C34, C40, C45, C54, C66) and D (Constants: pass-through buckets, price floor, EF end year, methane cap, road lags, power constants) are global rows at the bottom of ScenarioDefinition; the old cells read them. Duplicates of 2a now reading the template row: C33 SCCTargetConsistentCP, C35 SCCRise. Also built: C27 (reads EFsAdjustmentAnnexI, as legacy E7534 for every country), C36-C39 (legacy texts; the SCC selector and the Ricke keys read them), the scenario rows of 2c (CTaxCoversBiomass, ConsSubPhaseScope_*, PriceCtrlPhaseScope_*, ProdSubPhaseScope_*, per scenario after the power rows). Kept global by design: C21 (SpotPow, a global override), 2d (GovPriceControls, BiomassNormal, the trade-balance price source feed the shared parameter columns of the Inputs sheets). Not built: the vehicle-purchase rows (road model parked, I61).

User request (2026-10-18): "Any remaining switches and inputs might need to be appended to ScenarioDefinition at the bottom. Specifically distinguish between things that come directly from dashboard in legacy (they shouldn't!) in Transport engineer model and b) elsewhere; and secondly other switches and settings that you've added in. ... plan this out, but do not do it."

This is a plan. Nothing here is built yet. The inventory behind it (legacy cells, verbatim formulas, Dashboard addresses, prototype locations) was a read-only survey of legacy 456 and `build.py`, kept in the session notes. The rule it serves is NORMS 4: ScenarioDefinition is the input sheet, one column per scenario, as in legacy. 'Manual inputs' is the second source, for the blocks legacy keeps there (see the Manual inputs release).

### 0. Where ScenarioDefinition stands (v5.1)

- **Template rows 1-415:** the legacy layout, columns B:H.
- **Scenario columns from J:** J = scenario 1, K = the live scenario 2, L onward = definitions 3-6. Rows 4-6 hold Run?, the scenario number and the name.
- **Rows 417-479, appended in v3.5:** the 62 policy inputs of the road engineer model (TR_MT), per scenario.
- **How rows are read:** by name through Mapping (MT_KEYS) in the scenario's own column, or by `mt_setting(name)`, which reads only scenario 1, making the row global in effect.

### 1. Inputs legacy takes straight from the Dashboard

#### 1a. Road engineer model (legacy Mitigation rows 4300-5440, 2168-2169, 7935)

| Group | Legacy | prototype now | Plan |
|---|---|---|---|
| **Policies**: feebates, distance tax, EV subsidy, VAT, customs and ad-valorem changes, charging subsidy | Rows 4304-4319 copy Dashboard G63:Q98 cell by cell | ScenarioDefinition 418-479 per scenario (v3.5) | **Done.** Nothing to append. Keep the "Dashboard bypass" note in Transport_Method |
| **Model switch** TrModel | Dashboard G61 → ScenarioDefinition E340 | ScenarioDefinition 340 per scenario | **Done** |
| **Baseline VAT, customs duties, import shares** | Dashboard G78:Q87, themselves formulas on country data | Data (Prices_dom VAT_WEO, Transport1) | Keep as data. They are not inputs, so nothing to append |
| **Advanced parameters**: ownership, life, depreciation, insurance, maintenance, charging-station elasticities and costs, ownership coefficients and limits, VKT bounds, income elasticities of driving, new vs average efficiency, k-parameters, discount rates and thresholds, freight and 2-3 wheeler ownership targets (about 40 values) | Dashboard G542:V557, L551:L556, Q552:Q555, V551:V554 | Sheet TransportParams (global) | **Append as global rows** (block "Road engineer model: parameters", one row per TransportParams key; column F = default; read from column J like `mt_setting`). TransportParams then reads ScenarioDefinition. Values unchanged |
| **Options**: new-purchase VKT responds to prices (Q551), reconcile electricity with the energy balance (Q556), range-anxiety source (L61) with the Dashboard anxiety values and declines (G548:Q549) | Dashboard | TransportParams `vkt_new_price`, `recon_ele`, `ra_source`, `ra_dash|*`, `ra_decline|*`. ra_source and ra_dash are stored but **not read**: the prototype always uses Transport3 | **Append as global rows.** Build the "Dashboard" range-anxiety option at the same time, as legacy N4354:N4356. This is a legacy feature, so it is replicated, not an extension |
| **Vehicle purchases, actual data** (L557:L559) | Dashboard, legacy fiscal rows 7930-7935 | Stored, unused (rows not replicated) | Append as global rows **only when** the vehicle-purchase fiscal rows are built. Until then, list them in NotReplicated |

#### 1b. Elsewhere in legacy Mitigation

Direct `Dashboard!` references outside the road block are labels only: C2193:C2196, D16144:D16148 and D16169:D16171. Nothing to append. The real bypasses go through defined names:

| Name → Dashboard | Legacy use | prototype now | Plan |
|---|---|---|---|
| `D_WACCSource` → Q191 | WACC source of the power plants (X2988:X2996) | ScenarioDefinition 365 WACCSource, read from scenario 1 (Inputs_pset) | Already on ScenarioDefinition. P2 of the power plan makes it per scenario |
| `IncludeTransmissionCostsInGenerationCostsPercent` → Q197 | Share of transmission cost in levelised cost (rows 3326-3334, 3522-3530), 100% | Not an input: always fully included | **Append a global row** TransmissionCostShare (default 1) and read it in the levelised-cost rows. Egypt is unchanged at the default |
| `D_CPLevelTarget` → I6 | Chart scale only (C2730) | ScenarioDefinition 20 | Nothing |
| `ETSOnDash` → D30 | ETS price shown in results (L16141) | `ets.p` per scenario, switch ScenarioDefinition 84 | Nothing |
| `ScenarioNum` → D647; `_Country_code`, `_region` → D644, C644:C645 | Scenario number and country keys | Mitigation row 5 per group; Settings C4, C43 | Structural, not inputs. Nothing |
| ScenarioDefinition column E (240 cells `=Dashboard!…`) → F | The legacy route of every other input | Typed values in the scenario columns | Nothing: this is how the prototype already works |

### 2. Switches and settings the prototype added, and ScenarioDefinition rows read only for scenario 1

#### 2a. Duplicates: Settings cells that repeat an existing ScenarioDefinition row

Settings should read these rows, not hold its own value. For each, set the Settings cell to `mt_setting(<name>)` and convert the legacy coding where it differs (starred defaults, % strings):

| Settings | ScenarioDefinition row | Note |
|---|---|---|
| C21 SpotPow | 368 UseSpotFuelPricesInEngineerModel (No*) | |
| C27 CO2 calibration | 237/238 EFsAdjustmentAnnexI / NonAnnexI (Yes*) | Pick the row by the country's Annex I status |
| C33 SCCTgt, C35 SCCGr | 278 SCCTargetConsistentCP (75), 277 SCCRise (0.04) | |
| C36/C37 SCC sources | 269 NSCCSource, 275 GSCCSource (Target*) | |
| C38/C39 Ricke parameters | 273 NSCCDiscountRate (2%*), 274 NSCCMargUtilofCons (1.5%*) | Map the strings to the Ricke keys |

#### 2b. New prototype switches with no legacy row: append as global rows (block "CPAT-AI settings")

Each becomes a row with a name, a default in F and the value in J, read by `mt_setting`. Settings keeps a formula that reads it, so the defined names stay.

| Now | Content | Default |
|---|---|---|
| Settings C10 LastHist | Last historical price year | 2022 |
| Settings C14 OBREff | ETS relative effectiveness of output-based allocation (legacy hardcoded) | 0.5 |
| Settings C15 | ETS convergence exponent of the next-price proposal (legacy row 1966) | 0.5 |
| Settings C19 | Apply the 2023-2024 demand shock (always on in legacy, I22) | 1 |
| Settings C34 SCCTgtYr | Year of the target-consistent carbon price | 2030 |
| Settings C40 SCCEpa | US EPA SCC in the base year (legacy row 17684) | 62 |
| Settings C54 PavMethod | Average price change reported: Legacy* / Laspeyres (I31) | Legacy* |
| Settings C59 onward (v5.1) | Residential leakage settings | as built in v5.1 |

Settings B56:C58 (the multiplier-source mapping) is a lookup table, not an input. It stays on Settings.

#### 2c. Constants that are really choices

These are on Constants now. They become global ScenarioDefinition rows, or move to 'Manual inputs' at the legacy address where legacy keeps them there:

| Constant | Plan |
|---|---|
| PassManual 0.8 | 'Manual inputs' G167:J180, per fuel and sector, as legacy (done in v5.2, the Manual inputs release) |
| PassLo / PassMid / PassHi, PriceFloor | Global rows (legacy hardcoded) |
| ctcov\|bio\|all (carbon tax covers biomass) | Scenario row: it is a policy design |
| csi / pci (12 price blocks), psi (5 fuels) | **Scenario rows**: they are the scope of a phase-out (v4.16). Legacy has only the electricity exemption, ScenarioDefinition 138, which should feed csi/pci of electricity |
| gp.hi / gp.lo factors, EFEndYear, MethShareCap | Global rows (ghg.el moved to 'Manual inputs' K326:M327 in v5.2) |
| TrOwnDecline, TrRALag, TrPivotLag | Global rows in the road parameter block (1a) |
| EarlyMaxShare, InvPresentShare, HydInvShare, WaccDefault | Global rows in a power block (with P2 of the power plan) |
| ETS goal seek ETS_TOL, ETS_MAXITER (VBA and Python constants) | 'Manual inputs' E10:E12, as legacy; the macro reads the cells (done in v5.2) |

#### 2d. ScenarioDefinition rows read only for scenario 1

These become per scenario, read in each scenario's own column through Mapping (Section-1 rows), so a definition can change them:

- `mt_setting` rows: ResultsYear 233, GovPriceControls 194, BalancesOrConsumption 234, BiomassNormal 326, IntEnerPricForeSource 220 (trade balance).
  - ResultsYear and BalancesOrConsumption are structural: keep them global and say so on ScenarioDefinition (a note in column H).
- Inputs_pset: 28 power settings, and Inputs_power NewInv<type> / NewInv<type>Year (397-415). This is **P2 of the power plan** (decision 2: every power input on ScenarioDefinition is read per scenario).

### 3. Layout of the appendix

From row 481, below the road policy rows, each block gets a heading row (as row 417), then one row per input. The columns follow the template:
- B: name (NameOfParameter);
- C: label;
- D: unit;
- F: default;
- G: legacy source (Dashboard cell, Manual inputs cell or "prototype");
- H: "global" or "scenario".

Values go in the scenario columns. Global rows are read from column J only, and their other columns repeat J by formula, so that a copied definition column cannot silently differ.

| Block | Rows (about) | Content |
|---|---|---|
| A. Road engineer model: parameters and options | 40 + 6 | 1a advanced parameters and options |
| B. Power: model choices | 1 + 4 | Transmission share (1b); power constants (2c) |
| C. CPAT-AI settings | 8 | 2b |
| D. Choices from Constants | about 25 | 2c (except what moves to 'Manual inputs') |

### 4. Order and checks

1. Release after the Manual inputs release, so what moves to 'Manual inputs' is not appended twice.
2. One commit per block: A, then B with power P2, then C and D.
   - Each block is built from a list in the builder (as TR_MT): the name, label, unit, default, source and scope.
   - The reading formulas switch from TransportParams, Settings or Constants to ScenarioDefinition, with the old location kept as a formula that reads ScenarioDefinition. Defined names and LAMBDAs then stay.
3. Checks:
   - The quick check shows 0 change of output codes for every block, since only the defaults move.
   - The paste test passes.
   - The full check reads the same values.
   - A test scenario changes one appended input of each block in a definition column and sees the effect only in that scenario (scenario rows) or in all (global rows).
4. Docs:
   - QuickStart and DataTabs (where each input lives);
   - Transport_Method (the Dashboard bypass is gone);
   - the register (I-code for any legacy option built: the range-anxiety source);
   - LegacyDiff (the inputs moved).

### 5. Open points for the user

- Should the global rows (blocks A, C, D) really sit on ScenarioDefinition, or should only the per-scenario choices go there with the model parameters kept on their data tabs? The request says "might need to be appended"; this plan appends all of them and marks the scope.
- The vehicle-purchase fiscal rows (L557:L559 and legacy 7930-7935): build them, or list them as not replicated.

## 3. Power engineer model: features to add (plan, 2026-10-18; decisions recorded) (PowerFeatures_Plan)

**Status (v5.6, 2026-10-19): P1-P5 done** (P3 manual capacity and investment, P5 coal implicit cost and memo rows in v5.6; the optional GoalSeekCoal calibration script is not built: the stored legacy values are used). Earlier status: **(v5.4) P1, P2 and P4 done.** Item 1 in v4.14; items 3, 4 (P1), 2 (P2) and 5, 6, 7, 12 (P4) in v5.4 (`PowerModel_Method.md`, `PowerPrices_Method.md`). Open: P3 item 8 (manual capacity and investment) and P5 (items 10, 13), planned for v5.5. Dropped: items 11 and 14.

User request (2026-10-18): plan the features of the power engineer model that the prototype does not have yet. This is a plan, not a method note; each release gets its method text in `PowerModel_Method` / `PowerPrices_Method` when it is built.

Source: survey of the legacy power block (Mitigation rows 2731-4301 baseline, +6331 for the policy run; ScenarioDefinition rows from the template; 'Manual inputs'), checked against `build.py`. Every feature below is **off or zero for Egypt**, except items 1 and 2 (which change Egypt's results) and possibly item 9 (data). So most releases leave Egypt's numbers unchanged until a user sets an input; each needs a test scenario that switches it on.

Classification follows NORMS 0: a legacy feature is replicated (bugs fixed); a legacy bug is fixed and registered; anything that extends legacy needs your decision. Under the input rule (NORMS 4) the inputs come from ScenarioDefinition; the few that legacy keeps elsewhere ('Manual inputs', typed cells) go to Settings or a data tab.

### 1. The features

| # | Feature | Legacy (rows; inputs) | What the prototype lacks | Class | Egypt | Size |
|---|---|---|---|---|---|---|
| 1 | **Capacity for next year's demand** (I8, U9) | Investment need (rows 4022-4031) uses "Next Year Demand" (row 4027), but its formula is this year's demand (M3752). Row 4031 "should be the same" compares with next year's capacity. | `need` uses this year's demand, as legacy | **Legacy bug** (label and check row show the intent): fix, keep a switch for the legacy comparison. No circularity: next year's demand depends on this year's price. | Changes results: more new capacity a year earlier, less gas dispatch | Tiny |
| 2 | **Policy power inputs per scenario** (done v5.4) | Legacy runs each ScenarioDefinition column with its own baseline and policy run, so every power input can differ by scenario. | Inputs_pset reads every power setting from scenario 1, so a scenario that changes e.g. NewInvCoal ("no new coal"), early retirement or AdditionalEfficiencyPower has no effect | Departure from legacy (not a bug): replicate for the **policy-like** inputs; keep the **technical** ones (logit constants, WACC, CF bounds, storage, cost decline) global on scenario 1 and say so | None (shipped scenarios use the defaults) | Medium (plumbing) |
| 3 | **Final deficit to gas** (done v5.4) | Typed switch E4248 = No: the deficit left after the second investment round goes to gas (row 4252) | Not built | Legacy feature (input outside ScenarioDefinition: Settings, as legacy's typed cell) | None (off) | Tiny |
| 4 | **Two ignored inputs** (done v5.4) | MaximumGasCF (ScenarioDefinition 373) caps gas (row 3784); LongTermStorageFor100pcVRE (394) scales the long-term storage term (row 3909) | Gas uses the coal cap (MaximumCoalCF); the storage factor is implicitly 1 | Departures (same values at the defaults): wire both | None at the defaults | Tiny |
| 5 | **PPAs** (coal and gas; done v5.4) | Share (ScenarioDefinition 382) x phase-out factor (383 baseline / 384 policy, start 385, years 386; row 2218): that share runs at its historical capacity factor whatever its cost (rows 3801-3805) and cannot retire early (3987, 3993) | Not built | Legacy feature. Legacy oddities: share to phase out typed as 1 (Q2193); the switch fires only on the exact text "Yes*" (treat as an issue: replicate with "Yes" or "Yes*") | None (share 0) | Small |
| 6 | **Renewable subsidies** (done v5.4) | rns = base subsidy (354) + additional subsidy (355, policy only) phasing out over 356 years; hydro if 357 = Yes; enters levelised cost and revenue (rows 3142-3152, 3303-3313, 3665-3669) | Slot exists (rns = 0) | Legacy feature. Legacy bug: the start year reuses the consumer-subsidy phase-out year (ScenarioDefinition 132). Oddity: "nominal" input used as real | None (0) | Small |
| 7 | **Power revenue rebate** (PowerRebates, 342; done v5.4) | Carbon cost removed from end-user prices (rows 3595, 3615, 3644), revenue memo 3663 | Rebate fixed at 0 in `rp` | Legacy feature | None (off) | Small |
| 8 | **Manual capacity and investment** | NewInv<type> = "Manual" (397-405) and a capacity path per scenario ('Manual inputs' 342-371): investment = path increase + retirement (rows 4097-4105); all-manual mode (4287-4296) | Not built | Legacy feature. Legacy bug: the need net of manual investment (row 4108) is never used, so logit investment comes on top (over-investment). Unclear: one-year lag in the all-manual mode | None (no Manual type), but **the only way to enter El Dabaa nuclear** (no nuclear in the base year, so NewInvNuc "If Present*" blocks it) | Medium (rows + data table) |
| 9 | **Planned retirement data** (U13) | Coal only, Global Coal Plant Tracker (Power rows 1636-1878); Egypt: no data | The mechanism exists for every type; Egypt has no data | Data task | Changes results once data are entered | Small (data) |
| 10 | **Coal implicit cost** (D3) | Short- to long-term value by 2030 (rows 3361-3371), calibrated per country (tab GoalSeekCoal, 85 countries, not Egypt); No / Manual options (369-371) | Not built | Legacy feature. Issues: it also raises generation costs and tariffs (a calibration wedge treated as a cash cost); the gas implicit cost points at an empty cell. The lookups are stripped in the NoPropData file: data needed | None (no coal) | Small-medium + data + optional calibration script |
| 11 | **Feebate on power demand** | Row 3683 should feed a carbon price into the efficiency term of demand, but points at a blank row (L$2255): always 0 | Not built | Legacy bug with no working reference: needs a design decision | None | Small |
| 12 | **Electricity excise** (done v5.4) | Policy type 11 (row 2253: grid intensity x carbon price) and the manual electricity excise ('Manual inputs' 161-162) | Not built | Legacy feature | None | Small |
| 13 | **Memo tables** | F1-F7 (system cost, fuel prices per kWh, carbon intensity, switching carbon prices gas over coal), cost breakdown (344) | Not built | Reporting only | None | Small |
| 14 | **Elasticity-based power model** (legacy section 3) | A reduced-form model (about 220 rows a run), chosen by PowModelSelected (227: Engineer / Elasticity / Average); its demand can feed the engineer model (364) | Not built (engineer only) | Legacy feature, large. Legacy oddity: in "New" cost mode thermal plants carry only fuel and carbon costs | None (Egypt runs Engineer) | Large |

### 2. Decisions (user, 2026-10-18)

| # | Question | Decision |
|---|---|---|
| 1 | Item 1, capacity sized for this year's demand | **A legacy bug**: fix it (I8 becomes a legacy bug in the register when P1 is built), with a switch that reproduces legacy |
| 2 | Which power inputs per scenario | **Every power input on ScenarioDefinition** is read per scenario (technical ones too) |
| 3 | Manual capacity and investment, El Dabaa and announced plans | **The functionality is needed; no Egypt data to add.** Capacity plans come from 'Manual inputs': time to bring in the legacy 'Manual inputs' tab, the second input source after ScenarioDefinition |
| 4 | Item 11, demand-side power feebate | **Not built**: CPAT already has the functionality through the rebating of power prices (item 7) |
| 5 | Item 14, elasticity power model | **Not built** |
| 6 | Item 10, coal implicit cost in tariffs | **A switch, default as legacy** (the implicit cost enters generation costs and tariffs) |
| 7 | P3, capacity blocks | **One capacity block per prototype scenario** (an extension of legacy's two blocks, baseline and policy; user 2026-10-18) |
| 8 | P2, scope | **As legacy**: each scenario's ScenarioDefinition column holds everything a scenario changes; technical inputs are not usually changed across scenarios (user 2026-10-18) |

Not now (user 2026-10-18): the plan is defined, nothing is built yet. Built since: P1, P2, P4 in v5.4 (2026-10-19).

### 3. Releases

| Release | Content | Changes Egypt? |
|---|---|---|
| **P1: corrections** (done: item 1 v4.14, items 3 and 4 v5.4) | Item 1 **done in v4.14** (legacy bug L67; legacy kept as a switch in the Python reference only, NORMS 0) (and the capacity check of bug L10); item 3 (final deficit to gas, switch on Settings as legacy's typed cell E4248); item 4 (MaximumGasCF, LongTermStorageFor100pcVRE wired) | Yes (item 1) |
| **P2: power inputs per scenario** (done v5.4) | Every ScenarioDefinition power input read in the scenario's own column (section 1 / section 3 rows by scenario instead of Inputs_pset and Inputs_ptech scenario 1), e.g. NewInv<type> and their years (397-415), early retirement (378-379), pass-through (343), AdditionalEfficiencyPower (242), scale-up limits (359-362), logit constants, WACC, CF bounds, storage | No (shipped scenarios use the defaults) |
| **P3: the Manual inputs tab** (done in v5.2: the whole tab placed; the manual capacity block 342-371 is read when item 8 is built) | The legacy 'Manual inputs' tab in the INPUTS group at its legacy addresses (paste-compatible, as the data tabs, NORMS 1.5), read by the model where legacy reads it; the items the prototype already takes from legacy 'Manual inputs' move onto it (methane fee switches J196-J200, now Settings rows 47-51; ETS price override O15:AB15; BEV fuel economy paths 375-377, now TransportPaths). Then item 8: manual capacity and investment (NewInv<type> = Manual; capacity paths rows 342-371; legacy bug 4108 fixed: logit investment sized on the need net of manual investment; the all-manual lag decided when built). One capacity block per scenario (decision 7; legacy has a baseline and a policy block). No Egypt data | No (no data) |
| **P4: power policies** (done v5.4) | Item 5 (PPAs, baseline / policy phase-out by scenario); item 6 (renewable subsidies, own start year: legacy bug fixed); item 7 (power revenue rebate, PowerRebates, which also covers the demand-side feebate); item 12 (electricity excise: policy type and 'Manual inputs' 161-162, after P3) | No |
| **P5: coal implicit cost and memos** | Item 10 with the switch, default as legacy (enters tariffs); GoalSeekCoal data from the full legacy file; optional calibration script. Item 13 memo tables (F1-F7, cost breakdown) | No |

Dropped: item 11 (covered by item 7), item 14 (elasticity model). Item 9 (planned retirement data): the mechanism exists for every type; no Egypt data to add.

Each release: Python reference (`power_model_ref`) first, a test scenario that switches the feature on, quick check, paste test, register and LegacyDiff rows 28 and 34.

### 4. Points to settle when building

- P2: the prototype has one baseline (scenario 1) for every scenario, while legacy runs each ScenarioDefinition column with its own baseline. A technical input changed in a policy scenario therefore changes that scenario only, and its difference to scenario 1 mixes the input change with the policy. Technical inputs are not usually changed across scenarios (decision 8); said so on Inputs_pset (v5.4).

How v5.4 settled the points of the build:
- P2: the settings are section-1 rows (ScenarioDefinition, the scenario's column; sub-heading "Power sector settings"); section 3 sub-table A0 applies them to the power data of Inputs (capacity factor, efficiency, WACC, discounted lifetime, base-year capacity, permits and start years, scale-up and retirement rates, storage, PPA, subsidy, rebate and excise switches). The power data tables on Inputs keep scenario 1's values for reference. Not read (no prototype feature): CostBreakdownYear (344, P5 memo), ElasticityModel (345, dead), PowGenCostsOldNew (349) and UseElasticityModelPowerDemandInEngineerModel (364, elasticity model dropped), SupplyCostDeltaSubsidy (353, telescoped price S4), coal implicit cost (369-371, P5).
- P4 item 6: the start year of the additional subsidy is a new ScenarioDefinition row after the template (RenSubsidyAddStartYear, row 482, default 2027; legacy bug L107). The revenue counts the base subsidy once (legacy bug L108).
- P4 item 7: the rebate removes the carbon cost passed through (and its VAT) from end-user prices in policy scenarios with PowerRebates = Yes or a feebate scenario of the legacy scenario table; the government returns the carbon cost to consumers (row rreb; legacy bug L110: legacy's memo includes VAT never counted).
- P4 item 12: the electricity excise of the scenario Electricity excise (grid CO2 intensity of the base year x carbon price, issue I56) and the manual electricity excise of Manual inputs rows 161-162 (AdditionalExcise = Yes, policy scenarios; enters the price like the supply cost, relative to the last historical year, with pass-through; revenue = the excise in the price: legacy bug L111).
- Switches that legacy tests for the exact "Yes" or "Yes*" accept both (LEFT 3): PPA phase-out (issue I54), PowerRebates, RenewableSubsidyHydro, AdditionalExcise (issue I58).
- The capex decline options Low and Vhigh have no wind and solar series in the Power tab: the older series of the same option is used (legacy bug L109).
- P3: the Manual inputs tab is the second input source (NORMS 4); policy inputs there should come from legacy, not extend it.

### 5. Uncertain (from the survey)

- The one-year lag in legacy's all-manual mode (row 4288).
- Why the GoalSeekCoal lookups are empty in the NoPropData file.

## 4. CPAT policy taxonomy, extended to cover every FTT policy (plan, 2026-10-20; decisions open) (PolicyTaxonomy_Plan)

Proposal for one policy taxonomy that serves both CPAT projects (ScenarioDefinition, the prototype scenario definitions and `coded/cpat_model/constants.py`). It keeps every policy CPAT has today and adds every policy instrument in the FTT (Future Technology Transformations) models, so that a policy in either model has a slot in the taxonomy.

Sources:
- CPAT: `templates/MTInputs_template.xlsx` (legacy MTInputs rows), the prototype road and power rows (`Transport_Method.md` section 2, `Plans.md` (section PowerFeatures_Plan)), the main-scenario list (`Scenarios_Method.md` section 2b; `constants.py` `ALL_SCENARIOS`).
- FTT: the open-source stand-alone FTT, `github.com/cpmodel/FTT_StandAlone` at commit 8cf4bfd (2026-10-13): `Utilities/titles/VariableListing.csv`, `ftt_source/ftt_core/` (mandates, emissions regulation, exogenous sales and capacity), `ftt_source/Power/ftt_p_phase_out.py` and the LCOE/LCOT/LCOH cost functions where each policy enters. Modules: FTT:Power (P), FTT:Transport, passenger road (Tr), FTT:Freight (Fr), FTT:Heat, residential (H), FTT:Industrial Heat (IH: chemicals CHI, food-beverages-tobacco FBT, machinery and transport equipment MTM, non-metallic minerals NMM, other industry OIS).

### 1. Structure

Three levels:

1. **Family** (what kind of instrument): 10 families, section 2.
2. **Instrument** (one policy lever, with its own inputs): code `<family>.<instrument>`, section 3.
3. **Application**: sector coverage, fuel or technology coverage, and timing (start year, target year, start and target level, continuation). These stay as the ScenarioDefinition coverage switches and paths CPAT already has; they are not separate instruments.

Each instrument also carries a **representation** tag, because CPAT and FTT model policies differently. FTT chooses between technologies (shares equation on levelised costs, with regulations, mandates and exogenous changes acting on capacity or sales); CPAT models fuel demand with elasticities, with technology choice only in the engineer power model (and the dropped engineer road model).

| Tag | Meaning in CPAT |
|---|---|
| **D** direct | Changes a price, tax or quantity CPAT computes (retail price, power LCOE, power capacity) |
| **S** shadow price | Converted into an implicit carbon price on the efficiency margin (`reg.<sector>`, ScenarioDefinition rows 247-251), as CPAT does for its regulation scenarios |
| **X** exogenous path | An exogenous efficiency gain, demand path or capacity path (ScenarioDefinition rows 241-245, power manual capacity) |
| **N** needs a technology module | Cannot be represented faithfully without technology shares in that sector; at most S or X as an approximation |

### 2. Families

| Code | Family | Covers |
|---|---|---|
| PRC | Carbon and emissions pricing | Carbon tax, ETS, methane fee, existing carbon pricing |
| FTX | Energy taxes and price reform | Fuel excises, fuel price reform, electricity excise, VAT on energy, existing non-carbon taxes, Pigouvian tax |
| FFS | Fossil-fuel subsidy and price-control reform | Producer and consumer subsidy phase-out, price liberalisation, tax-exemption phase-out |
| TEC | Technology purchase and ownership taxes and subsidies | Upfront subsidies, purchase and registration taxes, annual ownership taxes, feebates on technology |
| OUT | Output and production support | Feed-in tariffs, per-kWh renewable subsidies, power revenue rebates |
| STD | Performance standards and regulations | Efficiency regulations, fleet CO2 standards, technology caps and bans |
| MAN | Quantity mandates and deployment | Sales mandates (ZEV, heat pumps), kick-starters, blending mandates, exogenous capacity and sales |
| PHO | Phase-outs of existing assets and contracts | Coal phase-out, PPA phase-out, investment-permission dates |
| BRD | Border measures | CBAM coverage |
| REV | Revenue use | Labour and corporate tax cuts, public investment, current spending, targeted transfers, rebates |

### 3. Instruments

Status: **C** in CPAT now; **C+F** in both; **F** FTT only (new for CPAT). "CPAT sector" names the CPAT sector the FTT module maps to.

#### PRC: carbon and emissions pricing

| Code | Instrument | Status | CPAT now (ScenarioDefinition) | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| PRC.CTAX | Carbon tax, by sector and fuel | C+F | rows 18-47 | `CO2taxP`, `CO2taxTr`, `CO2taxFr`, `CO2taxH` (USD 2023/tCO2, region x year; added to LCOE/LCOT/LCOH as emissions x price) | P, Tr, Fr, H | D | All |
| PRC.ETS | New ETS (cap, auctioning, benchmarks) | C | rows 83-115 | (FTT takes a permit price only, via the sector carbon price) | | D | Covered sectors |
| PRC.EXIST | Existing carbon tax and ETS | C | rows 208-214 | | | D | All |
| PRC.CH4 | Methane fee | C | rows 184-189 | | | D | Fossil-fuel supply, non-energy |
| PRC.TCP | Total carbon price measure | C | `TCP` scenario | | | D | All |

FTT has no carbon price variable for industrial heat; the IH modules price carbon through their fuel tax (FTX.FUEL below).

#### FTX: energy taxes and price reform

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| FTX.FUEL | Fuel excise by fuel and sector | C+F | Fuel price reform rows 139-183; `Coal excise`, `Road fuel tax` scenarios | `MTFT` (P, by technology, multiplies fuel cost), `RTFT` (Tr, cents/litre), `RZFT` (Fr, $/MJ), `HTRT` (H, % of fuel cost, also a subsidy if negative), `IFT1`-`IFT5` (IH, 2010 EUR/MWh) | P, Tr, Fr, H, IH | D | Power, road, residential, industry subsectors |
| FTX.ELEC | Electricity excise and electricity emissions tax | C | `Electricity excise`, `Electricity emissions tax` scenarios; Manual inputs 161-162 | | | D | Power |
| FTX.VAT | VAT reform on energy | C | row 284 | | | D | Residential, transport |
| FTX.EXIST | Existing non-carbon taxes | C | rows 286-294 | | | D | All |
| FTX.PIGOU | Pigouvian (externality) tax | C | rows 212, 216-218 | | | D | All |
| FTX.DIST | Distance tax | C | road rows 418-479 | | | D (road model) | Road |

#### FFS: fossil-fuel subsidy and price-control reform

| Code | Instrument | Status | CPAT now | FTT | Rep. |
|---|---|---|---|---|---|
| FFS.PROD | Producer subsidy phase-out | C | rows 122-129 | | D |
| FFS.CONS | Consumer subsidy phase-out | C | rows 130-138 | (a negative `HTRT` is a fuel subsidy in heat) | D |
| FFS.PCTRL | Price-control phase-out (liberalisation) | C | rows 190-195 | | D |
| FFS.EXEMPT | Carbon-tax exemption phase-out | C | rows 48-51 | | D |

#### TEC: technology purchase and ownership taxes and subsidies

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| TEC.UPSUB | Upfront capital subsidy (% of investment cost) by technology | F (C for EVs) | EV purchase subsidy, road rows | `MEWT` (P), `HTVS` (H), `ISB1`-`ISB5` (IH) | P, H, IH | D in power (capital cost of the engineer model); N elsewhere (S as approximation) | Power, residential, industry |
| TEC.PURTAX | Purchase tax or subsidy per vehicle, by technology | C+F | ad-valorem purchase taxes, VAT and customs on BEVs (road rows) | `TTVT` (Tr, th $/veh), `ZTVT` (Fr, $) | Tr, Fr | N (road model dropped) | Road |
| TEC.REGTAX | CO2-differentiated registration tax | F | | `RTCO` (Tr, $/gCO2/km) with `Base registration rate` (share of price, by technology); `RZCO` (Fr) | Tr, Fr | N; S as approximation | Road |
| TEC.ANNTAX | Annual road (circulation) tax by technology | F | | `TTRT` (Tr, $/y), `ZTRT` (Fr, $/vehicle-y) | Tr, Fr | N; S as approximation | Road |
| TEC.FEEBATE | Feebate on emission intensity, by sector or vehicle class | C | rows 52-82 (power, transport, residential, industry); road feebates by class; `Feebates`, `Power feebate` scenarios | (FTT: a registration tax with a negative base rate for clean technologies acts as a feebate) | | S (D in power) | Power, road, residential, industry |
| TEC.INFRA | Charging-infrastructure subsidy | C | road rows | | | N | Road |

#### OUT: output and production support

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. |
|---|---|---|---|---|---|---|
| OUT.FIT | Feed-in tariff / per-unit output subsidy by technology | C+F | Renewable subsidy $/kWh, rows 352-357 (all renewables, optional hydro) | `MEFI` (P, USD/MWh, subtracted from LCOE, by technology), `HEFI` (H, renewable-heat tariff) | P, H | D in power; N in residential |
| OUT.REBATE | Power revenue rebate | C | row 342 (PowerRebates) | | | D |

#### STD: performance standards and regulations

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| STD.EEREG | Energy-efficiency regulation by sector | C | `Energy efficiency regulations`, `Residential ...`, `Industrial efficiency regulations` scenarios; rows 241-251 | | | S / X | Residential, industry, services |
| STD.FUELECON | Vehicle fuel-economy standard | C | `Vehicle fuel economy` scenario; row 248 | | | S | Road |
| STD.FLEETCO2 | Fleet-average CO2 standard on new sales (`[start, end, max reduction]`, linear to the target; sales move from high- to low-emitting technologies) | F | | `EV CO2 regulation` (Tr), `EV truck CO2 regulation` (Fr); exclusive with MAN.SALES in the same sector | Tr, Fr | N; S as approximation (the fuel-economy shadow price is the nearest CPAT slot) | Road |
| STD.TECHCAP | Technology capacity cap or ban on new capacity (cap in GW or share; -1 = no new capacity) | F (part C) | Power: investment-permission dates and new-investment overrides, rows 396-415 | `MEWR` (P, GW), `TREG` (Tr, share), `HREG` (H), `ZREG` (Fr), `IRG1`-`IRG5` (IH, GW) | P, Tr, Fr, H, IH | D in power (extends rows 396-415 from on/off by date to a cap path); N elsewhere | Power, road, residential, industry |

#### MAN: quantity mandates and deployment

| Code | Instrument | Status | CPAT now | FTT | FTT sectors | Rep. | CPAT sector |
|---|---|---|---|---|---|---|---|
| MAN.SALES | Sales mandate for clean technologies (`[start, end, max share]`, linear from 0 to the max share of new sales) | F | | `EV mandate` (Tr), `EV truck mandate` (Fr), `HP mandate` (H) | Tr, Fr, H | N; X as approximation (fuel switch path) | Road, residential |
| MAN.KICK | Kick-starter (a sales mandate with a low max share, early years only) | F | | `EV truck kickstarter` (Fr); seeding of clean technologies in low-adoption regions is built into Tr, Fr and H (not a policy input) | Fr | N | Road |
| MAN.BLEND | Fuel blending mandate | F | | `RBFM` (Tr, biofuel %), `ZBFM` (Fr, biofuel %), `RHSM` (hydrogen share in freight) | Tr, Fr | D (changes the fuel mix and emission factor of road fuels; needs biofuel and hydrogen prices) | Road |
| MAN.EXOCAP | Exogenous capacity target by technology | C+F | Power manual capacity and investment (Manual inputs 342-371, P3) | `MWKA` (P, GW) | P | D / X | Power |
| MAN.EXOSALES | Exogenous sales or share shift by technology (sums to zero; capped at 80% of replacement sales) | F | | `TWSA` (Tr), `HWSA` (H), `ZWSA` (Fr), `IXS1`-`IXS5` (IH) | Tr, Fr, H, IH | N; X as approximation | Road, residential, industry |

#### PHO: phase-outs of existing assets and contracts

| Code | Instrument | Status | CPAT now | FTT | Rep. |
|---|---|---|---|---|---|
| PHO.COAL | Coal-power phase-out (linear to zero; FTT: by 2035 in high-income regions, 2045 elsewhere) | C+F | Cost-based coal retirement (rows 378-379); no mandated path | `coal phaseout` switch, applied through `MWKA` | D (as a capacity path in the engineer power model) |
| PHO.PPA | Coal and gas PPA phase-out | C | rows 381-386 | | D |
| PHO.PERMIT | Investment-permission dates by technology | C | rows 406-415 | | D |

#### BRD and REV

| Code | Instrument | Status | CPAT now |
|---|---|---|---|
| BRD.CBAM | CBAM goods process-emission coverage | C | rows 116-121 |
| REV.LABOUR, REV.CIT, REV.PUBINV, REV.CURR, REV.TRANSF | Revenue use shares and transfer targeting | C | rows 196-205, 305-313 |

FTT has no border measures and no revenue recycling (in E3ME-FTT these sit in E3ME).

### 4. What changes for CPAT

1. **Instruments new to CPAT (from FTT): 9.** TEC.UPSUB (outside EVs), TEC.REGTAX, TEC.ANNTAX, STD.FLEETCO2, STD.TECHCAP (as a cap path), MAN.SALES, MAN.KICK, MAN.BLEND, MAN.EXOSALES; plus PHO.COAL as a mandated path. All other FTT policies map onto an existing CPAT instrument.
2. **Main-scenario list (ScenarioDefinition row 13, `ALL_SCENARIOS`).** The list mixes instruments and packages. Proposal: keep the 14 legacy names (paste compatibility with legacy) and record for each its taxonomy code(s) in the Mapping sheet and `constants.py`, rather than adding FTT instruments to the list. New instruments get their own ScenarioDefinition rows, so they combine with any main scenario, as feebates and ETS do.
3. **Where each new instrument can be built.**
   - Power (engineer model): TEC.UPSUB, OUT.FIT by technology, STD.TECHCAP, PHO.COAL are direct: they enter the investment cost, the LCOE or the capacity paths the model already has.
   - Road: TEC.REGTAX, TEC.ANNTAX, STD.FLEETCO2, MAN.SALES, MAN.KICK, MAN.EXOSALES need the engineer road model, which the user dropped on 2026-10-20 (I61). Without it they can only be shadow prices (STD.FLEETCO2 through the fuel-economy margin) or exogenous paths. MAN.BLEND is direct in the elasticity model.
   - Residential and industry: technology-specific instruments need a technology module that CPAT does not have; S or X approximations only.
4. **Sector mapping FTT to CPAT:** P to power; Tr to road (passenger); Fr to road (freight; CPAT has no passenger/freight split); H to residential (heating only); IH CHI to mining & chemicals, FBT to food & forestry (closest), MTM to machinery, NMM to cement, OIS to other manufacturing.

### 5. Decisions needed (user)

1. Is this the FTT meant? This plan uses the open-source stand-alone FTT (P, Tr, Fr, H, IH). E3ME-FTT versions also have FTT modules for steel, hydrogen and agriculture; their policies are not in the stand-alone code.
2. Taxonomy only, or also build? Recommendation: adopt the taxonomy now (codes in Mapping and `constants.py`, a code next to each ScenarioDefinition policy row), then build the power instruments (TEC.UPSUB, OUT.FIT by technology, STD.TECHCAP, PHO.COAL) and MAN.BLEND, which CPAT can represent directly.
3. For the instruments tagged N: list them with their approximation (S or X), or leave them out of the ScenarioDefinition until a technology module exists?
4. Codes: keep the family.instrument codes here, or align them with the codes of `CPATMasterProcessesCodesAndDefaults.xlsx` once that alignment exercise runs?

## 5. Plan 2: air pollution module (legacy sheet Air pollution and its 9 data tabs) (Plan_AirPollution)

Status: planned, not built (user 2026-10-19: data tabs in the prototype workbook). Decisions for the user in section 7 (the key one: legacy bug B1, adult-disease incidence applied to the 25+ population, which roughly halves the adult burden; by the replication rule a bug is fixed, but the fix about doubles wel.air for Egypt and interacts with the optional Adjust-to-GBD factor). Research below: legacy structure, data tabs, settings, cached Egypt values, bugs and issues, prototype mapping, step plan.

### 1. Legacy `Air pollution` sheet

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

### 2. Data tabs (group `DATA_AIR_POLL->`)

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

### 3. Settings that drive it

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

### 4. Cached Egypt values for testing (B = baseline, P = policy, $50 carbon tax by 2030)

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

### 5. Legacy bugs found (proposed L items) and issues to replicate (I items)

#### Bugs (do not replicate)

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

#### Issues (replicate as legacy, register as I)

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

### 6. Mapping onto the prototype

**Inputs already in the prototype:**

| Legacy input | prototype source |
|---|---|
| Emissions 10 pollutants × 7 sectors + all, t (E3 15859-16065) | Section 15 `aps.<pol>.<sec>` (kt; ×tPerKt). Same layout and pollutant order (v3.12) |
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

### 7. Proposed plan

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

## 6. Plan 3: transport externalities (accidents, congestion, road damage) (Plan_TransportExternalities)

Status: planned, not built (user 2026-10-19: after plan 1 and before or after plan 2, as the user decides). Decisions D1-D9 in section 7 are for the user; D1 (source of vehicle-km: legacy engineer model, elasticity-consistent, or switch with TrModel) is the key one. Research below: legacy map, data, settings, cached Egypt values, bugs and issues, prototype mapping, step plan.

### 1. Where legacy computes it

#### 1.1 Map

| Where | Rows | What |
|---|---|---|
| Transport, A. Description | 1-24 | Text box only |
| Transport, B. Key assumptions | F28:F47 | Literal parameters: F30 `_tran_scenario` = "price"; F40 `_tran_years_SRLR` = 5; F41 0.57 multi-vehicle share of 4-wheeler deaths; F42 0.25 external share of multi-vehicle accident cost; F43 0.5 external share of road maintenance; F44 0.7 external share of congestion time (**unused**); F45 4 marginal/average congestion; F46 0.12 USD/km global road damage; F47 "Yes" (use F46) |
| Transport, B. Elasticities | 51-87 | Tran_Elast lookups (SR, LR, default) for congestion all, weekday and peak. Only `e_congestion_gdp` (H64 = 0.459) and `e_congestion_pop` (H65 = 1.140) feed results. The SR-LR dynamic elasticity (rows 63, 76, 87, 196, 276) feeds only the chart helper row 394 |
| Transport, B. Country data | 91-98 | Transport1 by country and year (array INDEX/MATCH): fatalities (91), maintenance spending (92), congestion avg and peak (93, 94), occupancy (95, unused), tax wedge (D96, first year), free-flow urban speed (D97), share of deaths that are 2-4 wheeler occupants (D98) |
| Transport, B. Macro | 102-108 | GDP growth from Mitigation 16166 (baseline), also used in the policy block; policy GDP 16173 unused. Population from UNPop (104), growth (105). Urban pop (106, unused). Hourly earnings = `'Air pollution'!K855`/8 (107). VSL = `'Air pollution'!K741` (108). Air pollution ends in 2040; 2041 is extrapolated as AA*AA/Z |
| Transport, B. Inputs from Mitigation | 112-157 | Block E of Mitigation, rows 15724-15823: engineer fuel economy by fuel, freight and total VKT (baseline 112-118, policy 130-136); fuel shares 120-128 and 138-146; driving and efficiency margins 148-157 |
| Transport, C. Baseline block (D159 = 1) | 162-237 | VKT, accidents, congestion, travel time, road damage, per-unit $/l |
| Transport, D. Policy block (D239 = ScenarioNum) | 242-317 | Same rows, +80 |
| Transport, E. Results for Mitigation | 321-351 | Per-unit $/l by fuel, `mf.1` and `mf.2`, by code lookup (IFERROR -> 0) |
| | 354-370 | Welfare: levels, changes 356, 360, 364, travel-time value 368-370 |
| Transport, F. Results for charts | 372-457 | Titles, $/l in YearDistn (H394:H398), VKT (404-406), deaths (414-418), congestion (426-435), travel time (442-444), road damage (450-452) |
| Transport | 459-728 | Historical scatter (Tran_Scatter, country list) |
| Mitigation | 128-133 | $/l (`=Transport!I322` ...), feeding Pigouvian tax rows 154-155 (ScenarioDefinition `AddEfficientTaxes`, default No) |
| Mitigation | 15724-15823 | Block E: transport inputs to the sheet (by output code from the engineer block and the switched energy totals) |
| Mitigation | 17733-17735 | Welfare `wel.rod.aci/con/dmg.usd` (= Transport I356, I360, I364). 17737 sum; 17740 `wel.rod.pct`; chart rows 17745-17749 |
| Mitigation | 17771-17779 | Social cost by externality: transport $/l (`tran.acc/con/rdm.cost.gso/die.1`), totals incl. climate (17720-17721) and air pollution (17759-17760) |
| Mitigation | 17788-17789 | FFS "environmental benefits, Harberger" for road gasoline and diesel: ($/l climate + air + accidents + congestion) x change in transport fuel (not in the welfare total; not exported) |
| Mitigation | 17804-17826 | Subsidies: externalities in implicit subsidies (17808, 17820 include transport $/l, baseline `mf.1`) |
| Mitigation | 17977-18006 | Efficient prices by component, scenario 2 (`mf.2`): accident (17980, 17995), congestion (17981, 17996), road damage (17997); Pigouvian tax 17989, 18004 |
| LiveOutputs | 885-897, 899-909, 273-299, 1224+ | Transport effects, welfare, efficient prices, subsidies (section 1.6) |
| Dashboard | 561-604 | 4 x 4 transport charts (section 1.6) |

#### 1.2 Equations (one scenario s; baseline s = 1)

**Accidents**
- Deaths: `D_s(2022)` = Transport1 fatalities; then `D_s(t) = D_s(t-1) x VKT_s(t)/VKT_s(t-1)`. The 2023-2025 data are not used.
- External deaths: `Dx = D x sh4 x 0.57 x 0.25 + D x (1 - sh4)`, with sh4 = 0.62 (D98).
- Fatal cost: `Dx x VSL / 1e9` (USD bn).
- Non-fatal cost = fatal cost x `0.049 x (Dx/D)^-2.56` (literal; 0.3416 for Egypt).
- `ACC_s` = fatal + non-fatal. Per km: `a = ACC/VKT`. It is identical in both scenarios (deaths scale with VKT), so `a(t) = a(2022) x VSL(t)/VSL(2022)`.

**Congestion**
- Average congestion `c(t)`: data 2022-2024 (row 197 is filled only I:K), then `c(t-1) x (1+g)^0.459 x (1+n)^1.140`. Here g is **baseline** GDP growth and n population growth, the same in both scenarios.
- Speed = free-flow speed / (1 + c/100).
- Delay hours = VKT/speed - VKT/free-flow speed.
- Value: `hours x wage_h x (1 - tax wedge)`. The note says "80% of after tax wages", but the formula has no 0.8 (see section 5).
- `CON_s = 4 x value`. Per km `k = CON/VKT` does not depend on VKT or the scenario.

**Road damage**
- `RDM_s = 0.12 x freightVKT_s` (F47 = "Yes").
- The country option (F47 = "No") uses maintenance spending x 0.5 / freight VKT, with data 2022-2024 then scaled by freight VKT.

**Per liter of fuel f** (gso, die, lpg, nga; ecy per kWh)
- `e_f = (cost per km) x FE_f x dm_f/(dm_f+em_f) x shT_f`.
  - FE_f: engineer average fuel economy of the stock.
  - dm and em: driving and efficiency elasticities. For diesel, LPG, gas and electricity they are weighted by engineer passenger/freight fuel use (Mitigation 15736-15745).
  - shT_f: road share of total use of fuel f (switched model).
- Road damage, diesel: `0.12 x FE_die x dm/(dm+em) x shFreight_die x shT_die`.
- Computed per scenario. The baseline (`mf.1`) feeds Mitigation 128-133, 17771-17776 and subsidies; the policy (`mf.2`) feeds efficient prices 17977+.

**Welfare (bn USD, + = gain)**
- `wel.rod.aci = ACC_1 - ACC_s = a x (VKT_1 - VKT_s)`
- `wel.rod.con = k x (VKT_1 - VKT_s)`
- `wel.rod.dmg = 0.12 x (frVKT_1 - frVKT_s)`

Checked against the cache: 2031 0.005817 x 30.58 = 0.1779; 0.008986 x 30.58 = 0.2747; 0.12 x (20.62 - 19.03) = 0.1916.

**Monetisation against the change in fuel use**
- The legacy welfare does not use the $/l values. It uses the engineer change in VKT directly.
- $/l x change in fuel appears only in:
  - the FFS rows 17788-17789: transport fuel ktoe change x liters per ktoe;
  - implicit subsidies: $/l x consumption;
  - efficient prices: $/l as price components.

#### 1.3 What depends on the parked engineer model (section 5b) and what does not

| Input | Source in legacy | Engineer-dependent? |
|---|---|---|
| Total VKT path, baseline and policy (rows 118, 136) | 5b distance (legacy 5336; prototype `trkmt`) | **Yes**: the denominator of deaths per km, delay hours, and the **policy change in VKT (all welfare)** |
| Freight VKT (117, 135) | 5b (5334; prototype `trkm` fre) | **Yes**: road damage level and change |
| Average fuel economy by fuel (112-116, 130-134) | 5b (5356-5373; prototype `trafg`, `trafo`, `trafe`) | **Yes**: every $/l value |
| Diesel/LPG/gas/electricity passenger-freight split (15727-15735) | 5b fuel use by class (prototype `trfcp`, `trfcf`, `trfcc`, `trfce`) | **Yes**: margin weights and the freight share of diesel |
| Road share of total fuel (15759-15781) | Switched model (`ener`) | No (follows TrModel) |
| Elasticities dm, em | `_el_dem_*_rod`, `_el_eff_*_rod` (prototype Elasticities, section 5 parameters) | No |
| VSL, wages, congestion, fatalities, speed, tax wedge, population, baseline GDP growth | Air pollution, Transport1, UNPop, Mitigation | No |

- prototype 5b is computed in every scenario whatever TrModel is, so legacy can be replicated today. But the default welfare would then depend on a model the user parked (I28, I61).
- An elasticity-consistent alternative (section 7, option B) needs from 5b only base-year (data-calibrated) quantities, or nothing at all if FE comes from Transport1.

---

### 2. Data tabs

| Legacy tab | Used for | In prototype? | Action |
|---|---|---|---|
| Transport1 | Fatalities, maintenance spending, share of deaths 2-4 wheeler occupants, total and peak congestion, urban travel speed, tax wedge (occupancy unused) | **Yes** (legacy table, `TrKey`, `TrYr`, `TrVal`); the columns are present (cols 16-21, 87-95 of `legacy_Transport1.csv`) | Only new lookups (`Inputs` block or section-18b data rows) |
| Tran_Elast (221 x 54, `_tran_elasticities`, `_tran_elastcountries`, `_tran_elastnames`) | `e_congestion_gdp`, `e_congestion_pop` (results); SR/LR elasticities (charts only) | **No** | New legacy table under `DATA_TRAN->>` (NORMS 1.5: unchanged, keys right); small |
| Tran_Scatter (124 x 23) | Historical scatter charts only | No | Skip (decision D7) |
| Notes | Text (econometrics of Tran_Elast) | No | Not needed; cite in method note |
| Air pollution (module sheet) | VSL (741: options 734-738), daily earnings (855), deflator to ResultsYear (718), PPP ratio (714 from WEO PPPPC/NGDPD) | No (prototype section 15 has emissions only, no health/VSL) | Rebuild VSL and earnings rows (they are also the future air-pollution health module's inputs) |
| ILO (603 rows; key `Earnings-<unit>-<iso>`, years 2018-2023) | Monthly earnings (USD) / `WorkDays` (ScenarioDefinition 334 = 20) | **No** | New legacy table (DATA_OTHER or with the air-pollution tabs) |
| Countries col X "VSL country grouping" | VSL group | **Yes** (`legacy_Countries_cells.csv` col 24) | Lookup only |
| Air pollution D45:E51 (group VSL in mln 2022 PPP USD and GDPpc 2022 PPP: OECD 7.1/56224, EU 8.4/58043, USA 8.5/77178, HIC 7.9/62989, UMIC/LMIC/LIC 1.1/13576) | VSL transfer | No | New small parameter table (TransportParams or a VSL parameter block) |
| WEO PPPPC, NGDPD; UNPop; population; deflator | VSL, earnings growth | **Yes** | Reuse |
| Air_Data (labour share), WB (GNI) | Earnings fallback when no ILO data; VSL options GNI x 100 / x 160 | No | Only if those options are replicated (D3) |

---

### 3. Settings that drive it

| Setting | Where | Options | Egypt default (legacy) |
|---|---|---|---|
| TrModel | ScenarioDefinition 340 | Elasticity / Engineer | Elasticity (the Transport sheet ignores it) |
| VSLMethod | ScenarioDefinition 327 | GNI*100, GNI*160, Transfer from Group (+ "PPP"/"USD" from Air pollution G36), Manual | "Transfer from Group" (G36 = USD), i.e. "Transfer from Group, USD"; the G (Defaults) column says "Transfer from OECD" |
| VSLManual | ScenarioDefinition 328 | number (constant ResultsYear PPP USD) | 500,000 |
| VslElSource, VslEl | ScenarioDefinition 329-330 | | **#REF!** in the legacy file; VSL income elasticity is hard-wired to 1 in Air pollution 736 |
| WorkDays | ScenarioDefinition 334 | days/month | 20 |
| ApLabSh | ScenarioDefinition 335 (Air pollution G82) | earnings fallback | 0.65 |
| YearDistn | ScenarioDefinition 304 | | 2030 (chart "externality per liter" H394:H398) |
| AddEfficientTaxes, ClimateEffTax, AddEfficientTaxesPhaseInYears, ExternalityAddVAT, YearFuelPrices | ScenarioDefinition 217, 216, 212, 218, 282 | | No*, Yes*, 5, Yes*, 2025: consumers of the $/l (Pigouvian tax, efficient prices); not in the prototype |
| Transport sheet literals | Transport F30, F40-F47 | | price, 5, 0.57, 0.25, 0.5, 0.7 (unused), 4, 0.12, Yes |
| Literals inside formulas | Transport 181, 107 | | 0.049, -2.56; 8 hours/day |
| Elasticities | `_el_dem_gso_rod` -0.4, `_el_eff_gso_rod` -0.4; diesel mix -0.340 (both) | | Elasticities tab |

Nothing for transport externalities is on 'Manual inputs'.

---

### 4. Cached Egypt values (for tests)

Static inputs:
- Transport1 2022: fatalities 5,610.47; maintenance 213.38 (2023: 314.96; 2024: 323.10); congestion 9.37 / 47.42; free-flow speed 59.05 km/h; tax wedge 0.20; share of deaths that are 2-4 wheeler occupants 0.62.
- Elasticities: e_congestion_gdp 0.45901, e_congestion_pop 1.14045.
- Daily earnings 2022: 8.4584 USD (ILO 169.168/20).
- VSL 2022: 387,389.73.
- H394:H398 (2030): accidents gso 0.03955, die 0.01163; congestion gso 0.05739, die 0.01687; road damage die 0.14839.

| Cell | Item | 2022 | 2025 | 2027 | 2030 | 2031 | 2035 | 2041 |
|---|---|---|---|---|---|---|---|---|
| T108 | VSL (constant 2026 USD) | 387,390 | 256,759 | 297,411 | 361,662 | 364,405 | 408,204 | 481,756 |
| T107 | Hourly earnings (USD) | 1.057 | 1.107 | 1.175 | 1.311 | 1.355 | 1.54 | 1.851 |
| T168/T248 | VKT all vehicles, base / policy (bn km) | 220.8 / 220.8 | 203.8 / 203.8 | 231.7 / 226.5 | 314 / 290.9 | 353.7 / 323.2 | 580.1 / 507.4 | 1,270 / 1,066 |
| T169/T135 | Freight VKT base / policy (bn km) | 12.01 / 12.01 | 11.12 / 11.12 | 13.5 / 13.23 | 18.32 / 17.11 | 20.62 / 19.03 | 33.16 / 29.45 | 66.96 / 57.49 |
| T173/T253 | Road deaths base / policy | 5,610 / 5,610 | 5,177 / 5,177 | 5,885 / 5,755 | 7,976 / 7,390 | 8,987 / 8,210 | 14,738 / 12,890 | 32,253 / 27,089 |
| T417 | Cumulative averted deaths | 0 | 0 | 129.9 | 1,405 | 2,182 | 7,788 | 29,076 |
| T200 | Congestion, average (%; both scenarios) | 9.37 | 9.728 | 10.47 | 11.79 | 12.24 | 14.15 | 17.39 |
| T210 | Congestion, peak (%) | 47.42 | 49.23 | 53 | 59.66 | 61.92 | 71.61 | 88.03 |
| T185 | Accident external cost per km (USD; both) | 0.006184 | 0.004099 | 0.004748 | 0.005773 | 0.005817 | 0.006516 | 0.00769 |
| T220 | Congestion external cost per km (USD; both) | 0.005369 | 0.005836 | 0.00667 | 0.008377 | 0.008986 | 0.01181 | 0.01745 |
| T184/T264 | Accident external cost base / policy (bn) | 1.366 / 1.366 | 0.8353 / 0.8353 | 1.1 / 1.076 | 1.813 / 1.679 | 2.058 / 1.88 | 3.78 / 3.306 | 9.763 / 8.2 |
| T219/T299 | Congestion external cost base / policy (bn) | 1.186 / 1.186 | 1.189 / 1.189 | 1.545 / 1.511 | 2.63 / 2.437 | 3.179 / 2.904 | 6.85 / 5.991 | 22.15 / 18.6 |
| T233/T313 | Road damage base / policy (bn) | 1.441 / 1.441 | 1.335 / 1.335 | 1.62 / 1.587 | 2.199 / 2.053 | 2.475 / 2.283 | 3.979 / 3.533 | 8.036 / 6.899 |
| T322/T323 | Accidents, gasoline $/l base / policy | 0.04142 / 0.04142 | 0.02781 / 0.02781 | 0.03239 / 0.03239 | 0.03955 / 0.03988 | 0.03995 / 0.04049 | 0.04537 / 0.04733 | 0.05551 / 0.06129 |
| T324/T325 | Accidents, diesel $/l base / policy | 0.0126 / 0.0126 | 0.008334 / 0.008334 | 0.009408 / 0.009507 | 0.01163 / 0.01221 | 0.01178 / 0.01255 | 0.01359 / 0.01552 | 0.01676 / 0.02145 |
| T333/T334 | Congestion, gasoline $/l base / policy | 0.03596 / 0.03596 | 0.0396 / 0.0396 | 0.04551 / 0.0455 | 0.05739 / 0.05787 | 0.0617 / 0.06254 | 0.08223 / 0.08577 | 0.1259 / 0.139 |
| T335/T336 | Congestion, diesel $/l base / policy | 0.01094 / 0.01094 | 0.01187 / 0.01187 | 0.01322 / 0.01335 | 0.01687 / 0.01771 | 0.0182 / 0.01939 | 0.02463 / 0.02813 | 0.03801 / 0.04866 |
| T344/T345 | Road damage, diesel $/l base / policy | 0.146 / 0.146 | 0.1457 / 0.1457 | 0.146 / 0.1479 | 0.1484 / 0.1572 | 0.1493 / 0.1608 | 0.1533 / 0.1774 | 0.1604 / 0.2078 |
| M17733 (T356) | Welfare: averted accidents (bn) `wel.rod.aci.usd` | 0 | 0 | 0.02427 | 0.1332 | 0.1779 | 0.4739 | 1.563 |
| M17734 (T360) | Welfare: reduced congestion (bn) `wel.rod.con.usd` | 0 | 0 | 0.03409 | 0.1933 | 0.2747 | 0.8589 | 3.546 |
| M17735 (T364) | Welfare: reduced road damage (bn) `wel.rod.dmg.usd` | 0 | 0 | 0.03242 | 0.1454 | 0.1916 | 0.446 | 1.137 |
| M17740 | Transport co-benefits, share of GDP (`wel.rod.pct`) | 0 | 0 | 0.0001369 | 0.0006114 | 0.0007965 | 0.001833 | 0.004975 |
| M17737 | Total national welfare (bn, legacy sum) | -6.9e-06 | 0.1242 | 2.56 | 9.67 | 11.58 | 19.39 | 31.51 |
| M17778 | Total externalities gasoline $/l (incl. climate, air pollution) | 0.1078 | 0.08863 | 0.1026 | 0.1271 | 0.1322 | 0.1622 | 0.2181 |
| M17779 | Total externalities diesel $/l | 0.2786 | 0.2443 | 0.2616 | 0.2944 | 0.2995 | 0.334 | 0.37 |
| M17810/M17822 | Efficient price gso / die (subsidy block, base) | 1.167 / 1.178 | 1.021 / 1.031 | 1.048 / 1.06 | 1.051 / 1.077 | 1.054 / 1.081 | 1.124 / 1.152 | 1.255 / 1.253 |

Use in tests:
- The engineer inputs of the cache (Transport rows 112-157) are in `data/mvp_legacy_extracts/legacy_transport_reference.csv` (legacy rows 5333-5373) and in `transport_model_ref.legacy_test(run, fix=frozenset())`.
- A Python reference fed with those inputs should reproduce every row above to rounding.
- The prototype 5b has the fixes L25-L41, so prototype values match legacy only in the base year and in the scenario-independent per-km costs.

---

### 5. Legacy bugs (proposed L items, next free L124+) and issues to replicate (I69+)

#### 5.1 Bugs

**B-a. Policy freight VKT points at the electricity fuel economy (survey B16).**
- Cells: Transport I249:AB249 `=IF($D239=1,I$117,I$134)`; label C249 = "Road electricity - fuel economy"; latent in I169 (`I$134` branch).
- Effect: row 309 country-specific maintenance extrapolation (only when F47 = "No") and code `tranfre.vkt.2`. None on the default welfare: rows 311 and 313 read 135 directly.
- Fix: the scenario's freight VKT.

**B-b. #DIV/0! where a fuel has no road use (survey B16).**
- Cells: Transport 188, 223, 235, 268, 303, 315: `SUM(margins)=0` for LPG gives #DIV/0!. It is masked to 0 by IFERROR in 326-351, but a total would break.
- Effect: none for Egypt.
- Fix: 0 when the margins sum to 0 or road use is 0.

**B-c. Value of time: label says 80% of the after-tax wage, formula uses 100%; F44 is a dead input. Candidate, confirm.**
- Cells: Transport 218/298: D218 note "80% of after tax wages", formula `wage_h x hours x (1 - wedge)` with no 0.8. F44 = 0.7 ("portion of travel time lost in congestion that is an externality") is never used.
- Effect: congestion costs and welfare x0.8 (x0.56 if F44 also applies), i.e. -20% (-44%).
- Options: replicate (and register as an issue), or fix.

**B-d. Road damage per liter of diesel uses the wrong fuel economy. Candidate, confirm.**
- Cells: Transport 234/314: `0.12 x FE_die(avg, passenger+freight; 6.3 km/l) x dm share x shFreight x shT`. The cost is per **freight** km, so the km per liter must be freight km per freight liter (about 1.8 km/l in Transport1), or freight km / road diesel liters.
- Effect: Egypt 2031 legacy 0.149 $/l against about 0.065 $/l with freight km per road diesel liter (20.6 bn km / 12.1 bn l = 1.71 km/l), so road damage per liter is about 2.3x too high. It flows into total externalities, implicit subsidies and efficient prices; the welfare levels are unaffected.

**B-e. Daily earnings not deflated to ResultsYear USD. Candidate.**
- Cells: Air pollution K850 (= ILO 2022 USD), labelled "constant 2026 $USD"; later years grown with real GDP per capita. The VSL is deflated (K718).
- Effect: congestion costs about 11% low (deflator 1.124).

**B-f. VSL elasticity inputs are #REF!.**
- Cells: ScenarioDefinition F329:F330 (VslElSource, VslEl). The income elasticity is hard-wired to 1 in Air pollution 736.
- Effect: none on values; dead inputs.
- Fix: drop, or wire up later with the air-pollution module.

**B-g. Accident chart row uses the full VSL with the wrong sign.**
- Cells: Transport I418: `-VSL x averted deaths` (all deaths, full VSL, opposite sign), titled "Change in externality cost from road accidents" (Dashboard R577). LiveOutputs and welfare use 356 (external share).
- Effect: chart only.
- Fix: `= ACC_1 - ACC_s`.

**B-h. LiveOutputs export gaps and mislabels.**
- Road-damage welfare (17735, `wel.rod.dmg.usd`) is not exported (rows 901-903).
- E885/886 codes `tran.vmt.*` while the sheet codes are `tran.vkt.*`.
- H887 'vmt' for deaths.
- D903:D909 take the unit of the row above (E17734 for 17736, ...).
- Fix in the prototype LiveOutputs.

**B-i. FFS diesel row: wrong conversion factor and road damage left out. Only if the FFS block is rebuilt.**
- Cells: Mitigation 17789: diesel converted with `_conv_ktoe_liter_gso`, and road damage 17776 omitted. The block is not in the welfare total and not exported.
- Same class as the section-18 note "diesel and kerosene converted with the wrong factors".

**B-j. Unit and scenario labels (cosmetic).**
- Transport 370, 442-444: "Million" but values are USD bn.
- 264-265: "baseline" in the policy block.
- Mitigation 15771-15775: "baseline" on policy rows.

#### 5.2 Design issues to replicate (I items, unless the user decides otherwise)

| # | Issue |
|---|---|
| I-a | Externalities use **engineer** VKT, fuel economy and class splits even when TrModel = Elasticity (survey B16), so welfare is inconsistent with the fuel use actually modelled. Egypt: engineer VKT -8.6% in 2031 (-16% in 2041) against switched road gasoline -12.9% and diesel -14.3% (-27% and -29% in 2041). The legacy note D168 says "simplified approach for now = change in fuel consumption". **This is decision D1** |
| I-b | Deaths scale 1:1 with VKT from the 2022 data (2023-2025 data unused). Congestion level does not respond to the policy: the elasticities are computed but unused, and the policy block uses baseline GDP growth. Congestion cost moves only with VKT |
| I-c | Congestion data used only for 2022-2024 (row 197 filled I:K), then grown with the GDP and population elasticities (Egypt 9.4% to 17.4% by 2041) |
| I-d | Literals: 0.049 x ratio^-2.56 (non-fatal), 0.57, 0.25, 0.5, 4, 0.12 USD/km (not deflated, constant), 8 h/day; tax wedge and free-flow speed of the first year only. Make them parameters (TransportParams) |
| I-e | Per liter: the all-vehicle average $/km is applied to every fuel. The driving share uses baseline margins; the diesel margins are weighted by engineer passenger/freight use. $/l is per liter of **all** use of the fuel (x road share) |
| I-f | The baseline $/l (`mf.1`) feeds Pigouvian taxes and implicit subsidies; the scenario $/l (`mf.2`) feeds efficient prices |
| I-g | VSL "Transfer from Group, USD": group VSL x (PPP GDPpc_t / group GDPpc) x deflator / (PPP/market ratio)_t. It is volatile with the exchange rate (Egypt 387k -> 257k over 2022-2025). Air pollution stops in 2040; 2041 is extrapolated geometrically |
| I-h | Welfare = change in the level of external costs (rectangle), not a triangle; 2-3 wheelers are in total VKT; road damage only for freight; country maintenance option unused by default |

---

### 6. Mapping onto the prototype

#### 6.1 Inputs already available
- Road and total fuel use by fuel, per scenario: `ener` road rows, section 5 and totals.
- Elasticities `εU` (usage) and `εF` (efficiency) of road fuels: section 4 parameters; legacy `_el_dem`/`_el_eff`.
- 5b engineer rows per scenario: `trkm` (pas, fre, cyc), `trkmt`, `trfcp`, `trfcf`, `trfcc`, `trfce`, `trafg`, `trafo` (die, lpg, nga; fix B22), `trafe`.
- GDP growth `gdp` (baseline via `.ref`), population `pop`, `pop.g`, deflator `defl`.
- WEO PPPPC and NGDPD; Countries col X; Transport1 (`TrKey`, `TrVal`); liters per ktoe constants; `wel.usd` (section 18).

#### 6.2 New
1. **Data**: Tran_Elast (legacy table, DATA_TRAN); ILO (legacy table); VSL group table and Transport literals as TransportParams keys (`tex.*`).
2. **Inputs block**, `Inputs_tex` (NORMS 1.5 rule 2c): Transport1 lookups (2022-2025), the two congestion elasticities, the group VSL parameters.
3. **Mitigation section 18, new lettered sub-block "18b Welfare and externalities, road transport"**. About 45 rows per scenario group; NORMS 3c.4 allows a module sheet instead, see D2. Proposed codes:

| Code | Content |
|---|---|
| `vsl` | VSL, constant ResultsYear USD |
| `wageh` | Hourly earnings |
| `tex.vkt`, `tex.vktf` | Total and freight VKT, per D1 |
| `tex.fe.<f>` | Fuel economy by fuel |
| `tex.dsh.<f>` | Driving share dm/(dm+em) |
| `tex.rsh.<f>`, `tex.fsh.die` | Road share of fuel use, freight share of diesel |
| `tex.dth`, `tex.dthx` | Deaths, external deaths |
| `tex.acc` | Accident external cost, USD bn |
| `tex.acckm` | Accident cost per km |
| `tex.cng`, `tex.cngp` | Congestion average and peak, % |
| `tex.spd`, `tex.hrs` | Speed, delay hours |
| `tex.con`, `tex.conkm` | Congestion external cost, per km |
| `tex.rdm` | Road damage, USD bn |
| `tex.acc.<f>`, `tex.con.<f>`, `tex.rdm.die` | $/l (gso, die; lpg, nga, ecy per D5) |
| `wrod.aci`, `wrod.con`, `wrod.dmg` | Welfare = `.ref` level - level (3c rule 2: differences that feed `wel` are scenario rows) |
| `wrod.all` | Sum of the three |

   Then `wel.usd = wcli.nat - eff - mfc + wrod.all`; new `wel.rod` (% of GDP); legacy chart order cli, air (later), rod, eff.
4. **LiveOutputs** (legacy codes, scenario appended):
   - `mit.wel.rod.aci.usd`, `mit.wel.rod.con.usd`, `mit.wel.rod.dmg.usd` (fixing B-h), `mit.wel.rod.pct`;
   - `tran.acc.cost.gso/die.1`, `tran.con.cost.gso/die.1`, `tran.rdm.cost.die.1` (from scenario 1 rows), with the `.2` series as efficient-price components later;
   - `tran.vkt.*` (fixing the `vmt` codes), `tran.deaths.*`, `tran.acc.avd.cum.*`, `tran.congestionP.*`.
5. **Charts**: VKT, deaths and averted deaths, congestion (all, peak), road damage, externality per liter in YearDistn (D7).
6. **Python reference**: `transport_ext_ref_v6_4.py`.
   - Pure functions for section 1.2.
   - `legacy_test()` feeds the cached legacy inputs (Transport rows 91-157 from the xlsb or the reference CSVs) and must reproduce rows 162-370 and Mitigation 17733-17740 for every year (switch `FIXES` off).
   - `ALL_FIXES` for the prototype.
7. **Checks** in `check_full.py`:
   - recompute 18b in every group from workbook values (`check_results_memos` style);
   - `wrod` = 0 in scenario 1;
   - per-km costs equal across groups (I-b);
   - `wel.usd` identity;
   - paste test (`check_paste`) for groups 4-7;
   - all-country clone (`check_allcountry`) with the Tran_Elast and ILO rows;
   - LAMBDA test group, if 18b rows get LAMBDAs (e.g. `EXTPERL` for $/l).
8. **Docs and register**: `ResultsSections_Method` section 18b; `Transport_vs_Legacy` (B16 resolved or kept); L items B-a..B-j, I items I-a..I-h, LegacyDiff rows; remove "transport co-benefits" from the Q42 "not as rows" list.

---

### 7. Proposed plan

| Step | Content | Size |
|---|---|---|
| 0 | User decisions D1-D9 (below); register L and I items | small |
| 1 | Python reference `transport_ext_ref_v6_4.py`: equations of 1.2, legacy mode reproducing the cache (all rows, 2022-2041, both blocks) and the fix switches; effect sizes of each candidate fix (B-c, B-d, B-e) and of option A vs B for Egypt | medium |
| 2 | Data: Tran_Elast and ILO legacy tables (extract script, `DATA_TRAN`/`DATA_OTHER`, names, keys right, all-country capacity), VSL group table and literals into TransportParams; `Inputs_tex` lookups | medium |
| 3 | VSL and hourly-earnings rows (Transfer from Group USD/PPP + Manual, per D3), WorkDays, deflator, PPP ratio from WEO; 2041 rule | medium |
| 4 | 18b physical rows: deaths, accident cost, congestion path, delay hours, congestion cost, road damage; per-km costs | medium |
| 5 | VKT, fuel-economy and share inputs per D1 (A: read 5b `trkmt`, `trkm`, `trafg`, `trafo`, `trfc*`; B: per-liter x change in road fuel with a base-year FE; C: switch) and the $/l rows | medium |
| 6 | Welfare rows `wrod.*`, `wel.usd`/`wel.rod` update, summary memo; LiveOutputs codes; Charts | small-medium |
| 7 | Checks (recompute, scenario-1 zero, paste, all-country, LAMBDA group if any); build and quick check; compare with the cache (base year exact; legacy-mode reference) | medium |
| 8 | Docs: ResultsSections 18b, Transport_vs_Legacy, Replicated/NotReplicated, LegacyDiff, CAVEATS, TODO | small |

The efficient prices, implicit and explicit subsidies, the Pigouvian tax and the FFS block are **not** in this plan. They also need the air-pollution $/l (legacy Air pollution module, not in the prototype). Step 5 delivers the transport $/l rows those blocks will read later.

#### Decisions for the user

**D1. VKT source (the key decision).**
- (A) **Legacy**: read engineer 5b VKT, fuel economy and splits in every scenario, whatever TrModel is. This replicates the cache's mechanics; register I-a. The default welfare then depends on the parked engineer model (I28, I61).
- (B) **Elasticity-consistent**: welfare = Σ_f $/l (road liter, driving share, no road-share factor) x change in road fuel f, with FE from the 5b base year or Transport1. Egypt 2031: accidents 0.083, congestion 0.128, road damage 0.40 (0.18 with B-d fixed), against legacy 0.178 / 0.275 / 0.192. This is a departure and needs a U/I entry.
- (C) Follow TrModel: A under Engineer, B under Elasticity. NORMS default is A; C is the likely best compromise.

**D2. Placement.** Sub-block 18b on Mitigation (recommended, about 45 rows) or a module sheet with Mitigation's group geometry (NORMS 3c.4).

**D3. VSL options.** Default plus Manual only, or all five (GNI x 100 and x 160 need WB GNI data). The earnings fallback (Air_Data labour share) is needed only for countries without ILO data.

**D4. Bug candidates.**
- Fix: B-a, B-b, B-g, B-h, B-j (clear bugs).
- Confirm: B-c (0.8 VOT and F44), B-d (road-damage fuel economy), B-e (earnings deflator).
- B-f and B-i go to the air-pollution module work later.

**D5. Fuels for $/l.** Gasoline and diesel only (what legacy Mitigation reads and exports), or also LPG, gas and electricity (computed in legacy, unused).

**D6. Scope.** Confirm that efficient prices, subsidies, the Pigouvian tax and the FFS rows wait for the air-pollution health module; the transport $/l rows are delivered now.

**D7. Charts.** Which Dashboard charts to port (VKT, fatalities, congestion, travel time, road damage, $/l in YearDistn); skip the Tran_Scatter historical plots (recommended).

**D8. Tran_Elast.** Import the whole legacy table (NORMS 1.5, recommended) or only the two congestion elasticities.

**D9. Literals.** Transport literals (F41-F47, 0.049/-2.56, 8 h) become TransportParams keys, not ScenarioDefinition rows (NORMS 4: no new ScenarioDefinition functionality).

## 7. Plan 1: everything else (user request 2026-10-19; status at v6.1, 2026-10-20) (Plan_Rest)

Plans 2 (air pollution) and 3 (transport externalities) are separate: `Plans.md` (section Plan_AirPollution),
`Plans.md` (section Plan_TransportExternalities); both modules were dropped by the user on 2026-10-20 (issues I69, I70). ETS goal-seek runs are excluded (NORMS 5: the user tests I30 separately).

### Step 1. Release v6.0 (done)

| # | Task | Status |
|---|---|---|
| 1.1 | Smaller items: I33 fixed, I43 replicated, I68 in part (WEO real GDP), I14 accepted | done |
| 1.2 | Distribution as legacy: ASPIRE and poverty-line transfers, median flags, chart outputs, production-sector prices and top-20 ranking, charts; bugs D10-D31; switch tests | done |
| 1.3 | Complete rebuild, quick check | done (PASS) |
| 1.4 | Full check (`check_full.py`, goal-seek parts skipped); fix genuine failures | v6.0: sections 0-4 pass; run on v6.1 |
| 1.5 | Regenerate every document: Word documentation, bugs/issues register (Word, Excel), bug-fix book, issues document, team tracker, replication lists, working-version copies, top-level workbook, README, TODO, CAVEATS, QuickStart | done (v6.1) |
| 1.6 | Consistency audit and report: one version everywhere; every bug and issue in the register, the Word and Excel registers, the tracker and the replication lists with the same status; method notes current; LegacyDiff consistent | done (v6.1) |
| 1.7 | Report on the rule (NORMS 0): every legacy bug fixed, every legacy issue replicated or tracked, with the exceptions | done (v6.1) |

Register labels to correct in 1.6 (status vs replication label disagree): I25 and I26 (resolved in v5.6 by replicating legacy, still labelled "not replicated"), I58, I67 (by design).

### Step 2. Open items that need no new data (v6.1, done)

| # | Item | What | Size |
|---|---|---|---|
| 2.1 | I49 producer subsidies | Replicate the legacy price effect: subsidy per unit spread over world demand (oil), half world / half domestic (coal, gas), domestic use (biomass), entering the supply cost (legacy formula as in the I49 register entry; world demand Prices_int rows 321-333 already in the prototype) | medium, done: replicated, L124 and L125 fixed |
| 2.2 | I46 revenue by policy | Renewable subsidies are in the power model since v5.4 (P4): add their revenue line if missing and close that half; transport revenues stay with the parked road model (I61) | done: renewable since v5.4; transport dropped |
| 2.3 | I68 rest | Reference years 2021-2022 from the GHGs inventory (already in the prototype); 2018-2020 need data (to the data list) | done: 2021-2024 from the inventory |
| 2.4 | I47 methane fee in the fiscal space | Needs a structural choice (the source allocation reads GHGYear activity, which makes fis.rev circular). Option: allocate on scenario-1 activity (no feedback), then count the fee from GHGYear + 1. **Your decision** | done: as legacy, on the stored scenario-1 activity (user 2026-10-20) |
| 2.5 | Distribution choices to confirm | No-data ASPIRE program falls back to cash (D11); median flag on the targeted transfer only (D13); urban and rural use the overall per-capita transfer (DI4/D15). **Your confirmation** | done: fixed as bugs (user 2026-10-20) |
| 2.6 | I52, I53 | Replicate when ETS coverage by Dashboard groups and manual domestic prices are built (not planned) | - |

### Step 3. Section 5: Excel review (I1)

| # | Task | Who |
|---|---|---|
| 3.1 | Checklist (`ExcelReview_Checklist.md`, done) for Excel 365 on Windows: open, recalculate, LAMBDA names, macros (RunAllScenarios with an ETS definition at the override price; CheckBatchRun), charts, rolled-up view, paste test | I prepare |
| 3.2 | Run the checklist in Excel, report differences | you (Windows) |
| 3.3 | Fix what Excel shows | I |

### Step 4. Data requests (to send; nothing to build until data arrive)

- I64: GAINS combustion emission-factor paths (high priority).
- I65: blank VAT cells in the IMF price dataset (high priority).
- I13: proprietary tables for other countries.
- I68: historical GHGs 2018-2020 (and any reference year after 2017).

Request note: `Plans.md` (section DataRequest) (done).

### Dropped or tested by the user (not in this plan)

Dropped 2026-10-20: I28 and I61 (engineer road model), I62 (partial adjustment), I63 (prices in real local currency),
I69 (air-pollution co-benefits), I70 (transport externalities). Tested by the user: I30 (ETS goal seek).

## 8. Data request (DataRequest)

Four items need data from the CPAT data team. Nothing is built until the data arrive. Until then the workbook keeps the fills described in the register (`issues_register.py`). Send one file per item, in the legacy layout. The data steps then load it unchanged.

| Issue | Priority | What we need | Format | Where it goes |
|---|---|---|---|---|
| I64 | High | GAINS combustion emission-factor paths by year: CH4, N2O and local pollutants, by fuel and sector, for every country. The NoPropData legacy file has zeros in these rows because the data are proprietary. | The legacy CPAT file with the proprietary tables, or sheet `EF_PM` of it (same columns as legacy) | Sheet `EF_PM` (legacy table, loaded by `extract_legacy_tables.py`). The prototype then reads the paths instead of the linear fill to EFEndYear (LegacyDiff LD47). |
| I65 | High | The blank VAT cells of the IMF price dataset: which are missing values and which are true zeros. | The corrected price dataset (legacy `Prices_dom` layout), or a list of country, fuel, sector and VAT rate | `data/` price files through `extract_data.py` (sheet `Prices_dom`). The prototype fill (general VAT rate for residential coal and gas and for oil products; LegacyDiff LD3) is then dropped. |
| I13 | Medium | The proprietary tables for all countries: Balances, EnergyCons, EF_PM, IO_GTAP, HHSurvey, ASPIRE, WHOCooking. The NoPropData file holds Egypt only. | The full legacy CPAT file, or the CPAT data pipeline output | The legacy data tabs of the same names (`extract_legacy_tables.py`). Then rebuild BaselineCO2 for scenario 1 and test a second country end to end. |
| I68 | Low | Historical GHG emissions 2018-2020 by country: GHGs excluding and including LULUCF, and CO2. Also any NDC reference year after 2017 that the inventory (2021-2024) does not cover. | Legacy `GHGs` rows 954-1189 layout with the extra year columns | Sheet `GHGHist`. NDC reference years 2018-2020 then stop returning N/A. |

Contacts and status are tracked in the team tracker (`legacy/workbooks/Tracking issues.xlsx`, sheet BUGSandISSUES).

## 9. Plan 4: modular CPAT - standalone Distribution, AP and TCB data links (plan, 2026-10-22; not started) (Plan_Modules)

**Request (user 2026-10-22).** Modularise CPAT: Distribution, air pollution (AP) and transport co-benefits (TCB) get their own workbooks and versions. Mitigation concentrates what it exports in one or two sections; each module starts with a section of inputs from Mitigation in the same format. Each module has a data-linking Cover (the approach of the Mitigation data links) pointing at a stably named copy of the latest mitigation workbook in the repo. The mitigation prototype is renamed a prototype. Priority: the standalone Distribution. AP and TCB: only the data import and export parts for now (no model yet; full plans for them stay in sections 5 and 6). Money units: one consistent convention, no hard-coded "bn" scaling in formulas. Starts only after the codes increment (R0-R9, v7.2) is complete, checked and pushed.

### What exists (v7.2)

- **Distribution** (prototype tab, deciles across, two scenario groups L and Y) reads Mitigation in **29 rows** only: GDP (`gdp.lcu`), exchange rate (`xr`), population (`pop`), revenue from new policies (`rnew.tot.tot`), residential after-tax prices (`atp.res.<fuel>`, 7), supply costs (`pav.sp.all.<fuel>`, 8), producer prices (`rpn`, 7), electricity prices (`rp.res/ind.ecy`), plus the year row; **24 ScenarioDefinition rows** (its own policy inputs: transfers, targeting) and **Settings** constants. Data tabs: DistMapping, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios.
- **AP**: section 15 of Mitigation (rows `em.*`, `<pol>.tot`, EF_PM data tab); **TCB**: not built (issue I70; plan section 6).
- **Data links** (v6.5-v7.1): Cover status table; macro `UpdateDataTables` builds a Power Query on the data workbook (file or URL) and copies values into the data tabs by column name.

### Decisions (user 2026-10-22: all agreed, with 3 and 5 as below)

1. **Rename** (a full release, NORMS 5): `CPAT-AI-Mitigation-Prototype-v8.0.xlsm`, every script and note `_v8_0`; "prototype" -> "prototype" in texts, documents and deck (`..._Overview_v8.0.pptx`). Modules: `CPAT-AI-Distribution-Prototype-v1.0.xlsm`, `CPAT-AI-AirPollution-Prototype-v0.1.xlsm`, `CPAT-AI-TransportCobenefits-Prototype-v0.1.xlsm`.
2. **Stable copy**: every mitigation build also writes `CPAT-AI-Mitigation_latest.xlsm` at the repository root (it replaces the versioned root copy; the versioned master stays in `mitigation/` and `Old/`). The modules link to it by default (relative path; a GitHub or SharePoint URL as other sources, as the data workbook).
3. **Inputs in Distribution**: a separate first tab `FromMitigation` (user 2026-10-22), in the Mitigation column layout (A-J and the year columns of the groups); the Distribution tab keeps its decile layout and reads only that tab.
4. **Scenarios, no batch** (user 2026-10-22): the modules never interact with the batch runs (RunAllScenarios, StoredOutputs). The end-to-end process runs one scenario at a time: set the scenario in Mitigation's live group, save (`_latest`), update the module from it, read the module's results. The export blocks carry the two groups of Mitigation (baseline, live scenario) and the scenario names.
5. **Section 15 (air pollution) stays in Mitigation**, also after the AP module is designed (user 2026-10-22). **It moves to the end, just before section 19 (user 2026-10-22)** (keeping its number and contents), and `ExportAP` covers section 15 and block 19b as one range, so the 249 pollutant rows are exported without copies. Within Mitigation only `ghg.enrp` (section 14) reads section 15 (`apf.all.all`), already a read further down the sheet; values unchanged. Calculating the pollutants inside the export block instead would mix calculations into a section of plain copies.
6. **One subsection of exports per module** (user question 2026-10-22): 19a Distribution, 19b AP, 19c TCB, each one contiguous block of copy rows with its own defined name; the few rows every module needs (year row, scenario names, GDP, population, exchange rate) are repeated in each block, so a module reads one range. No stored-scenario blocks (no batch interaction).

### Format (both sides the same)

- **Mitigation, new last section 19 "Exports to modules"**: 19a Distribution, 19b AP, 19c TCB. Each row a plain copy of a Mitigation row (`=K<r>` across every group), columns A-C (variable, fuel, sector), H description, I unit, J source ("Mitigation row <r>"), the code column keeps the copied row's code (the module's key; C10 counts codes outside section 19), year columns as Mitigation. One defined name per block (`ExportDistn`, `ExportAP`, `ExportTCB`): the Power Query reads only that range.
- **Module input tab** (`FromMitigation` in every module): the same rows and columns (codes as keys), filled by the module's `UpdateFromMitigation` (Power Query on the latest mitigation workbook, values copied by code, as the data links copy by column name); shipped with the values of the build. Module formulas read only this section (no reference to any mitigation sheet), so the tab in the prototype and the standalone module are the same.
- **Units**: one vocabulary, currency first, scale and price basis as words: `USD`, `USD m`, `USD bn`, `LCU`, `LCU bn`, `USD/GJ`, `USD/kWh`, `USD/tCO2`, each with ` real` or ` nominal` where it matters; never `$` (today: `$/GJ` 1,012 rows beside `USD/...`; `USD per tCO2` beside `USD/tCO2`; `bn, current prices`). Export rows carry a **scale column** (1, 1e3, 1e6, 1e9); the module's input section converts once to base units (LCU, USD, persons) with that column, so no formula body multiplies by `Billion`, `Thousand` or `USDperM` (today: GDP x Billion, population x Thousand, revenue x xr x USDperM in Distribution). Unit labels change text only (values equal; quick check 0 change).

### Steps (each: build, quick check, commit, push; the full check at the end)

- **M0 - rename to prototype, v8.0** (mechanical; full release): files, scripts, texts, `_latest` copy; checks accept the new names. Full check after M2.
- **M1 - units**: unit vocabulary on Mitigation, LiveOutputs, Distribution (labels only); register the old labels as aliases in the units sheet of the codes map.
- **M2 - prototype ready for Distribution**: section 19a (29 rows + year row + scenario names), tab `FromMitigation` before Distribution (with the scale conversion), Distribution re-pointed to it (88 references); its 24 ScenarioDefinition inputs grouped as the module's own scenario inputs. Check: Distribution values unchanged; a new quick-check rule "no module tab reads a Mitigation row outside its input section".
- **M3 - standalone Distribution v1.0**: `build_distribution_v1_0.py` reuses the prototype builder's Distribution functions (one source of truth), writes the module workbook: Cover (data-link status: mitigation workbook and data workbook), ScenarioDefinition (distribution rows only), Distribution (input section + body), its data tabs, Settings subset, VBA (`UpdateFromMitigation`, `UpdateDataTables`, recalculation buttons). Checks: the module fed from `_latest` (Python emulation of the update) equals the prototype's Distribution tab cell for cell, recalculated in LibreOffice; paste test of a scenario group; VBA undefined-name scan.
- **M4 - AP and TCB data parts (v0.1)**: in the prototype, sections 19b/19c and AP and TCB tabs in the Mitigation column layout holding only their input sections. AP inputs: fuel use by sector and fuel (`ener.*`), activity (`gen_mwy`, production), GDP, population, and the EF_PM data link; TCB inputs: road fuel use by fuel, vehicle-km and vehicles by class (`pass`/`fre`/`motor` `.vkt`/`.own`), road fuel prices, GDP, population, and a data-link slot for the legacy TCB parameters (extraction listed in plan section 6). Standalone v0.1 workbooks: Cover + input section + data tabs, no model. Section 15 stays in Mitigation (user 2026-10-22); 19b exports its results.
- **M5 - documents**: NORMS (module rules: exports in section 19, inputs at the top, units, `_latest`), READMEs, CAVEATS, register, documentation and deck (a modules slide).

### Risks

- Power Query cannot read a workbook that is open in Excel elsewhere; it reads the saved values of `_latest` (shipped with values, manual calculation: fine).
- Moving to v8.0 renames every script: done first, in one commit, so later steps do not mix names.

## 10. Plan 5: repository restructure (plan, 2026-10-22; decisions open) (Plan_Restructure)

**Request (user 2026-10-22).** The structure and documentation are out of date: build files mixed with human-readable places, legacy names (`copypaste`, `bugfix_procedure`, the old `distribution`), old and previous prototypes, a separate root `documentation/` folder that confuses. A total rethink.

### What is there (2026-10-22)

| Where | Files | Size | Problem |
|---|---|---|---|
| `excel_ai/mitigation/` (top) | 76 | | 36 scripts, 33 notes, workbook, reports in one folder; every name carries a version (`_v7_0`, `_v7_2`) |
| `.../mitigation/Old/` | 3,701 | 646 MB | every earlier script, note, workbook (69 .xlsm), already in git history |
| `.../presentation/` | 394 | | deck builder and screenshots of every version |
| `excel_ai/old/`, `standalone_initial_prototypes/`, `tecp_and_validation/`, `bugfix_procedure/` (v6.4 variants), `distribution/` (the pre-prototype distribution pipeline) | 131 | 230 MB | earlier prototypes and procedures, not current |
| `documentation/` (root) | 119 | 112 MB | decks and Word outputs, legacy fix plans with their tools and JSON, research PDFs; method notes live elsewhere |
| Root notes | | | `NORMS.md` (120 lines) and `excel_ai/NORMS.md` (509), `CAVEATS.md` (2,811 lines), `Plans.md` (1,500) |
| `.git` | | 966 MB | the binaries of every release |

### Principles

1. **One folder per product, self-contained**: what it is (README), the workbook, its sources, its checks, its documents. A reader finds everything for a model in one place; nothing generated sits beside a hand-written note.
2. **Versions live in git, not in file names**: scripts and notes have stable names (`build.py`, `check_full.py`, `Methods/Prices.md`); a release is a git tag (`mitigation-v8.0`) and a versioned workbook in `releases/`. No `Old/` folders: the history and the tags keep every earlier file. (Replaces NORMS 5's versioned names and `Old/` rule.)
3. **Separate what people read from what machines run**: `docs/` (hand-written and generated documents) vs `src/` (builders, VBA, deck builder) vs `checks/` (check scripts and their latest reports).
4. **Legacy CPAT and archived work in one clearly named place each**: `legacy/` (the reference workbook, codes master, tracker, our cell-level fix plans), `archive/` (earlier prototypes, kept only if still useful; otherwise only in history).
5. **Names say what things are**: prototype (not prototype), module names (mitigation, distribution, air_pollution, transport_cobenefits), no `copypaste`.

### Target layout

```
README.md                 What CPAT-AI is, the products, start here (one page)
AGENTS.md, CLAUDE.md      AI instructions (pointer)
NORMS.md                  One norms file (root + Excel norms merged, current rules only)
CHANGELOG.md              Releases (one line per release, newest first); CAVEATS.md stays the task log
mitigation/               The mitigation prototype
  README.md               What it does, how to use it, how to build and check it
  CPAT-AI-Mitigation_latest.xlsm   Stable name, rewritten by every build (modules link to it)
  releases/               Released workbooks (latest few; earlier ones by git tag)
  docs/                   Quick start, methods (one note per topic), equations, the Word documentation and core deck
  src/                    build.py, vba/CPATScenarios.bas, extract_*.py, deck/ (builder, screenshots)
  checks/                 check_quick.py, check_full.py, check_codes.py, check_paste.py, check_links.py, reports/
distribution/             The standalone distribution module (same sub-layout); its own releases
air_pollution/            Module v0.1 (data import and export only)
transport_cobenefits/     Module v0.1 (data import and export only)
shared/                   Python used by every module: LibreOffice session, VBA embedding, codes map, lint
legacy/                   Legacy CPAT: the reference workbooks, codes master, issue tracker; bug register sources,
                          cell-level fix plans (Word, PDF, JSON, tools) and the bug-fix procedure
data/                     Today's data (all data, converters, tests)
coded/                    Today's coded (Python model)
docs/                     Cross-cutting only: the bug and issue register (Word), decks for audiences, research PDFs, plans
archive/                  (optional) the few earlier prototypes worth keeping visible; everything else only in history
users/
```

The separate root `documentation/` disappears: each product's documents move into its own `docs/`; what concerns all products (the register of legacy bugs, audience decks, research, plans) goes to root `docs/`.

### Mapping (main moves)

| From | To |
|---|---|
| `excel_ai/mitigation/build.py`, `CPATScenarios.bas`, `extract_*`, `make_*` (build side) | `mitigation/src/` (stable names) |
| `check_*_v7_0.py`, `check_report_*.md`, `check_quick_report_*.md` | `mitigation/checks/`, reports in `checks/reports/` |
| `*_Method_v7_0.md`, `QuickStart`, `Equations`, `Formulas`, `DataTabs`, `Transport_*` notes | `mitigation/docs/` (stable names; generated ones marked as generated) |
| `presentation/` | `mitigation/src/deck/` (builder), deck output in `mitigation/docs/` |
| `lo_session`, `lo_run_macro`, `vba_project`, `excel_lint.py`, `xlsb_*` | `shared/` |
| `documentation/*_Documentation_*.docx`, `*_Overview_*.pptx` | `mitigation/docs/` |
| `documentation/*_BugsAndIssues_*.docx`, `excel_ai/legacy/bugfixes/`, `excel_ai/legacy/bugfix_procedure/BugFixProcedure.md`, `LegacyBugFixes`, `Replicated`/`NotReplicated` lists, `issues_register` | `legacy/` (register sources and outputs; the two lists stay linked from the root README) |
| `excel_ai/legacy/workbooks/` | `legacy/workbooks/` |
| `other/research/`, `presentations/`, `more/` | `docs/research/`, `docs/decks/`, `docs/` |
| `Plans.md`, `TODO*.md`, `Codes_Remediation_Plan`, `CPAT_CodesMap` | `docs/plans/` (one file per plan) and `mitigation/TODO.md` |
| `Old/`, `excel_ai/old/`, `standalone_initial_prototypes/`, `tecp_and_validation/`, `distribution/` (pre-prototype pipeline), `bugfix_procedure/` variants | removed from the tree (git tag `archive-2026-10` keeps them); anything still used moves first |
| `data/`, `coded/` | `data/`, `coded/` (paths updated in scripts and tests) |

### Steps (after the v7.2 full check; before the modules, so they are born in the new layout)

- **S0 - inventory and tag**: tag `archive-2026-10`; list every file the current builds, checks and documents read (a script trace), so nothing in use is removed.
- **S1 - move and rename** in one commit per product (git mv keeps history): mitigation, legacy, docs, shared, data, coded; scripts get stable names and a `PATHS` module instead of hard-coded `../..` paths; the full build and quick check run from the new place.
- **S2 - remove** `Old/` folders and the archived folders from the tree.
- **S3 - documents rewritten, not patched**: root README (one page), each product README (use, build, check), one NORMS (current rules only; history of rules to CAVEATS), CHANGELOG from the version log; "prototype" -> "prototype" everywhere (merges with modules step M0, which then needs no file renames).
- **S4 - checks**: quick check, full check, paste and links tests from the new layout; a link check over every Markdown file (no broken relative link).
- **Then** the modules plan (section 9), M1 onwards, in the new layout.

### Decisions (user 2026-10-22; they replace the target layout and decisions above where they differ)

1. **No `documentation/` folder.** Excel documents go into `excel_ai/`; everything else (research, other decks, `more/`) into `other/`.
2. **No `cpat_` prefix**: `excel_ai` -> `excel_ai` (user 2026-10-22: a name with AI; underscore as the other folders), `data` -> `data`, `coded` -> `coded` (every path in scripts, tests, READMEs and NORMS updated).
3. **`excel_ai/` shows three main files at its top**: the latest prototype workbook, the bug-fix documentation (the register of bugs and issues, Word) and the integrated slide deck. The integrated mitigation tool is the special one and is shown there; its sources live in `excel_ai/mitigation/` (src, checks, docs). Modules in `excel_ai/distribution/`, `excel_ai/air_pollution/`, `excel_ai/transport_cobenefits/`; `excel_ai/shared/`, `excel_ai/legacy/` as above.
4. **`BUGS.md` and `ISSUES.md`** (short names, in `excel_ai/`) replace `BUGS.md` and `ISSUES.md`.
5. **History removed**: the repository restarts from one commit of the cleaned tree (966 MB of history dropped; nobody else works on it yet). Dropped outright, no archive (user 2026-10-22).
6. **Versioned and latest copies, both kept**: each main file exists twice with equivalent contents, `..._v8.0` and `..._latest` (workbook, register, deck); the version table (the workbook's version log) is the same in both, and `excel_ai/releases.md` lists every release (version, date, summary, files). The `_latest` copies sit at the top of `excel/`, the versioned copies of every release from v7.2 on in `excel_ai/releases/`. Scripts and notes keep stable names (the git tag of each release marks their state).
7. **When**: as soon as it is safe, i.e. right after the v7.2 full check has passed and v7.2 is on main, with no build or check running; before the modules (plan section 9), so the modules start in the new layout.

### Target layout (as decided)

```
README.md, AGENTS.md, CLAUDE.md, NORMS.md (one, merged), CAVEATS.md
excel_ai/
  README.md                                   Start here
  CPAT-AI-Mitigation-Prototype_latest.xlsm    The integrated tool (stable name; modules link to it)
  CPAT-AI_BugsAndIssues_latest.docx           Bug-fix documentation: every legacy bug and issue, fix plans
  CPAT-AI_Overview_latest.pptx                The integrated slide deck
  BUGS.md, ISSUES.md                          The two short lists (generated)
  releases.md, releases/                      Every release from v7.2: the three files with _v<n>, one table
  mitigation/   src/ (build, VBA, extractors, deck builder), checks/ (and reports/), docs/ (quick start,
                methods, equations, formulas, the Word documentation)
  distribution/, air_pollution/, transport_cobenefits/   Modules (same sub-layout, own releases)
  shared/       LibreOffice session, VBA embedding, codes map, lint
  legacy/       Legacy CPAT workbooks, codes master, tracker; cell-level fix plans (Word, PDF, JSON, tools);
                bug-fix procedure; register sources
  plans/        Plans and TODOs (one file per plan)
data/           (was data)
coded/          (was coded)
other/          Research PDFs, other decks (AI and climate fiscal tools), more/
users/
```

### Documents and scripts after the restructure (user 2026-10-22)

- **One Word bug-fix document**: the register (`CPAT-AI_BugsAndIssues_latest.docx`, with every cell-level fix plan inside); the five separate fix-plan Word files and their PDFs are dropped (their JSON and tools stay in `legacy/` as sources). **The register spreadsheet stays** (one filterable table). `BUGS.md` and `ISSUES.md` stay; `LegacyBugFixes`, `NotReplicated`, `Replicated` copies and `BugFixProcedure.md` go (inside the register).
- **Method notes merged, 13 -> 6**: Prices; Power; Transport; Emissions; ETS; Macro and results (Distribution's note to the Distribution module).
- **Main documentation: simple and well structured, not everything in** (user: "a firehose of information; we humans can't cope"). Target about 20 pages: 1. what the tool is and what it answers (1 page); 2. quick start (2 pages); 3. how it works: one short section per block (policies, prices, demand, power, transport, revenues, emissions, macro) with the few key equations and a pointer to its method note (about 1 page each); 4. results and the dashboard (2 pages); 5. limits and differences from legacy: a pointer to the register, no lists. Out of it: every formula (`Formulas` stays a generated reference), legacy surveys, version history, bug lists, plans.
- **Scripts**: stable names; one `make_documents.py` entry for every document; one-off extractors and tools to `legacy/tools/`; about 20 scripts for build, checks and documents.
- **Two Word documents for mitigation** (user 2026-10-22), both generated from Markdown notes in the repository, in `excel_ai/mitigation/`: the **main documentation** (about 20 pages, as above; each block ends with "details: Methods, chapter X") and **Methods** (the 6 merged method notes as chapters, the full equations as an appendix; for someone checking or changing the model).
