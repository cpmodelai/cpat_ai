# data - the CPAT data: editions, the generic catalogue and legacy shell, the scripts

All data live here (`excel_ai/core/NORMS.md` section 8), as **editions**: folders of the same structure, each one data set (public perturbed here; real in the private data repository). What does not depend on the data (the scripts, the tests, the table catalogue, the legacy model without its proprietary data, the scenario sets) is generic and sits beside the editions. Restructured 2026-10-30 (user).

## Layout

```
data/
├── README.md
├── editions.csv              the registry of every edition (below)
├── catalog.csv               generic catalogue of every data table: tidy file, Excel tab, proprietary, provenance,
│                             the legacy "Data sources" columns (scripts/build_catalog.py)
├── legacy/
│   └── CPAT 1.0pre_465_Shell.xlsb     the legacy model, its six proprietary tabs empty (all else filled)
├── inputs/
│   └── scenarios_excel_ai.csv         scenario sets: MTInputs rows x scenarios (not data-dependent)
├── scripts/                  generic; each takes --edition (default: the default edition)
│   ├── editions.py           the registry and the paths inside an edition
│   ├── tidy_convert.py       tidy <-> xlsx (to-xlsx, to-tidy, check)
│   ├── tidy_specs.py         what each legacy table becomes in tidy form
│   ├── tidy_blocks.py        the legacy tabs kept at their cell addresses, and their data blocks
│   ├── legacy_csv.py         an edition's tidy/ in the legacy CSV form, in a build cache, for Excel-AI's scripts
│   ├── build_catalog.py      writes catalog.csv
│   ├── build_edition.py      writes an edition's EDITION.json and data_sources.csv
│   ├── perturb_proprietary.py   makes a public edition: perturbs the proprietary tables (+-3%, identities kept)
│   └── legacy_proprietary.py    shell: empties the six tabs; fill: the shell filled from an edition's tidy/
├── tests/
│   └── test_tidy_roundtrip.py   runs on every edition present
│
└── Public01/                 an edition (every edition has this structure)
    ├── EDITION.json          manifest: edition, type, based_on, legacy base, version, status, perturbation, checksums
    ├── data_sources.csv      catalog.csv + the column values (what the values are in this edition)
    ├── tidy/                 the source of truth: one CSV per table, plus _manifest.csv and _layout/
    ├── legacy_xlsx/
    │   └── CPAT_LegacyData.xlsx       the tables in the legacy layout (written from tidy/, never edited by hand)
    ├── legacy/
    │   └── CPAT 1.0pre_465_Public01.xlsb   the legacy shell filled with this edition's six proprietary tables
    └── inputs/
        └── baseline_co2.csv  inputs that depend on the data (Excel-AI's stored scenario-1 values)
```

## Editions

`editions.csv` is the record of every data set:

| Column | Content |
|---|---|
| `edition` | the name and folder: `<Type><NN>`, e.g. `Public01`, `Public02`, `Full01` |
| `type` | `public-perturbed` (public tables; the proprietary tables perturbed; may be shared) or `full-real` (every table with its real values; never shared, never in this repository) |
| `location` | `data/Public01`, or where it lives (the private data repository) |
| `based_on` | the edition it was made from (Public01: the real data, Full01) |
| `legacy_base` | the legacy version the tables follow (`CPAT 1.0pre_465`) |
| `version` | the date of the last change, `YYYY.MM.DD` |
| `status` | `planned`, `current`, `frozen`, `retired` |
| `default` | `yes` for the edition the models read when none is given |
| `notes` | what is in it |

| Edition | Type | Where | Status |
|---|---|---|---|
| `Public01` | public-perturbed | `data/Public01` | current, default |
| `Full01` | full-real | the private data repository | planned (not used here) |

Rules (user 2026-10-30):

- **Same structure in every edition**, same file names; models switch editions by path only.
- **A new number is new data** (a new legacy base, a new perturbation, new countries); `version` records the smaller corrections within an edition.
- **Frozen once released:** an edition that a released model links to is `frozen`; changes then go into the next number.
- **Choosing an edition:** scripts `--edition Public01`, or the environment variable `CPAT_DATA_EDITION`, else the default row. An edition outside this repository is found through `CPAT_DATA_<EDITION>` (e.g. `CPAT_DATA_FULL01=/path/to/Full01`). Coded CPAT: `cpat_model.settings.edition()`; `database='full'` reads `FULL_DATA_PATH` (the tidy folder of Full01). Excel-AI: the data source "Dummy - GitHub" reads `main/data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx`; the local search looks in `<repo>/data/Public01/legacy_xlsx/`.
- **Models print the edition and version on their outputs** (to do: Excel-AI and Coded CPAT), so a result says which data made it.
- **Git tags:** each data release is tagged with edition and version (e.g. `data-Public01-2026.10.30`).

### The manifest and the values column

`<edition>/EDITION.json` (`scripts/build_edition.py`) holds the edition's row of `editions.csv`, the perturbation (public editions: scripts, delta, date; factors not stored) and a SHA-256 checksum of every file of the edition. `<edition>/data_sources.csv` is `catalog.csv` plus the column `values`:

| `values` | Meaning |
|---|---|
| `real` | the real values (full-real editions only) |
| `public` | public data, as published |
| `perturbed` | a proprietary table, or a copy of one, perturbed |
| `derived-real` | computed from the real data before the perturbation (model outputs, fits): to be rebuilt |

Public01: 278 public, 10 perturbed, 6 derived-real. The data tests fail on a stale manifest, on any edition here that is not `public-perturbed`, on a table marked `real`, and on a proprietary table not `perturbed`.

## The catalogue `catalog.csv`

One row per tidy table (from the specs), then one per data tab of the legacy workbook that has no tidy table yet, then one per entry of the legacy "Data sources" tab that names no tab. Columns:

| Column | Content |
|---|---|
| `tidy_file` | the CSV in `<edition>/tidy/` (blank: not in tidy yet) |
| `excel_tab` | the tab in `<edition>/legacy_xlsx/CPAT_LegacyData.xlsx` (= the legacy tab name; blank: no tab) |
| `proprietary` | `proprietary` or `non-proprietary` (only these two) |
| `provenance` | where the table comes from: legacy version and place, or what it was derived from |
| `status` | `tidy + xlsx`, `legacy 465 only (not in tidy yet)`, `Data sources entry only (no tab)` |
| `data_sources_entry` | the name in column C of the legacy "Data sources" tab (old names mapped to the tabs, e.g. ECPPC -> ECP, ETS+LTS; Popn -> UNPop; Tran -> Transport1-3) |
| `module`, `topic`, `data_category`, `data_source`, `link`, `legacy_notes` | the legacy "Data sources" tab, as it is (`data_category` keeps the legacy wording) |

Legacy tabs that hold no input data are not listed: Data sources, MTOutputs, Glossary, Notes, VersionTracker.

## The six proprietary tables

Confirmed by the user (2026-10-30); every other table is non-proprietary, whatever the legacy "Data sources" tab says (it calls WHOCooking proprietary: here it is non-proprietary). A table derived from a proprietary one is non-proprietary, with the derivation in `provenance`.

| Legacy tab | Tidy table | Note |
|---|---|---|
| Balances | `energy_balances.csv` | IEA energy balances |
| EnergyCons | `energy_consumption.csv` | derived from Balances, listed separately |
| Prices_dom | `prices_domestic.csv` | domestic fuel prices |
| IO_GTAP | `io_gtap.csv` | GTAP input-output |
| HHSurvey | `hh_survey.csv` | household survey |
| Tran_Scatter | `tran_scatter.csv` | IRF World Road Statistics |

**The legacy shell** (`legacy/CPAT 1.0pre_465_Shell.xlsb`) has these six tabs empty below their header rows, and every other tab filled: the person updating the data clears or fills six tables only. An edition's copy is the shell filled from the edition's tidy tables (`scripts/legacy_proprietary.py fill`), one row per tidy row below the header, columns by the legacy header (legacy columns the tidy table has not, such as the Prices_dom Info columns, stay empty).

**Public01's values are perturbed, not real.** `scripts/perturb_proprietary.py` multiplied the Egypt rows of the proprietary tables by random factors within +-3%, keeping their identities (energy balances balance by fuel, the totals add up, energy consumption follows the balances, retail prices are supply cost plus taxes with VAT, each household's budget shares keep their total, each GTAP sector's levels keep their ratios), and recomputed Excel-AI's copies of them (`xai_energy_balance`, `xai_energy_use`, `xai_power_demand`). The factors come from the system's random source and are not stored. Not perturbed (`derived-real`): model outputs computed from the real data (`xai_legacy_cached_baseline`, the `xai_legacy_*_reference` tables, `xai_legacy_mtoutputs_465`, `range_anxiety_fit`, `inputs/baseline_co2.csv`) and the formula results cached in the legacy workbooks until Excel recalculates and saves them. The git history still holds the real values (to be purged).

## Scripts

Run from the repository root (`--edition` defaults to the default edition):

```bash
python data/scripts/tidy_convert.py to-xlsx --tidy data/Public01/tidy --out data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx
python data/scripts/tidy_convert.py check   --tidy data/Public01/tidy
python data/scripts/legacy_proprietary.py fill --edition Public01     # the shell + Public01's six tables
python data/scripts/build_catalog.py                                  # after adding a table
python data/scripts/build_edition.py --edition Public01               # after any change of the edition
python data/scripts/legacy_csv.py                                     # (re)write the legacy-form cache
python data/scripts/legacy_csv.py --save                              # the cache -> tidy/, after a script wrote into it
python -m pytest data/tests
```

**Making a new public edition** from real data: copy the real edition's folder to `data/Public02/` (on a machine that may hold real data; never commit it before the next step), add its row to `editions.csv`, then `perturb_proprietary.py --edition Public02`, `tidy_convert.py to-xlsx`, `legacy_proprietary.py fill --edition Public02`, `build_edition.py --edition Public02`, the tests.

- **After changing an edition's `tidy/`:** rewrite its workbook (`to-xlsx`) and its legacy copy (`fill`, if a proprietary table changed), run `build_catalog.py` if a table was added, then `build_edition.py`, then the tests.
- **Round trip:** tidy -> xlsx -> tidy gives back every value: numbers to 16 significant digits (openpyxl), whole numbers lose a trailing `.0`.
- **Importing a workbook** (`to-tidy --xlsx <file> --out <folder>`): into a scratch folder, then copy the tables wanted into `tidy/`. It is lossy where the workbook is (the 16 digits; the formula flags of the cells tabs and `_layout/prices_dom_header.csv` are not in the workbook).
- **Adding data in tidy form:** a row with a new key (a new country) is written after the rows the layout knows, with the legacy case of the country key. A new column of a melted header (a new year) stops the conversion.
- **Scripts that write tables** (Excel-AI `extract_*.py`, `update_prices_egypt.py`, `legacy_compare.py`, `ra_goalseek.py`, Coded CPAT `extract_excel_ai.py`) write into the cache (`.buildcache/legacy_csv/<edition>/`, git-ignored); `legacy_csv.py --save` puts the result into the edition's `tidy/`.
- **Legacy workbooks:** the scripts edit the `.xlsb` records directly (other parts stay byte for byte); the sheets' binary row indexes are dropped and the workbook recalculates fully when Excel opens it. The Excel-AI tools read the shell (`extract_legacy_tables.py`, which reads the proprietary tabs, reads the edition's copy).
- `build_catalog.py` needs `pyxlsb`. Every workbook a script writes passes `excel_ai/core/tools/excel_lint.py`.

## Known gaps

- Not in tidy yet (status `legacy 465 only`): MTInputs, CBAM, WDI, SSPs, OtherPowerUse, CalVal, Meta_mit, Mapping, Tran_Elast, and the 465 versions of the air-pollution tabs (WB, GBD, IHME, ILO, ExposureCoefs, IF PP, ConcMat, Air_Data, Air_meta: tidy holds their 459 versions, `ap459_*`).
- The `xai_*` tables are Excel-AI's derived tables kept as they are (not melted, no legacy layout).
- Some tidy tables come from older legacy versions or from Excel-AI, not 465 (see `provenance`: HHSurvey and HH_Elast from 456; FromAirPollution, FromTransportCB, RangeAnxietyFit from Excel-AI).
- `IO_GTAP`, `ASPIRE` and `WHOCooking` are cut to Egypt although 465 has every country; Prices_dom has Egypt 2019-2024.
- The released prototypes up to 1.0.4 (`excel_ai/mitigation/releases/`) still link `main/data/workbooks/CPAT_Data_dummy_python.xlsx`; the builder links `main/data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx` from 1.1.0. The user's price file read by `update_prices_egypt.py` is an argument (archived: git 2a446e4).
