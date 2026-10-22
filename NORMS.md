# CPAT-AI Norms (whole repository)

Rules for **every** task in this repository, Excel or Python. Project-specific norms live with each project:

| Project | Norms | Open work |
|---|---|---|
| Excel-AI (`excel_ai/`) | [`excel_ai/NORMS.md`](excel_ai/NORMS.md): columns, visual style guide (colours, fonts, borders, headings, white space), formulas, MTInputs, versioning | [`excel_ai/plans/TODO.md`](excel_ai/plans/TODO.md) |
| Coded CPAT (`coded/`) | [`coded/README.md`](coded/README.md): layout, conventions, tests | [`coded/TODO.md`](coded/TODO.md) |
| Data (`data/`, all data of both projects) | Section 8 below; [`data/README.md`](data/README.md): folders, formats, conversion scripts | the data items of the two TODOs |

Sections 1-5 (Excel) moved to `excel_ai/NORMS.md` on 2026-10-13; the numbering of sections 6 and 7 below is kept so existing references stay valid.

## Excel files written by code (every project)

Every .xlsx/.xlsm a script writes, in any project, is checked with `python excel_ai/shared/excel_lint.py <file>` before it is shipped or committed, and the builder fails on a problem. Excel repairs files that openpyxl and LibreOffice accept; the causes found so far and the procedure when Excel still repairs a file are in [`excel_ai/NORMS.md`](excel_ai/NORMS.md) section 3g.

## 6. Task completion: caveats log and bookkeeping

Applies to **every** task (Excel, Python, data, documentation). A task is not finished until it is logged. When a task is done:

1. **Add an entry to [`CAVEATS.md`](CAVEATS.md) (repo root).** This is the single record of completed work. Use the template at the top of that file and record:
   - **Task** - what was asked and what was done, with the task id or version (e.g. `v2.3`);
   - **Inputs** - files, sheets/ranges, data sources, specs and prior versions used;
   - **Outputs** - files created or changed (paths), version numbers, documents updated;
   - **Caveats** - placeholders, assumptions, known gaps, deferred items, regression differences that were explained rather than zero, decisions still open; anything the next person must know before building on the result.

   Newest entry at the bottom. Earlier entries may be edited to keep the log accurate (fix stale paths, mark a caveat resolved with the date and where it was resolved, correct a mistake), but the record of a task is not deleted. Keep entries short and point to the task spec, report or yaml notes for detail.
2. **Workbook version log** (Excel work: [`excel_ai/NORMS.md`](excel_ai/NORMS.md) section 5). Add the version-log row (version, date, one-line description, max abs regression diff) in the workbook's `Settings`/`ReadMe` tab. The `CAVEATS.md` entry and the version-log row must agree.
3. **Bugs and issues.** Never replicate a legacy bug; replicate every legacy issue and track it ([`excel_ai/NORMS.md`](excel_ai/NORMS.md) section 0). Every bug found and every issue met goes in the register, so that it shows in [`excel_ai/BUGS.md`](excel_ai/BUGS.md) or [`excel_ai/ISSUES.md`](excel_ai/ISSUES.md).
4. **Queue.** Tick the item in the project TODO ([`excel_ai/plans/TODO.md`](excel_ai/plans/TODO.md) or [`coded/TODO.md`](coded/TODO.md)). Follow-up work the task generated goes in as a new `TODO.md` item, not only as a caveat.
5. **Specs.** When a task applies a versioned spec (e.g. a method note `..._v2_3.md`), retarget it as a new version rather than editing it in place (same rule as `excel_ai/NORMS.md` section 5 for workbooks).
6. **No commit unless asked.** Leave changes in the working tree; the user decides what to commit.

`CAVEATS.md` summarises and points; detail stays where it is produced - the task spec, the workbook version log, and `excel_ai/distribution/LESSONS_LEARNED.md` for the LAMBDA/VBA workbook. The per-task conventions in `excel_ai/plans/TODO.md` (builders via Excel COM, codes/source/confidence for every new input, `Settings` version-log row, `Check`-sheet regression) remain in force and are the operational version of `excel_ai/NORMS.md` sections 3-5.


## 6b. Norms follow the lessons: update them in the same task (user rule 2026-10-22)

Every bug, repair prompt, compile error or false check that has a cause another file or task could repeat ends with a
norm, not only a fix. In the same task that fixes it:

1. **Name the class, not the instance:** what kind of mistake it was (e.g. "an Office-library constant in a project
   that references only Excel", not "msoTrue in StyleSeries").
2. **Add or sharpen the norm** in the project's NORMS (Excel: `excel_ai/NORMS.md`; repository-wide: here), with the
   date and the version or file where it was found. If a norm already covered it, say why it was missed and sharpen
   the wording or the check.
3. **Add the check** that would have caught it (a build assertion, `check_quick`, `excel_lint.py`, a test): the
   pattern, not the one formula or line (`excel_ai/NORMS.md` 3b.6). Show that the check fails on the old file.
4. **Look back:** search the current files for other instances of the class and fix them in the same task.
5. **Register it:** add a row to the lessons register of the project (Excel: `excel_ai/NORMS.md` section 3j,
   LAMBDA and VBA) and name the norm in the task's `CAVEATS.md` entry ("Norm: ...").
6. **A user report counts the same as a failing check:** when the user finds a problem the checks did not, the norm
   and the check are part of the fix.

## 7. Methodology and version notes are always different documents

A **methodology document** describes the method as it is now: equations, inputs, conventions, results and open issues. It is written for a reader who has never seen an earlier version, so it contains no change history: no "v0.3 changes (vs v0.2)", no "was X, now Y", no version log, no "superseded" commentary and no per-version result columns.

Version and change history goes in **separate version notes**, never in the methodology:

| What | Where |
|---|---|
| What changed between versions, and why | The version notes next to the document (e.g. `VersionNotes_<name>.md`), the workbook's `Settings` / `ReadMe` version log, and the `CAVEATS.md` entry |
| Caveats and decisions still open | `CAVEATS.md` and the document's own "Open issues" section (current state only) |
| Superseded copies | The relevant `Old/` folder |

When a task changes the method, rewrite the affected methodology text to describe the new state, and put the delta in the version notes and `CAVEATS.md`. A methodology that contains a version log or before/after comparisons is non-compliant: move that content out when you next touch the document.


## 8. Data: everything in `data/`; the legacy workbook and the dummy legacy data

**All data live in the root folder [`data/`](data/README.md)** (user 2026-10-20), in subfolders by kind, with the scripts that convert them:

| Folder | What it holds |
|---|---|
| `data/dummy/` | The Coded CPAT inputs, dummy version (CSVs); `coded/config.py` reads it by default |
| `data/workbooks/` | The data workbook of each version: `CPAT_Data_<version>_python.xlsx` (Python format) and `CPAT_Data_<version>_cpat.xlsx` (CPAT format, legacy sheet layout) |
| `data/legacy_dummy/` | The dummy legacy-data files (below) |
| `data/mvp_legacy_extracts/` | The legacy extracts and derived tables the mitigation MVP is built from |
| `data/distribution/` | The distribution data pipeline (`data_bymodule`, `data_tabular`, `data_standardized`, the `_regenerated` checks) |
| `data/scripts/`, `data/tests/` | The conversion scripts (`export_to_legacy.py`, `build_data_workbook.py`, `convert_data_workbook.py`) and their tests |

Rules:

- **New data go in `data/`**, in the subfolder of their kind (or a new subfolder, added to the table above and to `data/README.md`). Project folders hold code, documents and generated workbooks of the models, not data; code reads the data from `data/` by a path relative to the repository (never a copy).
- **Exceptions:** the legacy workbook and the CPAT team's reference files stay in `excel_ai/legacy/workbooks/` (the reference model, not data); test fixtures stay with their tests (`coded/cpat_testing/model/data_expected/`).
- **Only dummy or public data are committed.** Real (proprietary) data stay outside the repository (`REAL_DATA_PATH`, the restricted SharePoint site); `CPAT_Data_*.xlsx` and `CPAT_LegacyData*.xlsx` are git-ignored except the dummy files.
- **One change, every format.** When `data/dummy/` changes, rebuild in the same task the workbooks (`build_data_workbook.py`, then `convert_data_workbook.py to-cpat`) and the dummy legacy-data files, run `pytest tests` in `data/`, and log it in `CAVEATS.md`.

`excel_ai/legacy/workbooks/` holds the legacy workbook and the team's reference files:

| File | What it is | Rule |
|---|---|---|
| `CPAT 1.0pre_456_NoPropData.xlsb` | The legacy CPAT workbook with the proprietary data stripped | Read-only ground truth. Never edit or re-save it; work on a copy in a scratch folder |
| `CPAT 1.0pre_459_NoPropData.xlsb` | The updated legacy workbook (user 2026-10-18; a few bugs fixed by the CPAT team) | Read-only, as the 456 file; the register is keyed to 456 until it is reconciled |
| `CPATMasterProcessesCodesAndDefaults.xlsx` | The CPAT team's master list of codes, processes and defaults | Read-only reference (may be inaccurate in places; an alignment exercise is planned) |
| `Tracking issues.xlsx` | The CPAT team's bug and issue tracker | **Editable** (user 2026-10-18): add rows and columns, keep the team's content, use our codes (L, D, I, DI, M, LD); sheet BUGSandISSUES and the code columns are written by `excel_ai/mitigation/update_tracker_v<version>.py` at every release |

`data/legacy_dummy/` holds the dummy legacy data:

| File | What it is | Rule |
|---|---|---|
| `CPAT_LegacyData_dummy.xlsx` | Dummy (non-proprietary) data in the legacy layout: tabs `EnergyCons`, `Prices_dom`, `HHSurvey`, `IO_GTAP`, with the legacy sheet names, header rows and cell positions | Master of the dummy legacy data |
| `CPAT_LegacyData_dummy_csv/` | The same four tabs as CSVs (`<sheet>.csv`), cell for cell | Must equal the workbook |
| `CPAT_LegacyData_dummy_ReadMe.md` | Data range of each tab (paste with Paste Special > Values at the same cell of the legacy sheet) and the legacy columns the dummy data do not have | Must describe the workbook as it is |

They are written from the Coded CPAT dummy data by [`data/scripts/export_to_legacy.py`](data/README.md):

| Coded CPAT file (`data/dummy/`) | Legacy tab |
|---|---|
| `energy_consumption.csv` | `EnergyCons` |
| `prices_dom.csv` | `Prices_dom` |
| `distn_hh_survey.csv` | `HHSurvey` |
| `distn_io_gtap.csv` | `IO_GTAP` |

1. **Consistency.** The workbook, the CSV folder and these four `data/dummy/` files hold the same data. Check by re-running the export into a scratch folder (`python scripts/export_to_legacy.py --data dummy --out <scratch>/x.xlsx --csv-dir <scratch>/x_csv`, from `data/`) and comparing it with the committed files; `data/tests/test_export_to_legacy.py` tests the same.
2. **The workbook is the master.** If the files differ, change the CSVs in `data/dummy/` to match `CPAT_LegacyData_dummy.xlsx`, then re-run the export so that the CSV folder and ReadMe are rewritten from them, and check that the re-run workbook equals the committed one.
3. **When the dummy data change** (a new country, a new column, new values), regenerate all three dummy legacy-data files in the same task and log it in `CAVEATS.md`.
4. **No proprietary data.** Only dummy data are committed. An export of real data (`--data` pointing at `REAL_DATA_PATH`) stays out of the repository.
5. **The dummy data are not legacy values.** The mitigation tables (`EnergyCons`, `Prices_dom`) are randomised and serve as a format sample; do not compare them with the Egypt values cached in the NoPropData workbook. `HHSurvey` and `IO_GTAP` reproduce the NoPropData workbook (Egypt) cell for cell.
