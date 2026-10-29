# AGENTS.md - instructions for any AI working in this repo

Tool-neutral entry point (Claude, Codex, Gemini, Copilot, Cursor, ...). `CLAUDE.md` just points here. This file only routes you to the existing documentation; the rules live there, so do not duplicate them here.

## What this repo is
Two separate projects around the World Bank **Climate Policy Assessment Tool (CPAT)**: **Excel-AI** (`excel_ai/`, Excel prototypes replicating and extending the legacy model) and **Coded CPAT** (`coded/`, a Python reimplementation). Who reads what: [`README.md`](README.md).

## Bugs and issues: what to replicate
**Never replicate a legacy bug; always replicate a legacy issue, and track it.** Data problems are issues (Very high where a legacy bug with a cell plan covers them, Extremely high where the prototype aligns with legacy). Read [`excel_ai/BUGS.md`](excel_ai/BUGS.md) and [`excel_ai/ISSUES.md`](excel_ai/ISSUES.md) first; the master list is the tracker `excel_ai/Tracking_Legacy_Bugs_v<version>.xlsx`. The full rule, the codes (L, M, I, LD, U) and where each is kept: [`NORMS.md`](NORMS.md) section 0.

## Read before you start
1. [`README.md`](README.md) - who reads what, repo map.
2. [`NORMS.md`](NORMS.md) - rules for every task: task completion and caveats log (section 6), method vs version notes (section 7).
3. The project's own documents:
   - Excel: [`excel_ai/README.md`](excel_ai/README.md), [`NORMS.md`](NORMS.md) (columns, visual style guide, formulas, MTInputs, versioning), [`excel_ai/plans/TODO.md`](excel_ai/plans/TODO.md).
   - Python: [`coded/README.md`](coded/README.md), [`coded/TODO.md`](coded/TODO.md).
4. [`CAVEATS.md`](CAVEATS.md) - log of completed tasks and their caveats. Read before building on earlier work.

## Hard rules (summary; authority is the documents above)
- All data live in the root folder `data/`, in subfolders, with the scripts that convert them; new data go there too (`NORMS.md` section 8, `data/README.md`).
- The legacy workbook in `excel_ai/legacy/workbooks/` is read-only ground truth; the `CPAT_LegacyData_dummy*` files in `data/legacy_dummy/` are generated and must agree with `data/dummy/` (`NORMS.md` section 8).
- Never edit a released workbook in place; build the next version. Main files are named `<Name>_v<version>` at the top of `excel_ai/`, older versions in `excel_ai/releases/`, and `excel_ai/permalink/` holds only the files others link to (`NORMS.md` section 5a). Inputs: legacy MTInputs rows and `NameOfParameter` names, the same in Excel and Python (`NORMS.md` section 4).
- Every finished task ends with a new entry at the bottom of `CAVEATS.md`, plus the bookkeeping in `NORMS.md` section 6. Earlier entries may be corrected (stale paths, resolved caveats) but not deleted.
- Final methodology and version notes are always different documents (`NORMS.md` section 7). A methodology describes the current method only: no change history, no version log, no before/after columns.
- Do not commit unless the user asks.
- The Excel builders (mitigation, distribution, air pollution) write with openpyxl and recalculate in LibreOffice, so they run on Linux and in cloud sessions (see each folder's README). Excel COM appears only in the optional Excel-open test of `check_quick.py` (skipped without Excel); the Excel 365 review is the user's.

## Keeping this file useful
Add new generic, tool-agnostic guidance to the documents above (or here, if it is routing only). Tool-specific files (`CLAUDE.md` etc.) must stay thin pointers to this file.
