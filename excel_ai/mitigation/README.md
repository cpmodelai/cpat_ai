# Mitigation prototype: sources

The sources of the mitigation prototype: every version in [`releases/`](releases/) (`CPAT-AI-Mitigation-Prototype_v<version>.xlsm`), the permalinked copy in [`../active_workbooks/`](../active_workbooks/) (`CPAT-AI-Mitigation-Prototype_latest.xlsm`, the copy people open and other modules link to). Rules: [`../core/NORMS.md`](../core/NORMS.md). Open work: [`../core/TODO.md`](../core/TODO.md).

## Read

| File | What it is |
|---|---|
| `docs/CPAT-AI-Mitigation_Documentation.docx` | **The short documentation**: what it is, quick start, how it works, results, limits (from `docs/Documentation.md`) |
| `docs/CPAT-AI-Mitigation_Methods.docx` | **Methods**: one chapter per block (prices, power, transport, emissions, ETS, macro and results, distribution); equations and data tabs as appendices (from `docs/methods/`, `docs/Equations.md`) |
| `docs/Formulas.md` | Every workbook formula, generated (implementation reference) |
| `checks/check_report.md`, `checks/check_quick_report.md` | The last full check and quick check |

## Build and check

Python 3, openpyxl, LibreOffice (no Excel needed). Run from `excel_ai/mitigation/`.

```
python build.py                       # releases/CPAT-AI-Mitigation-Prototype_v<version>.xlsm and ../active_workbooks/..._latest.xlsm (about 8 min)
QUICK=1 python build.py               # quick build, no batch (CPAT-AI-Mitigation-Prototype_quick.xlsx)
python checks/check_quick.py          # after every change (about 2 min)
python checks/check_paste.py <file>   # copy-paste test, at every release (about 3.5 min)
python checks/check_full.py           # full check, at a milestone (several hours with the macro tests)
python docs/make_documentation.py     # Legacy_CPAT_Bugs, the tracker, the codes map, the Word documentation, core/BUGS.md and core/ISSUES.md
python docs/presentation/make_screenshots.py && node docs/presentation/build_deck.js   # the deck
```

## Folders and scripts

Every script starts by importing `../core/tools/xlpaths.py`, which puts every Excel-AI code folder and `data/scripts/` on the path; scripts in the subfolders use `mitigation/` as their base folder (`HERE`).

| Folder | Files |
|---|---|
| (top) | `build.py` (version in `VERSION`, also `version.json`), `CPATScenarios.bas` (VBA), `vba_project.py`, `names.tsv`, `tabs.json`, `excel_reserved_names.txt`, `make_variants.py` |
| `checks/` | `check_quick.py`, `check_full.py`, `check_paste.py`, `check_links.py`, `check_allcountry.py`; independent recalculations `power_model_ref.py`, `transport_model_ref.py`, `distribution_ref.py`; LibreOffice `lo_session.py`, `lo_run_macro.py`; `legacy_compare.py`; the reports |
| `extract/` | `extract_*.py` (from the legacy workbook and the data edition), `update_prices_egypt.py`, `ra_goalseek.py` (range-anxiety fit), `ets_goalseek.py` |
| `docs/` | `Documentation.md`, `methods/`, `Equations*.md`, `Formulas.md`, the Word documents and their scripts (`make_docs.py`, `make_equations.py`, `make_documentation.py`, `make_transport_doc.py`, `make_codesmap.py`), `presentation/` (the deck) |
| `releases/` | Every version of the workbook, and the older decks |
| elsewhere | The register and its documents: `../bugs_and_legacy/register/` (`issues_register.py`, `register.py`, `make_legacy_fixes.py`, `make_bugfix_book.py`, `make_tracker.py`, `make_replication_lists.py`); release layout and lint: `../core/tools/` |
