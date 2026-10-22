# Excel-AI: the CPAT prototypes in Excel

## The main files

| File | What it is |
|---|---|
| `CPAT-AI-Mitigation-MVP-v7.2.xlsm` | **The integrated prototype** (mitigation, with the distribution tab): open it in Excel 365, macros on |
| `CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.2.docx` | **The bug-fix register**: every legacy CPAT bug with its cell-level fix plan, the issues, the departures from legacy |
| `CPAT-AI-Mitigation-MVP_Overview_v7.2.pptx` | **The slide deck**: status, how to use it, results |
| [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md) | The two short lists: legacy bugs (all fixed) and legacy issues (replicated, tracked) |

## Folders

| Folder | Contents |
|---|---|
| [`mitigation/`](mitigation/README.md) | The prototype's sources: builder, VBA, checks, method notes, the Word documentation |
| `releases/` | Every released workbook since v7.2 |
| `legacy/` | Legacy CPAT: the reference workbooks, codes master and tracker (`workbooks/`); the fix-plan sources and tools (`bugfixes/`); the bug-fix procedure; the register as JSON |
| [`plans/`](plans/TODO.md) | The to-do list and the plans |
| `shared/`, `templates/` | Code and templates used by every builder |

Rules: [`NORMS.md`](NORMS.md) (Excel) and [`../NORMS.md`](../NORMS.md) (every task).
