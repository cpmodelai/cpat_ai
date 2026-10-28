# Excel-AI: the CPAT prototypes in Excel

## The main files

| File | What it is |
|---|---|
| `CPAT-AI-Mitigation-Prototype_latest.xlsm` | **The integrated prototype** (mitigation, with the distribution tab): open it in Excel 365, macros on |
| `CPAT-AI-Distribution-Prototype_latest.xlsm` | **The standalone distribution module**: household effects by decile of a mitigation scenario; its Cover links to the prototype (button Update from Mitigation) |
| `CPAT-AI_BugsAndIssues_latest.docx` | **The bug-fix register**: every legacy CPAT bug with its cell-level fix plan (cell references of legacy CPAT 1.0pre_465) and its status in legacy, the issues, the departures from legacy |
| `CPAT-AI_Overview_latest.pptx` | **The slide deck**: status, how to use it, results |
| [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md) | The two short lists: legacy bugs (all fixed in the prototype; column "In legacy 465") and legacy issues (replicated, tracked) |

## Folders

| Folder | Contents |
|---|---|
| [`mitigation/`](mitigation/README.md) | The prototype's sources: builder, VBA, checks, method notes, the Word documentation |
| [`distribution/`](distribution/README.md) | The distribution module's sources: builder (cuts the module from the prototype), VBA, check |
| [`air_pollution/`](air_pollution/README.md) | Recovered standalone v0.3 scaffold, public reference tables, equation inventory and Python comparison; calculations and numerical regression remain open |
| `releases/` | Every released workbook since v7.2 (`_v<n>` copies; the files above are the `_latest` copies) |
| `legacy/` | Legacy CPAT: the reference workbooks, codes master and tracker (`workbooks/`); the fix-plan sources and tools (`bugfixes/`, with the 456 to 465 row map); the bug-fix procedure; the register as JSON |
| [`bugsfixed/`](bugsfixed/README.md) | The latest legacy file (CPAT 1.0pre_465) and the check of the bugs the CPAT team fixed in it |
| [`plans/`](plans/TODO.md) | The to-do list and the plans |
| `shared/`, `templates/` | Code and templates used by every builder |

Rules: [`../NORMS.md`](../NORMS.md).
