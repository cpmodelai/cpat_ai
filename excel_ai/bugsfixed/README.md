# Legacy CPAT 1.0pre_465: the CPAT team's bug fixes, checked

`CPAT 1.0pre_465 - No Prop Data.xlsb` is the latest legacy file from the CPAT team (2026-10-22; the same file as in `../legacy/workbooks/`). The team marked 62 of our legacy bugs (and the prototype issues I18, I29) as fixed. Each fix was checked cell by cell against the bug's cell plan (baseline cell, filled range, policy copy) on 2026-10-22.

| File | What it is |
|---|---|
| `FixedBugsToConfirm.txt` | The team's list, split into **Confirmed fixed** (52) and **Fixed with caveats** (12: 8 bugs with caveats, L62 and L63 not fixed, and the prototype issues I18 and I29), with the caveat of each |
| `legacy465_check.json` | The same result for code: read by the register (`../mitigation/make_bugfix_book.py`), the lists and the tracker |
| `CPAT 1.0pre_465 - No Prop Data.xlsb` | The legacy file checked |

Where the result shows (v8.2):

- **Bug-fix register** `../CPAT-AI_BugsAndIssues_latest.docx`: every bug says its status in legacy; the confirmed fixes are in Appendix C, the fixes with caveats in Appendix B (red notes). Every cell reference is a 465 row.
- **Register spreadsheet** `../CPAT-AI_BugsAndIssues_latest.xlsx`, `../BUGS.md`, `../mitigation/LegacyBugFixes.md`: column "Status in legacy 465" / "In legacy 465".
- **The CPAT team's tracker** `../legacy/workbooks/Tracking issues.xlsx`: tab BUGS, column B "Status in legacy" (Closed rows struck through, filtered to Open).

The hand-edited copy of the register made on 2026-10-22 (`CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.5_fixedbugs.docx`) and the interim spreadsheet (`CPAT-AI_BugsAndIssues_interim_fixedbugs.xlsx`) were retired in v8.2: the regenerated register and register spreadsheet carry the same content (git history keeps both files).
