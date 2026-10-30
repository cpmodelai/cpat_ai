# AGENTS.md - instructions for any AI working on Excel-AI

Tool-neutral (Claude, Codex, Gemini, Copilot, Cursor, ...). The repository's entry point is [`../../AGENTS.md`](../../AGENTS.md); `CLAUDE.md` here points to this file. This file only routes you to the documents in `excel_ai/core/` (this folder: the rules, records and plans of Excel-AI); the rules live there, so do not duplicate them here.

## What Excel-AI is
The Excel prototypes replicating and extending legacy CPAT: modules `../mitigation/`, `../distribution/`, `../air_pollution/` (each with its builder, `checks/`, `docs/` and `releases/`), the permalinked workbooks in `../active_workbooks/`, the legacy bug register in `../legacy/`. Map: [`../README.md`](../README.md).

## Bugs and issues: what to replicate
**Never replicate a legacy bug; always replicate a legacy issue, and track it.** Data problems are issues (Very high where a legacy bug with a cell plan covers them, Extremely high where the prototype aligns with legacy). Read [`BUGS.md`](BUGS.md) and [`ISSUES.md`](ISSUES.md) first; the master list is the tracker `excel_ai/Tracking_Legacy_Bugs_v<version>.xlsx`. The full rule, the codes (L, M, DOC, I, LD, U) and where each is kept: [`NORMS.md`](NORMS.md) section 0. **Prototype bugs (`M`) are never put into Coded CPAT**: Python writes the correct formula and the prototype is fixed to align ([`NORMS.md`](NORMS.md) section 0 rule 6, [`coded/NORMS.md`](../../coded/NORMS.md) 0.3).

## Read before you start
1. [`../README.md`](../README.md) - the map of `excel_ai/`.
2. [`NORMS.md`](NORMS.md) - rules for every task: task completion and caveats log (section 6), method vs version notes (section 7), data (section 8).
3. [`TODO.md`](TODO.md) - the one list of open work; open plans in [`plans/`](plans/); module prompts in [`prompts/`](prompts/README.md).
4. [`CAVEATS.md`](CAVEATS.md) - log of completed tasks and their caveats. Read before building on earlier work.
5. The module's own README (`../mitigation/README.md`, ...); Python: [`coded/README.md`](../../coded/README.md); data: [`data/README.md`](../../data/README.md).

## Hard rules (summary; authority is the documents above)
- All data live in the root folder `data/`, as editions (`data/editions.csv`; `data/Public01/` here): in each, `tidy/` is the source of truth, `legacy_xlsx/` is written from it, `data_sources.csv` tags every table (proprietary or not; values public, perturbed or derived-real). Six tables are proprietary; this repository holds them perturbed, never real (`NORMS.md` section 8, `data/README.md`).
- The legacy workbook `data/legacy/CPAT 1.0pre_465_Shell.xlsb` (the only reference copy; its six proprietary tabs empty) is read-only ground truth; each edition holds it filled with its own data (`NORMS.md` section 8).
- Never edit a released workbook in place; build the next version. Every version of a module workbook is in the module's `releases/` (`<Name>_v<version>`), the permalinked copy in `excel_ai/active_workbooks/` (`<Name>_latest`); the documents people read (bug book, tracker, codes map, deck) keep their current version at the top of `excel_ai/` (`NORMS.md` section 5a; `core/tools/release.py`). Inputs: legacy MTInputs rows and `NameOfParameter` names, the same in Excel and Python (`NORMS.md` section 4).
- Every Excel-AI script starts by importing `core/tools/xlpaths.py` (four lines that walk up to `excel_ai/`), which puts every code folder and `data/scripts/` on the path.
- Every finished task ends with a new entry at the bottom of `CAVEATS.md`, plus the bookkeeping in `NORMS.md` section 6. Earlier entries may be corrected (stale paths, resolved caveats) but not deleted.
- Final methodology and version notes are always different documents (`NORMS.md` section 7). A methodology describes the current method only: no change history, no version log, no before/after columns.
- Do not commit unless the user asks.
- The Excel builders (mitigation, distribution, air pollution) write with openpyxl and recalculate in LibreOffice, so they run on Linux and in cloud sessions (see each folder's README). Excel COM appears only in the optional Excel-open test of `check_quick.py` (skipped without Excel); the Excel 365 review is the user's.

## Keeping this file useful
Add new generic, tool-agnostic guidance to the documents above (or here, if it is routing only). Tool-specific files (`CLAUDE.md` etc.) must stay thin pointers to this file.
