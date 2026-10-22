# Mitigation prototype: sources

The sources of `../CPAT-AI-Mitigation-Prototype_latest.xlsm`: the builder, the VBA module, the checks and the documents. Rules: [`../../NORMS.md`](../../NORMS.md). Open work: [`../plans/TODO.md`](../plans/TODO.md).

## Read

| File | What it is |
|---|---|
| `CPAT-AI-Mitigation_Documentation.docx` | **The short documentation**: what it is, quick start, how it works, results, limits (from `docs/Documentation.md`) |
| `CPAT-AI-Mitigation_Methods.docx` | **Methods**: one chapter per block (prices, power, transport, emissions, ETS, macro and results, distribution); equations and data tabs as appendices (from `docs/methods/`, `Equations.md`) |
| `Formulas.md` | Every workbook formula, generated (implementation reference) |
| `check_report.md`, `check_quick_report.md` | The last full check and quick check |

## Build and check

Python 3, openpyxl, LibreOffice (no Excel needed).

```
python build.py                # writes ../releases/CPAT-AI-Mitigation-Prototype_v<version>.xlsm and ../..._latest.xlsm (about 8 min)
QUICK=1 python build.py        # quick build, no batch (CPAT-AI-Mitigation-Prototype_quick.xlsx)
python check_quick.py          # after every change (about 2 min)
python check_paste.py <file>   # copy-paste test, at every release (about 3.5 min)
python check_full.py           # full check, at a milestone (several hours with the macro tests)
python make_documentation.py   # the Word documents, the register and its spreadsheet, BUGS.md and ISSUES.md
python presentation/make_screenshots.py && node presentation/build_deck.js   # the deck
```

## Scripts

| Group | Files |
|---|---|
| Build | `build.py` (version in `VERSION`, also `version.json`), `CPATScenarios.bas` (VBA), `vba_project.py`, `extract_data.py`, `tabs.json` |
| Checks | `check_quick.py`, `check_full.py`, `check_paste.py`, `check_links.py`, `check_allcountry.py`; independent recalculations `power_model_ref.py`, `transport_model_ref.py`, `distribution_ref.py`; LibreOffice `lo_session.py`, `lo_run_macro.py`; `legacy_compare.py` |
| Register and documents | `issues_register.py` (the register's data), `make_bugfix_book.py`, `make_bugs_issues_sheet.py`, `make_legacy_fixes.py`, `make_replication_lists.py`, `make_docs.py`, `make_equations.py`, `make_documentation.py`, `update_tracker.py` |
| Deck | `presentation/build_deck.js`, `presentation/make_screenshots.py`, `presentation/img/` |
| Tools | `ets_goalseek.py` (the user's ETS goal-seek test), `make_variants.py`, `extract_*.py` (legacy extracts), `update_prices_egypt.py` |
